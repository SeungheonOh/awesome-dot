---
name: reconstruct-partial-event-order
description: "Reconcile bounded event records into a causal partial order using evidenced source sequences and predecessor links, exposing contradictory cycles and unresolved relative ordering without trusting unsynchronized clocks."
---

# Reconstruct Partial Event Order

## When to use

Use this when a user or agent needs to reconcile records from several services, workers or devices and wall-clock sorting may be misleading. Produce a traceable partial order and identify what the evidence does not establish. This is a read-only reconstruction task, not permission to change logs, retry requests or assign blame.

## Required inputs

- A bounded, authorized event set with stable event identifiers
- A source/actor identifier and an evidenced local sequence when available
- Explicit predecessor, request/response or message-correlation evidence
- Original clock strings, their timezone/precision when known, and any documented clock guarantees
- The question being investigated and coverage limits, including missing sources or sequence gaps

Do not invent predecessor links from similar text or close timestamps. If a local sequence is merely an ingestion index, do not silently treat it as the event's execution order. Unclear sequencing semantics are a missing input.

## Workflow

1. **Preserve source evidence.** Retain stable identifiers, original timestamps and relevant correlation fields. Work on a copy. Separate source record identity from a display position; the latter can change when new evidence arrives.
2. **Define trusted ordering rules.** Record which source sequences guarantee local order and which links imply that one event preceded another. Clock strings alone should not impose cross-source order unless their synchronization, uncertainty bounds and semantics justify it. Capture assumptions explicitly.
3. **Validate references.** Reject duplicate event IDs, ambiguous sequence positions within an actor and predecessor references absent from the chosen scope. If a predecessor lies outside the scope, either retrieve it within authorization or mark the boundary unresolved; do not pretend that edge does not matter. Duplicate identical edges may be consolidated while preserving their provenance.
4. **Construct the directed constraint graph.** Add edges from an earlier source-sequence event to the next event in that source, and from each explicit predecessor to its successor. Preserve the reason and source for each edge. The graph encodes supplied constraints, not every real-world dependency.
5. **Check consistency before sorting.** A directed cycle means no total ordering can satisfy all recorded constraints. Return one concrete cycle with event IDs and edge evidence. Do not drop an inconvenient edge or select the “most likely” source without a documented decision. A self-predecessor is already a cycle.
6. **Expose uncertainty for an acyclic graph.** Produce one deterministic topological order for navigation, clearly labeling the tie-break rule. Compute reachability: two events with neither reachable from the other are unordered by the evidence. They may have occurred in either order; this does not prove they were simultaneous.
7. **Calculate rank bounds when useful.** For an event in a finite DAG, earliest one-based position is one plus its number of distinct ancestors. Latest position is total event count minus its number of distinct descendants. Count reachable events, not paths; diamond branches can reach the same descendant twice. These are individual bounds across valid orders, not permission to independently choose every event's position.
8. **Answer the actual incident question.** Tie each statement to a path, an unordered pair or a contradiction. Distinguish “must precede under these inputs” from “appears earlier by recorded clock.” Record missing actors and sequence gaps so a complete graph traversal is not mistaken for a complete real-world history.
9. **Verify before delivery.** Replay every edge against the displayed order, independently enumerate all valid orders for a small fixture, and compare rank bounds and unordered pairs. Test clock skew, a diamond, independent events, a missing predecessor and a cycle. Export the assumptions and source mappings alongside the result.

## Give pair-specific evidence

When asked why one event precedes another, return a path through the actual constraint edges, including stable event IDs and each edge's reason. Breadth-first search can keep the explanation short. A displayed position in one topological ordering is not sufficient evidence of a required relation. If the reverse path exists, explain the reversed relation; do not flip the recorded edge directions to match the wording of the question.

For an unresolved pair in a DAG, construct two complete witness orders: temporarily add the first-before-second constraint for one, and the second-before-first constraint for the other, then topologically order each augmented graph. This does not modify the source. Verify that both orders contain every event exactly once and satisfy every original edge, and that they actually reverse the selected pair. Label them as possible sequences, not reconstructed history or evidence of simultaneity.

Reject absent or identical IDs, and do not construct uncertainty witnesses for an inconsistent graph. Check small graphs against independently enumerated valid orders. Clear a displayed/exportable pair explanation when the selected pair or input changes, so stale evidence cannot appear to justify a newer question. Downloads containing original events need the same privacy treatment as the source logs.

## Worked example

Five events have these constraints:

- request: client sequence1, recorded clock10:00:04
- receive: server sequence1, explicitly after request, clock10:00:01
- log: logger sequence1, explicitly after receive, clock10:00:02
- reply: server sequence2, clock10:00:02
- finish: client sequence2, explicitly after reply and log, clock10:00:07

The server clock being behind does not override the explicit request-to-receive relation. Valid orders are request, receive, log, reply, finish and request, receive, reply, log, finish. The first two and final events have fixed positions1,2 and5. Both log and reply can occupy positions3–4. Their equal clock strings do not establish simultaneity.

Add an asserted edge finish→request. That creates a cycle, for example request→receive→reply→finish→request. Report the conflicting constraints rather than returning a chronological list that silently ignores one.

## Deliverable

Return the scoped event inventory, provenance of ordering edges, consistency result, a cycle witness if inconsistent, or a labeled topological order with unresolved pairs and optional rank bounds if consistent. Include coverage limits and the checks actually performed. Keep original timestamps alongside the reconstructed order.

## Data handling and stopping points

Logs can contain identifiers, payloads or confidential operational details. Minimize fields to those required for reconstruction and keep exports at the authorized destination. A complete exported graph may still reveal sensitive relationships. Stop for missing ordering semantics or contradictory evidence that requires an owner decision; continue independent analysis without repairing the source or making unsupported claims about causation.
