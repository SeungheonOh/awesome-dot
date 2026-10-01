---
id: savings-goal-arithmetic-lab
title: "Savings Goal Arithmetic Lab"
summary: "Explore how contribution amount and target date change a fictional savings goal under explicit interest assumptions."
category: finance
level: beginner
timebox_minutes: 30
capabilities: ["files"]
tags: ["savings-goals", "arithmetic", "scenarios"]
status: recipe-not-run
---

# Savings Goal Arithmetic Lab

Explore how contribution amount and target date change a fictional savings goal under explicit interest assumptions.

## Scenario

A fictional learner wants to understand why doubling a contribution changes the time to a fixed goal. They need a transparent arithmetic exercise without product suggestions or promised returns.

## Inputs to prepare

- A fictional starting amount and target amount
- Two or three hypothetical contribution amounts and their frequency
- A start date, currency and contribution timing convention
- A zero-interest baseline and any optional user-supplied hypothetical rate

## Copy this prompt into dot

```text
dot, build an educational savings-goal calculator for [FICTIONAL STARTING AMOUNT], [TARGET AMOUNT] and [CONTRIBUTION OPTIONS] beginning [START DATE]. Use [CURRENCY] and [CONTRIBUTION FREQUENCY]. Keep this a read-only arithmetic exercise with synthetic data. Do not recommend investments, savings products or personal allocations, and do not open accounts or move money.

Start with a zero-interest baseline. For each contribution option, show the number of full contribution periods needed, the illustrative target date and the final contribution required to avoid overshooting. State whether contributions occur at the beginning or end of a period. If I supply [HYPOTHETICAL RATE], put that calculation in a separate scenario with its compounding convention and exclusions; do not present it as an available or guaranteed return.

Show the formulas and a few worked rows so I can inspect the arithmetic. Test a goal already reached, a zero contribution with an unmet goal and a final partial contribution. Distinguish nominal target arithmetic from purchasing power, taxes, fees and uncertain future circumstances that are outside the model. Return the calculator or table, an assumption card and actual check results, clearly marking any unrun tests. Keep the outputs private and ask before adding any real-world product research.
```

## Iterate with a purpose

### 1. Reverse the calculation

```text
Using my chosen target date, calculate the illustrative contribution needed under the same timing convention and show how you count periods.
```

### 2. Compare timing conventions

```text
Show beginning-of-period and end-of-period versions side by side, explaining exactly which dates or interest calculations differ.
```

### 3. Explain rounding to a learner

```text
Walk through one synthetic case where the final payment is smaller, keeping display rounding separate from internal arithmetic.
```

## Expected deliverables

- A contribution-versus-time comparison table or calculator
- A zero-interest worked example
- An assumption card covering timing and exclusions
- A report on three boundary cases

## Acceptance checks

- The baseline uses zero interest and is clearly identified
- An already reached target requires no further contribution
- Zero contributions toward an unmet goal do not generate a finite completion date
- The final partial contribution reconciles exactly to the target
- Any hypothetical-rate case states compounding and contribution timing
- The output contains no promise of return or personalized product recommendation

## Access, privacy and stop conditions

- Use fictional amounts rather than revealing account balances
- Clarify a target date that precedes the starting date
- Real-world product selection and financial transactions are outside scope

## Two possible extensions

- Add a user-specified target-cost range
- Turn the worked example into a short arithmetic lesson
