---
id: sinking-fund-goal-planner
title: "Sinking-Fund Goal Planner"
summary: "Calculate illustrative contributions toward dated expenses while exposing shortfalls, overlapping goals and rounding effects."
category: finance
level: beginner
timebox_minutes: 30
capabilities: ["files"]
tags: ["sinking-funds", "goal-planning", "arithmetic"]
status: recipe-not-run
---

# Sinking-Fund Goal Planner

Calculate illustrative contributions toward dated expenses while exposing shortfalls, overlapping goals and rounding effects.

## Scenario

A fictional household wants to prepare for an annual membership, appliance replacement and a school-free community trip. The question is how the dates and contribution intervals interact, not which account to use.

## Inputs to prepare

- Fictional goals with target costs, due dates and existing earmarked amounts
- A start date, contribution frequency and end-of-period convention
- A user-chosen total contribution limit and currency
- A choice about whether to assume zero interest and fixed costs

## Copy this prompt into dot

```text
dot, make a sinking-fund planner for [FICTIONAL GOALS] using [TARGET COSTS], [DUE DATES], [EXISTING AMOUNTS] and [START DATE]. Use [CONTRIBUTION FREQUENCY], [CURRENCY] and my total contribution limit of [LIMIT]. This is educational budgeting with synthetic or sanitized data. Do not open accounts, transfer funds, choose products or recommend investments.

Assume zero interest and fixed target costs unless I supply another explicit arithmetic assumption. Count contribution dates before each deadline using a clearly stated beginning- or end-of-period convention. Calculate the remaining amount and illustrative equal contribution for each goal. Show exact calculated values separately from rounded display values, and place any rounding adjustment in the last contribution.

Combine goals into a dated schedule so overlapping contributions can be compared with my stated limit. If the limit is exceeded, show the size and timing of the gap and ask which user-controlled goal assumption to change; do not choose priorities for me. Test a goal already funded, a deadline before the next contribution date and an unfunded goal with no remaining periods. Return the schedule, formulas, assumptions and check results. Keep outputs private and clearly label them as scenarios rather than promises of affordability.
```

## Iterate with a purpose

### 1. Compare two contribution rhythms

```text
Recalculate weekly and monthly schedules using the same start date and deadlines. Explain the difference caused by actual contribution counts.
```

### 2. Add a target-cost range

```text
Replace one fixed target with my supplied low and high costs. Show the resulting contribution range without inventing inflation forecasts.
```

### 3. Apply my chosen priority

```text
Using the goal priority order I provide, illustrate a contribution allocation within the stated limit and identify goals that still miss their target.
```

## Expected deliverables

- A goal-by-goal contribution calculation
- A combined dated contribution schedule
- A visible contribution-limit gap summary
- A formula and edge-case check sheet

## Acceptance checks

- Each goal uses the actual count of eligible contribution dates
- Existing earmarked amounts are subtracted only once
- A fully funded goal requires zero additional contributions
- A deadline with no remaining contribution date yields a clear unresolved gap
- Rounded payments reconcile after the final adjustment
- Conflicting goals are flagged without silently changing their priority

## Access, privacy and stop conditions

- Use only synthetic goals or remove personal identifiers from supplied inputs
- A missing or impossible deadline requires clarification rather than an invented schedule
- No account choice, automatic transfer or external commitment is authorized

## Two possible extensions

- Create a printable manual progress tracker
- Compare user-selected deadline changes without changing the original plan
