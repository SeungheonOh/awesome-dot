# Saved-file evolution and delivery

Read the relevant sections when changing an existing database, promising recovery, distributing a portable app, or investigating a required slow path. Keep unrelated branches out of a small task.

## Open saved files without disguising a change

Define which file versions the application can read and write. A lightweight version marker such as `PRAGMA user_version` is available to the application; SQLite does not implement migration policy from it. Check the schema properties needed to recognize the app and reject unrelated or incomplete files. A familiar integer alone is insufficient evidence of the expected schema. [SQLite application version marker](https://www.sqlite.org/pragma.html#pragma_user_version)

Make ordinary startup behavior explicit for a current file, an older supported file needing upgrade, an unsupported future file, and an unexpected file. An explicit upgrade command is often clearest. If the established app already upgrades on opening, preserve that contract only with its defined recovery and failure behavior; a normal read must not accidentally trigger a destructive reset. Keep application version, schema version, and SQLite runtime version distinct.

Creation initializes a new file. Opening validates an existing file. Migration transforms a recognized older state. Do not use repeated `CREATE TABLE IF NOT EXISTS` or an unconditional version assignment as a substitute for those distinctions.

## Preserve a usable baseline before transformation

Identify the original app, its saved database state, the requested transformation, and the old callers/outputs that constrain it. For a small supplied app, inspect the complete relevant schema and records, including lifecycle-hidden data and dependent views, indexes, and triggers. Establish per-identity preservation expectations independently of the conversion code. A count or total can remain unchanged while values move to the wrong identities.

Use a supported SQLite backup into a separate, non-overwriting destination. The backup API produces a consistent database snapshot when completed; concurrent activity can affect its progress, so an incomplete or timed-out backup is not ready for use. [SQLite backup API](https://www.sqlite.org/backup.html)

Keep the original, pre-change backup, candidate, failure-test copy, and restore destination distinguishable when those roles are needed. They need not be a universal directory layout. Reopen the backup, inspect expected schema/records/version, and use the appropriate consumer before treating it as a recovery asset.

An open WAL database may hold committed state in its WAL. Copying the main file alone or removing sidecar files can lose that state. Use the supported database-copy route; do not invent an ad hoc file-copy recipe. [SQLite WAL file lifecycle](https://www.sqlite.org/wal.html#the_wal_file)

Bind evidence to a stable snapshot. A main-file hash taken while a live database changes is not a complete identity for committed state. Once a supported snapshot is finalized, its file identity and a reproducible logical inventory can support different checks. Neither authenticates an untrusted source by itself.

## Choose the smallest supported transition

Resolve source meaning, target representation, unconvertible values, preservation obligations, and version preconditions before applying the change. Prefer a coordinated one-step update when all relevant callers can move together. A migration framework or overlap protocol needs an actual lifecycle requirement.

Check the precise DDL operation against the consumer runtimes and dependencies. SQLite 3.53.0 added setting/dropping column `NOT NULL` constraints; therefore “SQLite always needs a table rebuild for that change” is too broad. Older supported consumers or other transformations may need a rebuild. Use the documented route for the required feature and version rather than imposing the author's newest runtime. [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html)

For a rebuild, follow the documented generalized procedure, inventory dependent schema objects, copy with explicit columns and reviewed conversions, recreate required objects, and validate before acceptance. Do not rewrite `sqlite_schema` to suppress a migration error. If the documented procedure needs temporarily changed foreign-key enforcement, arrange it outside the transaction, scope it to migration connections, and restore/read back the application setting afterward; do not copy that exception into ordinary writes. [SQLite generalized alterations](https://www.sqlite.org/lang_altertable.html#making_other_kinds_of_table_schema_changes)

Use the same deliberate driver transaction model as the application. Acquire the required boundary, then recheck source/version conditions against current state. Keep the transformation and its version update in the same transaction where supported. Fail rather than silently skipping rows that cannot satisfy the new representation. No helper may commit a partially migrated state behind the outer owner.

Check data and relationships separately. `PRAGMA integrity_check` does not check foreign keys; inspect `PRAGMA foreign_key_check` as well when relevant. Neither proves domain meanings, query populations, or consumer compatibility. [SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check)

For a consequential transformation, rehearse on a separate candidate and challenge an ordinary failure after meaningful work but before commit. Roll back through the supported mechanism, then reopen and compare the whole relevant logical state to the baseline. Separately run the successful migration, reopen the candidate, and call the new application's actual operations. Check the documented behavior of a repeated migration and unsupported file versions without resetting them.

## Keep compatibility and recovery claims separate

Compatibility belongs to actual callers and representations. A maintained legacy command can keep its old public fields while using a new schema internally. This does not establish that an untouched archived executable still works against the new database. Test each promise actually required, including updates that must preserve newly introduced facts an older format cannot express.

If old and new writers really must overlap, define authority at each phase: permitted writes, authoritative representation, conversion guard, switch condition, and retirement behavior. Delayed conversion must not overwrite an accepted newer edit, and catch-up must account for newly created or later-edited records. Exercise the consequential order with the real callers. Use a focused schema-transition workflow when this becomes substantial; do not impose coexistence on an offline local update.

Restore a retained backup into another destination and run the intended historical consumer there. This establishes recovery to that snapshot, not lossless reversal of the current app. Preserve a later accepted edit separately and account for its absence from the restored state when that limit matters. Old provenance is historical evidence; copying it back is not necessarily a correct reverse transformation of current values.

A useful maintenance result distinguishes:

- Failure before commit rolled back to its baseline
- The migrated candidate retains required identities and meanings and supports the new caller
- A restored historical snapshot supports its intended caller
- Any promised reverse transition preserves later writes, or remains unverified/unsupported

These are separate observations. A down script, backup file, or successful startup cannot establish all of them.

## Verify the delivered consumer

For a local script or library, document the actual invocation and database path behavior. From another working directory, open the selected saved file, perform the useful read, and exercise a permitted ordinary write on a separate copy if needed to keep the delivered file clean. Check loading of any schema, query, template, or migration resources that the app needs at runtime. Do not introduce an installer when direct execution is the intended delivery.

For a distribution, identify the exact package the user will receive and exercise its public entry point outside the source checkout in a suitable authorized consumer environment. Inspect required resources in that received artifact and establish their runtime origin. A successful source import or `--help` does not show that the installed app can open the saved database or perform the task. Follow the established package verification method; publication is a separate action from making and checking an artifact.

Read back promised export files and retained databases after the final relevant edits. Keep runnable sources, input/candidate identities, useful output, exact checks, and meaningful limitations together in the handoff. For a tiny app, usage and a compact verification section in the README can hold this evidence. Avoid manufacturing additional reports with no consumer.

## Measure performance only for a real question

First fix population, grain, ordering, and null interpretation. Identify the required query or operation, representative data volume and distribution, relevant indexes, runtime, and a bounded measurement method. Use `EXPLAIN QUERY PLAN` to inspect access strategy; its format is not a stable application API and it is not elapsed-time evidence. [SQLite query plans](https://www.sqlite.org/eqp.html)

Compare the same useful output before and after an index or query change. Include enough independent per-identity checks to reject a faster query that drops, duplicates, or misattributes facts. Measure the actual operation being claimed, including materialization or rendering when those are part of the user's latency. State cache/warmup and scope limits; a tiny synthetic improvement is not production throughput. Do not weaken durability or change the data contract merely to produce a speedup.
