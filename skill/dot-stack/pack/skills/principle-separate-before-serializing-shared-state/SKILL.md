---
name: principle-separate-before-serializing-shared-state
description: "Prevent concurrent writers from corrupting shared state by separating independent ownership or enforcing the synchronization a real shared invariant requires."
---

# Separate before serializing shared state

Use this when workers, requests, processes, or tools might update the same file, key, branch, or mutable object. “Please do not overlap” is not concurrency control.

## Identify the real shared invariant

List each actor's reads, writes, resource identity, and lifetime. Include read-modify-write sequences: two workers updating different fields in one JSON file still compete for the same mutable object. Determine whether they publish independent facts or maintain one canonical value.

For independent facts, give each actor an owned file, key, branch, or state directory. Combine results at a read or integration boundary with one responsible integrator. Preserve identity and version so a stale result cannot overwrite a newer one. Separate workspaces reduce collisions but do not by themselves merge conflicting semantics.

When one shared invariant is real, enforce it using a suitable mechanism: a single-writer queue, transaction, compare-and-swap with versioning, atomic update, or lock with defined ownership and failure behavior. Select the mechanism for the actual storage system. A lock file created non-atomically is only another race; replacing a whole file atomically prevents partial bytes but may still lose concurrent updates.

Keep critical sections narrow and define behavior for contention, crash, retry, timeout, and stale ownership. Do not split state that must commit atomically just to avoid a lock. Sharding inventory counters without a cross-shard invariant can oversell even when every file has one writer.

## Example and counterexample

Applies: an indexer and metrics collector both rewrite `state.json`. Their checkpoints are independent, so place them in separately owned records and have the report read both. Exercise simultaneous updates and confirm neither checkpoint disappears.

Does not apply: two reservations consume the last available item. They require one atomic availability decision, not independent per-worker counters followed by eventual merging.

## Verification

Force overlapping reads and writes with barriers or a controlled scheduler rather than hoping timing produces a race. Assert no lost update, correct conflict handling, and restart recovery after the owner fails. A written ownership convention is useful coordination evidence but not a demonstrated locking guarantee. Report which mechanism enforces the invariant and any untested distributed behavior; do not claim concurrency safety from sequential tests alone.
