# Fictional Disrupted Journey

All locations, services, quoted prices, transfer assumptions and connection rules below are invented test data. Real timezone identifiers provide date arithmetic only. No route is a real service; no live availability, provider rule or booking has been checked. There are deliberately no invented booking URLs.

## Supplied scenario

One traveler is in fictional Westport at 2026-10-15 18:30 in America/Los_Angeles (UTC−07:00). The original direct journey was canceled. The traveler cannot depart before 20:00 local, must reach a meeting venue in fictional Eastport by 2026-10-16 10:00 in America/New_York (UTC−04:00), and prefers at least 60 minutes of arrival slack. The replacement spending cap is USD 650, including one checked bag and required ground travel.

A fictional authorized itinerary extract, reference `scenario-itinerary-1`, establishes the original journey and constraints. An invented options sheet, `scenario-options-1`, supplies these schedules and prices at 2026-10-15 18:35 Westport time. Its price fields are arithmetic fixtures, not real quotes. For this fixture only, fare amounts include every mandatory tax and booking fee; the separate bag amount covers the required checked bag. The traveler is already at the origin terminal, so no origin transfer is needed; each ground amount covers the full required destination-to-venue transfer. Processing and transfer durations are elapsed durations. All replacement seat availability is unknown. Earliest-departure feasibility is a supplied scenario constraint; actual check-in and boarding cutoffs remain unverified.

The original ticket cost USD 500. A possible USD 125 refund is unconfirmed and excluded from every payable-now total. No reroute or change offer has been obtained from the original provider.

## Candidate A: direct service

- Departure: October 15 22:15 Westport, UTC−07:00 = October 16 05:15 UTC
- Arrival: October 16 06:45 Eastport, UTC−04:00 = October 16 10:45 UTC
- Flight elapsed time: 5 hours 30 minutes
- Scenario arrival processing: 45 minutes; venue transfer: 30 minutes
- Venue arrival: October 16 08:00 Eastport time
- Deadline slack: 2 hours; preferred 60-minute buffer is met
- Test cost: USD 430 fare + USD 35 bag + USD 45 ground = USD 510 payable now; USD 140 below cap

This is the strongest candidate to verify first. Availability, fare terms, exact terminals, operating status, cutoff rules and actual transfer time remain unverified. The schedule and cost arithmetic alone do not make it bookable.

## Candidate B: connection that fails

The fictional hub uses America/Chicago (UTC−05:00 on these dates).

- Leg 1 departs Westport October 15 20:30, UTC−07:00 = October 16 03:30 UTC
- Leg 1 arrives at the hub October 16 01:45, UTC−05:00 = October 16 06:45 UTC; elapsed 3 hours 15 minutes
- Leg 2 departs the hub October 16 02:40, UTC−05:00 = October 16 07:40 UTC
- Leg 2 arrives Eastport October 16 05:15, UTC−04:00 = October 16 09:15 UTC; elapsed 1 hour 35 minutes
- Connection: 07:40 − 06:45 UTC = 55 minutes
- Invented applicable connection minimum in the scenario: 65 minutes; shortfall 10 minutes
- Test cost: USD 350 fare + USD 35 bag + USD 45 ground = USD 430

Reject B on the supplied scenario rule. Its earlier final arrival and lower cost do not cure the failed connection. The 65-minute value is not guidance for any real terminal.

## Candidate C: nearby arrival terminal

- Departure: October 15 21:45 Westport, UTC−07:00 = October 16 04:45 UTC
- Arrival: October 16 06:20 at fictional Eastport Outer, UTC−04:00 = October 16 10:20 UTC
- Flight elapsed time: 5 hours 35 minutes
- Scenario arrival processing: 45 minutes; estimated venue transfer: 2 hours 45 minutes
- Estimated venue arrival: October 16 09:50 Eastport time
- Deadline slack: 10 minutes; preferred buffer is missed by 50 minutes
- Test cost: USD 310 fare + USD 35 bag + USD 135 ground = USD 480

C is a fragile fallback, conditional on a ground journey that is currently only an assumption. A 15-minute delay would produce a 10:05 arrival, five minutes late. Do not present the deadline as reliably met or call C feasible without checking that transfer and the traveler's tolerance for the smaller buffer.

## Candidate D: following morning

- Departure: October 16 06:00 Westport, UTC−07:00 = October 16 13:00 UTC
- Arrival: October 16 14:30 Eastport, UTC−04:00 = October 16 18:30 UTC
- Flight elapsed time: 5 hours 30 minutes
- Venue arrival after the same 75-minute arrival/transfer allowance: October 16 15:45
- Deadline missed by 5 hours 45 minutes

Reject D before spending effort on a fare search: it fails the mandatory arrival time.

## Appropriate result to the traveler

“Check A first. Its supplied schedule gets you to the venue at 08:00, two hours before the deadline, and its estimated USD 510 total fits the cap. There is no verified bookable offer yet. I need the original provider's recovery offer and current seats, full fare terms and transfer details for A. B fails the supplied connection minimum, C has only ten minutes of estimated slack, and D is too late.”

No reservation, cancellation or payment follows from this comparison. A live task should replace scenario references with actual source links and retrieval times, refresh the preferred offer and obtain any required transaction approval.

## Reproduce the date checks

Python 3 with the standard-library timezone database is sufficient. This checks date arithmetic on invented inputs, not transport feasibility or live availability. Provider-local schedule times are validated by round-trip conversion; ambiguous times need an explicit offset choice. Processing and ground durations are added on the UTC timeline so a clock change does not stretch or shorten their elapsed length.

```python
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def local(value, zone, fold=None):
    naive = datetime.fromisoformat(value)
    if naive.tzinfo is not None:
        raise ValueError("This helper expects provider-local time without an offset")
    tz = ZoneInfo(zone)
    candidates = {}
    for choice in (0, 1):
        aware = naive.replace(tzinfo=tz, fold=choice)
        instant = aware.astimezone(timezone.utc)
        if instant.astimezone(tz).replace(tzinfo=None) == naive:
            candidates.setdefault(instant, aware)
    if not candidates:
        raise ValueError("Nonexistent local time: clarify the provider's schedule")
    if len(candidates) == 1:
        return next(iter(candidates.values()))
    if fold not in (0, 1):
        raise ValueError("Ambiguous local time: obtain the intended offset")
    return naive.replace(tzinfo=tz, fold=fold)


def elapsed(start, end):
    return end.astimezone(timezone.utc) - start.astimezone(timezone.utc)


def add_elapsed(start, duration):
    return (start.astimezone(timezone.utc) + duration).astimezone(start.tzinfo)


west = "America/Los_Angeles"
hub = "America/Chicago"
east = "America/New_York"
deadline = local("2026-10-16T10:00", east)
a_dep = local("2026-10-15T22:15", west)
a_arr = local("2026-10-16T06:45", east)
a_venue = add_elapsed(a_arr, timedelta(minutes=75))
assert elapsed(a_dep, a_arr) == timedelta(hours=5, minutes=30)
assert a_dep.astimezone(timezone.utc).isoformat() == "2026-10-16T05:15:00+00:00"
assert elapsed(a_venue, deadline) == timedelta(hours=2)
assert 430 + 35 + 45 == 510
assert 650 - 510 == 140

b_arr = local("2026-10-16T01:45", hub)
b_dep = local("2026-10-16T02:40", hub)
assert elapsed(b_arr, b_dep) == timedelta(minutes=55)
assert timedelta(minutes=65) - elapsed(b_arr, b_dep) == timedelta(minutes=10)

c_dep = local("2026-10-15T21:45", west)
c_arr = local("2026-10-16T06:20", east)
c_venue = add_elapsed(c_arr, timedelta(minutes=45) + timedelta(hours=2, minutes=45))
assert elapsed(c_dep, c_arr) == timedelta(hours=5, minutes=35)
assert c_venue.hour == 9 and c_venue.minute == 50
assert elapsed(c_venue, deadline) == timedelta(minutes=10)
assert elapsed(deadline, add_elapsed(c_venue, timedelta(minutes=15))) == timedelta(minutes=5)
assert 310 + 35 + 135 == 480

d_dep = local("2026-10-16T06:00", west)
d_arr = local("2026-10-16T14:30", east)
d_venue = add_elapsed(d_arr, timedelta(minutes=75))
assert elapsed(d_dep, d_arr) == timedelta(hours=5, minutes=30)
assert elapsed(deadline, d_venue) == timedelta(hours=5, minutes=45)
# Additional regression cases: schedule ambiguity and elapsed time across a clock change.
repeated_hour = local("2026-11-01T01:30", east, fold=0)
after_processing = add_elapsed(repeated_hour, timedelta(minutes=75))
assert after_processing.isoformat() == "2026-11-01T01:45:00-05:00"
assert elapsed(repeated_hour, after_processing) == timedelta(minutes=75)
for unclear in ("2026-11-01T01:30", "2026-03-08T02:30"):
    try:
        local(unclear, east)
    except ValueError:
        pass
    else:
        raise AssertionError("Ambiguous or nonexistent local time was accepted")
print("Fictional travel arithmetic checks passed")
```

Observed on 2026-10-01 in Linux, Python 3.12.14: the exact block above printed `Fictional travel arithmetic checks passed` and exited successfully. Run it by saving the block to a temporary Python file and invoking `python <file>`. The skill frontmatter validator also reported `Skill is valid!`. These checks do not validate connection policies, transfer estimates, fares or seats.
