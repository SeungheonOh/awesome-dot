# Operations and connections

Read this when implementing the persistence seam, composing writes, keeping several reads coherent, or supporting competing actors. Keep the chosen rules in the application contract and code; do not introduce a cross-driver abstraction just for this reference.

## Own the file and the connection explicitly

Make create and open separate intentions. Creation should refuse an existing destination without overwriting it; use an appropriate no-overwrite/exclusive creation route if competing creators are possible. An existence check followed by an unrestricted create is not exclusive creation. If initialization fails, report that state without adopting an incomplete file as a valid app or deleting a pre-existing file.

Opening should select the intended existing file and check that it belongs to a supported application schema before ordinary work. Missing, unrelated, incomplete, and newer files need distinct useful diagnostics. Do not turn a misspelled path into a successful empty application. Do not run unconditional initialization SQL during normal reads. For Python, URI `mode=rw` opens without creating and `mode=ro` opens read-only; construct the URI with correct path escaping. [Python SQLite URI modes](https://docs.python.org/3.12/library/sqlite3.html#how-to-work-with-sqlite-uris)

Decide whether the caller supplies a connection or the application owns its lifetime. For an app-owned connection, close it on success and failure. For a caller-owned connection, say who starts/finishes transactions and do not close it unexpectedly. Return materialized results for a small bounded read, or expose the lifetime and closure obligation of a streaming result. A cursor must not outlive the connection it needs.

Apply connection-local enforcement consistently at connection creation. Keep that initialization separate from schema creation and migrations. If a required setting does not read back as expected, stop the operation instead of proceeding under weaker rules.

## Choose one transaction control model

For Python 3.12+, choose `autocommit` explicitly. With `True`, use SQL `BEGIN`/`COMMIT`/`ROLLBACK`; connection `commit()` and `rollback()` do nothing. With `False`, the driver maintains a transaction: initialize foreign keys before entering that mode, then use driver commit/rollback without an extra `BEGIN`. Legacy `isolation_level` behavior is a separate model; preserve it deliberately where supported. The connection context manager neither opens a transaction nor closes the connection, and does nothing with `autocommit=True`. Check `executescript()` for implicit commit behavior in the chosen mode. [Python transaction control](https://docs.python.org/3.12/library/sqlite3.html#transaction-control), [connection context manager](https://docs.python.org/3.12/library/sqlite3.html#how-to-use-the-connection-context-manager)

For another established driver or ORM, determine the equivalent rules from its supported API: automatic begin, commit behavior, nested scope, connection checkout initialization, and resource release. Do not transplant Python syntax into a different driver's ownership model.

For explicit-SQL control with no transaction already active, one operation-owned flow is shown below as pseudocode. Adapt transaction entry/exit to a driver-managed model instead of adding a second owner.

```text
open existing file
try:
    initialize and verify connection settings
    begin the selected transaction
    read state needed to decide the operation
    validate current-state preconditions
    apply all related changes using helpers that do not commit
    form the result and check required postconditions
    commit successfully
    return the committed outcome
on failure:
    if a transaction remains active, roll it back
    propagate a useful failure, retaining rollback trouble if any
finally:
    close the app-owned connection
```

Keep validation that needs no database outside a short write transaction. Recheck state-dependent conditions inside the boundary that protects them. A helper may receive a transaction-bound connection and perform statements; it must not quietly commit because it also happens to serve a standalone command. Wrap that helper with an outer operation for standalone use. This allows an importer to own a whole batch without each imported row becoming an early commit.

SQLite `BEGIN` transactions do not nest. A savepoint can provide a deliberate inner rollback scope; releasing it inside an outer transaction is not a durable commit. A failed statement can leave earlier changes and the transaction intact. Implement the promised operation rollback rather than assuming the last exception undid everything. [SQLite transactions](https://www.sqlite.org/lang_transaction.html), [savepoints](https://www.sqlite.org/lang_savepoint.html)

Do not report success before commit succeeds. If cleanup itself fails, preserve the original operation error and the cleanup failure, then discard the uncertain connection. Keep database commit separate from later file output or messages: failure to print a result cannot undo an already committed operation. If uncertain completion matters to the user, provide a resolvable operation identity or a documented readback route; a universal durable receipt table is not required.

## Make conflicts express the operation

Bind data values. Select dynamic identifiers only from established schema choices. Decode and validate user values before persistence, while retaining database constraints for writers that reach that boundary.

Choose statements by intended outcome. `INSERT OR REPLACE` can delete a conflicting record; `OR IGNORE` can silently skip a violating row. Neither means “update this entity without changing its identity” or “reject this entire batch.” [SQLite conflict behavior](https://www.sqlite.org/lang_conflict.html)

An UPSERT needs the intended uniqueness key, update fields, and any state condition. It does not choose which source is authoritative or resolve ambiguous identities. Check the runtime syntax you actually use; SQLite added UPSERT in 3.24.0 and generalized parts of its syntax in 3.35.0. [SQLite UPSERT](https://www.sqlite.org/lang_upsert.html)

Translate expected failures at the public boundary: malformed input, missing record, stale revision, duplicate identity, or busy resource as relevant. Use stable outcomes rather than requiring callers to parse a driver's human-readable error. Do not swallow unexpected storage failures into an empty result or a fabricated no-op.

## Keep dependent reads coherent when required

A list and its totals, or records and import provenance, may need to describe the same state. One SQL statement often suffices. Otherwise use one read transaction, fetch the agreed population, and finish it promptly. In SQLite, the snapshot is established by the transaction's database read, not by the wall-clock instant a deferred `BEGIN` is issued; subsequent reads in that transaction do not see another connection's later commits. [SQLite read transactions](https://www.sqlite.org/lang_transaction.html#read_transactions_versus_write_transactions)

Do not promise a coherent snapshot for unrelated queries on newly opened connections. Conversely, if independent current observations are acceptable, document that meaning instead of keeping a transaction open across a slow interactive session. Test coherence with a controlled intervening writer only when that guarantee is part of the application.

## Support competing writers only when needed

SQLite serializes writers. `BEGIN IMMEDIATE` acquires write intent before state-dependent reads and can fail busy; a deferred read transaction can fail when upgraded to a write. Select acquisition and timeout behavior for the operation. [SQLite transaction modes](https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions)

For a local edit form or another actor using stale state, choose whether the edit replaces current values intentionally or must reject a changed revision. Serialization alone does not make an old user's assumptions current. Put the comparison and change in one protected operation.

Retry only from a known state, with a bounded attempt/time budget and a safe unit. After rollback, a complete retry must reread current state and reevaluate preconditions; blindly replaying only the failed statement can combine old decisions with new data. Distinguish contention before any effect from an uncertain committed outcome. Retrying must obey the operation's repetition policy.

WAL can let readers and a writer proceed concurrently, but does not create multiple simultaneous writers. Choose it for a workload reason and account for its files and checkpoint lifetime; do not enable it as an automatic performance fix. [SQLite WAL](https://www.sqlite.org/wal.html)

Verify the contention or stale-edit rule with the actual supported actors and a controlled overlap, then inspect reopened state. A sequential test or a timeout setting establishes neither absence of lost updates nor every possible interleaving.
