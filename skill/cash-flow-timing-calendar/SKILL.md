---
name: cash-flow-timing-calendar
description: "Map dated income and bills to show when a positive monthly total can still hide a cash shortfall."
---

# Cash-Flow Timing Calendar

Map dated income and bills to show when a positive monthly total can still hide a cash shortfall.

## When to use

Use this when income and bills arrive on different dates and a monthly total hides what happens between them. Work from authorized records with identifying details minimized. The worked assumptions are scenarios, not predictions or instructions to move money.

## Required inputs

- An authorized balance for each sanitized account label, its timestamp, ledger/available/other basis, and known or unresolved pending amounts already reflected
- Dated income and a sanitized bill list, each assigned to an account and currency, with amounts and any timing ranges
- The planning month, currency, timezone and chosen warning threshold
- A preferred readable calendar or worksheet format

## Workflow

1. **Pin down the opening boundary and basis.** Confirm the first and last included local dates, timezone, currency precision and warning threshold. Record each account's balance basis (ledger, available or explicitly defined other); these are not interchangeable. Establish a balance at the horizon opening boundary, before the included movements, or bridge an older snapshot to that boundary with a separate, reconciled register of intervening movements. A later snapshot does not establish balances on earlier quiet days without the necessary reconciliation evidence. Record which movements the snapshot already includes, resolving timestamp ties. Do not discard pre-horizon movements while retaining an older balance. An unknown amount, uncertain snapshot coverage or an incomplete bridge leaves the boundary balance unresolved. Reject impossible dates and ambiguous signs or currencies.

2. **Create an event register.** Give every income or bill a stable identifier, sanitized account label, currency, amount, direction, contractual due date, expected cash-movement date, earliest and latest possible dates, and evidence or supplied assumption. Count cash movements rather than invoice creation. Link pending holds and settlements to the same underlying movement; record the signed amount already reflected and the remaining effect on the chosen balance basis. A settlement replacing an already reflected hold must not be deducted twice. Only net a hold release with settlement when their linkage and timing are supplied or evidenced; otherwise retain separate timing cases or mark the effect unresolved. Do not invent bank posting behavior. Distinguish pre-horizon bridge entries from other excluded boundary entries, and never count an identifier in both bridge and horizon. Missing amounts, account assignments or reflected status remain unknown, not zero; note which account's balances become incomplete and when.

3. **Construct the baseline in order, per account.** For each account and currency, calculate closing balance = opening balance plus remaining inflow effects minus remaining outflow effects, with the following day's opening equal to the prior closing. Show full movements and any reflected-amount adjustments separately. Include days without activity. Apply the confirmed same-day ordering. If only dates are known, show deposit-first and debit-first cases where the order could change an intraday shortfall. Distinguish the minimum daily closing balance from the minimum after an individual event. Flag each account before any optional aggregate; cash in another account does not prevent its shortfall. Aggregate only compatible currencies, bases and time boundaries, disclose incomplete components, and never imply an unmodeled transfer.

4. **Handle uncertainty with separate cases.** Make a dated baseline, a delayed-paycheck case and a boundary-crossing bill case. Preserve identifiers and amounts when changing dates so each movement appears once. If date windows are wide, evaluate explicit earliest/latest combinations, keeping dependent events together. Call these illustrative scenarios; do not claim their extrema are exhaustive bounds unless every allowed combination was evaluated or a justified bounding method was used.

5. **Verify balances and flags.** For each account and currency, reconcile the snapshot plus bridge to the horizon opening, then that opening plus included remaining effects to the final balance. Check a quiet day, consecutive debits, a same-day deposit/debit pair, a reflected hold, an older snapshot and a month-end crossing. Define whether a balance equal to the threshold triggers a warning. Confirm that changing timing inside the horizon changes intermediate balances but not the ending balance when inclusion and reflected-amount assumptions stay the same.

6. **Deliver the calendar and decisions.** Return the per-account daily tables, compact date view, event register, balance-basis and bridge reconciliations, scenario differences and any optional aggregate. Identify the earliest modeled threshold breach and account with the assumptions responsible, without prescribing borrowing or moving funds. Ask when balance basis, reflected status, an incomplete bridge, an uncertain large bill or same-day ordering could reverse the finding. Missing material inputs justify an incomplete scenario, never a precise prediction. Read only the records or account source authorized for this task. Produce the requested calendar or worksheet, save to an already authorized destination if specified, and inspect the saved output; these already-authorized reads and saves need no repeated permission. Payments, transfers and changes to financial records are outside this budgeting workflow.

## Deliverables

- Per-account daily cash-flow tables and matching calendar views, with any aggregate clearly secondary
- A list of balance-basis, reflected-amount, bridge, date, ordering and amount assumptions
- A reconciliation and three scenario check results
- A concise summary of the earliest possible shortfall

## Verification

- Every entry has an account and currency; bridge and horizon entries do not overlap
- Every movement affects its chosen balance basis exactly once, including pending/settlement reconciliation
- Each closing balance reconciles to its horizon-boundary opening and remaining net movement
- An older snapshot has a complete bridge; otherwise affected balances are incomplete
- An aggregate never hides an individual account's shortfall or combines incompatible currencies/bases
- Same-day ordering is explicit rather than hidden
- A delayed paycheck changes the correct days without changing its amount
- An item outside the month is excluded or carried forward visibly
- No scenario is described as a guaranteed future balance

## Stop and ask

- Use authorized records with identifying details minimized; omit account numbers and credentials from outputs
- Stop for a user decision if ambiguous dates materially change the shortfall finding
- Payments, transfers and financial account changes are outside this analysis; new sharing needs its own authorization

## Worked example

[Inspect a fictional cash calendar with a delayed receipt and a month-boundary bill](WORKED-EXAMPLE.md). The repeatable calculation distinguishes daily closing balances from within-day shortfalls.

## Example request

```text
dot, build a cash-flow timing calendar for [MONTH] in [TIMEZONE] using [ACCOUNT-LABELED BALANCES, BASIS, TIMESTAMPS AND REFLECTED PENDING AMOUNTS], [DATED INCOME] and [SANITIZED BILLS]. Use [CURRENCY] throughout. This is a read-only budgeting exercise; use only supplied records or the explicitly authorized source; do not move money, change payment dates or arrange payments.

First establish each account's horizon-boundary balance, bridging older snapshots separately and reconciling holds or pending amounts already reflected. Distinguish due dates from expected cash-movement dates. Ask about any ambiguity that could change the lowest balance. Otherwise label assumptions, including the ordering of income and bills on the same day. Show daily opening balances, inflows, outflows, reflected-amount adjustments and closing balances per account, plus a compact calendar highlighting days below [WARNING THRESHOLD]. Preserve a separate list of uncertain amounts or dates rather than making them look exact. Flag account shortfalls before any compatible aggregate.

Reconcile each snapshot through any bridge to the horizon opening, then reconcile the final balance using only remaining effects on its stated basis. Test a late paycheck, a bill crossing the month boundary and a same-day deposit and debit. Present these as scenarios, not predictions. Identify the earliest possible shortfall and the assumptions that cause it, without choosing financial actions for me. Return the calendar, arithmetic checks and a short list of questions to resolve. Keep all outputs private and omit personal identifiers from the working files, retaining only sanitized account labels.
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
