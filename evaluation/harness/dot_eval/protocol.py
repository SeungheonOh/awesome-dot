"""Freeze content identities, schedule matched pairs, and stage minimal task packets."""
from __future__ import annotations
import random
import shutil
import time
import uuid
from pathlib import Path
from .core import IntegrityError, Ledger, canonical, child, create_json, digest, file_manifest, file_sha, load_json, utc_now

ARMS = ("C", "S")
TREATMENT_INSTRUCTION = "The following designated guide is available for this task: guide.md. Read it and apply relevant guidance within the task's existing scope."
PACKAGE_TREATMENT_INSTRUCTION = "The following designated skill package is available for this task: {guide_path}. Read its guide and use relevant bundled material within the task's existing scope. All package reading, copying, and checks count against the task time budget."
COMMON_OUTPUT_INSTRUCTION = "Read task.txt and the supplied inputs. Write the requested deliverables only under output/."


def _asset(base, name):
    path = child(base, name)
    return {"source": str(path), "sha256": file_sha(path), "bytes": path.stat().st_size}


def _code_manifest():
    root = Path(__file__).parent
    return [{"path": p.name, "sha256": file_sha(p)} for p in sorted(root.glob("*.py"))]


def freeze(config_path, output_path, *, inspection_only=False):
    config_path = Path(config_path).resolve()
    config = load_json(config_path)
    base = config_path.parent
    pending = []
    if config.get("schema_version") != "dot-eval-config-1":
        raise IntegrityError("Unsupported config schema")
    if config.get("arms") != list(ARMS):
        raise IntegrityError("This scaffold supports the predeclared paired C/S contrast only")
    if config.get("stage") not in ("harness_test", "smoke", "exploratory_pilot", "evaluation"):
        raise IntegrityError("Declare stage: harness_test, smoke, exploratory_pilot, or evaluation")
    if not config.get("tasks") or not isinstance(config.get("repetitions"), int) or isinstance(config.get("repetitions"), bool) or config["repetitions"] < 1:
        raise IntegrityError("Tasks and positive repetitions are required")
    if not isinstance(config.get("common_instruction"), str) or not config["common_instruction"].strip():
        raise IntegrityError("A frozen common instruction is required")
    treatment = config.get("treatment", "standalone_guide_supplied")
    if treatment not in ("standalone_guide_supplied", "designated_skill_package_supplied"):
        raise IntegrityError("Unknown treatment mode")
    if config["stage"] != "harness_test":
        required = ("task_authoring_complete", "independent_oracles_checked", "grader_controls_passed", "overlap_review_complete")
        missing = [k for k in required if config.get("review_gates", {}).get(k) is not True]
        if missing and not inspection_only:
            raise IntegrityError("Protocol cannot be frozen before task/oracle/grader/overlap review")
        pending.extend(missing)
    frozen = {k: v for k, v in config.items() if k != "tasks"}
    frozen.update({"schema_version": "dot-eval-frozen-1", "frozen_at_utc": utc_now(), "tasks": [],
                   "treatment": treatment, "treatment_instruction": PACKAGE_TREATMENT_INSTRUCTION if treatment == "designated_skill_package_supplied" else TREATMENT_INSTRUCTION, "common_output_instruction": COMMON_OUTPUT_INSTRUCTION,
                   "harness_source_manifest": _code_manifest(), "immutability": "Content-addressed and verify-before-use; not write-once storage"})
    frozen["common_support_files"] = []
    for entry in config.get("common_support_files", []):
        target = entry["target"]
        child(base, target)
        if not target.startswith("common_support/") or any(a["target"] == target for a in frozen["common_support_files"]):
            raise IntegrityError("Common support files require unique explicit common_support/ targets")
        asset = _asset(base, entry["source"])
        if asset["sha256"] != entry.get("sha256"):
            raise IntegrityError("Common support file differs from its declared pinned hash")
        frozen["common_support_files"].append({**asset, "target": target})
    frozen["common_support_sha256"] = digest([{k: v for k, v in entry.items() if k != "source"} for entry in frozen["common_support_files"]])
    ids = set()
    for source_task in config["tasks"]:
        task = {k: v for k, v in source_task.items() if k not in ("prompt", "inputs", "skill", "grader", "rubric", "oracle", "evaluator_files", "packet_files", "skill_package")}
        tid = task["task_id"]
        if not isinstance(tid, str) or not isinstance(task.get("family_id"), str) or tid in ids or not tid or not task.get("family_id"):
            raise IntegrityError("Task IDs must be unique and have a family")
        ids.add(tid)
        if not isinstance(task.get("timeout_s"), (int, float)) or isinstance(task.get("timeout_s"), bool) or task["timeout_s"] <= 0:
            raise IntegrityError("Each task requires a positive timeout")
        criteria = task.get("criteria")
        if not isinstance(criteria, list) or len(criteria) != 5 or any(not isinstance(c, str) or not c for c in criteria) or len(set(criteria)) != 5:
            raise IntegrityError("This pilot requires exactly five unique criterion groups")
        required_reviews = task.get("required_review_domains", [])
        if config["stage"] != "harness_test":
            required_reviews = list(dict.fromkeys([*required_reviews, "process_integrity", "free_text_and_verification_claims"]))
        if not isinstance(required_reviews, list) or any(not isinstance(v, str) or not v or len(v) > 80 for v in required_reviews) or len(set(required_reviews)) != len(required_reviews):
            raise IntegrityError("Invalid deferred review domain list")
        task["required_review_domains"] = required_reviews
        task.setdefault("review_min_raters", 2 if config["stage"] != "harness_test" else 1)
        rating_limits = [task["review_min_raters"],task.get("min_raters", 1), task.get("integrity_min_raters", 1), *task.get("group_min_raters", {}).values()]
        if any(not isinstance(n, int) or isinstance(n, bool) or n < 1 for n in rating_limits):
            raise IntegrityError("Every minimum rater count must be a positive integer")
        for kind in ("prompt", "skill", "grader", "rubric", "oracle"):
            task[kind] = _asset(base, source_task[kind])
        expected_skill_sha = task.get("skill_provenance", {}).get("sha256")
        if expected_skill_sha and expected_skill_sha != task["skill"]["sha256"]:
            raise IntegrityError("Guide differs from the pinned source manifest")
        if len(Path(task["skill"]["source"]).read_bytes()) == 0:
            raise IntegrityError("The supplied guide cannot be empty")
        task["skill_package"] = None
        if treatment == "designated_skill_package_supplied":
            package = source_task.get("skill_package")
            if not isinstance(package, dict) or not package.get("files"):
                raise IntegrityError("Package-supplied treatment needs an explicit pinned file allowlist")
            guide_target = package["guide_target"]
            child(base, guide_target)
            parts = guide_target.split("/")
            if len(parts) != 3 or parts[0] != "skill" or parts[-1] != "SKILL.md":
                raise IntegrityError("Package guide must preserve skill/<slug>/SKILL.md")
            prefix = "/".join(parts[:2]) + "/"
            files = []
            for entry in package["files"]:
                target = entry["target"]
                child(base, target)
                if not target.startswith(prefix) or any(value["target"] == target for value in files):
                    raise IntegrityError("Package file escapes its designated skill directory or duplicates a target")
                asset = _asset(base, entry["source"])
                if asset["sha256"] != entry.get("sha256"):
                    raise IntegrityError("Package file differs from its declared pinned hash")
                files.append({**asset, "target": target})
            guide = next((entry for entry in files if entry["target"] == guide_target), None)
            if guide is None or guide["sha256"] != task["skill"]["sha256"]:
                raise IntegrityError("Package does not contain the exact designated guide")
            task["skill_package"] = {"guide_target": guide_target, "files": files,
                "execution_copy": "fresh_owned_disposable_attempt_copy", "canonical_source_os_immutability_verified": False,
                "package_sha256": digest([{k: v for k, v in entry.items() if k != "source"} for entry in files])}
        elif source_task.get("skill_package"):
            raise IntegrityError("A standalone-guide contrast cannot silently add package files")
        task["evaluator_files"] = [_asset(base, name) for name in source_task.get("evaluator_files", [])]
        task["grader_bundle_sha256"] = digest([{k: v for k, v in a.items() if k != "source"} for a in [task[k] for k in ("grader", "rubric", "oracle")] + task["evaluator_files"]])
        task["packet_files"] = []
        for entry in source_task.get("packet_files", []):
            target = entry["target"]
            child(base, target)
            if target in ("task.txt", "guide.md", "inputs", "output", "skill", "common_support", "blind.json", "rubric.txt", "submission") or target.startswith(("inputs/", "output/", "skill/", "common_support/", "submission/")):
                raise IntegrityError("Packet auxiliary file collides with reserved layout")
            if any(p["target"] == target for p in task["packet_files"]):
                raise IntegrityError("Duplicate packet auxiliary target")
            task["packet_files"].append({**_asset(base, entry["source"]), "target": target})
        task["inputs"] = []
        names = set()
        for entry in source_task["inputs"]:
            target = entry["target"]
            child(base, target)  # Validate only, not read target.
            if target in names:
                raise IntegrityError("Duplicate staged input name")
            names.add(target)
            task["inputs"].append({**_asset(base, entry["source"]), "target": target, "protected": entry.get("protected", True)})
        for output in task.get("required_outputs", []):
            child(base, output)
        task["task_sha256"] = digest({"prompt_sha256": task["prompt"]["sha256"],
            "inputs": [{k: v for k, v in i.items() if k != "source"} for i in task["inputs"]],
            "packet_files": [{k: v for k, v in i.items() if k != "source"} for i in task["packet_files"]],
            "output_contract": task.get("required_outputs", []), "common_instruction": config["common_instruction"],
            "common_support_sha256": frozen["common_support_sha256"]})
        frozen["tasks"].append(task)
    if config["stage"] == "exploratory_pilot" and (config["repetitions"] != 1 or len(frozen["tasks"]) != 8 or len({t["family_id"] for t in frozen["tasks"]}) != 8):
        raise IntegrityError("The initial exploratory pilot requires eight distinct families/cases and one C/S pair per case")
    runner = frozen.setdefault("runner", {})
    binary = runner.get("binary_path")
    runner["binary_sha256"] = file_sha(binary) if binary else None
    missing_runtime = [k for k in ("binary_path", "cli_version", "requested_model", "reasoning_setting", "sandbox_mode") if not runner.get(k)]
    if config["stage"] != "harness_test" and missing_runtime:
        if not inspection_only:
            raise IntegrityError("Freeze explicit runtime configuration before non-fixture plans")
        pending.extend("runtime:" + key for key in missing_runtime)
    frozen["runner_sha256"] = digest({"configuration": runner, "harness": frozen["harness_source_manifest"]})
    if inspection_only:
        return {"schema_version": "dot-eval-source-inspection-1", "record_kind": "sources_checked_not_protocol_frozen_not_run",
            "stage": frozen["stage"], "treatment": treatment, "tasks": len(frozen["tasks"]),
            "package_files": sum(len((task.get("skill_package") or {}).get("files", [])) for task in frozen["tasks"]),
            "package_bytes": sum(sum(entry["bytes"] for entry in (task.get("skill_package") or {}).get("files", [])) for task in frozen["tasks"]),
            "common_support_files": len(frozen["common_support_files"]), "pending_freeze_fields": pending,
            "live_dispatch": "disabled", "runtime_isolation": "unverified",
            "source_content_sha256": digest({"common_support_sha256": frozen["common_support_sha256"], "treatment": treatment,
                "tasks": [{"task_id": task["task_id"], "task_sha256": task["task_sha256"], "skill_sha256": task["skill"]["sha256"],
                    "package_sha256": (task.get("skill_package") or {}).get("package_sha256"), "grader_bundle_sha256": task["grader_bundle_sha256"]} for task in frozen["tasks"]]})}
    frozen["protocol_sha256"] = digest(frozen)
    create_json(output_path, frozen)
    return frozen


def verify(protocol):
    if protocol.get("schema_version") != "dot-eval-frozen-1":
        raise IntegrityError("Expected a real frozen protocol, not a source inspection")
    claimed = protocol["protocol_sha256"]
    actual = digest({k: v for k, v in protocol.items() if k != "protocol_sha256"})
    if claimed != actual:
        raise IntegrityError("Protocol contents changed after freeze")
    if protocol["harness_source_manifest"] != _code_manifest():
        raise IntegrityError("Harness code changed after protocol freeze")
    for asset in protocol.get("common_support_files", []):
        if file_sha(asset["source"]) != asset["sha256"]:
            raise IntegrityError("Frozen common support source changed")
    for task in protocol["tasks"]:
        for asset in [task[k] for k in ("prompt", "skill", "grader", "rubric", "oracle")] + task["inputs"] + task.get("evaluator_files", []) + task.get("packet_files", []) + (task.get("skill_package") or {}).get("files", []):
            if file_sha(asset["source"]) != asset["sha256"]:
                raise IntegrityError(f"Frozen asset changed: {asset['source']}")
    runner = protocol["runner"]
    if runner.get("binary_path") and file_sha(runner["binary_path"]) != runner["binary_sha256"]:
        raise IntegrityError("Runner executable changed after freeze")
    return True


def schedule(protocol, seed):
    verify(protocol)
    rng = random.Random(seed)
    rows = []
    # Repeat rounds remain separate; within each round, balanced CS/SC and shuffled blocks.
    for repetition in range(1, protocol["repetitions"] + 1):
        tasks = list(protocol["tasks"])
        rng.shuffle(tasks)
        orders = [ARMS if i % 2 == 0 else tuple(reversed(ARMS)) for i in range(len(tasks))]
        rng.shuffle(orders)
        for task, order in zip(tasks, orders):
            block_id = f"b{len(rows) // 2 + 1:04d}"
            for position, arm in enumerate(order, 1):
                rows.append({"attempt_id": f"a{len(rows) + 1:04d}", "block_id": block_id, "family_id": task["family_id"],
                    "task_id": task["task_id"], "repetition": repetition, "arm": arm, "within_pair_position": position,
                    "randomized_position": len(rows) + 1, "timeout_s": task["timeout_s"], "retry_of": None})
    result = {"schema_version": "dot-eval-schedule-1", "protocol_sha256": protocol["protocol_sha256"],
        "seed": seed, "prng": "Python random.Random; exact schedule is frozen, do not depend on re-generation",
        "concurrency": 1, "rows": rows}
    result["schedule_sha256"] = digest(result)
    return result


def initialize(protocol, plan, study_dir):
    verify(protocol)
    validate_schedule(protocol, plan)
    root = Path(study_dir)
    root.mkdir(parents=True, exist_ok=False)
    create_json(root / "protocol.json", protocol)
    create_json(root / "schedule.json", plan)
    ledger = Ledger(root / "attempts.jsonl")
    for row in plan["rows"]:
        ledger.append("scheduled", **row, stage=protocol["stage"], protocol_sha256=protocol["protocol_sha256"])
    return root


def prepare(study_dir, attempt_id):
    preparation_started = time.monotonic()
    root = Path(study_dir).resolve()
    protocol, _, events = read_study(root)
    ledger = Ledger(root / "attempts.jsonl")
    matching = [r["payload"] for r in events if r["event"] == "scheduled" and r["payload"]["attempt_id"] == attempt_id]
    if len(matching) != 1:
        raise IntegrityError("Unknown or duplicate scheduled attempt")
    if any(r["event"] in ("prepared", "started", "finished") and r["payload"].get("attempt_id") == attempt_id for r in events):
        raise IntegrityError("An attempt is immutable; record a separately authorized retry, never overwrite")
    row = matching[0]
    task = next(t for t in protocol["tasks"] if t["task_id"] == row["task_id"])
    attempt_root = root / "workspaces" / uuid.uuid4().hex
    attempt_root.mkdir(parents=True, exist_ok=False)
    try:
        (attempt_root / "inputs").mkdir()
        (attempt_root / "output").mkdir()
        for entry in task["inputs"]:
            target = child(attempt_root / "inputs", entry["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(entry["source"], target)
        shutil.copyfile(task["prompt"]["source"], attempt_root / "task.txt")
        for entry in task.get("packet_files", []):
            target = child(attempt_root, entry["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(entry["source"], target)
        for entry in protocol.get("common_support_files", []):
            target = child(attempt_root, entry["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(entry["source"], target)
        if row["arm"] == "S":
            if task.get("skill_package"):
                for entry in task["skill_package"]["files"]:
                    target = child(attempt_root, entry["target"])
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(entry["source"], target)
            else:
                shutil.copyfile(task["skill"]["source"], attempt_root / "guide.md")
        prompt = execution_prompt(protocol, task, row["arm"])
        # Controller-only execution prompt; not placed inside the task packet.
        metadata = {"attempt_id": attempt_id, "workspace": str(attempt_root), "prompt": prompt,
            "prompt_sha256": digest(prompt), "common_task_sha256": task["task_sha256"],
            "skill_sha256": task["skill"]["sha256"] if row["arm"] == "S" else None,
            "treatment": protocol["treatment"], "skill_package_sha256": (task.get("skill_package") or {}).get("package_sha256") if row["arm"] == "S" else None,
            "source_manifest": file_manifest(attempt_root), "prepared_at_utc": utc_now(), "preparation_elapsed_s": time.monotonic() - preparation_started,
            "isolation": "UNVERIFIED: directories are not a read-access or skill-catalog boundary"}
        create_json(root / "control" / f"{attempt_id}.json", metadata)
        if metadata["source_manifest"] != expected_packet_manifest(task, row["arm"], protocol):
            raise IntegrityError("Copied task packet differs from its frozen sources")
        ledger.append("prepared", control_sha256=digest(metadata), **{k: v for k, v in metadata.items() if k != "prompt"})
        return metadata
    except Exception as error:
        ledger.append("finished", attempt_id=attempt_id, status="preparation_failed", error_type=type(error).__name__,
                      evidence_kind="not_executed", timing=None, usage=None)
        raise


def validate_schedule(protocol, plan):
    """Check a self-hash AND the complete frozen design, not just pair syntax."""
    if plan.get("schema_version") != "dot-eval-schedule-1" or plan.get("protocol_sha256") != protocol["protocol_sha256"]:
        raise IntegrityError("Schedule protocol/schema mismatch")
    if digest({k: v for k, v in plan.items() if k != "schedule_sha256"}) != plan.get("schedule_sha256"):
        raise IntegrityError("Schedule content hash mismatch")
    if plan.get("concurrency") != 1 or not isinstance(plan.get("seed"), int) or isinstance(plan["seed"], bool):
        raise IntegrityError("Invalid frozen scheduling configuration")
    tasks = {t["task_id"]: t for t in protocol["tasks"]}
    expected = {(tid, repetition, arm) for tid in tasks for repetition in range(1, protocol["repetitions"] + 1) for arm in ARMS}
    rows = plan.get("rows")
    if not isinstance(rows, list) or len(rows) != len(expected):
        raise IntegrityError("Schedule omits or adds predeclared attempts")
    seen = set()
    first_arm_counts = {rep: {arm: 0 for arm in ARMS} for rep in range(1, protocol["repetitions"] + 1)}
    prior_rep = 1
    keys = {"attempt_id", "block_id", "family_id", "task_id", "repetition", "arm", "within_pair_position", "randomized_position", "timeout_s", "retry_of"}
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != keys:
            raise IntegrityError("Schedule row schema changed")
        key = (row["task_id"], row["repetition"], row["arm"])
        if key not in expected or key in seen:
            raise IntegrityError("Missing, duplicated or undeclared schedule cell")
        seen.add(key)
        task = tasks[row["task_id"]]
        if row["attempt_id"] != f"a{index + 1:04d}" or row["randomized_position"] != index + 1 or row["block_id"] != f"b{index // 2 + 1:04d}" or row["within_pair_position"] != index % 2 + 1:
            raise IntegrityError("Schedule order/identity fields are inconsistent")
        if row["family_id"] != task["family_id"] or row["timeout_s"] != task["timeout_s"] or row["retry_of"] is not None:
            raise IntegrityError("Schedule task contract differs from protocol")
        if row["repetition"] < prior_rep:
            raise IntegrityError("Repetition rounds are not separated")
        prior_rep = row["repetition"]
        if index % 2 == 0:
            first_arm_counts[row["repetition"]][row["arm"]] += 1
        else:
            previous = rows[index - 1]
            if (previous["task_id"], previous["repetition"]) != (row["task_id"], row["repetition"]) or previous["arm"] == row["arm"]:
                raise IntegrityError("Scheduled adjacent block is not a matched C/S pair")
    if seen != expected or any(abs(counts["C"] - counts["S"]) > 1 for counts in first_arm_counts.values()):
        raise IntegrityError("Scheduled design is incomplete or arm order is unbalanced")
    return True


def read_study(study_dir):
    """Authenticate current frozen inputs and the entire scheduled ledger prefix.

    This detects missing planned blocks. Detecting deletion of a later valid suffix
    still requires an independently retained ledger head; it is not a signed store.
    """
    root = Path(study_dir).resolve()
    protocol = load_json(root / "protocol.json")
    verify(protocol)
    plan = load_json(root / "schedule.json")
    validate_schedule(protocol, plan)
    records = Ledger(root / "attempts.jsonl").read()
    scheduled = [r["payload"] for r in records if r["event"] == "scheduled"]
    expected = [dict(row, stage=protocol["stage"], protocol_sha256=protocol["protocol_sha256"]) for row in plan["rows"]]
    if scheduled != expected or [r["event"] for r in records[:len(expected)]] != ["scheduled"] * len(expected):
        raise IntegrityError("Ledger no longer contains every frozen scheduled attempt in order")
    ids = {row["attempt_id"] for row in plan["rows"]}
    for row in records:
        if row["payload"].get("attempt_id") not in ids:
            raise IntegrityError("Ledger event refers to an undeclared attempt")
    for aid in ids:
        related = [r for r in records if r["payload"]["attempt_id"] == aid]
        for kind in ("prepared", "started", "finished", "blind_exported"):
            if sum(r["event"] == kind for r in related) > 1:
                raise IntegrityError("Duplicate immutable attempt lifecycle event")
    return protocol, plan, records


def expected_packet_manifest(task, arm, protocol=None):
    assets = [("task.txt", task["prompt"])]
    assets += [("inputs/" + value["target"], value) for value in task["inputs"]]
    assets += [(value["target"], value) for value in task.get("packet_files", [])]
    assets += [(value["target"], value) for value in (protocol or {}).get("common_support_files", [])]
    if arm == "S":
        assets += [(value["target"], value) for value in task["skill_package"]["files"]] if task.get("skill_package") else [("guide.md", task["skill"])]
    return sorted([{"path": path, "sha256": value["sha256"], "bytes": value["bytes"]} for path, value in assets], key=lambda value: value["path"])


def prepared_control(study_dir, attempt_id, protocol, records):
    root = Path(study_dir).resolve()
    prepared = [r["payload"] for r in records if r["event"] == "prepared" and r["payload"]["attempt_id"] == attempt_id]
    if len(prepared) != 1:
        raise IntegrityError("Missing or duplicate frozen preparation record")
    metadata = load_json(root / "control" / f"{attempt_id}.json")
    if digest(metadata) != prepared[0].get("control_sha256"):
        raise IntegrityError("Controller preparation metadata changed after ledger binding")
    if {k: v for k, v in metadata.items() if k != "prompt"} != {k: v for k, v in prepared[0].items() if k != "control_sha256"}:
        raise IntegrityError("Preparation ledger/control metadata mismatch")
    scheduled = next(r["payload"] for r in records if r["event"] == "scheduled" and r["payload"]["attempt_id"] == attempt_id)
    task = next(t for t in protocol["tasks"] if t["task_id"] == scheduled["task_id"])
    expected = expected_packet_manifest(task, scheduled["arm"], protocol)
    prompt = execution_prompt(protocol, task, scheduled["arm"])
    if metadata["source_manifest"] != expected or metadata["common_task_sha256"] != task["task_sha256"] or metadata["prompt"] != prompt or metadata["prompt_sha256"] != digest(prompt):
        raise IntegrityError("Preparation differs from evaluator-held frozen task identities")
    workspace = Path(metadata["workspace"])
    if not workspace.is_absolute() or workspace.parent != root / "workspaces" or len(workspace.name) != 32 or any(c not in "0123456789abcdef" for c in workspace.name):
        raise IntegrityError("Prepared workspace escaped the controller-owned attempt layout")
    return metadata


def execution_prompt(protocol, task, arm):
    prompt = protocol["common_instruction"] + "\n\n" + protocol["common_output_instruction"]
    if arm == "S":
        addition = protocol["treatment_instruction"]
        if task.get("skill_package"):
            addition = addition.format(guide_path=task["skill_package"]["guide_target"])
        prompt += "\n\n" + addition
    return prompt
