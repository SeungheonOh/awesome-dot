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

## Output

Per-policy trace results, capacity comparison, assumptions and a recommendation limited to the supplied workload.

## Verification and limits

Check all-identical/all-distinct traces and enough capacity for all distinct objects. The classic 1 2 3 4 1 2 5 1 2 3 4 5 trace produces FIFO 9 misses at 3 slots and 10 at 4.
