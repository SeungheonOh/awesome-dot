#!/usr/bin/env python3
"""Verify saved evidence and reproduce paired artifact counts; run no submitted code."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVALUATION = ROOT.parents[1]
SEMANTIC_IDS = {
    "F1": {"g5"},
    "F2": {f"g{i}" for i in range(1, 6)},
    "F4": {f"g{group}.{i}" for group, count in [(1, 4), (2, 4), (3, 2), (4, 3), (5, 1)] for i in range(1, count + 1)},
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def verified_file(base, relative, sha256, size=None):
    path = base / relative
    if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(base.resolve()):
        raise ValueError(f"Unsafe or missing file: {relative}")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha256 or (size is not None and len(data) != size):
        raise ValueError(f"Content differs: {relative}")
    return path


def counts(groups):
    states = [g["passed"] for g in groups]
    if any(s is not None and type(s) is not bool for s in states):
        raise ValueError("Criterion state must be true, false, or null")
    return {"passed": states.count(True), "failed": states.count(False),
            "unknown": states.count(None), "total": len(states)}


def summarize(rows):
    pairs = []
    for number in range(1, 9):
        case = f"F{number}"
        pair = {r["arm"]: r for r in rows if r["case_id"] == case}
        if len(pair) != 2 or set(pair) != {"C", "S"}:
            raise ValueError(f"Missing or repeated arm: {case}")
        c, s = [counts(pair[a]["criterion_groups"]) for a in ("C", "S")]
        comparable = c["unknown"] == s["unknown"] == 0 and c["total"] == s["total"]
        difference = s["passed"] - c["passed"] if comparable else None
        outcome = ("tie" if difference == 0 else "S_win" if difference > 0 else "S_loss") if comparable else "unresolved"
        pairs.append({"case_id": case, "C": c, "S": s,
                      "S_minus_C_passed_groups": difference, "paired_outcome": outcome})
    def arm_total(arm):
        return {key: sum(p[arm][key] for p in pairs) for key in ("passed", "failed", "unknown", "total")}
    return {"schema_version": 1, "outcome_scope": "artifact criterion groups only",
            "scheduled_cases": 8, "scheduled_attempts": 16, "first_submissions": len(rows),
            "rows": pairs, "C": arm_total("C"), "S": arm_total("S"),
            "paired_outcomes": {k: sum(p["paired_outcome"] == k for p in pairs) for k in ("S_win", "tie", "S_loss", "unresolved")},
            "overall_acceptance": None, "process_integrity": None,
            "interpretation": "Descriptive results on eight authored cases. No population inference, human-productivity estimate, or speed-saving claim."}


def verify():
    data = read(ROOT / "attempts.json")
    rows = data["rows"]
    schedule = read(ROOT / "schedule.json")["rows"]
    if len(rows) != 16 or {r["attempt_id"] for r in rows} != {r["attempt_id"] for r in schedule}:
        raise ValueError("All 16 scheduled attempts must be retained exactly once")
    manifest = read(ROOT / "artifact-manifest.json")
    f8 = {r["attempt_id"]: r for r in read(ROOT / "f8/execution-results.json")["rows"]}
    listed = []
    for row in rows:
        grade = None
        if len(row["criterion_groups"]) != 5 or {g["id"] for g in row["criterion_groups"]} != {f"g{i}" for i in range(1, 6)}:
            raise ValueError("Five distinct criterion groups required")
        if row["overall_acceptance"] is not None or row["process_integrity"] is not None:
            raise ValueError("Unknown process-level outcomes cannot become a pass")
        for f in row["artifact_files"]:
            verified_file(ROOT, f["path"], f["sha256"], f["bytes"])
            listed.append(f)
        for f in row["protected_inputs"]:
            verified_file(EVALUATION, f["source_relative_path"], f["sha256"], f["bytes"])
        if row["artifact_grade"] is not None:
            path = verified_file(ROOT, row["artifact_grade"], row["artifact_grade_sha256"])
            grade = read(path)
            if grade["case_id"] != row["case_id"] or [{k: g[k] for k in ("id", "passed")} for g in grade["groups"]] != row["criterion_groups"]:
                raise ValueError("Grade and attempt criterion states differ")
        reviews = []
        expected_semantics = SEMANTIC_IDS.get(row["case_id"], set())
        refs = row["semantic_reviews"]
        if expected_semantics:
            expected_paths = {f'reviews/reviewer-{letter}/{row["attempt_id"]}.json' for letter in ("a", "b")}
            if len(refs) != 2 or {ref["path"] for ref in refs} != expected_paths:
                raise ValueError("Exactly two distinct source-grounded semantic reviews required")
        elif refs:
            raise ValueError("Unexpected semantic review schema")
        artifact_hashes = {f["path"].split(f'artifacts/{row["attempt_id"]}/', 1)[1]: f["sha256"] for f in row["artifact_files"]}
        if row["case_id"] == "F8":
            evidence = f8[row["attempt_id"]]
            if evidence["artifact_hashes"] != artifact_hashes or [{k: g[k] for k in ("id", "passed")} for g in evidence["primary_groups"]] != row["criterion_groups"]:
                raise ValueError("F8 execution record differs from frozen artifact or score")
            if not evidence["static_integrity"]["passed"] or not all(evidence["g5_required_checks"].values()):
                raise ValueError("F8 source-reviewed execution checks are incomplete")
        for ref in row["semantic_reviews"]:
            review = read(verified_file(ROOT, ref["path"], ref["sha256"]))
            if review["case_id"] != row["case_id"]:
                raise ValueError("Review case differs")
            if review["submission_hashes"] != artifact_hashes:
                raise ValueError("Review must bind every saved artifact with exact hashes")
            if isinstance(review["groups"], dict):
                items = [(key, group["passed"]) for key, group in review["groups"].items()]
            else:
                items = [(a["id"], a["passed"]) for g in review["groups"] for a in g["assertions"]]
            states = dict(items)
            if len(states) != len(items) or set(states) != expected_semantics:
                raise ValueError("Semantic group/assertion IDs differ from the frozen rubric")
            if any(state is not None and type(state) is not bool for state in states.values()):
                raise ValueError("Semantic states must be true, false, or null")
            reviews.append(states)
        if expected_semantics:
            if grade is None:
                raise ValueError("Semantic ratings require a final artifact grade")
            graded_items = [(a.get("id", g["id"]), a["passed"]) for g in grade["groups"] for a in g.get("assertions", []) if a.get("kind") == "semantic"]
            graded_states = dict(graded_items)
            if len(graded_states) != len(graded_items) or set(graded_states) != expected_semantics:
                raise ValueError("Final grade semantic assertions differ from frozen rubric")
            if reviews[0] != reviews[1] or reviews[0] != graded_states:
                raise ValueError("Semantic reviews disagree with each other or final graded states")
    if sorted(listed, key=lambda x: x["path"]) != sorted(manifest["files"], key=lambda x: x["path"]):
        raise ValueError("Artifact manifest differs")
    actual = {p.relative_to(ROOT).as_posix() for p in (ROOT / "artifacts").rglob("*") if p.is_file()}
    if actual != {f["path"] for f in listed} or len(listed) != manifest["artifact_count"]:
        raise ValueError("Artifact inventory differs")
    return summarize(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-summary", action="store_true", help="Recompute paired-summary.json from saved ratings; does not rerate artifacts")
    args = parser.parse_args()
    summary = verify()
    destination = ROOT / "paired-summary.json"
    if args.write_summary:
        destination.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    elif read(destination) != summary:
        raise ValueError("Published summary differs from reproduced counts")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
