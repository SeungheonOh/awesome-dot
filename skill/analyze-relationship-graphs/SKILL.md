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

