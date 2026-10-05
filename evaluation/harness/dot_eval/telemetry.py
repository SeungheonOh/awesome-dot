"""Allowlisted Codex JSONL metrics; no raw reasoning, IDs or arbitrary status text."""
from __future__ import annotations
import hashlib
import json
import math
import re
from .core import canonical

USAGE_KEYS = ("input_tokens", "cached_input_tokens", "cache_write_input_tokens", "output_tokens", "reasoning_output_tokens")
ITEM_TYPES = ("command_execution", "mcp_tool_call", "web_search", "file_change", "agent_message", "reasoning", "todo_list")
EVENT_TYPES = ("thread.started", "turn.started", "turn.completed", "turn.failed", "item.started", "item.updated", "item.completed", "error")
ITEM_STATUSES = ("in_progress", "pending", "running", "completed", "failed", "cancelled", "canceled")
MODEL_LABEL = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:/+\-]{0,127}\Z")


class CodexEvents:
    def __init__(self):
        self.items = {}
        self.turns = []
        self.turn_index = -1
        self.started_turn_count = 0
        self.open_turn = False
        self.event_count = 0
        self.parse_errors = 0
        self.schema_warnings = []
        self.safe_events = []
        self.first_event_s = None
        self.first_turn_s = None
        self.last_terminal_s = None
        self.error_events = 0
        self.observed_model_metadata = []
        self._raw_hash = hashlib.sha256()
        self.raw_bytes = 0

    def _warn(self, name):
        if name not in self.schema_warnings:
            self.schema_warnings.append(name)

    def feed(self, line, elapsed_s=None):
        if isinstance(line, str):
            line = line.encode("utf-8", "surrogatepass")
        self._raw_hash.update(line)
        self.raw_bytes += len(line)
        if len(line) > 1024 * 1024 or self.raw_bytes > 64 * 1024 * 1024 or self.event_count >= 100000:
            self._warn("event_stream_size_limit_exceeded")
            return
        if not line.strip():
            return
        def strict_pairs(pairs):
            value = {}
            for key, item in pairs:
                if key in value:
                    raise ValueError("Duplicate event key")
                value[key] = item
            return value
        try:
            event = json.loads(line, object_pairs_hook=strict_pairs,
                parse_constant=lambda value: (_ for _ in ()).throw(ValueError("Non-finite event number")))
            if not isinstance(event, dict) or not isinstance(event.get("type"), str):
                raise ValueError("Expected an event object")
        except (ValueError, UnicodeDecodeError, RecursionError):
            self.parse_errors += 1
            return
        self.event_count += 1
        if elapsed_s is not None and (not isinstance(elapsed_s, (int, float)) or isinstance(elapsed_s, bool) or not math.isfinite(elapsed_s) or elapsed_s < 0):
            self._warn("invalid_controller_observation_time")
            elapsed_s = None
        if self.first_event_s is None:
            self.first_event_s = elapsed_s
        kind = event["type"]
        if kind not in EVENT_TYPES:
            self._warn("unrecognized_event_type")
            self.safe_events.append({"type": "unrecognized_event", "observed_elapsed_s": elapsed_s})
            return
        if kind in ("thread.started", "turn.started", "turn.completed"):
            for field in ("model", "model_version", "model_build_id", "service_tier"):
                value = event.get(field)
                if value is None:
                    continue
                if not isinstance(value, str) or not MODEL_LABEL.fullmatch(value):
                    self._warn("unrecognized_model_metadata_shape")
                    continue
                entry = {"event_type": kind, "event_number": self.event_count, "field": field, "value": value}
                if len(self.observed_model_metadata) < 100:
                    self.observed_model_metadata.append(entry)
                else:
                    self._warn("model_metadata_count_limit_exceeded")
        safe = {"type": kind, "observed_elapsed_s": elapsed_s}
        if kind == "turn.started":
            if self.open_turn:
                self._warn("overlapping_turn_starts")
            self.turn_index += 1
            self.started_turn_count += 1
            self.open_turn = True
            if self.first_turn_s is None:
                self.first_turn_s = elapsed_s
        elif kind in ("turn.completed", "turn.failed"):
            if self.turn_index < 0:
                self.turn_index = 0
                self._warn("terminal_without_turn_started")
            usage = event.get("usage")
            if usage is not None and not isinstance(usage, dict):
                self._warn("invalid_usage_object")
            usage = usage if isinstance(usage, dict) else {}
            values = {}
            for key in USAGE_KEYS:
                value = usage.get(key)
                if value is not None and (not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 2**63 - 1):
                    self._warn(f"invalid_usage_{key}")
                    value = None
                values[key] = value
            safe.update({"turn_index": self.turn_index, "usage": values,
                         "usage_field_presence": [k for k in USAGE_KEYS if k in usage]})
            prior = next((t for t in self.turns if t["turn_index"] == self.turn_index), None)
            turn = {"turn_index": self.turn_index, "terminal_type": kind, "usage": values,
                    "usage_field_presence": safe["usage_field_presence"]}
            if prior is None:
                self.turns.append(turn)
            elif prior != turn:
                self._warn("conflicting_terminal_events")
            self.open_turn = False
            self.last_terminal_s = elapsed_s
        elif kind in ("item.started", "item.updated", "item.completed"):
            item = event.get("item")
            if not isinstance(item, dict):
                self._warn("invalid_item_object")
            else:
                raw_id, item_type, status = item.get("id"), item.get("type"), item.get("status")
                if not isinstance(raw_id, str) or not 1 <= len(raw_id) <= 512:
                    self._warn("item_missing_or_invalid_id")
                else:
                    iid = hashlib.sha256(raw_id.encode("utf-8", "surrogatepass")).hexdigest()
                    if item_type not in ITEM_TYPES:
                        self._warn("unrecognized_item_type")
                        item_type = "unrecognized_item"
                    if status is not None and (not isinstance(status, str) or status not in ITEM_STATUSES):
                        self._warn("unrecognized_item_status")
                        status = None
                    safe.update({"item_id_sha256": iid, "item_type": item_type, "status": status})
                    old = self.items.get(iid)
                    if old and old["type"] != item_type:
                        self._warn("item_id_type_changed")
                        item_type = old["type"]
                    observed_exit = item.get("exit_code")
                    if observed_exit is not None and (not isinstance(observed_exit, int) or isinstance(observed_exit, bool) or not -65536 <= observed_exit <= 65536):
                        self._warn("invalid_item_exit_code")
                        observed_exit = None
                    error_observed = item.get("error") is not None
                    failed = status == "failed" or error_observed or observed_exit not in (None, 0)
                    if old and old["terminal"]:
                        if kind != "item.completed":
                            self._warn("item_update_after_terminal")
                        elif status != old["status"] or observed_exit != old["exit_code"]:
                            self._warn("conflicting_terminal_item_updates")
                        status, observed_exit = old["status"], old["exit_code"]
                    self.items[iid] = {"id_sha256": iid, "type": item_type, "status": status,
                        "terminal": kind == "item.completed" or (old or {}).get("terminal", False),
                        "error_observed": error_observed or (old or {}).get("error_observed", False),
                        "failure_observed": failed or (old or {}).get("failure_observed", False), "exit_code": observed_exit}
        elif kind == "error":
            self.error_events += 1
            safe["error_observed"] = True
        self.safe_events.append(safe)

    def finish(self, exit_code, timed_out=False):
        counts = {name: sum(i["type"] == name for i in self.items.values()) for name in ITEM_TYPES}
        terminal = self.turns[-1]["terminal_type"] if self.turns else None
        unfinished = sum(not i["terminal"] for i in self.items.values())
        complete = (exit_code == 0 and not timed_out and terminal == "turn.completed" and not self.open_turn
            and self.started_turn_count == 1 and len(self.turns) == 1 and self.parse_errors == 0 and not self.schema_warnings and unfinished == 0)
        values = dict.fromkeys(USAGE_KEYS)
        if len(self.turns) == 1:
            values.update(self.turns[0]["usage"])
        return {"event_count": self.event_count, "parse_errors": self.parse_errors,
            "schema_warnings": sorted(self.schema_warnings), "terminal_status": terminal,
            "per_turn": self.turns, "turn_count": len(self.turns), "started_turn_count": self.started_turn_count,
            "unfinished_turn": self.open_turn, "error_events": self.error_events,
            "logical_items": counts, "failed_items": sum(i["failure_observed"] for i in self.items.values()),
            "unfinished_items": unfinished, "counts_provenance": "Unique hashed emitted item IDs, not shell subcommands or all backend operations",
            "raw_stream_sha256": self._raw_hash.hexdigest(), "raw_stream_bytes": self.raw_bytes,
            "raw_stream_retained": False, "redacted_events_sha256": hashlib.sha256(canonical(self.safe_events)).hexdigest(),
            "capture_complete": complete, "usage": {**values, "source": "provider turn.completed/turn.failed event only",
                "capture_complete": complete, "counter_semantics_verified": False, "cross_category_total": None},
            "returned_model_label": next((m["value"] for m in reversed(self.observed_model_metadata) if m["field"] == "model"), None),
            "observed_model_metadata": self.observed_model_metadata, "exact_model_build": None,
            "metadata_semantics_verified": False,
            "billing": {"actual_cost": None, "currency": None, "source": None, "not_inferred_from_tokens": True}}
