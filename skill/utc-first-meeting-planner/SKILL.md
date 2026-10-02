---
name: utc-first-meeting-planner
description: Build a local multi-city meeting-time planner that handles daylight-saving changes, checks whole-meeting working windows, and exports an explicit UTC calendar file without accessing calendars.
---

# UTC-First Meeting Planner

Build a small planning utility that compares actual instants across cities. Distinguish user-entered working preferences from real calendar availability. Keep the app and test programs outside this skill contribution.

## Inputs and deliberate simplifications

Collect a search date, meeting duration, cities identified by IANA time-zone IDs, and local working windows. A compact first version can search 48 half-hour UTC start times for three cities, with durations from 30 to 120 minutes. Explain that the search date is UTC; some local dates will differ. State whether windows apply every day or exclude weekends. Do not silently treat unqueried calendars as free.

## Build in this order

1. Implement a strict date parser. Construct UTC midnight from the submitted YYYY-MM-DD date and compare the parsed result back to the input so invalid dates cannot roll into another month. Reject missing dates.
2. Represent all candidate instants as UTC timestamps. Generate candidates by adding elapsed milliseconds to UTC midnight. Never generate local clock strings and assume each corresponds to a unique instant: spring transitions can skip an hour, and autumn transitions can repeat one.
3. Format each instant with Intl.DateTimeFormat using the participant's IANA zone, an explicit 24-hour cycle, full local date, and short UTC offset. Cache formatters by zone. Preserve the distinction between a displayed local date and the UTC search date.
4. Evaluate the entire meeting interval against each local working window. For integer-minute durations, check every included minute in the half-open interval from start through end-minus-one-minute. Checking only the starting time or only endpoints is insufficient across boundaries and clock changes. If overnight windows are unsupported, reject start-at-or-after-end rather than guessing.
5. Build a pure result model containing UTC start/end, each city's local start/end/date/offset, whether the whole interval fits, and the number of fitting cities. Define tie-breaking explicitly, such as earliest UTC start among equally good candidates. Show a no-full-overlap result honestly instead of labeling a partial fit suitable for everyone.
6. Create city/window controls, a small shortlist, an explicit selected moment, and a scrollable full-day table. Rows should remain chronologically ordered in UTC even when a local clock repeats or skips. Display both dates when the meeting crosses a local or UTC midnight, and both offsets if a transition happens during the meeting.
7. Wire invalid states transactionally. Invalid dates/windows disable download and clear the selectable result model; fixing them recalculates results. Preserve keyboard focus when re-rendering city controls. A full-overlap filter may produce no rows without making outside-window candidates cease to exist.
8. Offer a local .ics download only after the selection is valid. Use UTC DTSTART/DTEND values ending in Z, an independent UID for a new event, and DTSTAMP. Normalize line breaks in user-provided titles, escape text delimiters, and fold long lines by UTF-8 byte count without splitting a code point. Follow [RFC 5545](https://www.rfc-editor.org/rfc/rfc5545.html), especially content lines, text values, and VEVENT date-time properties.
9. Describe download initiation accurately. Generating a file does not import an event, send invitations, reserve a room, or establish another person's availability. Keep those actions separate and authorization-bound.

## Observable checks

Use fixed dates and exact expected results, not the machine's current date, for model tests:

- New York spring transition: 2026-03-08 06:30 UTC formats as 01:30; 07:00 UTC formats as 03:00.
- New York autumn transition: 2026-11-01 05:30 and 06:30 UTC both format as 01:30, with different offsets. They remain two separate candidates.
- Bangkok at 2026-10-02 23:30 UTC has local date October 3. Include a fractional-offset zone as another fixture.
- For a 09:00–17:00 window, a 30-minute meeting at 16:30 fits; 31 minutes does not. An 08:30 start does not fit merely because it ends inside the window.
- UTC and Bangkok with identical 09:00–17:00 windows have exactly one hourly-meeting start on the half-hour grid: 09:00 UTC.
- A 90-minute meeting starting 23:30 UTC ends at 01:00 UTC the following day. The exported event must retain that date change.
- There are always 48 strictly increasing candidate starts for a searched UTC day, including local transition days.
- ICS title newlines cannot introduce properties or another event. Folded physical lines must stay within the chosen byte limit; unfold them and confirm the original Unicode text remains intact.

Test the interface independently: change cities, produce full/no overlap, filter results, enter an invalid window, recover, select a next-day meeting, initiate download, clear the date, and restore today's date. A DOM harness does not prove a real calendar imports the file correctly; use an independent calendar parser and real browser/calendar import check when available, and report what remains unverified.

## Reference-build evidence and limits

Timebridge's fixed model checks covered spring and autumn transitions, rollover, half-open windows, monotonically increasing UTC slots, exact overlap, and escaped/folded calendar output. Its simulated-DOM checks covered the 48-row day, overlap counts, filters, invalid windows, no-overlap states, next-day selection, export initiation, and date recovery. Real-browser visual QA and calendar-app import were not verified at contribution time. Current time-zone behavior depends on the runtime's installed zone data; repeat dated checks in the target runtime.

## Deliverable

Provide the runnable local app, its assumptions, model/UI checks, and any unverified rendering or calendar behavior. Publish to a hosting service only when that app's destination and audience are approved. Contribute only this SKILL.md here; keep product source, tests, artifacts, account details, and build notes outside the repository.
