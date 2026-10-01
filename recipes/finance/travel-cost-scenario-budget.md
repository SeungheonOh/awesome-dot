---
id: travel-cost-scenario-budget
title: "Travel Cost Scenario Budget"
summary: "Compare a fictional trip across clearly bounded cost scenarios while separating per-person, shared and uncertain expenses."
category: finance
level: beginner
timebox_minutes: 40
capabilities: ["files"]
tags: ["travel-budget", "scenarios", "shared-costs"]
status: recipe-not-run
---

# Travel Cost Scenario Budget

Compare a fictional trip across clearly bounded cost scenarios while separating per-person, shared and uncertain expenses.

## Scenario

A fictional group is deciding whether a weekend plan fits a budget discussion. Shared lodging, per-person tickets and uncertain local transport make a single total misleading.

## Inputs to prepare

- A fictional itinerary, traveler count and number of nights
- Synthetic or sanitized price inputs with dates, currencies and units
- Low, base and high assumptions chosen by the user
- A reporting currency and any dated exchange-rate assumptions supplied by the user

## Copy this prompt into dot

```text
dot, build a read-only cost scenario budget for [FICTIONAL TRIP] with [TRAVELER COUNT] travelers and [NIGHTS] nights. Use [SUPPLIED PRICE INPUTS] and report in [CURRENCY]. Do not book travel, send personal details, purchase anything or recommend financial products. Use synthetic or sanitized data, and do not claim supplied prices are currently available.

Separate shared costs, per-person costs and per-night costs before multiplying. Preserve original currencies beside converted amounts, using only [SUPPLIED RATE AND DATE]. If a needed rate or fee is missing, mark the relevant total incomplete instead of guessing. Distinguish taxes and mandatory charges from optional spending when the inputs allow it.

Create [LOW], [BASE] and [HIGH] scenarios from my explicit assumptions, not implied probabilities. Show the group total, per-person illustration and a subtotal excluding unknown costs. Check one traveler, an unevenly shared room, a trip crossing a billing night and a zero-cost optional activity. Reconcile line items to totals and explain rounding in shared allocations. Return the scenario table, a compact list of cost drivers and questions to settle before any later booking. Describe contingency amounts as user-chosen assumptions rather than guarantees, and keep the work private.
```

## Iterate with a purpose

### 1. Change only the group size

```text
Recalculate for the traveler counts I supply. Keep fixed costs fixed and show where room capacity or ticket rules require a new assumption.
```

### 2. Model an uneven split

```text
Use my stated split rules to allocate shared costs. Verify allocations sum to the group total and display any rounding adjustment.
```

### 3. Build the missing-cost checklist

```text
List each unknown mandatory charge, the source needed to resolve it and which scenario totals remain incomplete until then.
```

## Expected deliverables

- A low, base and high trip-cost table
- A line-item model with units and currency provenance
- An illustrative shared-cost allocation
- An uncertainty checklist and reconciliation results

## Acceptance checks

- Per-person, per-night and fixed costs have explicit units
- Shared costs are not multiplied by traveler count twice
- Converted amounts retain the original currency and dated rate
- Unknown mandatory charges make totals visibly incomplete
- One-traveler and uneven-split cases reconcile correctly
- No price is described as bookable without a later live availability check

## Access, privacy and stop conditions

- Use synthetic travelers and omit identity or payment information
- Ask for a missing currency rate or allocation rule that materially changes totals
- Booking, contacting providers and spending money are separate tasks requiring authorization

## Two possible extensions

- Add a user-supplied alternate itinerary
- Create a post-trip comparison using sanitized actual totals
