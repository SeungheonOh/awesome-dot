"""Verifier regression fixtures, not new agent trials or saved outcome scores."""
import contextlib
import copy
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch

import verify


class RunnerTests(unittest.TestCase):
    def run_wrapper(self, run):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(verify, "check_initial_bindings"), patch.object(verify, "read_file"), \
                patch.object(verify.subprocess, "run", run), \
                contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = verify.main([])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_all_commands_run_once_in_fixed_order(self):
        expected = [
            ("evaluation/verify.py", "--fixtures-only"),
            ("evaluation/verify.py", "--tests-only"),
            ("evaluation/results/native-cloud-2026-10-06/score.py",),
            ("evaluation/studies/repeated-stress-2026-10-06/reproduce_saved_evidence.py",),
            ("evaluation/report.py", "--check"),
        ]
        for _ in range(2):
            run = Mock()
            code, stdout, stderr = self.run_wrapper(run)
            self.assertEqual(code, 0)
            self.assertEqual(stderr, "")
            self.assertIn("All 6 local verification checks passed", stdout)
            self.assertEqual([call.args[0] for call in run.call_args_list],
                             [[sys.executable, "-I", "-B", *args] for args in expected])
            for call in run.call_args_list:
                self.assertEqual(call.kwargs["cwd"], verify.ROOT.parent)
                self.assertTrue(call.kwargs["check"])
                self.assertEqual(call.kwargs["timeout"], verify.TIMEOUT_SECONDS)
                self.assertNotIn("shell", call.kwargs)

    def test_each_failed_subprocess_is_nonzero_and_does_not_omit_later_checks(self):
        for position, (label, _) in enumerate(verify.COMMANDS):
            with self.subTest(label=label):
                effects = [None] * len(verify.COMMANDS)
                effects[position] = subprocess.CalledProcessError(7, ["fixture"])
                run = Mock(side_effect=effects)
                code, stdout, stderr = self.run_wrapper(run)
                self.assertEqual(code, 1)
                self.assertEqual(run.call_count, len(verify.COMMANDS))
                self.assertIn("FAILED: " + label, stderr)
                self.assertIn("exit status 7", stderr)
                self.assertNotIn("All 6 local verification checks passed", stdout)

    def test_timeout_and_launch_errors_fail_with_diagnostics(self):
        for error in (subprocess.TimeoutExpired(["fixture"], 900), OSError("cannot launch")):
            with self.subTest(error=error):
                run = Mock(side_effect=[error] + [None] * (len(verify.COMMANDS) - 1))
                code, _, stderr = self.run_wrapper(run)
                self.assertEqual(code, 1)
                self.assertIn("FAILED: Original source and fixture checks", stderr)
                self.assertEqual(run.call_count, len(verify.COMMANDS))

    def test_real_failing_subprocess_returns_nonzero(self):
        with patch.object(verify, "COMMANDS", (("Authored failure fixture", ("-c", "raise SystemExit(7)")),)), \
                patch.object(verify, "check_initial_bindings"), \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(verify.main([]), 1)
        self.assertIn("Authored failure fixture", stderr.getvalue())
        self.assertIn("exit status 7", stderr.getvalue())

    def test_binding_failure_remains_nonzero_after_successful_subprocesses(self):
        with patch.object(verify, "check_initial_bindings", side_effect=ValueError("bad binding")), \
                patch.object(verify, "read_file"), patch.object(verify.subprocess, "run") as run, \
                contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(verify.main([]), 1)
        self.assertEqual(run.call_count, len(verify.COMMANDS))
        self.assertIn("bad binding", stderr.getvalue())

    def test_python_environment_cannot_disable_child_assertions(self):
        run = Mock()
        with patch.dict(os.environ, {"PYTHONOPTIMIZE": "2", "PYTHONPATH": "/untrusted", "PYTHONHOME": "/bad"}):
            self.assertEqual(self.run_wrapper(run)[0], 0)
        for call in run.call_args_list:
            env = call.kwargs["env"]
            self.assertEqual({k for k in env if k.startswith("PYTHON")}, {"PYTHONDONTWRITEBYTECODE"})

    def test_import_does_not_run_checks_read_evidence_or_write_files(self):
        spec = importlib.util.spec_from_file_location("fresh_verify", verify.ROOT / "verify.py")
        module = importlib.util.module_from_spec(spec)
        with patch.object(subprocess, "run", side_effect=AssertionError("subprocess during import")), \
                patch.object(Path, "read_bytes", side_effect=AssertionError("evidence read during import")), \
                patch.object(Path, "write_text", side_effect=AssertionError("write during import")), \
                contextlib.redirect_stdout(io.StringIO()) as stdout, \
                contextlib.redirect_stderr(io.StringIO()) as stderr:
            spec.loader.exec_module(module)
        self.assertEqual(stdout.getvalue() + stderr.getvalue(), "")


class RegressionDiscoveryTests(unittest.TestCase):
    def test_known_report_and_navigation_tests_are_present(self):
        loader = unittest.TestLoader()
        self.assertEqual(loader.loadTestsFromName("test_check").countTestCases(), 8)
        self.assertEqual(loader.loadTestsFromName("test_report").countTestCases(), 11)
        self.assertFalse(loader.errors)

    def test_missing_module_fails_instead_of_zero_test_success(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "Missing test modules"):
                verify.run_regressions(Path(directory))

    def test_empty_module_fails(self):
        with patch.object(unittest.TestLoader, "loadTestsFromName", return_value=unittest.TestSuite()):
            with self.assertRaisesRegex(ValueError, "No tests discovered"):
                verify.run_regressions(verify.ROOT)

    def test_symlinked_test_cannot_import_saved_candidate_code(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in verify.REGRESSION_MODULES:
                (root / (name + ".py")).touch()
            (root / "artifacts").mkdir()
            candidate = root / "artifacts/candidate.py"
            candidate.write_text("raise RuntimeError('saved candidate executed')\n")
            (root / "test_candidate.py").symlink_to(candidate)
            with patch.object(unittest.TestLoader, "loadTestsFromName") as load:
                with self.assertRaisesRegex(ValueError, "Unsafe or missing file: test_candidate.py"):
                    verify.run_regressions(root)
            load.assert_not_called()

    def test_discovery_errors_fail(self):
        loader = Mock(errors=["broken import"])
        loader.loadTestsFromName.return_value.countTestCases.return_value = 1
        with patch.object(unittest, "TestLoader", return_value=loader):
            with self.assertRaisesRegex(ValueError, "broken import"):
                verify.run_regressions(verify.ROOT)

    def test_immediate_new_modules_are_sorted_and_saved_artifacts_not_discovered(self):
        suite = unittest.TestSuite([unittest.FunctionTestCase(lambda: None)])
        result = Mock(skipped=[])
        result.wasSuccessful.return_value = True
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            names = verify.REGRESSION_MODULES | {"test_z_extra", "test_a_extra"}
            for name in names:
                (root / (name + ".py")).touch()
            (root / "artifacts").mkdir()
            (root / "artifacts/test_candidate.py").touch()
            before = sys.path[:]
            with patch.object(unittest.TestLoader, "loadTestsFromName", return_value=suite) as load, \
                    patch.object(unittest.TextTestRunner, "run", return_value=result):
                self.assertEqual(verify.run_regressions(root), 0)
            self.assertEqual([call.args[0] for call in load.call_args_list], sorted(names))
            self.assertEqual(sys.path, before)

    def test_failed_or_skipped_regressions_are_nonzero(self):
        suite = unittest.TestSuite([unittest.FunctionTestCase(lambda: None)])
        for success, skipped in ((False, []), (True, [("test", "unavailable")])):
            result = Mock(skipped=skipped)
            result.wasSuccessful.return_value = success
            with patch.object(unittest.TestLoader, "loadTestsFromName", return_value=suite), \
                    patch.object(unittest.TextTestRunner, "run", return_value=result), \
                    contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(verify.run_regressions(verify.ROOT), 1)


class HarnessCoverageTests(unittest.TestCase):
    def test_each_known_harness_module_must_be_present_nonempty_and_unskipped(self):
        valid = "import unittest\nclass Checks(unittest.TestCase):\n    def test_ok(self):\n        pass\n"
        defects = {
            "missing": None,
            "empty": "",
            "decorator_skip": "import unittest\n@unittest.skip('fixture skip')\nclass Checks(unittest.TestCase):\n    def test_ok(self):\n        pass\n",
            "runtime_skip": "import unittest\nclass Checks(unittest.TestCase):\n    def test_ok(self):\n        self.skipTest('runtime fixture skip')\n",
            "class_setup_skip": "import unittest\nclass Checks(unittest.TestCase):\n    @classmethod\n    def setUpClass(cls):\n        raise unittest.SkipTest('class fixture skip')\n    def test_ok(self):\n        pass\n",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "verify.py").write_bytes((verify.ROOT / "verify.py").read_bytes())
            tests = root / "harness/tests"
            tests.mkdir(parents=True)
            for name in verify.HARNESS_MODULES:
                (tests / (name + ".py")).write_text(valid)
            command = [sys.executable, "-I", "-B", str(root / "verify.py"), "--harness-only"]
            baseline = subprocess.run(command, capture_output=True, text=True, timeout=10)
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            self.assertIn("Ran 3 tests", baseline.stderr)
            for name in sorted(verify.HARNESS_MODULES):
                path = tests / (name + ".py")
                for defect, content in defects.items():
                    with self.subTest(module=name, defect=defect):
                        if content is None:
                            path.unlink()
                        else:
                            path.write_text(content)
                        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
                        self.assertEqual(result.returncode, 1, result.stderr)
                        self.assertIn(name, result.stderr)
                        path.write_text(valid)

    def test_original_fixture_workflow_uses_strict_harness_once(self):
        check = Mock()
        original_run = check.run
        env = {"PYTHONDONTWRITEBYTECODE": "1"}
        def workflow():
            check.run(["inspect"], verify.ROOT, env)
            check.run(list(verify.HARNESS_COMMAND), verify.ROOT / "harness", env)
            check.run(["grader"], verify.ROOT / "evaluators/F1", env)
            return 0
        check.main.side_effect = workflow
        with patch.object(verify, "load_check", return_value=check), patch.object(verify.subprocess, "run") as run:
            self.assertEqual(verify.run_fixtures(verify.ROOT), 0)
        run.assert_called_once_with(
            [sys.executable, "-I", "-B", str(verify.ROOT / "verify.py"), "--harness-only"],
            cwd=verify.ROOT / "harness", env=env, check=True, timeout=120)
        self.assertEqual(original_run.call_count, 2)
        self.assertIs(check.run, original_run)

    def test_omitted_or_repeated_harness_stage_fails(self):
        for count in (0, 2):
            check = Mock()
            original_run = check.run
            def workflow():
                for _ in range(count):
                    check.run(list(verify.HARNESS_COMMAND), verify.ROOT / "harness", {})
                return 0
            check.main.side_effect = workflow
            with patch.object(verify, "load_check", return_value=check), patch.object(verify.subprocess, "run"):
                with self.assertRaisesRegex(ValueError, "Original check (omitted|repeated) its harness stage"):
                    verify.run_fixtures(verify.ROOT)
            self.assertIs(check.run, original_run)

    def test_strict_harness_failure_restores_original_runner(self):
        check = Mock()
        original_run = check.run
        check.main.side_effect = lambda: check.run(list(verify.HARNESS_COMMAND), verify.ROOT / "harness", {})
        with patch.object(verify, "load_check", return_value=check), \
                patch.object(verify.subprocess, "run", side_effect=subprocess.CalledProcessError(1, ["fixture"])):
            with self.assertRaises(subprocess.CalledProcessError):
                verify.run_fixtures(verify.ROOT)
        self.assertIs(check.run, original_run)


class InitialBindingTests(unittest.TestCase):
    def setUp(self):
        self.original_read = verify.read_file
        self.documents = {name: json.loads(self.original_read(verify.ROOT, f"{verify.INITIAL}/{name}.json"))
                          for name in ("attempts", "schedule", "provenance")}

    def validate(self):
        def read(root, relative, *args):
            for name, value in self.documents.items():
                if relative == f"{verify.INITIAL}/{name}.json":
                    return json.dumps(value).encode()
            return self.original_read(root, relative, *args)
        with patch.object(verify, "read_file", side_effect=read), contextlib.redirect_stdout(io.StringIO()):
            verify.check_initial_bindings(verify.ROOT)

    def test_current_saved_bindings_pass_without_new_scores(self):
        self.validate()

    def test_swapped_condition_labels_fail_even_when_totals_would_tie(self):
        for row in self.documents["attempts"]["rows"]:
            if row["case_id"] == "F1":
                row["arm"] = {"C": "S", "S": "C"}[row["arm"]]
        with self.assertRaisesRegex(ValueError, "Attempt arm mismatch"):
            self.validate()

    def test_changed_attempt_identity_fields_fail(self):
        original = copy.deepcopy(self.documents)
        for key, value in (("case_id", "F1"), ("schedule_ordinal", 99), ("attempt_number", 2), ("attempt_number", True),
                           ("timeout_cap_seconds", 1), ("dispatch_prompt_sha256", "0" * 64)):
            with self.subTest(field=key):
                self.documents = copy.deepcopy(original)
                self.documents["attempts"]["rows"][0][key] = value
                with self.assertRaisesRegex(ValueError, "Attempt " + key + " mismatch"):
                    self.validate()

    def test_swapped_schedule_tasks_fail(self):
        rows = self.documents["schedule"]["rows"]
        rows[0]["task_id"], rows[2]["task_id"] = rows[2]["task_id"], rows[0]["task_id"]
        with self.assertRaisesRegex(ValueError, "Schedule task_id mismatch"):
            self.validate()

    def test_coordinated_schedule_and_attempt_relabeling_still_fails(self):
        for source in ("schedule", "attempts"):
            for row in self.documents[source]["rows"]:
                if row["case_id"] == "F1":
                    row["arm"] = {"C": "S", "S": "C"}[row["arm"]]
        with self.assertRaisesRegex(ValueError, "Schedule attempt_id does not match"):
            self.validate()

    def test_coordinated_attempt_number_mutations_cannot_change_first_submission_policy(self):
        original = copy.deepcopy(self.documents)
        for value in (None, True, False, 0, -1, 2, 1.0, "1"):
            with self.subTest(value=value):
                self.documents = copy.deepcopy(original)
                for source in ("schedule", "attempts"):
                    self.documents[source]["rows"][0]["attempt_number"] = value
                with self.assertRaisesRegex(ValueError, "Schedule attempt_number must be integer 1"):
                    self.validate()

    def test_coordinated_timeout_mutations_must_match_hash_bound_task_cap(self):
        original = copy.deepcopy(self.documents)
        for index in (0, 15):
            for value in (None, True, False, 0, -1, 1, 900.0, "900", 900 if index == 15 else 1500):
                with self.subTest(index=index, value=value):
                    self.documents = copy.deepcopy(original)
                    self.documents["schedule"]["rows"][index]["timeout_seconds"] = value
                    self.documents["attempts"]["rows"][index]["timeout_cap_seconds"] = value
                    with self.assertRaisesRegex(ValueError, "Schedule timeout_seconds differs from source task"):
                        self.validate()

    def test_missing_duplicate_and_extra_ids_fail(self):
        original = copy.deepcopy(self.documents)
        for source in ("attempts", "schedule"):
            for mutation in ("missing", "duplicate", "extra"):
                with self.subTest(source=source, mutation=mutation):
                    self.documents = copy.deepcopy(original)
                    rows = self.documents[source]["rows"]
                    if mutation == "missing":
                        rows.pop()
                    elif mutation == "duplicate":
                        rows[-1]["attempt_id"] = rows[0]["attempt_id"]
                    else:
                        rows[-1]["attempt_id"] = "unknown-attempt"
                    with self.assertRaisesRegex(ValueError, "attempt"):
                        self.validate()

    def test_schedule_pair_and_ordinal_coverage_fail_closed(self):
        original = copy.deepcopy(self.documents)
        for key, value, message in (("arm", "C", "case/condition"), ("ordinal", 2, "ordinals")):
            with self.subTest(field=key):
                self.documents = copy.deepcopy(original)
                self.documents["schedule"]["rows"][0][key] = value
                with self.assertRaisesRegex(ValueError, message):
                    self.validate()

    def test_prompt_hash_agreement_does_not_claim_to_reconstruct_prompts(self):
        self.documents["provenance"]["frozen_prompt_hashes"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "Schedule prompt hash mismatch"):
            self.validate()

    def test_matching_invalid_prompt_hashes_cannot_pass(self):
        original = copy.deepcopy(self.documents)
        for digest in (None, "short", "G" * 64, 0):
            with self.subTest(digest=digest):
                self.documents = copy.deepcopy(original)
                self.documents["provenance"]["frozen_prompt_hashes"][0]["sha256"] = digest
                for source in ("schedule", "attempts"):
                    self.documents[source]["rows"][0]["dispatch_prompt_sha256"] = digest
                with self.assertRaisesRegex(ValueError, "Invalid schedule prompt hash"):
                    self.validate()

    def test_missing_or_duplicate_source_record_fails(self):
        original = copy.deepcopy(self.documents)
        for duplicate in (False, True):
            self.documents = copy.deepcopy(original)
            entries = self.documents["provenance"]["grading_sources"]
            entries.pop()
            if duplicate:
                entries.append(copy.deepcopy(entries[0]))
            with self.assertRaisesRegex(ValueError, "grading.source"):
                self.validate()

    def test_altered_source_config_and_manifest_bytes_fail(self):
        original = Path.read_bytes
        for relative in ("pilot-source-config.json", "cases/manifest.json", "packages/manifest.json",
                         "evaluators/F1/grade.py"):
            with self.subTest(path=relative):
                def changed(path):
                    raw = original(path)
                    return raw + b"\n" if path == verify.ROOT / relative else raw
                with patch.object(Path, "read_bytes", changed):
                    with self.assertRaisesRegex(ValueError, "Content differs"):
                        self.validate()

    def test_null_hash_or_size_metadata_cannot_disable_verification(self):
        original = copy.deepcopy(self.documents)
        for field in ("source_config_sha256", "case_manifest_sha256", "package_manifest_sha256", "sha256", "bytes"):
            with self.subTest(field=field):
                self.documents = copy.deepcopy(original)
                provenance = self.documents["provenance"]
                if field in ("sha256", "bytes"):
                    provenance["grading_sources"][0][field] = None
                else:
                    provenance[field] = None
                with self.assertRaisesRegex(ValueError, "Content differs"):
                    self.validate()


class ConfinedReadTests(unittest.TestCase):
    def test_missing_traversal_absolute_and_symlink_paths_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file").write_bytes(b"saved bytes")
            (root / "link").symlink_to(root / "file")
            (root / "folder").mkdir()
            (root / "linked-folder").symlink_to(root / "folder", target_is_directory=True)
            (root / "folder/file").write_bytes(b"saved bytes")
            for path in ("missing", "../outside", str(root / "file"), "link", "linked-folder/file"):
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, "Unsafe or missing"):
                    verify.read_file(root, path)

    def test_wrong_hash_or_size_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "file").write_bytes(b"saved bytes")
            self.assertEqual(verify.read_file(root, "file"), b"saved bytes")
            for kwargs in ({"sha256": "0" * 64}, {"size": 0}, {"sha256": None}, {"size": None}):
                with self.assertRaisesRegex(ValueError, "Content differs"):
                    verify.read_file(root, "file", **kwargs)


if __name__ == "__main__":
    unittest.main()
