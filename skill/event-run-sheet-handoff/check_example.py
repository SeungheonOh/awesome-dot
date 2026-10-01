#!/usr/bin/env python3
"""Validate the fictional supplied schedule, not generate or optimize one.

All tasks are non-preemptive. Named people and listed resources have capacity
one. Occupancy is [start, finish); availability and deadlines permit equality.
The lower-bound check ignores resource contention: it can prove one timing
contradiction but cannot establish full feasibility.
"""
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from itertools import combinations
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("Europe/London")
DAY = "2026-11-14"


def at(hhmm):
    # This fixture date/time is unambiguous. Not an arbitrary DST-time parser.
    return datetime.fromisoformat(f"{DAY}T{hhmm}:00").replace(tzinfo=ZONE)


ACCESS = at("14:00")
DEPARTURE = at("16:45")
AVAILABILITY = {name: ((ACCESS, DEPARTURE),)
                for name in ("Priya", "Theo", "Jo", "PA", "desk")}


@dataclass(frozen=True)
class Task:
    id: str
    phase: str
    label: str
    start: datetime
    finish: datetime
    minutes: int | None
    predecessors: tuple = ()  # (task ID, separately supplied lag in minutes)
    people: tuple = ()
    resources: tuple = ()


class UnresolvedInput(ValueError):
    pass


class InvalidModel(ValueError):
    pass


def task(id, phase, label, start, finish, minutes, predecessors, people, resources=()):
    return Task(id, phase, label, at(start), at(finish), minutes,
                tuple((p, 0) for p in predecessors), tuple(people), tuple(resources))


TASKS = (
    task("S1", "setup", "Room setup", "14:00", "14:25", 25, (), ("Priya",)),
    task("S2", "setup", "Audio check", "14:25", "14:40", 15, ("S1",), ("Theo",), ("PA",)),
    task("S3", "setup", "Desk setup", "14:25", "14:40", 15, ("S1",), ("Jo",), ("desk",)),
    task("S4", "setup", "Readiness review", "14:40", "14:50", 10, ("S2", "S3"), ("Priya", "Theo", "Jo")),
    task("O1", "opening", "Door briefing", "14:50", "15:00", 10, ("S4",), ("Priya", "Jo"), ("desk",)),
    task("O2", "opening", "Admissions", "15:00", "15:15", 15, ("O1",), ("Jo",), ("desk",)),
    task("P1", "program", "Welcome", "15:15", "15:20", 5, ("O2",), ("Priya",), ("PA",)),
    task("P2", "program", "Demonstration", "15:20", "16:00", 40, ("P1",), ("Theo",), ("PA",)),
    task("P3", "program", "Questions", "16:00", "16:15", 15, ("P2",), ("Priya", "Theo"), ("PA",)),
    task("C1", "close", "Equipment pack", "16:15", "16:35", 20, ("P3",), ("Theo", "Jo"), ("PA",)),
    task("C2", "close", "Room restoration", "16:15", "16:35", 20, ("P3",), ("Priya",)),
    task("C3", "close", "Handback/departure", "16:35", "16:45", 10, ("C1", "C2"), ("Priya", "Theo", "Jo")),
)


def preflight(tasks):
    by_id = {item.id: item for item in tasks}
    if len(by_id) != len(tasks):
        raise InvalidModel("duplicate task ID")
    for item in tasks:
        if item.minutes is None:
            raise UnresolvedInput(f"{item.id}: unknown supplied duration")
        if type(item.minutes) is not int or item.minutes < 0:
            raise InvalidModel(f"{item.id}: duration must be a nonnegative integer")
        for value in (item.start, item.finish):
            if value.utcoffset() is None:
                raise InvalidModel(f"{item.id}: timestamp needs an explicit time zone")
        if len(set(item.people)) != len(item.people) or len(set(item.resources)) != len(item.resources):
            raise InvalidModel(f"{item.id}: duplicated person or resource")
        for previous, lag in item.predecessors:
            if previous not in by_id:
                raise InvalidModel(f"{item.id}: unknown predecessor {previous}")
            if type(lag) is not int or lag < 0:
                raise InvalidModel(f"{item.id}: lag must be a nonnegative integer")
    active, visited, ordered = [], set(), []

    def visit(id):
        if id in active:
            cycle = active[active.index(id):] + [id]
            raise InvalidModel("dependency cycle: " + " -> ".join(cycle))
        if id in visited:
            return
        active.append(id)
        for previous, _ in by_id[id].predecessors:
            visit(previous)
        active.pop()
        visited.add(id)
        ordered.append(id)

    for id in by_id:
        visit(id)
    return by_id, ordered


def validate(tasks, availability=AVAILABILITY):
    by_id, _ = preflight(tasks)
    problems = []
    for item in tasks:
        if item.finish - item.start != timedelta(minutes=item.minutes):
            problems.append(("duration", item.id))
        if item.start < ACCESS:
            problems.append(("access", item.id))
        if item.finish > DEPARTURE:
            problems.append(("departure", item.id))
        for previous, lag in item.predecessors:
            if item.start < by_id[previous].finish + timedelta(minutes=lag):
                problems.append(("dependency", f"{previous} -> {item.id}"))
        for occupied in item.people + item.resources:
            if occupied not in availability:
                raise UnresolvedInput(f"availability missing for {occupied}")
            if not any(begin <= item.start and item.finish <= end
                       for begin, end in availability[occupied]):
                problems.append(("availability", f"{item.id}: {occupied}"))
    for id, field, anchor in (("O2", "start", at("15:00")),
                              ("P1", "start", at("15:15")),
                              ("P3", "finish", at("16:15"))):
        if id not in by_id:
            raise InvalidModel(f"missing anchored task {id}")
        if getattr(by_id[id], field) != anchor:
            problems.append(("anchor", f"{id}.{field}"))
    for a, b in combinations(tasks, 2):
        overlap = min(a.finish, b.finish) - max(a.start, b.start)
        if overlap <= timedelta(0):
            continue
        for category, left, right in (("role", a.people, b.people),
                                      ("resource", a.resources, b.resources)):
            for occupied in sorted(set(left) & set(right)):
                minutes = int(overlap.total_seconds() // 60)
                problems.append((category, f"{a.id}/{b.id}: {occupied}, {minutes} minutes"))
    return problems


def change(id, **fields):
    return tuple(replace(item, **fields) if item.id == id else item for item in TASKS)


def dependency_lower_bounds(tasks, releases):
    """Earliest possible finishes under only releases and predecessor lags.

    Ignoring role/resource contention and other constraints relaxes the model.
    A relaxed earliest finish beyond a hard deadline proves a contradiction.
    A relaxed finish meeting a deadline does NOT establish a feasible schedule.
    """
    by_id, order = preflight(tasks)
    bounds = {}
    for id in order:
        item = by_id[id]
        first = max([ACCESS, releases.get(id, ACCESS)] +
                    [bounds[p] + timedelta(minutes=lag) for p, lag in item.predecessors])
        bounds[id] = first + timedelta(minutes=item.minutes)
    return bounds


def expect_error(kind, text, function):
    try:
        function()
    except kind as error:
        assert text in str(error), str(error)
    else:
        raise AssertionError(f"expected {kind.__name__}: {text}")


def readback_example(content=None):
    if content is None:
        content = Path(__file__).with_name("example.md").read_text(encoding="utf-8")
    actual = {}
    lines = content.splitlines()
    headers = [i for i, line in enumerate(lines) if line.startswith("| ID / phase | Task |")]
    assert len(headers) == 1, "missing or repeated run-sheet table"
    start = headers[0]
    assert lines[start + 1].startswith("|---"), "missing run-sheet table separator"
    expected_ids = {item.id for item in TASKS}
    for line in lines[start + 2:]:
        if not line.startswith("| "):
            break
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        id = cells[0].split(" / ")[0]
        assert id in expected_ids, f"unknown documented task {id}"
        assert id not in actual, f"duplicate documented row {id}"
        actual[id] = cells
    assert set(actual) == expected_ids, "missing or extra fixture row"
    for item in TASKS:
        cells = actual[item.id]
        assert len(cells) == 8, (item.id, cells)
        assert cells[0] == f"{item.id} / {item.phase}"
        assert cells[1] == item.label
        assert cells[2] == f"{item.start:%H:%M}–{item.finish:%H:%M}"
        assert int(cells[3]) == item.minutes
        assert cells[4] == (", ".join(p for p, _ in item.predecessors) or "—")
        assert cells[5] == ", ".join(item.people) + " / " + (", ".join(item.resources) or "—")
    assert "Ready for review" in actual["S4"][6]
    assert "Reported complete" in actual["S2"][7]
    assert "independent acceptance pending" in actual["S2"][7]
    assert "Verified complete" in actual["S1"][7]
    assert "unknown recipient" in actual["C3"][6]
    for id in ("S4", "O1", "O2", "P1", "P2", "P3", "C1", "C2", "C3"):
        assert actual[id][7].startswith("Not started")
    assert "Europe/London, UTC+00:00" in content
    for literal in ("No task starts before 14:00", "O2 starts exactly 15:00",
                    "P1 starts exactly 15:15", "P3 finishes exactly 16:15",
                    "C3 finishes no later than 16:45"):
        assert literal in content


def main():
    assert ACCESS.utcoffset() == timedelta(0)
    assert ACCESS.astimezone(timezone.utc).isoformat() == "2026-11-14T14:00:00+00:00"
    assert not validate(TASKS)
    print("PASS: baseline intervals, anchors, dependencies and capacity")

    expect_error(UnresolvedInput, "S2: unknown supplied duration",
                 lambda: validate(change("S2", minutes=None)))
    print("PASS: unknown duration remains unresolved")

    expect_error(InvalidModel, "dependency cycle",
                 lambda: validate(change("S1", predecessors=(("C3", 0),))))
    print("PASS: dependency cycle rejected")

    assert ("role", "S2/S3: Jo, 15 minutes") in validate(change("S2", people=("Theo", "Jo")))
    print("PASS: shared-role overlap rejected (15 minutes)")

    assert not validate(TASKS)  # Nominal adjacency and deadline equality allowed.
    assert ("dependency", "S4 -> O1") in validate(change("O1", predecessors=(("S4", 1),)))
    print("PASS: explicit boundary equality and lag violation")

    assert ("resource", "S2/S3: PA, 15 minutes") in validate(change("S3", resources=("PA",)))
    print("PASS: exclusive-resource overlap rejected")

    narrowed = dict(AVAILABILITY, Priya=((at("14:01"), DEPARTURE),))
    assert ("availability", "S1: Priya") in validate(TASKS, narrowed)
    print("PASS: availability violation rejected")

    bounds = dependency_lower_bounds(TASKS, {"C1": at("16:25")})
    assert bounds["C1"] == at("16:45")
    assert bounds["C3"] == at("16:55")
    assert bounds["C3"] - DEPARTURE == timedelta(minutes=10)
    print("PASS: changed release-time model has a 16:55 lower bound")

    readback_example()
    print("PASS: example rows read back and agree with fixture")
    content = Path(__file__).with_name("example.md").read_text(encoding="utf-8")
    extra = ("| X1 / extra | Conflicting extra task | 14:25–14:40 | 15 | S1 | "
             "Jo / desk | Proposed | Not started |\n")
    changed = content.replace("| S1 / setup |", extra + "| S1 / setup |", 1)
    expect_error(AssertionError, "unknown documented task X1", lambda: readback_example(changed))
    print("PASS: unknown documented run-sheet task rejected")
    print("10 checks passed; no schedule optimization or live-event assurance")


if __name__ == "__main__":
    main()
