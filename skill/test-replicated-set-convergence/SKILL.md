---
name: test-replicated-set-convergence
description: "Test an observed-remove replicated set using algebraic merge laws, concurrent-update examples and reordered snapshot delivery, while separating visible agreement from internal convergence and eventual-delivery assumptions."
---

# Test replicated-set convergence

## When to use

Use this when reviewing a replicated set implementation, building a local synchronization experiment or adding regression tests for add/remove conflicts. The deliverable is a reproducible test corpus with explicit semantics and delivery assumptions, not a claim that a complete distributed system is production-ready.

This workflow covers a simple state-based observed-remove set with retained add records and removal tags. An optimized design without tombstones, operation-based delivery, counters, maps or text editing needs its own invariants. Do not silently apply this representation to a different data type.

## Required inputs

- The membership semantics, especially the intended concurrent add/remove outcome
- Replica identities, tag-generation rules and identity lifetime
- State representation, merge operation and equality definition
- Delivery model: snapshots or operations, duplication, loss, ordering and eventual delivery
- Persistence, restart and metadata-compaction behavior, if implemented
- Authorized test scope and practical action/state limits

If the implementation does not specify what should win during a concurrent add and remove, settle that before writing a test that assumes an answer.

## Workflow

### 1. Write down what membership means

For the simple retained-record representation, an add creates a unique tag associated with an item. A remove records every live tag for that item observed by its source replica. Membership means at least one add tag for the item is not removed.

Merge unions add records and removal tags. This makes an unseen concurrent add survive a remove, while an already-observed and removed tag stays removed when an old snapshot arrives later. This is the add-wins interpretation of concurrency, not a wall-clock comparison.

See [Shapiro et al., A comprehensive study of Convergent and Commutative Replicated Data Types](https://www.lip6.fr/Marc.Shapiro/papers/Comprehensive-CRDTs-RR7506-2011-01.pdf) for the observed-remove set and convergence background. Retain the distinction between its specific representations and the implementation being tested.

### 2. Make tag uniqueness an explicit precondition

A replica identifier plus a monotonic counter is sufficient only within its stated identity lifetime. Resetting a counter while old messages remain reachable can reuse a tag. Production restart behavior needs persistent counters, a new replica incarnation or another appropriate uniqueness mechanism.

Reject a merge if the same tag names different items instead of choosing one by arrival order. A simulator that restarts the entire scenario can reset counters only because it also discards every old state and packet. Do not generalize that reset into a safe distributed restart.

### 3. Test merge algebra on reachable states

Generate states through real add/remove/merge operations, then verify:

- Idempotence: merging a state with itself changes nothing
- Commutativity: merging A with B equals merging B with A
- Associativity: merging A with the merge of B and C equals merging the merge of A and B with C

Compare complete normalized state, not only the visible set. Different retained tags can currently display the same items yet respond differently to a later remove. Normalize ordering for comparison without throwing away meaningful metadata.

Also compare membership with a separate reference calculation: union all known add records, union all removal tags, discard removed tags, then deduplicate their associated items. Keep the oracle structurally distinct from the production membership helper.

### 4. Exercise delivery rather than only calling merge

Capture immutable snapshots at send time. Change the source after enqueueing a message and confirm that the queued snapshot does not change. Deliver snapshots in several orders, duplicate them and deliver older messages after newer ones.

For convergence assertions, ensure every participating replica eventually receives the relevant updates, possibly through a later full-state exchange. A dropped packet with no replacement violates that premise. The expected result in that case can be continued divergence, rather than a failed merge algorithm.

Test the actual queue controls too: duplicate creates an independent packet identity carrying the same snapshot, drop affects only that packet, and delivery applies to its recorded destination. Do not mistake a simulator's direct union of all states for a deployable anti-entropy protocol.

### 5. Cover the semantic counterexamples

Include these small histories before generating larger ones:

- Add, synchronize, remove, synchronize: the item disappears
- Remove a known tag while another replica independently re-adds the same item: the new tag survives
- Deliver a removed tag's old add snapshot after the removal: it does not resurrect
- Add the same item several times locally, then remove it: all observed live tags are removed
- Show matching visible sets with different internal records, then synchronize and compare full state

For retained tombstones, do not discard metadata merely because every currently visible replica agrees. Safe compaction depends on stronger knowledge about delayed messages, replica membership and causal stability; test it separately if supported.

### 6. Preserve a replayable failure

Save the initial model/version and the ordered commands with their packet identities. Reconstruct through the same validated commands, rather than trusting arbitrary imported internal state. Bound replay size and reject malformed commands atomically.

On failure, retain the seed and smallest useful command sequence. State which invariant failed and whether its delivery preconditions held. When an interface is involved, test stale file-read completion, undo-by-replay, text-only item rendering and focus after a packet is removed.

## Worked example

A adds Mango with tag A:1 and shares it with B. During a partition, A removes Mango, recording A:1 as removed. B independently adds Mango again with tag B:1.

After exchanging their snapshots, both know A:1 and B:1, and both have removal tag A:1. Mango remains because B:1 survives. This is the requested concurrent-add behavior, not a lost removal.

After seeing both tags, B removes Mango and synchronizes again. Mango disappears. Delivering the original A:1-only snapshot afterwards must leave it absent: the removal record is still retained.

## Verification record and limits

A three-replica local implementation exercised this workflow with 300 generated histories checking the merge laws and an independent union-minus-removals membership calculation. Another 100 shuffled delivery schedules included duplicated frozen snapshots and converged after complete delivery. Focused cases checked stale-message non-resurrection and tag-collision rejection.

Simulated-interface tests covered packet controls, visible versus internal agreement, replay export/import, undo, safe text rendering and an old file read completing after reset. These results do not verify real network delivery, authentication, durable storage, crash recovery, tombstone compaction or an unbounded number of replicas.
