#!/usr/bin/env python3
"""Reproduce one fictional flat-schema packet. No collection, network or upload."""
import argparse
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path
import re
import tempfile

ROOT = Path(__file__).resolve().parent
SOURCE = "originals/diagnostics.jsonl"
SOURCE_HASH = "75ab81aae71f8a336a4e0f4b4ac5f0483ccf439a9b75117a2513c77bf3d9b3c9"
POLICY_HASH = "26a58115fec53310e744422e1b46ca4cf4399f4abc87a8d51b5de9248c891c07"
MEMBERS = {"events.jsonl", "summary.txt"}
ENUMS = {"severity", "component", "event", "code"}
ALIASES = {"operation_id": "OP", "device_id": "DEV"}
INTEGERS = {"attempt", "elapsed_ms", "bytes_sent"}
FIELDS = ENUMS | set(ALIASES) | INTEGERS | {"event_at"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return sha256(data).hexdigest()


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key " + json.dumps(key, ensure_ascii=True))
        result[key] = value
    return result


def decode(data):
    def bad_constant(_):
        raise ValueError("non-finite JSON value")
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique,
                      parse_constant=bad_constant)


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, indent=2) + "\n").encode()


def utc(value):
    require(type(value) is str and re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z", value), "unsupported UTC timestamp")
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")


def policy_check(p):
    require(type(p) is dict and set(p) == {
        "schema", "audience", "purpose", "source_files", "row_handling",
        "unlisted_top_level", "release", "packet_files", "fields"
    }, "unsupported policy shape")
    fixed = {"schema": "support-log-policy-v1",
             "audience": "Fictional RelaySync support team, case DEMO-73",
             "purpose": "Review the observed sync sequence and incomplete outcome",
             "source_files": [SOURCE], "row_handling": "retain_every_object_in_source_order",
             "unlisted_top_level": "omit_and_record", "release": "prepare_only",
             "packet_files": ["events.jsonl", "summary.txt"]}
    require(all(p[k] == v for k, v in fixed.items()), "unsupported policy control value")
    require(type(p["fields"]) is dict and set(p["fields"]) == FIELDS,
            "unsupported field rule or omitted required rule")
    for field, rule in p["fields"].items():
        require(type(rule) is dict, f"{field}: rule is not an object")
        if field in ENUMS:
            require(set(rule) == {"type", "allow_missing", "values"} and
                    rule["type"] == "enum" and rule["allow_missing"] is False,
                    f"{field}: unsupported enum rule")
            values = rule["values"]
            require(type(values) is list and values and all(type(v) is str and
                    re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,47}", v) for v in values),
                    f"{field}: expected explicitly reviewed literal values")
            require(len(set(values)) == len(values), f"{field}: repeated policy value")
        else:
            require(rule.get("allow_missing") is True and rule.get("allow_null") is True,
                    f"{field}: missing/null controls must be explicit booleans")
            common = {"type", "allow_missing", "allow_null"}
            if field in ALIASES:
                require(set(rule) == common | {"prefix"} and rule["type"] == "local_alias"
                        and rule["prefix"] == ALIASES[field], f"{field}: unsupported alias rule")
            elif field in INTEGERS:
                require(set(rule) == common | {"min", "max"} and rule["type"] == "integer"
                        and type(rule["min"]) is int and type(rule["max"]) is int
                        and 0 <= rule["min"] <= rule["max"] <= 1048576,
                        f"{field}: unsupported bounded-integer rule")
            else:
                require(set(rule) == common | {"start", "end"} and rule["type"] == "utc_window",
                        "event_at: unsupported timestamp rule")
                require(utc(rule["start"]) <= utc(rule["end"]), "reversed timestamp window")


def project(source, policy_bytes):
    policy = decode(policy_bytes)
    policy_check(policy)
    lines = source.splitlines()
    require(lines and source.endswith(b"\n"), "nonempty newline-terminated JSONL required")
    aliases = {field: {} for field in ALIASES}
    events, decisions = [], []
    for ordinal, line in enumerate(lines, 1):
        require(line.strip(), f"line {ordinal}: blank line is not an event")
        try:
            row = decode(line)
        except (ValueError, UnicodeError) as error:
            raise ValueError(f"line {ordinal}: invalid JSON ({error})") from error
        require(type(row) is dict, f"line {ordinal}: event must be an object")
        event = {"occurrence": ordinal}
        decision = {"source_locator": f"{SOURCE}:{ordinal}", "packet_occurrence": ordinal,
                    "fields": {}, "omitted_subtrees": []}
        for field, rule in policy["fields"].items():
            locator = f"line {ordinal}/{field}"
            if field not in row:
                require(rule["allow_missing"] is True, f"{locator}: required field absent")
                event[field] = {"state": "absent"}
            elif row[field] is None:
                require(rule.get("allow_null") is True, f"{locator}: null not allowed")
                event[field] = {"state": "explicit_null"}
            else:
                value = row[field]
                if field in ENUMS:
                    require(type(value) is str and value in rule["values"],
                            f"{locator}: unreviewed enum value or type")
                    event[field] = value
                elif field in INTEGERS:
                    require(type(value) is int and rule["min"] <= value <= rule["max"],
                            f"{locator}: unsupported integer value or type")
                    event[field] = {"state": "present", "value": value}
                elif field in ALIASES:
                    require(type(value) is str and 1 <= len(value) <= 128 and
                            all(32 <= ord(c) < 127 for c in value), f"{locator}: unsupported alias input")
                    if value not in aliases[field]:
                        aliases[field][value] = f"{rule['prefix']}-{len(aliases[field]) + 1:03d}"
                    event[field] = {"state": "present", "alias": aliases[field][value]}
                else:
                    try:
                        timestamp = utc(value)
                    except ValueError as error:
                        raise ValueError(f"{locator}: unsupported timestamp value or type") from error
                    require(utc(rule["start"]) <= timestamp <= utc(rule["end"]),
                            f"{locator}: timestamp outside approved window")
                    event[field] = {"state": "present", "utc": value}
            decision["fields"][field] = {"action": rule["type"], "output": field,
                "state": event[field].get("state", "present") if type(event[field]) is dict else "present"}
            if field in ALIASES and event[field].get("state") == "present":
                decision["fields"][field]["alias"] = event[field]["alias"]
        for field in sorted(set(row) - FIELDS):
            escaped = field.replace("~", "~0").replace("/", "~1")
            decision["omitted_subtrees"].append({"pointer": "/" + escaped,
                "action": "omit_complete_subtree", "reason": "unlisted content, no value approval"})
        events.append(event)
        decisions.append(decision)
    packet = {"events.jsonl": b"".join((json.dumps(e, separators=(",", ":")) + "\n").encode()
                                       for e in events), "summary.txt": summary(events, policy)}
    record = {"fixture": "fictional-support-log-v1", "audience": policy["audience"],
              "source": {"file": SOURCE, "sha256": digest(source), "events": len(events), "preserved": True},
              "policy": {"file": "policy.json", "sha256": digest(policy_bytes)},
              "packet": {name: {"bytes": len(data), "sha256": digest(data)} for name, data in packet.items()},
              "decisions": decisions, "scope": "selected local UTF-8 text bytes and packet membership",
              "uninspected": ["filesystem attributes", "transport metadata", "remote access or history",
                              "logs outside the supplied excerpt"],
              "holds": ["No sending or upload authorized", "Real delivery needs destination and metadata checks"],
              "release": "prepared_only", "shared": False}
    return packet, record


def summary(events, policy):
    text = ["RelaySync support excerpt — fictional case DEMO-73", "", "Audience: " + policy["audience"],
            "Purpose: " + policy["purpose"], "", f"Selected excerpt: {len(events)} event occurrences in source order.",
            "Occurrence numbers preserve the supplied order; timestamps have not been used to sort events.", "",
            "Observed sequence:"]
    for e in events:
        op = e["operation_id"].get("alias", e["operation_id"]["state"])
        text.append(f"{e['occurrence']}. {e['severity']} {e['component']}/{e['event']}: {e['code']}; operation {op}")
    errors = [str(e["occurrence"]) for e in events if e["severity"] == "ERROR"]
    text += ["", f"ERROR occurrences: {', '.join(errors) if errors else 'none in this excerpt'}.",
             "Missing timestamp occurrences: " + positions(events, "absent") + ".",
             "Explicit-null timestamp occurrences: " + positions(events, "explicit_null") + "."]
    for previous, current in zip(events, events[1:]):
        a, b = previous["event_at"], current["event_at"]
        if a["state"] == b["state"] == "present" and b["utc"] <= a["utc"]:
            relation = "Equal adjacent timestamps" if a["utc"] == b["utc"] else "Backwards adjacent timestamp"
            text.append(f"{relation}: occurrences {previous['occurrence']} and {current['occurrence']}.")
    text += ["", "Outcome: unknown. No terminal success or terminal failure is present in this selected excerpt.",
             "Pending status, a dispatched retry, absent counters and zero sent bytes do not establish completion.",
             "The timestamp anomalies do not establish a causal order or a clock-corrected duration.",
             "No continuation, server-side trace or cause of the interruption was supplied.", "",
             "Reading the event file:",
             "Each optional field has a state: present, absent, or explicit_null. Integers keep their original units:",
             "attempt is a count; elapsed_ms is milliseconds; bytes_sent is bytes.",
             "OP and DEV aliases preserve only approved within-excerpt equality, separately by identifier field.",
             "An absent or null identifier is not attributed to an earlier alias. Aliases are not cross-packet IDs.", "",
             "Limit: all free-text messages and unlisted nested context were omitted by the supplied audience policy.",
             "Those omissions can remove explanatory detail; the retained codes alone do not prove root cause.",
             "Preparation only. The recipient packet contains events.jsonl and summary.txt; nothing was sent."]
    return ("\n".join(text) + "\n").encode("utf-8")


def positions(events, state):
    return ", ".join(str(e["occurrence"]) for e in events if e["event_at"]["state"] == state) or "none"


def input_bytes():
    for path in (ROOT / SOURCE, ROOT / "policy.json"):
        require(not path.is_symlink() and path.is_file(), "input must be a regular fixture file")
    return (ROOT / SOURCE).read_bytes(), (ROOT / "policy.json").read_bytes()


def build(out, source, policy):
    packet, record = project(source, policy)
    # mkdir and exclusive writes refuse existing destinations, including symlinks.
    require(not any(p.is_symlink() for p in [out] + list(out.parents)), "symlink destination is unsupported")
    out.mkdir()
    (out / "recipient").mkdir()
    (out / "private").mkdir()
    for name, data in packet.items():
        with (out / "recipient" / name).open("xb") as target:
            target.write(data)
    with (out / "private/review-record.json").open("xb") as target:
        target.write(encoded(record))


def packet_read(folder):
    require(folder.is_dir() and not folder.is_symlink(), "packet directory missing or symlinked")
    paths = list(folder.rglob("*"))
    require(all(p.is_file() and not p.is_symlink() for p in paths), "unexpected directory or symlink")
    require({p.relative_to(folder).as_posix() for p in paths} == MEMBERS, "packet membership mismatch")
    return {p.name: p.read_bytes() for p in paths}


def verify(source, policy, packet, record):
    require(digest(source) == SOURCE_HASH and digest(policy) == POLICY_HASH, "frozen source/policy drift")
    expected, expected_record = project(source, policy)
    require(set(packet) == MEMBERS and packet == expected, "packet differs from approved source projection")
    require(record == expected_record, "review record differs from source-to-output evidence")
    # Independent fixture expectations guard occurrence loss, false completion and correlation changes.
    events = [decode(line) for line in packet["events.jsonl"].splitlines()]
    require(len(events) == 9 and [e["occurrence"] for e in events] == list(range(1, 10)), "occurrence loss")
    require([e["code"] for e in events if e["severity"] == "ERROR"] ==
            ["E_TIMEOUT", "E_UNREACHABLE", "E_REMOTE_BUSY"], "error meaning changed")
    require([e["occurrence"] for e in events if e["operation_id"].get("alias") == "OP-001"] ==
            [2, 3, 4, 7, 8, 9], "correlation changed")
    require(events[5]["event_at"]["state"] == "explicit_null" and
            events[6]["event_at"]["state"] == "absent", "unknown evidence collapsed")
    require(events[1]["bytes_sent"] == {"state": "present", "value": 0} and
            events[7]["bytes_sent"] == {"state": "absent"}, "missing counter became zero")


def negatives(source, policy_bytes, packet, record):
    count = 0
    def rejected(label, action):
        nonlocal count
        try:
            action()
        except (ValueError, OSError, UnicodeError):
            count += 1
            print("PASS: rejected " + label)
        else:
            raise ValueError("negative case passed: " + label)

    for label, field, value in [("nested code", "code", {"text": "E_TIMEOUT"}),
            ("unreviewed code", "code", "E_UNREVIEWED"), ("free text in enum", "component", "private note"),
            ("boolean counter", "attempt", True), ("string counter", "attempt", "1"),
            ("out-of-range counter", "attempt", 999), ("nested alias input", "device_id", {"id": "demo"}),
            ("control character alias", "device_id", "demo\nnext"), ("out-of-window timestamp", "event_at", "2026-10-01T00:00:00.000Z")]:
        rows = source.splitlines()
        row = decode(rows[2]); row[field] = value
        rows[2] = json.dumps(row).encode()
        rejected(label, lambda: project(b"\n".join(rows) + b"\n", policy_bytes))
    rejected("duplicate diagnostic code key", lambda: project(source.replace(b'"code":"E_TIMEOUT"',
             b'"code":"C_READY","code":"E_TIMEOUT"', 1), policy_bytes))
    rejected("malformed JSON line", lambda: project(source.replace(b'"code":"E_TIMEOUT"',
             b'"code":', 1), policy_bytes))
    rejected("non-object event", lambda: project(b"[]\n", policy_bytes))
    rejected("non-finite nested JSON", lambda: project(source.replace(b'"retry_after":null',
             b'"retry_after":NaN'), policy_bytes))
    rejected("blank event line", lambda: project(source + b"\n", policy_bytes))
    for label, mutate in [("unknown policy control", lambda p: p.update(release="send")),
            ("unknown policy key", lambda p: p.update(copy_nested=True)),
            ("extra free-text field rule", lambda p: p["fields"].update(message={"type": "text"})),
            ("integer instead of boolean control", lambda p: p["fields"]["attempt"].update(allow_null=1)),
            ("unsupported nested rule", lambda p: p["fields"]["code"].update(nested=True)),
            ("expanded source selection", lambda p: p["source_files"].append("other.jsonl"))]:
        changed = decode(policy_bytes); mutate(changed)
        rejected(label, lambda: project(source, encoded(changed)))
    # Repeated event objects are occurrences, not duplicates to discard.
    repeated, _ = project(source + source.splitlines()[2] + b"\n", policy_bytes)
    repeated_rows = [decode(line) for line in repeated["events.jsonl"].splitlines()]
    require(len(repeated_rows) == 10 and repeated_rows[-1]["code"] == "E_TIMEOUT"
            and repeated_rows[-1]["operation_id"]["alias"] == "OP-001", "repeated occurrence lost")
    print("PASS: repeated event retained as a new occurrence with consistent alias")
    for label, change in [("lost error occurrence", lambda lines: lines[:2] + lines[3:]),
            ("reordered occurrences", lambda lines: [lines[1], lines[0]] + lines[2:]),
            ("extra free-text output", lambda lines: lines + [b'{"message":"unreviewed"}'])]:
        changed = dict(packet); changed["events.jsonl"] = b"\n".join(change(packet["events.jsonl"].splitlines())) + b"\n"
        forged = deepcopy(record)
        forged["packet"]["events.jsonl"] = {"bytes": len(changed["events.jsonl"]), "sha256": digest(changed["events.jsonl"])}
        rejected(label + " with updated hash", lambda: verify(source, policy_bytes, changed, forged))
    forged = deepcopy(record); forged.update(release="sent", shared=True)
    rejected("unsupported release claim", lambda: verify(source, policy_bytes, packet, forged))
    changed = dict(packet); changed["summary.txt"] += b"Outcome: successful.\n"
    rejected("invented successful outcome", lambda: verify(source, policy_bytes, changed, record))
    rejected("source drift", lambda: verify(source + b" ", policy_bytes, packet, record))
    with tempfile.TemporaryDirectory(prefix=".packet-check-", dir=ROOT) as temporary:
        out = Path(temporary) / "copy"
        build(out, source, policy_bytes)
        before = {p.relative_to(out): p.read_bytes() for p in out.rglob("*") if p.is_file()}
        rejected("clobber existing output", lambda: build(out, source, policy_bytes))
        require(before == {p.relative_to(out): p.read_bytes() for p in out.rglob("*") if p.is_file()}, "clobber changed bytes")
        recipient = out / "recipient"
        (recipient / "original.jsonl").write_bytes(source)
        rejected("extra packet file", lambda: packet_read(recipient))
        (recipient / "original.jsonl").unlink()
        (recipient / "nested").mkdir()
        rejected("extra empty directory", lambda: packet_read(recipient))
        (recipient / "nested").rmdir()
        (recipient / "events.jsonl").unlink()
        (recipient / "events.jsonl").symlink_to(out / "private/review-record.json")
        rejected("symlink packet member", lambda: packet_read(recipient))
        rejected("symlink build destination", lambda: build(recipient / "events.jsonl", source, policy_bytes))
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["build", "check"])
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    require(args.action != "build" or args.out is not None, "build requires a new --out destination")
    out = args.out if args.out is not None else ROOT / "example-output"
    source, policy = input_bytes()
    if args.action == "build":
        require(digest(source) == SOURCE_HASH and digest(policy) == POLICY_HASH, "frozen fixture input drift")
        build(out, source, policy)
    packet = packet_read(out / "recipient")
    record_path = out / "private/review-record.json"
    require(not record_path.is_symlink(), "review record must not be a symlink")
    record_bytes = record_path.read_bytes()
    verify(source, policy, packet, decode(record_bytes))
    print("PASS: 9 source-ordered occurrences, 3 errors, exact codes, counters, timestamp states and aliases")
    print("PASS: approved packet membership, complete source/policy/output hashes and separate locator record")
    if args.action == "check":
        count = negatives(source, policy, packet, decode(record_bytes))
        require(packet_read(out / "recipient") == packet and record_path.read_bytes() == record_bytes,
                "check changed saved output")
        print(f"PASS: {count} negative cases; saved packet and review record unchanged")
    require(input_bytes() == (source, policy), "source or policy changed during run")
    print("PASS: original and policy bytes unchanged; preparation only, no network or upload")
    print("LIMIT: this fictional flat-schema excerpt only; metadata outside the bytes and remote access uninspected")


if __name__ == "__main__":
    main()
