---
name: serialize-a-utc-calendar-event
description: "Prepare a valid calendar file from an agreed event interval while preserving time-zone interpretation, text escaping and import limits."
---

# Serialize a UTC calendar event

## When to use

The date and interval are already selected and the user needs a portable .ics event; this does not find availability or send invitations.

## Required inputs

- Exact start/end instants or local dates/times with IANA zones and resolved ambiguity
- Event title and only the authorized optional details
- Whether this is a new event or an update with a known UID

## Workflow

1. Resolve the interval to UTC using current zone data. For repeated or nonexistent local clock times, obtain the intended offset/instant rather than guessing. Confirm end follows start and preserve date rollovers.
2. For a new event generate a UID; for an update preserve the known event identity and applicable revision semantics. Do not invent attendees or organizer addresses.
3. Serialize UTC DTSTART/DTEND with Z and an actual DTSTAMP. Escape text backslashes, commas, semicolons and line breaks so user text cannot inject calendar properties.
4. Fold content lines by UTF-8 byte count without splitting a code point. Use CRLF and the required VCALENDAR/VEVENT structure under RFC 5545.
5. Parse the result independently when available and compare the recovered instants and text with the approved input. Save a new file; do not import or send invitations without authorization.

## Output

The .ics file and a short human-readable UTC/local interval summary, with validation and real calendar-import checks clearly distinguished.

## Verification and limits

Test next-day endings, DST transitions, fractional offsets, Unicode line folding and titles containing newlines/delimiters. Generating a file does not establish calendar availability.

## References

[RFC5545](https://www.rfc-editor.org/rfc/rfc5545.html)
