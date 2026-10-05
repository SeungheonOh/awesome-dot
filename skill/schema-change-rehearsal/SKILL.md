---
name: schema-change-rehearsal
description: "Execute a requested database schema or data-representation change on an isolated copy, reconcile identities and business invariants, test failure recovery, and establish application compatibility before a rollout decision."
---

# Rehearse a schema change and prove what survives

Turn one explicit schema change into a working, inspected migration and an evidence packet from a real isolated rehearsal. Produce the changed schema and rows, the observed failure behavior, an exercised recovery path, and a clear statement about which application versions can use each state.

Use this for splitting a table, replacing a field representation, adding a constraint with a defined backfill, or another bounded schema transition. An import into an unchanged service, a read-only reporting discrepancy, or collecting existing release evidence does not require this workflow. A successful rehearsal is evidence for a rollout decision, not an automatic production migration.

## Establish the input contract

Inspect the supplied database, schema, migration request and existing authorized documentation before asking for missing facts. Identify:

- The source snapshot and its scope: database/tenant, engine and runtime version, schema version, creation method, completeness, and any omitted tables or rows
- The exact requested before/after schema and representation, including units, null/empty/zero meanings, duplicate policy, defaults, identity and relationship rules, archived/deleted population, and treatment of unconvertible rows
- Dependent indexes, constraints, views, triggers, generated fields, migration history, and application readers/writers, including code that uses column order or `SELECT *`
- Business invariants and independent controls: required keys, cardinalities, unchanged fields, qualifying populations, known/unknown counts and relevant totals; a total alone will not detect swapped identities
- The isolated writable destination, allowed changes, immutable source evidence, and intended deliverables
- Recovery requirements: accepted data loss, retained backups/journals, supported restore method, application versions, and handling of writes accepted after the snapshot

Bind the plan to source and migration identities. Record content hashes for immutable input files and a reproducible logical snapshot of schema, ordered keys and values. For a live source, a hash of the main database file alone does not identify the committed state in its journal. Keep credentials and unrelated data out of the packet.

Resolve only meanings that change the transformation. For example, `1d` might mean a calendar day or a queue-specific number of work hours; never silently choose eight hours. Keep a visible row-level hold until authoritative semantics are supplied. Distinguish a field with no value from a known zero. Do not drop archived rows to satisfy a new constraint. If the requested conversion cannot represent a value, preserve it in the source evidence and stop that dependent transformation rather than substituting a convenient default.

## Make a supported isolated copy

Use the database engine's supported consistent backup/export facility with the existing authorized access. Identify the original, pre-change backup, candidate, failure-test copy and recovery destination separately. Reopen the backup and validate its contents before treating it as a recovery asset. An export with missing relationships or filtered history is not a full recovery backup.

For SQLite, use its backup API through `sqlite3.Connection.backup()` or another documented method appropriate to the source. An open WAL database's committed state can span the main file and WAL; do not raw-copy just the main file. The worked helper actually backs up a generated source while committed WAL content exists, then tests all migrations on separate copies. It does not test concurrent writers. [SQLite backup documentation](https://www.sqlite.org/backup.html), [WAL file behavior](https://www.sqlite.org/wal.html#the_wal_file), [Python backup interface](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup)

A user request to perform this bounded local rehearsal authorizes creating and changing the isolated copies. Proceed through execution and readback without another approval merely because the plan is ready. Do not broaden it to production, alter security settings, install a database, or overwrite the only source. Honor applicable approval requirements for destructive or unrecoverable operations and new access. If a live migration is separately requested and authorized, evaluate its actual engine, operational controls and scope; this fixture is not an execution route for it.

## Design the forward transition

Write an inspectable migration with explicit preconditions and postconditions. Preserve original IDs and significant values. Bind data values as parameters; select identifiers from the reviewed schema. Keep the source-to-target mapping and any rejected or unresolved rows. When provenance text is retained, say whether it is historical evidence or a current application field.

Inspect dependent schema objects before choosing an engine-supported alteration. Avoid blanket deletion, reset-to-empty, silent row filtering, disabled validation, or a table rewrite that forgets indexes/triggers. If a change needs a documented table-rebuild sequence, follow that engine/version's sequence and explicitly account for every affected dependency. A narrower supported alteration may be sufficient. SQLite's `DROP COLUMN` can fail when the column appears in a view, index, trigger or constraint; do not bypass that check. [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html)

Establish transaction behavior for the engine and driver actually used. Do not infer that all DDL is transactional across databases. In this SQLite example, Python 3.12+'s explicit `autocommit=True` mode is paired with SQL `BEGIN IMMEDIATE`, `COMMIT` and `ROLLBACK`; `Connection.commit()` and `rollback()` would have no effect in that mode. Recheck the bound source after acquiring the write transaction. Do not put a driver method with implicit transaction effects in the middle of the migration. [Python transaction control](https://docs.python.org/3/library/sqlite3.html#transaction-control)

Enable and read back SQLite foreign-key enforcement on each relevant connection before beginning a transaction. Changing it inside a transaction has no effect. Check relationships explicitly after transformation; `integrity_check` does not include foreign-key checks. For other engines, establish the equivalent documented controls. [SQLite foreign-key enforcement](https://www.sqlite.org/foreignkeys.html#fk_enable), [integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check)

## When old and new callers must coexist

Use a staged transition when the accepted task requires continued writes or overlapping application versions. If the controlled callers can move together, a simpler one-step transition may suffice. For each required intermediate state, establish which representations govern reads, which callers may write, and which values are permitted. Adding a column or completing a backfill does not by itself change that authority.

Keep conversion work distinct from an ordinary accepted edit. A captured value can become stale before a backfill write, and an already converted row can receive a later edit. Choose an engine-appropriate synchronization or conditional-write mechanism that preserves newer committed values and the caller compatibility contract. Re-reading current authoritative values, detecting a changed revision, or maintaining representations together may be suitable; no particular trigger, marker or dual-write design is mandatory.

Exercise a consequential interleaving through the actual callers: capture conversion work, accept a relevant edit, then attempt that delayed work. Check both readers and persisted values. Also check an accepted edit after conversion, and newly created records when those are allowed. Visiting every initial row is not enough to demonstrate catch-up with a changing population. Repeated or resumed conversion must preserve accepted edits and avoid duplicate relationships or accidental reactivation of a retired path.

Make the switch or retirement condition explicit. Reconcile current values and outstanding work before claiming the phase is ready, and use the authority specified by the task to change the supported reader/writer contract. Verify the actual old write entry point's intended compatibility or refusal after reopening the saved state. A recorded phase label alone does not enforce that behavior.

Reassess rollback at each boundary. Data may remain representable for old code during overlap while a later new-only value closes that option. Restoring archived application code can also bypass a newly required retirement rule. State those limits separately from snapshot recovery, and preserve later-write evidence. Local controlled interleavings do not establish production concurrency, deployment coordination or zero downtime.

## Execute, reconcile, and challenge the result

Run the migration only on its intended copy. Save the exact statements/code and parameters, source/decision identities, relevant errors, runtime versions and resulting migration version. If the version or source state differs from the plan, stop and replan; do not force a replay or erase intervening changes.

Verify before commit where supported, then close and reopen the saved result and verify again:

- Every original entity ID and its unchanged values, nullable links and archived state survive
- Each transformed row has the intended destination identity, value, units and provenance; unknown and zero still differ
- Relationship keys resolve, declared cardinalities hold, and unrelated tables and schema objects survive
- Per-record controls and business totals match the supplied semantics; unknown values remain visible instead of disappearing into a sum
- The schema/version marker and data persisted, and the new reader returns the correct population
- Representative old reads and writes either work under a stated compatibility contract or fail in the documented way

Exercise new constraints using ordinary invalid values on a disposable copy or savepoint. Confirm actual rejection and verify that the probe left no committed change. A declaration in a schema dump is weaker evidence than an observed constraint failure.

For a transactional migration, inject a bounded ordinary correctness failure after meaningful DDL/backfill work and before commit. Observe whether a statement failure leaves the transaction active, issue the supported rollback, and reopen the copy. Compare the entire relevant schema and rows with its pre-change state. Do not claim crash recovery, disk-full resilience, lock behavior or production atomicity from this test. SQLite distinguishes statement failure from transaction rollback; handle and inspect the actual transaction state. [SQLite transaction errors](https://www.sqlite.org/lang_transaction.html#response_to_errors_within_a_transaction)

Preserve failed evidence. When an expected test exposes a migration defect, correct the implementation and rehearse from a fresh supported copy. Do not patch the evidence or reuse a partially changed database as if it were the original baseline. Existing output directories must not be silently replaced.

## Prove recovery separately from compatibility

Keep these claims separate:

| Claim | Required evidence |
| --- | --- |
| Failed transaction rolled back | A failure before commit followed by reopened schema/data equality with its pre-transaction state |
| Data backup can be restored | The retained snapshot is restored through a supported mechanism into a distinct destination; restored schema, rows, relationships and intended reader are checked |
| Old application can run | Its actual relevant reads/writes work against the resulting schema and representation; a running process or successful restore command is insufficient |
| Committed change can be reversed without loss | The reverse transformation can represent current values, accounts for subsequent writes, and is exercised with the required application compatibility |

Do not call a migration reversible just because a down script exists or because the original text was saved. Later writes can invalidate that text as a current value; new entities or constraints may have no valid old representation. A restored snapshot ordinarily returns to its own point in time, not the latest state. Preserve the changed branch, show which later writes are absent, and state the reconciliation or data-loss decision needed before a real cutover. Restoring files and rolling back application code are separate operations.

Use a new destination for the rehearsal restore so it cannot destroy the candidate or later-write evidence. Verify the actual recovered behavior before recommending recovery. If a required recovery mechanism cannot be exercised, label it unverified and identify the missing prerequisite. Do not replace that gap with a paper-only success claim.

## Deliver the result

Return the requested migration and mapping, immutable input/decision identities, actual before/after schema and relevant rows, preserved-identity and business reconciliation, constraint/failure evidence, recovery readback and compatibility result. Explain remaining blockers and untested operational conditions. A compact report can link the machine-readable artifacts; avoid an unreviewable dump of unrelated data.

Complete authorized artifact delivery and readback. Keep the readiness conclusion scoped: successful transformation and snapshot recovery in a copy may still require application changes, later-write reconciliation, load testing, or a separately authorized production rollout.

## Worked example and reproduction

[The original example](example.md) moves fictional work estimates from a text column into a constrained child table. Read its [input contract](fixtures/change-contract.json), [source SQL](fixtures/source.sql), and the pending/resolved decision files before running the helper. The supplied resolution is part of the fictional input, so the example requires no additional user decision.

The helper accepts only a new output directory and always generates this fixture; it cannot open a user-selected database or connect to a service. It uses existing Python 3.12+ with SQLite 3.35+ and the standard library, creates temporary databases, and saves text evidence. No installation or database binary is needed.

From this skill folder, choose a destination that does not already exist:

```sh
python3 scripts/rehearse.py --output /tmp/schema-rehearsal-example
python3 scripts/verify.py
```

Inspect [the actual saved result](outputs/result.json), [final schema and rows](outputs/after.sql), [transaction failure](outputs/failed-transaction.json), and [recovery readback](outputs/restored.json). [Verification notes](verification.md) describe the performed checks and limits. The helper is an example-specific implementation; adapt and review it for another schema rather than passing real data to it unchanged.
