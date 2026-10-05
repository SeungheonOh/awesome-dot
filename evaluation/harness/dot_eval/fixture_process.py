"""Authored subprocess test double; NO model/API/network calls; not benchmark output."""
import json
from pathlib import Path
import sys
import time


def emit(value):
    print(json.dumps(value), flush=True)


if __name__ == "__main__":
    mode = sys.argv[1]
    sys.stdin.read()
    emit({"type": "thread.started", "thread_id": "synthetic-test-double"})
    emit({"type": "turn.started"})
    if mode == "timeout":
        time.sleep(60)
    elif mode == "failed":
        print("synthetic fixture failure", file=sys.stderr)
        emit({"type": "turn.failed", "error": {"message": "synthetic only"}})
        raise SystemExit(2)
    elif mode == "truncated":
        print('{"type":', flush=True)
        raise SystemExit(0)
    elif mode == "duplicate_items":
        for kind in ("item.started", "item.updated", "item.completed", "item.completed"):
            emit({"type": kind, "item": {"id": "fixture-item", "type": "command_execution", "status": "completed"}})
    elif mode == "mutate_input":
        next(Path("inputs").rglob("*.txt")).write_text("deliberately modified by test double\n")
    Path("output").mkdir(exist_ok=True)
    Path("output/result.txt").write_text("SYNTHETIC FIXTURE ONLY\n", encoding="utf-8")
    event = {"type": "turn.completed"}
    if mode != "missing_usage":
        # Arbitrary authored counters test parsing only. Never model usage results.
        event["usage"] = {"input_tokens": 11, "cached_input_tokens": 3, "output_tokens": 5}
    emit(event)
