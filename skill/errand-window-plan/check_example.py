"""Check the fictional same-zone, fixed-departure example. No file or network I/O."""

from itertools import permutations


def minute(value):
    hour, minute_ = map(int, value.split(":"))
    return 60 * hour + minute_


def clock(value):
    return f"{value // 60:02d}:{value % 60:02d}"


POINTS = "SABCE"
ROWS = (
    (0, 12, 20, 15, 25),
    (14, 0, 18, 20, 16),
    (24, 28, 0, 8, 18),
    (17, 16, 15, 0, 14),
    (22, 19, 21, 16, 0),
)
TRAVEL = {(a, b): ROWS[i][j] for i, a in enumerate(POINTS)
          for j, b in enumerate(POINTS)}
STOPS = {
    "A": {"open": "09:00", "close": "10:05", "duration": 15},
    "B": {"open": "09:00", "close": "10:45", "duration": 20,
          "arrival_by": "10:05", "appointment": "10:10"},
    "C": {"open": "09:40", "close": "11:00", "duration": 10,
          "arrival_by": "10:45"},
}
REQUIRED = {"A", "B"}
BUFFER = 5


def simulate(order, stops=STOPS, travel=TRAVEL, wait_allowed=True):
    """Earliest service after a fixed 09:00 departure; all waits allowed by default."""
    now, previous, events = minute("09:00"), "S", []
    for label in order:
        stop = stops[label]
        if stop.get("closed"):
            return {"failure": f"{label} is closed"}
        if stop.get("open") is None or stop.get("close") is None:
            return {"unresolved": f"{label} hours unknown"}
        if stop.get("duration") is None:
            return {"unresolved": f"{label} duration unknown"}
        if (previous, label) not in travel:
            return {"unresolved": f"{previous}->{label} travel unknown"}
        arrival = now + travel[previous, label] + BUFFER
        if "arrival_by" in stop and arrival > minute(stop["arrival_by"]):
            return {"failure": f"{label} arrival {clock(arrival)} > {stop['arrival_by']}"}
        start = max(arrival, minute(stop["open"]))
        if "appointment" in stop:
            appointment = minute(stop["appointment"])
            if start > appointment:
                return {"failure": f"{label} cannot start at {stop['appointment']}"}
            start = appointment
        wait = start - arrival
        if wait and not wait_allowed:
            return {"failure": f"{label} requires {wait}m waiting in this timing"}
        finish = start + stop["duration"]
        if finish > minute(stop["close"]):
            return {"failure": f"{label} finish {clock(finish)} > {stop['close']}"}
        events.append((label, arrival, wait, start, finish))
        previous, now = label, finish
    if (previous, "E") not in travel:
        return {"unresolved": f"{previous}->E travel unknown"}
    end = now + travel[previous, "E"] + BUFFER
    if end > minute("11:15"):
        return {"failure": f"E arrival {clock(end)} > 11:15"}
    return {"events": events, "end": end}


def feasible(result):
    return "end" in result


# Enumerate every required-only and every all-stop order: 2! + 3! = 8.
candidates = [(order, simulate(order)) for chosen in ("AB", "ABC")
              for order in permutations(chosen)]
assert len(candidates) == 8
assert len(TRAVEL) == 25 and all(TRAVEL[p, p] == 0 for p in POINTS)
assert TRAVEL["A", "B"] != TRAVEL["B", "A"]
assert all(REQUIRED <= set(order) for order, _ in candidates)
assert ["".join(order) for order, result in candidates if feasible(result)] == ["AB", "ABC"]

chosen = simulate("ABC")
assert chosen["events"] == [
    ("A", minute("09:17"), 0, minute("09:17"), minute("09:32")),
    ("B", minute("09:55"), 15, minute("10:10"), minute("10:30")),
    ("C", minute("10:43"), 0, minute("10:43"), minute("10:53")),
]
assert chosen["end"] == minute("11:12")
assert simulate("AB")["end"] == minute("10:53")
assert simulate("BAC")["failure"] == "A finish 11:18 > 10:05"
assert simulate("ACB")["failure"] == "B arrival 10:27 > 10:05"

# Arrival cutoff is inclusive; C may finish after it, but before closing.
two_late = dict(TRAVEL)
two_late["B", "C"] += 2
assert simulate("ABC", travel=two_late)["end"] == minute("11:14")
three_late = dict(TRAVEL)
three_late["B", "C"] += 3
assert simulate("ABC", travel=three_late)["failure"] == "C arrival 10:46 > 10:45"

unknown = {label: dict(stop) for label, stop in STOPS.items()}
unknown["C"]["open"] = None
assert simulate("ABC", stops=unknown)["unresolved"] == "C hours unknown"
assert feasible(simulate("AB", stops=unknown))
closed = {label: dict(stop) for label, stop in STOPS.items()}
closed["A"]["closed"] = True
assert simulate("AB", stops=closed)["failure"] == "A is closed"
missing = dict(TRAVEL)
del missing["A", "B"]
assert simulate("ABC", travel=missing)["unresolved"] == "A->B travel unknown"
assert simulate("ABC", wait_allowed=False)["failure"] == "B requires 15m waiting in this timing"
missing_duration = {label: dict(stop) for label, stop in STOPS.items()}
missing_duration["A"]["duration"] = None
assert simulate("AB", stops=missing_duration)["unresolved"] == "A duration unknown"

print("PASS: complete matrix; 8 orders; feasible AB and ABC; cutoff, waiting, closure and unknown checks")
for label, arrival, wait, start, finish in chosen["events"]:
    print(f"{label}: arrive {clock(arrival)}, wait {wait}m, service {clock(start)}-{clock(finish)}")
print(f"E: arrive {clock(chosen['end'])}; required-only E: {clock(simulate('AB')['end'])}")
print(f"Rejected BAC: {simulate('BAC')['failure']}")
