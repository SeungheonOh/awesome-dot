# Worked example: “one day before” is not always 24 hours

This fictional task is a materials checklist. Its deadline is October 25, 2026 at 09:00 in Europe/London. The user permits delivery from 09:00 to 18:00 and requests one reminder. No reminder is created by this example.

## Resolve the lead-time meaning

The clocks change during the interval in the timezone data used for this check.

| Interpretation supplied by the user | Warning in Europe/London | Warning in UTC | Actual elapsed lead time |
| --- | --- | --- | --- |
| One calendar day earlier, same local hour | October 24, 09:00 BST | October 24, 08:00 UTC | 25 hours |
| Exactly 24 elapsed hours earlier | October 24, 10:00 BST | October 24, 09:00 UTC | 24 hours |

Both fit the permitted delivery hours. They are different valid answers to different requests. If the user only says “a day before,” clarify the intended meaning instead of choosing silently when it matters.

An appropriate notification text is: “Materials checklist is due tomorrow at 09:00 Europe/London. Open the checklist and collect the missing item.” Use a neutral task label; no personal documents belong in the notification.

## Expected setup handoff

For the calendar-day interpretation, propose October 24 at 09:00 Europe/London, corresponding to 08:00 UTC. Inspect an existing matching reminder before creating one. If the service confirms the same task, deadline cycle, recipient and instant already exist, reuse that record.

After an authorized create or update, compare the saved instant, local interpretation, destination, message and one-occurrence behavior against the proposal. A description of the intended record is not setup evidence. If the service cannot show the saved state, say that verification is incomplete.

## Repeatable timezone check

This uses Python's installed timezone database. Actual scheduling should use the current supported service and timezone rules, not blindly reuse a date from this example.

```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

zone = ZoneInfo("Europe/London")
utc = timezone.utc

def possible_instants(local_naive):
    """Return zero, one or two UTC instants for a local wall-clock value."""
    results = set()
    for fold in (0, 1):
        candidate = local_naive.replace(tzinfo=zone, fold=fold)
        instant = candidate.astimezone(utc)
        round_trip = instant.astimezone(zone).replace(tzinfo=None)
        if round_trip == local_naive:
            results.add(instant)
    return sorted(results)

deadline_local = datetime(2026, 10, 25, 9, 0)
deadline_choices = possible_instants(deadline_local)
assert len(deadline_choices) == 1
deadline_utc = deadline_choices[0]
calendar_local = deadline_local - timedelta(days=1)
calendar_choices = possible_instants(calendar_local)
assert len(calendar_choices) == 1
calendar_utc = calendar_choices[0]
elapsed_utc = deadline_utc - timedelta(hours=24)
assert calendar_utc == datetime(2026, 10, 24, 8, 0, tzinfo=utc)
assert elapsed_utc == datetime(2026, 10, 24, 9, 0, tzinfo=utc)
assert calendar_utc.astimezone(zone).hour == 9
assert elapsed_utc.astimezone(zone).hour == 10
assert deadline_utc - calendar_utc == timedelta(hours=25)
assert deadline_utc - elapsed_utc == timedelta(hours=24)
# A repeated local hour requires a user choice between two real instants.
ambiguous = possible_instants(datetime(2026, 10, 25, 1, 30))
assert ambiguous == [datetime(2026, 10, 25, 0, 30, tzinfo=utc),
                     datetime(2026, 10, 25, 1, 30, tzinfo=utc)]
# A skipped local hour has no valid instant; constructing tzinfo alone is insufficient.
assert possible_instants(datetime(2026, 3, 29, 1, 30)) == []
print("PASS: calendar-day, elapsed-hour, repeated-hour and skipped-hour cases")
```

## Branches that should change the workflow

- **Past warning:** if the request is made after the proposed warning instant, ask for a useful future alternative. Do not send an immediate alert as an undisclosed fallback
- **Repeated or skipped local hour:** present the specific ambiguity or missing time. Do not assume that attaching a timezone to a naive timestamp validates it
- **Possible duplicate:** if two accessible saved records match but their identifiers or destinations differ, inspect and resolve them instead of creating a third
- **Unavailable destination:** return the exact unscheduled text and timestamp. Do not silently substitute another channel
- **Uncertain create response:** look for the resulting record before retrying; an interrupted response does not establish that creation failed

## Evidence

The exact calculation ran with Python 3.12.14 on 2026-10-01 and produced its stated PASS line. It checked timezone arithmetic and ambiguity detection only. It did not exercise a reminder service, create a schedule or verify future delivery.

[Return to the skill](SKILL.md)
