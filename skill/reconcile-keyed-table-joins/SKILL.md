---
name: reconcile-keyed-table-joins
description: "Plan and verify a join between two authorized tables using explicit key semantics, preserved duplicate multiplicity, unmatched-record lineage and bounded output expansion."
---

# Reconcile a Keyed Join before Using Its Output

## When to use

Use this when a user or agent needs to combine two bounded tables without losing rows, silently collapsing duplicate keys or confusing missing matches with empty source values. This is a local data-preparation task. It does not establish real-world entity identity, perform fuzzy matching, deduplicate records, upload an import or change a source service.

For a service-specific create/update import, use that service’s documented identity and import rules instead of treating this join as an operation plan. For general cleanup, keep unrelated value conversions outside the join.

## Required inputs

- Two authorized tables with source identities, selected row/column scope and parse rules
- The left/right key columns and join type: inner, left outer or full outer
- The key-comparison policy, including whitespace, case, Unicode, leading zeros and missing keys
- Duplicate treatment and the output row/byte budget
- Output format, destination and fields that should not be repeated

Inspect supplied data before asking for unavailable details. Do not assume a name column is a unique client identifier or that numeric-looking IDs should become numbers. If the matching policy is unknown, compare candidate policies privately and explain which matches change rather than silently picking the most convenient result.

## Workflow

### 1. Preserve sources and parse logical records

Record source identity and revision or byte digest when available. Keep the original inputs unchanged. Parse CSV with quoting, escaped quotes and embedded newlines; a logical record ordinal may span several physical lines. Assign source lineage separately from the business key.

Validate consistent record widths and bounded input size. Preserve duplicate or blank header positions with an explicit naming map; never lose a column because a dictionary reused its name. Keep every source cell as text unless a separate authorized conversion specifies otherwise.

If parsing fails, hold that interpretation rather than discarding malformed rows to make the join complete. Independent inspection of the other table can still finish. A filtered or partial source is not proof that unmatched entities do not exist elsewhere.

### 2. Define key equality separately from retained values

Write the comparison rule before indexing. Exact text, edge trimming, lowercasing and Unicode normalization are different policies. Lowercasing is not full linguistic case folding; a match after normalization is not evidence of the same real-world entity.

Preserve original cell values in the output. Use a separate comparison key for approved normalization. Keep `001` distinct from `1` unless an explicit identity rule equates them. Decide whether blank keys may match; a conservative review can keep blank/whitespace-only keys unmatched, but state that decision rather than assuming SQL or spreadsheet defaults.

Do not infer which duplicate is newest or authoritative from row order, completeness or a convenient timestamp. A join request alone does not authorize collapsing repeats.

### 3. Predict multiplicity before materializing rows

Index all source occurrences by comparison key, retaining their record IDs. For each matching key k with Lk left records and Rk right records, an ordinary many-to-many join produces Lk×Rk pairs. Sum those products before generating the result.

Count matched source records separately from matched pairs. Two left records matching two right records produce four output pairs but only two matched records on each side. Report duplicate-key groups, unmatched records and the expected output size for the chosen join type.

For inner join, output contains matching pairs only. A left join adds each unmatched left record once. A full outer join also adds each unmatched right record once. If predicted rows or bytes exceed the declared budget, stop expansion and return the counts and offending key groups; do not truncate silently or create a memory-heavy Cartesian product first.

### 4. Materialize with source lineage

Produce each intended pair once in a declared stable order, such as left source order followed by right occurrence order. For unmatched outer rows, retain a genuine missing-source marker independently of empty cells that existed in a source record.

Keep left and right columns distinguishable, using side/position metadata or clear prefixes. Retain left and right logical record IDs for every output row. A row with no source contribution should have a null lineage marker, not a fabricated record number.

Preserve an exception register of unmatched record IDs even for an inner join where those rows do not appear in the result. Do not describe an inner result as complete coverage of both sources without its excluded-record accounting.

### 5. Reconcile and review meaning

Verify the result count against the preflight formula and compare source-record pairs with an independent bounded enumeration on small fixtures. Check that every outer unmatched record appears exactly once and that no blank-key pair was created contrary to policy.

Spot-check normalized matches, duplicate expansions and preserved raw values. Ask the owner to resolve an unexpected many-to-many relationship if the business task required one-to-one identity. The arithmetic can be correct while the chosen key is inappropriate.

Invalidate an old result if either input or matching policy changes. A delayed file read must not overwrite a newer edit, and an export must correspond to the currently reviewed inputs rather than an earlier preview.

### 6. Export without hiding format losses

Choose a format that preserves the intended distinctions. JSON can retain null for a missing source row and empty string for a present empty cell. CSV normally renders both as blank, so disclose that loss and provide lineage separately when needed.

Treat formula-like CSV text as data while parsing. For a spreadsheet-facing review export, use a text-safe format or an explicitly selected escape policy. Prefixing an apostrophe changes the exported cell; do not silently use that representation as a machine-import value. Keep the original values in the preserved sources or lossless output.

Reopen the saved output and check row counts, column order, lineage and selected edge values. Do not upload the result or apply it to a service unless that destination and action are independently authorized.

## Deliverables

- Source and comparison-policy record
- Preflight counts: matched pairs, matched source rows, unmatched rows and duplicate groups
- The bounded joined output with distinct left/right columns and source-record lineage
- An unmatched/ambiguous-key review list and exact reconciliation result
- Export-format limitations and any unresolved business-identity decision

## Worked example

These are fictional records; blank means an empty key, not the literal word “blank.” The policy is exact text equality, with blank keys never matching.

| Left data record | Key | Label |
| --- | --- | --- |
| L1 | A1 | North |
| L2 | A1 | North backup |
| L3 | B2 | South |
| L4 | blank | Unknown |
| L5 | C3 | Coast |

| Right data record | Key | Request |
| --- | --- | --- |
| R1 | A1 | T1 |
| R2 | A1 | T2 |
| R3 | B2 | T3 |
| R4 | D4 | T4 |
| R5 | blank | No owner |

A1 produces four pairs: L1–R1, L1–R2, L2–R1 and L2–R2. B2 produces L3–R3. Thus there are five matching pairs but only three matched source records on each side. L4/L5 and R4/R5 are unmatched.

The inner join has 5 rows; the left join has 7; the full outer join has 9. The two blank-key records remain separate unmatched rows in the full result. Collapsing A1 to one left or right representative would change the supplied multiplicity and is not authorized by this join request.

For CSV lineage that counts the header as record 1, these data-record labels map to logical records 2 through 6 on each side. The worked counts and pairs were executed locally and compared with an independent nested-loop reference across 300 bounded join cases. This checks the join semantics, not whether A1 is a good identity key for a real client database.

## Stop and ask

- Hold materialization when the result exceeds the agreed row/byte budget
- Ask about an unexpected duplicate relationship when the task requires one-to-one matching
- Keep missing-key records visible; do not infer their identities from nearby rows
- Ask before collapsing duplicates, changing source values, uploading or applying service changes

## Example request

“Join these two exports on their supplied account IDs using exact text equality. Keep blank IDs unmatched and preserve every duplicate occurrence. Before materializing, show the expected row expansion; then return a full outer result with source-record lineage and a list of unmatched records. Preserve both originals and do not upload anything.”
