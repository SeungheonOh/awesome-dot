"""Authored positive/negative controls; none of these are model submissions."""
import copy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("action_handoff_check", HERE / "check.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

VALID = {"actions": [
    {"source_id": "S1", "owner": "Mira", "due_date": "2026-10-12"},
    {"source_id": "S3", "owner": None, "due_date": None},
]}


class AuthoredControlTests(unittest.TestCase):
    def check(self, data):
        return checker.check_bytes(json.dumps(data).encode("utf-8"))

    def assert_failed(self, result, identifier):
        self.assertEqual(result["status"], "failed")
        row = next(row for row in result["assertions"] if row["id"] == identifier)
        self.assertEqual(row["status"], "failed")
        self.assertTrue(row["errors"])
        return row

    def test_authored_valid(self):
        result = self.check(VALID)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(tuple(row["id"] for row in result["assertions"]), checker.ASSERTION_IDS)

    def test_equivalent_reversed_actions_keys_and_whitespace(self):
        data = {"actions": [dict(reversed(list(row.items())))
                            for row in reversed(VALID["actions"])]}
        raw = ("\n" + json.dumps(data, indent=4) + "\n").encode("utf-8")
        self.assertEqual(checker.check_bytes(raw)["status"], "passed")

    def test_invented_owner(self):
        data = copy.deepcopy(VALID)
        data["actions"][1]["owner"] = "Mira"
        row = self.assert_failed(self.check(data), "unassigned_fields")
        self.assertEqual(row["evidence"]["source"], "task.txt#S3")
        self.assertEqual(row["evidence"]["observed"][0]["owner"], "Mira")

    def test_suggestion_promoted_to_action(self):
        data = copy.deepcopy(VALID)
        data["actions"].append({"source_id": "S2", "owner": "Theo", "due_date": None})
        self.assert_failed(self.check(data), "agreed_actions")

    def test_duplicate_action(self):
        data = copy.deepcopy(VALID)
        data["actions"].append(copy.deepcopy(data["actions"][0]))
        self.assert_failed(self.check(data), "agreed_actions")

    def test_missing_action(self):
        self.assert_failed(self.check({"actions": VALID["actions"][:1]}), "agreed_actions")

    def test_wrong_assigned_date_or_owner(self):
        for field, value in (("due_date", "2026-10-13"), ("owner", "Theo")):
            with self.subTest(field=field):
                data = copy.deepcopy(VALID)
                data["actions"][0][field] = value
                self.assert_failed(self.check(data), "assigned_fields")

    def test_invented_unassigned_date(self):
        data = copy.deepcopy(VALID)
        data["actions"][1]["due_date"] = "2026-10-12"
        self.assert_failed(self.check(data), "unassigned_fields")

    def test_missing_field_is_not_null(self):
        data = copy.deepcopy(VALID)
        del data["actions"][1]["owner"]
        self.assert_failed(self.check(data), "json_shape")

    def test_malformed_json_and_duplicate_keys(self):
        for raw in (b"", b"{", b"```json\n{}\n```", b"\xff", b'{"actions": NaN}',
                    b'{"actions": [], "actions": []}', b"[" * 1500 + b"]" * 1500):
            with self.subTest(raw=raw[:50]):
                result = checker.check_bytes(raw)
                self.assert_failed(result, "json_shape")
                self.assertTrue(all(row["status"] == "not_assessed"
                                    for row in result["assertions"][1:]))

    def test_invalid_schema(self):
        bad_row = {"source_id": "S1", "owner": False, "due_date": None}
        for data in (None, [], {}, {"actions": None}, {"actions": [], "extra": 1},
                     {"actions": [bad_row]}, {"actions": [{}]},
                     {"actions": VALID["actions"] * 2}):
            with self.subTest(data=data):
                self.assert_failed(self.check(data), "json_shape")

    def test_byte_limit(self):
        raw = json.dumps(VALID).encode("utf-8")
        self.assertEqual(checker.check_bytes(raw.ljust(checker.MAX_BYTES))["status"], "passed")
        self.assert_failed(checker.check_bytes(raw.ljust(checker.MAX_BYTES + 1)), "json_shape")

    def test_cli_statuses_and_bounded_read(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "actions.json"
            for raw, expected_code, expected_status in (
                    (None, 2, "not_assessed"),
                    (json.dumps(VALID).encode("utf-8"), 0, "passed"),
                    (b"{}", 1, "failed"),
                    (b" " * (checker.MAX_BYTES + 1), 1, "failed")):
                with self.subTest(status=expected_status, raw_bytes=None if raw is None else len(raw)):
                    if raw is not None:
                        path.write_bytes(raw)
                    result = subprocess.run([sys.executable, "-I", "-B", str(HERE / "check.py"), str(path)],
                                            capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, expected_code, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["status"], expected_status)

    def test_cli_rejects_directory_and_fifo_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            fifo = Path(directory) / "pipe"
            os.mkfifo(fifo)
            for path in (Path(directory), fifo):
                with self.subTest(path=path.name):
                    result = subprocess.run([sys.executable, "-I", "-B", str(HERE / "check.py"), str(path)],
                                            capture_output=True, text=True, timeout=5)
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertEqual(json.loads(result.stdout)["status"], "not_assessed")


if __name__ == "__main__":
    unittest.main()
