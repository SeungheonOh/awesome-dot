#!/usr/bin/env python3
"""Run all local evaluation checks without model calls or fresh agent trials."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
INITIAL = "results/native-cloud-2026-10-06"
REGRESSION_MODULES = {"test_check", "test_report", "test_verify"}
HARNESS_MODULES = {"test_harness", "test_independent_boundaries", "test_independent_coverage"}
HARNESS_COMMAND = ("-m", "unittest", "discover", "-s", "tests", "-v")
# Keep the order explicit. No saved candidate or package helper is a command.
COMMANDS = (
    ("Original source and fixture checks", ("evaluation/verify.py", "--fixtures-only")),
    ("Report, navigation and verifier regressions", ("evaluation/verify.py", "--tests-only")),
    ("Earlier study saved evidence", (f"evaluation/{INITIAL}/score.py",)),
    ("Repeated study saved evidence", ("evaluation/studies/repeated-stress-2026-10-06/reproduce_saved_evidence.py",)),
    ("Published report consistency", ("evaluation/report.py", "--check")),
)
TIMEOUT_SECONDS = 900
UNBOUND = object()


def read_file(root, relative, sha256=UNBOUND, size=UNBOUND):
    """Read a confined regular file; never import or execute its contents."""
    relative = Path(relative)
    path = root / relative
    if (relative.is_absolute() or ".." in relative.parts
            or not path.resolve().is_relative_to(root.resolve())
            or any((root / parent).is_symlink() for parent in (relative, *relative.parents))
            or not path.is_file()):
        raise ValueError(f"Unsafe or missing file: {relative}")
    raw = path.read_bytes()
    if ((sha256 is not UNBOUND and hashlib.sha256(raw).hexdigest() != sha256)
            or (size is not UNBOUND and (type(size) is not int or len(raw) != size))):
        raise ValueError(f"Content differs: {relative}")
    return raw


def index_rows(rows, key, label):
    indexed = {}
    for row in rows:
        value = row[key]
        if not isinstance(value, str) or not value or value in indexed:
            raise ValueError(f"Missing or duplicate {key} in {label}: {value!r}")
        indexed[value] = row
    return indexed


def check_initial_bindings(root):
    """Add identity/source checks outside the unchanged historical study."""
    provenance = json.loads(read_file(root, f"{INITIAL}/provenance.json"))
    config = json.loads(read_file(root, "pilot-source-config.json", provenance["source_config_sha256"]))
    for name, key in (("cases/manifest.json", "case_manifest_sha256"),
                      ("packages/manifest.json", "package_manifest_sha256")):
        read_file(root, name, provenance[key])
    sources = index_rows(provenance["grading_sources"], "path", "grading sources")
    required_sources = {p.relative_to(root).as_posix()
                        for p in (root / "evaluators").rglob("*") if p.is_file()}
    if set(sources) != required_sources:
        raise ValueError("Missing or extra grading-source paths")
    for name, entry in sources.items():
        read_file(root, name, entry["sha256"], entry["bytes"])

    schedule = index_rows(json.loads(read_file(root, f"{INITIAL}/schedule.json"))["rows"],
                          "attempt_id", "schedule")
    attempts_data = json.loads(read_file(root, f"{INITIAL}/attempts.json"))
    attempts = index_rows(attempts_data["rows"], "attempt_id", "attempts")
    prompts = index_rows(provenance["frozen_prompt_hashes"], "attempt_id", "prompt hashes")
    tasks = index_rows(config["tasks"], "family_id", "source tasks")
    # This saved study retained one first submission per case/condition, as
    # declared in its method.md. The hash-bound source config also has one repeat.
    if type(config["repetitions"]) is not int or config["repetitions"] != 1:
        raise ValueError("Initial study requires one first submission per case/condition")
    expected_pairs = {(case, arm) for case in tasks for arm in config["arms"]}
    if (len(schedule) != len(expected_pairs) or attempts_data["scheduled_attempts"] != len(schedule)
            or set(schedule) != set(attempts) or set(schedule) != set(prompts)):
        raise ValueError("Missing or extra scheduled attempt IDs")
    if {(row["case_id"], row["arm"]) for row in schedule.values()} != expected_pairs:
        raise ValueError("Schedule case/condition pairs differ from source tasks")
    ordinals = [row["ordinal"] for row in schedule.values()]
    if any(type(value) is not int for value in ordinals) or sorted(ordinals) != list(range(1, len(schedule) + 1)):
        raise ValueError("Schedule ordinals are missing or duplicated")
    fields = (("case_id", "case_id"), ("arm", "arm"), ("schedule_ordinal", "ordinal"),
              ("attempt_number", "attempt_number"), ("timeout_cap_seconds", "timeout_seconds"),
              ("dispatch_prompt_sha256", "dispatch_prompt_sha256"))
    for aid, planned in schedule.items():
        expected_id = f"N{planned['ordinal']:02d}-{planned['case_id']}-{planned['arm']}"
        if aid != expected_id:
            raise ValueError(f"Schedule attempt_id does not match ordinal/case/condition: {aid}")
        if planned["task_id"] != tasks[planned["case_id"]]["task_id"]:
            raise ValueError(f"Schedule task_id mismatch: {aid}")
        if type(planned["attempt_number"]) is not int or planned["attempt_number"] != 1:
            raise ValueError(f"Schedule attempt_number must be integer 1 for a first submission: {aid}")
        timeout = planned["timeout_seconds"]
        task_timeout = tasks[planned["case_id"]]["timeout_s"]
        if (type(timeout) is not int or type(task_timeout) is not int
                or timeout <= 0 or timeout != task_timeout):
            raise ValueError(f"Schedule timeout_seconds differs from source task timeout_s: {aid}")
        prompt_hash = planned["dispatch_prompt_sha256"]
        if (not isinstance(prompt_hash, str) or len(prompt_hash) != 64
                or not set(prompt_hash) <= set("0123456789abcdef")):
            raise ValueError(f"Invalid schedule prompt hash: {aid}")
        if prompt_hash != prompts[aid]["sha256"]:
            raise ValueError(f"Schedule prompt hash mismatch: {aid}")
        for actual_key, planned_key in fields:
            if (type(attempts[aid][actual_key]) is not type(planned[planned_key])
                    or attempts[aid][actual_key] != planned[planned_key]):
                raise ValueError(f"Attempt {actual_key} mismatch: {aid}")
    print(f"Initial study bindings: {len(attempts)} attempts; {len(sources)} grading sources; "
          "3 config/manifest hashes. Prompt hash records agree; omitted prompts were not reconstructed.", flush=True)


def run_test_modules(root, required, search_paths=()):
    """Run immediate test modules once, rejecting omissions and runtime skips."""
    import unittest

    names = sorted(path.stem for path in root.glob("test_*.py"))
    missing = required - set(names)
    if missing:
        raise ValueError("Missing test modules: " + ", ".join(sorted(missing)))
    for name in names:
        read_file(root, name + ".py")
    previous_path = sys.path[:]
    try:
        sys.path[:0] = [str(root), *(str(path) for path in search_paths)]
        loader = unittest.TestLoader()
        suites = []
        for name in names:
            suite = loader.loadTestsFromName(name)
            if suite.countTestCases() == 0:
                raise ValueError(f"No tests discovered in {name}")
            suites.append(suite)
        if loader.errors:
            raise ValueError("Test discovery failed:\n" + "\n".join(loader.errors))
        result = unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(suites))
        if result.skipped:
            print("Test checks failed: skipped tests are not a complete verification", file=sys.stderr)
        return 0 if result.wasSuccessful() and not result.skipped else 1
    finally:
        sys.path[:] = previous_path


def run_regressions(root):
    return run_test_modules(root, REGRESSION_MODULES)


def load_check(root):
    import importlib.util

    read_file(root, "check.py")
    spec = importlib.util.spec_from_file_location("original_fixture_check", root / "check.py")
    check = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(check)
    return check


def run_fixtures(root):
    """Keep check.py's workflow, substituting only a strict harness runner."""
    check = load_check(root)
    original_run = check.run
    harness_runs = 0

    def run(command, cwd, env):
        nonlocal harness_runs
        if tuple(command) == HARNESS_COMMAND and Path(cwd) == root / "harness":
            harness_runs += 1
            if harness_runs != 1:
                raise ValueError("Original check repeated its harness stage")
            subprocess.run([sys.executable, "-I", "-B", str(root / "verify.py"), "--harness-only"],
                           cwd=cwd, env=env, check=True, timeout=120)
        else:
            original_run(command, cwd, env)

    check.run = run
    try:
        result = check.main()
        if harness_runs != 1:
            raise ValueError("Original check omitted its harness stage")
        return result
    finally:
        check.run = original_run


def verify(root):
    failures = []
    total = len(COMMANDS) + 1
    print(f"[1/{total}] Earlier study schedule and source bindings", flush=True)
    try:
        check_initial_bindings(root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        failures.append("Earlier study schedule and source bindings")
        print(f"FAILED: {failures[-1]}: {error}", file=sys.stderr, flush=True)
    # check.py deliberately sets PYTHONPATH for its own fixture subprocesses.
    # Remove inherited Python settings first, especially PYTHONOPTIMIZE: the
    # historical repeated-study verifier relies on assertions being enabled.
    env = {key: value for key, value in os.environ.items() if not key.startswith("PYTHON")}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    for number, (label, args) in enumerate(COMMANDS, 2):
        command = [sys.executable, "-I", "-B", *args]
        print(f"\n[{number}/{total}] {label}\n$ {shlex.join(command)}", flush=True)
        try:
            subprocess.run(command, cwd=root.parent, env=env, check=True, timeout=TIMEOUT_SECONDS)
        except (OSError, ValueError, subprocess.SubprocessError) as error:
            failures.append(label)
            print(f"FAILED: {label}: {error}", file=sys.stderr, flush=True)
    if failures:
        print(f"\nVerification failed ({len(failures)}/{total} checks): " + "; ".join(failures),
              file=sys.stderr, flush=True)
        return 1
    print(f"\nAll {total} local verification checks passed. Fixture tests are not agent outcomes. "
          "Saved-evidence verification made no model calls or submitted-code executions.", flush=True)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--tests-only", action="store_true", help="Run immediate evaluation regression tests only")
    modes.add_argument("--fixtures-only", action="store_true", help="Run original checks with strict harness discovery")
    modes.add_argument("--harness-only", action="store_true", help="Run immediate harness test modules with no skips")
    args = parser.parse_args(argv)
    try:
        if args.tests_only:
            return run_regressions(ROOT)
        if args.fixtures_only:
            return run_fixtures(ROOT)
        if args.harness_only:
            return run_test_modules(ROOT / "harness/tests", HARNESS_MODULES, (ROOT / "harness",))
        return verify(ROOT)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(f"Verification failed: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Verification interrupted; remaining checks were not completed", file=sys.stderr)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
