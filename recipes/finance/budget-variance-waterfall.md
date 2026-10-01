---
id: budget-variance-waterfall
title: "Budget Variance Waterfall"
summary: "Explain the gap between a fictional spending plan and actual totals with a reconciled category waterfall."
category: finance
level: beginner
timebox_minutes: 40
capabilities: ["files"]
tags: ["budget-variance", "visualization", "reconciliation"]
status: recipe-not-run
---

# Budget Variance Waterfall

Explain the gap between a fictional spending plan and actual totals with a reconciled category waterfall.

## Scenario

A project club planned a modest monthly budget, but its actual total is higher. Members need to see which categories explain the difference without blaming people or mistaking refunds for new income.

## Inputs to prepare

- Synthetic budget and actual amounts by category for one period
- A definition of spending signs, refunds, transfers and split purchases
- The reporting currency and rounding rule
- A small list of categories requiring separate visibility

## Copy this prompt into dot

```text
dot, explain the variance between [SYNTHETIC BUDGET] and [SANITIZED ACTUAL TOTALS] for [PERIOD]. Produce a readable category table and a waterfall chart from planned spending to actual spending, using [CURRENCY] and [ROUNDING RULE]. Keep this a read-only explanation; do not inspect bank accounts, change budgets in external apps or recommend investments.

Confirm the sign convention first. Define positive variance as actual spending minus planned spending, and label whether a higher number means overspending. Separate transfers, refunds and uncategorized entries before calculating. Do not guess missing categories or infer motives from a transaction label. Record any mapping decisions in a small audit table.

Show each category's planned amount, actual amount, absolute variance and share of total variance when that share is meaningful. Avoid misleading percentages where the planned amount or total variance is zero. Reconcile all steps in the chart to the same totals as the table. Check a refund, an unbudgeted category and exactly offsetting over- and underspending. Return the artifacts, an explanation of the largest arithmetic drivers and any unresolved classification choices. Use fictional labels and keep the result private.
```

## Iterate with a purpose

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

## Expected deliverables

- A category-level variance table
- A waterfall chart with a text equivalent
- An input-to-category mapping log
- A reconciliation and edge-case report

## Acceptance checks

- Planned total plus all category variances equals actual total
- The chart and table use the same sign convention
- Transfers do not become spending by default
- A refund reduces spending consistently with the documented rule
- A zero budget does not produce an infinite percentage
- Offsetting variances remain visible even when the net gap is zero

## Access, privacy and stop conditions

- Provide fictional or sanitized totals rather than identifiable statements
- Ask when a transfer or reimbursement cannot be classified from supplied evidence
- Do not share the chart with club members or change connected records without separate authorization

## Two possible extensions

- Compare two periods after agreeing on a stable category map
- Create a plain-language legend for recurring budget reports
