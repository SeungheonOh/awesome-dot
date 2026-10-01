---
name: budget-variance-waterfall
description: "Explain the gap between a spending plan and actual totals with a reconciled category waterfall."
---

# Budget Variance Waterfall

Explain the gap between a spending plan and actual totals with a reconciled category waterfall.

## When to use

Use this when household, club or project spending differs from its plan and the reader needs to understand the arithmetic drivers. Work from the user’s authorized records; the included example is fictional. Do not mistake refunds for income or assign blame from transaction labels.

## Required inputs

- Authorized budget and actual amounts by category for one period; sanitized exports are sufficient
- A definition of spending signs, refunds, transfers and split purchases
- The reporting currency and rounding rule
- A small list of categories requiring separate visibility

## Workflow

1. **Establish the comparison boundary.** Confirm one reporting period, the authorized source, one currency, the smallest currency unit and whether amounts include applicable supplied taxes. Use supplied records or the explicitly authorized account source, staying within the named period and fields. Require planned and actual totals on the same basis. Preserve the original rows with stable identifiers; do not edit the input to make totals agree. Record whether an absent category means zero, unavailable data or an intentionally excluded item.

2. **Normalize the ledger visibly.** Build the union of planned and actual categories, including an explicit unresolved bucket. Convert the supplied signs into positive spending and negative refunds. Keep transfers outside spending unless the user supplies a different classification. Retain a mapping table with input identifier, original category, reporting category, signed amount and reason. Split purchases only from supplied allocations, and verify that each split sums to its source row. Flag duplicate identifiers without silently removing similar transactions.

3. **Calculate the bridge.** For each category use variance = actual minus plan, in currency units. Total planned spending plus the sum of signed variances must equal total actual spending. When plan is nonzero, percentage variance is variance divided by plan times 100; label negative-plan cases separately because refund budgets can invert the usual interpretation. Do not calculate a conventional percentage against a zero plan.

4. **Choose an honest presentation.** Start the waterfall at the planned total, draw each signed category change, and finish at the actual total. When a chart is optional or an exact text bridge is requested, list every signed movement and running amount instead; keep an unresolved endpoint symbolic rather than inventing a numerical total. Use identical ordering and values in the accompanying table. If the net variance is zero or very small, omit contribution-to-net percentages and explain cancellation; show separate gross increases and reductions instead. Do not describe an arithmetic driver as a behavioral cause.

5. **Reconcile and probe boundaries.** Compare input spending totals, category totals and chart or text-bridge endpoints independently. Verify a negative refund, a new category with no budget, a split purchase and equal opposing variances. Retain full calculation precision and report the displayed rounding residual, if any; never hide it in an arbitrary category.

6. **Return a reviewable package.** Supply the category table, accessible waterfall or text bridge, mapping decisions and a check register with expected and observed results. List unresolved amounts and whether they prevent a complete total. Ask for classification only where it changes the interpretation; otherwise deliver the known subtotal with a clear limitation. Create the requested table, document or workbook and, if a destination is already authorized, save it there and read back the result. Keep financial sources unchanged: an unexplained variance does not authorize broader account access, record changes, blame or financial recommendations.

## Deliverables

- A category-level variance table
- An accessible waterfall chart with a text equivalent, or an exact text bridge when a chart is optional
- An input-to-category mapping log
- A reconciliation and edge-case report

## Verification

- Planned total plus all category variances equals actual total
- The chart or text bridge and category table use the same sign convention
- Transfers do not become spending by default
- A refund reduces spending consistently with the documented rule
- A zero budget does not produce an infinite percentage
- Offsetting variances remain visible even when the net gap is zero

## Stop and ask

- Use only the minimum authorized records; remove unnecessary account numbers and personal identifiers
- Ask when a transfer or reimbursement cannot be classified from supplied evidence
- Do not share the chart with club members or change connected records without separate authorization

## Worked example

[Inspect a fictional flat-total budget with offsetting category changes](WORKED-EXAMPLE.md), including a repeatable arithmetic check and unresolved-transfer branch.

## Example request

```text
dot, explain the variance between [AUTHORIZED BUDGET] and [SANITIZED ACTUAL TOTALS] for [PERIOD]. Produce a readable category table and a waterfall chart from planned spending to actual spending, using [CURRENCY] and [ROUNDING RULE]. Keep this a read-only explanation; use only the supplied records or named authorized source, and do not change financial records or recommend investments.

Confirm the sign convention first. Define positive variance as actual spending minus planned spending, and label whether a higher number means overspending. Separate transfers, refunds and uncategorized entries before calculating. Do not guess missing categories or infer motives from a transaction label. Record any mapping decisions in a small audit table.

Show each category's planned amount, actual amount, signed currency variance (actual minus plan) and share of total variance when that share is meaningful. Avoid misleading percentages where the planned amount or total variance is zero. Reconcile all steps in the chart to the same totals as the table. Check a refund, an unbudgeted category and exactly offsetting over- and underspending. Return the artifacts, an explanation of the largest arithmetic drivers and any unresolved classification choices. Minimize identifying details and keep the result private unless I have authorized a specific destination and audience.
```

## Focused follow-ups

### 1. Separate timing from lasting changes

```text
Using my supplied classifications, split the variance into timing differences and other differences. Keep unclassified items visible and do not infer their causes.
```

### 2. Audit the largest category

```text
Expand the largest variance into its sanitized component entries and verify that those entries add back to the category total.
```

### 3. Improve the chart labels

```text
Revise the chart for a reader unfamiliar with waterfalls. Add start and end totals, direction labels and a text equivalent of every plotted value.
```

## Evidence status

The [synthetic rehearsal](rehearsal/result.md) includes a [fictional input packet](rehearsal/input.md) and [local verification note](rehearsal/verification.md). In this one case, integer-cent calculations and artifact readback checked a duplicate refund, split purchase, excluded transfer and missing positive amount. The result is an exact text bridge with a known subtotal and symbolic complete total. No connected account, spreadsheet application or graphical chart renderer was exercised; this is bounded evidence for one synthetic case, not end-to-end or universal certification. Report actual checks and unrun steps for each use.
