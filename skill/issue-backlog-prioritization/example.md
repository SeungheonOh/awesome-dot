# Fictional backlog fixture

All records and criteria below are invented for a local test. No tracker, people or external service is involved.

## Given input

The user supplies this rubric: impact, urgency and reach are integers from 1 to 5, larger is more important. Importance = 3 × impact + 2 × urgency + reach. Preserve exact ties. All six records pass the supplied scope gate. An item can start only after all explicit prerequisites are complete. None is complete. The user authorizes a private comparison only.

| ID | Issue | Impact | Urgency | Reach | Requires |
|---|---|---:|---:|---:|---|
| BK-11 | Preserve labels in export | 5 | 4 | 3 | None |
| BK-12 | Correct stale preview | 4 | 3 | 3 | BK-15 |
| BK-13 | Add high-contrast controls | 4 | Unknown | 4 | None |
| BK-14 | Improve help search | 3 | 3 | 4 | None |
| BK-15 | Migrate preview cache | 2 | 2 | 2 | None |
| BK-16 | Improve empty-state guidance | 3 | 3 | 4 | None |

The table is the complete synthetic evidence source. Urgency for BK-13 has not been assessed; its allowed range comes from the user's scale, not an estimate.

## Checked expected output

- BK-11: 15 + 8 + 3 = 26; ready
- BK-12: 12 + 6 + 3 = 21; blocked by incomplete BK-15
- BK-13: 12 + [2, 10] + 4 = [18, 26]; ready by dependency checks, importance unresolved
- BK-14 and BK-16: 9 + 6 + 4 = 19 each; ready; equal tier
- BK-15: 6 + 4 + 2 = 12; ready

Known-score importance order: BK-11 > BK-12 > {BK-14, BK-16} > BK-15. This is not a total order including BK-13. BK-13 always outranks BK-15, may fall above or below the 19-point tier or BK-12, and may tie but cannot exceed BK-11. Do not call BK-11 uniquely first until that possible tie is resolved.

Known-score ready order: BK-11 > {BK-14, BK-16} > BK-15, with BK-13 unplaced within [18, 26]. BK-12 keeps its 21-point importance while blocked. Completing BK-15 would unblock BK-12; that does not change BK-15's score to 21 or create a promise to start it.

Decision-changing question: what is BK-13's evidenced urgency on the agreed scale? Tracker updates: none authorized, none performed.

## Additional edge checks

- If BK-15 also requires BK-12, report BK-12 → BK-15 → BK-12 as a cycle. Both are blocked; unaffected items remain evaluable
- If BK-11 requires an unavailable BK-99, mark BK-11's readiness unknown. Do not infer completion or delete the dependency
- Reversing the input row order must not change scores or equal-score tiers

## Reproduce the check

From this directory: `python3 check_example.py`

Observed in the repository's Linux environment with Python 3.12.14: the command returned exit status 0 and printed the expected score ranges, tied tiers, readiness and cycle path, followed by `PASS: arithmetic, bounds, partial order, ties, dependencies, cycle and missing reference`.

The script uses only this fixed fictional dataset and the Python standard library. It verifies arithmetic and dependency handling; it does not validate live evidence, connector permissions, remote concurrency or tracker readback.
