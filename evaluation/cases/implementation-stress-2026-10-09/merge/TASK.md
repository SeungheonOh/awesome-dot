> Public contract projection. Behavior and mathematical requirements are unchanged. Delivery/evaluation process instructions, where present, are omitted. See provenance.json for source hashes and changes. This package is UNRUN.

# Merge review comments from two editors without losing source correspondence

Implement the pure Python 3.12 function `merge_edits(base, left, right)` in `solution.py` using only the standard library. Submit executable source, not a precomputed answer. Inputs and nested values must not be mutated. No network, filesystem, subprocess, or external-service work is requested.

An application retains a shared base document and exact edit lists from two editors. The edit lists are already known; do not compute a new diff. Repeated text is intentional and must not relocate an edit to a different equal-looking occurrence.

Each edit is `{"id": str, "start": int, "end": int, "text": str}` and replaces the half-open slice `base[start:end]`. Insertion has `start == end`; deletion has empty text. Coordinates are Python Unicode code-point indexes, NOT UTF-8 bytes, UTF-16 code units, lines, or grapheme clusters. Inputs contain Unicode scalar values (no lone surrogates). Keep every code point exactly: do not normalize NFC/NFD, line endings, combining marks, variation selectors, or zero-width joiners. CR and LF are separate preserved characters, even if an edit falls between them; no final newline is added. This contract does not require grapheme segmentation.

Within each branch, IDs are unique ASCII identifiers of at most 40 characters, edits have strictly increasing starts, and each prior end is <= the next start. Ranges satisfy `0 <= start <= end <= len(base)`. Thus no same-branch overlapping replacements or duplicate insertion positions occur, but a replacement may end where a later insertion or replacement begins. The same ID may be used independently in opposite branches. All inputs are valid; invalid-input validation is not graded.

## Interaction and grouping policy

First remove every exact no-op edit whose text equals `base[start:end]`, including empty insertions. The remaining supplied edits carry their original IDs unchanged.

Two edits interact only if they belong to opposite branches and one of these is true:
- Both consume nonempty ranges, and those half-open ranges have strictly positive overlap
- Exactly one is an insertion at p, and the other consumes [s,e) with `s < p < e`
- Both are insertions at the same position

Insertions at either endpoint of a replacement are compatible with that replacement. Touching nonempty replacements are compatible. Form connected components under this relation, including isolated edits as singleton components. Transitive closure is required: a component may contain several edits from either branch even though same-branch edits never directly interact.

A component's base span is `[s,e]`, the min start and max end of its members. For each side separately, project that component by copying `base[s:e]` and applying only that side's member edits in original base coordinates. Include unchanged text between member edits. A side with no component members contributes the unchanged base slice. Do not include an independent insertion at an endpoint in this projection.

Classify the complete projected alternatives in this order:
1. If left == base slice and right == base slice: kind `base`, chosen text is the base slice
2. If left == right: kind `both`, chosen text is that common alternative
3. If left == base slice: kind `right`, chosen text is the right alternative
4. If right == base slice: kind `left`, chosen text is the left alternative
5. Otherwise: kind `conflict`, chosen text is null

This is a textual conflict policy, not a judgment that combined wording is semantically appropriate.

## Output and ordering

Return `{"segments": [...], "text": str or null, "conflict_ids": [...]}`.

Each segment has exactly these fields:
`{"span": [s,e], "kind": "base|left|right|both|conflict", "base": str, "left": str, "right": str, "left_ids": [str,...], "right_ids": [str,...], "text": str or null, "conflict_id": str or null}`.

Emit each interaction component as its own segment, even when adjacent components have the same kind. Order components by `(start, end)`; zero-width components at a boundary come before a nonempty component beginning there and after any nonempty component ending there. Between component spans, emit exactly one segment for each nonempty untouched base gap, with kind `base`, all three alternatives and text equal to that slice, empty ID lists, and conflict_id null. Never emit an empty untouched-gap segment. For unchanged nonempty input there is one base segment; for unchanged empty input there are no segments. Do not otherwise combine or split components.

For a component, `left_ids` and `right_ids` list only member edit IDs in their original branch order. Its base/left/right fields contain the exact projected alternatives. Assign conflicts IDs `C0`, `C1`, ... in emitted order, using no IDs for compatible components. `conflict_ids` lists those IDs in order. If any conflicts exist, top-level text is null; otherwise it is the concatenation of all segment texts. Conflict markers are not part of this API. There is no separate resolution API or persistent state to implement.

Example: base `abc`, left inserts `L` at [1,1], right replaces [1,2] with `R`. They are compatible endpoint edits. Output segments are untouched `a` at [0,1], left insertion `L` at [1,1], right replacement `R` at [1,2], untouched `c` at [2,3]. Top-level text is `aLRc`, conflict_ids is empty. For the component alternatives: insertion has base/right empty and left `L`; replacement has base/left `b` and right `R`.

Example: base `abcd`, left replaces [0,2] with `X`, right replaces [1,3] with `Y`. They form one conflict at [0,3], with base `abc`, left `Xc`, right `aY`, and IDs from their respective edits. A final untouched segment [3,4] contains `d`. Top-level text is null and conflict_ids is `["C0"]`.

## Finite tested domain

Base length <= 6000 code points, at most 180 edits per branch, and sum of replacement-text lengths across both branches <= 12000 code points. No IDs contain unexpected syntax; ASCII letters/digits/hyphen/underscore only. Tests compose ordinary one-sided/unchanged cases, equal or unequal collisions, transitive components, insertion/deletion endpoints, effective equality after projecting multiple edits, ignored no-ops, repeated lines, astral symbols, combining sequences, ZWJ sequences, CRLF, and absent final newlines. Sizes are deliberately bounded; neither a full diff algorithm nor full Unicode grapheme rules are required.

Each call must finish within 5 seconds and the frozen suite within 120 seconds on an ordinary Python worker with 512 MiB available memory. These limits only exclude nontermination or clearly unsuitable algorithms at the disclosed sizes. Report unavailable execution as unassessed. Object-key order is irrelevant; segment, provenance, and conflict orders are part of the explicit API. Any internal implementation that meets this contract is accepted.
