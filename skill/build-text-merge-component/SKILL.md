---
name: build-text-merge-component
description: Build or maintain an application-facing three-way text merger that carries common-base correspondence into compatible text, conflict regions, explicit resolutions, and the consuming workflow. Use for a reusable component, rather than a one-off Git or document merge.
---

# Build a text merge component

Connect a retained original and two edited texts to a result the application can review, resolve, and use. The central relationship is between where each branch changed the common base, the corresponding alternatives in all three texts, and what the consumer may do with those alternatives.

Ordinary Git integration belongs with [parallel-change-integration](../parallel-change-integration/SKILL.md), and choosing among document revisions with [document-revision-reconciliation](../document-revision-reconciliation/SKILL.md). Applying one supplied patch belongs with [verify-exact-text-patches](../verify-exact-text-patches/SKILL.md). Use [implement-scoped-change](../implement-scoped-change/SKILL.md) for general project delivery; this method supplies the merge-specific decisions.

## Establish the caller's merge contract

For maintenance, trace the existing merge entry point, result type, resolution operation, and actual caller before changing them. Preserve the current supported behavior unless the request changes it. For a new component, start with the intended caller and its accepted interface.

Settle the choices that affect correspondence and output:

- Which text is the common base, what the two branch roles mean, and which exact input revisions participate. Without a known base, offer a labeled comparison or resolve the missing lineage; do not invent a three-way history
- The matching units and source coordinates, such as retained lines, characters, or application tokens; encoding, separators, final-newline handling, and any accepted normalization or equality rule
- Which changes may combine automatically, when insertions or replacements compete, and who or what can resolve a conflict
- What the caller needs from a region, whether partial resolution is supported, and how review, save, export, or another consumer recognizes an incomplete result

Keep these decisions in the existing API or usage documentation. A new configuration framework is unnecessary. Textual compatibility does not establish semantic correctness or approval of the merged wording.

## Prefer an existing merge facility

Inspect the project's supported merger and its actual version and options. Prefer an API that exposes regions, alternatives, and status when the caller needs them. A library's default tokenization may discard distinctions the application preserves: for example, [node-diff3's API](https://github.com/bhousel/node-diff3#3-way-diff-and-merging) accepts arrays but splits string inputs on whitespace by default. Select a representation that can reconstruct the required text.

An existing command can also fit. [Git merge-file](https://git-scm.com/docs/git-merge-file) supports three inputs, stdout output, and distinct clean, conflict, and error outcomes; its matching algorithm is configurable. Inspect its actual conflict policy and output contract before adapting it. Do not turn every nonzero result into a conflict or treat a returned string as evidence of a clean merge.

If the facility already supplies suitable regions, retain their correspondence instead of independently diffing the same texts again to invent labels. A second alignment can assign repeated content differently. Use a smaller correspondence primitive only when a concrete gap requires application-specific region construction; a component request does not imply writing a new diff algorithm. Marker text may be a presentation format, but it is a poor substitute for a supported structured result when exact source regions are required.

## Project both changes through the common base

Whether supplied by the engine or assembled in an adapter, the result must preserve the following relationship:

1. **Relate each branch to the same base.** Retain the matching spans and changed spans with their corresponding branch slices. An insertion consumes an empty base range; a deletion produces an empty branch range. Keep coordinate units consistent with the retained text. If comparison normalizes text, retain the mapping back to the original regions the caller must inspect or preserve.
2. **Decide which edits interact.** Compare locations in base coordinates, not equal-looking offsets in the two branches. Use the accepted policy for overlapping replacements, unequal insertions at one position, and insertions inside or at a replacement boundary. Touching nonempty ranges and zero-width insertions need separate consideration; interval overlap alone cannot settle every boundary decision.
3. **Form coherent regions.** A region spanning related edits must project to the corresponding extent of each branch, including unchanged text between its constituent edits. Extend through related edits when necessary to obtain complete alternatives. Do not split a replacement at an invented interior correspondence or absorb unrelated compatible changes merely to simplify grouping.
4. **Classify the projected alternatives.** Under the usual policy of preserving independent edits, unchanged regions pass through, one-sided changes contribute their changed text, and identical effective changes appear once. Combine independent eligible regions in their established order. Genuinely competing alternatives remain unresolved unless an accepted conflict rule settles them. Compare complete projected alternatives, not only raw diff opcode names.
5. **Assemble without losing correspondence.** Preserve text outside the affected regions. For each reported alternative, its source locator must recover that same source slice under the declared representation. Check ordering and coverage so grouping cannot duplicate or omit text. An inconsistent projection is an error to diagnose, not an invitation to guess a nearby matching phrase.

Repeated text may admit several valid alignments. Require reproducible correspondence for the chosen inputs and configuration where the caller relies on stable regions; do not claim to recover the author's unique edit history. [Python's SequenceMatcher documentation](https://docs.python.org/3.12/library/difflib.html#sequence-matcher-objects) illustrates monotone matching blocks and base/branch opcode ranges, with tie-breaking and junk heuristics that affect matching. It is a correspondence tool, not a complete three-way conflict policy. Check relevant options and performance limits rather than promising minimal edits or a fixed region count.

## Keep resolutions attached to their regions

Expose compatible text and unresolved alternatives through the caller's result model. Preserve enough input identity and source-region correspondence to show what a choice applies to. A region can carry ranges and slices directly, or reference immutable source buffers through the application's established model. Keep malformed input or engine failure distinct from a valid result awaiting decisions.

A resolution operation must identify the current result and region, validate that relationship, and accept only the choices the contract allows. These might be a named alternative or replacement text. An explicit empty replacement is a decision; it must not be confused with a missing decision. When partial resolution is supported, preserve the other unresolved regions and the earlier accepted choices.

Changing an input, matching policy, or relevant correspondence makes old region choices potentially stale. Recompute or use an established reconciliation operation before applying them to the new result. Do not silently give an old choice the identity of a new region. Use the project's revision or identity mechanism; no particular digest, serialization, or region-key format is inherent to three-way merging.

Derive completion status from the actual unresolved regions and valid decisions. Retain the relationship between original alternatives and the chosen text needed for review. Rendering markers, hiding a conflict panel, or choosing an empty string must not independently mark a result complete.

## Carry the result through its real consumer

Connect the component to the requested review, save, reload, or export path. That path must use the same validated result and decisions, preserve unresolved status, and enforce its accepted completion rule. A workflow may allow saving an explicitly incomplete draft; it must not present that draft as a clean merged document. Check source currency at the boundary the application supports, without claiming that a pre-write check prevents all concurrent edits.

Verify the decisions most consequential to the actual contract, with expected content or state derived independently of the implementation:

- Unchanged or one-sided inputs, matching edits, and independent changes produce the expected complete text
- A genuine collision exposes truthful source alternatives; repeated content and relevant insertion/deletion boundaries follow the chosen correspondence and grouping policy
- Explicit resolution, including an empty choice when supported, updates only its intended region; changed inputs reject or explicitly reconcile stale results and decisions
- The real consumer preserves incomplete status, then uses the resolved output correctly. For a save workflow, inspect the saved content and its intended presentation or reader, and check the promised behavior of an unresolved save against an existing output

Select representation checks such as final newlines or normalized text from the supported domain. For a maintenance fix, retain a distinguishing failing case and a nearby working case. Do not assert one engine's hunk count when the contract permits other coherent groupings. Exercise partial choices, asynchronous ownership, or recovery only when those behaviors are part of the feature.

Deliver the requested component or configuration, its caller integration and concise usage, the material policy choices, and the checks actually performed. State relevant limits, including unsupported representations, merge size, or unavailable consumer checks. A separate evidence bundle, history system, global transaction, or semantic merger is not a default deliverable.
