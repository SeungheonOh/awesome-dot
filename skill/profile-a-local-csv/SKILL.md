---
name: profile-a-local-csv
description: "Inspect a supplied CSV for structural errors, missing values, candidate types and distributions while preserving source values and local processing."
---

# Profile an authorized CSV locally

## When to use

A dataset needs an initial quality review before analysis, charting or import into another system.

## Required inputs

- The authorized file or text and its encoding/header/separator expectations
- Size bounds and the missing-value convention
- Requested profile scope and any fields that must be excluded from the output

## Workflow

1. Preserve the source and parse quoted records with a CSV parser that handles escaped quotes and embedded newlines. A physical line is not always a logical record. Reject malformed quotes or inconsistent widths with a useful locator.
2. Confirm or disclose separator detection. Preserve duplicate/blank headers as distinct columns using an explicit naming map; never drop them silently.
3. Count missing cells under the agreed convention. Keep numeric zero, literal NA labels, percentages and currency strings distinct. Numeric-looking identifiers may be categorical.
4. Infer numeric columns only under a strict finite-number rule and report that rule. Calculate summaries excluding missing values with stated denominators. Guard overflow in sums/ranges and constant or underflowing histogram widths.
5. Produce a bounded preview and distributions. Category values may be private even when presented only as counts; minimize exported content to the authorized scope. Do not upload a table merely because a parser service is convenient.

### Produce a profile with a denominator

Keep physical byte identity separate from logical records after parsing. Report header handling, data-row count, excluded records and normalization explicitly. Decide whether a repeated row is meaningful data or a duplicate candidate; do not deduplicate during profiling.

For each summary, include included-value count and missing-value count. Distinct-value counts use an explicit exact-text or normalized-text rule. A column’s inferred numeric shape does not override a supplied semantic role such as postal code or client ID. Keep the output bounded so a top-category list does not disclose a large private roster unnecessarily.

## Output

A profile containing source identity, parse decisions, row/column counts, missingness, candidate types, anomalies and scoped summaries, with the original unchanged.

## Verification and limits

Reconcile histogram totals to included records. Spot-check quoted multiline cells, duplicate headers, zeros and empty values. Mark columns whose semantics remain unknown rather than guessing.

## Missing-input handling

If separator or encoding is ambiguous, present the bounded alternatives that change the parse. If a malformed record prevents reliable column alignment, report its logical record location and stop statistics for that parse rather than silently dropping it.

## Worked example

The fictional file has headers id,amount,note and three rows: (001, 0,"a,b"), (002,empty,"line one\nline two"), and (003, 4,NA). The second note is one quoted multiline field, not two records. The user identifies id as an identifier and defines only blank/whitespace cells as missing.

The profile has 3 data rows and 3 columns. amount has 2 numeric values, 1 missing value, mean 2, median 2 and range 0–4. Zero contributes to every numeric measure. The note value NA remains text, and the embedded comma/newline remain inside their original fields. IDs keep their leading zeros and categorical meaning.

The handoff includes the parser decisions and this reconciliation. It does not upload the rows, replace the empty amount with zero, or claim the table has only three physical lines.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
