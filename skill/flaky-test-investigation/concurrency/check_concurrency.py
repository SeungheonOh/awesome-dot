#!/usr/bin/env python3
"""Original local asyncio fixture. Python 3.11+; standard library only."""

import argparse
import asyncio
from collections import Counter
import hashlib
import inspect
import json
from pathlib import Path
import platform
import sys

from tally_before import Tally as Before
from tally_after import Tally as After


INITIAL = 7
ADDITIONS = {"A": 2, "B": 3}
ORDINARY_REPETITIONS = 8
CASE_TIMEOUT_SECONDS = 5
SOURCE_FILES = ("check_concurrency.py", "tally_before.py", "tally_after.py")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def correctness_assertion(actual, initial, additions):
    # This exact function is used before, after, and for all negative controls.
    require(type(actual) is int, "The stored total must be an integer")
    require(actual == initial + sum(additions.values()),
            f"Lost or extra addition: expected {initial + sum(additions.values())}, got {actual}")


def source_hashes():
    return {name: sha(Path(__file__).with_name(name).read_bytes()) for name in SOURCE_FILES}


async def next_loop_turn():
    """Model a local async operation's completion, without wall-clock sleeps."""
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    def complete():
        # Cancellation can settle the future before this queued callback runs.
        if not future.done():
            future.set_result(None)

    handle = loop.call_soon(complete)
    try:
        await future
    finally:
        handle.cancel()


class FixtureStore:
    """Each case gets a fresh fictional tally; no file, service, or global state."""

    def __init__(self, initial, first, controlled, trace):
        self.value = initial
        self.first = first
        self.controlled = controlled
        self.trace = trace
        self.first_read = asyncio.Event()
        self.release_first = asyncio.Event()
        self.contended = asyncio.Event()

    def emit(self, actor, step, **fields):
        self.trace.append({"sequence": len(self.trace) + 1, "actor": actor,
                           "step": step, **fields})

    async def read(self, actor):
        snapshot = self.value
        self.emit(actor, "read", value=snapshot)
        if self.controlled and actor == self.first:
            self.emit(actor, "pause_after_read")
            self.first_read.set()
            await self.release_first.wait()
            self.emit(actor, "resume_after_read")
        await next_loop_turn()
        return snapshot

    async def write(self, actor, value):
        await next_loop_turn()
        self.value = value
        self.emit(actor, "write", value=value)


class ObservedLock(asyncio.Lock):
    """Controlled cases only: observe public Lock methods without changing them."""

    def __init__(self, store):
        super().__init__()
        self.store = store

    async def acquire(self):
        actor = asyncio.current_task().get_name()
        locked = self.locked()
        self.store.emit(actor, "lock_attempt", observed_locked=locked)
        if locked:
            self.store.emit(actor, "lock_contended")
            self.store.contended.set()
        # No suspension between locked() and acquire() except acquire itself.
        acquired = await super().acquire()
        self.store.emit(actor, "lock_acquired")
        return acquired

    def release(self):
        super().release()
        self.store.emit(asyncio.current_task().get_name(), "lock_released")


class PerCallLock(After):
    """Negative control: a new lock per call does not protect shared state."""

    async def add(self, actor, amount):
        async with asyncio.Lock():
            current = await self.store.read(actor)
            await self.store.write(actor, current + amount)


class WriteOnlyLock(After):
    """Negative control: locking just the write preserves the stale read."""

    async def add(self, actor, amount):
        current = await self.store.read(actor)
        async with self._lock:
            await self.store.write(actor, current + amount)


async def exercise(product_type, mode, order, trace, initial, additions):
    controlled = mode == "controlled"
    store = FixtureStore(initial, order[0], controlled, trace)
    product = product_type(store)
    if controlled and hasattr(product, "_lock"):
        product._lock = ObservedLock(store)
    tasks = []
    branch = None

    async def worker(actor):
        store.emit(actor, "call_started", amount=additions[actor])
        await product.add(actor, additions[actor])
        store.emit(actor, "call_completed")

    def launch(actor):
        task = asyncio.create_task(worker(actor), name=actor)
        tasks.append(task)
        return task

    try:
        if controlled:
            first = launch(order[0])
            ready = asyncio.create_task(store.first_read.wait(), name="first-read-observer")
            tasks.append(ready)
            ready_or_done, _ = await asyncio.wait((first, ready), return_when=asyncio.FIRST_COMPLETED)
            if first in ready_or_done:
                first.result()
                raise RuntimeError("First worker completed without pausing at its controlled read")
            second = launch(order[1])
            notice = asyncio.create_task(store.contended.wait(), name="contention-observer")
            tasks.append(notice)
            done, _ = await asyncio.wait((second, notice), return_when=asyncio.FIRST_COMPLETED)
            if second in done:
                second.result()  # Worker errors are runner errors, never expected assertion failures.
                branch = "second_completed_while_first_paused"
            else:
                branch = "second_contended_on_held_lock"
            store.emit("controller", "release_first", reason=branch)
            store.release_first.set()
            await asyncio.gather(first, second)
        elif mode == "serial":
            for actor in order:
                await launch(actor)
        else:
            await asyncio.gather(*(launch(actor) for actor in order))
        return store.value, branch
    finally:
        # asyncio.wait does not cancel pending tasks. Explicitly settle all of ours.
        store.release_first.set()
        for task in tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


def trace_check(trace, revision, mode, order, initial, additions):
    if mode != "controlled" or revision not in ("before", "after"):
        return "not_applicable"
    operations = [(e["actor"], e["step"], e["value"])
                  for e in trace if e["step"] in ("read", "write")]
    first, second = order
    if revision == "before":
        expected = [(first, "read", initial), (second, "read", initial),
                    (second, "write", initial + additions[second]),
                    (first, "write", initial + additions[first])]
    else:
        expected = [(first, "read", initial),
                    (first, "write", initial + additions[first]),
                    (second, "read", initial + additions[first]),
                    (second, "write", initial + sum(additions.values()))]
        require(any(e["step"] == "lock_contended" and e["actor"] == second for e in trace),
                "Controlled repair did not observe lock contention")
    require(operations == expected, "Observed operations differ from the declared controlled schedule")
    return "passed"


async def run_case(slot, product_type, initial=INITIAL, additions=None):
    additions = dict(ADDITIONS if additions is None else additions)
    trace = []
    row = {**slot, "attempt": 1, "initial": initial, "additions": additions,
           "expected": initial + sum(additions.values()), "actual": None,
           "trace": trace, "detail": None, "schedule_check": "not_completed"}
    deadline = asyncio.timeout(CASE_TIMEOUT_SECONDS)
    try:
        async with deadline:
            actual, branch = await exercise(product_type, slot["mode"], slot["order"], trace, initial, additions)
        row.update(actual=actual, observed_branch=branch)
        row["schedule_check"] = trace_check(trace, slot["revision"], slot["mode"],
                                           slot["order"], initial, additions)
    except TimeoutError as error:
        if deadline.expired():
            row.update(outcome="timeout", detail="Case safety deadline expired; no correctness comparison")
        else:
            row.update(outcome="runner_error", detail=f"TimeoutError: {error}")
        return row
    except asyncio.CancelledError:
        row.update(outcome="cancelled", detail="Case cancelled; no correctness comparison")
        return row
    except Exception as error:
        row.update(outcome="runner_error", detail=f"{type(error).__name__}: {error}")
        return row
    try:
        correctness_assertion(actual, initial, additions)
    except AssertionError as error:
        row.update(outcome="assertion_fail", detail=str(error))
    else:
        row["outcome"] = "assertion_pass"
    return row


def planned_cases():
    plan = []
    for revision in ("before", "after"):
        for mode in ("serial", "controlled"):
            for order in (("A", "B"), ("B", "A")):
                plan.append({"revision": revision, "mode": mode, "order": list(order)})
        for repetition in range(1, ORDINARY_REPETITIONS + 1):
            plan.append({"revision": revision, "mode": "ordinary", "order": ["A", "B"],
                         "repetition": repetition})
    for revision in ("per_call_lock", "write_only_lock"):
        plan.append({"revision": revision, "mode": "controlled", "order": ["A", "B"]})
    return [{"slot": index, **slot} for index, slot in enumerate(plan, start=1)]


def summarize(rows):
    counts = Counter(row["outcome"] for row in rows)
    return {"attempted": len(rows), "completed_comparisons": counts["assertion_pass"] + counts["assertion_fail"],
            **{key: counts[key] for key in ("assertion_pass", "assertion_fail", "runner_error", "timeout", "cancelled")}}


async def experiment():
    identities = source_hashes()
    plan = planned_cases()
    types = {"before": Before, "after": After, "per_call_lock": PerCallLock, "write_only_lock": WriteOnlyLock}
    rows, unrun = [], []
    stop = None
    for slot in plan:
        if stop:
            unrun.append({**slot, "reason": stop})
            continue
        row = await run_case(slot, types[slot["revision"]])
        rows.append(row)
        if row["outcome"] not in ("assertion_pass", "assertion_fail"):
            stop = f"Stopped after slot {slot['slot']}: {row['outcome']}"

    controls = []
    for name, actual in (("lost_A", 10), ("lost_B", 9), ("extra_addition", 13), ("wrong_type", "12")):
        try:
            correctness_assertion(actual, INITIAL, ADDITIONS)
        except AssertionError as error:
            controls.append({"name": name, "actual": actual, "outcome": "assertion_fail", "detail": str(error)})
        else:
            controls.append({"name": name, "actual": actual, "outcome": "assertion_pass", "detail": "Invalid total accepted"})

    problems = []
    for row in rows:
        expected = None
        if row["revision"] in ("per_call_lock", "write_only_lock") or (row["revision"] == "before" and row["mode"] == "controlled"):
            expected = "assertion_fail"
        elif row["revision"] == "after" or row["mode"] == "serial":
            expected = "assertion_pass"
        if row["outcome"] not in ("assertion_pass", "assertion_fail") or (expected and row["outcome"] != expected):
            problems.append(f"Unexpected outcome in slot {row['slot']}: {row['outcome']}")
    if unrun:
        problems.append("Some planned slots were not run")
    if any(row["outcome"] != "assertion_fail" for row in controls):
        problems.append("An invalid-total control was accepted")
    unchanged = identities == source_hashes()
    if not unchanged:
        problems.append("Source files changed during the experiment")
    groups = {f"{revision}/{mode}": summarize([r for r in rows if r["revision"] == revision and r["mode"] == mode])
              for revision, mode in dict.fromkeys((p["revision"], p["mode"]) for p in plan)}
    fixture = {"initial": INITIAL, "additions": ADDITIONS}
    return {
        "scope": "Original fictional local asyncio tally; one loop, one tally owner, no external services",
        "command": "python3 -B check_concurrency.py", "source_files_sha256": identities,
        "product_sources_sha256": {"before": sha(inspect.getsource(Before).encode()), "after": sha(inspect.getsource(After).encode())},
        "correctness_assertion_sha256": sha(inspect.getsource(correctness_assertion).encode()),
        "fixture_sha256": sha(json.dumps(fixture, sort_keys=True).encode()),
        "environment": {"python": platform.python_version(), "implementation": platform.python_implementation(),
                        "os": platform.system(), "machine": platform.machine(), "optimization": sys.flags.optimize,
                        "dependencies": "standard library only", "event_loop": type(asyncio.get_running_loop()).__name__,
                        "workers": "two asyncio worker tasks on one thread", "randomness": "none; no seeds",
                        "clock": "monotonic timeout only; no sleeps", "timezone_locale": "not used"},
        "budget": {"planned": len(plan), "attempts_per_slot": 1, "hidden_retries": 0,
                   "case_timeout_seconds": CASE_TIMEOUT_SECONDS, "invalid_total_controls": len(controls),
                   "stop": "Finish fixed plan, or stop concurrency cases on timeout/cancellation/runner error",
                   "planned_cases": plan},
        "ledger": {**summarize(rows), "unrun": unrun, "skipped": 0}, "groups": groups,
        "runs": rows, "invalid_total_controls": controls,
        "checks": {"source_files_unchanged": unchanged, "problems": problems, "verified": not problems},
        "limits": ["Controlled schedules are chosen witnesses, not a probability estimate or exhaustive schedule search",
                   "Ordinary runs have no controller or observed lock, but still use the same synthetic async store",
                   "The repair covers a single owner on one event loop, not other instances, threads, processes, or external writers",
                   "No live repository, CI, network, throughput, fairness, or product cancellation guarantee was tested",
                   "Timeouts bound cooperative fixture waits; cancellation cleanup can exceed the nominal deadline"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Create this NEW directory and write results.json; existing paths are refused")
    args = parser.parse_args()
    if args.output:
        args.output.mkdir(parents=False, exist_ok=False)
    report = asyncio.run(experiment())
    payload = json.dumps(report, indent=2) + "\n"
    if args.output:
        with (args.output / "results.json").open("x", encoding="utf-8") as stream:
            stream.write(payload)
    else:
        print(payload, end="")
    return 0 if report["checks"]["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
