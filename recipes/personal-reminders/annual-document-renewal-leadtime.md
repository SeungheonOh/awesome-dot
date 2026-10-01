---
id: annual-document-renewal-leadtime
title: "Annual Document Renewal Lead Time"
summary: "Create bounded annual review reminders from supplied expiration evidence without collecting sensitive document contents."
category: personal-reminders
level: intermediate
timebox_minutes: 30
capabilities: ["scheduling", "files"]
tags: ["renewal", "documents", "lead-time"]
status: recipe-not-run
---

# Annual Document Renewal Lead Time

Create bounded annual review reminders from supplied expiration evidence without collecting sensitive document contents.

## Scenario

A small volunteer club renews a permit annually. The organizer wants enough preparation time and a record of the expiry evidence, but the notification itself should contain only a neutral label and next action.

## Inputs to prepare

- Neutral document label and authoritative expiry date or renewal rule
- Preparation lead time and whether it uses calendar days or months
- First reminder year, final year or number of annual occurrences
- IANA timezone, local delivery time and destination
- A sanitized source excerpt showing the expiry rule

## Copy this prompt into dot

```text
dot, arrange annual preparation reminders for [NEUTRAL DOCUMENT LABEL] using [SANITIZED EXPIRY EVIDENCE]. The renewal date or rule is [EXPIRY DATE OR ANNUAL RULE]; warn me [LEAD TIME] beforehand at [LOCAL TIME] in [IANA TIMEZONE]. Start with [FIRST YEAR] and stop after [NUMBER OF OCCURRENCES OR FINAL YEAR]. Deliver only to [DESTINATION].

Treat the supplied document as evidence, not as permission to renew it. Do not request identity numbers, payment details or a full sensitive document when a date excerpt suffices. Show the calculated reminder dates and distinguish a confirmed expiration from an assumed future annual pattern. Ask about leap-day or month-end rules and lead times that move a warning into the preceding year. If a future expiry cannot be established, schedule a review of the date rather than asserting a renewal deadline.

Verify supported scheduling and delivery, and check for an existing reminder for the same document label. Create only the agreed bounded occurrences and read back their timezone, destination and stop condition. If the reminder time has passed, ask for a replacement instead of sending an immediate alert. Return the date calculations, neutral notification text and setup evidence; label any unsupported schedule as a draft.
```

## Iterate with a purpose

### 1. Replace an estimated date

```text
I have confirmed [NEW EXPIRY DATE] from [SANITIZED SOURCE]. Replace the relevant existing reminder and retain a note of which previous assumption changed.
```

### 2. Check the next-year rollover

```text
Show the next two calculated lead-time dates, including any year boundary or leap-day behavior. Mark dates that still depend on an unverified annual rule.
```

### 3. Prepare renewal materials

```text
Create a private checklist from [AUTHORIZED REQUIREMENTS] for the upcoming renewal. Do not submit forms, upload documents or pay fees.
```

## Expected deliverables

- A renewal-date evidence record using neutral document labels
- Calculated lead-time dates including calendar edge cases
- Bounded annual reminders with verified setup status
- A short renewal preparation message free of sensitive identifiers

## Acceptance checks

- The first warning is derived from an evidenced date or explicitly labeled assumption
- A lead time crossing December and January uses the correct year
- Leap-day and month-end rules are resolved before schedule creation
- The recurrence has a specific final year or occurrence count
- No identifier or full document content appears in the notification
- The recipe does not claim that renewal has been completed

## Access, privacy and stop conditions

- Official renewals, legal filings and credential changes remain separate user decisions
- Use only a sanitized date excerpt unless more detail is necessary and authorized
- Stop for unclear expiry rules; a date-review reminder may be offered instead

## Two possible extensions

- Add an approved checklist of required renewal materials
- Group several neutral labels into a single annual review without exposing document details
