#!/usr/bin/env python3
"""Generate and reconcile only the bundled fictional FTS5 fixture in a NEW directory.

Usage: python scripts/rehearse_index.py /path/to/new-output-directory
No existing database is accepted. No extensions, networks or subprocesses are used.
"""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import sys

FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "fixture.json"
SCHEMA = """
CREATE TABLE documents (
    doc_id INTEGER PRIMARY KEY,
    revision INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL
);
CREATE VIRTUAL TABLE documents_fts USING fts5(
    title, body, content='documents', content_rowid='doc_id',
    tokenize='unicode61 remove_diacritics 0'
);
"""
FIELDS = ("doc_id", "revision", "title", "body")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fixture():
    raw = FIXTURE.read_bytes()
    require(len(raw) <= 32768, "Fixture exceeds the 32 KiB limit")
    fixture = json.loads(raw)
    for name in ("initial_rows", "current_rows"):
        rows = fixture[name]
        require(1 <= len(rows) <= 12, "Fixture must contain 1–12 rows per snapshot")
        require(all(set(r) == set(FIELDS) for r in rows), "Unexpected fixture fields")
        require(all(type(r["doc_id"]) is int and r["doc_id"] > 0 and
                    type(r["revision"]) is int and r["revision"] > 0 for r in rows),
                "Positive integer document IDs and revisions required")
        require(len({r["doc_id"] for r in rows}) == len(rows), "Duplicate document ID")
        require(all(isinstance(r[k], str) and 0 < len(r[k]) <= 1000
                    for r in rows for k in ("title", "body")), "Invalid fixture text")
    require(1 <= len(fixture["queries"]) <= 24, "Fixture must contain 1–24 queries")
    require(all(isinstance(q["expression"], str) and 0 < len(q["expression"]) <= 100
                for q in fixture["queries"]), "Invalid fixture query")
    return fixture, hashlib.sha256(raw).hexdigest()


def ordered(rows):
    return sorted(rows, key=lambda r: r["doc_id"])


def insert_row(db, row):
    db.execute("INSERT INTO documents VALUES (?, ?, ?, ?)", tuple(row[k] for k in FIELDS))


def make_stale_original(path, fixture):
    """Deliberately omit FTS maintenance after one complete initial build."""
    with sqlite3.connect(path) as db:
        db.execute("PRAGMA journal_mode=DELETE")
        db.executescript(SCHEMA)
        for row in fixture["initial_rows"]:
            insert_row(db, row)
        db.execute("INSERT INTO documents_fts(documents_fts) VALUES ('rebuild')")
        initial = {r["doc_id"]: r for r in fixture["initial_rows"]}
        current = {r["doc_id"]: r for r in fixture["current_rows"]}
        for doc_id in initial.keys() - current.keys():
            db.execute("DELETE FROM documents WHERE doc_id=?", (doc_id,))
        for doc_id, row in current.items():
            if doc_id not in initial:
                insert_row(db, row)
            elif row != initial[doc_id]:
                db.execute("UPDATE documents SET revision=?, title=?, body=? WHERE doc_id=?",
                           (row["revision"], row["title"], row["body"], doc_id))
    db.close()


def integrity(db, compare_content):
    """FTS checks use SQL INSERT syntax; execute only on a disposable memory copy."""
    try:
        db.execute("INSERT INTO documents_fts(documents_fts, rank) VALUES ('integrity-check', ?)",
                   (int(compare_content),))
        return {"status": "pass"}
    except sqlite3.DatabaseError as exc:
        return {"status": "error", "sqlite_errorname": getattr(exc, "sqlite_errorname", None),
                "message": str(exc)}
    finally:
        db.rollback()


def inspect(path, queries):
    """Read disk through a read-only connection; all diagnostic writes stay in memory."""
    source = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    db = sqlite3.connect(":memory:")
    try:
        source.backup(db)
    finally:
        source.close()
    try:
        db.row_factory = sqlite3.Row
        rows = [dict(r) for r in db.execute("SELECT * FROM documents ORDER BY doc_id")]
        by_id = {r["doc_id"]: r for r in rows}
        ordinary = [dict(r) for r in db.execute(
            "SELECT rowid, title, body FROM documents_fts ORDER BY rowid")]
        ledger = []
        for query in queries:
            ids = [r[0] for r in db.execute(
                "SELECT rowid FROM documents_fts WHERE documents_fts MATCH ? ORDER BY rowid",
                (query["expression"],))]
            # Resolve source separately: an orphan posting must not disappear in an inner join.
            ledger.append({**query, "matched_ids": ids,
                           "current_source_for_matches": [by_id.get(i) for i in ids]})
        db.execute("CREATE VIRTUAL TABLE temp.terms USING fts5vocab(main, documents_fts, 'instance')")
        posting_ids = [r[0] for r in db.execute("SELECT DISTINCT doc FROM temp.terms ORDER BY doc")]
        tokens = [dict(r) for r in db.execute(
            "SELECT doc AS doc_id, term, col AS column_name, offset FROM temp.terms "
            "ORDER BY doc, col, offset")]
        schema = [dict(r) for r in db.execute(
            "SELECT type, name, sql FROM sqlite_schema WHERE sql IS NOT NULL ORDER BY name")]
        return {"source_rows": rows,
                "source_count": len(rows),
                "ordinary_fts_count": db.execute("SELECT count(*) FROM documents_fts").fetchone()[0],
                "ordinary_fts_rows": ordinary,
                "posting_doc_ids": posting_ids,
                "source_ids_missing_from_postings": sorted(set(by_id) - set(posting_ids)),
                "posting_ids_missing_from_source": sorted(set(posting_ids) - set(by_id)),
                "indexed_token_instances": tokens,
                "queries": ledger, "schema": schema,
                "fts_internal_check": integrity(db, False),
                "fts_source_check": integrity(db, True)}
    finally:
        db.close()


def main():
    require(len(sys.argv) == 2, "Supply exactly one NEW output directory")
    fixture, fixture_hash = load_fixture()
    out = Path(sys.argv[1])
    # Refuse existing files, directories and symlinks. Never overwrite prior evidence.
    out.mkdir(parents=False, exist_ok=False)
    original = out / "original-stale.sqlite"
    candidate = out / "candidate-rebuilt.sqlite"
    make_stale_original(original, fixture)
    original_hash = digest(original)
    before = inspect(original, fixture["queries"])
    require(before["source_rows"] == ordered(fixture["current_rows"]), "Fixture source mismatch")
    require(before["fts_internal_check"]["status"] == "pass", "Unexpected internal FTS error")
    require(before["fts_source_check"].get("sqlite_errorname") == "SQLITE_CORRUPT_VTAB",
            "The intentional stale index was not detected as an external-content mismatch")
    # Safe here because this script owns the closed, quiescent, DELETE-journal fixture.
    # This is not a recipe for copying a live application database or a WAL file alone.
    require(not any(Path(str(original) + suffix).exists() for suffix in ("-wal", "-shm", "-journal")),
            "Unexpected source sidecar")
    shutil.copyfile(original, candidate)
    candidate_before_hash = digest(candidate)
    require(candidate_before_hash == original_hash, "Candidate copy differs before rebuild")
    with sqlite3.connect(candidate) as db:
        db.execute("INSERT INTO documents_fts(documents_fts) VALUES ('rebuild')")
    db.close()
    candidate_hash = digest(candidate)
    after = inspect(candidate, fixture["queries"])
    require(after["source_rows"] == before["source_rows"], "Candidate changed source rows")
    require(after["schema"] == before["schema"], "Candidate changed schema or tokenizer")
    require(after["fts_internal_check"]["status"] == "pass" and
            after["fts_source_check"]["status"] == "pass", "Candidate checks did not pass")
    require(not after["source_ids_missing_from_postings"] and
            not after["posting_ids_missing_from_source"], "Candidate fixture coverage mismatch")
    require(digest(original) == original_hash, "Original bytes changed")
    require(digest(candidate) == candidate_hash, "Inspection changed candidate bytes")
    require(candidate_hash != original_hash, "Candidate bytes did not change")
    report = {"fixture_sha256": fixture_hash, "python_version": sys.version.split()[0],
              "sqlite_version": sqlite3.sqlite_version,
              "files": {p.name: {"bytes": p.stat().st_size, "sha256": digest(p)}
                        for p in (original, candidate)},
              "candidate_before_sha256": candidate_before_hash,
              "checks": {"original_bytes_preserved": True, "candidate_readback_preserved": True,
                         "source_rows_preserved": True, "schema_and_tokenizer_preserved": True},
              "before": before, "after": after}
    (out / "query-ledger.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                          encoding="utf-8")
    print(json.dumps({"status": "verified fictional candidate", "sqlite_version": sqlite3.sqlite_version,
                      "source_rows": after["source_count"], "queries": len(after["queries"])}))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, sqlite3.Error, RuntimeError) as exc:
        sys.exit(f"Rehearsal stopped: {exc}")
