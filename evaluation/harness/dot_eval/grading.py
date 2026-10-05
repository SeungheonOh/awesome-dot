"""Arm-hidden artifact exchange and independent, immutable grading records."""
from __future__ import annotations
import shutil
import time
import uuid
from pathlib import Path
from .core import IntegrityError, Ledger, child, create_json, digest, file_manifest, load_json, copy_verified_file
from .protocol import read_study, prepared_control


def blind_export(study_dir, attempt_id, destination):
    export_started = time.monotonic()
    root = Path(study_dir).resolve()
    protocol, _, records = read_study(root)
    ledger = Ledger(root / "attempts.jsonl")
    if any(r["event"] == "blind_exported" and r["payload"].get("attempt_id") == attempt_id for r in records):
        raise IntegrityError("A frozen blind submission already exists for this attempt")
    row = next((r["payload"] for r in records if r["event"] == "scheduled" and r["payload"]["attempt_id"] == attempt_id), None)
    finished = next((r["payload"] for r in records if r["event"] == "finished" and r["payload"]["attempt_id"] == attempt_id), None)
    if not row or not finished or "artifact_manifest" not in finished:
        raise IntegrityError("Only a recorded frozen artifact submission can be exported")
    task = next(t for t in protocol["tasks"] if t["task_id"] == row["task_id"])
    workspace = Path(prepared_control(root, attempt_id, protocol, records)["workspace"])
    current = file_manifest(workspace / "output")
    if current != finished["artifact_manifest"]:
        raise IntegrityError("Submission changed after attempt completion")
    blind_id = uuid.uuid4().hex
    destination = Path(destination).resolve() / blind_id
    if destination.is_relative_to(workspace):
        raise IntegrityError("Blind grading material cannot be placed in the runner workspace")
    destination.mkdir(parents=True, exist_ok=False)
    copy_verified_file(task["prompt"]["source"], destination / "task.txt", task["prompt"]["sha256"], task["prompt"]["bytes"])
    copy_verified_file(task["rubric"]["source"], destination / "rubric.txt", task["rubric"]["sha256"], task["rubric"]["bytes"])
    for entry in task["inputs"]:
        target = child(destination / "inputs", entry["target"])
        target.parent.mkdir(parents=True, exist_ok=True)
        copy_verified_file(entry["source"], target, entry["sha256"], entry["bytes"])
    for entry in task.get("packet_files", []):
        target = child(destination, entry["target"])
        target.parent.mkdir(parents=True, exist_ok=True)
        copy_verified_file(entry["source"], target, entry["sha256"], entry["bytes"])
    (destination / "submission").mkdir()
    for entry in current:
        target = child(destination / "submission", entry["path"])
        target.parent.mkdir(parents=True, exist_ok=True)
        copy_verified_file(workspace / "output" / entry["path"], target, entry["sha256"], entry["bytes"])
    trace_sha = (finished.get("events") or {}).get("redacted_events_sha256")
    if trace_sha is not None and digest(load_json(root / "telemetry" / f"{attempt_id}.json")) != trace_sha:
        raise IntegrityError("Recorded sanitized trace changed before review export")
    review_evidence = {"schema_version": "dot-eval-review-evidence-1", "submission_sha256": digest(current),
        "redacted_trace_sha256": trace_sha, "trace_capture_complete": (finished.get("events") or {}).get("capture_complete"),
        "source_integrity": finished.get("source_integrity"), "external_effects_verified": finished.get("external_effects_verified"),
        "process_integrity_pass_supported": False,
        "limitation": "The scaffold has no verified containment/full activity observation; absence of unauthorized external effects cannot be certified from these metrics"}
    create_json(root / "review-evidence" / f"{attempt_id}.json", review_evidence)
    manifest = file_manifest(destination)
    blind = {"schema_version": "dot-eval-blind-1", "blind_id": blind_id, "criteria": task["criteria"],
        "submission_sha256": digest(current), "package_sha256": digest(manifest),
        "artifact_manifest": current, "required_review_domains": task.get("required_review_domains", []),
        "review_evidence_sha256": digest(review_evidence), "blindness": {"arm_guide_timing_logs_withheld": True,
            "content_may_self_identify_treatment": True, "access_boundary_enforced": False},
        "instructions": "Judge task-contract correctness and source support. Do not infer the treatment, consult sibling attempts, or require the guide's wording/style. Report any suspected unblinding."}
    create_json(destination / "blind.json", blind)
    ledger.append("blind_exported", attempt_id=attempt_id, blind_id=blind_id, destination=str(destination),
        submission_sha256=blind["submission_sha256"], package_sha256=blind["package_sha256"], blind_contract_sha256=digest(blind), grader_sha256=task["grader"]["sha256"],
        review_evidence_sha256=digest(review_evidence), review_evidence_path=str(root / "review-evidence" / f"{attempt_id}.json"),
        export_processing_s=time.monotonic() - export_started)
    return blind


def normalize_grade(report, criteria, review_domains=()):
    if not isinstance(report, dict):
        raise IntegrityError("Grade must be an object")
    groups = report.get("groups")
    if not isinstance(groups, list) or len(groups) != len(criteria):
        raise IntegrityError("A grade must report every frozen criterion, with null for unscored")
    normalized = {}
    for group in groups:
        if not isinstance(group, dict):
            raise IntegrityError("A grade criterion must be an object")
        gid = group.get("id")
        value = group.get("passed")
        if not isinstance(gid, str) or gid in normalized or gid not in criteria or (value is not None and not isinstance(value, bool)):
            raise IntegrityError("Unknown, duplicate or invalid grade criterion")
        normalized[gid] = value
    if set(normalized) != set(criteria):
        raise IntegrityError("Criterion set mismatch")
    integrity_object = report.get("integrity", {})
    if not isinstance(integrity_object, dict):
        raise IntegrityError("Integrity result must be an object")
    integrity = integrity_object.get("passed")
    if integrity is not None and not isinstance(integrity, bool):
        raise IntegrityError("Integrity must be true, false, or null")
    reviews = dict.fromkeys(review_domains)
    supplied_reviews = report.get("review_domains", {})
    if not isinstance(supplied_reviews, dict):
        raise IntegrityError("Deferred reviews must be a domain-to-boolean/null object")
    for domain, value in supplied_reviews.items():
        if domain not in reviews or (value is not None and not isinstance(value, bool)):
            raise IntegrityError("Unknown or invalid deferred review domain")
        reviews[domain] = value
    infrastructure_blocked = bool(report.get("infrastructure_reason"))
    if infrastructure_blocked:
        normalized = dict.fromkeys(criteria)
        integrity = None
        reviews = dict.fromkeys(review_domains)
    method = report.get("review_method")
    if method not in (None, "automated", "ai_assisted", "human", "mixed", "synthetic_test"):
        raise IntegrityError("Unknown review method")
    for key in ("suspected_unblinding", "independence_attested"):
        if report.get(key) is not None and not isinstance(report[key], bool):
            raise IntegrityError("Review attestations must be booleans or null")
    return {"groups": normalized, "integrity": integrity, "review_domains": reviews,
        "infrastructure_blocked": infrastructure_blocked, "review_method": method,
        "suspected_unblinding": report.get("suspected_unblinding", False),
        "independence_attested": report.get("independence_attested", None)}


def import_grade(study_dir, blind_id, grade_path, rater_id, kind="rating"):
    import_started = time.monotonic()
    if kind not in ("rating", "adjudication"):
        raise IntegrityError("Grade kind must be rating or adjudication")
    root = Path(study_dir)
    protocol, _, records = read_study(root)
    ledger = Ledger(root / "attempts.jsonl")
    exported = next((r["payload"] for r in records if r["event"] == "blind_exported" and r["payload"]["blind_id"] == blind_id), None)
    if not exported:
        raise IntegrityError("Unknown blind submission")
    attempt_id = exported["attempt_id"]
    existing = [r["payload"] for r in records if r["event"] == "graded" and r["payload"]["attempt_id"] == attempt_id]
    if any(g["rater_id"] == rater_id for g in existing):
        raise IntegrityError("Rater already submitted; ratings cannot be overwritten")
    if kind == "adjudication" and len([g for g in existing if g["kind"] == "rating"]) < 2:
        raise IntegrityError("Adjudication requires at least two independently recorded prior ratings")
    packet = Path(exported["destination"])
    if digest([f for f in file_manifest(packet) if f["path"] != "blind.json"]) != exported["package_sha256"]:
        raise IntegrityError("Blind package changed after export")
    report = load_json(grade_path)
    if report.get("blind_id") != blind_id or report.get("submission_sha256") != exported["submission_sha256"]:
        raise IntegrityError("Grade must bind to the exact blind ID and submission hash")
    contract = load_json(packet / "blind.json")
    if digest(contract) != exported.get("blind_contract_sha256"):
        raise IntegrityError("Blind grading contract changed after export")
    review_evidence = load_json(exported["review_evidence_path"])
    if digest(review_evidence) != exported["review_evidence_sha256"] or contract["review_evidence_sha256"] != exported["review_evidence_sha256"]:
        raise IntegrityError("Deferred review evidence changed after export")
    normalized = normalize_grade(report, contract["criteria"], contract.get("required_review_domains", []))
    if any(value is not None for value in normalized["review_domains"].values()):
        if report.get("review_evidence_sha256") != exported["review_evidence_sha256"] or normalized["independence_attested"] is not True:
            raise IntegrityError("Actual deferred review must bind exact artifacts/trace evidence and attest independence")
        if normalized["review_method"] not in ("ai_assisted", "human", "mixed", "synthetic_test"):
            raise IntegrityError("Automated artifact checks cannot assert a completed semantic/process review")
        if normalized["review_domains"].get("process_integrity") is True and review_evidence["process_integrity_pass_supported"] is not True:
            raise IntegrityError("Current partial activity evidence cannot certify process integrity")
    ledger.append("graded", attempt_id=attempt_id, blind_id=blind_id, rater_id=rater_id, kind=kind,
        report_sha256=digest(report), grader_sha256=exported["grader_sha256"],
        review_evidence_sha256=exported["review_evidence_sha256"], grade_import_processing_s=time.monotonic() - import_started, actual_grading_elapsed_s=None, human_effort_s=None, **normalized)
    # Preserve full rubric assertions in controller space; never expose them to a runner.
    create_json(root / "grades" / f"{uuid.uuid4().hex}.json", report)
    return normalized


def resolve_grades(grades, task):
    adjudications = [g for g in grades if g["kind"] == "adjudication"]
    if len(adjudications) > 1:
        raise IntegrityError("Multiple adjudications require a new explicit protocol, not last-wins")
    groups = {}
    disagreement = []
    if adjudications:
        groups = adjudications[0]["groups"]
        integrity = adjudications[0]["integrity"]
    else:
        for gid in task["criteria"]:
            votes = [g["groups"][gid] for g in grades if g["groups"][gid] is not None]
            minimum = task.get("group_min_raters", {}).get(gid, task.get("min_raters", 1))
            if len(set(votes)) > 1:
                disagreement.append(gid)
            groups[gid] = votes[0] if len(votes) >= minimum and len(set(votes)) == 1 else None
        integrity_votes = [g["integrity"] for g in grades if g["integrity"] is not None]
        if len(set(integrity_votes)) > 1:
            disagreement.append("integrity")
        integrity = (integrity_votes[0] if len(integrity_votes) >= task.get("integrity_min_raters", 1)
                     and len(set(integrity_votes)) == 1 else None)
    reviews = {}
    for domain in task.get("required_review_domains", []):
        if adjudications:
            reviews[domain] = adjudications[0].get("review_domains", {}).get(domain)
        else:
            votes = [g.get("review_domains", {}).get(domain) for g in grades if g.get("review_domains", {}).get(domain) is not None]
            if len(set(votes)) > 1:
                disagreement.append("review:" + domain)
            reviews[domain] = votes[0] if len(votes) >= task.get("review_min_raters", 1) and len(set(votes)) == 1 else None
    values = list(groups.values())
    acceptance_values = values + list(reviews.values())
    accepted = False if integrity is False or False in acceptance_values else True if integrity is True and all(v is True for v in acceptance_values) else None
    quality = sum(v is True for v in values) / len(values) if all(v is not None for v in values) else None
    return {"accepted": accepted, "quality_fraction": quality, "integrity": integrity,
        "groups": groups, "review_domains": reviews, "deferred_review_pending": any(value is None for value in reviews.values()),
        "evaluator_infrastructure_blocked": any(g.get("infrastructure_blocked") for g in grades), "disagreement": disagreement, "adjudicated": bool(adjudications),
        "rater_count": len(grades), "suspected_unblinding": any(g.get("suspected_unblinding") for g in grades)}
