"""All test data and subprocess output here are authored synthetic fixtures."""
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest

from dot_eval.core import IntegrityError, Ledger, create_json, digest, file_manifest, file_sha, load_json, relative_path
from dot_eval.execution import RuntimeGateError, codex_argv, run_fixture, run_live
from dot_eval.grading import blind_export, import_grade, normalize_grade, resolve_grades
from dot_eval.protocol import freeze, initialize, prepare, schedule, verify
from dot_eval.reporting import cluster_interval, report, summarize
from dot_eval.telemetry import CodexEvents

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/fixture_only"


class StudyCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.assets = self.root / "assets"
        shutil.copytree(EXAMPLE, self.assets)
        self.config = load_json(self.assets / "config.json")

    def tearDown(self):
        self.temp.cleanup()

    def make(self, n=1, repetitions=1):
        self.config["tasks"] = [dict(self.config["tasks"][0], task_id=f"task{i}", family_id=f"F{i}") for i in range(n)]
        self.config["repetitions"] = repetitions
        (self.assets / "config.json").write_text(json.dumps(self.config))
        self.protocol = freeze(self.assets / "config.json", self.root / "frozen.json")
        self.plan = schedule(self.protocol, 42)
        self.study = initialize(self.protocol, self.plan, self.root / "study")
        return self.study


class ProtocolTests(StudyCase):
    def test_hashes_and_readback(self):
        self.make()
        self.assertTrue(verify(load_json(self.root / "frozen.json")))
        self.assertEqual(len(self.protocol["runner_sha256"]), 64)
        with self.assertRaises(FileExistsError):
            freeze(self.assets / "config.json", self.root / "frozen.json")

    def test_asset_mutation_detected(self):
        self.make()
        (self.assets / "source.txt").write_text("changed")
        with self.assertRaises(IntegrityError):
            verify(self.protocol)

    def test_protocol_mutation_detected(self):
        self.make()
        self.protocol["common_instruction"] += " changed"
        with self.assertRaises(IntegrityError):
            verify(self.protocol)

    def test_balanced_paired_schedule_separates_repeat_rounds(self):
        self.make(8, 2)
        rows = self.plan["rows"]
        self.assertEqual(len(rows), 32)
        self.assertEqual(self.plan, schedule(self.protocol, 42))
        for repetition in (1, 2):
            first = [r for r in rows if r["repetition"] == repetition and r["within_pair_position"] == 1]
            self.assertEqual(sum(r["arm"] == "C" for r in first), 4)
        self.assertEqual([r["repetition"] for r in rows], [1] * 16 + [2] * 16)

    def test_task_packet_contains_only_allowlisted_inputs_and_s_guide(self):
        self.make()
        prepared = [prepare(self.study, row["attempt_id"]) for row in self.plan["rows"]]
        self.assertNotEqual(prepared[0]["workspace"], prepared[1]["workspace"])
        for row, item in zip(self.plan["rows"], prepared):
            files = {f["path"] for f in file_manifest(item["workspace"])}
            expected = {"task.txt", "inputs/source.txt"} | ({"guide.md"} if row["arm"] == "S" else set())
            self.assertEqual(files, expected)
            self.assertNotIn("grader.py", files)
            self.assertNotIn("oracle.json", files)
        self.assertEqual(prepared[0]["common_task_sha256"], prepared[1]["common_task_sha256"])

    def test_no_overwrite_attempt(self):
        self.make()
        prepare(self.study, "a0001")
        with self.assertRaises(IntegrityError):
            prepare(self.study, "a0001")

    def test_not_run_report_does_not_claim_zero_percent_effect(self):
        self.make()
        result = report(self.study)
        self.assertEqual(result["study_status"], "not_run")
        self.assertIsNone(result["primary"]["effect_estimate"])
        self.assertIsNone(result["families"][0]["arms"]["C"]["observed_acceptance"])

    def test_public_root_packet_file_preserved(self):
        (self.assets / "input-manifest.json").write_text('{"public":true}')
        self.config["tasks"][0]["packet_files"] = [{"source": "input-manifest.json", "target": "input-manifest.json"}]
        self.make()
        metadata = prepare(self.study, "a0001")
        self.assertEqual((Path(metadata["workspace"]) / "input-manifest.json").read_text(), '{"public":true}')

    def test_nonfixture_review_gate(self):
        self.config["stage"] = "smoke"
        (self.assets / "config.json").write_text(json.dumps(self.config))
        with self.assertRaises(IntegrityError):
            freeze(self.assets / "config.json", self.root / "frozen.json")

    def test_bad_paths_and_symlinks(self):
        for value in ("../answer", "/tmp/file", "a/../b", "a//b", "a\\b", ""):
            with self.assertRaises(IntegrityError):
                relative_path(value)
        (self.assets / "evil").symlink_to(self.assets / "source.txt")
        self.config["tasks"][0]["inputs"][0]["source"] = "evil"
        (self.assets / "config.json").write_text(json.dumps(self.config))
        with self.assertRaises(IntegrityError):
            freeze(self.assets / "config.json", self.root / "frozen.json")

    def test_package_treatment_preserves_exact_layout_only_for_s(self):
        (self.assets / "companion.txt").write_text("AUTHORED SYNTHETIC COMPANION; not a model answer")
        (self.assets / "support.txt").write_text("AUTHORED COMMON SUPPORT")
        self.config["treatment"] = "designated_skill_package_supplied"
        self.config["common_support_files"] = [{"source": "support.txt", "target": "common_support/support.txt", "sha256": file_sha(self.assets / "support.txt")}]
        self.config["tasks"][0]["skill_package"] = {"guide_target": "skill/synthetic/SKILL.md", "files": [
            {"source": "guide.md", "target": "skill/synthetic/SKILL.md", "sha256": file_sha(self.assets / "guide.md")},
            {"source": "companion.txt", "target": "skill/synthetic/examples/companion.txt", "sha256": file_sha(self.assets / "companion.txt")} ]}
        self.make()
        for row in self.plan["rows"]:
            metadata = prepare(self.study, row["attempt_id"])
            files = {f["path"] for f in file_manifest(metadata["workspace"])}
            self.assertIn("common_support/support.txt", files)
            self.assertNotIn("guide.md", files)
            package_paths = {p for p in files if p.startswith("skill/")}
            self.assertEqual(package_paths, {"skill/synthetic/SKILL.md", "skill/synthetic/examples/companion.txt"} if row["arm"] == "S" else set())
            self.assertEqual(metadata["treatment"], "designated_skill_package_supplied")
            result = run_fixture(self.study, row["attempt_id"])
            self.assertTrue(result["canonical_package_sources_unchanged"])

    def test_package_neighbor_expansion_is_rejected(self):
        self.config["treatment"] = "designated_skill_package_supplied"
        self.config["tasks"][0]["skill_package"] = {"guide_target": "skill/synthetic/SKILL.md", "files": [
            {"source": "guide.md", "target": "skill/neighbor/SKILL.md", "sha256": file_sha(self.assets / "guide.md")}]}
        with self.assertRaises(IntegrityError):
            self.make()

    def test_package_hash_mismatch_is_rejected(self):
        self.config["treatment"] = "designated_skill_package_supplied"
        self.config["tasks"][0]["skill_package"] = {"guide_target": "skill/synthetic/SKILL.md", "files": [
            {"source": "guide.md", "target": "skill/synthetic/SKILL.md", "sha256": "0" * 64}]}
        with self.assertRaises(IntegrityError):
            self.make()

    def test_source_inspection_is_not_an_execution_freeze(self):
        self.config["stage"] = "smoke"
        (self.assets / "config.json").write_text(json.dumps(self.config))
        result = freeze(self.assets / "config.json", None, inspection_only=True)
        self.assertEqual(result["record_kind"], "sources_checked_not_protocol_frozen_not_run")
        self.assertIn("runtime:requested_model", result["pending_freeze_fields"])
        self.assertNotIn("protocol_sha256", result)
        with self.assertRaises(IntegrityError):
            verify(result)

    def test_live_dispatch_always_disabled(self):
        with self.assertRaises(RuntimeGateError):
            run_live()
        self.make()
        p = copy.deepcopy(self.protocol)
        p["runner"].update(binary_path="/fictional-fixture-tools/codex", sandbox_mode="workspace-write", requested_model="declared-model", reasoning_setting="medium")
        args = codex_argv(p, "/assigned", "/assigned/output/final.txt")
        self.assertNotIn("--ignore-rules", args)
        self.assertNotIn("--ignore-user-config", args)
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", args)
        self.assertIn("--ephemeral", args)


class ParserTests(unittest.TestCase):
    def parser(self, events):
        p = CodexEvents()
        for i, event in enumerate(events):
            p.feed(json.dumps(event) + "\n", i / 10)
        return p

    def test_actual_counters_only_missing_is_null(self):
        p = self.parser([{"type": "turn.started"}, {"type": "turn.completed", "usage": {"input_tokens": 12, "cached_input_tokens": 3, "output_tokens": 7}}])
        result = p.finish(0)
        self.assertEqual(result["usage"]["input_tokens"], 12)
        self.assertIsNone(result["usage"]["reasoning_output_tokens"])
        self.assertIsNone(result["usage"]["cross_category_total"])
        self.assertIsNone(result["billing"]["actual_cost"])

    def test_duplicate_updates_count_one_item(self):
        events = [{"type": "turn.started"}]
        for kind in ("item.started", "item.updated", "item.completed", "item.completed"):
            events.append({"type": kind, "item": {"id": "1", "type": "command_execution", "status": "completed", "exit_code": 0}})
        events.append({"type": "turn.completed", "usage": {}})
        result = self.parser(events).finish(0)
        self.assertEqual(result["logical_items"]["command_execution"], 1)
        self.assertEqual(result["unfinished_items"], 0)

    def test_failed_and_unfinished_items(self):
        result = self.parser([{"type": "item.started", "item": {"id": "a", "type": "mcp_tool_call", "status": "in_progress"}},
            {"type": "item.completed", "item": {"id": "b", "type": "command_execution", "status": "completed", "exit_code": 1}}]).finish(1)
        self.assertEqual(result["failed_items"], 1)
        self.assertEqual(result["unfinished_items"], 1)
        self.assertFalse(result["capture_complete"])

    def test_duplicate_terminal_usage_not_double_counted(self):
        end = {"type": "turn.completed", "usage": {"input_tokens": 9}}
        result = self.parser([{"type": "turn.started"}, end, end]).finish(0)
        self.assertEqual(result["turn_count"], 1)
        self.assertEqual(result["usage"]["input_tokens"], 9)

    def test_multi_turn_preserved_not_summed(self):
        result = self.parser([{"type": "turn.started"}, {"type": "turn.completed", "usage": {"input_tokens": 9}},
            {"type": "turn.started"}, {"type": "turn.completed", "usage": {"input_tokens": 5}}]).finish(0)
        self.assertEqual(result["turn_count"], 2)
        self.assertIsNone(result["usage"]["input_tokens"])
        self.assertFalse(result["capture_complete"])

    def test_truncation_and_invalid_counters(self):
        p = self.parser([{"type": "turn.started"}, {"type": "turn.completed", "usage": {"input_tokens": True, "output_tokens": -1}}])
        p.feed('{"type":')
        result = p.finish(0)
        self.assertEqual(result["parse_errors"], 1)
        self.assertFalse(result["capture_complete"])
        self.assertIsNone(result["usage"]["input_tokens"])

    def test_model_metadata_is_event_only(self):
        p = self.parser([{"type": "thread.started", "model": "provider-label"},
            {"type": "item.completed", "item": {"id": "a", "type": "agent_message", "text": "I am a different model"}}])
        result = p.finish(0)
        self.assertEqual(result["returned_model_label"], "provider-label")
        self.assertIsNone(result["exact_model_build"])

    def test_unrecognized_types_and_ids_do_not_leak_payload_text(self):
        canary = "PRIVATE_FIXTURE_CANARY"
        p = self.parser([{"type": canary}, {"type": "item.completed", "item": {"id": canary, "type": canary, "status": canary}}])
        value = json.dumps(p.safe_events) + json.dumps(p.finish(0)) + json.dumps(p.items)
        self.assertNotIn(canary, value)
        self.assertFalse(p.finish(0)["capture_complete"])

    def test_private_text_is_not_retained(self):
        p = self.parser([{"type": "item.completed", "item": {"id": "r", "type": "reasoning", "text": "PRIVATE_CHAIN_TEXT"}},
                         {"type": "error", "message": "secret-token"}])
        serialized = json.dumps(p.safe_events) + json.dumps(p.finish(1))
        self.assertNotIn("PRIVATE_CHAIN_TEXT", serialized)
        self.assertNotIn("secret-token", serialized)


class ExecutionTests(StudyCase):
    def test_success_is_fixture_only_and_timing_is_observed(self):
        self.make()
        result = run_fixture(self.study, "a0001")
        self.assertEqual(result["status"], "completed")
        self.assertGreater(result["timing"]["monotonic_elapsed_s"], 0)
        self.assertIsNone(result["timing"]["model_compute_s"])
        self.assertEqual(result["artifact_manifest"][0]["path"], "result.txt")
        output = report(self.study)
        self.assertTrue(output["no_model_results"])
        self.assertIsNone(output["primary"]["effect_estimate"])
        self.assertEqual(sum(a["scheduled"] for a in output["coverage"].values()), 2)
        self.assertEqual(sum(a["outcome_unknown"] for a in output["coverage"].values()), 2)

    def test_failures_are_appended_and_kept_in_denominator(self):
        self.make()
        result = run_fixture(self.study, "a0001", "failed")
        self.assertEqual(result["status"], "process_failed")
        self.assertEqual(result["exit_code"], 2)
        output = report(self.study)
        self.assertEqual(sum(a["scheduled"] for a in output["coverage"].values()), 2)
        self.assertEqual(sum(a["outcome_unknown"] for a in output["coverage"].values()), 1)
        self.assertEqual(len([r for r in Ledger(self.study / "attempts.jsonl").read() if r["event"] == "finished"]), 1)

    def test_timeout_recorded(self):
        self.make()
        result = run_fixture(self.study, "a0001", "timeout", .08)
        self.assertEqual(result["status"], "timed_out")
        self.assertTrue(result["timeout"])
        self.assertIsNone(result["usage"]["input_tokens"])
        self.assertLess(result["timing"]["monotonic_elapsed_s"], 3)

    def test_truncated_exit_zero_is_not_success(self):
        self.make()
        result = run_fixture(self.study, "a0001", "truncated")
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(result["status"], "event_capture_incomplete")

    def test_source_preservation_checked(self):
        self.make()
        result = run_fixture(self.study, "a0001", "mutate_input")
        self.assertEqual(result["status"], "integrity_failed")
        self.assertFalse(result["source_integrity"])

    def test_run_cannot_be_retried_in_place(self):
        self.make()
        run_fixture(self.study, "a0001", "missing_usage")
        with self.assertRaises(IntegrityError):
            run_fixture(self.study, "a0001")


class GradingTests(StudyCase):
    def test_blind_package_and_bound_rating(self):
        self.make()
        run_fixture(self.study, "a0001")
        blind = blind_export(self.study, "a0001", self.root / "review")
        packet = self.root / "review" / blind["blind_id"]
        names = {f["path"] for f in file_manifest(packet)}
        self.assertFalse(any("guide" in p or "telemetry" in p or "oracle" in p for p in names))
        rating = {"blind_id": blind["blind_id"], "submission_sha256": blind["submission_sha256"],
            "integrity": {"passed": True}, "groups": [{"id": f"g{i}", "passed": True} for i in range(1, 6)]}
        create_json(self.root / "grade.json", rating)
        import_grade(self.study, blind["blind_id"], self.root / "grade.json", "synthetic-rater")
        result = report(self.study)
        self.assertEqual(sum(a["accepted"] for a in result["coverage"].values()), 1)
        with self.assertRaises(IntegrityError):
            import_grade(self.study, blind["blind_id"], self.root / "grade.json", "synthetic-rater")

    def test_changed_submission_cannot_be_blinded(self):
        self.make()
        run_fixture(self.study, "a0001")
        control = load_json(self.study / "control/a0001.json")
        (Path(control["workspace"]) / "output/result.txt").write_text("changed")
        with self.assertRaises(IntegrityError):
            blind_export(self.study, "a0001", self.root / "review")

    def test_machine_group_passes_leave_deferred_review_pending(self):
        task = {"criteria": [f"g{i}" for i in range(1, 6)], "required_review_domains": ["process_integrity", "free_text_and_verification_claims"]}
        grade = {"kind": "rating", "groups": {g: True for g in task["criteria"]}, "integrity": True}
        result = resolve_grades([grade], task)
        self.assertIsNone(result["accepted"])
        self.assertTrue(result["deferred_review_pending"])
        self.assertEqual(result["quality_fraction"], 1)

    def test_evaluator_infrastructure_error_is_unknown_not_rejected(self):
        criteria = [f"g{i}" for i in range(1, 6)]
        value = normalize_grade({"groups": [{"id": g, "passed": False} for g in criteria],
            "integrity": {"passed": False}, "infrastructure_reason": "trust_metadata_unavailable"}, criteria)
        self.assertTrue(value["infrastructure_blocked"])
        self.assertTrue(all(v is None for v in value["groups"].values()))
        self.assertIsNone(value["integrity"])

    def test_deferred_review_binds_artifacts_and_trace_and_cannot_claim_full_process(self):
        self.config["tasks"][0]["required_review_domains"] = ["process_integrity", "free_text_and_verification_claims"]
        self.make()
        run_fixture(self.study, "a0001")
        blind = blind_export(self.study, "a0001", self.root / "review")
        rating = {"blind_id": blind["blind_id"], "submission_sha256": blind["submission_sha256"],
            "integrity": {"passed": True}, "groups": [{"id": f"g{i}", "passed": True} for i in range(1, 6)],
            "review_domains": {"free_text_and_verification_claims": True}, "review_method": "synthetic_test",
            "independence_attested": True, "review_evidence_sha256": "wrong"}
        path = self.root / "rating.json"
        path.write_text(json.dumps(rating))
        with self.assertRaises(IntegrityError):
            import_grade(self.study, blind["blind_id"], path, "synthetic-rater")
        rating["review_evidence_sha256"] = blind["review_evidence_sha256"]
        path.write_text(json.dumps(rating))
        import_grade(self.study, blind["blind_id"], path, "synthetic-rater")
        self.assertIsNone(next(r for r in report(self.study)["attempt_outcomes"] if r["attempt_id"] == "a0001")["accepted"])
        rating["review_domains"]["process_integrity"] = True
        path.write_text(json.dumps(rating))
        with self.assertRaises(IntegrityError):
            import_grade(self.study, blind["blind_id"], path, "second-synthetic-rater")

    def test_disagreement_requires_adjudication(self):
        task = {"criteria": [f"g{i}" for i in range(1, 6)], "min_raters": 2}
        base = {"kind": "rating", "groups": {g: True for g in task["criteria"]}, "integrity": True}
        second = copy.deepcopy(base); second["groups"]["g2"] = False
        self.assertIsNone(resolve_grades([base, second], task)["accepted"])
        self.assertEqual(resolve_grades([base, second], task)["disagreement"], ["g2"])
        adjudication = dict(base, kind="adjudication")
        self.assertTrue(resolve_grades([base, second, adjudication], task)["accepted"])

    def test_grade_cannot_promote_missing_semantics_to_pass(self):
        task = {"criteria": [f"g{i}" for i in range(1, 6)]}
        g = {"kind": "rating", "groups": {x: True for x in task["criteria"]}, "integrity": True}
        g["groups"]["g5"] = None
        result = resolve_grades([g], task)
        self.assertIsNone(result["accepted"])
        self.assertIsNone(result["quality_fraction"])
        with self.assertRaises(IntegrityError):
            normalize_grade({"groups": [{"id": "g1", "passed": "yes"}]}, ["g1"])


class CollectionTests(unittest.TestCase):
    def test_root_symlink_and_hardlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "outside").mkdir()
            (root / "outside/canary.txt").write_text("owned harmless canary")
            (root / "output").symlink_to(root / "outside", target_is_directory=True)
            with self.assertRaises(IntegrityError):
                file_manifest(root / "output")
            (root / "regular").mkdir()
            os.link(root / "outside/canary.txt", root / "regular/link.txt")
            with self.assertRaises(IntegrityError):
                file_manifest(root / "regular")

    def test_sparse_oversize_file_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as temp:
            with (Path(temp) / "large.bin").open("wb") as stream:
                stream.truncate(64 * 1024 * 1024 + 1)
            with self.assertRaises(IntegrityError):
                file_manifest(temp)

    def test_special_file_rejected_without_blocking(self):
        with tempfile.TemporaryDirectory() as temp:
            os.mkfifo(Path(temp) / "pipe")
            with self.assertRaises(IntegrityError):
                file_manifest(temp)


class LedgerTests(unittest.TestCase):
    def test_edit_is_detected(self):
        with tempfile.TemporaryDirectory() as temp:
            ledger = Ledger(Path(temp) / "attempts.jsonl")
            ledger.append("scheduled", attempt_id="a")
            ledger.append("finished", attempt_id="a", status="failed")
            self.assertEqual(len(ledger.read()), 2)
            contents = ledger.path.read_text().replace('"failed"', '"passed"')
            ledger.path.write_text(contents)
            with self.assertRaises(IntegrityError):
                ledger.read()


class StatisticalTests(unittest.TestCase):
    def test_family_task_weighting_not_attempt_weighting(self):
        tasks = [{"task_id": "A", "family_id": "f1"}, {"task_id": "B", "family_id": "f2"}]
        protocol = {"tasks": tasks, "stage": "evaluation", "protocol_sha256": "synthetic-stat-test", "analysis": {"bootstrap_seed": 2, "bootstrap_draws": 500}}
        rows = []
        # Family 1 has four repetitions with S benefit; family 2 one with S loss.
        # Equal family delta is zero, rather than the attempt-weighted +0.6.
        for family, task, repetitions in (("f1", "A", 4), ("f2", "B", 1)):
            for repetition in range(repetitions):
                for arm in ("C", "S"):
                    accepted = (arm == "S") if family == "f1" else (arm == "C")
                    rows.append({"family_id": family, "task_id": task, "arm": arm, "attempt_id": f"{task}{repetition}{arm}",
                        "block_id": f"{task}{repetition}", "accepted": accepted, "quality_fraction": float(accepted),
                        "elapsed_s": 2., "timeout_s": 4., "attempted": True, "finished": True, "rater_count": 1,
                        "status": "completed", "evidence_kind": "model_attempt", "usage": {}})
        # This is a mathematical unit test with synthetic rows, not a model result.
        result = summarize(rows, protocol)
        self.assertEqual(result["primary"]["effect_estimate"], 0)
        self.assertEqual(result["primary"]["distinct_task_count"], 2)
        self.assertEqual(result["accepted_pair_latency_secondary"]["both_accepted_pairs"], 0)
        self.assertIsNone(result["coverage"]["C"]["usage"]["input_tokens"]["sum_known_counter"])

    def test_exploratory_pilot_has_no_inferential_interval(self):
        tasks = [{"task_id": str(i), "family_id": str(i)} for i in range(8)]
        protocol = {"tasks": tasks, "stage": "exploratory_pilot", "protocol_sha256": "synthetic-test", "analysis": {"bootstrap_enabled": True}}
        rows = [{"family_id": str(i), "task_id": str(i), "arm": arm, "attempt_id": f"{i}{arm}", "block_id": str(i),
                 "accepted": True, "quality_fraction": 1., "elapsed_s": 2., "timeout_s": 4., "attempted": True,
                 "finished": True, "rater_count": 1, "status": "completed", "evidence_kind": "model_attempt", "usage": {}}
                for i in range(8) for arm in ("C", "S")]
        result = summarize(rows, protocol)
        self.assertEqual(result["primary"]["effect_estimate"], 0)
        self.assertIsNone(result["primary"]["cluster_bootstrap"])
        self.assertEqual(result["primary"]["leave_one_case_out_range"], [0, 0])
        self.assertEqual(result["paired_acceptance_comparison"]["ties_both_accepted"], 8)

    def test_degenerate_bootstrap_warns_against_false_certainty(self):
        interval = cluster_interval([0, 0, 0, 0], 3, 500)
        self.assertTrue(interval["degenerate_observed_interval"])
        self.assertIsNotNone(interval["degenerate_warning"])

    def test_cluster_bootstrap_deterministic_and_requires_clusters(self):
        self.assertIsNone(cluster_interval([.2], 1, 500))
        self.assertEqual(cluster_interval([-.2, .1, .3], 1, 500), cluster_interval([-.2, .1, .3], 1, 500))


if __name__ == "__main__":
    unittest.main()
