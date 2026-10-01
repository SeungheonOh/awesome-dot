# Fictional example: two questions in one conversation

This is an offline decision exercise. No account, conversation, schedule or notification was created or read. The source extracts and observed states are fictional. The Python check tests the explicit rules below; it does not understand arbitrary message text or prove that a scheduling service retains state.

## Request and evidence boundary

**U1:** Watch conversation `room-question-a` after outgoing message `request-a`, sent 2026-10-02 at 08:00 UTC. A sufficient reply must confirm both that the room holds at least 18 people and that setup may begin at 08:30 on the requested Thursday. Answers can accumulate across replies from the venue in this conversation. An automated receipt or another conversation does not count. A conflicting answer must be resolved before treating that requirement as confirmed.

Check at 09:00, 10:00, 11:00, 12:00 and 13:00 UTC on that date, then stop. Notify the user privately when a question remains open, with at least two elapsed hours between unanswered-question nudges. A changed partial answer does not bypass that interval. Report a newly encountered source-read failure once per unresolved failure episode; count that notice toward the same maximum of four total notices. A read-failure notice does not reset the nudge interval. Stop on a sufficient answer, four notices, or the final check. Do not contact the venue. No reply-arrival notification was requested.

The actual implementation must verify that the chosen service can support this bounded state before promising the watch. If it cannot, offer the simpler supported arrangement. This example does not establish that capability.

## Supplied conversation observations

Each successful snapshot below is complete for the named conversation from `request-a` through its check time. A source failure supplies no current snapshot; it must not be replaced by an empty message list.

| Observation | Time (UTC) | Source evidence |
|---|---|---|
| O1 | 09:00 | No replies after `request-a` |
| O2 | 10:00 | V1, 09:20: automatic receipt, “Your question has reached our team.” V9, 09:40, is in a different conversation and says “08:30 setup is fine” |
| O3 | 11:00 | V1 plus V2, 10:35, venue reply in `room-question-a`: “The room capacity is 18 people.” No setup answer |
| O4 | 12:00 | Read failed. No current messages or current unanswered status can be established |
| O5 | 13:00 | Complete snapshot has V1, V2 and V3, 12:35, venue reply in `room-question-a`: “For the Thursday in your request, you may begin setup at 08:30.” No conflicting answer |

V9 is available only as a deliberate out-of-scope distractor in the fixture. A real watch should read the selected thread rather than search unrelated conversations for a convenient answer. Keep only the minimum answer evidence in private watch state.

## Resulting state and private notices

| Check | What is established | Notice and next state |
|---|---|---|
| 09:00 | Both requirements open | Notice 1: “The venue hasn't answered the capacity or setup-time questions yet. Review your room request before making plans.” Continue |
| 10:00 | Receipt is automatic; other-thread reply cannot satisfy this request | No notice: the two-hour nudge interval has not elapsed. Both requirements remain open |
| 11:00 | Capacity confirmed by V2; setup still open | Notice 2: “The venue confirms capacity for 18 people. Setup access at 08:30 is still unanswered.” Continue |
| 12:00 | Current source state unknown; last successful evidence was O3 | Notice 3: “I couldn't check the venue conversation. The last successful check confirmed capacity only; I can't tell whether setup has since been answered.” Continue to the final scheduled check |
| 13:00 | V2 and V3 jointly satisfy both requirements | Stop with reason `answered`; no fourth notice and no message to the venue |

The last notice count is three. Two are unanswered-question nudges; one is a source-access diagnostic. The 12:00 failure does not erase V2, but neither does V2 prove what the thread contains at 12:00. The 13:00 answer and final boundary coincide; the completed read supports the stronger closure reason `answered`. A failed final read would instead close at the time boundary with the answer status unknown.

### Implementation record

Keep the logical identity `(conversation, outgoing message, reply criteria)` separate from notification state. Repeating setup should recover that same watch, not reset its count or last-nudge time. Useful state is: next check, last successful observation time, confirmed/unresolved criteria with evidence, failure-episode status, last nudge time, total notices, and stopped/reason. A saved record is setup evidence; actual source reads, delivered notices and final cancellation each need their own service evidence.

## Reproducible decision check

The message-to-criterion annotations in this code are explicit interpretations of V1–V3, not an automatic language classifier. For real messages, inspect the actual wording and retain a short source reference. The test supplies no sending function.

```python
from copy import deepcopy
from datetime import datetime, timedelta, timezone

UTC = timezone.utc

def at(hour, minute=0):
    return datetime(2026, 10, 2, hour, minute, tzinfo=UTC)

THREAD, REQUEST = "room-question-a", "request-a"
CRITERIA = frozenset({"capacity-at-least-18", "setup-0830"})
START, END, SENT = at(9), at(13), at(8)
INTERVAL, MAX_NOTICES = timedelta(hours=2), 4

def message(mid, hour, minute, claims=(), *, thread=THREAD, automatic=False):
    return {"id": mid, "thread": thread, "at": at(hour, minute),
            "automatic": automatic, "claims": dict(claims)}

ack = message("V1", 9, 20, automatic=True)
capacity = message("V2", 10, 35, [("capacity-at-least-18", True)])
setup = message("V3", 12, 35, [("setup-0830", True)])
other = message("V9", 9, 40, [("setup-0830", True)], thread="other-thread")

def classify(snapshot, checked_at):
    evidence = {criterion: [] for criterion in CRITERIA}
    for row in snapshot:
        if (row["thread"] != THREAD or row["automatic"]
                or not SENT < row["at"] <= checked_at):
            continue
        for criterion, confirmed in row["claims"].items():
            if criterion in evidence:
                evidence[criterion].append((row["id"], confirmed))
    # A conflict remains open. Do not silently let a later statement erase it.
    satisfied = {criterion for criterion, claims in evidence.items()
                 if claims and all(value is True for _, value in claims)}
    return satisfied, evidence

def initial_state():
    return {"notices": 0, "last_nudge": None, "last_success": None,
            "satisfied": set(), "evidence": {}, "failure_episode": False,
            "stopped": False, "reason": None}

def check(state, checked_at, snapshot):
    """None means source failure; [] means a successful complete empty snapshot."""
    if state["stopped"]:
        return "stopped"
    if state["notices"] >= MAX_NOTICES:
        state.update(stopped=True, reason="notice-limit")
        return "stopped"
    if checked_at < START:
        return "before-start"
    if checked_at > END:
        state.update(stopped=True, reason="time-boundary")
        return "stopped"
    action = "silent"
    if snapshot is None:
        if not state["failure_episode"]:
            action = "source-failure-notice"
            state["notices"] += 1
        state["failure_episode"] = True
        # Do not replace last successful evidence with an invented empty thread.
    else:
        satisfied, evidence = classify(snapshot, checked_at)
        state.update(last_success=checked_at, satisfied=satisfied,
                     evidence=evidence, failure_episode=False)
        if satisfied == CRITERIA:
            state.update(stopped=True, reason="answered")
            return "answered-without-notice"
        if (state["last_nudge"] is None
                or checked_at - state["last_nudge"] >= INTERVAL):
            action = "unanswered-notice"
            state["notices"] += 1
            state["last_nudge"] = checked_at
    if state["notices"] >= MAX_NOTICES:
        state.update(stopped=True, reason="notice-limit")
    elif checked_at == END:
        state.update(stopped=True, reason="time-boundary")
    return action

snapshots = [[], [ack, other], [ack, capacity], None, [ack, capacity, setup]]
raw_before = deepcopy(snapshots)
state = initial_state()
actions = []
for hour, snapshot in zip(range(9, 14), snapshots):
    previous = deepcopy(state)
    actions.append(check(state, at(hour), snapshot))
    if hour == 12:
        assert state["last_success"] == at(11)
        assert state["satisfied"] == {"capacity-at-least-18"}
        assert state["evidence"] == previous["evidence"]
        assert state["last_nudge"] == at(11)
assert actions == ["unanswered-notice", "silent", "unanswered-notice",
                   "source-failure-notice", "answered-without-notice"]
assert state["notices"] == 3 and state["reason"] == "answered"
assert snapshots == raw_before
assert check(state, at(13), []) == "stopped"  # A retry cannot reopen the watch.
assert classify([other], at(10))[0] == set()
assert classify([ack], at(10))[0] == set()
assert classify([capacity, setup], at(13))[0] == CRITERIA
assert classify([capacity, setup], at(11))[0] == {"capacity-at-least-18"}
conflict = message("V4", 12, 40, [("setup-0830", False)])
assert classify([capacity, setup, conflict], at(13))[0] == {"capacity-at-least-18"}

# Repeated failures produce one diagnostic in the same unresolved episode.
failure = initial_state()
assert check(failure, at(9), None) == "source-failure-notice"
assert check(failure, at(10), None) == "silent"
assert failure["notices"] == 1 and failure["last_success"] is None
assert check(failure, at(11), []) == "unanswered-notice"  # Successful read resets episode.
assert check(failure, at(12), None) == "source-failure-notice"
assert check(failure, at(13), None) == "silent"
assert failure["reason"] == "time-boundary" and failure["notices"] == 3

# A recovered existing watch retains its count and cannot exceed the limit.
limited = initial_state()
limited["notices"] = 3
assert check(limited, at(9), []) == "unanswered-notice"
assert limited["notices"] == 4 and limited["reason"] == "notice-limit"
assert check(limited, at(10), [capacity]) == "stopped"
assert limited["notices"] == 4
recovered = initial_state()
recovered["notices"] = 4  # Count was saved even if the stopped flag was not.
assert check(recovered, at(9), None) == "stopped"
assert recovered["notices"] == 4 and recovered["reason"] == "notice-limit"
print("PASS: partial answers accumulate; unrelated/automated replies excluded;")
print("      failures stay unknown; notice spacing, limits and closure preserved")
```

Run the block from the repository root with Python 3:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/awaiting-reply-user-followup/EXAMPLE.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'reply-followup-example', 'exec'))
PY
```

Observed locally on 2026-10-01 with Python 3.12.14: the exact block passed. Its scope is fictional classification, timestamps, notice decisions, counters and state preservation. Scheduling, durable persistence, source completeness, actual cancellation and delivery are not exercised.
