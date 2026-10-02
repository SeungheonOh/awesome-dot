# Fictional example: making a cupboard restock checklist

This is an authored exercise. The logs, durations, output snapshots and people described below are fictional. Running its arithmetic checks is not a real workflow experiment and establishes no productivity result for dot or any assistant.

## Supplied request and review boundary

“Use these six existing task records to compare my usual spreadsheet workflow with an assisted draft workflow for a cupboard restock checklist. Tell me what I can conclude about hands-on work, getting an acceptable list back and review burden. Use the acceptance rules below. Include all three assigned pairs and shared setup. Keep it private; don't run any more tasks or order anything.”

Packet header F0 establishes one operator who also reviewed all six drafts; three distinct cupboard inventories per workflow; one operator at a time; no work outside each recorded interval except the setup records S-B and S-A. Each matched pair has six input rows, the same targets and output format. Pair 3 has one unknown count on each side. Pairing was assigned by these characteristics before the runs. Within every pair the operator did the baseline first, then the assisted version. There was no randomized ordering. Different cupboards mean the contents are similar in scope, not identical.

The reporting window is the single fictional session dated 2026-09-15, UTC. Its final cutoff is 12:15 UTC. All three baseline tasks and both accepted assisted tasks ended before then; A3 began at 11:45 UTC and remained unfinished at the cutoff. The local packet is the complete supplied intake for that session: six task attempts and one in-task retry, with no excluded tasks, duplicate exports or inaccessible files. No claim is made about tasks outside the packet.

## Source records

### Inventory and acceptance rules: F1

Quantities are whole purchase units: packs, boxes or bottles as named. Each task must produce all six rows in this fixed order, retaining the source row ID formed as task ID plus item ID (for example A1-soap).

| Item ID | Purchase unit | Target | B1 on hand | A1 on hand | B2 on hand | A2 on hand | B3 on hand | A3 on hand |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| paper | pack | 3 | 1 | 2 | 0 | 1 | 2 | 3 |
| pens | box | 6 | 3 | 2 | 4 | 5 | 6 | 4 |
| tea | box | 2 | 0 | 1 | 1 | 2 | 0 | 1 |
| bags | pack | 4 | 2 | 3 | 4 | 1 | 2 | 0 |
| soap | bottle | 4 | 3 | 3 | 2 | 4 | unknown | unknown |
| pads | pack | 2 | 1 | 0 | 0 | 1 | 2 | 1 |

The user supplied these gates before any run:

- Q1: six distinct rows, one per source item, including rows that need zero restock; correct source IDs and purchase units
- Q2: restock quantity is max(target minus on hand, 0) for every known count
- Q3: an unknown count is shown as “pending count” without an invented restock quantity
- Q4: a draft is complete only after the operator checks Q1–Q3 and marks its exact version accepted; no purchasing or account action is part of the task

### Output snapshots and review events: F2

Each vector below is the complete quantity column in the F1 item order. All present rows have the corresponding source IDs and purchase units; the stored snapshot has no additional rows. “Pending” means the exact text “pending count.” This representation compresses the table without hiding its contents or row coverage.

| Artifact | Quantities | Review record |
| --- | --- | --- |
| B1-v1 | 2, 3, 2, 2, 1, 1 | R-B1: all gates pass; accepted unchanged |
| A1-v1 | 1, 4, 1, 1, 0, 2 | R-A1-initial: Q2 fails for A1-soap; target 4 minus count 3 is 1, not 0 |
| A1-v2 | 1, 4, 1, 1, 1, 2 | R-A1-final: soap corrected to 1; all gates pass; accepted |
| B2-v1 | 3, 2, 1, 0, 2, 2 | R-B2: all gates pass; accepted unchanged |
| A2-v1 | 2, 1, 0, 3, 0, 1 | R-A2: all gates pass; accepted unchanged; review duration not captured |
| B3-v1 | 1, 0, 2, 2, pending, 0 | R-B3: all gates pass; accepted unchanged |
| A3-v1 | 0, 2, 1, 4 | R-A3: Q1 fails; soap and pads rows missing; no accepted version |

E-A3 records one retry within A3 after the failed review. The retry returned no new artifact before a timeout and the cutoff. It remains part of A3 and its recorded effort. No second independent task or eventual completion was recorded. A3's absent soap row does not count as a successful Q3 treatment.

### Recorded time: F3

Units are minutes. In this fictional packet, all numeric time fields are timer measurements except bounds calculated later. F0/F3 establish a complete single-person timeline for each attempt and no overlapping activity. Setup occurred outside the attempt intervals. Operation includes input handling, spreadsheet entry or prompts, artifact handling and the A3 retry. Correction includes making the A1 change and checking the revised output. A recorded 0 means the log affirmatively records no such phase; “?” is missing timing.

| Task | Preparation | Operation | Initial review | Correction/recheck | Known inactive wait | Other interval with activity unclassified | Elapsed endpoint |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| B1 | 2 | 8 | 4 | 0 | 4 | 0 | 18 to acceptance |
| A1 | 2 | 3 | 3 | 4 | 13 | 0 | 25 to acceptance |
| B2 | 2 | 10 | 4 | 0 | 4 | 0 | 20 to acceptance |
| A2 | 2 | 5 | ? | 0 | 9 | 16, includes untimed review and any other pauses | 32 to acceptance |
| B3 | 2 | 9 | 4 | 0 | 3 | 0 | 18 to acceptance |
| A3 | 2 | 4 | 3 | 0 | 21 | 0 | 30 through cutoff; unfinished |

For A2, the 16-minute unclassified interval contains the unknown review duration; it must not be added on top of that review duration. The reviewer completed the check somewhere in this interval. At least 7 active minutes are known. At most all 16 unclassified minutes could have been active, giving a conservative inclusive bound of 7–23 minutes. The lower bound does not mean the review took zero minutes. The complete single-person timeline supports the upper bound; without that evidence, it would not be justified.

S-B records 4 active minutes of reusable baseline setup. S-A records 10 active minutes of reusable assisted setup. Each setup was used for all three attempts in its variant. No prior training time or ongoing maintenance measurement is supplied. Those longer-term costs remain outside this session's observed boundary, not implicitly zero.

## Completed private comparison

The assisted workflow used 2 fewer active minutes in the only pair with exact effort measurements on both accepted results, but that pair took 7 more elapsed minutes to reach acceptance and required a quantity correction. Across the whole session, the baseline produced three accepted lists; the assisted workflow produced two and left one unfinished. Missing A2 review timing and unequal completion prevent a conclusion that assistance reduced the effort needed for equivalent accepted work.

### Outcomes and coverage

| Session outcome | Baseline | Assisted |
| --- | --- | --- |
| Eligible attempted tasks | 3 | 3 |
| First-submission passes | 3 of 3 | 1 of 3, A2 only |
| Accepted by cutoff | 3 of 3 | 2 of 3, A1 and A2 |
| Completed but rejected | 0 | 0 |
| Unfinished at cutoff | 0 | 1, A3 with one in-task retry |
| Corrected accepted tasks | 0 | 1, A1 |
| Exact active effort available | 3 of 3 attempts | 2 of 3 attempts, including unfinished A3 |
| Elapsed to accepted completion available | 3 of 3 attempts | 2 of 3 attempts |

The initial A3 rejection remains in the first-pass accounting; its final task outcome is unfinished, not a second completed-but-rejected task. Both variants used the same gates. A1's changed soap quantity is backed by F1 A1-soap and the v1/v2 review records, not by a post hoc relaxation of Q2.

### Paired times, with the endpoint held constant

Difference is assisted minus baseline. Negative means fewer minutes; positive means more.

| Pair and metric | Baseline | Assisted | Difference | Evidence/coverage |
| --- | ---: | ---: | ---: | --- |
| P1 human effort to acceptance | 14 | 12 | −2, or −14.3% of 14 | Exact; includes A1 correction; excludes shared setup on both sides |
| P2 human effort to acceptance | 16 | 7–23 | −9 to +7 | Bound, not an exact saving; A2 review timing missing |
| P3 human effort to acceptance | 15 | unavailable | unavailable | A3 spent 9 active minutes so far but has no accepted result |
| P1 elapsed to acceptance | 18 | 25 | +7 | Complete pair |
| P2 elapsed to acceptance | 20 | 32 | +12 | Complete pair |
| P3 elapsed to acceptance | 18 | unavailable | unavailable | A3's 30 minutes is elapsed through cutoff, not completion |

There is one exact pair for active effort to accepted completion. It cannot establish a typical active-time reduction. The two complete elapsed pairs have differences of +7 and +12 minutes: mean and median +9.5, observed range +7 to +12. These are descriptive values for the two accepted pairs, not a confidence interval or a forecast. The unfinished third assisted task remains visible in the all-attempt outcome counts.

In P1, baseline active/wait time is 14/4 and assisted active/wait time is 12/13. The sums reproduce the respective elapsed times, 18 and 25. The assisted run's smaller hands-on total coexists with later acceptance; “faster” would hide that distinction.

### Review, setup and spent effort

Baseline review totals 4 + 4 + 4 = 12 active minutes. Assisted review and correction total at least 3 + 4 + 3 = 10 known active minutes, plus A2's unknown review. A3's 3 minutes inspected its failed draft. The bound on A2's unclassified interval puts this review/correction total conservatively between 10 and 26 minutes; it is not an exact comparison of review burden. A1's known correction cost is 4 minutes, already included in its 12 active minutes and not added again.

Session human effort, counting setup and every attempted task:

- Baseline: 4 + 14 + 16 + 15 = 49 active minutes, yielding three accepted lists
- Assisted: 10 + 12 + [7, 23] + 9 = [38, 54] active minutes spent through cutoff, yielding two accepted lists and one unfinished task
- Difference in recorded spent effort: [38, 54] − 49 = [−11, +5] minutes. Either direction is possible within the supported bounds, and the completed output counts differ

These are batch resource accounts, not equal-output productivity ratios. Dividing the assisted total by two successes would include effort on its unfinished third task while implying a different output population from a simple per-task average. Any such ratio would need that definition and would still not establish the effort to complete three accepted lists. No setup cost is spread over imagined future tasks.

### What to do with this result

If the user wants a decision on these records alone, the baseline met the full session's acceptance goal; the assisted workflow has not yet demonstrated the same completion level. The records suggest checking the omitted-row failure and preserving an explicit quantity review. They do not establish what caused the elapsed differences or predict whether future assisted runs would be better.

The smallest missing historical input is A2's review/activity timing within the 16-minute interval. Without a contemporaneous record, retain the bounds; do not ask the user to reconstruct a precise duration from memory. Final A3 evidence would matter only if it already exists within an authorized later window. Extending the cutoff is a new scope choice and cannot rewrite this session's as-of result. No new runs or monitoring were started.

This is three matched task pairs from one fictional operator, with baseline always first and differing source inventories. Learning, order and task-content differences remain possible explanations. The review does not establish a causal benefit, statistical significance, effects for other people or long-term adoption cost.

## Small arithmetic and gate check

This standard-library check recomputes the expected quantities from the raw inventory numbers, confirms the two recorded initial failures and the accepted final snapshots, and checks time accounting. It does not validate a real product or measurement design. Run from this folder by extracting the fenced Python below, as recorded in [verification.md](verification.md).

```python
from statistics import mean, median

targets = [3, 6, 2, 4, 4, 2]
counts = {
    "B1": [1, 3, 0, 2, 3, 1], "A1": [2, 2, 1, 3, 3, 0],
    "B2": [0, 4, 1, 4, 2, 0], "A2": [1, 5, 2, 1, 4, 1],
    "B3": [2, 6, 0, 2, None, 2], "A3": [3, 4, 1, 0, None, 1],
}
initial = {
    "B1": [2, 3, 2, 2, 1, 1], "A1": [1, 4, 1, 1, 0, 2],
    "B2": [3, 2, 1, 0, 2, 2], "A2": [2, 1, 0, 3, 0, 1],
    "B3": [1, 0, 2, 2, None, 0], "A3": [0, 2, 1, 4],
}
expected = {k: [None if v is None else max(t-v, 0)
                for t, v in zip(targets, row)] for k, row in counts.items()}
assert {k for k in initial if initial[k] != expected[k]} == {"A1", "A3"}
accepted = {k: list(v) for k, v in initial.items() if k != "A3"}
accepted["A1"][4] = 1
assert all(v == expected[k] for k, v in accepted.items())
assert sum(k.startswith("B") for k in accepted) == 3
assert sum(k.startswith("A") for k in accepted) == 2
assert sum(initial[k] == expected[k] for k in ("A1", "A2", "A3")) == 1

active = {"B1": 2+8+4, "A1": 2+3+3+4, "B2": 2+10+4,
          "B3": 2+9+4, "A3": 2+4+3}
wait = {"B1": 4, "A1": 13, "B2": 4, "B3": 3, "A3": 21}
elapsed = {"B1": 18, "A1": 25, "B2": 20, "A2": 32, "B3": 18, "A3": 30}
assert all(active[k] + wait[k] == elapsed[k] for k in active)
a2_known, a2_unclassified, a2_wait = 7, 16, 9
assert a2_known + a2_unclassified + a2_wait == elapsed["A2"]
a2_bounds = (a2_known, a2_known + a2_unclassified)
assert a2_bounds == (7, 23)  # No midpoint or missing-value substitution.
assert active["A1"] - active["B1"] == -2
assert round(100 * (-2) / active["B1"], 1) == -14.3
complete_elapsed_pairs = [("B1", "A1"), ("B2", "A2")]
diffs = [elapsed[a] - elapsed[b] for b, a in complete_elapsed_pairs]
assert diffs == [7, 12] and mean(diffs) == median(diffs) == 9.5
baseline_total = 4 + sum(active[k] for k in ("B1", "B2", "B3"))
assisted_bounds = tuple(10 + active["A1"] + t + active["A3"] for t in a2_bounds)
assert baseline_total == 49 and assisted_bounds == (38, 54)
assert tuple(t-baseline_total for t in assisted_bounds) == (-11, 5)
assert (3+4+3, 3+4+3+a2_unclassified) == (10, 26)
print("PASS: quantity gates, correction, attempt counts, timing partitions, paired differences and bounds")
```
