---
name: nested-export-workbook
description: "Convert supplied nested app-data JSON into a usable XLSX with separate related tables, exact identifiers, explicit missing/null/empty states and saved-file reconciliation."
---

# Turn a Nested Export into a Review Workbook

Make an actual XLSX that someone can open, filter and trace back to an already-supplied JSON export. Preserve the exported records, their relationships, their order and their value states. Deliver the workbook with a compact mapping and reconciliation report.

Use this when the obstacle is nested machine data. Cleaning an existing spreadsheet belongs to [spreadsheet cleanup](../spreadsheet-cleanup-reconciliation/SKILL.md). Determining whether an export contains everything in an account belongs to [account export audit](../account-export-audit/SKILL.md). This conversion establishes fidelity to selected supplied bytes; it does not establish account completeness or test a live import.

## Establish the selection

Inspect the supplied input before asking questions. Resolve only decisions that change the workbook:

- Which file, export version and root collection should be included? If several snapshots exist, select one explicitly instead of silently combining them
- What will the reader need to filter or review? Are original IDs, nested notes, repeated child occurrences or omitted fields material?
- Is the deliverable a local XLSX, and which available application will be used to open it? Is any source field too large for one cell or beyond spreadsheet numeric precision?
- If dates, decimals or domain categories need conversion, what evidenced rules determine their meaning? Without those rules, retain exact text or an explicitly documented reversible encoding

Record source filename, bytes, SHA-256, supplied format/export metadata, selected root and exclusions. Preserve the original unchanged. A filename and digest identify the selected bytes; they do not authenticate the provider. Write into a new output directory. Do not run bundled code, open stored links, enable macros, refresh connections or upload private exports to make the conversion easier.

## Validate before writing

Use a strict parser that detects duplicate object keys before a normal dictionary can overwrite one. Reject malformed JSON, unsupported encodings, non-finite numbers and structures the adapter cannot preserve. Set bounds for file size, depth, record count, cell text and expansion appropriate to the actual input. Report the exact held field or structural limitation; do not omit troublesome records and call the result complete.

Inspect the schema instead of assuming a familiar extension implies a known layout. Inventory object fields, arrays and scalar types, including explicit nulls and omitted optional fields. Preserve unknown fields in a documented evidence table or hold until the mapping includes them. Do not relabel a real export as the fictional schema used below.

Treat IDs as strings. A long numeric JSON token may already exceed spreadsheet precision even when its printed digits look like an ID. Keep its exact token under an approved text mapping, or hold that conversion. Do not round, coerce null to zero, infer dates, trim text, normalize statuses or invent the meaning of an omitted field.

## Design related tables

Use one parent sheet and one child sheet for each independent child collection. A child row carries its parent source pointer and its original array index. Keep a native business ID separately from the source occurrence key. Repeated IDs and repeated identical values remain separate occurrences unless a different, explicit task authorizes consolidation.

Never flatten two sibling arrays by joining every child to every other child. Two items and two labels produce two item rows plus two label rows, not four item-label combinations. An empty child array produces no child rows, while the parent retains `EMPTY_ARRAY` and count zero. Null and absent relationships also produce no child rows, with distinct states and blank counts.

For every actual JSON node, preserve a JSON Pointer, parent pointer, key or array index, traversal ordinal and type/state. The root pointer is the empty string. Escape `~` as `~0` and `/` as `~1` inside pointer tokens. Keep source array order even when users later sort a review table; the ordinal and pointer must travel with the row.

Scalar fields need paired value/state evidence:

| Source observation | Review value | State | Reconstruction |
| --- | --- | --- | --- |
| `0` | numeric 0 | INTEGER | Restore zero |
| `""` | blank-looking cell | EMPTY_STRING | Restore supplied empty string |
| `null` | blank-looking cell | NULL | Restore explicit null |
| Field absent | blank-looking cell | MISSING | Do not add the field |
| `[]` | no child rows, count 0 | EMPTY_ARRAY | Restore empty array |
| Array with children | separate ordered rows | ARRAY | Attach those children in order |

A blank cell alone cannot distinguish these cases. Use nearby state columns for common review fields and a separate source-path table for full evidence. Label `MISSING` rows as observations about the declared schema, not invented source nodes. A scalar JSON token is a useful lossless text representation when a cell cannot show its original type safely: quotes around a string are encoding, not part of the decoded value. Keep formatting/escape spelling differences out of byte-fidelity claims; retain the original file for exact source bytes.

## Create the usable workbook

Follow the applicable spreadsheet creation workflow and use installed tools. Keep the ordinary review tables first, with clear headers, filterable table ranges, legible IDs, fitted widths and useful frozen panes. Put source metadata and the state legend in a small instruction area or final sheet. No charts or business calculations are necessary for a data-only conversion.

Write literal source strings as text using the author's supported API. Formula-looking values such as `=1+1` must remain that exact text with no formula node or added escape character in the saved value. Number formatting alone is not proof of storage type. Reject or explicitly encode a string when the available writer would infer another type. Do not use source text to construct executable formulas, hyperlinks or connections.

The workbook is a static review copy. Explain that manually changing a source value does not update its state or lineage. Regeneration from a newly selected source is a separate, explicit operation; do not overwrite a prior review or the original export.

## Reopen, reconstruct and reconcile

Check the saved XLSX, not just the in-memory plan:

1. Compare exact parent and child occurrences, IDs, ordinals and edges to the selected source. Reconcile each child array independently, including repeated values and parents with no children
2. Compare the complete ordered source-pointer set and every scalar token/state. Reconstruct the JSON tree from the saved evidence, excluding `MISSING` observations, then compare values, types, field presence and array order
3. Check underlying string/numeric cell types, not only displayed text. Verify long IDs, zero, empty string, null, missing field, timestamp/date-like text and a formula-looking literal
4. Inspect saved formulas and package relationships. A data-only workbook should contain no formulas, macros, active external links or connections
5. Open and save a disposable copy through the available native spreadsheet engine. Re-run exact value, state and relationship checks. Render that saved consumer copy and visually inspect every sheet for scientific-notation IDs, clipping, hidden data and unreadable states

Test meaningful failures: malformed/duplicate-key JSON must be held before authoring; unsupported numeric conversion must not round; removing a child, changing a parent link, replacing zero with blank or turning a literal into a formula must fail the checker. Rehash the source after the run. State the exact engine and checks performed. A successful export or one renderer does not establish behavior in Excel, a cloud spreadsheet or every viewer.

## Deliver or hold

Return the actual workbook, concise mapping/reconciliation report, source identity and verification limits. Include precise row counts and a preview of the review tables. Provide a portable reproduction/check path when useful.

Hold the affected conversion when the source is malformed, the schema is unsupported, a value cannot be represented reversibly, or saved-consumer checks change it. Explain the smallest evidence or mapping decision needed. If the requested application is unavailable, disclose that verification gap instead of implying compatibility. Finish when the selected input is faithfully represented and the stated consumer checks pass, or a specific unresolved decision prevents that result.

The [fictional worked example](example.md) includes the actual XLSX, source fixture, mapping report and reproducible checks. Its adapter is deliberately small and schema-specific.
