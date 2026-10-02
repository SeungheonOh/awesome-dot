---
name: subscription-cost-inventory
description: "Reconcile a sanitized subscription list into monthly and annual cost views with uncertainty and duplicate checks."
---

# Subscription Cost Inventory

Reconcile a sanitized subscription list into monthly and annual cost views with uncertainty and duplicate checks.

## When to use

Use this when recurring charges, memberships and trials are scattered across records and the user needs one reviewable picture. Work from their authorized list or bounded source access, distinguishing a monthly equivalent from the amount actually due next month.

## Required inputs

- A sanitized list of subscriptions, prices, billing intervals and next renewal dates, with evidenced calendar anchors and provider recurrence rules where supplied
- User-provided trial end dates and cancellation or refund terms
- A currency and a fixed as-of date
- Optional user-supplied usage notes without individual activity logs

## Workflow

1. **Fix the inventory boundary.** Confirm the as-of timestamp, timezone, reporting currency and the exact twelve-month window, preferably with an inclusive start and exclusive end. Accept supplied records or the specifically authorized source. Retrieve only the relevant subscription terms and minimize account identifiers; do not require a new integration when a small export is sufficient. Give each subscription a stable identifier so similarly named products, separate seats and duplicate records can be distinguished without exposing account details.

2. **Normalize the supplied terms.** Record price, price currency, interval, interval multiplier, next charge date, calendar anchor, provider recurrence rule, trial end, known post-trial price, status, tax treatment and source. The anchor means the billing day/month and cycle phase required by that rule, not necessarily a historical signup date. An explicit ongoing monthly day-31 rule with a compatible next occurrence can suffice. Keep the next occurrence separate from that anchor and rule: a supplied February 28 charge alone does not establish whether later billing falls on the 28th, 29th, 30th or 31st. Mark missing anchors or rules unknown rather than deriving them from the next date. Preserve the difference between unknown, explicitly free and already prepaid. Flag a renewal date before the as-of date for clarification; do not infer that payment occurred or that the subscription was canceled. Capture supplied notice periods and refund restrictions without interpreting their legal effect.

3. **Separate run-rate from cash timing.** For an annual price A, monthly equivalent is A/12; for a monthly price M, annual run-rate is 12 × M. A charge every k months has annual run-rate equal to charge × 12/k. If annualizing weekly or daily prices, label the chosen year-length convention and approximation. These figures compare rates only; they are never substituted for dated upcoming charges.

4. **Expand the actual charge calendar.** Generate recurrence dates only from a supplied anchor and provider rule within the window, beginning with the supplied next occurrence. Check that the next charge agrees with that anchor, interval and rule. If they disagree, retain the supplied date as conflicted, report the source conflict and stop later projections until resolved; do not silently replace it. If the anchor or rule is unavailable, preserve the known next charge but leave subsequent dates unresolved, so the period total is incomplete. Apply month-end or leap-day handling only when explicitly supplied or clarified; original-day clamping is not a universal merchant policy. Stop a series at a supplied end date. A free trial with unknown future pricing should create an unknown-charge event, not a zero charge or an invented forecast. Keep currencies separate unless the user supplies a dated conversion rule.

5. **Review duplicates and verify totals.** Identify possible duplicates using label, plan, interval and renewal date, but retain them until the user resolves identity. Sum dated charges independently by subscription and by month; both paths must equal the same complete known period subtotal. Check an annual renewal, a twelve-month boundary event, an unknown trial conversion and a leap-day recurrence. Explain why the calendar total can differ from annualized run-rate due to partial periods or timing.

6. **Return an actionable inventory.** Provide the normalized register, run-rate table, dated charge calendar, unresolved-price list and duplicate candidates with check outcomes. Identify which totals are incomplete and which supplied terms need review first. Describe hypothetical reductions as modeled differences only. Create the requested inventory, including a usable worksheet if appropriate, and verify any save to the already authorized destination. Keep source services unchanged: do not cancel, renew, contact providers, expand account access, claim achieved savings or recommend investments. Any subsequent service change needs its own instruction.

### Keep arithmetic exact until presentation

Parse supplied decimal prices without first converting them to binary floating point. Use the currency's defined minor-unit scale or an appropriate decimal representation; do not assume every currency has two decimal places. Reject excess precision or apply only the rounding rule the task explicitly permits.

Keep normalized rates as rational amounts until the currency subtotal is complete. Rounding each annual charge's monthly equivalent before adding them can change the total. Round the aggregate once for display, state the rounding convention, and preserve exact supplied charge amounts in the dated calendar. Currency conversion and changing tax assumptions are separate transformations requiring their own supplied rules.

As a synthetic arithmetic check, twelve annual charges of 0.01 in a two-decimal currency sum to 0.12 annually and 0.01 per month. Rounding each individual 0.01/12 monthly equivalent to cents first would incorrectly produce a zero subtotal. This is a comparison-rate calculation, not a prediction of twelve monthly charges.

Reconcile the known calendar subtotal in two independent ways: sum events by subscription, and group them by calendar month and currency. Count unknown-price events separately. A zero known subtotal with unresolved prices or dates must remain explicitly incomplete. Preserve a supplied next charge that conflicts with an inactive status as a review conflict rather than silently erasing either record.

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
- A clipped next charge retains its separately supplied original anchor; missing rules and conflicting dates remain unresolved
- The calendar period total reconciles to its individual charges
- Hypothetical savings are labeled as unachieved

## Stop and ask

- Use sanitized labels without login details or payment data
- Missing renewal rules or material prices may block a precise calendar
- Cancellation, renewal changes and provider contact require a separate request and authorization

## Worked example

[Inspect a fictional inventory where annualized cost differs from upcoming charges](WORKED-EXAMPLE.md), including an unknown trial price, duplicate-record question and repeatable recurrence checks.

## Example request

```text
dot, build a subscription cost inventory from [SANITIZED SUBSCRIPTION LIST] as of [DATE] in [TIMEZONE]. Use [CURRENCY] and distinguish actual upcoming charges from normalized monthly and annual equivalents. This is a read-only budgeting review. Use only supplied records or the named authorized source. Do not cancel services, contact providers or change renewal settings.

For each item, record the supplied price, interval, next renewal, original calendar anchor, provider recurrence rule, trial end, source and any known cancellation or refund restriction. Keep the anchor and rule separate from the next renewal date. Preserve a known next charge when its recurrence is unknown, leaving later dates unresolved; flag a next date that conflicts with the supplied anchor or rule instead of correcting it silently. Label missing information as unknown. Convert annual prices to monthly equivalents for comparison, but never use those equivalents as the predicted next charge. Flag probable duplicates for review without merging them automatically, and keep optional usage notes separate from judgments about value.

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

## Executed local checks

A bounded calendar-and-money calculator exercised explicit original-day clamping with 93 independently enumerated calendars covering anchor days 1–31 at monthly, quarterly and annual intervals in a leap year. Separate cases covered missing anchors, conflicting next dates, a past next charge, an unknown trial conversion amount, explicit zero prices, retained duplicate candidates and separate currencies.

The twelve-small-annual-charges example above and calendar subtotal reconciliation passed using exact minor-unit arithmetic. Simulated-interface checks kept unknown amounts visible and disabled stale exports after edits. These checks used fictional records; they did not verify any provider's terms, actual payment, tax treatment, account status or real-browser presentation.
