---
name: export-date-only-milestones
description: Export bounded date-only milestones or projected charge dates as an iCalendar file without inventing clock times, recurrence rules, reminders or calendar updates.
---

# Export date-only milestones

## When to use

Use when a reviewed list of calendar dates should become a portable calendar file. Examples include renewal reviews, project checkpoints and document-expiry lists. This workflow creates a file; it does not book time, send invitations or import into an account.

## Required inputs

- Validated dates and labels, with supplied versus projected provenance
- A bounded reporting window and any unresolved source conflicts
- Which details may be exported and whether amounts or other fields are unknown
- Identity intent: a fresh snapshot or updates to established calendar entries

## Workflow

### Preserve date semantics

Use DTSTART with VALUE=DATE for a day without an agreed clock time. Do not convert midnight UTC into a local instant: that can display on the preceding day elsewhere. For a one-day event, use the following calendar date as exclusive DTEND, also VALUE=DATE. Test month, year and leap-day boundaries.

Retain each reviewed occurrence explicitly when recurrence semantics are uncertain or provider-specific. A list projected using an original-day clamp is not automatically equivalent to a monthly RRULE. Do not generate extra dates or reinterpret a trial milestone as a verified charge.

### Carry uncertainty into the artifact

Distinguish supplied dates, projections and actual completed actions. Use tentative status and transparent availability when the entries are planning references rather than appointments. Keep unknown amounts unknown; zero has a different meaning. Carry concise conflict and duplicate warnings where they affect interpretation.

Omit source URLs, private notes and account details that are unnecessary for the calendar. CLASS:PRIVATE is metadata, not access control: the calendar account or sharing destination still controls visibility. Do not add alarms, attendees or organizer fields without the corresponding intent.

### Choose an identity policy

For an actual update, preserve established UIDs and the consumer's revision semantics. For a standalone snapshot without an established import target, fresh export IDs are reasonable, but disclose that importing another snapshot may duplicate entries. A local row number is not a durable identity across different inventories.

Use a real export-time DTSTAMP. Never treat a file download request as confirmation that a calendar accepted the entries.

### Serialize safely

Escape TEXT backslashes, commas, semicolons and line breaks. Reject unsupported control characters and malformed Unicode rather than silently changing a label. Construct property names and parameters from fixed code, not source text. Use CRLF between content lines.

Fold lines at no more than 75 UTF-8 octets, including the leading whitespace of continuation lines. Iterate Unicode code points so a multibyte character is never split. Bound record count and text lengths before creating the file.

### Validate and hand over

Parse the exported bytes with an independent calendar library when available. Compare recovered dates, exclusive ends, exact text, event count, status, transparency and UID uniqueness to the reviewed source. Include delimiter/newline injection fixtures and long non-ASCII labels. If a parser is unavailable, state the narrower validation performed.

Disable export when inputs change or a replacement review fails. Keep file generation separate from account import, which needs its own authorization and verification.

## Worked example

A fictional review contains a supplied renewal on February 29, 2028 with an unknown price. Export an all-day tentative entry beginning 20280229 and ending 20280301. Its description says the amount is unknown and identifies the supplied-date basis. It does not invent a midnight billing time or a payment result.

A later March 31 date projected from an evidenced original-day rule is a separate event labeled projected. Replacing that list with an unqualified monthly recurrence could skip or shift dates. The recipient reviews the snapshot before import; repeated fresh snapshots can produce duplicates.

## Stop conditions and limits

Stop when the file is validated and delivered, or when an unresolved date or export-permission conflict prevents trustworthy output. File syntax validation is not proof of destination privacy, calendar import or billing accuracy.

## Reference

[RFC 5545](https://www.rfc-editor.org/rfc/rfc5545.html), especially content-line folding, TEXT escaping and VEVENT date boundaries.
