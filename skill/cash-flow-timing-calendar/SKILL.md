---
name: cash-flow-timing-calendar
description: "Map dated income and bills to show when a positive monthly total can still hide a cash shortfall."
---

# Cash-Flow Timing Calendar

Map dated income and bills to show when a positive monthly total can still hide a cash shortfall.

## When to use

Use this when income and bills arrive on different dates and a monthly total hides what happens between them. Work from authorized records with identifying details minimized. The worked assumptions are scenarios, not predictions or instructions to move money.

## Required inputs

- An authorized opening balance with its timestamp and dated income entries
- A sanitized bill list with due dates, amounts and any timing ranges
- The planning month, currency, timezone and chosen warning threshold
- A preferred readable calendar or worksheet format

## Workflow

1. **Pin down the time boundary.** Confirm the first and last included local dates, timezone, currency precision, opening balance timestamp and warning threshold. The opening amount must precede the first included cash movement. Check that already received income is not also included as a future inflow. Reject impossible dates and ask about amounts whose sign or currency is ambiguous.

2. **Create an event register.** Give every income or bill a stable identifier, amount, direction, contractual due date, expected cash-movement date, earliest and latest possible dates, and evidence or supplied assumption. Count cash movements rather than invoice creation. Keep entries outside the month in a boundary register so excluding them is visible. Missing amounts remain unknown, not zero; note which daily balances become incomplete after an unresolved event.

3. **Construct the baseline in order.** For each date, calculate closing balance = opening balance plus inflows minus outflows, with the following day's opening equal to the prior closing. Include days without activity. Apply the confirmed same-day ordering. If only dates are known, show deposit-first and debit-first cases where the order could change an intraday shortfall. Distinguish the minimum daily closing balance from the minimum after an individual event.

4. **Handle uncertainty with separate cases.** Make a dated baseline, a delayed-paycheck case and a boundary-crossing bill case. Preserve identifiers and amounts when changing dates so each movement appears once. If date windows are wide, evaluate explicit earliest/latest combinations, keeping dependent events together. Call these illustrative scenarios; do not claim their extrema are exhaustive bounds unless every allowed combination was evaluated or a justified bounding method was used.

5. **Verify balances and flags.** Recalculate the final balance directly from the opening amount and all included movements. Check a quiet day, consecutive debits, a same-day deposit/debit pair and a month-end crossing. Define whether a balance equal to the threshold triggers a warning. Confirm that changing timing inside the horizon changes intermediate balances but not the ending balance.

6. **Deliver the calendar and decisions.** Return the daily table, compact date view, event register, scenario differences and reconciliation results. Identify the earliest modeled threshold breach with the assumptions responsible, without prescribing borrowing or moving funds. Ask when the opening balance timing, an uncertain large bill or same-day ordering could reverse the finding. Missing material inputs justify an incomplete scenario, never a precise prediction. Read only the records or account source authorized for this task. Produce the requested calendar or worksheet, save to an already authorized destination if specified, and inspect the saved output. Payments, transfers and changes to financial records are outside this budgeting workflow.

## Deliverables

- A daily cash-flow table and matching calendar view
- A list of date, ordering and amount assumptions
- A reconciliation and three scenario check results
- A concise summary of the earliest possible shortfall

## Verification

- Every in-scope dated entry appears exactly once in the totals
- The closing balance reconciles to the stated opening balance and net movement
- Same-day ordering is explicit rather than hidden
- A delayed paycheck changes the correct days without changing its amount
- An item outside the month is excluded or carried forward visibly
- No scenario is described as a guaranteed future balance

## Stop and ask

- Use synthetic or sanitized records without account numbers or credentials
- Stop for a user decision if ambiguous dates materially change the shortfall finding
- Any real payment, bank interaction or new sharing is outside this exercise

## Worked example

[Inspect a fictional cash calendar with a delayed receipt and a month-boundary bill](WORKED-EXAMPLE.md). The repeatable calculation distinguishes daily closing balances from within-day shortfalls.

## Example request

```text
dot, build a cash-flow timing calendar for [MONTH] in [TIMEZONE] using [OPENING BALANCE AND TIMESTAMP], [DATED INCOME] and [SANITIZED BILLS]. Use [CURRENCY] throughout. This is a read-only budgeting exercise; use only supplied records or the explicitly authorized source; do not move money, change payment dates or arrange payments.

First distinguish due dates from expected cash-movement dates. Ask about any ambiguity that could change the lowest balance. Otherwise label assumptions, including the ordering of income and bills on the same day. Show a daily opening balance, inflows, outflows and closing balance, plus a compact calendar highlighting days below [WARNING THRESHOLD]. Preserve a separate list of uncertain amounts or dates rather than making them look exact.

Reconcile the final balance to opening balance plus total income minus total spending. Test a late paycheck, a bill crossing the month boundary and a same-day deposit and debit. Present these as scenarios, not predictions. Identify the earliest possible shortfall and the assumptions that cause it, without choosing financial actions for me. Return the calendar, arithmetic checks and a short list of questions to resolve. Keep all outputs private and omit identifiers from the working files.
```

## Focused follow-ups

### 1. Stress the payday assumption

```text
Recalculate with one paycheck arriving three days later. Show only the changed balance days and explain whether the warning threshold is crossed.
```

### 2. Make timing uncertainty visible

```text
Replace uncertain bill dates with earliest and latest dates. Evaluate all permitted combinations if feasible; otherwise label sampled cases as illustrative rather than proven bounds. Do not assign probabilities.
```

### 3. Prepare a reusable month

```text
Create a blank copy with clearly marked input cells and a checklist for rolling the calendar into another month without carrying stale dates.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
