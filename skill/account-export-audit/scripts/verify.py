#!/usr/bin/env python3
"""Independent readback plus behavioral countercases, using only fictional files."""
import csv
from hashlib import sha256
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from audit import audit, read_archive, UnsupportedArchive
from build_fixtures import build

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
ARCHIVES = FIXTURES / "archives"
PART1 = ARCHIVES / "cobalt-part-1.zip"
PART2 = ARCHIVES / "cobalt-part-2.zip"
LATER = ARCHIVES / "amber-part-2.zip"


def json_read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def rewrite(source, target, change):
    # Only normal synthetic members and data are used in these countercases.
    with zipfile.ZipFile(source) as original:
        members = {name: original.read(name) for name in original.namelist()}
    change(members)
    with zipfile.ZipFile(target, "x", compression=zipfile.ZIP_STORED) as output:
        for name, value in members.items():
            output.writestr(name, value)


class AuditChecks(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="export-audit-fictional-")
        self.work = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def run_audit(self, parts=None, name="run", incomplete=False):
        destination = self.work / name
        report = audit(FIXTURES, parts or [PART1, PART2, LATER], destination, incomplete)
        return report, destination

    def copy_controls(self):
        destination = self.work / "controls"
        destination.mkdir()
        for name in ("need.json", "source-control.json", "source-inventory.csv"):
            (destination / name).write_bytes((FIXTURES / name).read_bytes())
        return destination

    def write_inventory_value(self, controls, identifier, field, value):
        path = controls / "source-inventory.csv"
        with path.open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        next(row for row in rows if row["id"] == identifier)[field] = value
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def test_saved_outputs_reproduce_and_inputs_stay_unchanged(self):
        original = {p.relative_to(FIXTURES): p.read_bytes() for p in FIXTURES.rglob("*") if p.is_file()}
        cases = [("partial", [PART1, LATER], False), ("resolved", [PART1, PART2, LATER], False),
                 ("incomplete-control", [PART1, PART2, LATER], True)]
        for name, parts, incomplete in cases:
            _, output = self.run_audit(parts, name, incomplete)
            committed = ROOT / "outputs" / name
            observed = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
            saved = {p.relative_to(committed): p.read_bytes() for p in committed.rglob("*") if p.is_file()}
            self.assertEqual(observed, saved)
        self.assertEqual(original, {p.relative_to(FIXTURES): p.read_bytes() for p in FIXTURES.rglob("*") if p.is_file()})

    def test_deterministic_archive_bytes(self):
        generated = self.work / "archives"
        build(generated)
        for path in ARCHIVES.glob("*.zip"):
            self.assertEqual(path.read_bytes(), (generated / path.name).read_bytes())

    def test_independent_ids_relationships_counts_and_bytes(self):
        report, output = self.run_audit()
        # Parse controls and saved data afresh without the audit's reconciliation helpers.
        with (FIXTURES / "source-inventory.csv").open(encoding="utf-8", newline="") as stream:
            rows = list(csv.DictReader(stream))
        expected = {r["id"]: r for r in rows if r["in_scope"] == "yes"}
        records = json_read(output / "consolidated/records.json")
        actual = {r["id"]: r for r in records}
        self.assertEqual(len(actual), len(records))
        self.assertEqual(set(actual), set(expected))
        self.assertEqual(len(actual), 5)
        for identifier, row in expected.items():
            record = actual[identifier]
            self.assertEqual((record["kind"], record["state"], record["revision"], record["parent_id"]),
                             (row["kind"], row["state"], row["revision"], row["parent_id"] or None))
            self.assertEqual(record.get("attachment_ids", []), json.loads(row["attachment_ids"]))
            if record["parent_id"] is not None:
                self.assertIn(record["parent_id"], actual)
        source_records = []
        for part in (PART1, PART2):
            with zipfile.ZipFile(part) as archive:
                source_records.extend(json.loads(archive.read("records.json")))
        self.assertEqual(records, source_records)
        controls = json_read(FIXTURES / "source-control.json")["attachments"]
        total_bytes = 0
        for item in controls:
            payload = (output / "consolidated" / item["path"]).read_bytes()
            self.assertEqual(len(payload), item["bytes"])
            self.assertEqual(sha256(payload).hexdigest(), item["sha256"])
            self.assertIn(item["id"], actual[item["owner_id"]]["attachment_ids"])
            total_bytes += len(payload)
        self.assertEqual(total_bytes, 95)
        self.assertEqual(report["counts"]["expected_objects"], report["counts"]["matched_objects"] + report["counts"]["missing_objects"] + report["counts"]["conflicting_objects"])
        self.assertEqual(report["counts"]["observed_attachment_references"], len(controls))
        self.assertEqual(report["counts"]["matched_attachment_bytes"], total_bytes)

    def test_missing_null_empty_and_tombstone_remain_distinct(self):
        _, output = self.run_audit()
        records = {r["id"]: r for r in json_read(output / "consolidated/records.json")}
        self.assertEqual(records["note-0001"]["body"], "")
        self.assertNotIn("color", records["note-0001"])
        self.assertIsNone(records["note-0002"]["color"])
        self.assertEqual(records["note-0002"]["tags"], ["loaner", "café"])
        self.assertEqual(records["note-0003"]["state"], "deleted")
        self.assertNotIn("body", records["note-0003"])
        self.assertNotIn("attachment_ids", records["note-0003"])

    def test_partial_cannot_borrow_from_later_generation(self):
        report, output = self.run_audit([PART1, LATER])
        self.assertEqual(report["status"], "held")
        self.assertEqual(report["missing_parts"], [2])
        self.assertEqual(report["counts"]["missing_objects"], 3)
        self.assertEqual(report["counts"]["matched_attachment_bytes"], 39)
        self.assertEqual([r["status"] for r in report["records"] if r["id"] == "note-0002"], ["missing"])
        self.assertFalse((output / "consolidated").exists())

    def test_resolved_keeps_later_generation_held(self):
        report, output = self.run_audit()
        self.assertEqual(report["status"], "supported-for-stated-snapshot-copy")
        later = [a for a in report["archives"] if a["name"] == LATER.name][0]
        self.assertEqual(later["status"], "held")
        self.assertEqual(later["generation"], "generation-43")
        records = {r["id"]: r for r in json_read(output / "consolidated/records.json")}
        self.assertEqual(records["note-0002"]["revision"], "7")
        self.assertEqual(records["note-0002"]["title"], "Loaner bag")

    def test_all_archive_rows_do_not_prove_source_coverage(self):
        report, output = self.run_audit(incomplete=True)
        self.assertEqual(report["counts"]["matched_objects"], 5)
        self.assertEqual(report["counts"]["matched_attachment_bytes"], 95)
        self.assertFalse(report["control_complete"])
        self.assertEqual(report["status"], "held")
        self.assertFalse((output / "consolidated").exists())

    def test_missing_required_body_is_not_an_empty_body(self):
        changed = self.work / "missing-body.zip"
        def mutation(members):
            records = json.loads(members["records.json"])
            records[0].pop("body")
            members["records.json"] = json.dumps(records).encode()
        rewrite(PART2, changed, mutation)
        report, output = self.run_audit([PART1, changed])
        self.assertEqual(report["counts"]["conflicting_objects"], 1)
        self.assertFalse((output / "consolidated").exists())

    def test_same_length_attachment_change_is_detected(self):
        changed = self.work / "different-bytes.zip"
        def mutation(members):
            path = "attachments/attachment-002/notes.txt"
            members[path] = b"c" + members[path][1:]
        rewrite(PART2, changed, mutation)
        report, output = self.run_audit([PART1, changed])
        attachment = next(a for a in report["attachments"] if a["id"] == "attachment-002")
        self.assertEqual(attachment["observed_bytes"], attachment["bytes"])
        self.assertEqual(attachment["status"], "conflicting")
        self.assertFalse((output / "consolidated").exists())

    def test_equal_total_with_wrong_identity_still_fails(self):
        changed = self.work / "wrong-object.zip"
        def mutation(members):
            records = json.loads(members["records.json"])
            records[-1]["id"] = "note-0088"
            members["records.json"] = json.dumps(records).encode()
        rewrite(PART2, changed, mutation)
        report, output = self.run_audit([PART1, changed])
        self.assertEqual(report["counts"]["missing_objects"], 1)
        self.assertEqual(report["unexpected_ids"], ["note-0088"])
        self.assertFalse((output / "consolidated").exists())

    def test_duplicate_part_has_no_first_or_last_winner(self):
        report, output = self.run_audit([PART1, PART2, PART2])
        self.assertIn("note-0002", report["duplicate_ids"])
        self.assertEqual(report["status"], "held")
        self.assertFalse((output / "consolidated").exists())

    def test_existing_output_is_never_overwritten(self):
        destination = self.work / "existing"
        destination.mkdir()
        marker = destination / "keep.txt"
        marker.write_text("original", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            audit(FIXTURES, [PART1, PART2], destination)
        self.assertEqual(marker.read_text(), "original")

    def test_benign_member_count_limit_is_enforced(self):
        path = self.work / "too-many-members.zip"
        with zipfile.ZipFile(path, "x") as archive:
            for index in range(33):
                archive.writestr(f"attachments/item-{index}/note.txt", b"sample\n")
        with self.assertRaisesRegex(UnsupportedArchive, "member count"):
            read_archive(path)

    def test_missing_control_and_payload_do_not_erase_a_required_attachment(self):
        controls = self.copy_controls()
        control = json_read(controls / "source-control.json")
        control["attachments"] = control["attachments"][:1]
        (controls / "source-control.json").write_text(json.dumps(control), encoding="utf-8")
        changed = self.work / "missing-attachment.zip"
        rewrite(PART2, changed, lambda members: members.pop("attachments/attachment-002/notes.txt"))
        output = self.work / "run"
        report = audit(controls, [PART1, changed], output)
        self.assertEqual(report["status"], "held")
        self.assertFalse(report["attachment_controls_complete"])
        self.assertEqual(report["counts"]["expected_attachments"], 2)
        self.assertIsNone(report["counts"]["expected_attachment_bytes"])
        self.assertEqual(next(a["status"] for a in report["attachments"] if a["id"] == "attachment-002"), "unresolved")
        self.assertFalse((output / "consolidated").exists())

    def test_repeated_attachment_control_does_not_inflate_matched_bytes(self):
        controls = self.copy_controls()
        control = json_read(controls / "source-control.json")
        control["attachments"].append(dict(control["attachments"][0]))
        (controls / "source-control.json").write_text(json.dumps(control), encoding="utf-8")
        output = self.work / "run"
        report = audit(controls, [PART1, PART2], output)
        self.assertEqual(report["status"], "held")
        self.assertEqual(report["counts"]["expected_attachments"], 2)
        self.assertEqual(report["counts"]["matched_attachment_bytes"], 56)
        self.assertFalse((output / "consolidated").exists())

    def test_audit_only_request_does_not_create_or_claim_a_copy(self):
        controls = self.copy_controls()
        need = json_read(controls / "need.json")
        need["consolidation_authorized"] = False
        (controls / "need.json").write_text(json.dumps(need), encoding="utf-8")
        output = self.work / "run"
        report = audit(controls, [PART1, PART2], output)
        self.assertEqual(report["status"], "supported-for-stated-snapshot-copy")
        self.assertIs(report["consolidated_copy_created"], False)
        self.assertFalse((output / "consolidated").exists())
        self.assertIn("No consolidated copy was requested", (output / "report.md").read_text())

    def test_consolidation_authority_requires_a_json_boolean(self):
        controls = self.copy_controls()
        need = json_read(controls / "need.json")
        invalid_values = ["false", "true", 0, 1, None, [], {}]
        for index, value in enumerate(invalid_values):
            with self.subTest(value=value):
                need["consolidation_authorized"] = value
                (controls / "need.json").write_text(json.dumps(need), encoding="utf-8")
                output = self.work / ("invalid-authority-" + str(index))
                with self.assertRaisesRegex(ValueError, "must be a JSON boolean"):
                    audit(controls, [PART1, PART2], output)
                self.assertFalse(output.exists())
        need.pop("consolidation_authorized")
        (controls / "need.json").write_text(json.dumps(need), encoding="utf-8")
        output = self.work / "missing-authority"
        with self.assertRaisesRegex(ValueError, "must be a JSON boolean"):
            audit(controls, [PART1, PART2], output)
        self.assertFalse(output.exists())

    def test_body_control_cannot_weaken_the_required_note_body(self):
        controls = self.copy_controls()
        changed = self.work / "missing-body.zip"
        def mutation(members):
            records = json.loads(members["records.json"])
            records[0].pop("body")
            members["records.json"] = json.dumps(records).encode()
        rewrite(PART2, changed, mutation)
        for index, value in enumerate(["unknown", "unexamined", "not_applicable", "absent_expected"]):
            with self.subTest(value=value):
                self.write_inventory_value(controls, "note-0002", "body_presence", value)
                output = self.work / ("invalid-body-control-" + str(index))
                with self.assertRaisesRegex(ValueError, "body_presence"):
                    audit(controls, [PART1, changed], output)
                self.assertFalse(output.exists())

    def test_inventory_scope_markers_are_exact(self):
        controls = self.copy_controls()
        for index, value in enumerate(["YES", "true", "", "unknown"]):
            with self.subTest(value=value):
                self.write_inventory_value(controls, "note-9000", "in_scope", value)
                output = self.work / ("invalid-scope-control-" + str(index))
                with self.assertRaisesRegex(ValueError, "in_scope must be exactly yes or no"):
                    audit(controls, [PART1, PART2], output)
                self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
