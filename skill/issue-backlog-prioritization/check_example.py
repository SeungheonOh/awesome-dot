#!/usr/bin/env python3
"""Check the fixed fictional example; not a tracker or prioritization service."""
from copy import deepcopy
import json

ROWS = {
    "BK-11": {"values": (5, 4, 3), "requires": []},
    "BK-12": {"values": (4, 3, 3), "requires": ["BK-15"]},
    "BK-13": {"values": (4, None, 4), "requires": []},
    "BK-14": {"values": (3, 3, 4), "requires": []},
    "BK-15": {"values": (2, 2, 2), "requires": []},
    "BK-16": {"values": (3, 3, 4), "requires": []},
}
WEIGHTS = (3, 2, 1)


def bounds(values):
    assert all(v is None or (type(v) is int and 1 <= v <= 5) for v in values)
    return tuple(sum(w * (endpoint if v is None else v)
                     for w, v in zip(WEIGHTS, values)) for endpoint in (1, 5))


def readiness(rows, key):
    dependencies = rows[key]["requires"]
    # All present records are explicitly incomplete in this fixture.
    if any(d in rows for d in dependencies):
        return "blocked"
    if any(d not in rows for d in dependencies):
        return "unknown"
    return "ready"


def find_cycle(rows):
    active, done = [], set()

    def visit(key):
        if key in active:
            return active[active.index(key):] + [key]
        if key in done or key not in rows:
            return None
        active.append(key)
        for dependency in sorted(rows[key]["requires"]):
            cycle = visit(dependency)
            if cycle:
                return cycle
        active.pop()
        done.add(key)
        return None

    for key in sorted(rows):
        cycle = visit(key)
        if cycle:
            return cycle
    return None


def tiers(rows):
    exact = {key: bounds(row["values"])[0] for key, row in rows.items()
             if None not in row["values"]}
    return [sorted(key for key, value in exact.items() if value == score)
            for score in sorted(set(exact.values()), reverse=True)]


def main():
    before = deepcopy(ROWS)
    scores = {key: bounds(row["values"]) for key, row in ROWS.items()}
    assert scores == {"BK-11": (26, 26), "BK-12": (21, 21), "BK-13": (18, 26),
                      "BK-14": (19, 19), "BK-15": (12, 12), "BK-16": (19, 19)}
    # Exhaustively enumerate the only unknown rather than assuming endpoint math.
    possibilities = [bounds((4, u, 4))[0] for u in range(1, 6)]
    assert possibilities == [18, 20, 22, 24, 26]
    assert (min(possibilities), max(possibilities)) == scores["BK-13"]
    assert all(value > scores["BK-15"][1] for value in possibilities)
    assert any(value > 21 for value in possibilities) and any(value < 21 for value in possibilities)
    assert any(value < 19 for value in possibilities) and any(value > 19 for value in possibilities)
    assert max(possibilities) == 26 and not scores["BK-11"][0] > scores["BK-13"][1]
    expected_tiers = [["BK-11"], ["BK-12"], ["BK-14", "BK-16"], ["BK-15"]]
    assert tiers(ROWS) == expected_tiers
    assert tiers(dict(reversed(list(ROWS.items())))) == expected_tiers
    ready = {key: readiness(ROWS, key) for key in ROWS}
    assert ready == {"BK-11": "ready", "BK-12": "blocked", "BK-13": "ready",
                     "BK-14": "ready", "BK-15": "ready", "BK-16": "ready"}
    assert tiers({key: row for key, row in ROWS.items() if ready[key] == "ready"}) == [
        ["BK-11"], ["BK-14", "BK-16"], ["BK-15"]]
    assert find_cycle(ROWS) is None
    cycle_rows = deepcopy(ROWS)
    cycle_rows["BK-15"]["requires"] = ["BK-12"]
    cycle = find_cycle(cycle_rows)
    assert cycle == ["BK-12", "BK-15", "BK-12"]
    assert readiness(cycle_rows, "BK-12") == readiness(cycle_rows, "BK-15") == "blocked"
    assert readiness(cycle_rows, "BK-14") == "ready"
    missing = deepcopy(ROWS)
    missing["BK-11"]["requires"] = ["BK-99"]
    assert readiness(missing, "BK-11") == "unknown"
    self_cycle = deepcopy(ROWS)
    self_cycle["BK-15"]["requires"] = ["BK-15"]
    assert find_cycle(self_cycle) == ["BK-15", "BK-15"]
    assert ROWS == before and ROWS["BK-13"]["values"][1] is None
    print(json.dumps({"scores": scores, "known_score_tiers": expected_tiers,
                      "readiness": ready, "cycle_variant": cycle}, indent=2))
    print("PASS: arithmetic, bounds, partial order, ties, dependencies, cycle and missing reference")


if __name__ == "__main__":
    main()
