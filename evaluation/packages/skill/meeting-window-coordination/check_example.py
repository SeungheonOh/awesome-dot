#!/usr/bin/env python3
"""Fictional interval checks; standard library only, no network or calendar writes."""
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc
MINUTE = timedelta(minutes=1)


def local(text, zone, fold=None):
    """Resolve a full local ISO date/time; reject gaps and unchosen folds."""
    wall = datetime.fromisoformat(text)
    if wall.tzinfo is not None:
        raise ValueError("Supply a local clock time without an offset")
    tz = ZoneInfo(zone)
    choices = {}
    for candidate_fold in (0, 1):
        candidate = wall.replace(tzinfo=tz, fold=candidate_fold)
        instant = candidate.astimezone(UTC)
        if instant.astimezone(tz).replace(tzinfo=None) == wall:
            choices[candidate_fold] = instant
    if not choices:
        raise ValueError("Nonexistent local time")
    if fold is None:
        distinct = set(choices.values())
        if len(distinct) != 1:
            raise ValueError("Ambiguous local time: choose an occurrence")
        return distinct.pop()
    if fold not in choices:
        raise ValueError("Invalid occurrence")
    return choices[fold]


def interval(start, end, zone):
    pair = (local(start, zone), local(end, zone))
    if pair[0] >= pair[1]:
        raise ValueError("An interval must have positive elapsed duration")
    return pair


def merge(intervals):
    result = []
    for start, end in sorted(intervals):
        if start >= end:
            raise ValueError("Invalid interval")
        if result and start <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], end))
        else:
            result.append((start, end))
    return result


def subtract(windows, busy):
    result = []
    blocks = merge(busy)
    for start, end in merge(windows):
        cursor = start
        for b_start, b_end in blocks:
            if b_end <= cursor or b_start >= end:
                continue
            if b_start > cursor:
                result.append((cursor, b_start))
            cursor = max(cursor, min(b_end, end))
        if cursor < end:
            result.append((cursor, end))
    return result


def intersect(left, right):
    return merge([
        (max(a, c), min(b, d))
        for a, b in left for c, d in right
        if max(a, c) < min(b, d)
    ])


def closed_intersect(left, right):
    """Intersect CLOSED start ranges without discarding singleton starts."""
    intersections = sorted((max(a, c), min(b, d))
                           for a, b in left for c, d in right
                           if max(a, c) <= min(b, d))
    result = []
    for start, end in intersections:
        if result and start <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], end))
        else:
            result.append((start, end))
    return result


def start_ranges(people, duration, before, after):
    """Common buffer lengths, per-person work policy; CLOSED start ranges."""
    if not people or duration <= timedelta(0) or min(before, after) < timedelta(0):
        raise ValueError("People, positive duration and nonnegative buffers required")
    unknown = [p["name"] for p in people if p["busy"] is None]
    if unknown:
        return [], unknown
    common = None
    for person in people:
        work = merge(person["work"])
        # If wider coverage was not supplied, no time outside work is assumed free.
        coverage = merge(person.get("coverage", work))
        inside = person.get("buffers_inside_work", True)
        if type(inside) is not bool:
            raise ValueError("Buffer working-window policy must be explicit")
        checked = intersect(work, coverage) if inside else coverage
        free = subtract(checked, person["busy"])
        buffered = [(a + before, b - duration - after) for a, b in free
                    if a + before <= b - duration - after]
        if inside:
            ranges = buffered
        else:
            bodies = [(a, b - duration) for a, b in work if a <= b - duration]
            ranges = closed_intersect(bodies, buffered)
        common = ranges if common is None else closed_intersect(common, ranges)
    return common, []


def valid(start, duration, before, after, people):
    """Independent direct check against raw busy, work and known coverage."""
    a, b = start - before, start + duration + after
    for p in people:
        if p["busy"] is None:
            return False
        work = merge(p["work"])
        coverage = merge(p.get("coverage", work))
        if not any(w_start <= start and start + duration <= w_end for w_start, w_end in work):
            return False
        if not any(c_start <= a and b <= c_end for c_start, c_end in coverage):
            return False
        if p.get("buffers_inside_work", True) and not any(w_start <= a and b <= w_end for w_start, w_end in work):
            return False
        if any(a < busy_end and busy_start < b for busy_start, busy_end in p["busy"]):
            return False
    return True


def must_reject(text, zone, message):
    try:
        local(text, zone)
    except ValueError as error:
        assert message in str(error), error
    else:
        raise AssertionError(f"Expected rejection for {text} in {zone}")


def main():
    london, new_york, singapore = "Europe/London", "America/New_York", "Asia/Singapore"
    people = [
        {"name": "Noor Vale", "zone": london,
         "work": [interval("2026-10-28T12:00", "2026-10-28T17:00", london)],
         "busy": [interval("2026-10-28T12:00", "2026-10-28T12:15", london)]},
        {"name": "Eli Marlow", "zone": new_york,
         "work": [interval("2026-10-28T08:00", "2026-10-28T13:00", new_york)],
         "busy": [interval("2026-10-28T09:30", "2026-10-28T10:15", new_york)]},
        {"name": "Sana Ito", "zone": singapore,
         "work": [interval("2026-10-28T20:00", "2026-10-29T00:00", singapore)],
         "busy": [interval("2026-10-28T23:30", "2026-10-29T00:00", singapore)]},
    ]
    duration, before, after = 45 * MINUTE, 15 * MINUTE, 15 * MINUTE
    starts, unknown = start_ranges(people, duration, before, after)
    expected = [datetime(2026, 10, 28, hour, 30, tzinfo=UTC) for hour in (12, 14)]
    assert not unknown and starts == [(s, s) for s in expected], starts
    assert [s.astimezone(ZoneInfo(p["zone"])).utcoffset()
            for p in people for s in expected[:1]] == [timedelta(0), timedelta(hours=-4), timedelta(hours=8)]

    # Direct inequalities catch both endpoint handling and accidental double padding.
    for start in expected:
        assert valid(start, duration, before, after, people)
        assert not valid(start - MINUTE, duration, before, after, people)
        assert not valid(start + MINUTE, duration, before, after, people)
    # These pass/fail claims concern this fixture, not every possible meeting.
    assert start_ranges(people, 46 * MINUTE, before, after) == ([], [])
    missing = [{**p, "busy": None if p["name"] == "Sana Ito" else p["busy"]} for p in people]
    assert start_ranges(missing, duration, before, after) == ([], ["Sana Ito"])
    assert not valid(expected[0], duration, before, after, missing)
    # A working-window boundary is hard even if there are no events at all.
    boundary = [{**people[0], "busy": []}]
    assert not valid(local("2026-10-28T12:00", london), duration, before, after, boundary)
    assert valid(local("2026-10-28T12:15", london), duration, before, after, boundary)
    # Outside-window permission differs from inside-window policy, but never invents coverage.
    nine = datetime(2026, 10, 28, 9, tzinfo=UTC)
    work_end = nine + 60 * MINUTE
    outside = {"name": "Boundary case", "work": [(nine, work_end)], "busy": [],
               "coverage": [(nine - 15 * MINUTE, work_end + 15 * MINUTE)],
               "buffers_inside_work": False}
    half_hour = 30 * MINUTE
    assert start_ranges([outside], half_hour, before, after) == ([(nine, nine + 30 * MINUTE)], [])
    inside = {**outside, "buffers_inside_work": True}
    assert start_ranges([inside], half_hour, before, after) == ([(nine + 15 * MINUTE, nine + 15 * MINUTE)], [])
    assert not valid(nine, half_hour, before, after, [inside])
    assert valid(nine, half_hour, before, after, [outside])
    no_margin = {k: v for k, v in outside.items() if k != "coverage"}
    assert start_ranges([no_margin], half_hour, before, after) == ([(nine + 15 * MINUTE, nine + 15 * MINUTE)], [])
    assert not valid(nine, half_hour, before, after, [no_margin])
    busy_margin = {**outside, "busy": [(work_end, work_end + 10 * MINUTE)]}
    assert start_ranges([busy_margin], half_hour, before, after) == ([(nine, nine + 15 * MINUTE)], [])
    assert valid(nine + 15 * MINUTE, half_hour, before, after, [busy_margin])
    assert not valid(nine + 16 * MINUTE, half_hour, before, after, [busy_margin])
    coverage_gap = {**outside, "coverage": [(nine - 15 * MINUTE, nine),
                                            (nine + 5 * MINUTE, work_end + 15 * MINUTE)]}
    assert start_ranges([coverage_gap], half_hour, before, after) == ([(nine + 20 * MINUTE, nine + 30 * MINUTE)], [])
    assert not valid(nine + 15 * MINUTE, half_hour, before, after, [coverage_gap])
    assert start_ranges([outside, inside], half_hour, before, after) == ([(nine + 15 * MINUTE, nine + 15 * MINUTE)], [])
    # Union and subtraction must handle overlapping blocks and exact contact.
    a = datetime(2026, 10, 28, 12, tzinfo=UTC)
    assert subtract([(a, a + 90 * MINUTE)], [
        (a, a + 15 * MINUTE), (a + 10 * MINUTE, a + 30 * MINUTE),
        (a + 60 * MINUTE, a + 90 * MINUTE),
    ]) == [(a + 30 * MINUTE, a + 60 * MINUTE)]
    must_reject("2026-10-25T01:30", london, "Ambiguous")
    must_reject("2026-03-29T01:30", london, "Nonexistent")
    first = local("2026-10-25T01:30", london, fold=0)
    second = local("2026-10-25T01:30", london, fold=1)
    assert first == datetime(2026, 10, 25, 0, 30, tzinfo=UTC)
    assert second - first == timedelta(hours=1)

    print("PASS: two exact feasible starts with 15-minute buffers against raw busy intervals")
    for start in expected:
        print(f"UTC: {start.isoformat()} to {(start + duration).isoformat()}")
        for p in people:
            tz = ZoneInfo(p["zone"])
            print(f"  {p['name']} ({p['zone']}): {start.astimezone(tz).isoformat()} to {(start + duration).astimezone(tz).isoformat()}")
    print("PASS: offsets, endpoint boundaries, 46-minute no-intersection, unknown-calendar branch")
    print("PASS: working-window buffer, overlapping busy union, ambiguous/skipped local times")
    print("PASS: inside/outside buffer policies, known coverage margins, gaps and raw outside busy time")
    print("LIMIT: synthetic interval checks only; no provider access, invitations, identity resolution or concurrency tested")


if __name__ == "__main__":
    main()
