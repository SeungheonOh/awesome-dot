---
name: deadline-leadtime-alert
description: "Schedule a single warning early enough to act on a deadline, with a verified local time and no repeat notifications."
---

# One Deadline, One Useful Warning

Schedule a single warning early enough to act on a deadline, with a verified local time and no repeat notifications.

## When to use

A community workshop application closes on a Friday evening. A reminder at the deadline would be useless: the applicant needs two evenings to gather material. This guide turns the deadline and preparation lead time into one bounded notification.

## Required inputs

- A sanitized task label and exact deadline, including timezone
- The preparation lead time and whether it uses calendar days or elapsed hours
- The notification destination and permitted local delivery hours
- Whether a matching reminder already exists

## Workflow

### Intake and date model

Build a record with task label, source deadline, deadline IANA timezone, lead-time value and unit, allowed delivery hours, destination and next action. Require a positive lead time and an exact deadline or a user-selected interpretation of a date-only deadline. Keep the deadline zone separate from the user's notification zone. Record the source of each date; an inferred closing hour must never become a confirmed fact.

### Procedure

1. Inspect the available reminder service's supported create, inspect, update and cancel actions. Confirm one-shot delivery to the requested destination and whether the service accepts a named timezone or requires an absolute instant. If any essential capability is absent, produce a dated draft instead of substituting another destination.
2. Calculate the candidate warning. Subtract elapsed hours from the deadline instant; subtract calendar days in the deadline's named timezone before choosing the delivery hour. These operations can differ across daylight-saving transitions. Show both the local result and UTC offset, and use timezone-aware arithmetic rather than a fixed offset remembered from today.
3. Check the local hour against the permitted window, including windows spanning midnight. A nonexistent spring-forward time, repeated autumn hour, past warning or warning after the deadline requires a choice. Present the earliest useful future alternative without creating an immediate alert or reducing preparation time silently.
4. Search accessible pending reminders for the same task, deadline cycle and recipient. This combination defines the logical reminder identity; similar wording alone does not. Reuse an exact match. For a changed deadline, inspect the existing record and update its identifier rather than creating a replacement blindly. After an uncertain response, look up the record before retrying creation.
5. Save the agreed one-shot message with its task, deadline and concrete next action. Inspect the saved record or authoritative creation response and compare the timestamp, timezone interpretation, text, destination and single-occurrence behavior with the proposal. A successful save establishes setup, not future delivery.

### Result and stopping boundary

Return the date calculation, exact message, saved reminder reference and verification result. Include a manual calendar entry if setup is blocked. Recalculate the interval independently and test a clock-change example without sending a notification. Completion or cancellation reported before delivery means locating this same pending reminder, obtaining any required approval to stop it and verifying its final state. The workflow expires after its one occurrence; it must not restart because the user did not respond. Stop for unresolved time semantics, inaccessible saved state or conflicting duplicate records rather than claiming one reliable warning exists.

## Deliverables

- A calculated reminder timestamp with local timezone and UTC offset
- The exact notification text and destination
- A verified one-shot schedule record, or a clearly unscheduled draft

## Verification

- The difference between deadline and reminder matches the selected lead-time unit
- A daylight-saving boundary is calculated using the named timezone
- A reminder time in the past leads to a decision instead of an immediate send
- Only one matching pending reminder remains after a repeated request
- The saved schedule has one occurrence and the intended destination

## Stop and ask

- Use task labels rather than private application material in notifications
- Access to a destination must be verified before claiming setup
- Stop for a past or ambiguous time that changes when the warning will arrive

## Worked example

[Compare a calendar-day warning with an elapsed-hour warning across a clock change](WORKED-EXAMPLE.md). The repeatable check also detects repeated and skipped local hours; it does not create a reminder.

## Example request

```text
dot, set up one preparation reminder for [TASK LABEL]. The deadline is [DEADLINE DATE AND TIME] in [IANA TIMEZONE]. I need [LEAD TIME] before it, measured in [CALENDAR DAYS OR ELAPSED HOURS]. Deliver the reminder to [DESTINATION] and include [SHORT NEXT ACTION]. This is a single notification, not a recurring check-in.

First verify that supported scheduling and delivery to that destination are available. Check for an existing reminder with the same task, deadline and audience so that repeating this request does not create duplicates. Calculate the proposed reminder time, show its local timezone and UTC offset, and resolve any ambiguity around daylight saving or an unavailable local hour. If the calculated time has passed or falls outside [ALLOWED HOURS], ask me which future time to use rather than sending a surprise immediate alert.

Create the one-shot schedule only after the required details are settled. Verify the saved time, message and destination from the returned schedule details. Its start is the agreed reminder instant; its stop is completion of that one delivery. Report setup evidence and any unverified delivery behavior. If scheduling is unavailable, return the exact reminder text and timestamp as an unscheduled draft.
```

## Focused follow-ups

### 1. Recalculate a changed deadline

```text
The deadline moved to [NEW DEADLINE]. Find the original reminder, recompute its lead time, and update that reminder after resolving any timezone ambiguity. Do not add a second one.
```

### 2. Make the warning actionable

```text
Rewrite the reminder into a task label, deadline and one action I can start immediately. Keep the saved time and destination unchanged.
```

### 3. Check completion before delivery

```text
I completed [TASK LABEL]. Locate its pending one-shot reminder and ask for any approval needed to remove it; confirm the result rather than assuming it stopped.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
