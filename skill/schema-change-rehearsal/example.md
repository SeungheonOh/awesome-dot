# Work estimates: text field to constrained relation

The requested change replaces `work_item.estimate_text` with a `work_estimate` row for each known estimate. `item_id` keeps the original text ID; `estimated_minutes` is a nonnegative integer; `original_text` preserves the exact historical source value. A missing estimate remains unknown through a left join. Archived items and their notes remain in scope.

All records, rules and decisions here were invented for this example. [source.sql](fixtures/source.sql) creates the original schema, two owners, five work items and five notes. [change-contract.json](fixtures/change-contract.json) is the complete semantic request. [expected.json](fixtures/expected.json) supplies independent per-item values and business controls; it is not generated from the conversion code.

## The decision that changes the answer

The initial [decision](fixtures/decision-pending.json) leaves `1d` unresolved. The generated [pending plan](outputs/plan-pending.json) identifies W-041 and prevents the entire schema transition. Other rows can be inspected, but they do not authorize partial transformation of this one schema change.

The supplied [resolution](fixtures/decision-resolved.json) says this queue uses seven work hours per day, so W-041 becomes 420 minutes. That is example-specific input, not an assumed workday. The [resolved plan](outputs/plan-resolved.json) retains source text, row identity, transformation and source/decision/contract digests.

| Work item | Original estimate | Final minutes | State that must survive |
| --- | --- | ---: | --- |
| W-001 | `1h 30m` | 90 | owner team-01 and both notes |
| W-002 | SQL NULL | SQL NULL through no estimate row | nullable owner and unknown estimate |
| W-010 | `0m` | 0 | known zero, distinct from unknown |
| W-041 | `1d` | 420 | explicit seven-hour decision and owner team-01 |
| W-900 | `2h` | 120 | archived timestamp, nullable owner, Unicode title and archived note |

The final active population contains four items: three known estimates totaling 510 minutes and one unknown estimate. The archived population contains one known estimate totaling 120 minutes. All five item IDs, five notes, two owners and both existing indexes survive. [Persisted rows](outputs/after.json) and [the final SQL export](outputs/after.sql) show the complete small result.

## Database identities and actual execution

The runner creates these separate temporary database files; none is an external or live database:

| Identity | Purpose | Relationship |
| --- | --- | --- |
| source.sqlite | Generated version-1 fixture in WAL mode | Original used only to create the supported snapshot |
| before.sqlite | Pre-change backup | Created with SQLite's backup API; thereafter opened read-only |
| failed.sqlite | Transaction failure test | Fresh backup of before.sqlite |
| migrated.sqlite | Successful version-2 candidate | Separate fresh backup of before.sqlite |
| later-writes.sqlite | Post-migration edit scenario | Backup of migrated.sqlite, then two scoped synthetic edits |
| restored.sqlite | Recovery destination | New file restored from before.sqlite through the backup API |

The source has committed content in its WAL when the backup is taken. No raw main-file copy is used. This demonstrates the supported backup mechanism on that generated source; it does not test concurrent writers or production snapshot coordination. All temporary files are removed when the runner exits; the saved SQL and JSON are complete inspectable evidence, not a production backup set.

The migration enables and verifies foreign keys, starts an explicit write transaction, rechecks the bound source, creates the estimate relation, backfills supported rows, removes the legacy column, checks invariants, marks version 2 and commits. Each connection is closed and reopened for persisted verification. The migration never disables foreign-key checks or deletes unrelated records.

## Observed failures and recovery

The injected failure is an accidental second insertion of W-001 after the backfill and `DROP COLUMN`. SQLite rejects the duplicate primary key. The helper explicitly rolls back; reopened schema, rows and version equal the original. The [failure artifact](outputs/failed-transaction.json) contains the actual statement trace and error. This verifies ordinary transaction failure behavior in the tested runtime, not abrupt-process or hardware-failure recovery.

The new database rejects an orphan estimate, negative minutes, fractional minutes and NULL provenance text. Probe savepoints leave the committed state unchanged. Both the old reader and old writer fail with `no such column: estimate_text`; old application code therefore cannot simply be rolled back against version 2. The new left-join reader preserves all items and reports the values above.

Recovery restores before.sqlite into a new restored.sqlite, reopens it, verifies the complete version-1 state and runs the old reader successfully. This is actual backup restoration, separate from the earlier transaction rollback.

To expose its limit, later-writes.sqlite changes W-041's title to `Batch preview v2` and its estimate to 600 minutes. The original migration provenance still says `1d`. Restoring the old snapshot returns `Batch preview` and legacy `1d` (420 minutes under the supplied rule), so both later edits are absent. The later-write branch remains intact for comparison. Copying historical provenance back into a legacy field would not preserve the new 600-minute estimate.

The result is suitable evidence for this isolated transition. It does not authorize a real cutover, establish a no-loss down migration, or prove mixed-version application compatibility. A real recovery would need to account for writes after the snapshot and deploy application code compatible with the recovered schema.

## Reproduce and inspect

From this folder, use a new destination whose parent exists:

```sh
python3 scripts/rehearse.py --output /tmp/schema-rehearsal-example
python3 scripts/verify.py
```

An existing output destination is rejected before creating the databases or writing artifacts. Retain previous output when trying another run. The original fixtures are hashed before and after execution; saved JSON is reopened and compared. The verifier also reloads each generated SQL export into a new disposable database and compares schema/rows with its JSON counterpart.

The SQL inspection exports turn off foreign-key enforcement only while loading into an empty disposable database, because dump table order may differ from relationship order. They then turn it back on and run checks. This is not the migration mechanism or the recovery method tested above; do not run an inspection export over an existing database.
