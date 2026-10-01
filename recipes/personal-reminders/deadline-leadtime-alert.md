---
id: deadline-leadtime-alert
title: "One Deadline, One Useful Warning"
summary: "Schedule a single warning early enough to act on a deadline, with a verified local time and no repeat notifications."
category: personal-reminders
level: beginner
timebox_minutes: 15
capabilities: ["scheduling"]
tags: ["deadline", "lead-time", "one-shot"]
status: recipe-not-run
---

# One Deadline, One Useful Warning

Schedule a single warning early enough to act on a deadline, with a verified local time and no repeat notifications.

## Scenario

A community workshop application closes on a Friday evening. A reminder at the deadline would be useless: the applicant needs two evenings to gather material. This guide turns the deadline and preparation lead time into one bounded notification.

## Inputs to prepare

- A sanitized task label and exact deadline, including timezone
- The preparation lead time and whether it uses calendar days or elapsed hours
- The notification destination and permitted local delivery hours
- Whether a matching reminder already exists

## Copy this prompt into dot

```text
dot, set up one preparation reminder for [TASK LABEL]. The deadline is [DEADLINE DATE AND TIME] in [IANA TIMEZONE]. I need [LEAD TIME] before it, measured in [CALENDAR DAYS OR ELAPSED HOURS]. Deliver the reminder to [DESTINATION] and include [SHORT NEXT ACTION]. This is a single notification, not a recurring check-in.

First verify that supported scheduling and delivery to that destination are available. Check for an existing reminder with the same task, deadline and audience so that repeating this request does not create duplicates. Calculate the proposed reminder time, show its local timezone and UTC offset, and resolve any ambiguity around daylight saving or an unavailable local hour. If the calculated time has passed or falls outside [ALLOWED HOURS], ask me which future time to use rather than sending a surprise immediate alert.

Create the one-shot schedule only after the required details are settled. Verify the saved time, message and destination from the returned schedule details. Its start is the agreed reminder instant; its stop is completion of that one delivery. Report setup evidence and any unverified delivery behavior. If scheduling is unavailable, return the exact reminder text and timestamp as an unscheduled draft.
```

## Iterate with a purpose

### 1. Recalculate a changed deadline

```text
The deadline moved to [NEW DEADLINE]. Find the original reminder, recompute its lead time, and update that reminder after resolving any timezone ambiguity. Do not add a second one.
```

### 2. Make the warning actionable

```text
Rewrite the reminder into a task label, deadline and one action I can start in five minutes. Keep the saved time and destination unchanged.
```

### 3. Check completion before delivery

```text
I completed [TASK LABEL]. Locate its pending one-shot reminder and ask for any approval needed to remove it; confirm the result rather than assuming it stopped.
```

## Expected deliverables

- A calculated reminder timestamp with local timezone and UTC offset
- The exact notification text and destination
- A verified one-shot schedule record, or a clearly unscheduled draft

## Acceptance checks

- The difference between deadline and reminder matches the selected lead-time unit
- A daylight-saving boundary is calculated using the named timezone
- A reminder time in the past leads to a decision instead of an immediate send
- Only one matching pending reminder remains after a repeated request
- The saved schedule has one occurrence and the intended destination

## Access, privacy and stop conditions

- Use task labels rather than private application material in notifications
- Access to a destination must be verified before claiming setup
- Stop for a past or ambiguous time that changes when the warning will arrive

## Two possible extensions

- Add a separate final-day reminder only if the user requests it
- Create a reusable lead-time worksheet for several unrelated deadlines
