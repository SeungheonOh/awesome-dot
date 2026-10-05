"""Stdlib, evaluator-side F8 grader. Runner packet has no dependency on this file."""
import argparse
import importlib.util
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
# Load only this evaluator-owned module, even when imported by file path.
_safe_spec = importlib.util.spec_from_file_location("f8_evaluator_safe_io", HERE/"safe_io.py")
_safe_io = importlib.util.module_from_spec(_safe_spec)
_safe_spec.loader.exec_module(_safe_io)
REQUIRED = ("merge_session.py", "card_editor.py", "merge_primitive.py", "demo_cards.json",
            "tests/test_smoke.py", "tests/test_regressions.py", "checks.txt")
TEST_COMMAND = "python -m unittest discover -s tests -v"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment():
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_tests(root, pattern=None):
    try:
        command = [sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests", "-v"]
        if pattern is not None:
            command += ["-p", pattern]
        proc = subprocess.run(command,
                              cwd=root, env=environment(), capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        return False, None, "unittest exceeded the 10-second fixture limit"
    output = proc.stdout + proc.stderr
    count = re.search(r"Ran (\d+) tests? in ", output)
    return proc.returncode == 0, int(count.group(1)) if count else None, output[-6000:]


def _execute_author_fixture(submission_dir, runner_dir):
    submission, runner = Path(submission_dir).absolute(), Path(runner_dir).absolute()
    integrity_result = _static_integrity(submission, runner)
    if integrity_result["passed"] is None:
        raise ValueError("Author fixture execution blocked by evaluator trust infrastructure: " + "; ".join(integrity_result["reasons"]))
    integrity = integrity_result["reasons"]
    groups = [{"id": f"g{i}", "passed": False, "reasons": ["behavior probe did not complete"]} for i in range(1,6)]
    if submission.is_dir():
        with tempfile.TemporaryDirectory(prefix="f8-grade-") as directory:
            stage = Path(directory)/"submission"
            shutil.copytree(submission, stage, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            try:
                proc = subprocess.run([sys.executable, "-I", "-B", str(HERE/"probe.py"), str(stage)],
                                      env=environment(),capture_output=True,text=True,timeout=10)
                if proc.returncode != 0:
                    raise ValueError("probe process failed: " + proc.stderr[-1000:])
                candidate = json.loads(proc.stdout)
                if not isinstance(candidate, list) or [g.get("id") for g in candidate] != [f"g{i}" for i in range(1,6)]:
                    raise ValueError("invalid probe result")
                groups = candidate
            except (ValueError, subprocess.TimeoutExpired) as error:
                for group in groups:
                    group["reasons"] = [str(error)]
            g5 = groups[4]
            def fail(reason):
                g5["passed"] = False
                g5["reasons"].append(reason)
            passed, count, output = run_tests(stage)
            if not passed:
                fail("submitted unittest suite does not pass: " + output[-1600:])
            if count is None or count < 5:
                fail("need the 3 protected tests and at least 2 runnable new regression tests")
            focused_passed, focused_count, focused_output = run_tests(stage, "test_regressions.py")
            if not focused_passed or focused_count is None or focused_count < 2:
                fail("tests/test_regressions.py must itself run at least two passing regression tests")
            try:
                checks = (stage/"checks.txt").read_text(encoding="utf-8")
                for label, expected in (("Command",TEST_COMMAND),("Result","PASS"),("Tests",str(count))):
                    matches = re.findall(r"^"+label+r": (.*)$", checks, flags=re.MULTILINE)
                    if matches != [expected]:
                        fail("checks.txt " + label + " must match the verified command/result/test count")
            except (OSError, UnicodeError):
                fail("checks.txt missing or not UTF-8 text")
            # Exercise the submitted tests against isolated, API-conforming failure implementations.
            # The expected results above never import or compute with these controls.
            for shape in ("stale", "unresolved"):
                mutant = Path(directory)/shape
                shutil.copytree(stage,mutant)
                for module in ("merge_session.py", "card_editor.py"):
                    shutil.copyfile(HERE/"test_mutants"/shape/module,mutant/module)
                mutant_passed, mutant_count, mutant_output = run_tests(mutant, "test_regressions.py")
                if mutant_passed:
                    fail("submitted regressions do not detect the isolated " + shape + " failure")
                elif mutant_count is None or mutant_count < 2 or "Traceback (most recent call last)" not in mutant_output:
                    fail("regression sensitivity check must run tests and fail assertions, not fail discovery: " + shape)
    else:
        groups[4]["reasons"].append("submission directory missing")
    passed_count = sum(bool(group["passed"]) for group in groups)
    return {"case_id":"F8", "integrity":{"passed":not integrity,"reasons":integrity},
            "groups":groups, "accepted":not integrity and passed_count == 5, "quality":passed_count/5}


ISOLATION_REASON = ("PENDING: submitted Python was not executed. A verified isolated execution "
                    "backend is not configured; subprocess separation alone is not a sandbox.")


def _trusted_manifest():
    path = HERE/"trusted_manifest.json"
    with path.open("rb") as handle:
        raw = handle.read(1048577)
    if len(raw) > 1048576:
        raise ValueError("trusted manifest exceeds metadata limit")
    trusted = json.loads(raw)
    runner_names = {"task.txt", "input-manifest.json"} | {
        "inputs/scaffold/"+name for name in ("merge_session.py", "card_editor.py", "merge_primitive.py", "demo_cards.json", "tests/test_smoke.py")}
    protected_names = {"merge_primitive.py", "demo_cards.json", "tests/test_smoke.py"}
    if type(trusted) is not dict or trusted.get("case_id") != "F8":
        raise ValueError("trusted manifest case/schema is invalid")
    for field, names in (("runner_files", runner_names), ("protected_submission_files", protected_names)):
        values = trusted.get(field)
        if type(values) is not dict or set(values) != names:
            raise ValueError("trusted manifest required file keys are invalid: " + field)
        if any(type(value) is not str or re.fullmatch(r"[0-9a-f]{64}",value) is None for value in values.values()):
            raise ValueError("trusted manifest hashes are invalid: " + field)
    return trusted


def _static_integrity(submission, runner):
    reasons = []
    try:
        trusted = _trusted_manifest()
    except (OSError, UnicodeError, ValueError, TypeError, KeyError) as error:
        return {"passed": None, "reasons": ["PENDING: evaluator trust metadata unavailable or malformed: " + type(error).__name__]}
    trees = {}
    for label, root in (("runner", runner), ("output", submission)):
        try:
            trees[label] = _safe_io.tree_hashes(root)
        except (OSError, ValueError, TypeError) as error:
            reasons.append(label + " ingestion: " + str(error))
            trees[label] = {}
    for relative, expected in trusted["runner_files"].items():
        if trees["runner"].get(relative) != expected:
            reasons.append("protected runner file missing or changed: " + relative)
    for relative in REQUIRED:
        if relative not in trees["output"]:
            reasons.append("required regular deliverable missing: " + relative)
    for relative, expected in trusted["protected_submission_files"].items():
        if trees["output"].get(relative) != expected:
            reasons.append("protected output copy missing or changed: " + relative)
    return {"passed": not reasons, "reasons": reasons}


def grade(submission_dir, runner_dir):
    """Production-facing, fail-closed API: static inspection only, no submitted code execution."""
    integrity = _static_integrity(submission_dir, runner_dir)
    result = {"case_id": "F8", "integrity": integrity,
            "groups": [{"id": f"g{i}", "passed": None, "reasons": [ISOLATION_REASON]} for i in range(1, 6)],
            "accepted": False if integrity["passed"] is False else None, "quality": None,
            "blocked_reason": "untrusted_python_execution_requires_verified_isolation"}
    if integrity["passed"] is None:
        result["infrastructure_reason"] = "evaluator_trust_metadata_unavailable_or_malformed"
    return result


def _tree_hashes(root):
    hashes = _safe_io.tree_hashes(root)
    return {relative: digest for relative, digest in hashes.items()
            if "__pycache__" not in Path(relative).parts and not relative.endswith(".pyc")}


def grade_author_fixture(submission_dir, runner_dir):
    """ONLY original author-authored, exact-hash-allowlisted local fixture/control code."""
    hashes = _tree_hashes(submission_dir)
    allowlist = json.loads((HERE/"author_fixture_allowlist.json").read_text(encoding="utf-8"))
    if hashes not in [entry["files"] for entry in allowlist["fixtures"]]:
        raise ValueError("Not an exact allowlisted author fixture; use fail-closed grade()")
    # Verify every file that will replace a fixture during regression sensitivity checks.
    for relative, expected in allowlist["mutation_module_files"].items():
        path = HERE/relative
        if not path.is_file() or path.is_symlink() or digest(path) != expected:
            raise ValueError("Author regression-sensitivity module changed: " + relative)
    return _execute_author_fixture(submission_dir, runner_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission",required=True)
    parser.add_argument("--runner",required=True)
    args=parser.parse_args()
    print(json.dumps(grade(args.submission,args.runner),ensure_ascii=False,indent=2))
