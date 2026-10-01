---
id: trip-countdown-milestones
title: "A Trip Countdown with Milestones"
summary: "Create a finite sequence of preparation reminders tied to a trip departure, with explicit ownership and cancellation handling."
category: personal-reminders
level: intermediate
timebox_minutes: 30
capabilities: ["scheduling", "files"]
tags: ["travel", "countdown", "milestones"]
status: recipe-not-run
---

# A Trip Countdown with Milestones

Create a finite sequence of preparation reminders tied to a trip departure, with explicit ownership and cancellation handling.

## Scenario

A traveler has a confirmed departure but keeps a scattered list of errands. A useful countdown separates tasks that require a week from tasks that belong the evening before, then ends when preparation is over.

## Inputs to prepare

- Departure date, time and departure-city timezone
- Three to six preparation milestones with lead times and task owners
- The earliest allowed reminder date and notification destination
- Local quiet hours and a rule for milestones that are already overdue
- A sanitized trip label that does not reveal booking details

## Copy this prompt into dot

```text
dot, create a bounded preparation countdown for [TRIP LABEL], departing at [DEPARTURE DATETIME] in [IANA TIMEZONE]. Use [MILESTONES WITH LEAD TIMES AND OWNERS], starting no earlier than [START DATE] and ending at departure. Send reminders only to me at [DESTINATION], even when a milestone mentions another person's task.

Verify supported scheduling and destination access before making commitments. Turn each milestone into an actionable notification, calculate its local delivery time, and show the complete sequence before resolving missing choices. Respect [QUIET HOURS]. Flag milestones whose useful window has already passed; ask whether to omit them or schedule a new time instead of triggering them immediately. Distinguish elapsed-hour offsets from calendar-day offsets and account for daylight-saving changes.

Check existing reminders for this trip label and departure so retries cannot duplicate the sequence. Create only the agreed finite occurrences, with nothing after departure. Read back the saved dates, timezone and destination, and mark any unsupported behavior honestly. Include a short change plan explaining how a moved or canceled trip would affect the sequence, without changing anything else. If setup is unavailable, return a dated countdown checklist labeled unscheduled. Keep booking numbers, accommodation addresses and identity documents out of notification text.
```

## Iterate with a purpose

### 1. Handle a moved departure

```text
The departure is now [NEW DATETIME AND TIMEZONE]. Show which milestones remain useful, update the existing sequence, and verify that obsolete occurrences are no longer pending.
```

### 2. Reduce notification clutter

```text
Combine milestones that fall on the same local day into one preparation message, preserving each owner and due action. Show the revised finite sequence before applying changes.
```

### 3. Close a canceled trip

```text
The trip is canceled. Identify this trip’s remaining reminders, obtain any required confirmation, and verify that the sequence is stopped without affecting other trips.
```

## Expected deliverables

- A milestone table with lead-time units, owners and calculated local times
- Concise notification text for each agreed milestone
- A finite schedule inventory with verified setup status
- A departure-change and cancellation checklist

## Acceptance checks

- Every milestone can be traced to a supplied task and lead time
- No scheduled occurrence precedes the approved start or follows departure
- A same-day or overdue milestone has an explicit decision path
- Moving the departure updates existing items rather than leaving two countdowns
- Notifications go only to the supplied personal destination

## Access, privacy and stop conditions

- A countdown does not book travel or contact other travelers
- Use sanitized trip labels and omit private itinerary details from alerts
- Stop if the trip date is provisional enough to invalidate the countdown

## Two possible extensions

- Add a return-home unpacking checklist as a separately approved sequence
- Link each milestone to an authorized private packing checklist
