#!/usr/bin/env python3
"""Reproduce/check only the adjacent authored fixtures. No arbitrary repair mode."""

import argparse
import codecs
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import platform
import sys


ROOT = Path(__file__).resolve().parent
FIXTURES = ROOT / "fixtures"
CSV_SETTINGS = dict(delimiter=",", quotechar='"', doublequote=True,
                    escapechar=None, skipinitialspace=False,
                    quoting=csv.QUOTE_MINIMAL, strict=True)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def identity(data):
    return {"size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def load_json(path):
    return json.loads(path.read_bytes().decode("utf-8", "strict"))


def parse_text(text):
    return list(csv.reader(io.StringIO(text, newline=""), **CSV_SETTINGS))


def parse_saved(path):
    with path.open("r", encoding="utf-8", errors="strict", newline="") as stream:
        return list(csv.reader(stream, **CSV_SETTINGS))


def newline_sequence(text):
    return [(i, ord(char)) for i, char in enumerate(text) if char in "\r\n"]


def same_sources(snapshot):
    for name, data in snapshot.items():
        require((FIXTURES / name).read_bytes() == data,
                "Source changed during rehearsal: " + name)


def prepare():
    """Check captured identities and intended fields before creating output."""
    contract = load_json(FIXTURES / "contract.json")
    expected = load_json(FIXTURES / "expected-rows.json")
    source = contract["source"]
    require(contract["fixture_version"] == 1, "Unsupported fixture version")
    require(source["file"] == "catalog-windows1252.csv" and
            source["encoding"] == "cp1252" and source["signature"] == "none" and
            source["export_profile"] == "tiny-catalog-export-v1",
            "This helper supports only the declared fixture export profile")
    require(contract["output"]["encoding"] == "utf-8" and
            contract["output"]["signature"] == "forbidden" and
            contract["output"]["file"] == "catalog-utf8.csv" and
            contract["output"]["expected_rows_file"] == "expected-rows.json" and
            contract["output"]["newline_policy"] == "preserve_all_CR_and_LF" and
            contract["output"]["other_text_changes"] == "none" and
            contract["output"]["allowed_transformations"] ==
            ["strict cp1252 decode", "strict utf-8 encode"],
            "Unsupported fixture output contract")
    require(contract["consumer"] == {
            "name": "Python standard-library csv.reader", "encoding": "utf-8",
            "errors": "strict", "newline": "", **CSV_SETTINGS,
            "quoting": "QUOTE_MINIMAL",
            "field_types": "all strings; no type inference or evaluation"},
            "Unsupported fixture consumer settings")
    require(set(contract["controls"]) == {"ambiguous.csv", "known-lossy-utf8.csv",
            "literal-unicode-utf8.csv"}, "Unsupported fixture control names")
    declarations = {source["file"]: source, **contract["controls"]}
    require(set(declarations) == {"catalog-windows1252.csv", "ambiguous.csv",
            "known-lossy-utf8.csv", "literal-unicode-utf8.csv"},
            "This helper only accepts its four named fixtures")
    control_specs = contract["controls"]
    require(control_specs["ambiguous.csv"]["status"] == "held" and
            "encoding" not in control_specs["ambiguous.csv"] and
            control_specs["known-lossy-utf8.csv"]["status"] == "held" and
            control_specs["known-lossy-utf8.csv"]["encoding"] == "utf-8" and
            control_specs["known-lossy-utf8.csv"]["affected_fields"] ==
            ["0041/name", "0041/title"] and
            control_specs["literal-unicode-utf8.csv"]["status"] == "preserve exactly" and
            control_specs["literal-unicode-utf8.csv"]["encoding"] == "utf-8",
            "Unsupported fixture control declaration")
    snapshot = {name: (FIXTURES / name).read_bytes() for name in declarations}
    for name, declared in declarations.items():
        require(identity(snapshot[name]) == {key: declared[key]
                for key in ("size_bytes", "sha256")},
                "Captured fixture identity mismatch: " + name)
    raw = snapshot[source["file"]]
    text = raw.decode("cp1252", "strict")
    require(text.encode("cp1252", "strict") == raw, "Source roundtrip failed")
    require(parse_text(text) == expected, "Source differs from authored rows")
    sample = source["independent_sample"]
    require(sample["record_id"] == "0007" and sample["field"] == "note" and
            expected[0] == ["record_id", "label", "note", "quantity"] and
            expected[1][0] == sample["record_id"] and
            sum(row[0] == sample["record_id"] for row in expected[1:]) == 1 and
            sample["code_points_at_distinctive_characters"] ==
            ["U+201C", "U+201D", "U+20AC"] and
            expected[1][2] == sample["text"] == "\u201csmall, blue\u201d costs \u20ac5",
            "Known source sample conflicts with interpretation")
    return snapshot, text, expected, contract


def controls(snapshot, contract):
    raw = snapshot["catalog-windows1252.csv"]
    try:
        raw.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        strict_error = {"start": error.start, "end": error.end,
                        "reason": error.reason}
    else:
        raise ValueError("Expected the captured cp1252 source to fail UTF-8")
    lossy = {}
    for mode in ("replace", "ignore"):
        candidate = raw.decode("utf-8", mode)
        require(candidate.encode("utf-8", "strict") != raw,
                "Negative control unexpectedly preserved source bytes")
        require(parse_text(candidate) != parse_text(raw.decode("cp1252", "strict")),
                "Negative control unexpectedly preserved fields")
        lossy[mode] = {"source_bytes_preserved": False,
                       "expected_rows_preserved": False,
                       "status": "rejected; demonstration only, not saved"}

    latin1 = raw.decode("latin-1", "strict")
    require(latin1.encode("latin-1", "strict") == raw, "Latin-1 roundtrip failed")
    latin_note = parse_text(latin1)[1][2]
    require(latin_note == "\u0093small, blue\u0094 costs \u00805" and
            latin_note != contract["source"]["independent_sample"]["text"],
            "Latin-1 control did not contradict the known note")

    ambiguous_raw = snapshot["ambiguous.csv"]
    ambiguous = {}
    for encoding in ("utf-8", "cp1252"):
        decoded = ambiguous_raw.decode(encoding, "strict")
        require(decoded.encode(encoding, "strict") == ambiguous_raw,
                "Ambiguous control roundtrip failed")
        label = parse_text(decoded)[1][1]
        ambiguous[encoding] = {"label": label, "code_points":
                              ["U+%04X" % ord(char) for char in label],
                              "roundtrip": True}
    require(ambiguous["utf-8"]["label"] == "\u00e9" and
            ambiguous["cp1252"]["label"] == "\u00c3\u00a9",
            "Ambiguous fixture no longer demonstrates two interpretations")

    lost_rows = parse_text(snapshot["known-lossy-utf8.csv"].decode("utf-8", "strict"))
    require(lost_rows == [["record_id", "name", "title"], ["0041", "Ren\ufffde", "Caf?"]],
            "Known-lossy fixture changed")
    # Distinct possible predecessors, not authoritative corrections for row 0041.
    name_predecessors = ("Ren\u00e9e", "Ren\u00e8e")
    title_predecessors = ("Caf\u00e9", "Caf\u00e8")
    require(all(value.encode("cp1252", "strict").decode("utf-8", "replace") ==
                lost_rows[1][1] for value in name_predecessors),
            "Replacement-history witness failed")
    require(all(value.encode("ascii", "replace").decode("ascii", "strict") ==
                lost_rows[1][2] for value in title_predecessors),
            "Question-mark-history witness failed")
    return {
        "utf8_strict_source_decode": {"status": "rejected", "error": strict_error},
        "lossy_utf8_decoders": lossy,
        "latin1": {"status": "rejected by independent known text",
                   "roundtrip": True, "note": latin_note},
        "ambiguous": {"status": "held; no recovered file", "candidates": ambiguous},
        "known_lossy": {"status": "held; no guessed correction or recovered file",
                        "strict_utf8_accepts": True,
                        "affected_fields": ["0041/name", "0041/title"],
                        "distinct_predecessors_produce_same_current_fields": True}
    }


def validate_outputs(out, snapshot, text, expected, contract, diagnostics):
    require({p.name for p in out.iterdir()} <=
            {"catalog-utf8.csv", "literal-unicode-preserved.csv", "result.json"},
            "Unexpected file in fixture output directory")
    candidate_path = out / "catalog-utf8.csv"
    saved = candidate_path.read_bytes()
    require(not saved.startswith(codecs.BOM_UTF8), "Output has a forbidden signature")
    reopened = saved.decode("utf-8", "strict")
    require(reopened == text, "Saved candidate changed the character sequence")
    require(newline_sequence(reopened) == newline_sequence(text), "Newlines changed")
    require(reopened.encode("cp1252", "strict") == snapshot["catalog-windows1252.csv"],
            "Saved candidate cannot reproduce the source bytes")
    require(parse_saved(candidate_path) == expected, "Saved CSV rows differ")
    literal_path = out / "literal-unicode-preserved.csv"
    literal = literal_path.read_bytes()
    require(literal == snapshot["literal-unicode-utf8.csv"], "Literal content changed")
    require(not literal.startswith(codecs.BOM_UTF8), "Literal fixture gained a signature")
    require(parse_saved(literal_path) ==
            contract["controls"]["literal-unicode-utf8.csv"]["expected_rows"],
            "Literal Unicode parser result differs")
    same_sources(snapshot)
    return {
        "source": {"file": "catalog-windows1252.csv",
                   **identity(snapshot["catalog-windows1252.csv"]),
                   "bytes_preserved": True, "interpretation": "declared cp1252"},
        "candidate": {"file": "catalog-utf8.csv", **identity(saved),
                      "encoding": "utf-8", "leading_signature": False,
                      "exact_character_readback": True, "source_roundtrip": True,
                      "newline_characters_preserved": True,
                      "crlf_sequences": reopened.count("\r\n"),
                      "csv_header_and_all_records_match": True,
                      "data_record_count": len(expected) - 1,
                      "all_fields_remain_strings": True},
        "controls": diagnostics,
        "literal_unicode": {"file": "literal-unicode-preserved.csv", **identity(literal),
                            "source_bytes_and_parsed_fields_preserved": True,
                            "literal_U_FFFD_and_question_mark_preserved": True,
                            "interior_U_FEFF_preserved": True},
        "scope": "Python csv.reader with explicit UTF-8 strict decoding, newline='', "
                 "comma delimiter, double ASCII quotes, and all-string fields. "
                 "No Excel, service ingestion, visual rendering, or semantic correctness claim."
    }


def run(mode, out):
    snapshot, text, expected, contract = prepare()
    diagnostics = controls(snapshot, contract)
    if mode == "rehearse":
        same_sources(snapshot)
        out.mkdir()  # Atomic refusal if any file, directory or symlink already exists.
        # Binary writes prevent platform newline rewriting. Never modify source files.
        with (out / "catalog-utf8.csv").open("xb") as stream:
            stream.write(text.encode("utf-8", "strict"))
        with (out / "literal-unicode-preserved.csv").open("xb") as stream:
            stream.write(snapshot["literal-unicode-utf8.csv"])
    result = validate_outputs(out, snapshot, text, expected, contract, diagnostics)
    if mode == "rehearse":
        result["run"] = {"python": platform.python_version(), "implementation":
                         platform.python_implementation(), "date_utc":
                         datetime.now(timezone.utc).date().isoformat()}
        with (out / "result.json").open("x", encoding="utf-8", newline="\n") as stream:
            json.dump(result, stream, ensure_ascii=True, indent=2)
            stream.write("\n")
    else:
        recorded = load_json(out / "result.json")
        for key, value in result.items():
            require(recorded.get(key) == value, "Saved result disagrees with recheck: " + key)
    same_sources(snapshot)
    print("PASS: saved bytes and exact csv.reader fields verified; "
          "ambiguous and known-lossy fixtures remain held")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("rehearse", "check"))
    parser.add_argument("output", type=Path, help="new directory for rehearsal; saved directory for check")
    args = parser.parse_args()
    try:
        run(args.mode, args.output)
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print("STOP: " + str(error), file=sys.stderr)
        print("Inputs are never rewritten. Inspect any partial new output before retrying; "
              "this tool does not overwrite or remove it.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
