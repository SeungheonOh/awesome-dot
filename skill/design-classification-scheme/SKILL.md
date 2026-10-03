---
name: design-classification-scheme
description: Design a reusable taxonomy, tag scheme or annotation codebook for ordinary non-personal material, with clear category boundaries and any requested assignments. Use when the categories and labeling rules need deciding, rather than merely extracting known fields, applying an established scheme, filing documents or summarizing feedback themes.
---

# Design a Classification Scheme

Deliver the actual scheme another person can apply: useful categories, their meanings and the rules for assigning them. Include the requested classification of supplied material. A list of attractive label names or a general explanation of taxonomies is insufficient when the user needs consistent decisions.

Keep the output proportional. A short request may need a few definitions and examples in the response. A reusable codebook and assignment file should be saved when requested. This workflow does not require a classifier, database, ontology, workshop or statistical agreement study.

Use the substantive workflow when categories are supporting another result. Feedback synthesis owns the investigation brief; extraction owns finding stated values; data modeling owns persistent facts and relationships; interface design owns screens and interactions. This guide owns deciding a classification scheme itself. It concerns ordinary documents, assets, items or non-personal observations, not sensitive inferences or consequential judgments about people.

## Establish what the labels must help someone do

Read the request, supplied material and any existing scheme. Identify the decisions or retrieval questions the categories should support. Labels useful for browsing by subject may be poor labels for explaining failure modes; a folder destination may need one choice while annotation may need several.

Define the unit being classified. A document, passage, product variant, observation and report about an observation can need different assignments. Preserve source occurrence identity and meaningful versions. Two notes about one defect can remain two annotation occurrences without proving two distinct defects. A pointer entry may need its own record even when its content is explicitly equivalent to another entry.

Distinguish accepted constraints from design choices. Honor established terminology, required categories, compatibility rules and requested output fields. Treat existing informal tags as evidence to inspect, not automatic authority. Ask only when a material purpose or meaning is unsettled; make and label ordinary reversible design choices when the user has delegated them.

Inspect representative content before choosing a structure. Include ordinary items, mixed cases, apparent exceptions and material with incomplete evidence. Titles and metadata can locate candidates but may not establish their contents. A small supplied collection shows cases the scheme must handle; it does not establish every future case or the prevalence of a category.

## Choose dimensions and useful granularity

Separate dimensions that answer different questions. Subject, purpose, format, lifecycle and evidence status can all describe one item without belonging in a single exclusive list. Use a few facets when they make selection clearer; use a flat scheme when one dimension is sufficient. Do not create a facet merely because a column happens to exist.

Choose categories at a level that helps the intended decision. A category for every title does not generalize, while a broad miscellaneous category can hide the distinctions the user needs. Split a category when a recurring decision or important boundary warrants it; combine categories when their distinction has no useful consequence in the stated task. Rare but consequential cases need not be discarded because they occur once.

Decide assignment cardinality explicitly:

- If a facet requires one label, state the choice rule for mixed material and when the evidence leaves that choice unresolved
- If several labels can coexist, explain what earns each one and whether supporting mentions are enough
- If a primary label is needed, define what makes it primary rather than choosing the first or longest passage automatically
- If no current category fits inspected material, keep that gap visible instead of forcing an inaccurate label

Do not require mutual exclusivity or exhaustive coverage unless the use needs them. Where a hierarchy helps, define what a parent-child relationship means. A narrower kind, a component and a related topic are different relationships. Do not silently mix them into a tree or infer ancestor assignments without a stated convention. A flat vocabulary can be the clearest sufficient result.

## Define meanings, not just names

Give each useful category a plain label and an operational definition. State the evidence that includes an item, the nearby cases it excludes, and any rule needed to distinguish it from a competing category. Use contrasting examples from the supplied material when they expose a real boundary. An example illustrates a rule; it should not become a hidden list of record IDs that a future editor must memorize.

Preserve stable category identity when assignments will be saved or reused. A display label can change without changing the concept, and one ambiguous word can have several meanings. Keep preferred labels and permitted aliases separate from definitions. Do not treat an old tag as an alias merely because it resembles the new label; inspect how it was actually used.

Make evidence states interpretable. Depending on the task, distinguish an inspected absence, unavailable content, an inapplicable dimension, a conflicting interpretation and an inspected item outside the vocabulary. Use only the states needed, but do not let one blank or Other value hide materially different situations. State the meaning of empty cells or reserved values in a delivered schema.

Keep source claims and editorial judgments separate. A reported symptom, a proposed explanation and a suggested change may occur in one passage. A category assignment can describe what was reported without verifying that the event happened or that the explanation is correct. Preserve negation, conditions, scope and uncertainty in the supporting evidence. A title, quoted allegation or suggested fix does not become a directly observed fact through classification.

Define how relationships affect assignments when relevant. An explicit same-content pointer can support a derivative assignment under a stated rule; an ordinary link does not transfer all of its destination's labels. Retain the relationship and evidence basis, and preserve uncertainty when the target or equivalence is unknown. Do not merge source records as a side effect of labeling them.

## Apply and challenge the scheme

Apply the definitions to the requested population. Retain original identities, relevant source versions and concise evidence for consequential assignments. Keep supported labels alongside material unresolved portions when only part of an item is known. Unassigned labels must not silently mean their properties were checked and absent.

Use the same rule across comparable cases. Review mixed-purpose items, similar wording with different meanings, sparse records and plausible counterexamples. Check whether two categories compete because the evidence is ambiguous or because their definitions overlap unintentionally. Resolve the latter by improving the scheme; preserve the former as an evidence limit.

When a case exposes a weakness, decide what should change: the assignment, definition, category boundary, facet structure or input evidence. Avoid adding a category to escape each difficult judgment. Conversely, do not stretch a definition until materially different cases become indistinguishable. Explain consequential changes and recheck the assignments they affect.

Check usefulness against the original goal. Walk a few concrete retrieval or labeling questions through the actual scheme and assignments. Can a reader find the relevant material without mixing lifecycle, format or confidence into the wrong dimension? Can another editor decide a boundary case from the codebook alone? Use a fresh reader when available and useful, but do not invent agreement or usability results from a self-review.

For a small collection, inspect every assignment. For larger work, choose checks across ordinary, mixed and uncertain cases and state the coverage. If quantitative coding reliability or classifier performance is requested, establish the appropriate independent judgments, units and evaluation design separately. Internal consistency on a few examples is not an accuracy estimate, population model or proof that all editors will agree.

## Preserve meaning when the scheme changes

Keep versioning as simple as the reuse requires. A wording-only rename can retain category identity with an alias or change note. A changed inclusion boundary is a semantic revision even when the display name stays the same. Do not reuse a retired identifier for a different meaning.

For a split, merge or redefinition, identify which past assignments can be translated directly and which need their underlying evidence reviewed. An old broad label may not contain enough information to select one new narrow label. Record a conditional or unresolved mapping instead of inventing precision. Keep the old scheme and assignment snapshot interpretable when history matters.

When correcting assignments or incorporating new evidence, distinguish the new source version from a change to the scheme itself. A document can change while the categories remain stable. A new category definition can change assignments even when the documents are untouched. Preserve the relevant reason and version rather than silently rewriting earlier results.

Do not apply file moves, database updates, model training or live tagging merely because a migration mapping has been designed. Continue those actions only when they are within the requested scope and supported by the actual destination.

## Save and deliver the usable scheme

Return the requested codebook and assignments, with only the supporting material needed to apply or review them. Keep label identifiers, definitions, examples and machine-readable values consistent. Reopen saved files and check record coverage, original identities, valid labels, missing-value meanings and representative exact evidence. A count of assignments is different from a count of source records or underlying entities.

State what is proposed, what was applied, which checks actually ran and what remains uncertain. A coherent scheme can be ready for the requested editorial use while still lacking reader research or measured inter-editor agreement. Deliver that bounded result without claiming deployment, universal coverage or empirical validation that did not occur.

## Reference

The [W3C SKOS Primer](https://www.w3.org/TR/skos-primer/) distinguishes concepts from their labels and describes documentation and relationships within concept schemes. Those distinctions can inform a simple codebook without requiring RDF, SKOS serialization or web publication.
