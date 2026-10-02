#!/usr/bin/env python3
"""Original SQLite sample consumer for fictional-asset-registry-v1 only.

No service, account, network, notifications, or formula evaluation is involved.
The durable file is a local sample target, not a replica of any real product.
"""

import csv
import io
import json
import sqlite3
from contextlib import contextmanager


HEADERS = ["source_id", "operation", "external_id", "record_id",
           "expected_revision", "idempotency_key", "label", "status", "details"]
FIELDS = ["label", "status", "details"]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def parse_import(data):
    rows = list(csv.reader(io.StringIO(data.decode("utf-8"), newline=""), strict=True))
    if not rows or rows[0] != HEADERS or any(len(r) != len(HEADERS) for r in rows[1:]):
        raise ValueError("Import headers or record width differ from the fictional contract")
    records = [dict(zip(HEADERS, row)) for row in rows[1:]]
    for field in ("source_id", "external_id", "idempotency_key"):
        values = [row[field] for row in records]
        if any(not value for value in values) or len(values) != len(set(values)):
            raise ValueError(f"Batch requires nonempty, unique {field}")
    return records


@contextmanager
def connect(path):
    db = sqlite3.connect(path, isolation_level=None, timeout=10)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def initialize(path, contract, target):
    if (contract.get("fictional") is not True or target.get("fictional") is not True
            or contract.get("adapter") != "fictional-asset-registry-v1"
            or contract["destination"] != target["destination"]
            or contract["import_headers"] != HEADERS
            or contract["clear_token"] != "__CLEAR__"
            or contract["allowed_status"] != ["active", "retired"]
            or contract["create_default_status"] != "active"):
        raise ValueError("This consumer implements only the supplied fictional adapter")
    if path.exists():
        raise ValueError("Refusing to reset an existing target database")
    with connect(path) as db:
        db.executescript("""
            CREATE TABLE scope (destination TEXT PRIMARY KEY, next_id INTEGER NOT NULL);
            CREATE TABLE records (
                record_id TEXT PRIMARY KEY, external_id TEXT COLLATE BINARY NOT NULL,
                label TEXT NOT NULL, status TEXT NOT NULL, details TEXT,
                revision TEXT NOT NULL);
            CREATE TABLE operations (
                destination TEXT NOT NULL, idempotency_key TEXT NOT NULL,
                payload BLOB NOT NULL, first_submission INTEGER NOT NULL,
                receipt TEXT NOT NULL, PRIMARY KEY(destination, idempotency_key));
        """)
        db.execute("BEGIN IMMEDIATE")
        try:
            db.execute("INSERT INTO scope VALUES (?, 1)", (contract["destination"],))
            for record in target["records"]:
                db.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
                           tuple(record[k] for k in ("record_id", "external_id", *FIELDS, "revision")))
            db.commit()
        except Exception:
            db.rollback()
            raise


def submit(path, destination, row, now):
    """Commit one row and its receipt together; now is controlled logical seconds.

    The request payload is the canonical UTF-8 JSON of exact decoded CSV cells.
    Equivalent CSV quoting gives identical request bytes; cell text is unmodified.
    All writers using this consumer acquire the SQLite write lock before checking
    identity. There is deliberately NO unique external_id database index: the
    original seed contains two legacy rows for one key.
    """
    if set(row) != set(HEADERS) or any(not isinstance(v, str) for v in row.values()):
        raise ValueError("Submission must contain the exact textual import columns")
    payload = canonical(row).encode("utf-8")

    def rejected(error):
        return {"source_id": row["source_id"], "result": "rejected", "error": error}

    with connect(path) as db:
        db.execute("BEGIN IMMEDIATE")
        try:
            if db.execute("SELECT destination FROM scope").fetchone()[0] != destination:
                raise ValueError("Wrong fictional destination")
            prior = db.execute("SELECT * FROM operations WHERE destination=? AND idempotency_key=?",
                               (destination, row["idempotency_key"])).fetchone()
            if prior:
                if prior["payload"] != payload:
                    result = rejected("idempotency_payload_mismatch")
                elif not 0 <= now - prior["first_submission"] < 86400:
                    result = rejected("replay_outside_retention")
                else:
                    result = json.loads(prior["receipt"])
                db.commit()
                return result

            matches = db.execute("SELECT * FROM records WHERE external_id=?", (row["external_id"],)).fetchall()
            error = None
            if not all(row[k] for k in ("source_id", "external_id", "idempotency_key")):
                error = "missing_identity"
            elif row["status"] not in ("", "active", "retired") or row["label"] == "__CLEAR__":
                error = "invalid_value"
            elif row["operation"] == "create":
                if row["record_id"] or row["expected_revision"] or not row["label"]:
                    error = "invalid_create"
                elif matches:
                    error = "external_id_exists"
            elif row["operation"] == "update":
                if len(matches) != 1:
                    error = "missing_or_ambiguous_identity"
                elif matches[0]["record_id"] != row["record_id"]:
                    error = "record_identity_mismatch"
                elif matches[0]["revision"] != row["expected_revision"]:
                    error = "revision_conflict"
                elif not any(row[k] for k in FIELDS):
                    error = "empty_update"
            else:
                error = "unsupported_operation"

            if error:
                result = rejected(error)
            else:
                details = None if row["details"] in ("", "__CLEAR__") else row["details"]
                if row["operation"] == "create":
                    number = db.execute("SELECT next_id FROM scope").fetchone()[0]
                    record_id, revision = f"LOCAL-{number:04d}", "v1"
                    db.execute("UPDATE scope SET next_id=next_id+1")
                    db.execute("INSERT INTO records VALUES (?, ?, ?, ?, ?, ?)",
                               (record_id, row["external_id"], row["label"], row["status"] or "active", details, revision))
                else:
                    before = matches[0]
                    record_id = before["record_id"]
                    revision = f"v{int(before['revision'][1:]) + 1}"
                    values = [row[k] if row[k] else before[k] for k in ("label", "status")]
                    values.append(details if row["details"] else before["details"])
                    cursor = db.execute("UPDATE records SET label=?, status=?, details=?, revision=? "
                                        "WHERE record_id=? AND revision=?",
                                        (*values, revision, record_id, row["expected_revision"]))
                    if cursor.rowcount != 1:
                        raise RuntimeError("Guarded update did not affect exactly one record")
                result = {"source_id": row["source_id"], "result": "applied",
                          "record_id": record_id, "revision": revision}
            db.execute("INSERT INTO operations VALUES (?, ?, ?, ?, ?)",
                       (destination, row["idempotency_key"], payload, now, canonical(result)))
            db.commit()
            return result
        except Exception:
            db.rollback()
            raise


def consume(path, destination, csv_bytes, now, lose_response_for=()):
    observed = []
    for row in parse_import(csv_bytes):
        receipt = submit(path, destination, row, now)
        # Failure injection is after the real local COMMIT, before receipt delivery.
        observed.append({"source_id": row["source_id"],
                         "receipt": None if row["source_id"] in lose_response_for else receipt})
    return observed


def readback(path):
    # Every call opens and closes a fresh connection; never read an in-memory plan.
    with connect(path) as db:
        # Keep the scope, records, and receipt ledger on one consistent snapshot.
        db.execute("BEGIN")
        result = {
            "scope": dict(db.execute("SELECT * FROM scope").fetchone()),
            "records": [dict(r) for r in db.execute("SELECT * FROM records ORDER BY record_id")],
            "operations": [{"destination": r["destination"], "idempotency_key": r["idempotency_key"],
                            "request": json.loads(r["payload"]), "first_submission": r["first_submission"],
                            "receipt": json.loads(r["receipt"])}
                           for r in db.execute("SELECT * FROM operations ORDER BY idempotency_key")],
        }
        db.commit()
        return result
