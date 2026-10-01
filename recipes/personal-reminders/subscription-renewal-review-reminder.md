---
id: subscription-renewal-review-reminder
title: "A Reminder Before Subscription Renewal"
summary: "Schedule a neutral pre-renewal decision prompt without analyzing spending or changing the subscription."
category: personal-reminders
level: beginner
timebox_minutes: 20
capabilities: ["scheduling", "files"]
tags: ["subscription", "renewal", "decision"]
status: recipe-not-run
---

# A Reminder Before Subscription Renewal

Schedule a neutral pre-renewal decision prompt without analyzing spending or changing the subscription.

## Scenario

A user wants time to review a trial before its stated renewal date. The task is deliberately narrow: preserve the date evidence and deliver one timely decision prompt. Whether to keep or cancel remains a separate decision.

## Inputs to prepare

- A neutral subscription label and sanitized renewal or trial-end evidence
- The deadline for making a change, if different from the renewal date
- Desired decision lead time and local allowed notification hours
- IANA timezone and notification destination
- Any matching reminder already in place

## Copy this prompt into dot

```text
dot, set one decision reminder for [SUBSCRIPTION LABEL] before the renewal shown in [SANITIZED RENEWAL EVIDENCE]. The renewal is [DATE AND TIME WITH SOURCE TIMEZONE], and the latest stated change deadline is [DEADLINE OR UNKNOWN]. I want [LEAD TIME] to decide. Notify me at [DESTINATION] in [IANA TIMEZONE], within [ALLOWED HOURS].

Use the earlier confirmed action deadline when calculating the warning. If the source gives only a date or does not establish a cancellation cutoff, say so and ask which conservative reminder time to use; do not invent the provider's rules. Include the label, evidenced date and a neutral instruction to review my choice. Do not analyze my spending, cancel, renew, change a plan, open an account or make any payment.

Verify supported one-shot scheduling and destination access. Check for an existing reminder for this subscription and renewal cycle, then create or update the intended single reminder without duplication. Its start is the agreed warning instant and its stop is its one delivery. Verify the saved local time, timezone, destination and message. If the useful warning window is already past, ask what I want next instead of acting immediately. Return setup evidence or a clearly unscheduled reminder draft.
```

## Iterate with a purpose

### 1. Update a changed renewal date

```text
The provider now shows [NEW DATE] in [SANITIZED EVIDENCE]. Recalculate and update the existing reminder for this cycle; preserve the distinction between renewal and change deadline.
```

### 2. Shorten the decision prompt

```text
Make the reminder fit one short notification containing the subscription label, the confirmed date and a neutral review action. Exclude prices and account identifiers.
```

### 3. Close this renewal cycle

```text
I have made my decision for this cycle. Locate any remaining reminder for it and obtain any required confirmation to remove it; do not change the subscription.
```

## Expected deliverables

- A renewal and action-deadline evidence summary
- The calculated decision-reminder timestamp
- Neutral notification text with no implied cancellation decision
- Verified one-shot setup or an unscheduled fallback

## Acceptance checks

- A confirmed earlier change deadline takes priority over the renewal date
- A date-only source is not silently interpreted as midnight
- A past warning window triggers a user choice
- Repeated setup leaves one reminder for the same renewal cycle
- No subscription status, payment method or plan is changed

## Access, privacy and stop conditions

- Only sanitized renewal details are needed; account and payment information stay out of prompts
- This guide covers a reminder rather than budgeting or subscription recommendations
- Stop before any provider action or uncertain deadline assumption

## Two possible extensions

- Add a separately approved reminder for the following renewal cycle
- Create a private evidence checklist for finding renewal dates
