"""Offline, bounded example: correctness first, measured controls, raw evidence.

Run from the skill directory: python3 -B example/verify.py --out evidence/new.json
Read existing evidence: python3 -B example/verify.py --readback evidence/run.json
No dependencies, installs, network, subprocesses, or timing-based pass threshold.
"""

import argparse
import copy
from datetime import datetime, timezone
import gc
import hashlib
import itertools
import json
import os
from pathlib import Path
import platform
import statistics
import sys
import time

sys.dont_write_bytecode = True
import summary

ROOT = Path(__file__).resolve().parent.parent
FILES = ("example/summary.py", "example/verify.py", "example/contract.json",
         "example/workloads.json")
VARIANTS = {name: getattr(summary, name) for name in
            ("baseline", "candidate", "wrong_last_record")}
SCOPES = ("algorithm_only", "in_memory_json_pipeline")
BLOCKS = 12
MAX_SECONDS = 10


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def manifest():
    return {name: digest((ROOT / name).read_bytes()) for name in FILES}


def validate_input(records, requests):
    require(isinstance(records, list) and isinstance(requests, list), "input lists")
    require(all(isinstance(q, str) for q in requests), "string request IDs")
    for r in records:
        require(isinstance(r, dict) and isinstance(r.get("id"), str), "record ID")
        require(set(r) <= {"id", "value"}, "record fields")
        require(r.get("value") is None or type(r["value"]) is int, "integer or unknown")


def oracle(records, requests):
    """Literal contract oracle: selections and reductions, no aggregate index."""
    result = []
    for identifier in requests:
        selected = [r for r in records if r["id"] == identifier]
        values = [r["value"] for r in selected
                  if "value" in r and r["value"] is not None]
        result.append(dict(id=identifier, matches=len(selected), known=len(values),
                           total=sum(values) if values else None))
    return result


def checked_call(function, records, requests, expected):
    before = encode([records, requests])
    actual = function(records, requests)
    require(actual == expected, f"contract mismatch: {function.__name__}")
    require(encode([records, requests]) == before, "input mutated")
    require(all(set(row) == {"id", "matches", "known", "total"} for row in actual),
            "output fields")
    require(all(type(row["matches"]) is int and type(row["known"]) is int and
                (row["total"] is None or type(row["total"]) is int) for row in actual),
            "exact output value types")
    return actual


def correctness(contract, workloads):
    counts = {"explicit_cases_per_accepted_variant": len(contract["cases"]),
              "exhaustive_cases_per_accepted_variant": 0,
              "timing_workloads_per_accepted_variant": len(workloads),
              "metamorphic_checks_per_accepted_variant": 0}
    for case in contract["cases"]:
        validate_input(case["records"], case["requests"])
        require(oracle(case["records"], case["requests"]) == case["expected"],
                "oracle disagrees with separately authored fixture")
        for name in ("baseline", "candidate"):
            checked_call(VARIANTS[name], case["records"], case["requests"], case["expected"])
    # All sequences of length 0..3 from six distinct observation possibilities.
    atoms = [{"id": "07"}, {"id": "07", "value": None},
             {"id": "07", "value": 0}, {"id": "07", "value": -2},
             {"id": "07", "value": 2}, {"id": "7", "value": 4}]
    requests = ["7", "07", "missing", "07"]
    for size in range(4):
        for selected in itertools.product(atoms, repeat=size):
            records = list(selected)
            expected = oracle(records, requests)
            for name in ("baseline", "candidate"):
                checked_call(VARIANTS[name], records, requests, expected)
            counts["exhaustive_cases_per_accepted_variant"] += 1
    for w in workloads:
        records, requests = w["records"], w["requests"]
        validate_input(records, requests)
        expected = oracle(records, requests)
        for name in ("baseline", "candidate"):
            function = VARIANTS[name]
            checked_call(function, records, requests, expected)
            checked_call(function, list(reversed(records)), requests, expected)
            checked_call(function, records + [{"id": "not-requested", "value": 8}],
                         requests, expected)
            checked_call(function, records, requests + requests, expected + expected)
        counts["metamorphic_checks_per_accepted_variant"] += 3
    witness = contract["cases"][0]
    wrong = VARIANTS["wrong_last_record"](witness["records"], witness["requests"])
    require(wrong != witness["expected"], "negative control must actually fail")
    differences = [{"index": i, "expected": e, "actual": a}
                   for i, (e, a) in enumerate(zip(witness["expected"], wrong)) if e != a]
    return {"accepted_for_timing_comparison": ["baseline", "candidate"],
            "rejected_regardless_of_timing": ["wrong_last_record"],
            "counts": counts, "negative_control_case": witness["name"],
            "negative_control_differences": differences}


def distribution(values):
    return {"n": len(values), "min": min(values), "median": statistics.median(values),
            "max": max(values)}


def summarize(samples):
    groups = {}
    for s in samples:
        key = f'{s["workload"]}/{s["scope"]}'
        groups.setdefault(key, {}).setdefault(s["variant"], []).append(s)
    output = {}
    for key, variants in groups.items():
        baseline = {s["block"]: s["elapsed_ns"] / s["loops"] for s in variants["baseline"]}
        candidate = {s["block"]: s["elapsed_ns"] / s["loops"] for s in variants["candidate"]}
        output[key] = {
            "ns_per_call": {v: distribution([s["elapsed_ns"] / s["loops"] for s in ss])
                            for v, ss in variants.items()},
            "paired_baseline_over_candidate": distribution([baseline[b] / candidate[b]
                                                             for b in sorted(baseline)]),
            "paired_candidate_minus_baseline_ns": distribution([candidate[b] - baseline[b]
                                                                 for b in sorted(baseline)]),
            "invalid_control_eligible_for_speed_claim": False,
        }
    return output


def environment():
    clock = time.get_clock_info("perf_counter")
    cpu = "unknown"
    cpuinfo = Path("/proc/cpuinfo")
    if cpuinfo.is_file():
        cpu = next((line.split(":", 1)[1].strip() for line in cpuinfo.read_text().splitlines()
                    if line.startswith("model name")), "unknown")
    return {"python": platform.python_version(), "implementation": platform.python_implementation(),
            "os": platform.system(), "kernel": platform.release(), "architecture": platform.machine(),
            "cpu_model_reported_by_guest": cpu, "logical_cpu_count_visible": os.cpu_count(),
            "affinity_cpu_count": len(os.sched_getaffinity(0)) if hasattr(os, "sched_getaffinity") else None,
            "clock": {"implementation": clock.implementation, "resolution_seconds": clock.resolution,
                      "monotonic": clock.monotonic, "adjustable": clock.adjustable},
            "gc_enabled": gc.isenabled(), "gc_thresholds": list(gc.get_threshold()),
            "process_hash_seed": os.environ.get("PYTHONHASHSEED", "interpreter default (not fixed)"),
            "uncontrolled": ["host load", "CPU frequency/turbo", "CPU placement", "thermal state",
                             "virtualization scheduling", "memory allocator state", "OS page cache"],
            "not_measured": ["peak memory", "CPU time", "power", "process startup", "cold cache",
                             "file I/O", "network", "deployment", "human effort"]}


def payload(w):
    return {"records": w["records"], "requests": w["requests"]}


def workload_metadata(w):
    input_bytes = encode(payload(w))
    expected = oracle(w["records"], w["requests"])
    return {"name": w["name"], "record_occurrences": len(w["records"]),
            "distinct_record_ids": len({r["id"] for r in w["records"]}),
            "request_occurrences": len(w["requests"]), "loops_per_sample": w["loops_per_sample"],
            "pipeline_input_bytes": len(input_bytes), "pipeline_input_sha256": digest(input_bytes),
            "expected_output_sha256": digest(encode(expected))}


def operation(function, scope, w, input_bytes):
    if scope == "algorithm_only":
        return function(w["records"], w["requests"])
    decoded = json.loads(input_bytes)
    return encode(function(decoded["records"], decoded["requests"]))


def check_readback(result):
    require(result["source_sha256"] == manifest(), "source/input/contract identity changed")
    workloads = json.loads((ROOT / "example/workloads.json").read_text())
    contract = json.loads((ROOT / "example/contract.json").read_text())
    require(result["correctness"] == correctness(contract, workloads), "correctness evidence changed")
    expected_keys = {(w["name"], scope, block, variant)
                     for w in workloads for scope in SCOPES
                     for block in range(BLOCKS) for variant in VARIANTS}
    samples = result["samples"]
    actual_keys = [(s["workload"], s["scope"], s["block"], s["variant"]) for s in samples]
    require(len(actual_keys) == len(set(actual_keys)) and set(actual_keys) == expected_keys,
            "missing or duplicate samples")
    orders = list(itertools.permutations(VARIANTS))
    expected_sequence = [(w["name"], scope, block, variant)
                         for w in workloads for scope in SCOPES for block in range(BLOCKS)
                         for variant in orders[block % len(orders)]]
    require(actual_keys == expected_sequence, "execution order changed")
    require([s["sequence"] for s in samples] == list(range(len(samples))), "sequence labels changed")
    require(result["workloads"] == [workload_metadata(w) for w in workloads], "workload metadata changed")
    by_name = {w["name"]: w for w in workloads}
    expected_outputs = {}
    for w in workloads:
        expected = oracle(w["records"], w["requests"])
        for name, function in VARIANTS.items():
            actual = function(w["records"], w["requests"])
            expected_outputs[w["name"], name] = (digest(encode(actual)), actual == expected)
    for s in samples:
        require(type(s["elapsed_ns"]) is int and s["elapsed_ns"] > 0, "invalid elapsed time")
        w = by_name[s["workload"]]
        require(s["loops"] == w["loops_per_sample"], "loop count changed")
        output_hash, passes = expected_outputs[w["name"], s["variant"]]
        require(s["output_sha256"] == output_hash, "output identity changed")
        require(s["contract_pass"] == passes, "sample contract status changed")
    require(result["summaries"] == summarize(samples), "raw samples disagree with summaries")
    require(result["setup"]["loaded_workload_bytes_sha256"] ==
            digest((ROOT / "example/workloads.json").read_bytes()), "workload bytes changed")
    return {"source_files_checked": len(FILES), "samples_checked": len(samples),
            "summaries_recomputed": len(result["summaries"]), "correctness_reexecuted": True}


def readback_guards(result):
    failures = []
    for kind in ("changed_source", "missing_sample", "changed_summary", "changed_output"):
        altered = copy.deepcopy(result)
        if kind == "changed_source":
            altered["source_sha256"]["example/summary.py"] = "0" * 64
        elif kind == "missing_sample":
            altered["samples"].pop()
        elif kind == "changed_summary":
            first = next(iter(altered["summaries"].values()))
            first["ns_per_call"]["candidate"]["median"] += 1
        else:
            altered["samples"][0]["output_sha256"] = "0" * 64
        try:
            check_readback(altered)
        except ValueError:
            failures.append(kind)
        else:
            raise ValueError(f"readback failed to reject {kind}")
    return failures


def run():
    start = time.perf_counter_ns()
    before_hashes = manifest()
    setup_start = time.perf_counter_ns()
    workload_bytes = (ROOT / "example/workloads.json").read_bytes()
    workloads = json.loads(workload_bytes)
    contract = json.loads((ROOT / "example/contract.json").read_text())
    setup_ns = time.perf_counter_ns() - setup_start
    correctness_start = time.perf_counter_ns()
    checks = correctness(contract, workloads)
    correctness_ns = time.perf_counter_ns() - correctness_start
    result = {"schema": 1, "started_at_utc": datetime.now(timezone.utc).isoformat(),
              "source_sha256": before_hashes, "environment": environment(), "correctness": checks,
              "design": {"blocks_per_workload_scope": BLOCKS, "orders": [list(order) for order in itertools.permutations(VARIANTS)],
                         "order_policy": "All six variant permutations, repeated twice; deterministic, not randomized.",
                         "sample_unit": "One elapsed wall-clock batch divided by its fixed loop count.",
                         "warmup": "One untimed call for each workload/scope/variant, after correctness checks.",
                         "state": "Same warm process. Fresh per-call indexes; reused inputs for algorithm_only; fresh JSON parse per pipeline call.",
                         "gc_policy": "Leave automatic GC enabled at inherited thresholds; do not force collection.",
                         "uncertainty": "Descriptive within-process ranges; no confidence intervals, independent-process replication, or population estimate.",
                         "budget_seconds": MAX_SECONDS, "budget_policy": "Check between timed batches; stop without a completed report if exceeded."},
              "setup": {"load_contract_and_workloads_ns": setup_ns, "correctness_checks_ns": correctness_ns,
                        "loaded_workload_bytes_sha256": digest(workload_bytes),
                        "excluded": ["interpreter startup and imports (not timed)", "authored workload generation (not timed)",
                                     "warmup", "report formatting and writes", "readback checks"],
                        "build": "No build, install, compilation step or dependencies requested; Python source is the candidate."},
              "workloads": [], "samples": []}
    orders = list(itertools.permutations(VARIANTS))
    for w in workloads:
        input_bytes = encode(payload(w))
        original = encode(payload(w))
        expected = oracle(w["records"], w["requests"])
        result["workloads"].append(workload_metadata(w))
        for scope in SCOPES:
            reference = {}
            for name, function in VARIANTS.items():
                reference[name] = operation(function, scope, w, input_bytes)
            for block in range(BLOCKS):
                for name in orders[block % len(orders)]:
                    require((time.perf_counter_ns() - start) / 1e9 < MAX_SECONDS, "benchmark budget exceeded")
                    function, loops = VARIANTS[name], w["loops_per_sample"]
                    tick = time.perf_counter_ns()
                    for _ in range(loops):
                        actual = operation(function, scope, w, input_bytes)
                    elapsed = time.perf_counter_ns() - tick
                    require(actual == reference[name], "unstable output during timing")
                    require(encode(payload(w)) == original, "timed implementation mutated input")
                    decoded = json.loads(actual) if isinstance(actual, bytes) else actual
                    passes = decoded == expected
                    require(passes == (name != "wrong_last_record"), "unexpected timing contract result")
                    result["samples"].append({"sequence": len(result["samples"]), "workload": w["name"],
                                              "scope": scope, "block": block, "variant": name, "loops": loops,
                                              "elapsed_ns": elapsed, "output_sha256": digest(encode(decoded)),
                                              "contract_pass": passes})
    require(manifest() == before_hashes, "source changed during measurement")
    result["summaries"] = summarize(result["samples"])
    result["harness_elapsed_before_readback_ns"] = time.perf_counter_ns() - start
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", type=Path)
    group.add_argument("--readback", type=Path)
    args = parser.parse_args()
    if args.readback:
        result = json.loads(args.readback.read_text())
        print(json.dumps({"readback": check_readback(result), "tamper_guards": readback_guards(result)}, indent=2))
        return
    require(not args.out.exists(), "output exists; choose a new evidence filename")
    result = run()
    result["readback"] = check_readback(result)
    result["readback_guard_rejections"] = readback_guards(result)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    saved = json.loads(args.out.read_text())
    require(saved == result, "saved JSON differs from generated evidence")
    print(json.dumps({"readback": check_readback(saved), "harness_seconds_before_readback":
                      result["harness_elapsed_before_readback_ns"] / 1e9,
                      "summaries": result["summaries"]}, indent=2))


if __name__ == "__main__":
    main()
