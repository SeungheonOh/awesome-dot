#!/usr/bin/env python3
"""Bounded synthetic flake experiment. Standard library; no external services."""

from collections import Counter
from dataclasses import asdict, dataclass, replace
import hashlib
import inspect
from itertools import permutations
import json
from pathlib import Path
import platform
import random
import sys


@dataclass(frozen=True)
class Record:
    entry_id: str
    title: str
    copies: int


EXPECTED = [
    Record("print-17", "River", 2),
    Record("print-23", "Bridge", 1),
    Record("print-42", "Garden", 3),
]
SEEDS = tuple(range(12))  # Predeclared budget; no stop-on-pass or hidden retry.


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def fetch_records(seed):
    """Fictional contract: these complete records, multiplicity intact, any order."""
    records = list(EXPECTED)
    random.Random(seed).shuffle(records)
    return records


def original_assertion(actual, expected):
    require(actual == expected, "Ordered list equality failed")


def repaired_assertion(actual, expected):
    # Frozen Record equality/hashing includes every declared field.
    require(Counter(actual) == Counter(expected), "Complete-record multiset equality failed")


def run_attempt(assertion, seed):
    actual = fetch_records(seed)
    outcome, detail = "assertion_pass", None
    try:
        assertion(actual, EXPECTED)
    except AssertionError as error:
        outcome, detail = "assertion_fail", str(error)
    # Unexpected errors are deliberately not converted to passing outcomes.
    return {"seed": seed, "actual_order": [r.entry_id for r in actual],
            "outcome": outcome, "detail": detail}


def experiment(assertion):
    runs = [{"slot": i, "attempt": 1, **run_attempt(assertion, seed)}
            for i, seed in enumerate(SEEDS, start=1)]
    totals = Counter(run["outcome"] for run in runs)
    return {"test_revision": sha(inspect.getsource(assertion).encode()),
            "planned": len(SEEDS), "attempted": len(runs), "completed_comparisons": len(runs),
            "assertion_pass": totals["assertion_pass"], "assertion_fail": totals["assertion_fail"],
            "setup_or_runner_error": 0, "skipped": 0, "unrun": 0,
            "hidden_retries": 0, "runs": runs}


def must_reject(actual, expected):
    try:
        repaired_assertion(actual, expected)
    except AssertionError:
        return "detected_assertion_failure"
    raise AssertionError("Negative control passed: a record defect was hidden")


def main():
    script = Path(__file__)
    product_before = sha(inspect.getsource(fetch_records).encode())
    before = experiment(original_assertion)
    after = experiment(repaired_assertion)
    require(before["assertion_pass"] > 0 and before["assertion_fail"] > 0,
            "Fixture did not demonstrate both outcomes in the declared seed matrix")
    require(after["assertion_pass"] == len(SEEDS) and after["assertion_fail"] == 0,
            "Repaired comparison rejected a permitted seeded ordering")
    require([r["actual_order"] for r in before["runs"]] == [r["actual_order"] for r in after["runs"]],
            "Before/after inputs changed")

    permutation_runs = []
    for slot, order in enumerate(permutations(EXPECTED), start=1):
        repaired_assertion(list(order), EXPECTED)
        permutation_runs.append({"slot": slot, "seed": "not randomized: exhaustive fixture permutation",
                                 "actual_order": [r.entry_id for r in order], "outcome": "assertion_pass"})
    require(len(permutation_runs) == 6, "Did not enumerate every fixture permutation")

    controls = {
        "missing_record": (EXPECTED[:-1], EXPECTED),
        "extra_record": (EXPECTED + [Record("print-99", "Spare", 1)], EXPECTED),
        "added_duplicate": (EXPECTED + [EXPECTED[0]], EXPECTED),
        "same_length_duplicate_substitution": ([EXPECTED[0], EXPECTED[0], EXPECTED[2]], EXPECTED),
        "changed_field": ([EXPECTED[0], replace(EXPECTED[1], title="Wrong title"), EXPECTED[2]], EXPECTED),
        "required_duplicate_removed": ([EXPECTED[0], EXPECTED[1]], [EXPECTED[0], EXPECTED[0], EXPECTED[1]]),
    }
    control_results = {name: must_reject(actual, expected) for name, (actual, expected) in controls.items()}
    require(set(EXPECTED + [EXPECTED[0]]) == set(EXPECTED), "Set-loss illustration is inconsistent")
    require(product_before == sha(inspect.getsource(fetch_records).encode()), "Product implementation changed")

    result = {
        "scope": "Synthetic in-memory unordered-record fixture only; no live repository edits, CI runs, services or production changes",
        "command": "python3 check_example.py", "script_revision_sha256": sha(script.read_bytes()),
        "product_revision_sha256": product_before,
        "fixture_revision_sha256": sha(json.dumps([asdict(r) for r in EXPECTED], sort_keys=True).encode()),
        "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                        "platform": platform.system(), "machine": platform.machine(),
                        "dependencies": "Python standard library only", "workers": 1,
                        "clock": "not used", "timezone_locale": "not used by fixture or comparisons",
                        "randomness": "per-attempt random.Random(seed); no shared RNG", "python_optimization": sys.flags.optimize},
        "budget": {"seed_matrix_per_revision": list(SEEDS), "attempts_per_seed": 1,
                   "permutations": "All permutations of this three-record fixture only",
                   "stop": "Finish the fixed matrix and controls; unexpected errors terminate with nonzero exit"},
        "before": before, "after": after,
        "exhaustive_fixture_permutations": {"planned": 6, "attempted": len(permutation_runs),
                                            "assertion_pass": len(permutation_runs), "assertion_fail": 0,
                                            "runs": permutation_runs},
        "negative_controls": control_results,
        "checks": {"same_seeded_inputs_before_after": "passed", "product_function_unchanged": "passed",
                   "lossy_set_would_hide_added_duplicate": "confirmed"},
        "limits": ["Selected seeds are not a statistical estimate of live failure probability",
                   "No concurrency, network, native runner or CI integration was exercised",
                   "Complete-record hashing is valid for this frozen dataclass; real schemas need their own canonicalization"],
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
