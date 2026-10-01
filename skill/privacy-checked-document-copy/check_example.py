#!/usr/bin/env python3
"""Read-only checks for this fictional text fixture; not a document sanitizer."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_HASH = "af698c7c2514a5dc3aa9964af3b293d9ca531913fffde8bc086b578e4f235b58"
AUDIENCE = "Taylor Reed, venue coordinator, taylor@venue.example"
APPROVED = b"""Workshop venue brief

Event: Printmaking meetup
Date: 2026-11-07
Time: 10:00-12:00
Attendance: 12 adults
Room: Studio B
Constraint: Use a water-cleanup area.
"""


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(source, output, record):
    require(sha256(source).hexdigest() == SOURCE_HASH, "source differs from frozen input")
    require(record["source"]["sha256"] == SOURCE_HASH, "source record mismatch")
    require(record["source"]["preserved"] is True, "source preservation missing")
    require(record["source"]["file"] == "source.md", "wrong source identity")
    require(record["output"]["file"] == "venue-copy.txt", "wrong output identity")
    require(output == APPROVED, "output differs from approved bytes")
    source_lines = source.decode("utf-8").splitlines()
    rebuilt = (source_lines[4][2:] + "\n\n" + "\n".join(source_lines[7:13]) + "\n").encode()
    require(rebuilt == output, "retained source content or qualification changed")
    require(record["output"]["sha256"] == sha256(output).hexdigest(), "output hash mismatch")
    require(record["output"]["bytes"] == len(output), "output size mismatch")
    require(record["audience"] == AUDIENCE, "audience changed")
    require(record["release"] == "prepared_only" and record["shared"] is False,
            "unsupported release claim")
    require(record["verification"]["scope"] == "text bytes only", "overbroad check scope")
    require({row["category"] for row in record["removed"]} == {
        "frontmatter", "personal contacts", "internal planning", "HTML comment", "link and target"
    }, "removal categories incomplete")
    surfaces = {row["surface"]: row["state"] for row in record["surfaces"]}
    require(surfaces.get("complete output bytes") == "checked", "output bytes not checked")
    require(surfaces.get("filesystem attributes and provider history") == "uninspected",
            "uninspected surface was claimed checked")
    require(len(record["holds"]) == 2, "release limits missing")


def main():
    before = {name: (ROOT / name).read_bytes() for name in (
        "source.md", "venue-copy.txt", "review-record.json")}
    source, output = before["source.md"], before["venue-copy.txt"]
    record = json.loads(before["review-record.json"])
    check(source, output, record)
    print("PASS: exact saved copy, original fingerprint, retained facts, record and release boundary")

    cases = []
    for label, changed in (
        ("comment leak", output + b"<!-- internal review -->\n"),
        ("link-target leak", output + b"[notes](https://organizer.example/notes)\n"),
        ("lost constraint", output.replace(b"Constraint: Use a water-cleanup area.\n", b"")),
        ("changed attendance", output.replace(b"12 adults", b"120 adults")),
        ("invisible character", output + "\u200b".encode("utf-8")),
    ):
        revised = deepcopy(record)
        revised["output"].update(sha256=sha256(changed).hexdigest(), bytes=len(changed))
        cases.append((label, source, changed, revised))
    cases.append(("source drift", source + b"\nNew internal note\n", output, record))
    revised = deepcopy(record)
    revised["output"]["sha256"] = "0" * 64
    cases.append(("wrong final hash", source, output, revised))
    revised = deepcopy(record)
    revised["surfaces"][0]["state"] = "uninspected"
    cases.append(("unknown output surface", source, output, revised))
    revised = deepcopy(record)
    revised.update(release="sent", shared=True)
    cases.append(("unauthorized release claim", source, output, revised))
    for label, candidate_source, candidate_output, candidate_record in cases:
        try:
            check(candidate_source, candidate_output, candidate_record)
        except ValueError:
            print(f"PASS: rejected {label}")
        else:
            raise ValueError(f"negative case incorrectly passed: {label}")
    require(all((ROOT / name).read_bytes() == data for name, data in before.items()),
            "the check modified a fixture file")
    print(f"PASS: {len(cases)} negative cases; all saved fixtures unchanged")
    print("LIMIT: text bytes only; no PDF, Office, image or provider-history verification")


if __name__ == "__main__":
    main()
