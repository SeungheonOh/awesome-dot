---
name: budget-variance-waterfall
description: "Explain the gap between a fictional spending plan and actual totals with a reconciled category waterfall."
---

# Budget Variance Waterfall

Explain the gap between a fictional spending plan and actual totals with a reconciled category waterfall.

## When to use

A project club planned a modest monthly budget, but its actual total is higher. Members need to see which categories explain the difference without blaming people or mistaking refunds for new income.

## Required inputs

- Synthetic budget and actual amounts by category for one period
- A definition of spending signs, refunds, transfers and split purchases
- The reporting currency and rounding rule
- A small list of categories requiring separate visibility

## Workflow

1. **Establish the comparison boundary.** Confirm one reporting period, one currency, the smallest currency unit and whether amounts include applicable supplied taxes. Require planned and actual totals on the same basis. Preserve the original rows with stable identifiers; do not edit the input to make totals agree. Record whether an absent category means zero, unavailable data or an intentionally excluded item.

2. **Normalize the ledger visibly.** Build the union of planned and actual categories, including an explicit unresolved bucket. Convert the supplied signs into positive spending and negative refunds. Keep transfers outside spending unless the user supplies a different classification. Retain a mapping table with input identifier, original category, reporting category, signed amount and reason. Split purchases only from supplied allocations, and verify that each split sums to its source row. Flag duplicate identifiers without silently removing similar transactions.

3. **Calculate the bridge.** For each category use variance = actual minus plan, in currency units. Total planned spending plus the sum of signed variances must equal total actual spending. When plan is nonzero, percentage variance is variance divided by plan times 100; label negative-plan cases separately because refund budgets can invert the usual interpretation. Do not calculate a conventional percentage against a zero plan.

4. **Choose an honest presentation.** Start the waterfall at the planned total, draw each signed category change, and finish at the actual total. Use identical ordering and values in the accompanying table. If the net variance is zero or very small, omit contribution-to-net percentages and explain cancellation; show separate gross increases and reductions instead. Do not describe an arithmetic driver as a behavioral cause.

5. **Reconcile and probe boundaries.** Compare input spending totals, category totals and chart endpoints independently. Verify a negative refund, a new category with no budget, a split purchase and equal opposing variances. Retain full calculation precision and report the displayed rounding residual, if any; never hide it in an arbitrary category.

6. **Return a reviewable package.** Supply the category table, accessible waterfall or text bridge, mapping decisions and a check register with expected and observed results. List unresolved amounts and whether they prevent a complete total. Ask for classification only where it changes the interpretation; otherwise deliver the known subtotal with a clear limitation. Keep this educational and read-only: an unexplained variance does not authorize account access, record changes, blame or financial recommendations.

## Deliverables

- A category-level variance table
- A waterfall chart with a text equivalent
- An input-to-category mapping log
- A reconciliation and edge-case report

## Verification

- Planned total plus all category variances equals actual total
- The chart and table use the same sign convention
- Transfers do not become spending by default
- A refund reduces spending consistently with the documented rule
- A zero budget does not produce an infinite percentage
- Offsetting variances remain visible even when the net gap is zero

## Stop and ask

- Provide fictional or sanitized totals rather than identifiable statements
- Ask when a transfer or reimbursement cannot be classified from supplied evidence
- Do not share the chart with club members or change connected records without separate authorization

## Worked example

[Inspect a fictional flat-total budget with offsetting category changes](WORKED-EXAMPLE.md), including a repeatable arithmetic check and unresolved-transfer branch.

## Example request

```text
dot, explain the variance between [SYNTHETIC BUDGET] and [SANITIZED ACTUAL TOTALS] for [PERIOD]. Produce a readable category table and a waterfall chart from planned spending to actual spending, using [CURRENCY] and [ROUNDING RULE]. Keep this a read-only explanation; do not inspect bank accounts, change budgets in external apps or recommend investments.

Confirm the sign convention first. Define positive variance as actual spending minus planned spending, and label whether a higher number means overspending. Separate transfers, refunds and uncategorized entries before calculating. Do not guess missing categories or infer motives from a transaction label. Record any mapping decisions in a small audit table.

Show each category's planned amount, actual amount, absolute variance and share of total variance when that share is meaningful. Avoid misleading percentages where the planned amount or total variance is zero. Reconcile all steps in the chart to the same totals as the table. Check a refund, an unbudgeted category and exactly offsetting over- and underspending. Return the artifacts, an explanation of the largest arithmetic drivers and any unresolved classification choices. Use fictional labels and keep the result private.
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

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
