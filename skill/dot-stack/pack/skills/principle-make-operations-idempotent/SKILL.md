---
name: principle-make-operations-idempotent
description: "Design and test commands or lifecycle operations for repeated requests, ambiguous outcomes, and interruption without duplicating effects or taking over unrelated state."
---

# Make operations idempotent

Use this for setup, jobs, lifecycle commands, migrations, and retryable mutations. Define the operation's identity and desired state before adding retries.

## Distinguish three properties

- **Idempotence:** applying the same logical operation again does not change its intended effect after the first success.
- **Retry safety:** repeating after an ambiguous response will not cause an unwanted duplicate effect.
- **Recoverability:** after a partial failure, a supported reconciliation, resume, or compensation can reach an acceptable state.

One does not imply all three. Writing the same file can be idempotent while sending the notification after it twice is not. A compensating action may recover a workflow without making the original operation idempotent.

## Design around observable state

Identify the logical operation key, owned resources, durable checkpoints, and externally visible effects. Reconcile actual state before repeating a mutation. Reuse an existing compatible resource only when identity and ownership match; do not adopt an unrelated process because a name looks familiar.

Use atomic writes, transactions, uniqueness constraints, or compare-and-swap where the invariant needs them. Persist deduplication evidence at the effect boundary, with defined retention and concurrent-duplicate behavior. A client-generated key is useful only if the receiver enforces its semantics. Treat unknown delivery as unknown until a receipt or authoritative read resolves it.

For locks, choose a primitive appropriate to the filesystem or distributed service. PID-only stale detection is insufficient across PID reuse, hosts, or namespaces. Bind ownership and freshness to a reliable identity or lease, and release only the lock actually owned. Cleanup requires evidence that the artifact is stale, owned, and safe to remove.

For recurring processing, refresh inputs after each cycle, preserve completed identities, and bound retries by a meaningful terminal condition or explicit task deadline. Idempotence does not justify endless retries or bypassing an authorization failure.

## Verification

Run the same operation twice; inject interruption before and after each meaningful durable/effect boundary; retry after an effect succeeded but its response was lost; and exercise concurrent duplicates. Assert final state and side-effect count, not just a success exit code.

Applies: a job with key `invoice-42` writes one record and produces one durable outbox entry despite duplicate delivery.

Does not apply: blindly repeating a payment or email after timeout without receiver deduplication or a delivery lookup. Stop that dependent action and resolve its status. Use isolated fixtures for failure injection; testing retry safety does not authorize live transactions.
