---
name: compare-cache-replacement-traces
description: "Evaluate FIFO, LRU and a future-aware optimum against the same supplied request trace and capacity assumptions."
---

# Compare cache replacement traces

## When to use

A cache-policy choice or teaching explanation needs request-level evidence rather than an assumed relationship between cache size and performance.

## Required inputs

- Authorized identifier trace and identity/case rules
- Capacity range, initial state and object-size/miss-cost assumptions
- Policies and desired metrics

## Workflow

1. Fix the model: hits find a resident object; misses load it and evict only if full. Keep variable-size objects or unequal miss costs outside an equal-slot model unless explicitly handled.
2. Run FIFO without moving entries on hits, LRU with recency updates, and OPT by farthest next use with deterministic ties. Label OPT as an offline oracle, not an online implementation.
3. Record request-level hit/miss, eviction and resident state, retaining immutable snapshots when tracing. Reconcile hits plus misses with processed requests.
4. Compare whole-trace misses across capacities. More capacity need not improve FIFO; do not generalize that anomaly to every policy.
5. For bounded short traces, cross-check OPT with an independent exhaustive eviction search. Keep modeled misses distinct from measured latency, throughput or memory overhead.

### Make each result reproducible

Record initial residents, capacity, object identity and tie-breaking. If the input is a real trace, preserve the authorized ordering and explain any sampling; reordering changes the answer. Keep resident state immutable in retained trace snapshots so inspection cannot rewrite earlier results.

When comparing capacities, run each policy from the declared initial state for the entire trace. Do not compare a partial playback count at one capacity with a full-run count at another. Missing request intervals limit workload conclusions even when the model is internally correct.

## Output

Per-policy trace results, capacity comparison, assumptions and a recommendation limited to the supplied workload.

## Verification and limits

Check all-identical/all-distinct traces and enough capacity for all distinct objects. The classic 1 2 3 4 1 2 5 1 2 3 4 5 trace produces FIFO 9 misses at 3 slots and 10 at 4.

## Useful follow-up

If the user supplies a new capacity or trace, rerun the same declared model and show which evictions changed. Do not assume a policy that won one trace remains best on the next.

## Worked example

For the synthetic trace A,B,A,C,A and two initially empty slots, FIFO misses on A and B, hits A without changing arrival order, then evicts A for C and misses on the final A:4 misses. LRU updates A on the hit, evicts B for C, then hits A:3 misses.

An offline optimum also has 3 misses because A,B,C each require a first load and the two-slot cache can retain A. Its knowledge of future requests is explicitly labeled. These numbers compare equal-size slots and equal-cost misses, not measured application latency.

The handoff includes the eviction at C as the decisive difference and leaves real-world cache overhead and workload representativeness unmeasured.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
