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

## Restore editable inputs separately from computed evidence

Give editable networks and computed result/certificate exports distinct schema identities. On import, validate endpoint types without coercion, numeric capacities, arc count, file size, version and any experiment settings before changing the current work. Preserve the ordered input arcs and rebuild their identities deterministically. Recompute the solution rather than trusting a stored maximum, cut or history. Unknown fields must not silently become solver options.

Keep the previous network on malformed input. Use an operation identity for asynchronous reads: later edits, resets or a newer import must prevent an older completion or error from replacing the current view. Check a pending import followed by an input edit, a newer successful import followed by an older failure, and changes to experiment controls while reading. Test the public export through the public import path; JSON serialization alone is not evidence of a usable roundtrip.

## Check diagrams against the certificate

Build the diagram from the same immutable state used for the table and download. Preserve input arc IDs in labels; do not collapse parallel or opposite arcs into a single line. Give siblings distinct paths using a canonical endpoint ordering, so reversing an input arc does not accidentally put it on another arc's curve. Keep source and sink identifiable even when they are isolated.

A selected reverse residual step needs a reverse arrow on the original arc and an explanation that it cancels flow. Recoloring the forward arrow alone conveys the wrong direction. Check the overlay's actual geometry and original ID against the recorded path; matching only the number of highlighted edges misses swapped identities. A final-cut overlay shown during earlier steps must remain labeled as final, rather than suggesting the partial flow is already optimal.

Exercise maximum parallelism, opposite arcs, all supported vertices, zero flow and a known cancellation fixture. Require finite coordinates, distinct arc paths where identities differ, deterministic layout, current flow/capacity labels and complete clearing after invalidation. Bound the canvas and offer a readable table for dense graphs. Do not promise every label is overlap-free merely because the geometry is finite.

Distinguish DOM/SVG assertions, a static image render, and actual browser interaction. A blocked preview does not validate browser layout. Verify narrow-screen scrolling, text size, navigation and controls in a supported browser when available; retain an explicit verification limit otherwise.

## Evaluate capacity changes without overclaiming

A marked minimum cut is not a list of upgrades guaranteed to help. To evaluate a proposal, change exactly the specified input arc, solve the new bounded network, and independently check the resulting certificate. Keep the original input and result unchanged. Preserve caps explicitly: an increment near the allowed maximum may be truncated, and an arc at the cap has no modeled headroom.

For a single arc increased by d, the maximum-flow gain must lie between zero and d. This is a useful invariant, not a replacement for the cut check. Compare small scenarios with direct cut enumeration; test both useful and ineffective upgrades, zero capacities, parallel/opposite arcs, and capacity caps. Never sum gains from separate one-arc scenarios as if they were a joint plan. Joint changes need a separate solve, and cost-benefit claims need a cost model.

For example, A→B capacity 4 and B→D capacity 4 have two equal bottlenecks. Increasing either arc alone by 5 still leaves maximum flow 4. In contrast, A→B capacity 3 and B→D capacity 8 gain 5 when the first arc is increased by 5; increasing only the second gains nothing. These fixtures catch explanations that mistake membership in one minimum cut for guaranteed marginal benefit.

## Worked example

For A→B capacity 8, A→C capacity 5, B→C capacity 3, B→D capacity 5 and C→D capacity 7, a feasible flow of 12 reaches D. The partition with A, B and C on the source side cuts B→D and C→D, totaling 12. Feasibility plus this matching cut proves the value is maximal; a source out-capacity of 13 alone would not establish the answer.
