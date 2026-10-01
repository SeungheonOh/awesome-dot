---
id: subscription-cost-inventory
title: "Subscription Cost Inventory"
summary: "Reconcile a sanitized subscription list into monthly and annual cost views with uncertainty and duplicate checks."
category: finance
level: beginner
timebox_minutes: 35
capabilities: ["files"]
tags: ["subscriptions", "recurring-costs", "audit"]
status: recipe-not-run
---

# Subscription Cost Inventory

Reconcile a sanitized subscription list into monthly and annual cost views with uncertainty and duplicate checks.

## Scenario

A fictional studio keeps a small list of recurring tools, memberships and trials. It needs an inventory that distinguishes a monthly equivalent from the amount actually due next month.

## Inputs to prepare

- A sanitized list of subscriptions, prices, billing intervals and renewal dates
- User-provided trial end dates and cancellation or refund terms
- A currency and a fixed as-of date
- Optional user-supplied usage notes without individual activity logs

## Copy this prompt into dot

```text
dot, build a subscription cost inventory from [SANITIZED SUBSCRIPTION LIST] as of [DATE] in [TIMEZONE]. Use [CURRENCY] and distinguish actual upcoming charges from normalized monthly and annual equivalents. This is a read-only budgeting review. Do not connect financial accounts, cancel services, contact providers or change renewal settings.

For each item, record the supplied price, interval, next renewal, trial end, source and any known cancellation or refund restriction. Label missing information as unknown. Convert annual prices to monthly equivalents for comparison, but never use those equivalents as the predicted next charge. Flag probable duplicates for review without merging them automatically, and keep optional usage notes separate from judgments about value.

Produce a twelve-month charge calendar using only dates and recurrence rules I supplied, plus a cost summary and a list of questions requiring my decision. Test an annual renewal, a free trial with an unknown future price, a leap-day recurrence and two similarly named services. Reconcile calendar charges to the period total and explain partial-period assumptions. Avoid claiming any savings until a separately authorized change is actually confirmed. Return the inventory and check results privately, using fictional labels instead of account identifiers.
```

## Iterate with a purpose

### 1. Resolve the duplicate candidates

```text
Use my answers to distinguish true duplicate records from separate plans. Show which records changed and verify the total again.
```

### 2. Model my chosen changes

```text
Calculate a hypothetical cost difference for the subscriptions I name, respecting supplied notice periods and prepaid terms. Do not make any changes.
```

### 3. Create a renewal review checklist

```text
Make a manual checklist organized by upcoming renewal date, with the specific missing price or term to verify for each item.
```

## Expected deliverables

- A sanitized subscription inventory with source and uncertainty fields
- Separate normalized-cost and upcoming-charge views
- A twelve-month charge calendar
- A duplicate review list and arithmetic check report

## Acceptance checks

- Annual prices are not misrepresented as monthly cash charges
- Unknown trial prices are not silently treated as zero
- Possible duplicates stay separate until resolved
- Leap-day recurrence follows an explicit supplied or clarified convention
- The calendar period total reconciles to its individual charges
- Hypothetical savings are labeled as unachieved

## Access, privacy and stop conditions

- Use sanitized labels without login details or payment data
- Missing renewal rules or material prices may block a precise calendar
- Cancellation, renewal changes and provider contact require a separate request and authorization

## Two possible extensions

- Add a separate calendar for a second currency without mixing totals
- Create a blank quarterly review template
