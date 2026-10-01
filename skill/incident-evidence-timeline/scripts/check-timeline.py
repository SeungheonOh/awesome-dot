#!/usr/bin/env python3
"""Offline arithmetic/identity checks for the bundled fictional packet only."""

import copy
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys


def utc(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("Timestamp has no explicit offset")
    return parsed.astimezone(timezone.utc)


def event_interval(event, sources):
    skew = sources[event["source"]]["skew_seconds"]
    try:
        time = utc(event["event_time"])
    except ValueError:
        return None
    if skew is None:
        return None
    low, high = skew
    if low > high:
        raise ValueError("Reversed clock bounds")
    # Fixture contract: no additional timestamp representation uncertainty.
    return time - timedelta(seconds=high), time - timedelta(seconds=low)


def relation(left, right):
    if left is None or right is None:
        return "unknown"
    if left[1] < right[0]:
        return "before"
    if right[1] < left[0]:
        return "after"
    return "unresolved"


def deduplicate(events, sources):
    groups = {}
    payloads = {}
    for event in events:
        source = sources[event["source"]]
        identity = source["origin"], source["namespace"], event["event_id"]
        payload = {key: value for key, value in event.items()
                   if key not in {"row", "source", "ingested_at"}}
        if identity in payloads and payload != payloads[identity]:
            raise ValueError("Conflicting payloads under one event identity")
        payloads[identity] = payload
        groups.setdefault(identity, []).append(event)
    return list(groups.values())


def coverage(source, window):
    if source["coverage"] is None:
        return None
    start, end = map(utc, window)
    spans = []
    for raw_start, raw_end in source["coverage"]:
        left, right = utc(raw_start), utc(raw_end)
        if right < left:
            raise ValueError("Reversed coverage interval")
        left, right = max(start, left), min(end, right)
        if left < right:
            spans.append((left, right))
    merged = []
    for left, right in sorted(spans):
        if merged and left <= merged[-1][1]:
            merged[-1] = merged[-1][0], max(merged[-1][1], right)
        else:
            merged.append((left, right))
    gaps, cursor = [], start
    for left, right in merged:
        if cursor < left:
            gaps.append((cursor, left))
        cursor = right
    if cursor < end:
        gaps.append((cursor, end))
    seconds = sum((right - left).total_seconds() for left, right in merged)
    return seconds, gaps


def percent(row):
    # Same-unit, same-population, disjoint-window compatibility is supplied
    # by this fixture's metric contract, not established by this helper.
    numerator, denominator = row["errors_5xx"], row["attempts"]
    if denominator is None or denominator == 0:
        return None
    if not 0 <= numerator <= denominator:
        raise ValueError("Invalid fixture count relationship")
    return 100 * numerator / denominator


def stamp(value):
    return value.isoformat().replace("+00:00", "Z")


def main():
    path = Path(__file__).resolve().parents[1] / "references/fictional-evidence.json"
    packet = json.loads(path.read_text())
    sources, events, metrics = packet["sources"], packet["events"], packet["metrics"]
    rows = {event["row"]: event for event in events}
    intervals = {key: event_interval(value, sources) for key, value in rows.items()}
    passed = []

    def check(name, condition):
        if not condition:
            raise AssertionError(name)
        passed.append(name)

    def rejects(name, operation):
        try:
            operation()
        except ValueError:
            check(name, True)
        else:
            check(name, False)

    check("explicit offset conversion", utc(rows["C1"]["event_time"]) == utc("2026-05-14T13:00:30Z"))
    rejects("offset-free timestamp rejected", lambda: utc(rows["N1"]["event_time"]))
    check("positive skew bounds", intervals["L1"] == (utc("2026-05-14T13:00:29Z"), utc("2026-05-14T13:00:31Z")))
    alternate = copy.deepcopy(sources)
    alternate["CHG"]["skew_seconds"] = [-5, -3]
    check("negative skew bounds", event_interval(rows["C1"], alternate) == (utc("2026-05-14T13:00:33Z"), utc("2026-05-14T13:00:35Z")))
    alternate["CHG"]["skew_seconds"] = None
    check("unknown clock stays unknown", event_interval(rows["C1"], alternate) is None)
    check("note remains unplaced", intervals["N1"] is None and relation(intervals["N1"], intervals["L2"]) == "unknown")
    check("overlap does not establish order", relation(intervals["C1"], intervals["L1"]) == "unresolved")
    point = utc("2026-05-14T13:00:00Z")
    check("touching bounds are not strictly ordered", relation((point, point + timedelta(seconds=1)), (point + timedelta(seconds=1), point + timedelta(seconds=2))) == "unresolved")
    check("disjoint event bounds establish order", relation(intervals["L1"], intervals["L2"]) == "before")
    check("ingestion order differs from event order", utc(rows["L2"]["ingested_at"]) < utc(rows["L1"]["ingested_at"]))
    groups = deduplicate(events, sources)
    check("raw rows reconcile with duplicate", len(events) == 5 and len(groups) == 4 and sum(len(group) - 1 for group in groups) == 1)
    log_groups = deduplicate([row for row in events if row["source"] == "LOG"], sources)
    check("similar messages retain distinct event IDs", len(log_groups) == 2)
    conflict = copy.deepcopy(events)
    conflict[2]["message"] = "Different outcome under the same event ID"
    rejects("conflicting identity is not collapsed", lambda: deduplicate(conflict, sources))
    alternate = copy.deepcopy(sources)
    alternate["OTHER"] = dict(sources["LOG"], namespace="cedar/west/pod-a/boot-8")
    other = dict(rows["L1"], source="OTHER")
    check("same ID in another namespace stays distinct", len(deduplicate([rows["L1"], other], alternate)) == 2)
    check("requested sources reconcile", sum(source["available"] for source in sources.values()) == 4 and len(sources) == 5)
    metric_coverage = coverage(sources["MET"], packet["window"])
    check("metric coverage and missing window", metric_coverage == (180, [(utc("2026-05-14T13:01:00Z"), utc("2026-05-14T13:02:00Z"))]))
    check("unknown coverage is not zero", coverage(sources["NOTE"], packet["window"]) is None and coverage(sources["TRACE"], packet["window"]) is None)
    overlapping = {"coverage": [["2026-05-14T13:00:00Z", "2026-05-14T13:02:00Z"], ["2026-05-14T13:01:00Z", "2026-05-14T13:03:00Z"]]}
    check("overlapping coverage is unioned", coverage(overlapping, packet["window"])[0] == 180)
    oversized = {"coverage": [["2026-05-14T12:00:00Z", "2026-05-14T14:00:00Z"]]}
    check("coverage clipped to incident window", coverage(oversized, packet["window"]) == (240, []))
    check("compatible rate calculation", percent(metrics[0]) == 6)
    check("missing denominator stays unknown", percent(metrics[1]) is None)
    check("measured zero remains scoped rate", percent(metrics[2]) == 0)
    check("zero denominator is not zero rate", percent({"errors_5xx": 0, "attempts": 0}) is None)
    check("completed action distinguished from plan", [row["row"] for row in events if row.get("action_stage") == "completed"] == ["C1"] and rows["N1"]["action_stage"] == "proposed")

    print(f"PASS: {len(passed)} offline checks; Python {sys.version.split()[0]}")
    print("Events: 5 raw rows -> 4 unique identities; LOG: 3 rows -> 2 identities")
    for group in groups:
        interval = event_interval(group[0], sources)
        label = ", ".join(row["row"] for row in group)
        value = "unplaced" if interval is None else f"[{stamp(interval[0])}, {stamp(interval[1])}]"
        print(f"{label}: {value}")
    print("Order: C1/L1 unresolved; L1 before L2; N1 absolute position unknown")
    print("Sources: 4/5 available; MET: 180/240 seconds covered; missing [13:01,13:02) UTC")
    for row in metrics:
        rate = percent(row)
        print(f"{row['row']}: {row['errors_5xx']}/{row['attempts']} -> {'unknown' if rate is None else f'{rate:g}%'}")
    print("Completed-action evidence: C1; proposed-only evidence: N1")


if __name__ == "__main__":
    main()
