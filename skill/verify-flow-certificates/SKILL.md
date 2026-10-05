---
name: verify-flow-certificates
description: Validate directed capacity-flow solvers and their explanations using feasible-flow invariants, residual reachability and independently enumerated cut bounds.
---

# Verify flow certificates

Use when implementing or reviewing a maximum-flow engine, capacity allocation model or an interactive augmentation trace. Preserve the specified model; a capacity-only solution is not evidence about cost, travel time, losses, scheduling or physical safety.

## Fix the model and identity contract

Identify source, sink, directed arcs, capacities and numeric bounds. Reject invalid endpoints, unsupported self loops and nonfinite or out-of-range capacities before solving. Define zero-capacity and disconnected-network behavior. Keep parallel and opposite-direction input arcs distinguishable when users need per-arc results.

A residual reverse edge is bookkeeping for canceling earlier flow, not a newly supplied arc. Store the original arc identity and traversal direction on both residual halves. An opposite input arc needs its own residual pair. A single matrix cell cannot faithfully explain separate parallel-arc allocations without additional identity mapping.

## Verify feasibility at every recorded state

For every original arc, require flow between zero and capacity. Compute net outgoing flow independently at every vertex: it equals the reported value at the source, its negative at the sink, and zero everywhere else. Handle signed zero in strict numerical test frameworks without weakening nonzero comparisons.

Replay each augmentation from the previous snapshot. Check that the residual path starts at the source, ends at the sink and is contiguous. Forward steps add the bottleneck amount to the identified original arc; reverse steps subtract it. Require the reported value to increase by that amount. Historical arrays must own their data so later mutations cannot rewrite prior evidence.

Include an explicit fixture requiring reverse-edge cancellation. Random graphs alone may never exercise that branch, especially with correlated low bits in a pseudorandom generator. Also test parallel arcs, opposite arcs, isolated terminals, zero capacity and bound-sized graphs.

## Certify optimality independently

After the final augmentation, traverse positive residual capacity from the source. The sink must be unreachable. This reachable vertex set defines a cut; sum original capacities directed from its source side to the complement. Do not sum residual capacity, reverse bookkeeping edges or incoming arcs.

Check that the feasible flow value equals the cut capacity. The equality combines a constructive lower bound and an upper bound. A claimed maximum without either feasibility or the cut witness is incomplete evidence.

For small graphs, enumerate all source-containing, sink-excluding vertex subsets and compute their cut capacities directly from the original arcs. Compare the solver's value with the minimum. This brute-force oracle should not call the production residual search. Keep enumeration bounded and use larger randomized cases only where resource limits permit.

## Review the consumer and its claims

Keep final cut marks explicitly labeled when showing earlier augmentation states. A source-side partition is one minimum cut and need not be unique. Preserve IDs in downloads and explain reverse traversals in path displays. Input edits must invalidate old solutions and exports; malformed edits must not leave an apparently current result visible.

Exercise previous/next/final navigation, empty and disconnected outcomes, error recovery and export contents through the real caller or a clearly labeled simulated consumer. Rendering checks and mathematical checks establish different things; disclose untested layers.

## Worked example

For A→B capacity 8, A→C capacity 5, B→C capacity 3, B→D capacity 5 and C→D capacity 7, a feasible flow of 12 reaches D. The partition with A, B and C on the source side cuts B→D and C→D, totaling 12. Feasibility plus this matching cut proves the value is maximal; a source out-capacity of 13 alone would not establish the answer.
