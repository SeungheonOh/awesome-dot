---
id: small-project-break-even
title: "Small Project Break-Even Map"
summary: "Calculate the unit volume needed to cover a fictional small project under explicit cost and capacity assumptions."
category: finance
level: intermediate
timebox_minutes: 45
capabilities: ["files"]
tags: ["break-even", "unit-economics", "project-budget"]
status: recipe-not-run
---

# Small Project Break-Even Map

Calculate the unit volume needed to cover a fictional small project under explicit cost and capacity assumptions.

## Scenario

A community workshop is considering a fictional print run. Fixed setup costs, per-unit materials and limited capacity need a simple model before anyone mistakes revenue for surplus.

## Inputs to prepare

- Synthetic fixed costs, unit price and variable cost per unit
- A bounded sales-volume range and production capacity
- Known batch sizes, unsold-unit assumptions and fee rules
- A currency and user-selected alternative price or cost scenarios

## Copy this prompt into dot

```text
dot, create a break-even map for [FICTIONAL SMALL PROJECT] using [FIXED COSTS], [UNIT PRICE], [VARIABLE COSTS], [CAPACITY] and [CURRENCY]. This is read-only project-budget education using synthetic inputs, not investment, tax or business-launch advice. Do not make purchases, create accounts, accept orders or commit money.

First define what one unit means and distinguish units produced from units sold. State which costs are fixed, per unit produced, per unit sold or triggered by a batch. Build the smallest model that matches those rules. Show revenue, total costs and modeled surplus or deficit across [VOLUME RANGE]. Calculate an algebraic break-even point only when the assumptions support it, then round to feasible whole units and check against capacity.

Test zero sales, a nonpositive contribution margin and a calculated break-even volume beyond capacity. If inventory costs or step changes make the simple formula invalid, use an explicit volume table and explain the limitation. Compare my [ALTERNATIVE ASSUMPTIONS] one at a time without forecasting demand or assigning probabilities. Return the table, a chart if useful, formulas and reconciliation checks. Highlight excluded costs and avoid calling a positive modeled surplus guaranteed profit. Keep all outputs private.
```

## Iterate with a purpose

### 1. Separate produced and sold units

```text
Use my supplied unsold-inventory assumption to show how producing a full batch changes cash costs even when only part of it sells.
```

### 2. Add a stepped cost

```text
Incorporate the batch or capacity charge I provide. Recheck the first feasible nonnegative result around each cost step.
```

### 3. Test one assumption at a time

```text
Create a sensitivity table for my chosen unit-price and variable-cost changes, clearly separating each case from a demand forecast.
```

## Expected deliverables

- A volume-by-volume revenue and cost table
- A feasible-unit break-even calculation or explanation of why none exists
- A compact sensitivity comparison
- An assumptions, exclusions and check record

## Acceptance checks

- Produced and sold units are separately defined when they differ
- Zero sales still incurs applicable fixed and production costs
- A nonpositive contribution margin does not produce a misleading finite break-even claim
- Whole-unit rounding is checked by evaluating the adjacent volumes
- A break-even point above capacity is flagged as infeasible under current assumptions
- Batch charges appear at the correct thresholds
- Modeled surplus is not presented as guaranteed profit or demand

## Access, privacy and stop conditions

- Use fictional project data or sanitize commercial details
- Ask for missing cost behavior if it changes which model is valid
- No purchasing, selling, account creation or financial commitment is authorized

## Two possible extensions

- Create a printable worksheet for a project-planning workshop
- Compare two user-supplied production batch sizes
