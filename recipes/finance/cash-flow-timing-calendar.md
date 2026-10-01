---
id: cash-flow-timing-calendar
title: "Cash-Flow Timing Calendar"
summary: "Map a fictional month of income and bills to show when a positive monthly total can still hide a cash shortfall."
category: finance
level: beginner
timebox_minutes: 30
capabilities: ["files"]
tags: ["cash-flow", "calendar", "budgeting"]
status: recipe-not-run
---

# Cash-Flow Timing Calendar

Map a fictional month of income and bills to show when a positive monthly total can still hide a cash shortfall.

## Scenario

A fictional household receives two paychecks but most bills arrive before the second one. A monthly budget looks comfortable, yet it does not explain the lowest balance between paydays.

## Inputs to prepare

- A synthetic opening balance and dated income entries
- A sanitized bill list with due dates, amounts and any timing ranges
- The planning month, currency, timezone and chosen warning threshold
- A preferred readable calendar or worksheet format

## Copy this prompt into dot

```text
dot, build a cash-flow timing calendar for [MONTH] in [TIMEZONE] using [SYNTHETIC OPENING BALANCE], [DATED INCOME] and [SANITIZED BILLS]. Use [CURRENCY] throughout. This is a read-only budgeting exercise; do not access accounts, move money, change payment dates or arrange payments.

First distinguish due dates from expected cash-movement dates. Ask about any ambiguity that could change the lowest balance. Otherwise label assumptions, including the ordering of income and bills on the same day. Show a daily opening balance, inflows, outflows and closing balance, plus a compact calendar highlighting days below [WARNING THRESHOLD]. Preserve a separate list of uncertain amounts or dates rather than making them look exact.

Reconcile the final balance to opening balance plus total income minus total spending. Test a late paycheck, a bill crossing the month boundary and a same-day deposit and debit. Present these as scenarios, not predictions. Identify the earliest possible shortfall and the assumptions that cause it, without choosing financial actions for me. Return the calendar, arithmetic checks and a short list of questions to resolve. Keep all outputs private and omit identifiers from the working files.
```

## Iterate with a purpose

### 1. Stress the payday assumption

```text
Recalculate with one paycheck arriving three days later. Show only the changed balance days and explain whether the warning threshold is crossed.
```

### 2. Make timing uncertainty visible

```text
Replace uncertain bill dates with earliest and latest dates, and show a bounded range for the lowest balance without assigning probabilities.
```

### 3. Prepare a reusable month

```text
Create a blank copy with clearly marked input cells and a checklist for rolling the calendar into another month without carrying stale dates.
```

## Expected deliverables

- A daily cash-flow table and matching calendar view
- A list of date, ordering and amount assumptions
- A reconciliation and three scenario check results
- A concise summary of the earliest possible shortfall

## Acceptance checks

- Every dated entry appears exactly once in the totals
- The closing balance reconciles to the stated opening balance and net movement
- Same-day ordering is explicit rather than hidden
- A delayed paycheck changes the correct days without changing its amount
- An item outside the month is excluded or carried forward visibly
- No scenario is described as a guaranteed future balance

## Access, privacy and stop conditions

- Use synthetic or sanitized records without account numbers or credentials
- Stop for a user decision if ambiguous dates materially change the shortfall finding
- Any real payment, bank interaction or new sharing is outside this exercise

## Two possible extensions

- Add a separate next-month view to reveal bills straddling the boundary
- Create a printable weekly checklist for manually updating expected dates
