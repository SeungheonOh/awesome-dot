"""Recorded local fixture runner. Live Codex dispatch is deliberately disabled."""
from __future__ import annotations
import hashlib
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time
from .core import IntegrityError, Ledger, child, create_json, digest, file_manifest, file_sha, load_json, utc_now
from .protocol import prepare, verify, read_study, prepared_control
from .telemetry import CodexEvents


class RuntimeGateError(RuntimeError):
    pass


def codex_argv(protocol, workspace, final_answer_path):
    """Preview only. This is NOT a verified isolation configuration or a launcher."""
    r = protocol["runner"]
    if r.get("sandbox_mode") not in ("read-only", "workspace-write"):
        raise RuntimeGateError("Only existing read-only/workspace-write policies are supportable")
    if not r.get("requested_model") or not r.get("reasoning_setting"):
        raise RuntimeGateError("A fixed model label and reasoning setting must be declared")
    return [r["binary_path"], "exec", "--json", "--ephemeral", "--skip-git-repo-check", "--color", "never",
        "--sandbox", r["sandbox_mode"], "--cd", str(workspace), "--model", r["requested_model"],
        "-c", f'model_reasoning_effort="{r["reasoning_setting"]}"',
        "--output-last-message", str(final_answer_path), "-"]


def run_live(*args, **kwargs):
    raise RuntimeGateError("Live model dispatch is not implemented or authorized in this scaffold. Resolve runtime startup, supported containment/catalog controls, task/grader freeze and trial authorization first. No bypass flags, credential copying, or security changes are provided.")


def _capture_fixture(argv, cwd, prompt, timeout_s):
    """Private plumbing called only with this package's synthetic fixture producer."""
    started = time.monotonic()
    utc_start = utc_now()
    events = CodexEvents()
    stderr_hash = hashlib.sha256()
    stderr_bytes = 0
    error_categories = set()
    first_stdout = None
    spawned = None
    process = None
    timed_out = False
    exit_code = None
    spawn_error = None
    try:
        process = subprocess.Popen(argv, cwd=cwd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            start_new_session=True, env={"PATH": os.environ.get("PATH", ""), "PYTHONIOENCODING": "utf-8"})
        spawned = time.monotonic()
        process.stdin.write(prompt.encode("utf-8"))
        process.stdin.close()
        messages = queue.Queue()
        def read_stream(stream, label):
            try:
                for line in iter(stream.readline, b""):
                    messages.put((label, line, time.monotonic()))
            finally:
                stream.close()
                messages.put((label, None, time.monotonic()))
        threads = [threading.Thread(target=read_stream, args=(stream, label), daemon=True)
                   for stream, label in ((process.stdout, "stdout"), (process.stderr, "stderr"))]
        for thread in threads:
            thread.start()
        closed = set()
        kill_at = None
        while len(closed) < 2:
            now = time.monotonic()
            if not timed_out and now - started >= timeout_s:
                timed_out = True
                kill_at = now
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            # A surviving inherited pipe cannot keep controller accounting open forever.
            if kill_at is not None and now - kill_at > 2:
                error_categories.add("pipe_drain_incomplete")
                break
            try:
                label, line, observed = messages.get(timeout=min(0.02, max(0.001, timeout_s - (now - started))))
            except queue.Empty:
                continue
            if line is None:
                closed.add(label)
            elif label == "stdout":
                if first_stdout is None:
                    first_stdout = observed - started
                events.feed(line, observed - started)
            else:
                stderr_hash.update(line)
                stderr_bytes += len(line)
                lower = line.lower()
                for needle, category in ((b"read-only", "read_only_filesystem"), (b"permission", "permission_error"),
                    (b"authentication", "authentication_error"), (b"rate limit", "rate_limit"), (b"fixture", "synthetic_fixture_diagnostic")):
                    if needle in lower:
                        error_categories.add(category)
        exit_code = process.wait(timeout=2)
    except (OSError, subprocess.TimeoutExpired, BrokenPipeError) as error:
        spawn_error = type(error).__name__
        if process is not None and process.poll() is None:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            exit_code = process.wait()
    ended = time.monotonic()
    elapsed = ended - started
    terminal_s = events.last_terminal_s
    metadata = events.finish(exit_code, timed_out)
    status = ("launch_failed" if spawn_error else "timed_out" if timed_out else "process_failed" if exit_code != 0
              else "event_capture_incomplete" if not metadata["capture_complete"] else "completed")
    return {"status": status, "exit_code": exit_code, "timeout": timed_out, "error_type": spawn_error,
        "timing": {"utc_before_dispatch": utc_start, "utc_result_observed": utc_now(), "monotonic_elapsed_s": elapsed,
            "process_spawn_s": spawned - started if spawned else None, "first_stdout_observed_s": first_stdout,
            "first_turn_observed_s": events.first_turn_s, "last_terminal_observed_s": terminal_s,
            "first_to_terminal_observed_s": terminal_s - events.first_turn_s if terminal_s is not None and events.first_turn_s is not None else None,
            "terminal_to_process_observed_s": elapsed - terminal_s if terminal_s is not None else None,
            "model_compute_s": None, "service_queue_s": None, "tool_compute_s": None, "human_effort_s": None,
            "time_budget_s": timeout_s, "boundary_description": "Monotonic before local Popen through process and stream completion; event times are controller arrival observations, not provider compute durations"},
        "events": metadata, "usage": metadata["usage"], "billing": metadata["billing"],
        "stderr": {"sha256": stderr_hash.hexdigest(), "bytes": stderr_bytes, "categories": sorted(error_categories), "raw_retained": False},
        "redacted_events": events.safe_events}


def run_fixture(study_dir, attempt_id, mode="success", timeout_override=None):
    if mode not in ("success", "failed", "timeout", "truncated", "missing_usage", "duplicate_items", "mutate_input"):
        raise IntegrityError("Unknown synthetic fixture mode")
    root = Path(study_dir).resolve()
    protocol, _, events = read_study(root)
    if protocol["stage"] != "harness_test":
        raise RuntimeGateError("Synthetic process fixtures may run only in harness_test studies")
    ledger = Ledger(root / "attempts.jsonl")
    if any(e["event"] in ("started", "finished") and e["payload"].get("attempt_id") == attempt_id for e in events):
        raise IntegrityError("Attempt already started or finished")
    control = root / "control" / f"{attempt_id}.json"
    if not control.exists():
        prepare(root, attempt_id)
        protocol, _, events = read_study(root)
    metadata = prepared_control(root, attempt_id, protocol, events)
    scheduled = next(e["payload"] for e in ledger.read() if e["event"] == "scheduled" and e["payload"]["attempt_id"] == attempt_id)
    task = next(t for t in protocol["tasks"] if t["task_id"] == scheduled["task_id"])
    workspace = Path(metadata["workspace"])
    if file_manifest(workspace) != metadata["source_manifest"]:
        raise IntegrityError("Prepared packet changed before dispatch")
    timeout = timeout_override if timeout_override is not None else task["timeout_s"]
    if timeout <= 0:
        raise IntegrityError("Positive fixture timeout required")
    argv = [sys.executable, str(Path(__file__).with_name("fixture_process.py")), mode]
    ledger.append("started", attempt_id=attempt_id, evidence_kind="synthetic_fixture_only", argv_sha256=digest(argv),
                  timeout_s=timeout, timeout_override_for_harness_test=timeout_override)
    result = {"timing": None, "usage": None}
    try:
        result = _capture_fixture(argv, str(workspace), metadata["prompt"], timeout)
        create_json(root / "telemetry" / f"{attempt_id}.json", result.pop("redacted_events"))
        after = file_manifest(workspace)
        before_map = {f["path"]: f["sha256"] for f in metadata["source_manifest"]}
        after_map = {f["path"]: f["sha256"] for f in after}
        unprotected = {"inputs/" + i["target"] for i in task["inputs"] if not i["protected"]}
        changed = [p for p, sha in before_map.items() if p not in unprotected and after_map.get(p) != sha]
        artifact_manifest = file_manifest(workspace / "output")
        present = {f["path"] for f in artifact_manifest}
        missing = [p for p in task["required_outputs"] if p not in present]
        canonical_assets = (task.get("skill_package") or {}).get("files", [])
        canonical_after = [{"target": entry["target"], "sha256": file_sha(entry["source"])} for entry in canonical_assets]
        canonical_preserved = all(after["sha256"] == before["sha256"] for before, after in zip(canonical_assets, canonical_after))
        result.update({"canonical_package_sources_unchanged": canonical_preserved,
            "canonical_package_source_hashes_after": canonical_after, "artifact_manifest": artifact_manifest, "artifact_manifest_sha256": digest(artifact_manifest),
            "source_integrity": not changed and canonical_preserved, "changed_protected_paths": changed, "missing_required_outputs": missing,
            "contamination_flag": None, "external_effects_verified": False,
            "isolation": "unverified_shared_filesystem_fixture_process_only"})
        if changed or not canonical_preserved:
            result["status"] = "integrity_failed"
        elif missing and result["status"] == "completed":
            result["status"] = "missing_output"
    except Exception as error:
        result.pop("redacted_events", None)
        result.update({"status": "integrity_failed" if isinstance(error, IntegrityError) else "controller_failed",
                  "collection_integrity_failure": isinstance(error, IntegrityError), "collection_error_type": type(error).__name__})
    ledger.append("finished", attempt_id=attempt_id, evidence_kind="synthetic_fixture_only", **result)
    return result
