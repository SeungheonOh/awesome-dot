"""Equal-family/equal-task paired summaries; missingness and failures stay visible."""
from __future__ import annotations
from collections import Counter, defaultdict
import math
from pathlib import Path
import random
import statistics
from .core import IntegrityError, Ledger, digest, load_json
from .grading import resolve_grades
from .telemetry import USAGE_KEYS
from .protocol import read_study


def mean(values):
    return statistics.fmean(values) if values else None


def quantile(values, probability):
    if not values:
        return None
    values = sorted(values)
    location = (len(values) - 1) * probability
    low = math.floor(location)
    high = math.ceil(location)
    return values[low] + (values[high] - values[low]) * (location - low)


def distribution(values):
    return {"n": len(values), "mean": mean(values), "median": quantile(values, .5), "p90": quantile(values, .9),
            "min": min(values) if values else None, "max": max(values) if values else None}


def cluster_interval(family_deltas, seed, draws):
    """Resample entire families. Variants/repetitions are never independent resamples."""
    if len(family_deltas) < 2 or draws < 100:
        return None
    rng = random.Random(seed)
    n = len(family_deltas)
    samples = [mean([family_deltas[rng.randrange(n)] for _ in range(n)]) for _ in range(draws)]
    return {"lower": quantile(samples, .025), "upper": quantile(samples, .975), "level": .95,
        "method": "Percentile cluster bootstrap of equal-weight family means", "resampling_unit": "family",
        "draws": draws, "seed": seed, "degenerate_observed_interval": min(samples) == max(samples),
        "degenerate_warning": "A degenerate interval reflects only the observed paired values; it does not establish certainty or absence of a population effect" if min(samples) == max(samples) else None, "caution": "Descriptive and unstable with few curated families; no broad population claim"}


def summarize(rows, protocol, ledger_head=None):
    tasks = {task["task_id"]: task for task in protocol["tasks"]}
    grouped = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for row in rows:
        grouped[row["family_id"]][row["task_id"]][row["arm"]].append(row)
    families = []
    for family_id, by_task in sorted(grouped.items()):
        arms = {}
        for arm in ("C", "S"):
            task_metrics = []
            for task_id, by_arm in sorted(by_task.items()):
                samples = by_arm[arm]
                if not samples:
                    raise IntegrityError("Scheduled task has an empty arm")
                task_metrics.append({"task_id": task_id, "n": len(samples),
                    "observed_acceptance": mean([float(r["accepted"] is True) for r in samples]),
                    "acceptance_upper": mean([float(r["accepted"] is not False) for r in samples]),
                    "quality_lower": mean([r["quality_fraction"] if r["quality_fraction"] is not None else 0.0 for r in samples]),
                    "quality_upper": mean([r["quality_fraction"] if r["quality_fraction"] is not None else 1.0 for r in samples]),
                    "capped_time_to_accepted_s": mean([r["elapsed_s"] if r["accepted"] is True and r["elapsed_s"] is not None else r["timeout_s"] for r in samples])})
            arms[arm] = {key: mean([t[key] for t in task_metrics]) for key in ("observed_acceptance", "acceptance_upper", "quality_lower", "quality_upper", "capped_time_to_accepted_s")}
            arms[arm]["tasks"] = task_metrics
        families.append({"family_id": family_id, "arms": arms,
            "observed_acceptance_delta_S_minus_C": arms["S"]["observed_acceptance"] - arms["C"]["observed_acceptance"],
            "missing_outcome_contrast_bounds": [arms["S"]["observed_acceptance"] - arms["C"]["acceptance_upper"],
                                                arms["S"]["acceptance_upper"] - arms["C"]["observed_acceptance"]]})
    blocks = defaultdict(dict)
    for row in rows:
        if row["arm"] in blocks[row["block_id"]]:
            raise IntegrityError("Duplicate primary arm in paired block")
        blocks[row["block_id"]][row["arm"]] = row
    pairs = []
    accepted_pair_latencies = []
    for block, arms in sorted(blocks.items()):
        if set(arms) != {"C", "S"}:
            raise IntegrityError("Incomplete scheduled paired block")
        both = all(arms[a]["accepted"] is True for a in ("C", "S"))
        c, s = (arms[a]["elapsed_s"] for a in ("C", "S"))
        latency = {"difference_s": s - c, "ratio_S_over_C": s / c if c > 0 else None} if both and c is not None and s is not None else None
        if latency:
            accepted_pair_latencies.append(latency)
        pairs.append({"block_id": block, "task_id": arms["C"]["task_id"],
            "C": {k: arms["C"][k] for k in ("attempt_id", "accepted", "status", "elapsed_s")},
            "S": {k: arms["S"][k] for k in ("attempt_id", "accepted", "status", "elapsed_s")},
            "both_accepted_latency": latency})
    paired_comparison = {"S_wins": 0, "ties_both_accepted": 0, "ties_both_rejected": 0, "S_losses": 0, "unknown_pairs": 0}
    for pair in pairs:
        c, s = pair["C"]["accepted"], pair["S"]["accepted"]
        key = ("unknown_pairs" if c is None or s is None else "ties_both_accepted" if c and s else
               "ties_both_rejected" if not c and not s else "S_wins" if s else "S_losses")
        paired_comparison[key] += 1
    coverage = {}
    for arm in ("C", "S"):
        samples = [r for r in rows if r["arm"] == arm]
        coverage[arm] = {"scheduled": len(samples),
            "observed_accepted_fraction_of_scheduled": sum(r["accepted"] is True for r in samples) / len(samples) if any(r["attempted"] for r in samples) else None, "attempted": sum(r["attempted"] for r in samples),
            "terminal_recorded": sum(r["finished"] for r in samples), "graded": sum(r["rater_count"] > 0 for r in samples),
            "acceptance_observed": sum(r["accepted"] is not None for r in samples), "accepted": sum(r["accepted"] is True for r in samples),
            "outcome_unknown": sum(r["accepted"] is None for r in samples),
            "grader_disagreement_attempts": sum(bool(r.get("disagreement")) for r in samples),
            "suspected_unblinding_attempts": sum(bool(r.get("suspected_unblinding")) for r in samples), "statuses": dict(Counter(r["status"] for r in samples)),
            "elapsed_s_all_observed": distribution([r["elapsed_s"] for r in samples if r["elapsed_s"] is not None]),
            "elapsed_s_by_status": {status: distribution([r["elapsed_s"] for r in samples if r["status"] == status and r["elapsed_s"] is not None]) for status in sorted({r["status"] for r in samples})},
            "usage": {}}
        for field in USAGE_KEYS:
            known = [(r.get("usage") or {}).get(field) for r in samples]
            values = [v for v in known if v is not None]
            coverage[arm]["usage"][field] = {"known_attempts": len(values), "scheduled_attempts": len(samples),
                "complete_capture_attempts": sum((r.get("usage") or {}).get("capture_complete", False) and (r.get("usage") or {}).get(field) is not None for r in samples),
                "sum_known_counter": sum(values) if values else None, "mean_known_counter": mean(values),
                "comparative_claim_supported": False}
    evidence = sorted({r["evidence_kind"] for r in rows})
    all_finished = all(r["finished"] for r in rows)
    model_only = bool(rows) and "model_attempt" in evidence and set(evidence).issubset({"model_attempt", "not_executed"})
    any_attempted = any(r["attempted"] for r in rows)
    effect_eligible = protocol["stage"] in ("exploratory_pilot", "evaluation") and all_finished and model_only
    deltas = [f["observed_acceptance_delta_S_minus_C"] for f in families]
    analysis = protocol.get("analysis", {})
    task_deltas = []
    for by_task in grouped.values():
        for by_arm in by_task.values():
            task_deltas.append(mean([float(r["accepted"] is True) for r in by_arm["S"]]) - mean([float(r["accepted"] is True) for r in by_arm["C"]]))
    leave_one_case_out = [mean([d for j, d in enumerate(task_deltas) if i != j]) for i in range(len(task_deltas))] if len(task_deltas) > 1 else []
    primary = {"claim_scope": "Observed contrast on this exact curated task set in this configured runtime only; no population efficacy, power or significance claim", "estimand": "Equal family weight; within family equal task-instance weight; within task equal scheduled repetition weight. Unknown acceptance contributes zero observed acceptance and remains visible in bounds.",
        "contrast": "S minus C", "units": "fraction; multiply by 100 for percentage points", "family_count": len(families),
        "distinct_task_count": len(grouped) and len({r["task_id"] for r in rows}),
        "paired_block_count": len(blocks), "effect_estimate": mean(deltas) if effect_eligible else None,
        "missing_outcome_contrast_bounds": [mean([f["missing_outcome_contrast_bounds"][i] for f in families]) for i in (0, 1)] if effect_eligible else None,
        "cluster_bootstrap": cluster_interval(deltas, analysis.get("bootstrap_seed", 741), analysis.get("bootstrap_draws", 10000)) if effect_eligible and protocol["stage"] == "evaluation" and analysis.get("bootstrap_enabled") is True else None,
        "bootstrap_disabled_reason": "No inferential interval for the eight-case, unreplicated exploratory convenience sample" if protocol["stage"] == "exploratory_pilot" else "Requires a separately frozen justified analysis plan with bootstrap_enabled=true",
        "leave_one_case_out_range": [min(leave_one_case_out), max(leave_one_case_out)] if effect_eligible and protocol["stage"] == "exploratory_pilot" and leave_one_case_out else None,
        "quality_delta_S_minus_C": mean([f["arms"]["S"]["quality_lower"] - f["arms"]["C"]["quality_lower"] for f in families]) if effect_eligible and all(r["quality_fraction"] is not None for r in rows) else None,
        "quality_missingness_contrast_bounds": [mean([f["arms"]["S"]["quality_lower"] - f["arms"]["C"]["quality_upper"] for f in families]), mean([f["arms"]["S"]["quality_upper"] - f["arms"]["C"]["quality_lower"] for f in families])] if effect_eligible else None,
        "capped_time_to_accepted_delta_s": mean([f["arms"]["S"]["capped_time_to_accepted_s"] - f["arms"]["C"]["capped_time_to_accepted_s"] for f in families]) if effect_eligible else None,
        "leave_one_family_out": {f["family_id"]: mean([d for j, d in enumerate(deltas) if i != j]) for i, f in enumerate(families)} if effect_eligible and len(families) > 1 else None,
        "effect_not_reported_reason": None if effect_eligible else "Requires a finished exploratory_pilot/evaluation model study; transport smoke, fixtures, not-started and intermediate results are not skill-effect evidence"}
    if not effect_eligible:
        for family in families:
            family["observed_acceptance_delta_S_minus_C"] = None
            family["missing_outcome_contrast_bounds"] = None
    if not any_attempted:
        for family in families:
            for arm in family["arms"].values():
                for key in ("observed_acceptance", "acceptance_upper", "quality_lower", "quality_upper", "capped_time_to_accepted_s"):
                    arm[key] = None
                    for task in arm["tasks"]:
                        task[key] = None
    return {"schema_version": "dot-eval-report-1", "study_status": "not_run" if not any_attempted else "finished" if all_finished else "incomplete", "protocol_sha256": protocol["protocol_sha256"], "ledger_head_sha256": ledger_head,
        "stage": protocol["stage"], "evidence_kind": evidence, "no_model_results": not model_only, "all_scheduled_finished": all_finished,
        "primary": primary, "coverage": coverage, "families": families, "paired_outcomes": pairs, "paired_acceptance_comparison": paired_comparison,
        "attempt_outcomes": [{k: v for k, v in r.items() if k not in ("usage", "protocol_sha256")} for r in rows],
        "accepted_pair_latency_secondary": {"selected_subset": True, "both_accepted_pairs": len(accepted_pair_latencies),
            "difference_s": distribution([x["difference_s"] for x in accepted_pair_latencies]),
            "ratio_S_over_C": distribution([x["ratio_S_over_C"] for x in accepted_pair_latencies if x["ratio_S_over_C"] is not None])},
        "billing": {"actual_cost": None, "currency": None},
        "warnings": ["Directories and instructions do not enforce isolation or grader blindness", "Exact backend model build, cache state and queue/model compute decomposition may be unavailable", "Counter semantics are not assumed; no cross-category token total or dollar estimate", "All scheduled primary attempts remain in the denominator; retries must remain separately identified"]}


def report(study_dir):
    root = Path(study_dir)
    protocol, _, records = read_study(root)
    task_map = {t["task_id"]: t for t in protocol["tasks"]}
    rows = []
    for scheduled in (r["payload"] for r in records if r["event"] == "scheduled"):
        aid = scheduled["attempt_id"]
        related = [r for r in records if r["payload"].get("attempt_id") == aid]
        finishes = [r["payload"] for r in related if r["event"] == "finished"]
        if len(finishes) > 1:
            raise IntegrityError("Multiple terminal records for one immutable attempt")
        finished = finishes[0] if finishes else None
        grades = [r["payload"] for r in related if r["event"] == "graded"]
        resolution = resolve_grades(grades, task_map[scheduled["task_id"]])
        accepted = resolution["accepted"]
        if not finished:
            accepted = None
        elif finished["status"] != "completed":
            accepted = False
        if finished and (finished.get("source_integrity") is False or finished.get("contamination_flag") is True):
            accepted = False
        rows.append({**scheduled, **resolution, "accepted": accepted,
            "attempted": any(r["event"] == "started" for r in related), "finished": finished is not None,
            "status": finished["status"] if finished else "not_started" if not any(r["event"] == "started" for r in related) else "in_progress_or_interrupted",
            "elapsed_s": ((finished or {}).get("timing") or {}).get("monotonic_elapsed_s"),
            "usage": (finished or {}).get("usage"), "evidence_kind": (finished or {}).get("evidence_kind", "not_executed")})
    return summarize(rows, protocol, records[-1]["record_sha256"] if records else None)
