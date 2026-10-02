# Verification record

Checked on 2026-10-02 with Python 3.12.14 and SQLite 3.53.1. Only the original fictional fixture and separate disposable SQLite files were used. All dependencies came from the existing Python standard library; no installs or external database connections were involved.

## Executed result

`python3 scripts/rehearse.py --output outputs` generated the included [result](outputs/result.json), [final rows/schema](outputs/after.json), [SQL export](outputs/after.sql), plans, failure trace and recovery evidence. The source WAL contained 90,672 bytes when the SQLite backup API created the baseline snapshot. Physical file sizes and runtime version strings may differ in another environment.

The committed result contains five items, four estimate rows, five notes and two owners. Unknown W-002 remains unknown; W-010 remains a known zero; archived W-900 retains its timestamp, title and note. Known active work totals 510 minutes; archived work totals 120 minutes. Per-ID values and complete unchanged rows were checked, not just aggregate totals.

The ambiguity test left version 1 untouched. The injected duplicate occurred after the legacy column was removed; SQLite emitted `UNIQUE constraint failed: work_estimate.item_id`. The recorded trace ends in an explicit rollback. After closing and reopening the copy, its full logical state matched the baseline. Recovery through `Connection.backup` into another new file produced the same baseline state and a successful old-reader result.

| State | SHA-256 of canonical schema/version/ordered-row JSON |
| --- | --- |
| Original, failed transaction after rollback, restored snapshot | `bed02bb7f789bb1c4b436e171d7a91fddbb00659dd073539d9c9f5f8ec235abe` |
| Successful version 2 | `862b8211c9c3ec789bffd4a786a8eb4bdac22ded156baed816dff14667d8e1c5` |
| Version 2 with later title/estimate edits | `67dde18748b6dfb22c26d9f29d6e2cc533e93d402062fc0da758bcae0d75b6e1` |

These are logical content identities, not database-file hashes. [The result](outputs/result.json) also contains exact hashes for every original fixture file. No database binaries are distributed; the databases are regenerated locally and the final/recovered schema and data are preserved as text.

## Behavioral checks

`python3 scripts/verify.py` passed these observed checks:

- Complete rehearsal and persisted readback, including constraint enforcement, old-code failure and separate snapshot recovery
- Existing output destination rejected with every prior artifact's hash preserved
- Empty, whitespace-altered, fractional, unsupported, negative, non-ASCII-number and overflowing estimate text blocked before mutation
- Decision scoped to the named change and an explicit positive integer workday conversion within the storage range
- Stale plan rejected after a source edit, without erasing the newer source value
- A dependent view prevented column removal; the full transaction rolled back, preserving that view, schema and data
- Already-applied migration rejected without repeated backfill
- Both saved SQL exports loaded into new disposable databases and matched their saved JSON schema/rows; foreign-key and integrity checks passed
- Every original fixture file retained its exact bytes

The dependency probe returned `error in view legacy_estimates after drop column: no such column: estimate_text`. The normal fixture has no such view; this added dependency is confined to its own test copy. The helper relies on SQLite's refusal for this extra case rather than pretending to rewrite arbitrary dependent application objects.

The standard skill frontmatter/name validator also passed. Relative document links were checked against the delivered files. The Python sources and fixture SQL were read before execution.

## Interpretation and limits

Old readers and writers fail against version 2 because the old column is absent. Restoring the pre-change backup makes the old reader work again; a complete application or restored old-writer integration test was not performed. The new reader was exercised, along with two ordinary new-schema writes in the later-write scenario.

The restored snapshot omits the later title and 600-minute estimate. Historical `original_text = '1d'` would recover only the original 420-minute meaning. No down migration or lossless rollback after later writes is claimed. The candidate and later-write branch remain separate during recovery.

This is a small local correctness and recovery rehearsal. It does not establish production performance, lock contention, concurrent-writer snapshot coordination, abrupt-process recovery, disk-full behavior, a mixed-version deployment, another database engine's DDL semantics, or production cutover authorization. The saved inspection SQL is not the exercised backup mechanism.

## Independent readback

A separate review inspected the source, repeated the full rehearsal and behavioral verifier in an isolated copy, and reproduced all ten saved evidence artifacts byte-for-byte in the recorded runtime. Additional disposable probes confirmed the active transaction after a statement failure, explicit SQL rollback after the driver method had no effect, null/duplicate/relationship constraint rejection, and scoped old-writer behavior on a restored version-1 copy. A plan that swapped per-ID estimates while preserving their aggregate total was rejected and rolled back. These are SQL-level checks, not full application integration.

A fresh guide-only case used an integer-millisecond target and an archived half-millisecond value. It held the transition for one representation decision, then applied the supplied ties-to-even rounding rule while retaining the archived row, historical values and the distinction between unknown and rounded zero. Its mapping reconciled the half-millisecond total difference. That case reviewed the procedure and expected mapping; no second migration was executed.

## Documentation checked

Current official documentation was inspected on the verification date for the specific decisions used here:

- [Python SQLite backup API](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup) and [transaction control](https://docs.python.org/3/library/sqlite3.html#transaction-control): supported copying, explicit autocommit mode, and transaction-method behavior
- [SQLite backup API](https://www.sqlite.org/backup.html) and [WAL files](https://www.sqlite.org/wal.html#the_wal_file): snapshot mechanism and why main-file copying is insufficient for an open WAL database
- [SQLite transaction error behavior](https://www.sqlite.org/lang_transaction.html#response_to_errors_within_a_transaction): statement failure versus whole-transaction rollback
- [SQLite foreign-key enforcement](https://www.sqlite.org/foreignkeys.html#fk_enable) and [integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check): connection-local enforcement, transaction timing, and separate relationship validation
- [SQLite column removal](https://www.sqlite.org/lang_altertable.html#alter_table_drop_column): dependency restrictions and rewriting behavior

The official documentation supplies engine/driver semantics. The saved outputs supply the evidence that this particular implementation actually exercised them.
