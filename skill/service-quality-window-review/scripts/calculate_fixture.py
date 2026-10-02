#!/usr/bin/env python3
"""Read one local quality-window-v1 fixture; emit calculations, never modify it.

This is a bounded example calculator, not a Prometheus/OTLP parser or verifier
of producer attestations. Uses only the Python standard library; no network.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def instant(value):
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "Timestamps require an explicit offset")
    return parsed.astimezone(timezone.utc)


def label(value):
    return value.isoformat().replace("+00:00", "Z")


def fraction(numerator, denominator):
    return {"numerator": numerator, "denominator": denominator,
            "percent": f"{100 * numerator / denominator:.6f}" if denominator else None}


def coverage(intervals, shards, start, end):
    missing, covered_seconds = [], 0
    for shard in shards:
        cursor = start
        for lo, hi in sorted((r[1], r[2]) for r in intervals if r[0] == shard):
            require(cursor <= lo, "Overlapping observation intervals")
            if cursor < lo:
                missing.append({"shard": shard, "start": label(cursor), "end": label(lo)})
            covered_seconds += int((hi - lo).total_seconds())
            cursor = hi
        if cursor < end:
            missing.append({"shard": shard, "start": label(cursor), "end": label(end)})
    edges = sorted({start, end, *(t for r in intervals for t in r[1:])})
    all_seconds = sum(int((hi - lo).total_seconds()) for lo, hi in zip(edges, edges[1:])
                      if all(any(s == shard and a <= lo and hi <= b
                                 for s, a, b in intervals) for shard in shards))
    expected = len(shards) * int((end - start).total_seconds())
    return {"observed_shard_seconds": covered_seconds, "expected_shard_seconds": expected,
            "shard_time_coverage": fraction(covered_seconds, expected),
            "all_shards_observed_seconds": all_seconds, "missing": missing,
            "complete": not missing}


def histogram_delta(a, b, policy, eligible):
    for snapshot in (a, b):
        h = snapshot["latency"]
        require(isinstance(h, dict), "Invalid histogram object")
        require(h["unit"] == policy["latency_unit"], "Latency unit mismatch")
        require(h["population"] == policy["latency_population"], "Latency population mismatch")
        require(h["upper_bounds"] == policy["upper_bounds"], "Incompatible histogram bounds")
        values = h["cumulative_le"]
        require(isinstance(values, list), "Invalid cumulative bucket list")
        require(len(values) == len(policy["upper_bounds"]), "Missing histogram bucket")
        require(all(type(v) is int and v >= 0 for v in values), "Invalid bucket count")
        require(values == sorted(values), "Nonmonotone cumulative buckets")
        require(type(h["count"]) is int and values[-1] == h["count"], "+Inf/count mismatch")
        require(h["count"] == snapshot["attempts"] - snapshot["canceled"],
                "Snapshot latency/eligible population count mismatch")
    delta = [y - x for x, y in zip(a["latency"]["cumulative_le"], b["latency"]["cumulative_le"])]
    require(all(v >= 0 for v in delta) and delta == sorted(delta), "Invalid interval buckets")
    require(delta[-1] == eligible, "Interval latency/eligible count mismatch")
    return delta


def diagnostic_counts(rows, start, end, shards):
    request_ids, attempt_ids = set(), set()
    finals = {"success": 0, "error": 0, "canceled": 0}
    attempts = dict(finals)
    unresolved = unfinished = outside = 0
    for row in rows:
        require(row["id"] not in request_ids, "Duplicate logical request identity")
        request_ids.add(row["id"])
        require(row["shard"] in shards, "Unexpected diagnostic shard")
        if row["final"] == "unresolved":
            require(row["final_at"] is None, "Unresolved request has a final time")
            unresolved += 1
        else:
            require(row["final"] in finals, "Unknown logical outcome")
            if start <= instant(row["final_at"]) < end:
                finals[row["final"]] += 1
        for attempt in row["attempts"]:
            require(attempt["id"] not in attempt_ids, "Duplicate attempt identity")
            attempt_ids.add(attempt["id"])
            if attempt["outcome"] == "unfinished":
                require(attempt["terminal_at"] is None, "Unfinished attempt has terminal time")
                unfinished += 1
            else:
                require(attempt["outcome"] in attempts, "Unknown attempt outcome")
                if start <= instant(attempt["terminal_at"]) < end:
                    attempts[attempt["outcome"]] += 1
                else:
                    outside += 1
    return {"source": "telemetry.json:diagnostic_requests", "service_coverage": "unknown; selected examples only",
            "selected_request_ids": len(request_ids), "terminal_logical_outcomes_in_window": finals,
            "logical_error_fraction": fraction(finals["error"], finals["error"] + finals["success"]),
            "unresolved_requests": unresolved, "terminal_attempt_outcomes_in_window": attempts,
            "attempt_error_fraction": fraction(attempts["error"], attempts["error"] + attempts["success"]),
            "unfinished_attempts": unfinished, "terminal_attempts_outside_window": outside}


def analyze(data):
    require(data["format"] == "quality-window-v1" and data["fictional"] is True,
            "This calculator accepts only the fictional quality-window-v1 contract")
    p = data["contract"]
    fixed = {"window_boundary": "[start,end)", "snapshot_boundary": "terminal_event_time < timestamp",
             "denominator_unit": "terminal_noncanceled_attempt", "retry_policy": "count_each_attempt",
             "cancel_policy": "exclude_from_error_and_latency_denominators",
             "error_policy": "server_failure_or_application_deadline_timeout",
             "latency_population": "terminal_noncanceled_attempt", "latency_unit": "s",
             "latency_measurement": "attempt_admission_to_terminal_event",
             "snapshot_temporality": "cumulative_since_epoch", "bucket_representation": "cumulative_le",
             "quantile_policy": "nearest_rank_bound", "target_requires_complete_window": True}
    require(all(p[k] == v for k, v in fixed.items()), "Unsupported or missing policy; do not silently substitute")
    start, end = instant(p["start"]), instant(p["end"])
    require(start < end, "Empty/reversed review window")
    require(all(t.microsecond == 0 for t in (start, end)), "Fixture uses whole-second boundaries")
    shards = p["expected_shards"]
    require(shards and len(shards) == len(set(shards)), "Invalid expected shard inventory")
    bounds = p["upper_bounds"]
    require(bounds[-1] == "+Inf" and bounds[:-1] == sorted(set(bounds[:-1]))
            and all(type(b) in (int, float) and b > 0 for b in bounds[:-1]), "Invalid latency bounds")
    require(p["latency_threshold"] in bounds[:-1], "Threshold is inside a bucket; this helper does not interpolate")
    limits = [Fraction(p["error_target_max"]), Fraction(p["latency_target_min"])]
    quantiles = [Fraction(q) for q in p["quantiles"]]
    require(all(0 <= t <= 1 for t in limits) and all(0 < q <= 1 for q in quantiles), "Invalid target or quantile")
    snapshots = {s["id"]: s for s in data["snapshots"]}
    require(len(snapshots) == len(data["snapshots"]), "Duplicate snapshot identity")
    snapshot_payloads = {}
    for s in snapshots.values():
        require(s["shard"] in shards and s["epoch"], "Missing/unknown series identity")
        require(all(type(s[k]) is int and s[k] >= 0 for k in ("attempts", "errors", "canceled")), "Invalid counter")
        require(s["errors"] + s["canceled"] <= s["attempts"], "Counter outcome partition conflict")
        identity = (s["shard"], instant(s["at"]), s["epoch"])
        payload = {k: s.get(k) for k in ("attempts", "errors", "canceled", "latency")}
        require(identity not in snapshot_payloads or snapshot_payloads[identity] == payload,
                "Conflicting snapshot payloads for the same shard/time/epoch")
        snapshot_payloads[identity] = payload
    accepted, excluded, count_intervals, latency_intervals, all_intervals = [], [], [], [], []
    totals = {"attempts": 0, "errors": 0, "canceled": 0, "eligible": 0}
    pooled = [0] * len(bounds)
    span_ids = set()
    for span in data["spans"]:
        require(span["id"] not in span_ids, "Duplicate span identity")
        span_ids.add(span["id"])
        a, b = snapshots[span["start"]], snapshots[span["end"]]
        lo, hi = instant(a["at"]), instant(b["at"])
        require(start <= lo < hi <= end and a["shard"] == b["shard"], "Invalid span boundaries/series")
        require(lo.microsecond == hi.microsecond == 0, "Fixture uses whole-second boundaries")
        cell = (a["shard"], lo, hi)
        all_intervals.append(cell)
        record = {"id": span["id"], "shard": a["shard"], "start": label(lo), "end": label(hi),
                  "sources": ["telemetry.json:spans/" + span["id"],
                              "telemetry.json:snapshots/" + a["id"], "telemetry.json:snapshots/" + b["id"]]}
        delta = {key: b[key] - a[key] for key in ("attempts", "errors", "canceled")}
        if span["complete_observation"] is not True or not span["evidence"] or a["epoch"] != b["epoch"]:
            excluded.append({**record, "reason": "Unknown continuity or changed epoch; no whole-span delta"})
            continue
        if min(delta.values()) < 0 or delta["errors"] + delta["canceled"] > delta["attempts"]:
            excluded.append({**record, "reason": "Counter decrease or incompatible outcome delta"})
            continue
        delta["eligible"] = delta["attempts"] - delta["canceled"]
        count_intervals.append(cell)
        for key in totals:
            totals[key] += delta[key]
        record.update(delta)
        try:
            h = histogram_delta(a, b, p, delta["eligible"])
            pooled = [x + y for x, y in zip(pooled, h)]
            latency_intervals.append(cell)
            record["latency_cumulative_le"] = h
        except (ValueError, KeyError) as error:
            record["latency_unavailable"] = str(error)
        accepted.append(record)
    coverage(all_intervals, shards, start, end)  # Reject overlap even in excluded spans.
    count_coverage = coverage(count_intervals, shards, start, end)
    latency_coverage = coverage(latency_intervals, shards, start, end)
    n = pooled[-1]
    quantile_bounds = []
    for q_text, q in zip(p["quantiles"], quantiles):
        if not n:
            quantile_bounds.append({"q": q_text, "rank": None, "bound": None})
            continue
        position = q * n
        rank = (position.numerator + position.denominator - 1) // position.denominator
        index = next(i for i, count in enumerate(pooled) if count >= rank)
        quantile_bounds.append({"q": q_text, "rank": rank,
                                "lower": bounds[index - 1] if index else 0,
                                "lower_inclusive": index == 0,
                                "upper": bounds[index] if bounds[index] != "+Inf" else None,
                                "upper_inclusive": bounds[index] != "+Inf"})
    fast = pooled[bounds.index(p["latency_threshold"])]
    error_comparison = None if not totals["eligible"] else Fraction(totals["errors"], totals["eligible"]) <= limits[0]
    latency_comparison = None if not n else Fraction(fast, n) >= limits[1]
    complete = count_coverage["complete"] and latency_coverage["complete"]
    verdict = "undetermined" if not complete or error_comparison is None or latency_comparison is None else (
        "targets_met" if error_comparison and latency_comparison else "targets_not_met")
    try:
        diagnostic = diagnostic_counts(data["diagnostic_requests"], start, end, shards)
    except (ValueError, KeyError, TypeError, AttributeError) as error:
        diagnostic = {"source": "telemetry.json:diagnostic_requests", "status": "unavailable",
                      "reason": str(error), "service_coverage": "unknown; selected examples only"}
    return {"source_revision": data["source_manifest"]["revision"], "contract": p,
            "count_coverage": count_coverage, "latency_coverage": latency_coverage,
            "accepted_intervals": accepted, "excluded_intervals": excluded,
            "known_counts": {**totals, "success": totals["eligible"] - totals["errors"],
                             "error_fraction": fraction(totals["errors"], totals["eligible"])},
            "latency": {"unit": p["latency_unit"], "count": n, "upper_bounds": bounds,
                        "cumulative_le": pooled, "disjoint_bins": [pooled[0]] + [b - a for a, b in zip(pooled, pooled[1:])],
                        "threshold_fraction": fraction(fast, n), "quantile_bounds": quantile_bounds},
            "observed_subset_target_comparison": {"error_meets": error_comparison, "latency_meets": latency_comparison},
            "full_window_verdict": verdict,
            "diagnostic_ledger": diagnostic}


if __name__ == "__main__":
    require(len(sys.argv) == 2, "Usage: calculate_fixture.py telemetry.json")
    raw = Path(sys.argv[1]).read_bytes()
    result = analyze(json.loads(raw))
    result["input_sha256"] = hashlib.sha256(raw).hexdigest()
    print(json.dumps(result, indent=2, allow_nan=False))
