# Sources used for the reconciliation decisions

Consult the relevant primary source when the input uses semantics beyond the worked profile. These links were checked on October 2, 2026. A current product's official import instructions should be checked again for a real transfer.

- [RFC 5545, event component](https://www.rfc-editor.org/rfc/rfc5545#section-3.6.1): inclusive start, exclusive end and omitted-end behavior
- [RFC 5545, recurrence identity](https://www.rfc-editor.org/rfc/rfc5545#section-3.8.4.4): identifying the original slot of a moved occurrence
- [RFC 5545, time-zone identifier](https://www.rfc-editor.org/rfc/rfc5545#section-3.2.19): referenced local time-zone definitions; compare the actual file's definitions
- [RFC 5545, time-zone component](https://www.rfc-editor.org/rfc/rfc5545#section-3.6.5): an observance onset combines its local `DTSTART` with `TZOFFSETFROM`; do not encode the post-jump clock time as the onset
- [GOV.UK, clock changes](https://www.gov.uk/when-do-the-clocks-change): London advances at 01:00 on March 29, 2026. The spring regression checks the resulting missing hour against both the embedded definition and installed ZoneInfo data
- [RFC 5545, recurrence rule](https://www.rfc-editor.org/rfc/rfc5545#section-3.8.5.3): use a capable recurrence engine rather than implementing unfamiliar combinations from memory
- [RFC 5545, sequence number](https://www.rfc-editor.org/rfc/rfc5545#section-3.8.7.4): revision metadata, not a local duplicate counter
- [RFC 5546, component revisions and message sequencing](https://www.rfc-editor.org/rfc/rfc5546#section-2.1.4): scheduling messages carry semantics beyond simply collecting events into a snapshot. The example does not implement iTIP
- [icalendar's official usage documentation](https://icalendar.readthedocs.io/en/stable/how-to/usage.html): supported parsing and serialization interfaces. The worked run records the installed version instead of assuming it matches the moving stable documentation
- [python-dateutil's recurrence documentation](https://dateutil.readthedocs.io/en/stable/rrule.html): the installed recurrence engine used for the narrow finite projection. Dateutil is not a calendar UI or a provider import test
- [Google Calendar's official import documentation](https://support.google.com/calendar/answer/37118?hl=en): check destination selection, transfer limitations and lack of ongoing synchronization before treating a file as a migration plan

The source standards guide the format distinctions. The selection plan, dependency-group holds, byte preservation, evidence ledger and bounded verification workflow are original practical decisions for this skill; they are not claimed as requirements of the entire iCalendar standard.
