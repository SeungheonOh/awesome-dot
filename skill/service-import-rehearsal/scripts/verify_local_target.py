#!/usr/bin/env python3
"""Execute a durable local round trip; write portable JSON evidence only.

Run beside the existing rehearsal package, or pass --package to its directory.
Temporary SQLite files stay under --work and are removed after the checks.
"""

import argparse
import csv
import hashlib
import io
import json
import platform
import sqlite3
import sys
import tempfile
import threading
import types
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
from local_target import HEADERS, consume, connect, initialize, parse_import, readback


def sha(data):
    return hashlib.sha256(data).hexdigest()


def csv_bytes(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=HEADERS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if json.loads(path.read_text(encoding="utf-8")) != value:
        raise AssertionError("Saved JSON differs on reopened readback")


def run(package, work, output):
    relative_inputs = ["fixtures/import-contract.json", "fixtures/target-before.json",
                       "fixtures/source.csv", "outputs/import-ready.csv", "scripts/rehearse.py"]
    inputs = {name: (package / name).read_bytes() for name in relative_inputs}
    contract = json.loads(inputs[relative_inputs[0]])
    target = json.loads(inputs[relative_inputs[1]])
    destination = contract["destination"]
    submitted_csv = inputs["outputs/import-ready.csv"]
    rows = parse_import(submitted_csv)
    by_source = {row["source_id"]: row for row in rows}
    checks = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        checks.append(name)

    # Reuse the upstream planner for intended values, never as the target consumer.
    # Loading this exact source via compile produces no files in the input package.
    adapter = types.ModuleType("rehearsal_adapter")
    exec(compile(inputs["scripts/rehearse.py"], "rehearse.py", "exec"), adapter.__dict__)
    plan = adapter.make_plan(contract, target, inputs["fixtures/source.csv"],
                             sha(inputs["fixtures/import-contract.json"]))
    ready = [item for item in plan if item["disposition"] in ("create", "update")]
    check("Actual import CSV equals the adapter's five accepted rows",
          len(rows) == 5 and rows == [adapter.import_row(item, contract) for item in ready])

    work.mkdir(parents=True, exist_ok=True)
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fictional-consumer-", dir=work) as temporary:
        folder = Path(temporary)

        def seeded(name):
            path = folder / f"{name}.sqlite"
            initialize(path, contract, target)
            return path

        def one(path, row, now=60):
            return consume(path, destination, csv_bytes([row]), now)[0]["receipt"]

        def probe(base, suffix, **changes):
            return {**base, "source_id": "P-" + suffix, "idempotency_key": "probe-" + suffix, **changes}

        database = seeded("round-trip")
        seeded_state = readback(database)
        check("All eight original target records are seeded without alteration",
              seeded_state["records"] == target["records"])
        delivered = consume(database, destination, submitted_csv, 0, lose_response_for={"S003"})
        committed = readback(database)
        check("Three creates and two updates committed to disk with durable receipts",
              len(committed["records"]) == 11 and len(committed["operations"]) == 5
              and all(r["receipt"]["result"] == "applied" for r in committed["operations"]))
        records = {r["record_id"]: r for r in committed["records"]}
        for item in ready:
            observed = [r for r in records.values() if r["external_id"] == item["raw"]["external_id"]]
            check(f"{item['source_id']}: fresh-connection state equals planned field values",
                  len(observed) == 1 and all(observed[0][k] == v for k, v in item["intended"].items()))
        check("Six untouched original records, including both legacy 0200 duplicates, are unchanged",
              all(records[r["record_id"]] == r for r in target["records"]
                  if r["record_id"] not in {"F-102", "F-106"})
              and sum(r["external_id"] == "0200" for r in records.values()) == 2)
        check("Updated rows increment their target-generated revisions exactly once",
              records["F-102"]["revision"] == "v8" and records["F-106"]["revision"] == "v5")
        check("Lost response is absent at caller while its real committed receipt is reopened from disk",
              next(r for r in delivered if r["source_id"] == "S003")["receipt"] is None
              and any(r["receipt"]["source_id"] == "S003" for r in committed["operations"]))
        replay_create = one(database, by_source["S003"])
        replay_update = one(database, by_source["S002"])
        check("Same-key create and stale-original-revision update replay return original receipts without effects",
              replay_create == next(r["receipt"] for r in committed["operations"] if r["receipt"]["source_id"] == "S003")
              and replay_update == next(r["receipt"] for r in committed["operations"] if r["receipt"]["source_id"] == "S002")
              and readback(database) == committed)
        mismatch = one(database, {**by_source["S003"], "details": "changed payload"})
        expired = one(database, by_source["S003"], now=86400)
        check("Changed payload and expired replay fail without changing state or original receipts",
              mismatch["error"] == "idempotency_payload_mismatch"
              and expired["error"] == "replay_outside_retention" and readback(database) == committed)

        guard_database = seeded("guards")
        with connect(guard_database) as other_writer:
            other_writer.execute("BEGIN IMMEDIATE")
            other_writer.execute("UPDATE records SET label=?, details=?, revision=? WHERE record_id=?",
                                 ("Concurrent owner edit", "separate writer", "v5", "F-106"))
            other_writer.commit()
        concurrent_before = next(r for r in readback(guard_database)["records"] if r["record_id"] == "F-106")
        partial = consume(guard_database, destination, submitted_csv, 0)
        concurrent_after = readback(guard_database)
        check("Another connection's revision change blocks the stale fifth update while four rows commit",
              [r["receipt"]["result"] for r in partial] == ["applied"] * 4 + ["rejected"]
              and partial[-1]["receipt"]["error"] == "revision_conflict"
              and next(r for r in concurrent_after["records"] if r["record_id"] == "F-106") == concurrent_before)
        duplicate = one(guard_database, probe(by_source["S003"], "duplicate-create"))
        ambiguous = one(guard_database, probe(by_source["S002"], "legacy-duplicate", external_id="0200",
                                               record_id="F-107", expected_revision="v1"))
        check("A new-key duplicate create and an update of legacy duplicate identity are rejected",
              duplicate["error"] == "external_id_exists" and ambiguous["error"] == "missing_or_ambiguous_identity"
              and readback(guard_database)["records"] == concurrent_after["records"])

        semantics = seeded("semantics")
        blank = probe(by_source["S002"], "blank-preserve", label="Renamed, café 🧪", details="")
        blank_receipt = one(semantics, blank)
        blank_state = next(r for r in readback(semantics)["records"] if r["record_id"] == "F-102")
        clear = probe(blank, "explicit-clear", label="", details="__CLEAR__", expected_revision=blank_receipt["revision"])
        one(semantics, clear)
        clear_state = next(r for r in readback(semantics)["records"] if r["record_id"] == "F-102")
        check("Blank update cells preserve old details/status; explicit clear writes SQL NULL and preserves label",
              blank_state["details"] == "old rack" and blank_state["status"] == "active"
              and clear_state["details"] is None and clear_state["label"] == blank_state["label"])
        defaults = probe(by_source["S003"], "create-defaults", external_id="007", label="=1+1", status="", details="")
        one(semantics, defaults)
        exact = probe(defaults, "distinct-leading-zero", external_id="7", label="@queue", details="  café\n🧪  ")
        one(semantics, exact)
        exact_state = readback(semantics)
        created = {r["external_id"]: r for r in exact_state["records"] if r["external_id"] in {"007", "7"}}
        check("Create defaults, distinct leading zeros, formula-like text, whitespace and Unicode persist literally",
              created["007"]["label"] == "=1+1" and created["007"]["status"] == "active"
              and created["007"]["details"] is None and created["7"]["label"] == "@queue"
              and created["7"]["details"] == "  café\n🧪  ")

        race_db = seeded("create-race")
        barrier = threading.Barrier(2)
        competing = [probe(by_source["S003"], f"race-{n}", external_id="0777", label=f"Writer {n}") for n in (1, 2)]

        def race(row):
            barrier.wait(timeout=10)
            return one(race_db, row)

        with ThreadPoolExecutor(max_workers=2) as executor:
            race_receipts = list(executor.map(race, competing))
        race_state = readback(race_db)
        check("Two threaded submissions with different keys create exactly one record for one identity",
              sorted(r["result"] for r in race_receipts) == ["applied", "rejected"]
              and sum(r["external_id"] == "0777" for r in race_state["records"]) == 1
              and next(r for r in race_receipts if r["result"] == "rejected")["error"] == "external_id_exists")

        snapshot_db = seeded("coherent-readback")
        snapshot_before = readback(snapshot_db)
        with connect(snapshot_db) as db:
            journal_mode = db.execute("PRAGMA journal_mode=WAL").fetchone()[0]
        interleaving = []

        def commit_between_selects(statement):
            # WAL allows a real writer COMMIT while the reader snapshot is open.
            # Trigger immediately before the ledger SELECT, after records were read.
            if statement == "SELECT * FROM operations ORDER BY idempotency_key":
                try:
                    interleaving.append(one(snapshot_db, by_source["S003"]))
                except Exception as error:
                    # SQLite trace callbacks swallow exceptions: surface them below.
                    interleaving.append({"error": str(error)})

        @contextmanager
        def traced_connection(path):
            with connect(path) as db:
                db.set_trace_callback(commit_between_selects)
                yield db

        with patch("local_target.connect", traced_connection):
            coherent_snapshot = readback(snapshot_db)
        snapshot_after = readback(snapshot_db)
        check("A real commit between record and receipt SELECTs cannot mix readback snapshots",
              journal_mode == "wal" and len(interleaving) == 1
              and interleaving[0].get("result") == "applied"
              and coherent_snapshot == snapshot_before
              and len(snapshot_after["records"]) == 9
              and len(snapshot_after["operations"]) == 1
              and snapshot_after["scope"]["next_id"] == 2)

        rollback_db = seeded("atomic-rollback")
        before_failure = readback(rollback_db)
        with connect(rollback_db) as db:
            db.execute("CREATE TRIGGER injected_failure BEFORE INSERT ON operations "
                       "BEGIN SELECT RAISE(ABORT, 'injected receipt write failure'); END")
        try:
            one(rollback_db, by_source["S003"])
        except sqlite3.IntegrityError:
            pass
        else:
            raise AssertionError("Injected journal failure did not run")
        check("A receipt-write failure rolls back the record and ID allocation in the same transaction",
              readback(rollback_db) == before_failure)
        try:
            consume(rollback_db, destination, csv_bytes([rows[0], rows[0]]), 0)
        except ValueError:
            pass
        else:
            raise AssertionError("Duplicate batch was accepted")
        check("Repeated source/key rows are rejected before any batch writes",
              readback(rollback_db) == before_failure)

        check("All five original input files retain their exact bytes",
              all((package / name).read_bytes() == data for name, data in inputs.items()))
        with connect(database) as db:
            indexes = [dict(r) for r in db.execute("PRAGMA index_list(records)")]
            unique_columns = [[r["name"] for r in db.execute(f"PRAGMA index_info('{idx['name']}')")]
                              for idx in indexes if idx["unique"]]
            check("The record-ID index is unique; no external-ID uniqueness index is falsely claimed",
                  unique_columns == [["record_id"]])
            check("SQLite integrity check passes on reopened primary target",
                  db.execute("PRAGMA integrity_check").fetchone()[0] == "ok")

        report = {
            "evidence_kind": "Executed local SQLite sample implementing an explicitly fictional contract",
            "executed_at_utc": datetime.now(timezone.utc).isoformat(),
            "runtime": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version},
            "scope": "No network, live accounts, external services, or supplied fictional receipt packet used",
            "input_sha256": {name: sha(data) for name, data in inputs.items()},
            "consumer_sha256": sha(Path(__file__).with_name("local_target.py").read_bytes()),
            "verifier_sha256": sha(Path(__file__).read_bytes()),
            "accepted_csv_rows": len(rows), "created": 3, "updated": 2, "persisted_records": 11,
            "unchanged_original_records": 6, "legacy_duplicate_records_preserved": 2,
            "passed_checks": checks, "passed_check_count": len(checks),
            "caller_observations_with_injected_lost_response": delivered,
            "replay_at_logical_seconds": 60,
            "replay_receipts": [replay_create, replay_update],
            "replay_rejections": [mismatch, expired],
            "stale_revision_batch_receipts": partial,
            "other_writer_record_after_rejected_update": concurrent_before,
            "concurrent_create_receipts": race_receipts,
            "readback_interleaving": {
                "journal_mode": journal_mode,
                "writer_committed": "after records SELECT, before receipt-ledger SELECT",
                "reader_record_count": len(coherent_snapshot["records"]),
                "reader_operation_count": len(coherent_snapshot["operations"]),
                "reader_next_id": coherent_snapshot["scope"]["next_id"],
                "fresh_read_record_count": len(snapshot_after["records"]),
                "fresh_read_operation_count": len(snapshot_after["operations"]),
                "fresh_read_next_id": snapshot_after["scope"]["next_id"],
            },
            "record_indexes": indexes,
            "limitations": [
                "This original local implementation provides no evidence about a real service.",
                "Only fixture records seed the sample; the truncated external snapshot is not made complete.",
                "Atomic uniqueness applies to writers using this consumer; direct SQL can bypass its checks.",
                "Failure injection discards a returned local receipt after commit; it is not a network test.",
                "Replay time is controlled logical time. Expired keys are held, never treated as safe new work.",
                "The two-thread submission test is a bounded check, not a production concurrency or power-loss proof.",
                "CSV quoting is decoded first; idempotency compares canonical UTF-8 bytes of exact cell strings.",
                "Revision generation supports this sample's v-number fixture format only."
            ],
        }
        write_json(output / "local-target-readback.json", committed)
        write_json(output / "local-target-report.json", report)
    print(json.dumps({"passed_checks": len(checks), "accepted_rows": len(rows), "persisted_records": 11}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    run(args.package, args.work, args.output)
