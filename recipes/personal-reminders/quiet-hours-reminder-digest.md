---
id: quiet-hours-reminder-digest
title: "A Quiet-Hours Digest for Routine Reminders"
summary: "Combine a chosen set of low-stakes reminder items into one bounded daily digest without claiming control over unrelated alerts."
category: personal-reminders
level: intermediate
timebox_minutes: 35
capabilities: ["scheduling", "files"]
tags: ["digest", "quiet-hours", "deduplication"]
status: recipe-not-run
---

# A Quiet-Hours Digest for Routine Reminders

Combine a chosen set of low-stakes reminder items into one bounded daily digest without claiming control over unrelated alerts.

## Scenario

A user has several low-stakes household tasks but prefers one evening summary. This recipe creates a digest for an explicitly chosen list; it does not pretend to suppress every notification from the user’s devices or connected apps.

## Inputs to prepare

- An authorized list of low-stakes tasks with stable labels and due dates
- Quiet hours, daily digest time and IANA timezone
- Start and end dates and a verified personal notification destination
- A rule for overdue items, unchanged items and an empty digest
- Existing reminders that might overlap and the user’s choice about them

## Copy this prompt into dot

```text
dot, create one daily digest for [AUTHORIZED LOW-STAKES TASK LIST]. Run from [START DATE] through [END DATE] at [LOCAL DIGEST TIME] in [IANA TIMEZONE], delivering to [DESTINATION]. My quiet hours are [QUIET HOURS]. Include items due in [LOOKAHEAD WINDOW] and handle overdue items using [OVERDUE RULE]. This digest must not include urgent, health-sensitive or safety-critical alerts.

Verify scheduling, delivery and access to the supplied list. Check that the chosen delivery time sits outside quiet hours, including a window that crosses midnight. Identify overlapping reminders and ask whether I want to keep them or explicitly modify the named ones; do not assume permission to disable anything. Do not claim that this digest controls unrelated app notifications.

Use stable task labels and a dated digest identity to prevent duplicate setup or duplicate messages for the same daily window. Apply [UNCHANGED-ITEM RULE] and skip empty digests if supported; otherwise explain the actual behavior before setup. Verify the saved start, end, timezone and destination. Do not send missed digests in a catch-up burst. Return a sample with a due item, an overdue item and an empty-day outcome, plus setup evidence. If scheduling or filtering is unsupported, offer a clearly labeled simpler draft.
```

## Iterate with a purpose

### 1. Test the midnight boundary

```text
Check the digest against [QUIET HOURS THAT CROSS MIDNIGHT] and the next timezone clock change. Show the selected delivery time and any unresolved edge case.
```

### 2. Reduce repeated items

```text
Use [UNCHANGED-ITEM RULE] to shorten repeated low-stakes items while keeping materially changed due dates visible. Do not suppress new items or broaden the source list.
```

### 3. End the digest cleanly

```text
Stop this digest at [EARLIER END DATE]. Verify its remaining schedule and list any independent reminders that still exist without modifying them.
```

## Expected deliverables

- A digest inclusion rule and low-stakes source scope
- An example digest plus the empty-day behavior
- A duplicate-prevention and unchanged-item policy
- A verified finite daily schedule with quiet-hours checks

## Acceptance checks

- A quiet-hours window crossing midnight is interpreted correctly
- Only items from the explicit source list enter the digest
- The same task appears once within a given digest
- An empty day follows verified scheduler behavior rather than an assumed skip feature
- No digest is scheduled beyond the end date
- Unrelated notifications and overlapping schedules remain explicitly accounted for

## Access, privacy and stop conditions

- Restrict the digest to routine items that can safely wait until its delivery time
- Changing existing reminders requires an explicit selection and any required approval
- Do not promise system-wide notification suppression
- Stop if the chosen digest time conflicts with quiet hours and no alternative is approved

## Two possible extensions

- Add a separately approved weekend digest pattern
- Create a private task-entry template with stable labels and due dates
