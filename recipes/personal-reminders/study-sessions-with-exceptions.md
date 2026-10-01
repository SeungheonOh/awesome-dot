---
id: study-sessions-with-exceptions
title: "Study Sessions That Respect Exceptions"
summary: "Create a finite study schedule that preserves planned breaks and makes missed-session handling explicit."
category: personal-reminders
level: beginner
timebox_minutes: 25
capabilities: ["scheduling", "files"]
tags: ["study", "exceptions", "routine"]
status: recipe-not-run
---

# Study Sessions That Respect Exceptions

Create a finite study schedule that preserves planned breaks and makes missed-session handling explicit.

## Scenario

A learner wants eight weeks of language practice but already knows about travel and exam weeks. A useful reminder series respects those exceptions and ends with the course, rather than accumulating guilt-inducing catch-up messages.

## Inputs to prepare

- Study goal, session length and short default activity
- Start and end dates, regular days and local reminder time
- IANA timezone and notification destination
- Dates to skip and the chosen missed-session policy

## Copy this prompt into dot

```text
dot, schedule study prompts for [SUBJECT AND GOAL] from [START DATE] through [END DATE]. The normal pattern is [DAYS AND LOCAL TIME] in [IANA TIMEZONE], with [SESSION LENGTH] sessions and [DEFAULT ACTIVITY]. Notify me at [DESTINATION]. Skip [EXCEPTION DATES], and use [MISSED-SESSION POLICY] without adding unrequested catch-up reminders.

First verify supported scheduling and delivery. Preview the actual session dates, showing excluded dates and the last occurrence. Check whether the scheduler supports exceptions. If it does not, use a supported finite set of dated reminders or present an unscheduled plan; never claim an exception rule works when it cannot be verified. Ask if the supplied dates leave no sessions or if a local time is ambiguous around a clock change.

Look for an existing series with the same goal and date range before creating it. Keep messages short: subject, one specific starting action, planned duration and permission to skip according to my policy. Verify the saved timezone, destination, exceptions and end condition. Do not infer attendance from reminder delivery or move the end date after missed sessions. Return a calendar-style plan, the verified setup details, and a distinction between delivery status and actual study progress.
```

## Iterate with a purpose

### 1. Swap one study day

```text
Move the session on [DATE] to [REPLACEMENT DATE AND TIME] if it remains inside the course window. Update the existing occurrence and check for a collision.
```

### 2. Make sessions easier to start

```text
Rewrite each prompt around a two-minute first action followed by the original session goal. Keep the established dates, exceptions and ending unchanged.
```

### 3. Review observed progress

```text
Use [MY SESSION LOG] to compare planned and completed sessions. Suggest a realistic next block without creating or extending a schedule yet.
```

## Expected deliverables

- A dated study plan with excluded days shown
- Actionable reminder text matched to the study goal
- A verified finite schedule or an explicitly unscheduled fallback
- A simple progress log format that does not equate delivery with attendance

## Acceptance checks

- Every exception date is absent from the saved occurrences
- The final reminder falls within the supplied end date
- A schedule with all dates excluded leads to a user decision
- Clock-change ambiguity is resolved in the named timezone
- Missed sessions do not silently extend the schedule or create a burst
- A repeated setup does not produce a duplicate course series

## Access, privacy and stop conditions

- Scheduling support and exception behavior must be checked during the actual run
- No educational account enrollment or paid subscription is implied
- Stop and ask if the cadence conflicts with the supplied availability

## Two possible extensions

- Attach a private set of practice exercises to each session
- Create a separately approved revision block after the original course ends
