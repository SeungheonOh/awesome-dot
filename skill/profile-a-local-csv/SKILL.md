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

## Output

A profile containing source identity, parse decisions, row/column counts, missingness, candidate types, anomalies and scoped summaries, with the original unchanged.

## Verification and limits

Reconcile histogram totals to included records. Spot-check quoted multiline cells, duplicate headers, zeros and empty values. Mark columns whose semantics remain unknown rather than guessing.
