# Worked example: one cross-zone meeting

All people, addresses, availability and requests below are fictional. This fixture represents supplied availability, not a real calendar export. No invitations or schedules are created.

## Request and evidence

> Find options for a 45-minute prototype handoff on October 28, 2026 with Noor Vale, Eli Marlow and Sana Ito. All three are required. Each needs 15 minutes free before and after the new meeting, inside the supplied working window. Do not send an invitation yet.

The synthetic participant record resolves the names to `noor.vale@example.test`, `eli.marlow@example.test` and `sana.ito@example.test`. These addresses are example data, not usable contacts. In a real run, resolve identities from authorized evidence rather than copying them.

The following are complete raw busy intervals for the supplied windows. No buffers have already been added. The fixture's working windows are explicit inputs, not proposed defaults.

| Participant | IANA zone | Allowed local window | Raw busy in local time |
| --- | --- | --- | --- |
| Noor | Europe/London | Oct 28, 12:00–17:00 | Oct 28, 12:00–12:15 |
| Eli | America/New_York | Oct 28, 08:00–13:00 | Oct 28, 09:30–10:15 |
| Sana | Asia/Singapore | Oct 28, 20:00 to Oct 29, 00:00 | Oct 28, 23:30 to Oct 29, 00:00 |

## Derive the options

On these dates the installed time-zone database gives London UTC+00:00, New York UTC−04:00 and Singapore UTC+08:00. London is four hours ahead of New York on this date; applying an offset from a different date would be unsafe.

The common allowed interval is Oct 28, 12:00–16:00 UTC. Subtracting the union of the raw busy intervals leaves:

```text
12:15–13:30 UTC: 75 minutes
14:15–15:30 UTC: 75 minutes
```

Each gap exactly fits 15 minutes before + 45 meeting minutes + 15 minutes after. Its feasible-start range therefore contains a single point. Buffer the new meeting once; do not also pad the busy intervals.

| Option | London, Oct 28 (+00:00) | New York, Oct 28 (−04:00) | Singapore, Oct 28 (+08:00) |
| --- | --- | --- | --- |
| A | 12:30–13:15 | 08:30–09:15 | 20:30–21:15 |
| B | 14:30–15:15 | 10:30–11:15 | 22:30–23:15 |

An appropriate result is: “Two windows fit the supplied availability and the 15-minute buffers: 12:30–13:15 or 14:30–15:15 London time on October 28.” Include the other local times and source limitations when presenting the actual options. Stop there for this find-options request.

## Decision branches

- **Unknown calendar:** replace Sana's availability with unknown and remove any supplied availability for Sana. The checker returns no all-participant result and names Sana as unknown. The two known calendars cannot establish that Sana is free. Known-subset proposals may still be shown with that qualification; missing data is not a no-intersection result.
- **No intersection:** increase the duration to 46 minutes while preserving the hard buffers and windows. Neither 75-minute gap can contain the required 76 minutes. Report no fit within these constraints; do not cut the buffers to make it work.
- **Changed availability:** if a fresh pre-booking check adds a conflict to option A, discard A. “Book A” does not authorize B; “book the earliest remaining feasible option from these windows” can authorize B after rechecking it.
- **Explicit booking:** if the user subsequently says “Send the earlier option to these three for the prototype handoff on my Work calendar, using the agreed meeting location,” apply that request once the calendar, location and identities are resolved. Recheck available sources immediately, create the one-off event, and read it back. Do not add another send-approval question merely because the action sends invitations.
- **Unknown remains at booking:** ask only for the missing availability or a decision to proceed despite that specific unknown, unless the user already authorized booking from supplied availability or despite it. Label the limitation even if proceeding is authorized.

For a real booking of A, the readback must show start `2026-10-28T12:30:00Z`, end `2026-10-28T13:15:00Z`, the correct Work calendar/organizer, exactly the three verified attendee addresses with the correct roles, the agreed destination, and no recurrence. Check the provider's notification state before saying invitations were sent. A saved event is not proof of RSVP acceptance. This branch is instructional and was not executed.

## Repeat the local check

From the repository root:

```bash
python3 --version
python3 skill/meeting-window-coordination/check_example.py
```

Observed on 2026-10-01 with Python 3.12.14 and installed time-zone data version 2026b (`zoneinfo`): exit status 0. The checker printed both UTC/local options above and passed these assertion groups:

```text
PASS: two exact feasible starts with 15-minute buffers against raw busy intervals
PASS: offsets, endpoint boundaries, 46-minute no-intersection, unknown-calendar branch
PASS: working-window buffer, overlapping busy union, ambiguous/skipped local times
```

The script also checks that moving either start one minute in either direction fails; the buffered interval may touch a raw busy endpoint but not overlap it. It rejects London's ambiguous `2026-10-25 01:30` without an occurrence choice and nonexistent `2026-03-29 01:30`; selecting the two valid fall-back occurrences yields UTC instants one hour apart.

Limits: this is one synthetic case plus focused arithmetic edge checks. The helper assumes identical buffers for all participants and complete supplied working windows. It does not test live identity resolution, provider integrations, access permissions, stale-data detection, invitations, delivery, RSVPs, concurrent bookings, or every time-zone rule. Do not treat a passing fixture as evidence that a real invitation was sent or that a real person is available.

For a different 30-minute case with an independently checked singleton result, read [second-case.md](second-case.md). It records synthetic interval verification only.

## Additional buffer-policy regression

The primary case requires buffers inside each working window. The checker also exercises a separate UTC boundary case: working time 09:00–10:00, known availability coverage 08:45–10:15, a 30-minute meeting and 15 minutes free before and after it. Inside-window buffers permit only a 09:15 start. If the user explicitly permits buffers outside work, every start in the closed range 09:00–09:30 is valid. That permission does not itself prove outside availability: with coverage limited to 09:00–10:00, only 09:15 remains verified. A busy interval at 10:00–10:10 reduces the outside-permitted range to 09:00–09:15. Coverage gaps are never bridged as if free. These are local interval checks, not a calendar-provider test.
