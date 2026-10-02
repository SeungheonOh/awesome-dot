#!/usr/bin/env python3
"""Behavioral checks for the bundled rehearsal; temporary databases only."""

import copy
import json
from pathlib import Path
import sqlite3
import sys
import tempfile

sys.dont_write_bytecode = True
import rehearse as r


def expect_blocked(action, fragment):
    try:
        action()
    except r.Blocked as exc:
        r.require(fragment in str(exc), "Wrong blocked-operation reason")
        return str(exc)
    raise AssertionError("Operation should have been blocked")


def main():
    checks = []
    fixture_hashes = {p.name: r.digest_bytes(p.read_bytes()) for p in r.FIXTURES.iterdir() if p.is_file()}
    with tempfile.TemporaryDirectory(prefix="schema-rehearsal-checks-") as directory:
        temp = Path(directory)
        result = r.run(temp / "evidence")
        r.require(result["status"] == "passed", "Full rehearsal failed")
        checks.append("Complete rehearsal, reopened schema/rows, constraints, old-code failure and recovery")

        before_files = {p.name: r.digest_bytes(p.read_bytes()) for p in (temp / "evidence").iterdir()}
        try:
            r.run(temp / "evidence")
        except FileExistsError:
            pass
        else:
            raise AssertionError("Existing evidence directory was accepted")
        r.require(before_files == {p.name: r.digest_bytes(p.read_bytes()) for p in (temp / "evidence").iterdir()},
                  "Existing evidence changed")
        checks.append("Existing output refused and every previous artifact hash preserved")

        con = r.seed(temp / "controls.sqlite")
        try:
            baseline = r.state(con)
            resolved = r.plan(baseline, r.load("decision-resolved.json"))
            bad_values = ("", " 1h", "1h ", "1.5h", "half day", "1d 2m", "-1m", "١h", str(2**63) + "m")
            for text in bad_values:
                altered = copy.deepcopy(baseline)
                altered["rows"]["work_item"][0]["estimate_text"] = text
                rejected = r.plan(altered, r.load("decision-resolved.json"))
                r.require(rejected["status"] == "blocked" and "W-001" in rejected["blocked_items"],
                          "Unsupported source text was silently converted")
                expect_blocked(lambda: r.migrate(con, rejected), "Unresolved semantics")
                r.require(r.state(con) == baseline, "Blocked syntax case changed database")
            checks.append("Unsupported/blank/whitespace/fractional/overflow estimate syntax blocks without writes")

            wrong = {**r.load("decision-resolved.json"), "change_id": "different-change"}
            expect_blocked(lambda: r.plan(baseline, wrong), "different change")
            for day in (None, True, 0, 2**63):
                decision = {**r.load("decision-resolved.json"), "workday_minutes": day}
                r.require(r.plan(baseline, decision)["blocked_items"] == ["W-041"],
                          "Invalid day decision was accepted")
            checks.append("Decision is change-bound and requires an explicit valid workday value")

            con.execute("UPDATE work_item SET title=? WHERE id=?", ("New source revision", "W-001"))
            revised = r.state(con)
            expect_blocked(lambda: r.migrate(con, resolved), "Source version or logical content changed")
            r.require(r.state(con) == revised, "Drift handling erased a newer source edit")
            checks.append("Stale plan rejected while preserving the newer source revision")
        finally:
            con.close()

        con = r.seed(temp / "dependency.sqlite")
        try:
            con.execute("CREATE VIEW legacy_estimates AS SELECT id, estimate_text FROM work_item")
            with_view = r.state(con)
            view_plan = r.plan(with_view, r.load("decision-resolved.json"))
            try:
                r.migrate(con, view_plan)
            except sqlite3.OperationalError as exc:
                dependency_error = str(exc)
                r.require("legacy_estimates" in dependency_error and "estimate_text" in dependency_error,
                          "Unexpected schema dependency failure")
            else:
                raise AssertionError("Dependent view should prevent DROP COLUMN")
            r.require(not con.in_transaction and r.state(con) == with_view,
                      "Dependency failure did not preserve the view, schema, and rows")
            checks.append("A dependent view stops DROP COLUMN and the entire transaction rolls back")
        finally:
            con.close()

        con = r.seed(temp / "repeat.sqlite")
        try:
            repeat_plan = r.plan(r.state(con), r.load("decision-resolved.json"))
            r.migrate(con, repeat_plan)
            already_done = r.state(con)
            expect_blocked(lambda: r.migrate(con, repeat_plan), "Source version or logical content changed")
            r.require(r.state(con) == already_done, "Repeated migration changed version 2")
            checks.append("Already-applied migration rejected without duplicate backfill")
        finally:
            con.close()

        # Independent sqlite3 connection reloads the saved SQL, rather than trusting
        # a JSON serializer or reusing the backup routine as its own verification.
        for name, expected_file in (("after", "after.json"), ("restored", "restored.json")):
            db = temp / (name + "-export-readback.sqlite")
            with db.open("xb"):
                pass
            con = sqlite3.connect(db, autocommit=True)
            try:
                con.executescript((temp / "evidence" / (name + ".sql")).read_text(encoding="utf-8"))
                con.row_factory = sqlite3.Row
                expected = json.loads((temp / "evidence" / expected_file).read_text(encoding="utf-8"))
                r.require(r.state(con) == expected, "Saved SQL did not reproduce saved schema/rows")
                r.integrity(con)
            finally:
                con.close()
        checks.append("Final and recovered SQL exports reload into new files with identical schema/rows and valid FKs")

    r.require(fixture_hashes == {p.name: r.digest_bytes(p.read_bytes()) for p in r.FIXTURES.iterdir() if p.is_file()},
              "Behavioral checks modified source evidence")
    checks.append("All original fixture bytes unchanged")
    print(json.dumps({"status": "passed", "checks": checks, "dependency_error": dependency_error}, indent=2))


if __name__ == "__main__":
    main()
