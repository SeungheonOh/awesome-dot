#!/usr/bin/env python3
"""Fixed external predicate for the original room-slot history example only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


# These are declared before any search. The application contract is half-open
# intervals, irrespective of the caller's legacy-compatibility setting.
CASES = [
    ("touch-after", [[10, 20]], 20, 25, True),
    ("touch-before", [[10, 20]], 5, 10, True),
    ("exact-gap", [[10, 20], [30, 40]], 20, 30, True),
    ("overlap-left", [[10, 20]], 9, 11, False),
    ("overlap-right", [[10, 20]], 19, 21, False),
    ("contained", [[10, 20]], 12, 18, False),
    ("identical", [[10, 20]], 10, 20, False),
    ("empty", [], 20, 25, True),
    ("negative-touch", [[0, 10]], -5, 0, True),
    ("empty-query", [], 10, 10, "ValueError"),
]
MODES = ["standard", "legacy", "standard"]

# The checked-out module is explicitly loaded; no shell or package runner is used.
CHECK = r'''
import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("fixture_slots", "slots.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
if not hasattr(module, "is_available"):
    print(json.dumps({"kind": "unavailable", "reason": "named API is absent"}))
    sys.exit(20)
failures = []
for name, bookings, start, end, expected in json.loads(sys.argv[1]):
    try:
        actual = module.is_available(bookings, start, end)
    except ValueError:
        actual = "ValueError"
    if type(actual) is not type(expected) or actual != expected:
        failures.append({"case": name, "expected": expected, "actual": actual})
print(json.dumps({"kind": "evaluated", "case_count": len(json.loads(sys.argv[1])),
                  "failures": failures}, sort_keys=True))
sys.exit(10 if failures else 0)
'''


def classify(attempts):
    kinds = {attempt["outcome"] for attempt in attempts}
    if "abort" in kinds:
        return 128, "abort"
    if "unavailable" in kinds:
        return 125, "skip-unavailable"
    if kinds == {"good", "bad"}:
        return 125, "skip-unstable-matrix"
    if kinds == {"good"}:
        return 0, "good"
    if kinds == {"bad"}:
        return 1, "bad"
    return 128, "abort"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, required=True)
    parser.add_argument("--label", default="bisect")
    args = parser.parse_args()
    attempts = []
    source = Path("slots.py")
    revision = subprocess.run(["git", "--no-optional-locks", "rev-parse", "HEAD"],
                              text=True, capture_output=True, check=True).stdout.strip()
    # The source fixture and this command are inspected before execution. This is
    # isolation from incidental interpreter settings, not a security sandbox.
    base_env = {"PATH": os.defpath, "LC_ALL": "C", "TZ": "UTC"}
    for mode in MODES:
        env = dict(base_env, BOOKING_POLICY=mode)
        try:
            result = subprocess.run([sys.executable, "-I", "-B", "-c", CHECK,
                                     json.dumps(CASES)], env=env, text=True,
                                    capture_output=True, timeout=5)
            payload = json.loads(result.stdout)
            valid = isinstance(payload, dict)
            if valid and result.returncode == 0 and payload.get("kind") == "evaluated" and payload.get("failures") == []:
                outcome = "good"
            elif valid and result.returncode == 10 and payload.get("kind") == "evaluated" and isinstance(payload.get("failures"), list) and payload["failures"]:
                outcome = "bad"
            elif valid and result.returncode == 20 and payload.get("kind") == "unavailable":
                outcome = "unavailable"
            else:
                outcome = "abort"
            attempts.append({"mode": mode, "outcome": outcome,
                             "child_exit": result.returncode, "result": payload})
        except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as error:
            # Do not pass a signal, timeout, missing executable or runner error
            # through to Git as an ordinary bad commit.
            attempts.append({"mode": mode, "outcome": "abort",
                             "reason": type(error).__name__})
            break
    code, classification = classify(attempts)
    record = {"label": args.label, "revision": revision,
              "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest() if source.is_file() else None,
              "classification": classification, "exit": code, "attempts": attempts}
    with args.record.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")
    print(json.dumps({key: record[key] for key in ("revision", "classification", "exit")}, sort_keys=True))
    return code


if __name__ == "__main__":
    # A fault in this harness aborts the search. A Python traceback normally exits
    # 1, which Git would misinterpret as evidence against the checked-out commit.
    try:
        sys.exit(main())
    except Exception as error:
        print("predicate infrastructure error: " + type(error).__name__, file=sys.stderr)
        sys.exit(128)
