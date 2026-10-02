#!/usr/bin/env python3
"""Execute only the bundled fictional SQLite schema-change rehearsal.

Python 3.12+ / SQLite 3.35+. No arbitrary database path, SQL, or network target.
All database files live in an owned temporary directory. Outputs are text evidence.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"
MAX_INTEGER = 9223372036854775807
TABLES = ("owner", "work_item", "item_note", "work_estimate")
OLD_READ = "SELECT id, estimate_text FROM work_item ORDER BY id"
NEW_READ = """SELECT w.id, w.title, w.owner_id, w.archived_at, e.estimated_minutes
FROM work_item AS w LEFT JOIN work_estimate AS e ON e.item_id = w.id
ORDER BY w.id"""
CREATE_ESTIMATE = """CREATE TABLE work_estimate (
    item_id TEXT NOT NULL PRIMARY KEY REFERENCES work_item(id) ON DELETE RESTRICT,
    estimated_minutes INTEGER NOT NULL
        CHECK (typeof(estimated_minutes) = 'integer' AND estimated_minutes >= 0),
    original_text TEXT NOT NULL
)"""


class Blocked(ValueError):
    """A supplied meaning or source precondition is unresolved."""


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def digest(value):
    return digest_bytes(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                   separators=(",", ":")).encode("utf-8"))


def load(name):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def connect(path, *, new=False, readonly=False):
    if new:
        with path.open("xb"):
            pass
    mode = "ro" if readonly else "rw"
    con = sqlite3.connect(path.resolve().as_uri() + "?mode=" + mode,
                          uri=True, autocommit=True, timeout=2.0)
    try:
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        require(con.execute("PRAGMA foreign_keys").fetchone()[0] == 1,
                "Foreign-key enforcement is unavailable")
        return con
    except BaseException:
        con.close()
        raise


def query(con, sql, parameters=()):
    return [dict(row) for row in con.execute(sql, parameters)]


def state(con):
    schema = query(con, """SELECT type, name, tbl_name, sql FROM sqlite_schema
        WHERE name NOT LIKE 'sqlite_%' ORDER BY type, name""")
    actual_tables = {row["name"] for row in schema if row["type"] == "table"}
    require(actual_tables <= set(TABLES), "Unexpected table in the fixture")
    rows = {}
    for table in TABLES:
        if table in actual_tables:
            key = "item_id" if table == "work_estimate" else "id"
            rows[table] = query(con, f'SELECT * FROM "{table}" ORDER BY "{key}"')
    return {"user_version": con.execute("PRAGMA user_version").fetchone()[0],
            "schema": schema, "rows": rows}


def integrity(con):
    check = [row[0] for row in con.execute("PRAGMA integrity_check")]
    foreign_keys = [list(row) for row in con.execute("PRAGMA foreign_key_check")]
    require(check == ["ok"] and not foreign_keys, "Integrity or relationship check failed")
    return {"integrity_check": check, "foreign_key_check": foreign_keys,
            "foreign_keys_enabled": con.execute("PRAGMA foreign_keys").fetchone()[0] == 1}


def seed(path):
    con = connect(path, new=True)
    try:
        require(con.execute("PRAGMA journal_mode = WAL").fetchone()[0] == "wal",
                "Fixture could not enter WAL mode")
        # Only this inspected, bundled fixture is executed as a script. No migration
        # transaction is open here; migration uses execute() statement by statement.
        con.executescript((FIXTURES / "source.sql").read_text(encoding="utf-8"))
        integrity(con)
        return con
    except BaseException:
        con.close()
        raise


def backup_new(source, destination):
    target = connect(destination, new=True)
    try:
        source.backup(target)
        require(state(source) == state(target), "Backup differs logically from source")
        integrity(target)
    finally:
        target.close()


def minutes(text, decision):
    if text is None:
        return None
    match = re.fullmatch(r"([0-9]+)([mhd])(?: ([0-9]+)m)?", text)
    if not match or (match[3] is not None and match[2] != "h"):
        raise Blocked("Unsupported estimate syntax; do not guess or normalize")
    number, unit = int(match[1]), match[2]
    if unit == "d":
        day = decision.get("workday_minutes")
        if (decision.get("status") != "resolved" or type(day) is not int
                or not 1 <= day <= MAX_INTEGER):
            raise Blocked("Supply the queue owner's workday-minutes decision")
        result = number * day
    elif unit == "h":
        result = number * 60 + int(match[3] or 0)
    else:
        result = number
    if result > MAX_INTEGER:
        raise Blocked("Converted minutes exceed SQLite's signed integer range")
    return result


def plan(before, decision):
    if decision.get("change_id") != "work-estimates-v2":
        raise Blocked("Decision belongs to a different change")
    entries, blockers = [], []
    for row in before["rows"]["work_item"]:
        entry = {"item_id": row["id"], "original_text": row["estimate_text"]}
        try:
            entry["estimated_minutes"] = minutes(row["estimate_text"], decision)
            entry["action"] = "no estimate row" if row["estimate_text"] is None else "backfill"
        except Blocked as exc:
            entry["action"] = "blocked"
            entry["reason"] = str(exc)
            blockers.append(row["id"])
        entries.append(entry)
    return {"change_id": "work-estimates-v2", "status": "blocked" if blockers else "ready",
            "source_logical_sha256": digest(before), "decision_sha256": digest(decision),
            "contract_sha256": digest(load("change-contract.json")),
            "blocked_items": blockers, "entries": entries}


def validate_after(con, before, migration_plan):
    after = state(con)
    expected_items = [{key: value for key, value in row.items() if key != "estimate_text"}
                      for row in before["rows"]["work_item"]]
    require(after["rows"]["work_item"] == expected_items, "Original item values changed")
    for table in ("owner", "item_note"):
        require(after["rows"][table] == before["rows"][table], f"{table} records changed")
    expected_estimates = [{key: entry[key] for key in
                          ("item_id", "estimated_minutes", "original_text")}
                         for entry in migration_plan["entries"] if entry["action"] == "backfill"]
    require(after["rows"]["work_estimate"] == expected_estimates, "Estimate backfill differs")
    original_objects = {(row["type"], row["name"]): row for row in before["schema"]
                        if row["name"] != "work_item"}
    actual_objects = {(row["type"], row["name"]): row for row in after["schema"]}
    require(all(actual_objects.get(key) == value for key, value in original_objects.items()),
            "An unrelated schema object changed")
    readback = query(con, NEW_READ)
    require({row["id"]: row["estimated_minutes"] for row in readback}
            == load("expected.json")["minutes_by_item"], "Independent per-item control failed")
    totals = {}
    for group, predicate in (("active", "IS NULL"), ("archived", "IS NOT NULL")):
        totals[group] = query(con, f"""SELECT COUNT(*) AS items,
          COUNT(e.item_id) AS known_estimates,
          COUNT(*) - COUNT(e.item_id) AS unknown_estimates,
          SUM(e.estimated_minutes) AS known_minutes
          FROM work_item AS w LEFT JOIN work_estimate AS e ON e.item_id = w.id
          WHERE w.archived_at {predicate}""")[0]
    require(totals == load("expected.json")["business_totals"], "Business controls differ")
    return {"readback": readback, "business_totals": totals, **integrity(con)}


def migrate(con, migration_plan, *, inject_duplicate=False):
    if migration_plan["status"] != "ready":
        raise Blocked("Unresolved semantics; schema was not changed")
    before = state(con)
    if before["user_version"] != 1 or digest(before) != migration_plan["source_logical_sha256"]:
        raise Blocked("Source version or logical content changed; replan before migration")
    con.execute("BEGIN IMMEDIATE")
    try:
        # Recheck after obtaining the write transaction, not only before BEGIN.
        require(state(con) == before, "Source changed before the transaction began")
        con.execute(CREATE_ESTIMATE)
        con.executemany("INSERT INTO work_estimate VALUES (?, ?, ?)",
                        [(entry["item_id"], entry["estimated_minutes"], entry["original_text"])
                         for entry in migration_plan["entries"] if entry["action"] == "backfill"])
        con.execute("ALTER TABLE work_item DROP COLUMN estimate_text")
        if inject_duplicate:
            # Ordinary accidental repeated backfill, after DDL and data changes.
            con.execute("INSERT INTO work_estimate VALUES (?, ?, ?)", ("W-001", 90, "1h 30m"))
        validation = validate_after(con, before, migration_plan)
        con.execute("PRAGMA user_version = 2")
        con.execute("COMMIT")
        return {"status": "committed", **validation}
    except BaseException:
        if con.in_transaction:
            con.execute("ROLLBACK")
        raise


def rejected_statement(con, name, sql, params, expected_fragment):
    before = state(con)
    con.execute("SAVEPOINT probe")
    error = None
    try:
        con.execute(sql, params).fetchall()
    except sqlite3.DatabaseError as exc:
        error = str(exc)
    finally:
        con.execute("ROLLBACK TO probe")
        con.execute("RELEASE probe")
    require(error is not None and expected_fragment in error, f"{name} was not rejected as expected")
    require(state(con) == before, f"{name} changed persisted state")
    return {"name": name, "error": error, "state_unchanged": True}


def constraint_probes(con):
    return [
        rejected_statement(con, "orphan estimate", "INSERT INTO work_estimate VALUES (?, ?, ?)",
                           ("W-MISSING", 5, "5m"), "FOREIGN KEY"),
        rejected_statement(con, "negative minutes", "UPDATE work_estimate SET estimated_minutes=? WHERE item_id=?",
                           (-1, "W-001"), "CHECK constraint"),
        rejected_statement(con, "fractional minutes", "UPDATE work_estimate SET estimated_minutes=? WHERE item_id=?",
                           (1.5, "W-001"), "CHECK constraint"),
        rejected_statement(con, "null source text", "UPDATE work_estimate SET original_text=NULL WHERE item_id=?",
                           ("W-001",), "NOT NULL"),
        rejected_statement(con, "old reader", OLD_READ, (), "no such column: estimate_text"),
        rejected_statement(con, "old writer", "UPDATE work_item SET estimate_text=? WHERE id=?",
                           ("3h", "W-001"), "no such column: estimate_text")]


def write_json(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    require(json.loads(path.read_text(encoding="utf-8")) == value, "Saved JSON failed readback")


def write_sql(path, con):
    # This is an inspectable data/schema artifact, not the exercised backup mechanism.
    with path.open("x", encoding="utf-8") as stream:
        stream.write("-- Inspection export; replay only into a new empty disposable database.\n")
        stream.write("PRAGMA foreign_keys = OFF;\n")
        stream.write(f"PRAGMA user_version = {state(con)['user_version']};\n")
        stream.write("\n".join(con.iterdump()) + "\n")
        stream.write("PRAGMA foreign_keys = ON;\nPRAGMA foreign_key_check;\nPRAGMA integrity_check;\n")


def run(output):
    require(sys.version_info >= (3, 12), "Python 3.12 or newer is required")
    require(sqlite3.sqlite_version_info >= (3, 35, 0), "SQLite 3.35 or newer is required")
    inputs = {path.name: digest_bytes(path.read_bytes()) for path in sorted(FIXTURES.iterdir()) if path.is_file()}
    output.mkdir(parents=False, exist_ok=False)
    with tempfile.TemporaryDirectory(prefix="schema-rehearsal-") as directory:
        temp = Path(directory)
        source = seed(temp / "source.sqlite")
        try:
            before = state(source)
            wal_bytes = (temp / "source.sqlite-wal").stat().st_size
            require(wal_bytes > 0, "Expected committed fixture content in WAL")
            backup_new(source, temp / "before.sqlite")
            require(state(source) == before, "Snapshot creation changed source")
        finally:
            source.close()

        snapshot = connect(temp / "before.sqlite", readonly=True)
        try:
            for name in ("failed.sqlite", "migrated.sqlite"):
                backup_new(snapshot, temp / name)
            pending = plan(before, load("decision-pending.json"))
            resolved = plan(before, load("decision-resolved.json"))
            require(pending["blocked_items"] == ["W-041"], "Expected only the day ambiguity")
            failed = connect(temp / "failed.sqlite")
            failure_trace = []
            try:
                try:
                    migrate(failed, pending)
                except Blocked as exc:
                    ambiguity_error = str(exc)
                else:
                    raise AssertionError("Unresolved migration ran")
                require(state(failed) == before, "Ambiguity changed source")
                failed.set_trace_callback(lambda sql: failure_trace.append(sql)
                    if sql.startswith(("BEGIN", "CREATE", "INSERT", "ALTER", "COMMIT", "ROLLBACK")) else None)
                try:
                    migrate(failed, resolved, inject_duplicate=True)
                except sqlite3.IntegrityError as exc:
                    failure_error = str(exc)
                    require("UNIQUE constraint" in failure_error, "Unexpected injected failure")
                else:
                    raise AssertionError("Injected duplicate did not fail")
                require(not failed.in_transaction and state(failed) == before,
                        "DDL/data rollback did not restore the full pre-change state")
            finally:
                failed.close()
            failed = connect(temp / "failed.sqlite", readonly=True)
            try:
                require(state(failed) == before, "Rollback differs after reopening")
                failure = {"ambiguity_error": ambiguity_error, "injected_error": failure_error,
                           "injection_point": "after backfill and DROP COLUMN, before COMMIT",
                           "transaction_trace": failure_trace,
                           "reopened_state_equals_before": True, "logical_sha256": digest(state(failed)),
                           **integrity(failed)}
            finally:
                failed.close()

            migrated = connect(temp / "migrated.sqlite")
            try:
                migration = migrate(migrated, resolved)
            finally:
                migrated.close()
            migrated = connect(temp / "migrated.sqlite")
            try:
                after = state(migrated)
                require(after["user_version"] == 2, "Version did not persist")
                reopened = validate_after(migrated, before, resolved)
                probes = constraint_probes(migrated)
                write_sql(output / "after.sql", migrated)
                backup_new(migrated, temp / "later-writes.sqlite")
            finally:
                migrated.close()

            later = connect(temp / "later-writes.sqlite")
            try:
                later.execute("BEGIN IMMEDIATE")
                later.execute("UPDATE work_item SET title=? WHERE id=?", ("Batch preview v2", "W-041"))
                later.execute("UPDATE work_estimate SET estimated_minutes=? WHERE item_id=?", (600, "W-041"))
                later.execute("COMMIT")
                post_change = state(later)
                integrity(later)
            finally:
                later.close()
            # Recovery is a real SQLite backup restore to a NEW separate destination.
            # The successful migration and later-writes branch remain intact.
            backup_new(snapshot, temp / "restored.sqlite")
            restored = connect(temp / "restored.sqlite", readonly=True)
            try:
                restored_state = state(restored)
                require(restored_state == before, "Recovery changed original schema or data")
                old_reader = query(restored, OLD_READ)
                require(len(old_reader) == 5, "Old reader did not recover")
                later_item = next(row for row in post_change["rows"]["work_item"] if row["id"] == "W-041")
                later_estimate = next(row for row in post_change["rows"]["work_estimate"] if row["item_id"] == "W-041")
                restored_item = next(row for row in restored_state["rows"]["work_item"] if row["id"] == "W-041")
                restored_minutes = minutes(restored_item["estimate_text"], load("decision-resolved.json"))
                require(later_item["title"] != restored_item["title"]
                        and later_estimate["estimated_minutes"] != restored_minutes,
                        "Later writes were not distinguished from snapshot recovery")
                write_sql(output / "restored.sql", restored)
                recovery = {"method": "sqlite3.Connection.backup from pre-change snapshot into a new file",
                            "reopened_state_equals_before": True,
                            "old_reader": old_reader, **integrity(restored),
                            "later_writes_not_in_snapshot": [
                                {"item_id": "W-041", "field": "title", "later": later_item["title"],
                                 "restored": restored_item["title"]},
                                {"item_id": "W-041", "field": "estimated_minutes",
                                 "later": later_estimate["estimated_minutes"],
                                 "restored_version_has_this_column": False,
                                 "restored_legacy_text": restored_item["estimate_text"],
                                 "legacy_text_minutes_under_supplied_decision": restored_minutes}],
                            "application_rollback_alone_compatible": False}
            finally:
                restored.close()
            later = connect(temp / "later-writes.sqlite", readonly=True)
            try:
                require(state(later) == post_change, "Recovery modified the later-writes branch")
            finally:
                later.close()
            require(state(snapshot) == before, "Pre-change backup was modified")
        finally:
            snapshot.close()

    for name, value in (("before.json", before), ("plan-pending.json", pending),
                        ("plan-resolved.json", resolved), ("failed-transaction.json", failure),
                        ("after.json", after), ("later-writes.json", post_change),
                        ("restored.json", restored_state)):
        write_json(output / name, value)
    require(inputs == {path.name: digest_bytes(path.read_bytes()) for path in sorted(FIXTURES.iterdir()) if path.is_file()},
            "Fixture evidence changed")
    result = {"status": "passed", "runtime": {"python": sys.version.split()[0], "sqlite": sqlite3.sqlite_version},
              "input_sha256": inputs,
              "snapshot": {"method": "sqlite3.Connection.backup", "source_journal_mode": "wal",
                           "source_wal_had_committed_content": wal_bytes > 0,
                           "source_wal_bytes_observed": wal_bytes, "concurrent_writers_tested": False},
              "logical_sha256": {"before": digest(before), "after": digest(after),
                                 "failed_after_rollback": failure["logical_sha256"],
                                 "restored": digest(restored_state), "later_writes": digest(post_change)},
              "migration": migration, "reopened_readback": reopened,
              "constraint_and_application_probes": probes, "recovery": recovery,
              "limits": ["Synthetic local fixture only; no production migration or deployment occurred.",
                         "Old reader and writer fail against version 2; deploy matching application code.",
                         "Snapshot recovery omits later writes; no lossless down migration is claimed.",
                         "No crash, disk-full, concurrent-writer, load, or mixed-version rollout test was performed.",
                         "Database binaries were temporary; the saved SQL and JSON are inspection evidence."]}
    write_json(output / "result.json", result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New evidence directory; parent must exist")
    args = parser.parse_args()
    try:
        result = run(args.output)
    except (OSError, sqlite3.Error, ValueError, AssertionError) as exc:
        parser.exit(1, f"Rehearsal stopped: {exc}\n")
    print(json.dumps({"status": result["status"], "output": str(args.output),
                      "business_totals": result["reopened_readback"]["business_totals"]}, indent=2))


if __name__ == "__main__":
    main()
