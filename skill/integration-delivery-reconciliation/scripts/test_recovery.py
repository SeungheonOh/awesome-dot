#!/usr/bin/env python3
"""Decision-regression checks against the bundled fictional evidence packet."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from check_recovery import reconcile, event_digest

PACKET = json.loads((Path(__file__).resolve().parent.parent / "fixtures" / "packet.json").read_text())


def decision(packet, eid):
    report, plan = reconcile(packet)
    return next(r for r in report["ledger"] if r["event_id"] == eid), plan


class RecoveryDecisions(unittest.TestCase):
    def test_baseline_accounting(self):
        report, plan = reconcile(PACKET)
        self.assertEqual(report["counts"]["source_events"], 8)
        self.assertEqual(report["counts"]["delivery_attempts"], 8)
        self.assertEqual(report["counts"]["observed_202_responses"], 7)
        self.assertEqual(report["counts"]["durable_receipts"], 6)
        self.assertEqual(report["counts"]["observed_processing_runs"], 8)
        self.assertEqual(report["counts"]["observed_committed_effects"], 4)
        self.assertEqual(sum(report["counts"]["outcomes"].values()), 8)
        self.assertEqual(plan["candidate_allowlist"], ["ev-002"])
        self.assertEqual(plan["live_changes_performed"], 0)
        self.assertEqual(plan["status"], "conditional_plan_only_not_executable")

    def test_acceptance_does_not_mean_applied(self):
        row, _ = decision(PACKET, "ev-002")
        self.assertEqual(row["outcome"], "terminal_not_applied")
        self.assertEqual(row["broken_boundary"], "transform_before_target_write")

    def test_duplicate_delivery_is_one_effect(self):
        row, _ = decision(PACKET, "ev-001")
        self.assertEqual(row["delivery_attempts"], 2)
        self.assertEqual(row["observed_committed_effects"], 1)
        self.assertEqual(row["disposition"], "no_replay")

    def test_one_delivery_can_have_two_effects(self):
        row, _ = decision(PACKET, "ev-007")
        self.assertEqual(row["delivery_attempts"], 1)
        self.assertEqual(row["outcome"], "duplicate_effect")
        self.assertEqual(row["disposition"], "hold_duplicate_cleanup")

    def test_newer_manual_edit_blocks_replay(self):
        row, _ = decision(PACKET, "ev-003")
        self.assertEqual(row["disposition"], "hold_newer_target")

    def test_tombstone_blocks_stale_update(self):
        row, _ = decision(PACKET, "ev-004")
        self.assertEqual(row["disposition"], "hold_tombstone")
        applied, _ = decision(PACKET, "ev-005")
        self.assertEqual(applied["outcome"], "applied_once")

    def test_matching_target_without_lineage_stays_unknown(self):
        row, _ = decision(PACKET, "ev-006")
        self.assertEqual(row["target_ids"], ["LT-106"])
        self.assertEqual(row["disposition"], "hold_unknown")

    def test_unsent_is_not_a_replay(self):
        row, _ = decision(PACKET, "ev-008")
        self.assertEqual(row["outcome"], "not_dispatched")
        self.assertEqual(row["disposition"], "hold_first_delivery")

    def test_missing_effect_coverage_holds_candidate(self):
        packet = deepcopy(PACKET)
        packet["coverage"]["effect_complete_events"].remove("ev-002")
        row, plan = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_unknown")
        self.assertEqual(plan["candidate_allowlist"], [])

    def test_pending_retry_holds_candidate(self):
        packet = deepcopy(PACKET)
        packet["runs"][2]["retry_state"] = "scheduled"
        row, plan = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_pending")
        self.assertEqual(plan["candidate_allowlist"], [])

    def test_source_changed_holds_candidate(self):
        packet = deepcopy(PACKET)
        packet["source_current"][1]["version"] = 2
        row, _ = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_superseded")

    def test_incomplete_target_lookup_holds_candidate(self):
        packet = deepcopy(PACKET)
        packet["coverage"]["target_lookup_complete_entities"].remove("CR-102")
        row, _ = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_target_lookup")

    def test_new_target_holds_candidate(self):
        packet = deepcopy(PACKET)
        packet["targets"].append({"row_id": "T02NEW", "target_id": "LT-102", "entity_id": "CR-102", "revision": 1,
                                  "origin_event": None, "last_editor": "human"})
        row, _ = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_existing_target")

    def test_receipt_presence_does_not_prove_durability(self):
        for state, boundary, durable_ids in (("pending", "receipt_observed", []),
                                            ("durable", "durable_receipt", ["ib-006"])):
            with self.subTest(state=state):
                packet = deepcopy(PACKET)
                packet["receipts"].append({"row_id": "I06", "receipt_id": "ib-006",
                                            "event_id": "ev-006", "state": state})
                row, plan = decision(packet, "ev-006")
                self.assertEqual(row["highest_evidenced_boundary"], boundary)
                self.assertEqual(row["durable_receipt_ids"], durable_ids)
                self.assertEqual(row["disposition"], "hold_unknown")
                self.assertNotIn("ev-006", plan["candidate_allowlist"])

    def test_missing_receipt_does_not_get_filled_in(self):
        packet = deepcopy(PACKET)
        packet["receipts"] = [r for r in packet["receipts"] if r["event_id"] != "ev-002"]
        row, _ = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_unknown")
        self.assertTrue(row["linkage_issues"])

    def test_wrong_run_parent_is_a_conflict(self):
        packet = deepcopy(PACKET)
        packet["effects"][0]["run_id"] = "run-005"
        row, _ = decision(packet, "ev-001")
        self.assertEqual(row["disposition"], "hold_unknown")

    def test_orphaned_effect_is_preserved(self):
        packet = deepcopy(PACKET)
        orphan = deepcopy(packet["effects"][0])
        orphan.update(row_id="E99", effect_id="tx-099", event_id="ev-099")
        packet["effects"].append(orphan)
        report, _ = reconcile(packet)
        self.assertEqual(report["orphaned_downstream"], [{"collection": "effects", "row_id": "E99", "event_id": "ev-099"}])
        self.assertEqual(report["counts"]["observed_committed_effects"], 5)

    def test_orphan_effect_conflicting_with_candidate_run_blocks_it(self):
        packet = deepcopy(PACKET)
        packet["effects"].append({"row_id": "E99", "effect_id": "tx-099", "event_id": "ev-099",
                                   "run_id": "run-002", "target_id": "LT-999", "action": "create",
                                   "committed": True, "at": "2026-05-12T09:01:03Z"})
        row, plan = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_unknown")
        self.assertEqual(plan["candidate_allowlist"], [])
        self.assertIn("packet.json#E99", row["evidence"])

    def test_ambiguous_identity_is_rejected(self):
        packet = deepcopy(PACKET)
        duplicate = deepcopy(packet["events"][1])
        duplicate.update(row_id="S02CONFLICT", version=2)
        packet["events"].append(duplicate)
        with self.assertRaisesRegex(ValueError, "event_id"):
            reconcile(packet)

    def test_changed_readback_is_not_claimed_verified(self):
        for change in ({"status": "Done"}, {"source_version": 0}, {"title": "Different task"}):
            with self.subTest(change=change):
                packet = deepcopy(PACKET)
                packet["targets"][0].update(change)
                row, _ = decision(packet, "ev-001")
                self.assertEqual(row["disposition"], "hold_unknown")

    def test_committed_action_must_match_event(self):
        packet = deepcopy(PACKET)
        packet["effects"][0]["action"] = "update"
        row, _ = decision(packet, "ev-001")
        self.assertEqual(row["disposition"], "hold_unknown")

    def test_conflicting_target_provenance_blocks_candidate(self):
        packet = deepcopy(PACKET)
        packet["targets"].append({"row_id": "T99", "target_id": "LT-999", "entity_id": "CR-999",
                                  "revision": 1, "source_version": 1, "origin_event": "ev-002",
                                  "title": "Asset handoff", "status": "Open", "last_editor": "integration"})
        row, plan = decision(packet, "ev-002")
        report, _ = reconcile(packet)
        self.assertEqual(row["disposition"], "hold_unknown")
        self.assertEqual(plan["candidate_allowlist"], [])
        self.assertEqual(report["orphaned_downstream"][0]["row_id"], "T99")
        self.assertIn("packet.json#T99", row["evidence"])

    def test_unmatched_tombstone_is_preserved(self):
        packet = deepcopy(PACKET)
        packet["tombstones"].append({"row_id": "TB99", "target_id": "LT-999", "entity_id": "CR-999",
                                     "revision": 1, "source_version": 1, "origin_event": "pre-window"})
        report, _ = reconcile(packet)
        self.assertEqual(report["orphaned_downstream"][0]["row_id"], "TB99")

    def test_multiple_retained_receipts_block_candidate(self):
        packet = deepcopy(PACKET)
        packet["receipts"].append({"row_id": "I02SECOND", "receipt_id": "ib-002-second",
                                    "event_id": "ev-002", "state": "durable"})
        row, plan = decision(packet, "ev-002")
        self.assertEqual(row["disposition"], "hold_unknown")
        self.assertEqual(plan["candidate_allowlist"], [])
        self.assertEqual(row["durable_receipt_ids"], ["ib-002", "ib-002-second"])

    def test_digest_changes_with_payload(self):
        original = PACKET["events"][1]
        changed = deepcopy(original)
        changed["payload"]["title"] = "A different task"
        self.assertNotEqual(event_digest(original), event_digest(changed))

    def test_input_packet_is_not_mutated(self):
        original = deepcopy(PACKET)
        reconcile(PACKET)
        self.assertEqual(PACKET, original)


if __name__ == "__main__":
    unittest.main(verbosity=2)
