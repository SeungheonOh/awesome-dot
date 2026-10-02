#!/usr/bin/env python3
"""Check the fictional packet's lineage and recovery decisions; no service I/O.

This deliberately supports only the bundled schema and one-effect-per-event
contract. It is not a product connector, replay runner or idempotency proof.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COLLECTIONS = ("events", "source_current", "dispatch", "deliveries", "receipts",
               "runs", "effects", "targets", "tombstones")


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                            ensure_ascii=False).encode("utf-8")).hexdigest()


def event_digest(event):
    return digest({k: v for k, v in event.items() if k != "row_id"})


def unique(rows, key):
    values = [r[key] for r in rows]
    if len(values) != len(set(values)):
        raise ValueError(f"Conflicting or repeated {key}; preserve and resolve identity first")
    return {r[key]: r for r in rows}


def reconcile(packet):
    if packet.get("fictional") is not True:
        raise ValueError("This helper only accepts the explicitly fictional example schema")
    if not packet["scope"].get("source_events_complete"):
        raise ValueError("Incomplete source population; this helper cannot produce a full ledger")
    all_rows = [r for collection in COLLECTIONS for r in packet[collection]]
    unique(all_rows, "row_id")
    event_by_id = unique(packet["events"], "event_id")
    current = unique(packet["source_current"], "entity_id")
    dispatch = unique(packet["dispatch"], "event_id")
    receipt_by_id = unique(packet["receipts"], "receipt_id")
    run_by_id = unique(packet["runs"], "run_id")
    unique(packet["deliveries"], "attempt_id")
    unique(packet["effects"], "effect_id")
    unique(packet["targets"] + packet["tombstones"], "target_id")
    coverage = packet["coverage"]
    orphaned = []
    for name in ("dispatch", "deliveries", "receipts", "runs", "effects"):
        orphaned.extend({"collection": name, "row_id": r["row_id"],
                         "event_id": r["event_id"]}
                        for r in packet[name] if r["event_id"] not in event_by_id)
    entity_ids = {r["entity_id"] for r in packet["events"]}
    provenance_conflicts = {}
    for name, parent_key, parents in (("deliveries", "receipt_id", receipt_by_id),
                                      ("runs", "receipt_id", receipt_by_id),
                                      ("effects", "run_id", run_by_id)):
        for row in packet[name]:
            parent = parents.get(row[parent_key])
            if parent is not None and parent["event_id"] != row["event_id"]:
                for related_event in {parent["event_id"], row["event_id"]}:
                    provenance_conflicts.setdefault(related_event, []).append(row)
    for name in ("targets", "tombstones"):
        for row in packet[name]:
            origin = row["origin_event"]
            origin_event = event_by_id.get(origin)
            conflicts = origin_event is not None and origin_event["entity_id"] != row["entity_id"]
            if row["entity_id"] not in entity_ids or conflicts:
                orphaned.append({"collection": name, "row_id": row["row_id"],
                                 "event_id": origin, "entity_id": row["entity_id"],
                                 "target_id": row["target_id"],
                                 "reason": "unmatched entity or conflicting originating-event identity"})
            if conflicts:
                provenance_conflicts.setdefault(origin, []).append(row)
                for event in packet["events"]:
                    if event["entity_id"] == row["entity_id"]:
                        provenance_conflicts.setdefault(event["event_id"], []).append(row)
    ledger, candidates = [], []
    for event in packet["events"]:
        eid, entity = event["event_id"], event["entity_id"]
        deliveries = [r for r in packet["deliveries"] if r["event_id"] == eid]
        receipts = [r for r in packet["receipts"] if r["event_id"] == eid]
        runs = [r for r in packet["runs"] if r["event_id"] == eid]
        effects = [r for r in packet["effects"] if r["event_id"] == eid]
        committed = [r for r in effects if r["committed"] is True]
        targets = [r for r in packet["targets"] if r["entity_id"] == entity]
        tombstones = [r for r in packet["tombstones"] if r["entity_id"] == entity]
        state, source_now = dispatch.get(eid), current.get(entity)
        worker_complete = eid in coverage["worker_complete_events"]
        effect_complete = eid in coverage["effect_complete_events"]
        target_complete = entity in coverage["target_lookup_complete_entities"]
        current_complete = entity in coverage["source_current_complete_entities"]
        conflict_rows = provenance_conflicts.get(eid, [])
        linkage_issues = [f'{r["row_id"]}: event identity conflicts across linked evidence'
                          for r in conflict_rows]
        if len(receipts) > 1:
            linkage_issues.append("Multiple retained receipts conflict with the stated ingress identity contract")
        for delivery in deliveries:
            rid = delivery["receipt_id"]
            if rid is not None and (rid not in receipt_by_id or receipt_by_id[rid]["event_id"] != eid):
                linkage_issues.append(f'{delivery["row_id"]}: missing or conflicting receipt')
        for run in runs:
            rid = run["receipt_id"]
            if rid not in receipt_by_id or receipt_by_id[rid]["event_id"] != eid:
                linkage_issues.append(f'{run["row_id"]}: missing or conflicting receipt')
        for effect in effects:
            rid = effect["run_id"]
            if rid not in run_by_id or run_by_id[rid]["event_id"] != eid:
                linkage_issues.append(f'{effect["row_id"]}: missing or conflicting run')
        if state and set(state["delivery_ids"]) != {r["attempt_id"] for r in deliveries}:
            linkage_issues.append(f'{state["row_id"]}: dispatch/delivery identity mismatch')
        if state and state["state"] == "unsent" and (deliveries or receipts or runs or effects):
            linkage_issues.append(f'{state["row_id"]}: unsent conflicts with downstream evidence')
        pending = any(r["retry_state"] != "none" or r["status"] not in
                      {"applied", "duplicate_suppressed", "dead_letter"} for r in runs)
        readback = []
        for effect in committed:
            collection = tombstones if effect["action"] == "delete" else targets
            matches = [t for t in collection if t["target_id"] == effect["target_id"]
                       and t["origin_event"] == eid and t.get("source_version") == event["version"]]
            action_matches = effect["action"] == event["type"]
            if effect["action"] != "delete":
                expected_status = packet["contract"]["transform_v1"].get(event["payload"].get("status"))
                matches = [t for t in matches if expected_status is not None
                           and t.get("title") == event["payload"].get("title")
                           and t.get("status") == expected_status]
            readback.append(action_matches and bool(matches))
        durable = any(r["state"] == "durable" for r in receipts)
        # Gaps and contradictory joins must not be promoted to safe replay.
        if linkage_issues:
            outcome = "unknown_conflicting"
        elif len(committed) > 1 and all(readback) and target_complete:
            outcome = "duplicate_effect"
        elif pending:
            outcome = "pending"
        elif len(committed) == 1 and all(readback) and effect_complete and target_complete:
            outcome = "applied_once"
        elif (durable and runs and worker_complete and effect_complete and not effects
              and all(r["status"] == "dead_letter" and r["phase"] == "transform"
                      and r["handler"] == "worker-1" for r in runs)):
            outcome = "terminal_not_applied"
        elif (state and state["state"] == "unsent" and coverage["source_dispatch_complete"]
              and not deliveries and not receipts and not runs and not effects):
            outcome = "not_dispatched"
        else:
            outcome = "unknown_conflicting"

        if outcome == "applied_once":
            disposition, reason = "no_replay", "One committed effect with corroborating target/deletion readback"
        elif outcome == "duplicate_effect":
            disposition, reason = "hold_duplicate_cleanup", "Two committed creates and two targets; preserve independent comments and decide cleanup separately"
        elif outcome == "pending":
            disposition, reason = "hold_pending", "An active run or automatic retry may still produce an effect"
        elif outcome == "not_dispatched":
            disposition, reason = "hold_first_delivery", "Initial delivery is a distinct operation requiring its own validated scope"
        elif outcome == "unknown_conflicting":
            disposition, reason = "hold_unknown", "Missing, conflicting or incomplete lineage/effect evidence; matching values do not prove origin"
        elif not current_complete or source_now is None:
            disposition, reason = "hold_source_lookup", "Current source identity/version is not authoritatively established"
        elif tombstones:
            disposition, reason = "hold_tombstone", "A deletion marker protects this entity from stale recreation"
        elif source_now["deleted"] or source_now["version"] != event["version"] or source_now["event_id"] != eid:
            disposition, reason = "hold_superseded", "Current source identity/version differs from the event"
        elif not target_complete:
            disposition, reason = "hold_target_lookup", "Target absence, uniqueness or deletion state is not authoritatively established"
        elif len(targets) > 1:
            disposition, reason = "hold_duplicate_target", "Source identity resolves to multiple target records"
        elif event["type"] == "create" and targets:
            disposition, reason = "hold_existing_target", "Target already exists; terminal failure does not authorize another create"
        elif event["type"] == "update" and (len(targets) != 1 or targets[0]["revision"] != event.get("expected_target_revision") or targets[0]["last_editor"] == "human"):
            disposition, reason = "hold_newer_target", "Expected target revision is stale or a human edit must be preserved"
        elif event["type"] != "create":
            disposition, reason = "hold_unsupported_operation", "This bounded example checker proposes only absent-target creates"
        elif event["payload"].get("status") not in packet["contract"]["proposed_transform_v2"]:
            disposition, reason = "hold_unmapped", "Proposed mapping does not define the event status"
        elif eid in coverage["delivery_receipt_gap_events"]:
            disposition, reason = "hold_unknown", "Receiver coverage is incomplete"
        else:
            disposition, reason = "candidate_after_fix", "Evidence supports one absent-target create after mapping repair and atomic recovery guards are implemented and verified"
            candidates.append({
                "event_id": eid, "entity_id": entity, "source_event_sha256": event_digest(event),
                "receipt_id": receipts[0]["receipt_id"], "prior_run_ids": [r["run_id"] for r in runs],
                "operation": "create", "proposed_route": "retry_dead_letter_v2",
                "expected_source": {"version": event["version"], "event_id": eid, "deleted": False},
                "expected_target": {"matching_records": 0, "tombstones": 0},
                "intended_values": {"external_source_id": entity, "title": event["payload"]["title"],
                                    "status": packet["contract"]["proposed_transform_v2"][event["payload"]["status"]]},
                "still_required": ["Implement and verify transformation and guarded recovery route in the actual authorized environment",
                                   "Obtain authority for this one-event live recovery and its effects",
                                   "Refresh source, job ownership, effects, target absence and tombstone state",
                                   "Enforce preconditions atomically when writing; retain one recovery operation identity",
                                   "Read terminal receipt, exact target identity count and effect journal before declaring recovery"]})
        if committed and all(readback):
            boundary = "target_effect_readback"
        elif runs:
            boundary = "processing_run"
        elif durable:
            boundary = "durable_receipt"
        elif receipts:
            boundary = "receipt_observed"
        elif deliveries:
            boundary = "delivery_attempt"
        else:
            boundary = "source_dispatch"
        if outcome == "terminal_not_applied":
            broken_boundary = "transform_before_target_write"
        elif outcome == "duplicate_effect":
            broken_boundary = "single_event_effect_uniqueness"
        elif outcome == "not_dispatched":
            broken_boundary = "source_to_delivery"
        else:
            broken_boundary = None
        evidence_rows = [event] + ([state] if state else []) + deliveries + receipts + runs + effects + targets + tombstones + ([source_now] if source_now else []) + conflict_rows
        ledger.append({"event_id": eid, "entity_id": entity, "source_version": event["version"],
                       "delivery_attempts": len(deliveries), "durable_receipt_ids": [r["receipt_id"] for r in receipts if r["state"] == "durable"],
                       "run_ids": [r["run_id"] for r in runs], "observed_committed_effects": len(committed),
                       "target_ids": [r["target_id"] for r in targets], "tombstone_ids": [r["target_id"] for r in tombstones],
                       "highest_evidenced_boundary": boundary, "broken_boundary": broken_boundary,
                       "outcome": outcome, "disposition": disposition, "reason": reason,
                       "linkage_issues": linkage_issues,
                       "evidence": [f'packet.json#{r["row_id"]}' for r in evidence_rows] + ["packet.json#C01", "packet.json#CV01"]})
    counts = {"source_events": len(packet["events"]), "source_entities": len({r["entity_id"] for r in packet["events"]}),
              "delivery_attempts": len(packet["deliveries"]), "observed_202_responses": sum(r["response"] == 202 for r in packet["deliveries"]),
              "transport_timeouts": sum(r["response"] == "timeout" for r in packet["deliveries"]),
              "durable_receipts": sum(r["state"] == "durable" for r in packet["receipts"]),
              "observed_processing_runs": len(packet["runs"]), "observed_committed_effects": sum(r["committed"] is True for r in packet["effects"]),
              "active_target_records": len(packet["targets"]), "active_target_source_entities": len({r["entity_id"] for r in packet["targets"]}),
              "deletion_markers": len(packet["tombstones"]), "orphaned_downstream_rows": len(orphaned),
              "outcomes": dict(sorted(Counter(r["outcome"] for r in ledger).items()))}
    plan = {"fictional": True, "packet_id": packet["packet_id"], "as_of": packet["scope"]["as_of"],
            "status": "conditional_plan_only_not_executable", "live_changes_performed": 0,
            "destination": {key: packet["scope"][key] for key in ("source_account", "target_project", "integration_id")},
            "candidate_allowlist": [r["event_id"] for r in candidates], "maximum_recovery_events": len(candidates),
            "candidates": candidates, "excluded_events": [{"event_id": r["event_id"], "disposition": r["disposition"], "reason": r["reason"]} for r in ledger if r["disposition"] != "candidate_after_fix"],
            "stop_conditions": ["Any prerequisite or immutable event changes", "Any active retry or ambiguous effect appears", "Unexpected target, tombstone or target revision", "Scope or side effects expand", "The real route lacks a necessary atomic guard", "Terminal result or target readback is unknown"]}
    return {"fictional": True, "packet_id": packet["packet_id"], "as_of": packet["scope"]["as_of"], "counts": counts,
            "ledger": ledger, "orphaned_downstream": orphaned, "limits": [coverage["gap"], "No real handler, API, atomic guard or recovery was executed"]}, plan


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=ROOT / "fixtures" / "packet.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = args.packet.read_bytes()
    report, plan = reconcile(json.loads(data))
    for output in (report, plan):
        output["input_sha256"] = sha256(data).hexdigest()
    args.output.mkdir(parents=True, exist_ok=True)
    for filename, value in (("reconciliation.json", report), ("recovery-plan.json", plan)):
        (args.output / filename).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"source_events": report["counts"]["source_events"],
                      "outcomes": report["counts"]["outcomes"], "candidate_allowlist": plan["candidate_allowlist"],
                      "status": plan["status"], "live_changes_performed": 0}, sort_keys=True))


if __name__ == "__main__":
    main()
