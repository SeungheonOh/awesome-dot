#!/usr/bin/env python3
"""Behavioral checks for the offline fictional import rehearsal. No live writes."""

import copy
import csv
import io
import json
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
from rehearse import canonical, digest, load_json, make_plan, parse_csv, reconcile, run

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
CONTRACT = load_json(FIXTURES / "import-contract.json")
TARGET = load_json(FIXTURES / "target-before.json")
EVIDENCE = load_json(FIXTURES / "partial-result.json")
SOURCE = (FIXTURES / "source.csv").read_bytes()
CONTRACT_HASH = digest((FIXTURES / "import-contract.json").read_bytes())
CHECKS = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    CHECKS.append(name)


def plan(source=SOURCE, target=None):
    return make_plan(CONTRACT, target or TARGET, source, CONTRACT_HASH)


def modified_source(index, **changes):
    records = parse_csv(SOURCE, CONTRACT["source_headers"])
    records[index].update(changes)
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, CONTRACT["source_headers"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(records)
    return stream.getvalue().encode("utf-8")


def by_id(rows):
    return {r["source_id"]: r for r in rows}


def evidence_results(evidence, rows=None):
    return by_id(reconcile(rows or plan(), evidence, CONTRACT)["operations"])


def rejects_call(name, callback):
    try:
        callback()
    except ValueError:
        CHECKS.append(name)
    else:
        raise AssertionError(name)


def main():
    rows = plan()
    items = by_id(rows)
    check("All five dispositions and exact source accounting", {
        name: sum(r["disposition"] == name for r in rows)
        for name in ("create", "update", "no-op", "reject", "ambiguous")
    } == {"create": 3, "update": 2, "no-op": 3, "reject": 3, "ambiguous": 5})
    check("Logical record numbering survives embedded newline", len(rows) == 16 and items["S004"]["raw"]["external_id"] == "0100")
    check("Unicode and multiline text survive", items["S003"]["intended"]["details"] == "R&D; café\nrack B" and items["S015"]["intended"]["label"] == "Worker 🧪")
    check("Leading-zero identifiers remain exact strings", items["S003"]["payload"]["external_id"] == "0099")
    check("Literal formula-like values are not escaped or evaluated", items["S004"]["intended"]["label"] == "=VERSION()" and items["S004"]["intended"]["details"] == "@queue")
    check("Blank update preserves details while explicit clear sets null", items["S001"]["intended"]["details"] == "preserve me" and items["S002"]["intended"]["details"] is None)
    check("Blank status preserves existing enum", items["S015"]["intended"]["status"] == "retired" and "status" not in items["S015"]["payload"]["fields"])
    check("Source conflict blocks both competing operations", items["S009"]["disposition"] == items["S010"]["disposition"] == "ambiguous")
    check("Duplicate export representative has explicit lineage", items["S014"]["reason"] == "exact_source_duplicate_suppressed" and items["S014"]["representative"] == "S013")
    check("Duplicate target key and crossed identifiers are held", items["S008"]["reason"] == "duplicate_target_identity" and items["S011"]["reason"] == "external_and_internal_identity_disagree")
    check("Truncated export absence never becomes create", items["S016"]["reason"] == "identity_lookup_incomplete")
    missing = copy.deepcopy(TARGET)
    del missing["exact_lookups"]["0007"]
    check("One visible match without uniqueness evidence is held", plan(target=missing)[0]["disposition"] == "ambiguous")
    missing["exact_lookups"]["0099"]["complete"] = False
    check("Incomplete empty lookup never becomes create", by_id(plan(target=missing))["S003"]["disposition"] == "ambiguous")
    check("Whitespace in identity is not silently trimmed", by_id(plan(modified_source(0, external_id=" 0007")))["S001"]["disposition"] == "ambiguous")
    check("Repeated explicit target ID across different keys is held", by_id(plan(modified_source(8, target_id="F-101")))["S001"]["reason"] == "conflicting_source_identity")
    check("Blank create status uses only the documented default", by_id(plan(modified_source(2, lifecycle="")))["S003"]["intended"]["status"] == "active")
    check("Unclearable label is rejected", by_id(plan(modified_source(2, display_name="__CLEAR__")))["S003"]["reason"] == "label_cannot_be_cleared")
    duplicate_bad = modified_source(12, lifecycle="sleeping")
    check("Conflicting duplicate does not leak a representative", all(r["disposition"] not in ("create", "update") for r in plan(duplicate_bad)[12:14]))
    check("Operation key is deterministic for immutable input", canonical(plan()) == canonical(rows))
    changed = by_id(plan(modified_source(2, note="changed")))
    check("Changed payload gets a different operation identity", changed["S003"]["idempotency_key"] != items["S003"]["idempotency_key"])
    outcomes = evidence_results(EVIDENCE)
    check("Partial result accounts for all five submitted rows", {sid: r["status"] for sid, r in outcomes.items()} == {
        "S002":"confirmed_applied", "S003":"confirmed_applied", "S004":"safe_same_key_retry",
        "S013":"confirmed_rejected", "S015":"hold_conflict"})
    absent = copy.deepcopy(EVIDENCE)
    del absent["exact_readback"]["0100"]
    check("Missing readback never authorizes retry", evidence_results(absent)["S004"]["status"] == "hold_unknown")
    expired = copy.deepcopy(EVIDENCE)
    expired["evaluated_at"] = "2026-01-13T10:00:00Z"
    check("Expired replay window blocks retry", evidence_results(expired)["S004"]["status"] == "hold_conflict")
    contradictory = copy.deepcopy(EVIDENCE)
    contradictory["exact_readback"]["0042"]["records"][0]["label"] = "Someone else's edit"
    check("Success receipt is insufficient without matching readback", evidence_results(contradictory)["S002"]["status"] == "hold_conflict")
    no_receipt = copy.deepcopy(EVIDENCE)
    no_receipt["receipts"] = [r for r in no_receipt["receipts"] if r["source_id"] != "S003"]
    check("Desired state alone is not attributed to this operation", evidence_results(no_receipt)["S003"]["status"] == "observed_desired_state")
    incomplete = copy.deepcopy(EVIDENCE)
    incomplete["exact_readback"]["0042"]["complete"] = False
    check("Incomplete readback is not confirmed applied", evidence_results(incomplete)["S002"]["status"] == "hold_unknown")
    wrong_id = copy.deepcopy(EVIDENCE)
    wrong_id["exact_readback"]["0042"]["records"][0]["record_id"] = "F-404"
    check("Equal values under another stable ID do not confirm update", evidence_results(wrong_id)["S002"]["status"] == "hold_conflict")
    conflicting_receipt = copy.deepcopy(EVIDENCE)
    conflicting_receipt["receipts"].append(copy.deepcopy(conflicting_receipt["receipts"][0]))
    rejects_call("Repeated receipt is not silently overwritten", lambda: reconcile(rows, conflicting_receipt, CONTRACT))
    wrong_scope = copy.deepcopy(EVIDENCE)
    wrong_scope["destination"] = "other-synthetic-account/asset-registry"
    rejects_call("Cross-account evidence is refused", lambda: reconcile(rows, wrong_scope, CONTRACT))
    broken_target = copy.deepcopy(TARGET)
    broken_target["exact_lookups"]["0007"]["record_ids"] = []
    rejects_call("Contradictory lookup and snapshot are refused", lambda: plan(target=broken_target))
    rejects_call("Ragged source record is refused", lambda: plan(SOURCE + b"bad,row\n"))
    rejects_call("Duplicate source headers are refused", lambda: plan(SOURCE.replace(b"target_id", b"external_id", 1)))
    with tempfile.TemporaryDirectory(prefix=".verify-", dir=ROOT) as temp:
        output = Path(temp) / "output"
        summary, partial = run(FIXTURES, output)
        imported = parse_csv((output / "import-ready.csv").read_bytes(), CONTRACT["import_headers"])
        check("Actual files reopen with exact text and clear tokens", len(imported) == 5 and imported[0]["details"] == "__CLEAR__" and imported[2]["label"] == "=VERSION()")
        check("Retry candidate contains only the identical eligible original row", parse_csv((output / "same-key-retry-candidate.csv").read_bytes(), CONTRACT["import_headers"]) == [imported[2]])
        check("Source stays byte-for-byte unchanged", (FIXTURES / "source.csv").read_bytes() == SOURCE and summary["source_unchanged_pass"])
        check("All saved artifacts parse and reconcile", summary["source_accounting_pass"] and summary["import_accounting_pass"] and sum(partial["counts"].values()) == 5 and len(load_json(output / "operation-plan.json")) == 16 and len(load_json(output / "rejects-and-ambiguities.json")) == 8)
        first = {p.name: p.read_bytes() for p in output.iterdir()}
        run(FIXTURES, output)
        check("Repeat execution produces identical artifact bytes", first == {p.name: p.read_bytes() for p in output.iterdir()})
    print(json.dumps({"passed": len(CHECKS), "checks": CHECKS, "live_write_performed": False}, indent=2))


if __name__ == "__main__":
    main()
