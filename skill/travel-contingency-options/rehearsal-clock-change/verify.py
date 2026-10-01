#!/usr/bin/env python3
"""Check this fictional packet's arithmetic offline using Python's IANA zones."""

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

UTC = timezone.utc
PACKET = Path(__file__).with_name("input.md").read_text(encoding="utf-8")
CHECKS = 0


def check(actual, expected, label):
    global CHECKS
    if actual != expected:
        raise AssertionError(f"{label}: got {actual!r}; expected {expected!r}")
    CHECKS += 1


def capture(pattern, text=PACKET):
    match = re.search(pattern, text)
    if not match:
        raise ValueError(f"Required fixture field missing: {pattern}")
    return match.group(1)


def instants(wall, zone_name):
    """Return every valid UTC instant; reject skipped times by round-tripping."""
    wall = datetime.fromisoformat(wall)
    zone = ZoneInfo(zone_name)
    result = set()
    for fold in (0, 1):
        candidate = wall.replace(tzinfo=zone, fold=fold).astimezone(UTC)
        if candidate.astimezone(zone).replace(tzinfo=None) == wall:
            result.add(candidate)
    if not result:
        raise ValueError(f"Nonexistent local time: {wall} in {zone_name}")
    return sorted(result)


def explicit(wall, zone_name, offset):
    candidate = datetime.fromisoformat(wall + offset).astimezone(UTC)
    if candidate not in instants(wall, zone_name):
        raise ValueError(f"Offset {offset} invalid for {wall} in {zone_name}")
    return candidate


def clock(value):
    return value.strftime("%H:%M")


def minutes(later, earlier):
    # Callers pass UTC-aware instants, never subtract local wall-clock values.
    return int((later - earlier).total_seconds() / 60)


def timestamp(section, field):
    match = re.search(
        rf"- {field}: ([0-9-]+ [0-9:]+), ([A-Za-z_]+/[A-Za-z_]+), offset ([+-][0-9:]+)",
        section,
    )
    if not match:
        raise ValueError(f"Missing explicit timestamp: {field}")
    return explicit(*match.groups())


def main():
    origin = capture(r"origin terminal, which uses (\S+)")
    destination = capture(r"destination venue uses ([A-Za-z_]+/[A-Za-z_]+)")
    zone = ZoneInfo(destination)
    boundary_wall = capture(r"Departure cannot be before ([0-9-]+ [0-9:]+)")
    boundary_choices = instants(boundary_wall, origin)
    check(len(boundary_choices), 1, "Earliest departure is unambiguous")
    boundary = boundary_choices[0]
    deadline_wall = capture(r"Hard arrival deadline: ([0-9-]+ [0-9:]+)")
    deadline_offset = capture(r"Hard arrival deadline: .*?UTC offset ([+-][0-9:]+)")
    deadline = explicit(deadline_wall, destination, deadline_offset)
    buffer = int(capture(r"Prefer at least (\d+) minutes"))
    budget = int(capture(r"Maximum new spending is USD (\d+)"))
    check(clock(boundary), "04:00", "UTC departure boundary")
    check(clock(deadline), "08:15", "UTC deadline")
    check(clock(deadline - timedelta(minutes=buffer)), "07:55", "Preferred UTC target")
    check(budget, 500, "Unadjusted spending limit")

    # Expected tuples: depart, terminal, processing end, venue (UTC), local venue,
    # flight minutes, whole-journey minutes, slack, payable now, budget headroom.
    expected = {
        "A": ("04:10", "06:30", "07:00", "07:45", "2026-11-01T01:45-06:00", 140, 215, 30, 485, 15),
        "B": ("04:40", "07:10", "07:30", "08:00", "2026-11-01T02:00-06:00", 150, 200, 15, 425, 75),
    }
    results = {}
    sections = {}
    for name in "ABC":
        match = re.search(rf"## Candidate {name}[^\n]*\n(.*?)(?=\n## |\Z)", PACKET, re.S)
        if not match:
            raise ValueError(f"Missing fixture section: Candidate {name}")
        sections[name] = match.group(1)

    for name in "AB":
        section = sections[name]
        depart = timestamp(section, "Origin departure")
        terminal = timestamp(section, "Destination-terminal arrival")
        processing = int(capture(r"Arrival processing: (\d+) elapsed minutes", section))
        ground = int(capture(r"Ground transfer to venue: (\d+) elapsed minutes", section))
        processed = terminal + timedelta(minutes=processing)
        venue = processed + timedelta(minutes=ground)
        fare = int(capture(r"Fare USD (\d+)", section))
        bag = int(capture(r"checked bag USD (\d+)", section))
        transfer = int(capture(r"full ground transfer USD (\d+)", section))
        total = fare + bag + transfer  # Unconfirmed refunds are never spendable.
        slack = minutes(deadline, venue)
        result = (clock(depart), clock(terminal), clock(processed), clock(venue),
                  venue.astimezone(zone).isoformat(timespec="minutes"),
                  minutes(terminal, depart), minutes(venue, depart), slack, total, budget - total)
        check(result, expected[name], f"Candidate {name} timeline and full cost")
        check(depart >= boundary, True, f"Candidate {name} departure boundary")
        check(slack >= 0, True, f"Candidate {name} hard deadline")
        check(slack >= buffer, name == "A", f"Candidate {name} preferred buffer")
        check(total <= budget, True, f"Candidate {name} budget")
        results[name] = (terminal, venue)
        print(f"{name}: depart {clock(depart)} UTC; terminal {clock(terminal)} UTC; "
              f"venue {clock(venue)} UTC; slack {slack} min; USD {total}; headroom USD {budget - total}")

    check(minutes(results["B"][0], results["A"][0]), 40, "A terminal advantage")
    check(minutes(results["B"][1], results["A"][1]), 15, "A venue advantage")
    check(clock(results["A"][0].astimezone(zone)) > clock(results["B"][0].astimezone(zone)),
          True, "A's earlier instant displays a later terminal clock")

    section = sections["C"]
    depart = timestamp(section, "Origin departure")
    wall = capture(r"Destination-terminal arrival: ([0-9-]+ [0-9:]+)", section)
    missing_zone = capture(r"Destination-terminal arrival: [^,]+, ([A-Za-z_]+/[A-Za-z_]+)", section)
    check("offset/fold is missing" in section, True, "C occurrence stays unresolved")
    check("checked-bag price is missing" in section, True, "C bag cost stays unresolved")
    check(depart >= boundary, True, "Candidate C departure boundary")
    processing = int(capture(r"Arrival processing: (\d+) elapsed minutes", section))
    ground = int(capture(r"Ground transfer to venue: (\d+) elapsed minutes", section))
    branches = []
    for terminal in instants(wall, missing_zone):
        processed = terminal + timedelta(minutes=processing)
        venue = processed + timedelta(minutes=ground)
        branches.append((clock(terminal), clock(processed), clock(venue),
                         venue.astimezone(zone).isoformat(timespec="minutes"),
                         minutes(terminal, depart), minutes(venue, depart), minutes(deadline, venue)))
    check(branches, [
        ("06:10", "06:30", "07:15", "2026-11-01T01:15-06:00", 125, 190, 60),
        ("07:10", "07:30", "08:15", "2026-11-01T02:15-06:00", 185, 250, 0),
    ], "Both conditional C branches; no occurrence selected")
    known = int(capture(r"Fare USD (\d+)", section)) + int(capture(r"full ground transfer USD (\d+)", section))
    check(known, 360, "C known cost, excluding unknown bag")
    check(budget - known, 140, "C maximum bag charge for budget compliance")
    check(int(capture(r"possible USD (\d+) refund is unconfirmed")), 150, "Refund remains unconfirmed")
    print("C: unselected terminal branches 06:10/07:10 UTC; venue branches 07:15/08:15 UTC; USD 360 + unknown bag")
    print(f"PASS: {CHECKS} fixture checks; IANA offsets and UTC elapsed arithmetic; no live travel verification")


if __name__ == "__main__":
    try:
        main()
    except ZoneInfoNotFoundError as error:
        raise SystemExit(f"IANA timezone data unavailable: {error}. Use Python 3.9+ with America/New_York and America/Chicago zone data.")
