> Public contract projection. Behavior and mathematical requirements are unchanged. Delivery/evaluation process instructions, where present, are omitted. See provenance.json for source hashes and changes. This package is UNRUN.

# Reconcile revisioned observations into an evidenced partial order

Implement the pure function `analyze(observations, queries)` in `solution.py` using Python 3.11+ standard library. This is a fictional offline implementation task, not a request to predict one supplied trace. The evaluator calls your implementation on other inputs. Return the documented JSON tree, do no I/O or import-time work, preserve input trees, and use no persistent process state. Internal architecture is unrestricted.

## Input records and scope

Each observation is exactly `{id, revision, actor, sequence, predecessors, clock}`. IDs and actors are nonempty Unicode strings. revision is a nonnegative integer. sequence is a positive integer or null. predecessors is a list of event IDs, possibly repeated. clock is an opaque Unicode string, preserved as evidence; it provides no ordering guarantee. All inputs have valid shape. There are at most 30 distinct event IDs, 300 observations, 30 predecessors per observation, and 30 queries. Each string is at most 120 characters. Queries are two-element lists of distinct IDs occurring somewhere in observations; duplicate queries are allowed. Empty observations has no queries.

A record is a complete snapshot of one event at a revision, including its entire predecessor list. A higher revision replaces the earlier snapshot; do not union obsolete predecessor lists or preserve obsolete actor/sequence facts. For each ID, use only observations with its maximum revision. Canonicalize predecessor lists as sorted sets. If those maximum-revision records are identical in every field after that canonicalization, collapse them into one active event. If they differ in any field, report that ID as a conflict and do not choose a winner. Lower revisions, including conflicting lower revisions, are superseded. Replaying or permuting observations must not change the answer, except valid path/cycle/witness choices may differ between different implementations.

This normalization is part of the task's ingestion contract. It deliberately precedes the unique-event graph and takes precedence over generic advice to reject every repeated event ID. No source clocks, ingestion position, or greater revision number establish an edge between different events.

## Unresolved evidence and precedence

`events` is the list of all unambiguous canonical active records, sorted by ID. Collect exactly these issues:
- `conflicts`: sorted IDs with nonidentical highest-revision records
- `missing`: sorted objects `{event, predecessor}` for each distinct predecessor referenced by an unambiguous active record that is absent from the entire ID inventory. Sort by event then predecessor. A referenced conflicted ID is not missing; it is already an unresolved conflict
- `positions`: objects `{actor, sequence, events}` for every non-null `(actor, sequence)` shared by two or more unambiguous active events. Sort by actor then sequence; each events list is sorted

If any issue list is nonempty, status is `unresolved`. This takes precedence over any cycle one might infer from the remaining records. Return edges and gaps as empty lists, order/ranks/unordered/cycle as null, and an unresolved query result as described below. Do not compute a convenient partial ordering or silently discard problematic constraints. This conservative whole-scope policy is intentional.

## Graph and evidence

When all issue lists are empty, create nodes for all active events. Add an edge from every explicit predecessor to its event. For each actor, sort its events that have non-null sequence by numeric sequence and add edges between successive known positions. Null sequence events receive no sequence edge; explicit predecessor edges still apply. Sequence gaps do not invent extra nodes or block analysis: sequences guarantee relative order of known events even when some records are absent.

`edges` is a sorted list of `{from, to, reasons}`. Order by from then to. Deduplicate edges and sort their distinct reasons, each exactly `explicit` or `sequence`. An edge justified both ways has both reasons. Preserve explicit self-links.

`gaps` is sorted by actor then after then before and contains `{actor, after, before}` for each consecutive known sequence pair whose difference exceeds one. These are coverage gaps, not extra edges beyond the sequence rules and not proof of a complete real-world history.

If the graph has a directed cycle, status is `cyclic`. Return any concrete closed simple cycle in `cycle`: repeat the first ID at the end, all other IDs distinct, and every consecutive pair an actual directed edge. A self-link is `[id, id]`. Keep edges/gaps/events/issues; order/ranks/unordered are null. Do not drop an edge to force an ordering.

Otherwise status is `ok`, cycle is null, and:
- `order` is the lexicographically smallest topological order: repeatedly choose the smallest available ID (Python string ordering)
- `ranks` maps every ID to `{earliest, latest}`, its minimum and maximum one-based positions over all valid topological orders. Count distinct reachable events, never path multiplicity
- `unordered` is every unordered pair of IDs `[smaller, larger]` where neither is reachable from the other, sorted lexicographically. Unordered does not mean simultaneous

For the empty graph, order and unordered are empty lists, ranks is an empty object, and status is ok.

## Queries

Return one query object per input query, preserving input order, with exactly these fields for its relation:
- If status is unresolved: `{pair: [a,b], relation: "unresolved", reason: "evidence"}`
- If status is cyclic: `{pair: [a,b], relation: "unresolved", reason: "cycle"}`
- In a DAG where a reaches b: `{pair: [a,b], relation: "before", path: [a,...,b]}`
- In a DAG where b reaches a: `{pair: [a,b], relation: "after", path: [b,...,a]}`
- Otherwise: `{pair: [a,b], relation: "unordered", witness_ab: [...], witness_ba: [...]}`

Paths must be simple and follow actual edges in the supplied direction. Any such path is valid; shortest is not required. Each witness is a complete topological order of the original graph, with a before b for witness_ab and b before a for witness_ba. Any valid witness is accepted; it need not use the primary order's tie-break. A display position in one order is not a path or proof of required order.

The result object has exactly `status`, `events`, `issues`, `edges`, `gaps`, `order`, `ranks`, `unordered`, `cycle`, `queries`. Return ordinary detached JSON-compatible trees; do not mutate inputs or share mutable output descendants with them. Repeated calls must be deterministic and independent. Invalid input shape handling is out of scope.

