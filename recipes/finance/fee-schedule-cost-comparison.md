---
id: fee-schedule-cost-comparison
title: "Fee Schedule Cost Comparison"
summary: "Compare the arithmetic of fictional service fees under explicit usage patterns without recommending a financial provider."
category: finance
level: intermediate
timebox_minutes: 45
capabilities: ["files"]
tags: ["fees", "comparison", "education"]
status: recipe-not-run
---

# Fee Schedule Cost Comparison

Compare the arithmetic of fictional service fees under explicit usage patterns without recommending a financial provider.

## Scenario

Three fictional payment services use different monthly, per-use and threshold fees. Their headline prices cannot be compared until the same usage assumptions and exclusions are applied.

## Inputs to prepare

- Fictional or sanitized fee schedules with their stated effective dates
- Two or three user-defined usage patterns
- A currency, comparison period and rule for any supplied exchange rates
- Known exclusions, minimum charges and threshold details

## Copy this prompt into dot

```text
dot, compare the costs of [FICTIONAL SERVICE FEE SCHEDULES] under [USER-DEFINED USAGE PATTERNS] for [PERIOD] in [CURRENCY]. Use only the supplied schedules and clearly identify their effective dates. This is a read-only educational cost comparison, not a recommendation about a provider, account or investment. Do not sign in, create accounts or initiate transactions.

Extract monthly charges, per-use charges, minimums, tiers, caps and waived-fee conditions into a common table. Attach each extracted rule to its supplied source location. Ask about any ambiguity that changes the math. Mark unspecified fees as unknown rather than zero, and exclude currency conversion unless I provide a rate and date.

Calculate a transparent cost breakdown for each usage pattern. Show where rankings depend on an omitted charge, a waiver assumption or a threshold boundary. Test zero usage and usage immediately below, at and above each relevant threshold. If a break-even point exists, show its equation and valid range rather than extrapolating beyond the fee rules. Return the cost matrix, calculation notes and unresolved questions. Keep inputs sanitized and do not claim that arithmetic alone establishes suitability, service quality or the best choice.
```

## Iterate with a purpose

### 1. Resolve one ambiguous fee

```text
Use the additional fee clause I supply to update only affected calculations. Preserve a before-and-after record and cite the clause location.
```

### 2. Draw the cost curves

```text
Plot total cost against a bounded usage range, marking thresholds and any crossing points. Include exact values for representative points.
```

### 3. Separate known and unknown costs

```text
Create a decision worksheet listing known costs, unknown charges and non-price questions, without selecting a provider.
```

## Expected deliverables

- A normalized fee-rule table with source locations
- A cost matrix across the supplied usage patterns
- Threshold and break-even calculations where valid
- A list of unknown fees and excluded comparison factors

## Acceptance checks

- Every fee rule links back to a supplied schedule location
- An unspecified fee remains unknown rather than becoming zero
- Zero usage includes applicable fixed charges
- Threshold inclusivity is tested at the exact boundary
- Any break-even equation respects the relevant fee tier
- The conclusion distinguishes cheapest modeled cost from suitability

## Access, privacy and stop conditions

- Remove account identifiers and confidential contract details before use
- Ask for a missing fee clause when it could reverse a cost comparison
- Live price claims require a separately scoped retrieval of current dated sources
- Provider selection, account creation and transactions are excluded

## Two possible extensions

- Add one more synthetic usage pattern
- Produce a reusable checklist for reading fee schedules
