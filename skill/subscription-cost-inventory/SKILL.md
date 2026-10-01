---
name: subscription-cost-inventory
description: "Reconcile a sanitized subscription list into monthly and annual cost views with uncertainty and duplicate checks."
---

# Subscription Cost Inventory

Reconcile a sanitized subscription list into monthly and annual cost views with uncertainty and duplicate checks.

## When to use

A fictional studio keeps a small list of recurring tools, memberships and trials. It needs an inventory that distinguishes a monthly equivalent from the amount actually due next month.

## Required inputs

- A sanitized list of subscriptions, prices, billing intervals and renewal dates
- User-provided trial end dates and cancellation or refund terms
- A currency and a fixed as-of date
- Optional user-supplied usage notes without individual activity logs

## Workflow

1. **Fix the inventory boundary.** Confirm the as-of timestamp, timezone, reporting currency and the exact twelve-month window, preferably with an inclusive start and exclusive end. Accept sanitized service labels and supplied records only. Give each subscription a stable identifier so similarly named products, separate seats and duplicate records can be distinguished without exposing account details.

2. **Normalize the supplied terms.** Record price, price currency, interval, interval multiplier, next charge date, trial end, known post-trial price, status, tax treatment and source. Preserve the difference between unknown, explicitly free and already prepaid. Flag a renewal date before the as-of date for clarification; do not infer that payment occurred or that the subscription was canceled. Capture supplied notice periods and refund restrictions without interpreting their legal effect.

3. **Separate run-rate from cash timing.** For an annual price A, monthly equivalent is A/12; for a monthly price M, annual run-rate is 12 × M. A charge every k months has annual run-rate equal to charge × 12/k. If annualizing weekly or daily prices, label the chosen year-length convention and approximation. These figures compare rates only; they are never substituted for dated upcoming charges.

4. **Expand the actual charge calendar.** Generate recurrence dates from each supplied rule within the window. Apply an explicit month-end or leap-day policy; ask when February handling changes an actual charge date. Stop a series at a supplied end date. A free trial with unknown future pricing should create an unknown-charge event, not a zero charge or an invented forecast. Keep currencies separate unless the user supplies a dated conversion rule.

5. **Review duplicates and verify totals.** Identify possible duplicates using label, plan, interval and renewal date, but retain them until the user resolves identity. Sum dated charges independently by subscription and by month; both paths must equal the same complete known period subtotal. Check an annual renewal, a twelve-month boundary event, an unknown trial conversion and a leap-day recurrence. Explain why the calendar total can differ from annualized run-rate due to partial periods or timing.

6. **Return an actionable inventory.** Provide the normalized register, run-rate table, dated charge calendar, unresolved-price list and duplicate candidates with check outcomes. Identify which totals are incomplete and which supplied terms need review first. Describe hypothetical reductions as modeled differences only. Keep this read-only and educational: do not cancel, renew, contact providers, inspect payment accounts, claim achieved savings or recommend investments. Any subsequent service change needs its own instruction.

## Deliverables

- A sanitized subscription inventory with source and uncertainty fields
- Separate normalized-cost and upcoming-charge views
- A twelve-month charge calendar
- A duplicate review list and arithmetic check report

## Verification

- Annual prices are not misrepresented as monthly cash charges
- Unknown trial prices are not silently treated as zero
- Possible duplicates stay separate until resolved
- Leap-day recurrence follows an explicit supplied or clarified convention
- The calendar period total reconciles to its individual charges
- Hypothetical savings are labeled as unachieved

## Stop and ask

- Use sanitized labels without login details or payment data
- Missing renewal rules or material prices may block a precise calendar
- Cancellation, renewal changes and provider contact require a separate request and authorization

## Example request

```text
dot, build a subscription cost inventory from [SANITIZED SUBSCRIPTION LIST] as of [DATE] in [TIMEZONE]. Use [CURRENCY] and distinguish actual upcoming charges from normalized monthly and annual equivalents. This is a read-only budgeting review. Do not connect financial accounts, cancel services, contact providers or change renewal settings.

For each item, record the supplied price, interval, next renewal, trial end, source and any known cancellation or refund restriction. Label missing information as unknown. Convert annual prices to monthly equivalents for comparison, but never use those equivalents as the predicted next charge. Flag probable duplicates for review without merging them automatically, and keep optional usage notes separate from judgments about value.

Produce a twelve-month charge calendar using only dates and recurrence rules I supplied, plus a cost summary and a list of questions requiring my decision. Test an annual renewal, a free trial with an unknown future price, a leap-day recurrence and two similarly named services. Reconcile calendar charges to the period total and explain partial-period assumptions. Avoid claiming any savings until a separately authorized change is actually confirmed. Return the inventory and check results privately, using fictional labels instead of account identifiers.
```

## Focused follow-ups

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

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
