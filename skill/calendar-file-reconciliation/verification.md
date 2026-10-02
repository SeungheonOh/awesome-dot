# Verification record

The completed behavioral run used Python 3.12.14 with the following packages downloaded for this example and used from an isolated dependency environment:

- [icalendar 6.3.2](https://pypi.org/project/icalendar/6.3.2/)
- [python-dateutil 2.9.0.post0](https://pypi.org/project/python-dateutil/2.9.0.post0/)
- [tzdata 2026.4](https://pypi.org/project/tzdata/2026.4/)
- [six 1.17.0](https://pypi.org/project/six/1.17.0/)

Installed wheel members were compared byte-for-byte with the official PyPI distributions before the final run, excluding installer-generated `RECORD` files. The public skill does not bundle those dependencies or require changing a system installation. A reader needs an interpreter with the dependencies available to reproduce the parser checks.

## Observed offline behavior

The behavioral checker completed on October 2, 2026 and reported passing results for:

- All twelve source components accounted for as four retained, one duplicate, two superseded and five held, with no held UID in the candidate
- A plan holding every group stops with no-candidate guidance before creating an ICS file or output directory
- Source bytes and evidence unchanged; fresh repeated runs produce the same candidate bytes; an existing output directory is not overwritten
- UIDs, sequence values and the moved instance's original 09:00 recurrence identity preserved
- London occurrences at 08:00 UTC before the clock change, the moved session at 10:00 UTC afterward, and the extra November 3 session at 09:00 UTC; the excluded November 2 instance absent
- Both source `VTIMEZONE` definitions and the saved definition agree with installed `ZoneInfo("Europe/London")` at the March 29 spring transition: 01:30 does not exist, 02:30 exists, and 01:00 UTC becomes 02:00 local. End-to-end checks reject a 01:30 appointment and accept 02:30 at 01:30 UTC
- All-day values retained as dates covering October 24–26, with the exclusive end October 27
- Independent same-title event retained under its distinct UID
- Unicode, escaped punctuation, a description newline, folded content lines, CRLF serialization and the fixture's extension field surviving saved-file parsing
- Changed source/evidence hashes rejected before output
- Equal-revision conflicts, floating time, stale active copies of a cancellation, emitting the cancelled component, omitted overrides and selecting a different UID rejected
- Scheduling `METHOD`, unsupported calendar scale, range overrides, unsupported recurrence, conflicting embedded zone definitions, non-positive event spans and alarms rejected before output

The checker prohibited network socket creation during every reconciliation call. It used only fictional files. Dependency setup is separate from this offline execution evidence.

The spring expectation is independently supported by [GOV.UK's clock-change guidance](https://www.gov.uk/when-do-the-clocks-change): the 2026 change is March 29, with clocks advancing at 01:00. The fixture represents this as `DTSTART:20260329T010000` with `TZOFFSETFROM:+0000` and `TZOFFSETTO:+0100`. See [RFC 5545's time-zone component definition](https://www.rfc-editor.org/rfc/rfc5545#section-3.6.5) for using the onset's local time together with the prior offset.

An independent code and source review reran all 20 scenarios and regenerated the three delivered outputs byte-for-byte. The source packet stayed unchanged. This included the no-candidate result for all-held input and both the accepted 02:30 and rejected 01:30 spring-transition cases.

## What the result does not establish

This is a parser/serializer round trip and a finite recurrence projection using two installed libraries. It is not a calendar UI import, a provider migration, a complete RFC 5545 validation, a full future-series proof or an iTIP message implementation. No real calendar, invitation, account, attachment, alarm or network service was exercised by the checks.

The current helper deliberately holds unsupported semantics rather than modifying them. A file that passes this profile may still require destination-specific testing for duplicate handling, existing-event updates, cancelled events, notifications and preservation of unsupported fields.
