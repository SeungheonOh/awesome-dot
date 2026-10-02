#!/usr/bin/env python3
"""Reproduce the small Cedar fixture packet; not an arbitrary inbox exporter.

Only the declared five-source, CRLF, ASCII-wire example is supported. Filenames
are metadata. Every output name comes from a checked local occurrence identity.
"""
import argparse
import base64
import binascii
import hashlib
import json
import quopri
import re
from email import policy
from email.parser import BytesParser
from pathlib import Path


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data):
    with path.open("xb") as stream:
        stream.write(data)


def defects(part):
    found = [type(x).__name__ for x in part.defects]
    for _, header in part.items():
        found.extend(type(x).__name__ for x in getattr(header, "defects", ()))
    return found


def decode_leaf(part, wire):
    encoding = str(part.get("Content-Transfer-Encoding", "7bit")).strip().lower()
    if encoding == "base64":
        # email's decoder can recover malformed input; this example holds it.
        direct = base64.b64decode(re.sub(rb"[ \t\r\n]", b"", wire), validate=True)
    elif encoding == "quoted-printable":
        if re.search(rb"=(?![0-9A-Fa-f]{2}|\r\n)", wire):
            raise ValueError("malformed quoted-printable escape")
        direct = quopri.decodestring(wire)
    elif encoding == "7bit":
        if any(byte > 127 for byte in wire):
            raise ValueError("non-ASCII bytes under 7bit")
        direct = wire
    else:
        raise NotImplementedError(f"unsupported transfer encoding: {encoding}")
    parsed = part.get_payload(decode=True)
    if not isinstance(parsed, bytes) or parsed != direct or defects(part):
        raise ValueError("decoder disagreement or parser defect")
    return direct


def inspect_source(raw, source_id):
    """Pair a parser tree with exact fixture wire spans; never serialize it."""
    if len(raw) > 65536 or b"\n" in raw.replace(b"\r\n", b""):
        raise ValueError("fixture requires at most 64 KiB and CRLF wire lines")
    message = BytesParser(policy=policy.default).parsebytes(raw)
    records, decoded = [], {}

    def visit(part, start, end, path, body_context=False, related=False, depth=0):
        if depth > 6 or len(records) >= 40:
            raise ValueError("fixture part/depth bound exceeded")
        separator = raw.find(b"\r\n\r\n", start, end)
        if separator < 0:
            raise ValueError("part header separator unavailable")
        payload_start = separator + 4
        locator = f"{source_id}:{path}"
        content_type = part.get_content_type()
        record = {
            "occurrence": locator, "source": source_id, "part": path,
            "content_type": content_type, "disposition": part.get_content_disposition(),
            "filename_display": part.get_filename(),
            "content_id": str(part.get("Content-ID", "")) or None,
            "transfer_encoding": str(part.get("Content-Transfer-Encoding", "7bit")),
            "wire_range": [start, end], "header_range": [start, separator],
            "payload_range": [payload_start, end],
            "raw_headers_latin1": raw[start:separator].decode("latin-1"),
            "defects": defects(part), "status": "unclassified"
        }
        records.append(record)
        if record["defects"]:
            record.update(status="held_malformed", reason="Parser or header defect; subtree not released.")
            return
        if content_type in {"multipart/signed", "multipart/encrypted", "application/pkcs7-mime", "application/x-pkcs7-mime"}:
            record.update(status="held_protected", reason="Protected entity preserved only; no signature validation or decryption.")
            return
        if content_type == "message/rfc822":
            record.update(status="excluded_nested_message", reason="Attached-message contents are outside the requested selection.")
            return
        if part.is_multipart():
            if content_type not in {"multipart/mixed", "multipart/alternative", "multipart/related"}:
                record.update(status="held_unsupported", reason="Container outside this fixture adapter.")
                return
            boundary = part.get_boundary()
            if not boundary or not boundary.isascii():
                raise ValueError("fixture boundary unavailable")
            pattern = re.compile(rb"(?m)^--" + re.escape(boundary.encode("ascii")) + rb"(--)?[ \t]*\r\n")
            markers = list(pattern.finditer(raw, payload_start, end))
            children = list(part.iter_parts())
            if len(markers) != len(children) + 1 or not markers[-1].group(1) or any(m.group(1) for m in markers[:-1]):
                raise ValueError("wire delimiters disagree with parser tree")
            record.update(status="container", reason="Structural MIME container, not an attachment selection.")
            for number, child in enumerate(children, 1):
                child_start, child_end = markers[number - 1].end(), markers[number].start() - 2
                if raw[child_end:child_end + 2] != b"\r\n":
                    raise ValueError("fixture delimiter CRLF unavailable")
                child_path = str(number) if path == "root" else f"{path}.{number}"
                visit(child, child_start, child_end, child_path,
                      body_context or content_type == "multipart/alternative",
                      related or content_type == "multipart/related", depth + 1)
            return
        if related:
            record.update(status="excluded_related", reason="Body-associated resource, outside explicit attachment selection.")
            return
        if body_context or part.get_content_disposition() != "attachment":
            record.update(status="excluded_body", reason="Message body or body alternative, not a requested attachment.")
            return
        if content_type != "text/plain":
            record.update(status="held_unsupported", reason="Only plain-text attachments are supported by this fixture adapter.")
            return
        try:
            data = decode_leaf(part, raw[payload_start:end])
        except NotImplementedError as error:
            record.update(status="held_unsupported", reason=str(error))
            return
        except (ValueError, binascii.Error) as error:
            record.update(status="held_malformed", reason=str(error))
            return
        record.update(status="available_attachment", decoded_bytes=len(data), decoded_sha256=digest(data))
        decoded[locator] = data

    visit(message, 0, len(raw), "root")
    return message, records, decoded


def build(fixtures, out):
    plan = json.loads((fixtures / "selection.json").read_text(encoding="utf-8"))
    if plan.get("schema") != "cedar-attachment-example-v1" or len(plan["sources"]) != 5:
        raise ValueError("unsupported fixture layout")
    sources, all_records, payloads, originals = [], [], {}, {}
    for number, source in enumerate(plan["sources"], 1):
        source_id, filename = f"s{number:03}", f"message-{number:03}.eml"
        if source["id"] != source_id or source["file"] != filename:
            raise ValueError("unexpected fixture source identity")
        path = fixtures / "messages" / filename
        if path.is_symlink() or not path.is_file():
            raise ValueError("fixture source must be a regular file")
        raw = path.read_bytes()
        message, records, decoded = inspect_source(raw, source_id)
        originals[source_id] = raw
        sources.append({"source": source_id, "supplied_file": filename, "bytes": len(raw),
                        "sha256": digest(raw), "reviewed_sha256": source["sha256"],
                        "matches_reviewed_source": digest(raw) == source["sha256"],
                        "message_id_display": str(message.get("Message-ID", "")),
                        "from_display": str(message.get("From", "")), "date_display": str(message.get("Date", "")),
                        "saved_original": f"originals/{source_id}.eml"})
        all_records.extend(records)
        payloads.update(decoded)
    by_source = {source["source"]: source for source in sources}
    by_occurrence = {record["occurrence"]: record for record in all_records}
    unresolved = []
    for item in plan["unresolved"]:
        current = dict(item)
        evidence_sources = item["evidence_sources"]
        stale = [source for source in evidence_sources if not by_source[source]["matches_reviewed_source"]]
        current["evidence_fresh"] = not stale
        if stale:
            current["previously_reviewed_reason"] = item["reason"]
            current["reason"] = "Previous selection evidence has changed in " + ", ".join(stale) + "; the earlier explanation is not a current claim."
            current["needed"] = "Reinspect the changed supplied evidence and refresh the reviewed selection before deciding this item."
        unresolved.append(current)
    pending = {occurrence for item in plan["unresolved"] for occurrence in item["candidates"]}
    selected_keys, selected = set(), []
    for decision in plan["selected"]:
        key = f'{decision["source"]}:{decision["part"]}'
        if key in selected_keys or key not in by_occurrence:
            raise ValueError("duplicate or absent planned occurrence")
        selected_keys.add(key)
        record = by_occurrence[key]
        evidence_keys = [f'{x["source"]}:{x["part"]}' for x in decision["evidence"]]
        if any(key not in by_occurrence for key in evidence_keys):
            raise ValueError("selection evidence locator unavailable")
        fresh_sources = {decision["source"]} | {x["source"] for x in decision["evidence"]}
        if any(not by_source[x]["matches_reviewed_source"] for x in fresh_sources):
            record.update(status="held_changed_source", reason="Selected source or decision evidence differs from reviewed bytes.")
            continue
        if record["status"] != "available_attachment":
            continue
        if record["decoded_sha256"] != decision["decoded_sha256"]:
            record.update(status="held_changed_payload", reason="Decoded bytes differ from the reviewed selection.")
            continue
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)*", decision["part"]):
            raise ValueError("unexpected fixture part identity")
        output = f'files/{decision["source"]}-part-{decision["part"].replace(".", "-")}.txt'
        record.update(status="selected", output=output, role=decision["role"], selection_reason=decision["reason"], decision_evidence=evidence_keys)
        selected.append(record)
    for record in all_records:
        if record["status"] == "available_attachment":
            status = "held_unresolved_selection" if record["occurrence"] in pending else "excluded_not_selected"
            reason = "No final revision choice is supported." if record["occurrence"] in pending else "Outside the reviewed selection; earlier route note is superseded by s002:1 and s004:1."
            if not by_source[record["source"]]["matches_reviewed_source"]:
                status, reason = "held_changed_source", "Candidate source differs from reviewed bytes; its prior selection rationale needs review."
            elif record["occurrence"] == "s001:2" and any(not by_source[source]["matches_reviewed_source"] for source in ("s002", "s004")):
                reason = "Outside the reviewed selection; previous supersession evidence has changed and needs review."
            record.update(status=status, reason=reason)
    # Inspect everything before writing. An existing destination is never replaced.
    out.mkdir()
    (out / "originals").mkdir()
    (out / "files").mkdir()
    for source in sources:
        write_new(out / source["saved_original"], originals[source["source"]])
    for record in selected:
        write_new(out / record["output"], payloads[record["occurrence"]])
    saved = []
    for source in sources:
        actual = (out / source["saved_original"]).read_bytes()
        if actual != originals[source["source"]]:
            raise ValueError("saved original differs")
    for record in selected:
        actual = (out / record["output"]).read_bytes()
        if actual != payloads[record["occurrence"]]:
            raise ValueError("saved selected file differs")
        saved.append({"occurrence": record["occurrence"], "output": record["output"], "bytes": len(actual), "sha256": digest(actual)})
    for source in sources:
        if (fixtures / "messages" / source["supplied_file"]).read_bytes() != originals[source["source"]]:
            raise ValueError("source changed during build")
    result = {"schema": "cedar-attachment-packet-v1", "request": plan["request"],
              "scope": "Five supplied message occurrences; top-level attachment selection. No mailbox completeness or sender-authenticity claim.",
              "sources": sources, "parts": all_records, "selected_outputs": saved,
              "unresolved_requests": unresolved,
              "readback": {"originals_match_input": True, "selected_decoded_bytes_match": True, "sources_unchanged": True},
              "limits": ["No nested-message selection", "No decryption or signature validation", "No live mail-client or target-application test"]}
    write_new(out / "index.json", (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
    lines = ["# Cedar attachment packet", "", "This is a partial, usable local packet from five supplied fictional message occurrences.", "",
             f"Selected decoded files: {len(saved)}. Original EML occurrences preserved: {len(sources)}.", "",
             "## Start with these files", ""]
    for record in selected:
        lines.append(f'- [{record["role"]}: {record["occurrence"]}]({record["output"]}) — {record["decoded_bytes"]} bytes; filename metadata is recorded in index.json')
    lines.extend(["", "## Unresolved requests", ""])
    for item in unresolved:
        lines.append(f'- **{item["item"]}:** {item["reason"]} Needed: {item["needed"]}')
    extra_holds = [r for r in all_records if r["status"].startswith("held_") and r["status"] != "held_unresolved_selection"]
    lines.extend(["", "## Other held parts", ""])
    lines.extend(f'- {r["occurrence"]}: {r["status"]}; {r["reason"]}' for r in extra_holds)
    lines.extend(["", "The [index](index.json) maps each selected occurrence to original EML bytes, exact part ranges, encoded headers, decoded hashes and decision evidence. Repeated messages and identical payloads remain distinct occurrences.", "",
                  "Verification covers local parsing, transfer decoding, output readback and original preservation. It does not establish sender authenticity, account completeness, signature validity, successful decryption or compatibility with a live email client.", ""])
    write_new(out / "packet.md", "\n".join(lines).encode("utf-8"))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, default=Path(__file__).resolve().parents[1] / "fixtures")
    parser.add_argument("--out", type=Path, required=True, help="New, absent local directory")
    args = parser.parse_args()
    result = build(args.fixtures, args.out)
    print(json.dumps({"selected_files": len(result["selected_outputs"]), "originals": len(result["sources"]), "unresolved_requests": len(result["unresolved_requests"])}))
