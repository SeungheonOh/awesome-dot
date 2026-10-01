---
id: rotating-chores-bounded-series
title: "A Bounded Rotation of Household Chores"
summary: "Turn a chore rotation into a finite, inspectable series of personal reminders with fair rollover behavior."
category: personal-reminders
level: intermediate
timebox_minutes: 30
capabilities: ["scheduling", "files"]
tags: ["household", "rotation", "bounded-series"]
status: recipe-not-run
---

# A Bounded Rotation of Household Chores

Turn a chore rotation into a finite, inspectable series of personal reminders with fair rollover behavior.

## Scenario

Roommates want to rotate common-area chores for a six-week trial. The organizer needs a clear sequence and personal prompts to coordinate it, without the assistant assuming permission to message every household member.

## Inputs to prepare

- Chore list and sanitized participant labels in rotation order
- Start date, final date or fixed number of cycles, and recurrence interval
- The organizer’s notification destination and timezone
- Known away dates and whether missed turns skip or shift the rotation
- A rule for weeks containing two chores or an uneven final cycle

## Copy this prompt into dot

```text
dot, plan a chore rotation for [CHORE LIST] across [PARTICIPANT LABELS] in the listed order. The trial begins [START DATE], repeats [CADENCE] at [LOCAL TIME] in [IANA TIMEZONE], and stops after [COUNT OF CYCLES OR END DATE]. Send all reminders only to me at [DESTINATION]; listing another person as owner does not authorize contacting them.

Create the rotation table first, including [AWAY DATES] and the agreed missed-turn rule [SKIP OR SHIFT]. Flag conflicts and show whether workload remains balanced, especially in an incomplete final cycle. Do not assume an unacknowledged reminder means a chore was completed. Include a short completion checklist in each notification.

Verify actual scheduling support, date bounds and destination access. Check for a matching household trial before creating anything. If conditional rotation cannot be automated, use a fixed agreed sequence and clearly explain the manual adjustment step. Verify the saved occurrences or recurrence end condition, including the final allowed reminder. Do not schedule indefinite repeats or catch-up bursts. On repeated setup, reconcile with the existing series rather than duplicating it. Return the rotation, schedule evidence and an unscheduled version if setup is unavailable.
```

## Iterate with a purpose

### 1. Rebalance an absence

```text
[PARTICIPANT] will be away on [DATES]. Propose the smallest fair change to the remaining turns, preserving completed turns and the original end date.
```

### 2. Audit the trial workload

```text
Count assigned turns per participant and distinguish scheduled, confirmed complete and unknown. Explain any difference without inferring completion from silence.
```

### 3. Renew with a decision

```text
Summarize the trial and propose the next [NUMBER] cycles. Do not extend the schedule until I explicitly choose a new end condition.
```

## Expected deliverables

- A finite rotation table showing owner, chore and date
- A conflict and workload-balance summary
- Reminder text with simple completion criteria
- Verified schedule bounds and a manual fallback for unsupported rotation logic

## Acceptance checks

- Each scheduled turn has exactly one stated owner
- The final incomplete cycle is visible in the fairness summary
- An away date follows the selected skip-or-shift rule
- Silence is recorded as unknown rather than completed
- There are no reminders beyond the trial end
- Only the organizer receives notifications unless separately authorized

## Access, privacy and stop conditions

- Household labels should not expose private availability in a public artifact
- Do not contact participants or edit shared calendars without authorization
- Stop for a rotation conflict that would override a participant’s stated availability

## Two possible extensions

- Add an approved shared completion sheet with explicit recipients
- Compare two rotation rules before beginning a new trial
