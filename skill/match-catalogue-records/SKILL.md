---
name: match-catalogue-records
description: Match records across inconsistent non-personal catalogues into an evidence-backed crosswalk, retaining competing candidates and unresolved identities. Use when reliable shared keys do not settle correspondence, rather than for an exact-key join, registry lookup, source cleanup or merging already matched records.
---

# Match Catalogue Records

Deliver the requested correspondence result: supported links, unresolved candidates and records with no qualifying counterpart in the searched population. Preserve original record identities and enough evidence to review each consequential decision. A list of similar titles, an exact join or a ranked candidate list is not a completed identity crosswalk when the user needs matching judgments.

Use this for ordinary item, asset, document or edition catalogues. Keep exact-key joins and authoritative identifier lookups as simpler routes when they already resolve identity. This workflow does not identify people, enrich personal profiles, authorize merging source records or establish that catalogue assertions are true in the world.

## Decide what the same thing means

Read the selected catalogues and the user's identity definition before comparing names. Establish the entity level: a work or its edition, a product family or an orderable pack, an asset or a particular variant. A compatible substitute, translation, supplement or related item may be useful without being the same requested entity.

Keep source occurrence identity separate from entity identity. Two rows may be separate scans or listings of one edition; two similar rows may represent different items. Scope identifiers to their actual source or namespace. Equal record IDs from different suppliers are not automatically one record, and different IDs do not prove different entities.

Establish the permitted relationship cardinality. One-to-one, many-to-one and many-to-many correspondences have different meanings. Use an evidenced requirement rather than forcing a one-to-one assignment to make the output tidy. Matching several occurrences to one entity does not authorize selecting a survivor, deleting duplicates or replacing their attributes.

Resolve a material ambiguity in the identity level before treating dependent links as settled. Continue source inventory and supported comparisons when possible. Ordinary choices about output columns or readable wording do not require another approval.

## Prepare comparisons without erasing evidence

Inspect actual fields, types, missingness and selected source coverage. Retain original values and locators. Put useful normalization in a separate comparison representation: supplied aliases, equivalent units, title tokenization or established identifier syntax. Do not silently rewrite the catalogues or assume an abbreviation, punctuation change or transliteration preserves identity.

Compare like attributes. The same number can describe a different dimension, unit, pack quantity or reference period. Missing metadata is not agreement, and a blank revision is not the first release. Keep quantities and their meanings together. If a source correction or authority rule is supplied, apply it only to the record, field and scope it actually governs; recency alone does not settle all conflicts.

Use an identifier as strong evidence only within its established scheme and scope. A supplier's internal code, a manufacturer-reported code and an occurrence ID may have different authority. A convenient composite key can help compare records without becoming proof that the fields uniquely identify the intended entity.

## Make candidate coverage visible

For a small bounded task, examining all cross-catalogue pairs may be simpler than introducing scoring or a search service. For larger data, choose transparent candidate rules that reduce work while retaining plausible counterparts. Use the available local tools or an authorized service, and state the relevant population and limits.

Candidate generation is a separate source of error from deciding between candidates. A title-prefix filter can miss an abbreviated title; a required field can exclude the true counterpart when that field is missing. Use complementary retrieval paths where the data warrants them, and inspect a few plausible cases outside a chosen filter. Do not hide a discarded tail behind an arbitrary top-k cutoff.

Keep enough information to explain why a pair was considered and which records were never compared. A search result cap, unavailable page or interrupted run limits the no-match conclusion. Distinguish not examined from examined without a qualifying counterpart. An empty candidate set is not proof that an entity does not exist elsewhere.

Do not send private catalogue values to a new service simply to obtain candidate suggestions. Use the access and source scope authorized for the task; check the actual service's identity, coverage and scoring behavior when it is used. A provider result remains evidence to interpret under the user's identity definition.

## Judge evidence and competing matches

Compare candidates using the attributes that distinguish identity for this task. Separate positive evidence, incompatible facts and missing information. Title resemblance may identify a useful candidate but cannot override a substantive edition, model, language or pack-size conflict. A common introductory passage may occur in several revisions; interpret its actual coverage before calling two documents identical.

Give source-based reasons for decisions. If a code suggests the same item while specifications contradict it, identify the conflict rather than silently choosing the code or inventing a correction. State whether the evidence establishes a different entity, leaves a possible metadata error unresolved or merely fails to support the link. Those are different conclusions.

Review plausible counterparts together. Keep a tie or insufficient distinction unresolved instead of choosing the first row, the highest score or the most complete record. Name the specific evidence that would resolve it. If several counterparts are supported at the requested entity level, retain them under the allowed cardinality rather than declaring an artificial conflict.

Use scores only when they help the task. Explain the relevant features and what the score means. A similarity score is not a probability of identity, and two systems' scores need not be comparable. Choose any acceptance threshold with the consequences of false links and missed links in view; do not tune it merely to produce a pleasing match rate. For a small manual crosswalk, direct judgments and explicit uncertainty may be enough.

Do not infer a whole entity cluster from a chain of resemblance. A–B and B–C candidate similarities do not establish that A, B and C are the same thing. If consolidating accepted relationships into groups is requested, inspect contradictory attributes and the intended entity level across the whole group. Optimization can enforce an agreed assignment constraint; it cannot turn unsupported pair scores into identity evidence.

## Build the usable crosswalk

Use the requested schema and format. A practical crosswalk usually needs original source identities, counterpart identities where present, a clear disposition and the decisive evidence or unresolved question. Keep proposed candidates distinguishable from accepted links in both human and machine-readable output.

Account for unmatched or unexamined records without fabricating an ID. Define a blank or null counterpart marker when the output format needs one. Retain repeated occurrences and meaningful order; do not key an output dictionary solely by a duplicated business identifier. Include unmatched records from both sides when that is part of the requested reconciliation.

Keep matching separate from canonical-value selection. Establishing that two records describe one edition does not decide which title, date or other attribute should overwrite the other. If cleanup, consolidation or import is also requested, carry the reviewed crosswalk into that work under its stated rules and authority. A matching request alone ends before those source changes.

Keep the handoff proportional. A small requested comparison can be a direct answer with supported and unresolved pairs. A reusable catalogue crosswalk should be an actual saved artifact. A complete all-pairs ledger, custom matcher, database and statistical benchmark are not mandatory deliverables.

## Verify decisions and saved coverage

Reopen the actual saved result and compare important links and exclusions with the source fields and identity definition. Check plausible false matches and ambiguous cases as well as easy positive links. Inspect candidate coverage separately from the correctness of a selected pair, including a relevant case that could have fallen outside the search rule.

Reconcile pairs, source occurrences and entity groups as different units. Six links need not mean six distinct records on each side. Check that every promised record is accounted for, each intended pair appears once, unresolved candidates have not become positive links and original evidence remains intact. For a small task, reviewing all decisions may be appropriate; for a larger task, state which decisions and populations were actually checked.

If the user requests a reusable matcher, exercise its real saved entry point on representative records and inspect the actual crosswalk. Preserve useful failures and version the data, rules and decisions when they change. A snapshot-specific script that reproduces reviewed decisions can be useful, but label it as such rather than claiming it generalizes to new catalogues.

Use independently adjudicated pairs when estimating matching performance. Include plausible nonmatches and ambiguity, and keep development examples separate from evaluation when making broader performance claims. Report the measured population, candidate coverage and relevant wrong-link/missed-link tradeoff. Without that evidence, report inspected decisions and remaining uncertainty rather than an invented accuracy percentage. Do not require a labeled benchmark merely to finish a small manual reconciliation.

Return the crosswalk and its material limits. Explain what remains unresolved, what source would settle it and how far no-counterpart claims extend. Complete the requested local result without presenting it as a live merge, a verified external identity register or universal proof of catalogue accuracy.

## Reference

[OpenRefine's reconciliation documentation](https://openrefine.org/docs/manual/reconciling) distinguishes original values, candidate suggestions and match judgments, and notes that reconciliation scores depend on the service. Those concepts are useful here without requiring OpenRefine or an external service.
