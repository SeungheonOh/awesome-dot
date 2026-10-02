#!/usr/bin/env python3
"""Offline CSV rehearsal for the explicitly fictional contract in fixtures/.

No network, account writes, spreadsheet evaluation, or third-party dependencies.
Adapt and review the contract adapter before applying this pattern elsewhere.
"""

import argparse
import csv
import hashlib
import io
import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

FIELDS = ("label", "status", "details")
DISPOSITIONS = ("create", "update", "no-op", "reject", "ambiguous")
SOURCE_HEADERS = ["external_id", "target_id", "display_name", "lifecycle", "note"]
MAPPING = dict(zip(SOURCE_HEADERS, ["external_id", "record_id", *FIELDS]))


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest(value):
    return hashlib.sha256(value).hexdigest()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_csv(data, expected_headers):
    # newline="" keeps embedded newlines intact. csv.reader does no numeric coercion.
    rows = list(csv.reader(io.StringIO(data.decode("utf-8"), newline=""), strict=True))
    if not rows or rows[0] != expected_headers:
        raise ValueError("CSV header must exactly match the contract, without duplicate columns")
    if any(len(row) != len(expected_headers) for row in rows[1:]):
        raise ValueError("Ragged CSV records cannot be assigned a reliable field mapping")
    return [dict(zip(expected_headers, row)) for row in rows[1:]]


def validate_inputs(contract, target):
    if contract.get("fictional") is not True or contract.get("adapter") != "fictional-asset-registry-v1":
        raise ValueError("This helper accepts only the named fictional contract adapter")
    if contract["source_headers"] != SOURCE_HEADERS or contract["mapping"] != MAPPING:
        raise ValueError("Adapt the field adapter before changing the mapping")
    if contract["clear_token"] != "__CLEAR__" or contract["allowed_status"] != ["active", "retired"]:
        raise ValueError("Adapt the value adapter before changing enum or clear semantics")
    if contract["create_default_status"] != "active":
        raise ValueError("Unsupported create default")
    if target.get("fictional") is not True or contract["destination"] != target["destination"]:
        raise ValueError("Target scope differs from contract")
    records = target["records"]
    ids = [r["record_id"] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("Snapshot repeats a supposedly stable internal record ID")
    for record in records:
        if not all(isinstance(record[k], str) for k in ("record_id", "external_id", "label", "status", "revision")):
            raise ValueError("Target identity and required fields must be text")
        if record["details"] is not None and not isinstance(record["details"], str):
            raise ValueError("Target details must be nullable text")
    by_id = {r["record_id"]: r for r in records}
    for key, evidence in target["exact_lookups"].items():
        referenced = evidence["record_ids"]
        if len(referenced) != len(set(referenced)):
            raise ValueError("Lookup repeats a record ID")
        if any(rid not in by_id or by_id[rid]["external_id"] != key for rid in referenced):
            raise ValueError("Lookup and expanded records contradict one another")
        visible = {r["record_id"] for r in records if r["external_id"] == key}
        if evidence.get("complete") and visible != set(referenced):
            raise ValueError("Complete exact lookup contradicts visible target records")


def make_plan(contract, target, source_bytes, contract_hash):
    validate_inputs(contract, target)
    source_hash = digest(source_bytes)
    source = parse_csv(source_bytes, contract["source_headers"])
    by_id = {r["record_id"]: r for r in target["records"]}
    key_groups, id_groups = defaultdict(list), defaultdict(list)
    for index, raw in enumerate(source):
        if raw["external_id"]:
            key_groups[raw["external_id"]].append(index)
        if raw["target_id"]:
            id_groups[raw["target_id"]].append(index)
    conflict, duplicate_of = set(), {}
    for group in key_groups.values():
        if len(group) < 2:
            continue
        if len({canonical(source[i]) for i in group}) > 1:
            conflict.update(group)
        else:
            duplicate_of.update({i: group[0] for i in group[1:]})
    for group in id_groups.values():
        if len({source[i]["external_id"] for i in group}) > 1:
            conflict.update(group)

    plan = []
    for index, raw in enumerate(source):
        source_id = f"S{index + 1:03d}"
        item = {"source_id": source_id, "lineage_id": f"{source_hash}:{source_id}",
                "source_record_ordinal": index + 1, "raw": raw}
        key = raw["external_id"]

        def finish(disposition, reason, **extra):
            item.update(disposition=disposition, reason=reason, **extra)
            plan.append(item)

        if not key:
            finish("reject", "missing_external_id")
            continue
        if raw["lifecycle"] not in ("", *contract["allowed_status"]):
            finish("reject", "unsupported_status")
            continue
        if raw["display_name"] == contract["clear_token"]:
            finish("reject", "label_cannot_be_cleared")
            continue
        if index in conflict:
            finish("ambiguous", "conflicting_source_identity")
            continue
        if index in duplicate_of:
            representative = plan[duplicate_of[index]]
            if representative["disposition"] in ("create", "update", "no-op"):
                finish("no-op", "exact_source_duplicate_suppressed",
                       representative=representative["source_id"])
            else:
                finish(representative["disposition"], "duplicate_of_excluded_record",
                       representative=representative["source_id"])
            continue
        evidence = target["exact_lookups"].get(key)
        if not evidence or evidence.get("complete") is not True:
            finish("ambiguous", "identity_lookup_incomplete")
            continue
        matches = evidence["record_ids"]
        if len(matches) > 1:
            finish("ambiguous", "duplicate_target_identity", candidates=matches)
            continue
        if raw["target_id"] and (not matches or raw["target_id"] != matches[0]):
            finish("ambiguous", "external_and_internal_identity_disagree", candidates=matches)
            continue
        before = by_id[matches[0]] if matches else None
        if before is None and not raw["display_name"]:
            finish("reject", "create_requires_label")
            continue
        fields = {}
        for source_field, target_field in (("display_name", "label"), ("lifecycle", "status"), ("note", "details")):
            value = raw[source_field]
            if before is not None and value == "":
                continue
            if target_field == "details" and value in ("", contract["clear_token"]):
                value = None
            if target_field == "status" and value == "":
                value = contract["create_default_status"]
            if before is None or before[target_field] != value:
                fields[target_field] = value
        after = ({k: before[k] for k in ("external_id", *FIELDS)} if before else {"external_id": key})
        after.update(fields)
        if before is not None and not fields:
            finish("no-op", "target_already_has_intended_values", before=before, intended=after)
            continue
        operation = "update" if before else "create"
        payload = {"operation": operation, "external_id": key,
                   "record_id": before["record_id"] if before else "",
                   "expected_revision": before["revision"] if before else "", "fields": fields}
        payload_hash = digest(canonical(payload).encode("utf-8"))
        identity = {"destination": contract["destination"], "contract_sha256": contract_hash,
                    "source_sha256": source_hash, "source_id": source_id, "payload_sha256": payload_hash}
        op_key = "op-" + digest(canonical(identity).encode("utf-8"))
        finish(operation, "field_differences" if before else "authoritative_absence",
               before=before, intended=after, payload=payload, payload_sha256=payload_hash,
               idempotency_key=op_key)
    return plan


def import_row(item, contract):
    payload = item["payload"]
    row = {"source_id": item["source_id"], "idempotency_key": item["idempotency_key"]}
    row.update({key: payload[key] for key in ("operation", "external_id", "record_id", "expected_revision")})
    for field in FIELDS:
        value = payload["fields"].get(field, "")
        if value is None:
            value = contract["clear_token"] if item["disposition"] == "update" else ""
        row[field] = value
    return row


def parse_time(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Evidence timestamps require a timezone")
    return result


def reconcile(plan, evidence, contract):
    if evidence.get("fictional") is not True or evidence["destination"] != contract["destination"]:
        raise ValueError("Partial-result evidence is outside this fictional destination")
    ready = {r["source_id"]: r for r in plan if r["disposition"] in ("create", "update")}
    receipts = {}
    for receipt in evidence["receipts"]:
        sid = receipt["source_id"]
        if sid not in ready or sid in receipts or receipt["result"] not in ("applied", "rejected"):
            raise ValueError("Receipt is duplicated, unknown, or outside submitted operations")
        receipts[sid] = receipt
    submitted = parse_time(evidence["submitted_at"])
    evaluated = parse_time(evidence["evaluated_at"])
    retention = evidence["idempotency_retention_hours"]
    if retention != 24 or evaluated < submitted:
        raise ValueError("Retry evidence contradicts the adapter contract or time order")
    replay_valid = evaluated < submitted + timedelta(hours=retention)
    results = []
    for sid, item in ready.items():
        receipt = receipts.get(sid)
        lookup = evidence["exact_readback"].get(item["raw"]["external_id"])
        state = "hold_unknown"
        reason = "Readback missing or incomplete; no retry."
        if lookup and lookup.get("complete") is True:
            observed = lookup["records"]
            if any(r["external_id"] != item["raw"]["external_id"] for r in observed):
                raise ValueError("Readback contains a different external identity")
            expected_id = item["payload"]["record_id"]
            matches = (len(observed) == 1 and
                       all(observed[0].get(k) == v for k, v in item["intended"].items()) and
                       (not expected_id or observed[0]["record_id"] == expected_id))
            if receipt and receipt["result"] == "applied":
                if matches and observed[0]["record_id"] == receipt.get("record_id"):
                    state, reason = "confirmed_applied", "Success receipt and exact readback agree; exclude from retries."
                else:
                    state, reason = "hold_conflict", "Success receipt contradicts readback; inspect history before any retry."
            elif receipt and receipt["result"] == "rejected":
                before = item["before"]
                unchanged = (len(observed) == 1 and observed[0] == before) if before else not observed
                if unchanged:
                    state, reason = "confirmed_rejected", f"Service rejected: {receipt['error']}; revise and rehearse before resubmission."
                else:
                    state, reason = "hold_conflict", "Rejection and changed target state require investigation; no automatic retry."
            elif matches:
                state, reason = "observed_desired_state", "Desired state observed without success receipt; do not repeat effects."
            elif not observed and item["disposition"] == "create" and replay_valid:
                state = "safe_same_key_retry"
                reason = "Complete lookup is empty; replay is within documented retention with the identical payload/key and atomic uniqueness. Earlier application is not disproved."
            else:
                state, reason = "hold_conflict", "State differs, identity is duplicated, or replay protection expired; no automatic retry."
        results.append({"source_id": sid, "idempotency_key": item["idempotency_key"],
                        "payload_sha256": item["payload_sha256"], "status": state,
                        "reason": reason, "receipt": receipt, "readback": lookup})
    return {"evidence_kind": "synthetic, offline; no submission or retry performed",
            "batch_outcome": evidence["batch_outcome"], "evaluated_at": evidence["evaluated_at"],
            "counts": dict(Counter(r["status"] for r in results)), "operations": results}


def run(fixtures, output):
    contract_path = fixtures / "import-contract.json"
    source_path = fixtures / "source.csv"
    target_path = fixtures / "target-before.json"
    partial_path = fixtures / "partial-result.json"
    contract, target = load_json(contract_path), load_json(target_path)
    source_bytes = source_path.read_bytes()
    source_hash = digest(source_bytes)
    plan = make_plan(contract, target, source_bytes, digest(contract_path.read_bytes()))
    ready = [r for r in plan if r["disposition"] in ("create", "update")]
    expected_rows = [import_row(r, contract) for r in ready]
    keys = [r["external_id"] for r in expected_rows]
    if len(keys) != len(set(keys)):
        raise ValueError("Multiple operations target the same external identity")
    output.mkdir(parents=True, exist_ok=True)
    import_path = output / "import-ready.csv"
    with import_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=contract["import_headers"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(expected_rows)
    reread = parse_csv(import_path.read_bytes(), contract["import_headers"])
    if reread != expected_rows:
        raise ValueError("Saved import does not round-trip exactly")
    counts = {d: sum(r["disposition"] == d for r in plan) for d in DISPOSITIONS}
    summary = {"source_records": len(plan), "counts": counts, "import_ready_records": len(ready),
               "source_accounting_pass": sum(counts.values()) == len(plan),
               "import_accounting_pass": counts["create"] + counts["update"] == len(ready),
               "saved_csv_roundtrip_pass": True, "source_unchanged_pass": digest(source_path.read_bytes()) == source_hash,
               "target_export_complete": target["export_complete"],
               "coverage_limit": "Only listed complete exact-key lookups establish match cardinality or current absence.",
               "unresolved_lookup_source_ids": [r["source_id"] for r in plan if r["reason"] == "identity_lookup_incomplete"],
               "live_write_performed": False}
    if not summary["source_unchanged_pass"]:
        raise ValueError("Source changed during rehearsal")
    manifest = {"destination": contract["destination"], "adapter": contract["adapter"],
                "inputs": {p.name: digest(p.read_bytes()) for p in (contract_path, source_path, target_path, partial_path)},
                "source_id_namespace": "source SHA-256 plus logical CSV record ordinal",
                "import_ready_sha256": digest(import_path.read_bytes()),
                "snapshot_revision": target["snapshot_revision"], "retrieved_at": target["retrieved_at"]}
    rules = {
        "external_id": ("required", "required", "reject", "reject", "Exact text identity; no coercion or normalization"),
        "record_id": ("omit", "optional identity cross-check", "no existing record ID", "resolve by external_id", "Exact target ID; must agree with external_id"),
        "label": ("required", "optional", "reject", "preserve", "Exact text; clear token is rejected"),
        "status": ("optional", "optional", "default active", "preserve", "Exact active or retired; no aliases"),
        "details": ("optional", "optional", "null", "preserve", "Clear token sets null; other text is literal")
    }
    mapping = []
    for src, dst in contract["mapping"].items():
        create, update, blank_create, blank_update, conversion = rules[dst]
        mapping.append({"source": src, "target": dst, "type": "text" if dst != "details" else "nullable text",
                        "create_requirement": create, "update_requirement": update,
                        "blank_on_create": blank_create, "blank_on_update": blank_update,
                        "rule_source": "import-contract.json", "conversion": conversion})
    result = reconcile(plan, load_json(partial_path), contract)
    retry_ids = {r["source_id"] for r in result["operations"] if r["status"] == "safe_same_key_retry"}
    retry_rows = [r for r in reread if r["source_id"] in retry_ids]
    retry_path = output / "same-key-retry-candidate.csv"
    with retry_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=contract["import_headers"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(retry_rows)
    if parse_csv(retry_path.read_bytes(), contract["import_headers"]) != retry_rows:
        raise ValueError("Saved retry candidate does not preserve the original operation")
    manifest["same_key_retry_candidate_sha256"] = digest(retry_path.read_bytes())
    artifacts = {"manifest.json": manifest, "mapping.json": mapping, "operation-plan.json": plan,
                 "rejects-and-ambiguities.json": [r for r in plan if r["disposition"] in ("reject", "ambiguous")],
                 "reconciliation.json": summary, "partial-result-reconciliation.json": result}
    for filename, value in artifacts.items():
        write_json(output / filename, value)
        if load_json(output / filename) != value:
            raise ValueError(f"Saved JSON readback failed: {filename}")
    return summary, result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixtures", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    summary, partial = run(args.fixtures, args.output)
    print(json.dumps({"source_records": summary["source_records"], "dispositions": summary["counts"],
                      "import_ready_records": summary["import_ready_records"], "readback": partial["counts"],
                      "live_write_performed": False}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
