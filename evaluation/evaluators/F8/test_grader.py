"""Fixture/grader tests only; no model or external service is used."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from grade import grade, grade_author_fixture, _safe_io

ROOT=Path(__file__).resolve().parent
PACKET=ROOT.parents[1]/"cases/F8"


class FixtureTests(unittest.TestCase):
    def test_author_reference_is_accepted(self):
        result=grade_author_fixture(ROOT/"reference/accepted",PACKET)
        self.assertTrue(result["accepted"],result)
        self.assertEqual(result["quality"],1.0)
        self.assertEqual([g["id"] for g in result["groups"]],[f"g{i}" for i in range(1,6)])
        self.assertTrue(all(g["passed"] and not g["reasons"] for g in result["groups"]))

    def test_every_control_has_its_frozen_outcome(self):
        index=json.loads((ROOT/"controls/index.json").read_text())
        covered=set()
        for control in index["controls"]:
            with self.subTest(control=control["id"]):
                result=grade_author_fixture(ROOT/control["submission"],PACKET)
                expected=control["expected"]
                self.assertEqual(result["accepted"],expected["accepted"])
                self.assertEqual(result["integrity"]["passed"],expected["integrity_passed"])
                failed=[g["id"] for g in result["groups"] if not g["passed"]]
                self.assertEqual(failed,expected["failed_groups"],result)
                self.assertEqual(result["quality"],(5-len(failed))/5)
                if control["id"] == "g5_false_test_report":
                    # The public label must not mask the intended false-count check.
                    report = (ROOT/control["submission"]/"checks.txt").read_text()
                    self.assertTrue(report.startswith("DELIBERATELY INVALID SYNTHETIC NEGATIVE CONTROL\n"))
                    self.assertEqual(result["groups"][4]["reasons"], [
                        "checks.txt Tests must match the verified command/result/test count"
                    ])
                for group in result["groups"]:
                    if not group["passed"]:
                        self.assertTrue(group["reasons"])
                covered.update(failed)
                if not result["integrity"]["passed"]:
                    covered.add("integrity")
        self.assertEqual(covered,{"g1","g2","g3","g4","g5","integrity"})

    def test_public_api_is_fail_closed_even_for_known_reference(self):
        result=grade(ROOT/"reference/accepted",PACKET)
        self.assertTrue(result["integrity"]["passed"])
        self.assertIsNone(result["accepted"])
        self.assertIsNone(result["quality"])
        self.assertEqual(result["blocked_reason"],"untrusted_python_execution_requires_verified_isolation")
        self.assertTrue(all(g["passed"] is None and g["reasons"] for g in result["groups"]))

    def test_public_api_does_not_execute_modified_code(self):
        with tempfile.TemporaryDirectory() as directory:
            submission=Path(directory)/"output"
            shutil.copytree(ROOT/"reference/accepted",submission)
            marker=Path(directory)/"would-have-executed"
            module=submission/"merge_session.py"
            module.write_text("from pathlib import Path\nPath("+repr(str(marker))+").write_text('executed')\n"+module.read_text())
            result=grade(submission,PACKET)
            self.assertIsNone(result["accepted"])
            self.assertFalse(marker.exists())
            with self.assertRaisesRegex(ValueError,"Not an exact allowlisted"):
                grade_author_fixture(submission,PACKET)
            self.assertFalse(marker.exists())

    def test_modified_runner_is_detected_from_evaluator_trust(self):
        with tempfile.TemporaryDirectory() as directory:
            runner=Path(directory)/"runner"
            shutil.copytree(PACKET,runner)
            task=runner/"task.txt"
            task.write_text(task.read_text()+"\nmodified\n")
            # The mutable runner manifest cannot bless the changed task.
            manifest=runner/"input-manifest.json"
            manifest.write_text('{"files": []}\n')
            result=grade(ROOT/"reference/accepted",runner)
            self.assertFalse(result["integrity"]["passed"])
            self.assertFalse(result["accepted"])
            self.assertIn("task.txt"," ".join(result["integrity"]["reasons"]))

    def test_missing_deliverable_is_known_integrity_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            submission=Path(directory)/"output"
            shutil.copytree(ROOT/"reference/accepted",submission)
            (submission/"checks.txt").unlink()
            result=grade(submission,PACKET)
            self.assertFalse(result["integrity"]["passed"])
            self.assertFalse(result["accepted"])
            self.assertIsNone(result["quality"])

    def test_standard_cli_returns_only_json_and_unknown_behavior(self):
        process=subprocess.run([sys.executable,"-B",str(ROOT/"grade.py"),
                                "--submission",str(ROOT/"reference/accepted"),
                                "--runner",str(PACKET)],capture_output=True,text=True,check=True)
        result=json.loads(process.stdout)
        self.assertIsNone(result["accepted"])
        self.assertEqual(len(result["groups"]),5)
        self.assertEqual(process.stderr,"")


    def test_symlinks_in_editable_files_or_any_ancestor_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            submission=root/"output"
            shutil.copytree(ROOT/"reference/accepted",submission)
            outside=root/"module.py"
            shutil.copyfile(submission/"merge_session.py",outside)
            (submission/"merge_session.py").unlink()
            (submission/"merge_session.py").symlink_to(outside)
            result=grade(submission,PACKET)
            self.assertFalse(result["integrity"]["passed"])
            self.assertFalse(result["accepted"])
            (submission/"merge_session.py").unlink()
            shutil.copyfile(outside,submission/"merge_session.py")
            alias=root/"alias"
            alias.symlink_to(root,target_is_directory=True)
            result=grade(alias/"output",PACKET)
            self.assertFalse(result["integrity"]["passed"])
            runner_alias=root/"runner-alias"
            runner_alias.symlink_to(PACKET,target_is_directory=True)
            self.assertFalse(grade(submission,runner_alias)["integrity"]["passed"])
            tests=root/"outside-tests"
            (submission/"tests").rename(tests)
            (submission/"tests").symlink_to(tests,target_is_directory=True)
            self.assertFalse(grade(submission,PACKET)["integrity"]["passed"])

    def test_directory_missing_and_invalid_paths_produce_integrity_reasons(self):
        with tempfile.TemporaryDirectory() as directory:
            submission=Path(directory)/"output"
            shutil.copytree(ROOT/"reference/accepted",submission)
            (submission/"checks.txt").unlink()
            (submission/"checks.txt").mkdir()
            for path in (submission,Path(directory)/"missing",None,"\x00bad"):
                with self.subTest(path=repr(path)):
                    result=grade(path,PACKET)
                    self.assertFalse(result["integrity"]["passed"])
                    self.assertTrue(result["integrity"]["reasons"])
                    self.assertFalse(result["accepted"])

    @unittest.skipUnless(hasattr(os,"mkfifo"),"POSIX FIFO check")
    def test_special_fifo_file_is_rejected_without_reading(self):
        with tempfile.TemporaryDirectory() as directory:
            submission=Path(directory)/"output"
            shutil.copytree(ROOT/"reference/accepted",submission)
            os.mkfifo(submission/"must-not-block")
            result=grade(submission,PACKET)
            self.assertFalse(result["integrity"]["passed"])
            self.assertIn("regular file"," ".join(result["integrity"]["reasons"]))

    def test_oversized_regular_file_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            submission=Path(directory)/"output"
            shutil.copytree(ROOT/"reference/accepted",submission)
            with (submission/"oversized.bin").open("wb") as handle:
                handle.truncate(_safe_io.MAX_FILE_BYTES+1)
            result=grade(submission,PACKET)
            self.assertFalse(result["integrity"]["passed"])
            self.assertIn("8 MiB"," ".join(result["integrity"]["reasons"]))

    def test_tree_reader_enforces_total_count_and_depth_bounds(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/"a").write_bytes(b"123")
            (root/"b").write_bytes(b"456")
            with self.assertRaises(_safe_io.FileIssue):
                _safe_io.tree_hashes(root,max_tree_bytes=5)
            with self.assertRaises(_safe_io.FileIssue):
                _safe_io.tree_hashes(root,max_entries=1)
            (root/"nested").mkdir()
            (root/"nested"/"c").write_bytes(b"7")
            with self.assertRaises(_safe_io.FileIssue):
                _safe_io.tree_hashes(root,max_depth=0)

    def test_missing_or_malformed_trust_is_unknown_infrastructure(self):
        original=json.loads((ROOT/"trusted_manifest.json").read_text())
        missing_key=json.loads(json.dumps(original))
        del missing_key["runner_files"]["task.txt"]
        bad_hash=json.loads(json.dumps(original))
        bad_hash["runner_files"]["task.txt"]=True
        variants=[None,"not JSON",json.dumps({}),json.dumps([]),json.dumps(missing_key),json.dumps(bad_hash)]
        module=sys.modules[grade.__module__]
        with tempfile.TemporaryDirectory() as directory:
            here=Path(directory)
            path=here/"trusted_manifest.json"
            for content in variants:
                with self.subTest(content=content):
                    if content is None:
                        if path.exists():path.unlink()
                    else:
                        path.write_text(content)
                    with patch.object(module,"HERE",here):
                        result=grade(ROOT/"reference/accepted",PACKET)
                    self.assertIsNone(result["integrity"]["passed"])
                    self.assertIsNone(result["accepted"])
                    self.assertIsNone(result["quality"])
                    self.assertTrue(all(group["passed"] is None for group in result["groups"]))
                    self.assertEqual(result["infrastructure_reason"],"evaluator_trust_metadata_unavailable_or_malformed")

    def test_runner_has_only_contract_and_owned_scaffold(self):
        expected={"task.txt","input-manifest.json","inputs/scaffold/merge_primitive.py",
                  "inputs/scaffold/merge_session.py","inputs/scaffold/card_editor.py",
                  "inputs/scaffold/demo_cards.json","inputs/scaffold/tests/test_smoke.py"}
        actual={str(p.relative_to(PACKET)) for p in (PACKET).rglob("*") if p.is_file()}
        self.assertEqual(actual,expected)


if __name__=="__main__":
    unittest.main()
