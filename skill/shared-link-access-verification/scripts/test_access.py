"""Behavioral checks for permission uncertainty, evidence and scoped changes."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from evaluate_access import evaluate, matrix, review_delta

ROOT = Path(__file__).resolve().parent.parent


class AccessTests(unittest.TestCase):
    def setUp(self):
        self.before = json.loads((ROOT / "fixtures/before.json").read_text())
        self.after = json.loads((ROOT / "fixtures/after.json").read_text())
        self.request = json.loads((ROOT / "fixtures/request.json").read_text())
        self.people = {p["account"].split("@")[0]: p for p in self.request["recipients"]}

    def row(self, person, snapshot=None):
        return evaluate(self.after if snapshot is None else snapshot, self.people[person])

    def test_baseline_distinguishes_all_four_outcomes(self):
        self.assertEqual([r["permission"] for r in matrix(self.before, self.request)["recipients"]],
                         ["confirmed", "absent", "unknown", "blocked"])

    def test_approved_direct_grant_and_recipient_report(self):
        row = self.row("dana")
        self.assertEqual(row["permission"], "confirmed")
        self.assertEqual(row["recipient_opening"]["status"], "reported_success")

    def test_owner_open_is_not_recipient_proof(self):
        row = self.row("priya", self.before)
        self.assertEqual(row["permission"], "confirmed")
        self.assertEqual(row["recipient_opening"]["status"], "untested")

    def test_link_restriction_preserves_inherited_editor(self):
        person = self.request["incidental_access_check"]
        before, after = evaluate(self.before, person), evaluate(self.after, person)
        self.assertEqual(after["permission"], "confirmed")
        self.assertIn("edit", after["grant_capability_floor"])
        self.assertIn("link", [r["origin"] for r in before["confirmed_routes"]])
        self.assertEqual([r["origin"] for r in after["confirmed_routes"]], ["folder"])

    def test_unknown_group_membership_is_not_absent(self):
        self.assertEqual(self.row("morgan")["permission"], "unknown")

    def test_known_nonmember_can_be_absent(self):
        self.after["memberships"]["review-circle"][self.people["morgan"]["account"]] = "no"
        self.assertEqual(self.row("morgan")["permission"], "absent")

    def test_missing_membership_evidence_remains_unknown(self):
        del self.after["memberships"]["review-circle"]
        self.assertEqual(self.row("morgan")["permission"], "unknown")

    def test_known_member_gets_group_capabilities(self):
        self.after["memberships"]["review-circle"][self.people["morgan"]["account"]] = "yes"
        self.assertEqual(self.row("morgan")["permission"], "confirmed")
        self.assertIn("comment", self.row("morgan")["grant_capability_floor"])

    def test_known_view_with_unknown_higher_role(self):
        self.after["memberships"]["review-circle"][self.people["priya"]["account"]] = "unknown"
        self.after["grants"][1]["role"] = "editor"
        row = self.row("priya")
        self.assertEqual(row["permission"], "confirmed")
        self.assertEqual(row["grant_capability_floor"], ["view"])
        self.assertEqual(row["additional_possible_capabilities"], ["comment", "edit"])
        self.people["priya"]["capability"] = "edit"
        self.assertEqual(self.row("priya")["permission"], "unknown")

    def test_viewer_cannot_be_claimed_editor(self):
        self.people["priya"]["capability"] = "edit"
        self.assertEqual(self.row("priya")["permission"], "absent")

    def test_policy_block_overrides_shared_drive_grant(self):
        row = self.row("lee")
        self.assertEqual(row["permission"], "blocked")
        self.assertEqual(row["confirmed_routes"][0]["origin"], "shared_drive")

    def test_unknown_policy_does_not_confirm_known_grant(self):
        self.after["policy"][self.people["priya"]["account"]] = "unknown"
        self.assertEqual(self.row("priya")["permission"], "unknown")

    def test_wrong_current_account_is_separate_from_entitlement(self):
        self.after["sessions"][self.people["dana"]["account"]] = "unintended@guest.example"
        row = self.row("dana")
        self.assertEqual(row["permission"], "confirmed")
        self.assertEqual(row["session"], "wrong_account")

    def test_expiration_boundary_removes_grant(self):
        self.after["grants"][-1]["expires_at"] = self.after["captured_at"]
        self.assertEqual(self.row("dana")["permission"], "absent")

    def test_pending_invitation_is_not_active_grant(self):
        self.after["grants"][-1]["active"] = False
        self.assertEqual(self.row("dana")["permission"], "absent")

    def test_partial_route_coverage_cannot_prove_absence(self):
        self.before["coverage"] = "partial"
        self.assertEqual(self.row("dana", self.before)["permission"], "unknown")

    def test_inapplicable_observation_is_excluded(self):
        cases = [("file_id", "another-file"), ("account", "owner@studio.example"),
                 ("session_account", "other@guest.example"), ("permission_revision", "perm-11"),
                 ("action", "edit"), ("observed_at", "2026-09-19T00:00:00Z")]
        for field, value in cases:
            with self.subTest(field=field):
                changed = deepcopy(self.after)
                changed["observations"][-1][field] = value
                self.assertEqual(self.row("dana", changed)["recipient_opening"]["status"], "untested")

    def test_current_denial_is_not_successful_opening(self):
        self.after["observations"][-1]["result"] = "denied"
        row = self.row("dana")
        self.assertEqual(row["recipient_opening"]["status"], "failed")
        self.assertTrue(row["evidence_conflict"])

    def test_conflicting_current_observations_are_held(self):
        other = deepcopy(self.after["observations"][-1])
        other["result"] = "denied"
        self.after["observations"].append(other)
        row = self.row("dana")
        self.assertEqual(row["recipient_opening"]["status"], "conflicting")
        self.assertTrue(row["evidence_conflict"])

    def test_exact_approved_delta_and_input_preservation(self):
        before, after, request = deepcopy(self.before), deepcopy(self.after), deepcopy(self.request)
        self.assertEqual(review_delta(before, after, request)["status"], "matches_fictional_approval")
        self.assertEqual((before, after, request), (self.before, self.after, self.request))

    def test_ancestor_grant_removal_is_outside_approval(self):
        self.after["grants"] = [g for g in self.after["grants"] if g["id"] != "grant-casey"]
        self.assertEqual(review_delta(self.before, self.after, self.request)["status"], "held")

    def test_public_link_is_outside_approval(self):
        self.after["link"]["audience"] = "anyone"
        self.assertEqual(review_delta(self.before, self.after, self.request)["status"], "held")

    def test_substituted_recipient_is_outside_approval(self):
        self.after["grants"][-1]["principal"] = "dana.personal@guest.example"
        self.assertEqual(review_delta(self.before, self.after, self.request)["status"], "held")

    def test_content_version_change_invalidates_comparison(self):
        self.after["file"]["content_revision"] = "content-8"
        with self.assertRaises(ValueError):
            review_delta(self.before, self.after, self.request)

    def test_unknown_grant_source_rejects_packet(self):
        self.after["grants"][0]["source_id"] = "unlisted-folder"
        with self.assertRaises(ValueError):
            self.row("priya")

    def test_duplicate_grant_identity_rejects_packet(self):
        self.after["grants"].append(deepcopy(self.after["grants"][0]))
        with self.assertRaises(ValueError):
            self.row("priya")

    def test_unknown_link_possession_is_unknown_route(self):
        self.before["link"]["audience"] = "anyone"
        self.people["dana"]["has_link"] = "unknown"
        self.assertEqual(self.row("dana", self.before)["permission"], "unknown")

    def test_organization_link_does_not_grant_known_external_user(self):
        self.assertEqual(self.row("dana", self.before)["permission"], "absent")
        self.before["link"]["audience"] = "anyone"
        self.assertEqual(self.row("dana", self.before)["permission"], "confirmed")

    def test_unapproved_notification_is_held(self):
        self.after["notifications_sent"] = True
        self.assertEqual(review_delta(self.before, self.after, self.request)["status"], "held")

    def test_added_account_must_be_in_approved_data_audience(self):
        self.request["recipients"] = [r for r in self.request["recipients"] if r["account"] != "dana@guest.example"]
        self.assertEqual(review_delta(self.before, self.after, self.request)["status"], "held")

    def test_nonfictional_input_is_rejected(self):
        self.request["fictional"] = False
        with self.assertRaises(ValueError):
            matrix(self.after, self.request)

    def test_broader_correction_contract_is_rejected(self):
        self.request["approved_changes"]["link_audience"] = "anyone"
        with self.assertRaises(ValueError):
            review_delta(self.before, self.after, self.request)


if __name__ == "__main__":
    unittest.main()
