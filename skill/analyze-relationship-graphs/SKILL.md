---
name: analyze-relationship-graphs
description: Answer a structural question from authorized entity-and-link data using a faithful graph model and checked results. Use for dependency impact, reachability, cyclic groups, connected components, membership projections or other graph-defined relationships. Drawing established relationships and ordinary tabular summaries have separate primary workflows.
---

# Analyze Relationship Graphs

Return the requested structural answer, with enough source evidence to explain what the nodes, links and result actually mean. A graph library call or attractive diagram does not establish that the chosen representation answers the question.

Use `analyze-data-question` for ordinary tabular populations and trends when graph structure is incidental, and `visualize-information` for drawing already established relationships. A diagram can support this analysis without becoming another project. Keep causal event reconstruction with `reconstruct-partial-event-order`, finite transition-property checks with `find-finite-workflow-counterexamples`, and a best feasible allocation under an objective with `solve-constrained-optimization`. A graph-derived dependency order can inform `plan-project-delivery`; it is not by itself a staffed or timed delivery plan.

## Define the relationship and question

Inspect the actual authorized sources and the requested outcome before choosing algorithms. Identify the entities, the meaning and direction of each relation, source coverage, and any relevant state or time. Clarify a consequential ambiguity such as “uses” versus “is used by,” or current links versus proposed links. Do not turn a clear small question into a graph-design intake.

State the unit being counted: source records, relationship identities, distinct endpoint pairs, memberships, paths or entities. These can have different totals. Define whether a target is included in its own reachable set, whether only known inventory records count, and which edge types or states are eligible when those choices affect the answer.

Preserve exact IDs separately from display names. Numeric-looking text can remain distinct, and identical labels need not identify the same entity. Use separate namespaces or typed keys when different entity classes can share an ID. Keep the original source and a recoverable row, record or passage reference for each modeled relationship.

Treat absent data as a coverage boundary. A referenced entity missing from the inventory may have a known ID but unknown attributes or further links. Retain it as such when the relation is supported. An unconnected listed entity is different from an entity omitted from the selected sources; missing edges do not establish that no real relationship exists.

## Build the smallest faithful model

Choose directed or undirected edges from the relation's meaning. Decide whether parallel relationships and self-links are meaningful. A simple graph can silently merge distinct links; a multigraph can accidentally count repeated captures as new relationships. Reconcile repeated source observations using the supplied identity and version rules, retaining their provenance. Do not deduplicate solely by endpoints or display text.

Store meaningful edge attributes such as type, status, time and weight. Explain what a weight measures and its units: frequency, cost, distance, capacity or similarity are not interchangeable. Aggregating several links requires a stated rule appropriate to the quantity. Preserve the underlying evidence when a simplified adjacency view is sufficient for one calculation.

For membership data, retain the two entity sets and the original memberships before deriving a projection. Repeated appearances within one record may be one membership or several events; use the source contract. A projected link means shared membership under a rule, not automatically direct interaction. If its weight counts distinct shared members, retain those member IDs and avoid counting both orientations of an undirected pair.

Retain declared isolates, empty membership records and unresolved attributes when relevant. Check endpoint references, node types, edge identity collisions and invalid values before analysis. Stop the affected calculation for a conflicting identity or undefined weight interpretation while completing independent work; do not resolve a contradiction by keeping whichever row was read last.

Use available tools and formats that preserve these semantics. The [NetworkX graph-type reference](https://networkx.org/documentation/stable/reference/classes/index.html) illustrates the separate choices of direction, parallel edges and self-links. No particular library, graph database or hosted service is required. Inspect the chosen tool's behavior rather than assuming every algorithm supports every graph type.

## Apply the method that answers the question

Run only the relevant analysis, with its assumptions explicit. Avoid an unrequested catalogue of metrics.

- **Reachability or impact:** Follow the relation in the required direction. If arrows mean consumer to dependency, finding consumers of a changed dependency follows incoming links. Supply an evidence path when it helps explain membership in the result. One valid path proves reachability; it does not establish a shortest path, all possible paths, actual failure or an applied change.
- **Paths and distances:** Define allowed edges, path direction, cost and tie handling. Distinguish minimum hops from minimum weighted cost. Check the chosen algorithm's restrictions, including negative weights or cycles when relevant. Do not turn a frequency or similarity into distance by an unexplained inverse. Avoid enumerating every simple path when the task only needs a witness or a bounded summary.
- **Components and cycles:** Distinguish undirected connectivity, weak directed connectivity and mutual directed reachability. A self-link or cyclic group can be valid data rather than an error. When ordering a directed model with cycles, contract strongly connected groups and retain their members and internal evidence. The resulting condensation is acyclic, as described in the [condensation reference](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.components.condensation.html). Order groups in the direction required by the task; do not invent a strict internal order.
- **Membership projections:** State the projected entity set, pair rule and weight definition. Check that the input memberships meet the assumed two-set structure. Different normalizations answer different questions; the [weighted-projection reference](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bipartite.projection.weighted_projected_graph.html) distinguishes shared-neighbor counts from a normalized ratio. Preserve enough base data to reconstruct the projection.
- **Bridges or removal scenarios:** Name the object being removed and the connectivity definition. In an undirected graph a bridge is an edge whose removal increases the component count; see the [bridge reference](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.bridges.bridges.html). Removing a projected edge, one parallel relation, a source record or an entity can have different effects. Do not substitute one operation for another.
- **Ranks or groups:** Use a requested, justified structural measure with its direction, normalization and parameters. Degree, centrality and detected communities are properties of this representation and algorithm. They do not establish importance, quality, causality or a true classification without additional evidence.

Choose deterministic tie rules where reproducible output matters, without calling one arbitrary valid ordering uniquely correct. For approximate, sampled or limited calculations, state what was searched and what remains unresolved. A resource limit or failed run is not proof of disconnection or absence.

## Compare states without changing the source facts

Keep the baseline and any proposed, filtered or time-specific graph separate. State exactly which nodes or edges changed, whether the node population remains fixed, and whether counts refer to each view or their difference. Preserve excluded relationships in the reusable source representation when appropriate.

A thresholded view can create isolates or split components. Retain the intended node population instead of dropping nodes merely because no displayed edge remains. Report sensitivity when a chosen threshold materially drives the conclusion; do not imply that a visually tidy partition validates the threshold.

Co-occurrence, connectivity and hypothetical removal are structural observations under the declared model. They do not by themselves establish statistical association, causal effect, operational failure or permission to change the underlying resources. Keep those interpretations separate from the computed result.

## Verify the saved answer and present it usefully

Reopen the actual graph and result files when files are requested. Check that serialization preserves IDs, namespaces, direction, multiplicity, attributes, isolates and source references. A drawing is not the reusable graph, and matching counts alone cannot detect reversed edges or merged identities.

Reconcile the important results with the original records. Replay representative or complete evidence paths at a scale appropriate to the task; verify each edge and its eligibility. Check group membership, source-supported projection weights, conservation of the modeled node population and the stated comparison deltas. For a small graph, direct reachability or edge-removal checks can provide a useful independent check of a more complex method. For larger work, use suitable invariants and targeted cases rather than claiming exhaustive verification.

Keep test cases focused on the model's actual failure risks: a direction-sensitive path, meaningful parallel links, a valid cycle, a namespace collision, an isolate, or a threshold boundary where relevant. Do not add every case to every task. If a saved consumer or update command is part of the request, exercise that actual interface and report its limits.

When providing a visual, inspect the rendered output at a usable size. Make arrow meaning, IDs or labels, state distinctions, weights and omitted context clear. Avoid layouts that hide parallel edges, boundary nodes or isolated records. A simplified view should identify its simplification and point to the underlying result; node proximity on the page is not an additional measured relation.

Lead the handoff with the answer, the decisive model assumptions and any material coverage limit. Provide the requested graph, table, view or rerunnable method, with source evidence close enough to check consequential claims. A short response can be complete without separate files or an appendix. Describe what was actually calculated, reopened, executed and viewed, and leave unavailable verification explicitly unresolved.


## Worked Boolean implication witness

For a conjunction of clauses with at most two Boolean literals each, preserve clause IDs while mapping A OR B to !A → B and !B → A. A unit clause A is A OR A. Arbitrary longer clauses cannot be handled by this construction unchanged. If a variable and its negation are mutually reachable, return both source-linked paths: either truth choice implies its opposite. A generic cycle elsewhere is not sufficient to prove inconsistency.

For clauses 1: A OR B, 2: !A OR B, 3: A OR !B, 4: !A OR !B, one witness is A → B (2) → !A (4) and !A → B (1) → A (3). Verify each edge against its cited clause and verify that the paths meet the required endpoints. The union of these clauses is unsatisfiable, but do not call it a smallest conflict unless separately proved. For a satisfiable result, return a complete variable assignment and evaluate every original clause against it; graph exploration alone is not the user-facing witness.

A bounded local implementation was checked against exhaustive truth tables for 800 seeded formulas over at most six variables, along with unit contradictions, tautologies, malformed syntax and maximum input bounds. Each returned path was replayed against the original clauses. This supports the declared two-literal model only; it does not establish that a real policy was fully captured or authorize changing its settings.

In a satisfiable two-literal model, distinguish a chosen value from a forced one. A path !A → A proves A must be true; A → !A proves it must be false. Return the clause-linked path as evidence. When neither path exists, each value can occur in some model, but do not imply that multiple flexible variables can be set independently: A OR B allows each individually to be false, not both together. Check these classifications against the full set of satisfying assignments on small fixtures.

To reduce a reported conflicting rule set, retain stable source IDs and distinguish irreducible from smallest. Start from a verified unsatisfiable subset, try removing each clause, and retain a removal only when the remainder is still unsatisfiable. Finish by checking a satisfying assignment for every single retained-clause removal. These certificates prove irreducibility of the returned subset, not global minimum size or that omitted rules are consistent. Reindexing an internal solver input must not change the source IDs cited in the final paths. Run potentially repeated solver calls in a bounded, cancellable operation; edits and cancellation must invalidate late results. A local worked implementation checked 202 contradictory generated formulas, each removal assignment and source-ID preservation, plus cancellation and worker-error paths.

For a reusable proof file, separate computation from verification. Reconstruct the graph-defining clauses from the supplied input, compare saved source identities, and independently replay the claimed assignment or contradiction edges rather than accepting the solver's `success` field. For an irreducible core, verify its original-clause subset, its contradiction and every removal assignment. Reject missing, duplicated or altered evidence. State exactly which claims the checker covers: validating a satisfiability witness does not authenticate its author, validate external policy assumptions, prove minimum conflict size or automatically validate unrelated annotations. Bound file size before reading and prevent a superseded asynchronous import from overwriting a newer verdict.

A flexibility claim can carry constructive evidence too: provide two complete satisfying assignments with opposite values for the selected variable. Check both against every original clause and confirm the selected values differ as claimed. For A OR B together with !A OR !B, the alternatives are A=false/B=true and A=true/B=false; the paired assignments make the dependency visible. Require a complete, unique annotation set if a proof file claims to classify every variable, and verify forced paths separately from flexible assignments. Do not silently accept older annotations that lack the newly required evidence. A local worked checker exercised all 800 truth-table fixtures, a 40-variable flexible case, and mutations of pinned values, missing assignments, forced directions and clause provenance.

## Worked relative-difference constraints

For requirements of the form TO minus FROM at most MAX, retain a directed edge FROM to TO with weight MAX and the original requirement ID. A negative edge alone is valid. A connected cycle whose edge weights sum to a negative number is a contradiction: adding its inequalities cancels every variable and demands zero be less than a negative bound. Initialize a zero-weight super-source to every node when checking the entire system, so an unrelated component's conflict cannot be missed. See the [MIT treatment of Bellman-Ford and difference constraints](https://ocw.mit.edu/courses/6-046j-introduction-to-algorithms-sma-5503-fall-2005/resources/lecture-18-shortest-paths-ii-bellman-ford-linear-programming-difference-constraints/).

For design to build at most 3 ticks, build to launch at most 2, and launch to design at most -6, the loop totals -1. Return the source-linked loop and check its continuity and exact sum independently. In a feasible system, return a complete potential assignment and evaluate every original inequality. Translating all potentials to put a reference node at zero preserves differences, but does not make the result an earliest schedule or establish alignment between disconnected groups. Explicitly exclude calendars, resource capacities and other constraints not supplied by the user.

Use bounded exact arithmetic or justify safe numeric limits; do not silently round tight inequalities. Preserve parallel requirements and self-constraints. A local worked implementation checked 1,200 seeded graphs against independent Floyd-Warshall negative-diagonal detection, plus 400 independently constructed feasible systems and direct evidence checks. Its saved-proof checker reconstructs source identities and checks assignments or cycle certificates without invoking the solver. Verification of a witness does not certify ancillary annotations, minimal conflict size, authorship or real-world completeness.

For a feasible difference-constraint system, answer a pair-range question separately from displaying one arbitrary assignment. A path from A to B bounds B minus A above by its total; the reverse direction bounds it below. To certify a claimed *tight* finite bound, supply both a source-linked path and a complete feasible assignment attaining that value. A longer path may establish a valid but loose bound, so path replay alone is insufficient. For an unbounded direction, establish feasibility first and verify that the corresponding endpoint is unreachable in the constraint graph; do not substitute a missing displayed path for a reachability check. Keep same-event differences at zero. A worked checker compared 4,453 pairs with independent all-pairs distances and validated endpoint assignments, a forged loose-bound case, disconnected directions and exact large integer sums.
