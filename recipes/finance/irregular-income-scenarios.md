---
id: irregular-income-scenarios
title: "Irregular-Income Scenario Grid"
summary: "Build transparent low, middle and high income scenarios for a fictional freelancer without pretending to predict earnings."
category: finance
level: intermediate
timebox_minutes: 45
capabilities: ["files"]
tags: ["income-scenarios", "budgeting", "uncertainty"]
status: recipe-not-run
---

# Irregular-Income Scenario Grid

Build transparent low, middle and high income scenarios for a fictional freelancer without pretending to predict earnings.

## Scenario

A fictional freelancer has confirmed invoices, possible work and uneven payment dates. A single average income figure hides the difference between work being booked and cash actually arriving.

## Inputs to prepare

- Synthetic confirmed and possible receipts with expected payment windows
- A fictional list of fixed and variable outflows
- Three user-chosen income assumptions and a starting cash amount
- A horizon, currency and any user-supplied reserve amounts

## Copy this prompt into dot

```text
dot, create a scenario grid for [FICTIONAL FREELANCER] over [HORIZON] using [SYNTHETIC RECEIPTS], [OUTFLOWS] and [STARTING CASH] in [CURRENCY]. The purpose is to understand arithmetic under uncertain income, not predict earnings or give tax, credit or investment advice. Do not access financial accounts or take actions.

Separate confirmed receipts from possible work, and invoice dates from expected receipt dates. Use my [LOW], [MIDDLE] and [HIGH] assumptions exactly; do not invent probabilities or call the middle case most likely. Treat [USER-SUPPLIED RESERVE AMOUNTS] as inputs without assessing whether they satisfy any legal obligation.

For each scenario, show monthly cash in, fixed costs, variable costs, reserves and ending cash. Mark the first month below [USER-CHOSEN FLOOR], if any. Include a bridge explaining which assumptions differ between scenarios. Test zero new work, one late confirmed receipt and a receipt moved beyond the horizon. Reconcile every ending balance and keep uncertain amounts visibly approximate. Return a compact grid, formulas, assumption notes and questions whose answers would materially change the result. Keep personal identifiers out of the files and do not suggest a personal financial product or transaction.
```

## Iterate with a purpose

### 1. Separate amount and timing risk

```text
Hold total receipts constant and vary only payment timing. Show how the lowest balance changes even though total income does not.
```

### 2. Expose the controlling assumption

```text
Change each user-supplied assumption one at a time by a stated amount and rank the resulting changes in the lowest balance, without implying probability.
```

### 3. Create a manual update sheet

```text
Add an input sheet for replacing possible work with confirmed receipts, with duplicate checks so the same invoice cannot be counted twice.
```

## Expected deliverables

- A three-scenario monthly cash grid
- A bridge listing the assumptions changed in each case
- Documented formulas and horizon conventions
- A result for each requested stress case

## Acceptance checks

- Confirmed and possible receipts cannot be silently double-counted
- The scenario names do not imply likelihood
- Each monthly closing balance becomes the next opening balance
- A receipt beyond the horizon contributes no cash inside it
- The zero-new-work case is handled without dividing by zero
- Reserve inputs are not presented as tax compliance advice

## Access, privacy and stop conditions

- Use a fictional business and sanitized amounts
- Stop to clarify whether a material receipt is booked work or cash already received
- Tax obligations, borrowing decisions and account actions remain outside scope

## Two possible extensions

- Add a second planning horizon while preserving the original assumptions
- Produce an anonymized scenario summary for a user-approved audience
