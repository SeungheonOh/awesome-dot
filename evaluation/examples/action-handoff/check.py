#!/usr/bin/env python3
"""Bounded JSON checks for this authored exercise, not a live evaluation runner."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

MAX_BYTES = 16_384
ASSERTION_IDS = ("json_shape", "agreed_actions", "assigned_fields", "unassigned_fields")
FIELDS = {"source_id", "owner", "due_date"}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"Non-JSON constant: {value}")


def assertion(identifier, passed, evidence, error):
    return {"id": identifier, "status": "passed" if passed else "failed",
            "evidence": evidence, "errors": [] if passed else [error]}


def invalid_artifact(message):
    rows = [assertion("json_shape", False, {}, message)]
    rows.extend({"id": name, "status": "not_assessed", "evidence": {},
                 "errors": ["Blocked by invalid JSON shape"]}
                for name in ASSERTION_IDS[1:])
    return {"status": "failed", "assertions": rows}


def check_bytes(raw):
    """Inspect data only. Order/whitespace are immaterial; no candidate code runs."""
    if len(raw) > MAX_BYTES:
        return invalid_artifact(f"Artifact exceeds {MAX_BYTES} bytes")
    try:
        data = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                          parse_constant=reject_constant)
    except (UnicodeError, ValueError, RecursionError) as error:
        return invalid_artifact(f"Invalid UTF-8 JSON: {error}")
    if not isinstance(data, dict) or set(data) != {"actions"}:
        return invalid_artifact("Expected an object with only an actions key")
    actions = data["actions"]
    if not isinstance(actions, list) or len(actions) > 3:
        return invalid_artifact("actions must be an array of at most three objects")
    for index, row in enumerate(actions):
        if not isinstance(row, dict) or set(row) != FIELDS:
            return invalid_artifact(f"actions[{index}] must have exactly {sorted(FIELDS)}")
        if not isinstance(row["source_id"], str) or any(
                row[key] is not None and not isinstance(row[key], str)
                for key in ("owner", "due_date")):
            return invalid_artifact(f"actions[{index}] has an invalid field type")

    sources = [row["source_id"] for row in actions]
    assigned = [row for row in actions if row["source_id"] == "S1"]
    unassigned = [row for row in actions if row["source_id"] == "S3"]
    rows = [
        assertion("json_shape", True, {"action_count": len(actions)}, ""),
        assertion("agreed_actions", sorted(sources) == ["S1", "S3"],
                  {"source": "task.txt#S1-S3", "observed_source_ids": sources},
                  "Expected S1 and S3 exactly once each; S2 is only a suggestion"),
        assertion("assigned_fields", assigned == [
                      {"source_id": "S1", "owner": "Mira", "due_date": "2026-10-12"}],
                  {"source": "task.txt#S1", "observed": assigned},
                  "S1 must occur once with owner Mira and due_date 2026-10-12"),
        assertion("unassigned_fields", unassigned == [
                      {"source_id": "S3", "owner": None, "due_date": None}],
                  {"source": "task.txt#S3", "observed": unassigned},
                  "S3 must occur once with owner and due_date both null"),
    ]
    return {"status": "passed" if all(row["status"] == "passed" for row in rows)
            else "failed", "assertions": rows}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", type=Path, help="Saved actions.json to inspect")
    args = parser.parse_args(argv)
    try:
        if not args.artifact.is_file():
            raise OSError("Expected a regular artifact file")
        with args.artifact.open("rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
    except OSError as error:
        # Missing collection is not proof that the model omitted its deliverable.
        result = {"status": "not_assessed", "assertions": [],
                  "errors": [f"Artifact could not be read: {error}"]}
        code = 2
    else:
        result = check_bytes(raw)
        code = 0 if result["status"] == "passed" else 1
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
