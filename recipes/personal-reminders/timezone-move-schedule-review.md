---
id: timezone-move-schedule-review
title: "Review Reminders After a Timezone Move"
summary: "Schedule a bounded review that helps distinguish fixed local-time routines from fixed-instant commitments after a move."
category: personal-reminders
level: intermediate
timebox_minutes: 30
capabilities: ["scheduling"]
tags: ["timezone", "relocation", "review"]
status: recipe-not-run
---

# Review Reminders After a Timezone Move

Schedule a bounded review that helps distinguish fixed local-time routines from fixed-instant commitments after a move.

## Scenario

A person moving between regions has morning routines mixed with meetings tied to another city. Shifting every reminder by the same offset could break both. The intended outcome is a scheduled review and a change proposal, not an automatic mass migration.

## Inputs to prepare

- Move date and the old and new IANA timezones
- Sanitized reminder labels and whether each should preserve local time or absolute time
- A review date after arrival and one-shot notification destination
- Schedules that must be left unchanged

## Copy this prompt into dot

```text
dot, help me review reminder timing for a move from [OLD IANA TIMEZONE] to [NEW IANA TIMEZONE] on [MOVE DATE]. I want one review notification at [LOCAL REVIEW DATE AND TIME] in the new timezone, delivered to [DESTINATION], and no recurring timezone monitoring.

Verify available scheduling and destination access, then check for an existing review for this move. Before scheduling, resolve ambiguous or nonexistent local times and show the intended local time with its UTC offset. The one-shot schedule starts at that agreed instant and stops after its single delivery. Verify its saved settings; if unsupported, provide an unscheduled reminder draft.

Using [AUTHORIZED REMINDER LIST], prepare a review sheet that separates routines intended to preserve local wall-clock time from commitments intended to preserve their absolute instant. Ask about unclear entries instead of deciding silently. Show before-and-after examples for [SAMPLE DATE] and the next daylight-saving transition where relevant. Do not change the underlying reminders during this review. Identify any schedules whose timezone behavior cannot be verified and note the evidence needed. Keep the review notification short, with no private event descriptions, and include a checklist for approving specific changes after arrival.
```

## Iterate with a purpose

### 1. Classify uncertain reminders

```text
For the entries marked unclear, ask the smallest set of questions needed to choose fixed local time or fixed instant. Update only the review sheet.
```

### 2. Preview a seasonal transition

```text
Show how the proposed timings behave across the next daylight-saving change in each relevant region. Flag reminders that would shift relative to the other region.
```

### 3. Apply selected timing changes

```text
Apply only [APPROVED REMINDER CHANGES] to the identified existing schedules, preserving their content and audience. Read back the resulting timezone and next occurrence for each.
```

## Expected deliverables

- A verified one-shot move-review notification or an unscheduled draft
- A classification sheet for fixed-local-time and fixed-instant reminders
- A proposed timing comparison with unresolved choices highlighted
- A checklist for reviewing and authorizing actual schedule changes

## Acceptance checks

- Old and new zones use unambiguous IANA identifiers
- A meeting fixed to an instant and a morning routine produce different migration logic
- Ambiguous or skipped local times are surfaced before setup
- The review itself does not change existing routine schedules
- Duplicate setup requests leave one move-review notification
- The review has no recurrence after its single occurrence

## Access, privacy and stop conditions

- Review only schedules the user has authorized access to
- Changing account-wide timezone settings is outside this recipe
- Pause any underlying schedule change until the user identifies the intended timing semantics

## Two possible extensions

- Add a second review after a separately approved seasonal clock change
- Build a portable timezone comparison sheet for a household move
