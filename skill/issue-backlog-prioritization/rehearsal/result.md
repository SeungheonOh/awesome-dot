# Decision from the fictional backlog packet

The [supplied packet](input.md) does **not support a unique highest-importance item that can start**. Q-14 and Q-15 are ready and tied at 12. Ready Q-13 ranges from 6–13, so it could lead, tie or trail them. Q-12 is ready at 2 and would unblock the highest-importance eligible issue, Q-11; that dependency does not raise Q-12's score.

This is a condensed decision artifact from a synthetic rehearsal. Snapshot: 2026-10-01T12:00:00Z. All issues are open. No tracker was read or changed.

## Reconciled comparison

Eleven [source rows](input.md#source-records) describe ten distinct issues. R11 duplicates R3's Q-13 version 7 exactly; both locators are retained and the issue is counted once. X-90 is only an absent prerequisite reference, not an additional scored issue.

The endorsed formula is **3 × impact + 2 × urgency − effort**. These are ordinal points, not durations. Only gate-pass issues are eligible. The table shows failed/unknown-gate arithmetic for transparency, outside the eligible comparison.

| Issue / sources / version | Impact / urgency / effort | Importance | Gate | Readiness and evidence |
| --- | --- | --- | --- | --- |
| Q-11 / R1 / v3 | 5 / 2 / 3 | 16 | pass | Blocked: Q-12 is open |
| Q-12 / R2 / v2 | 1 / 0 / 1 | 2 | pass | Ready: no prerequisites |
| Q-13 / R3, R11 / v7 | 4 / 1 / unknown | 14 − effort = **[6, 13]** | pass | Ready: no prerequisites; uncertain effort affects importance only |
| Q-14 / R4 / v4 | 3 / 3 / 3 | 12 | pass | Ready: no prerequisites |
| Q-15 / R5 / v2 | 4 / 2 / 4 | 12 | pass | Ready: no prerequisites |
| Q-16 / R6 / v1 | 5 / 3 / 1 | 20, excluded | fail | Blocked: fields are outside approved project scope |
| Q-17 / R7 / v5 | 5 / 3 / 2 | 19, eligibility unresolved | unknown | Unknown: source-use decision missing |
| Q-18 / R8 / v2 | 2 / 1 / 1 | 7 | pass | Blocked: requires open Q-19 |
| Q-19 / R9 / v2 | 2 / 0 / 2 | 4 | pass | Blocked: requires open Q-18 |
| Q-20 / R10 / v3 | 3 / 2 / 5 | 8 | pass | Unknown: X-90 record/completion evidence absent |

## Importance and what can start

Known-score eligible tiers are **Q-11 > {Q-14, Q-15} > Q-20 > Q-18 > Q-19 > Q-12**. This is not a total ranking including Q-13. IDs within a tie are display order only; no tie-breaker was authorized.

Because effort is subtracted, its maximum allowed value 8 gives Q-13's minimum score 6, and its minimum value 1 gives the maximum 13. Q-11 definitely outranks Q-13. Q-13 definitely outranks Q-19 and Q-12. Its comparisons with Q-14, Q-15, Q-20 and Q-18 remain unresolved. No midpoint or dependency bonus is used.

For the current gate-passed ready set:

- Q-13 effort **1** would make it the unique highest-importance ready issue, at 13
- Effort **2** would tie Q-13, Q-14 and Q-15 at 12
- Effort **3–8** would leave Q-14 and Q-15 tied for highest importance among ready issues

The dependency cycle is **Q-18 → Q-19 → Q-18**, where an arrow means “requires.” Neither can start and no topological order exists for that component. Independent ready work remains available. Missing X-90 evidence makes Q-20's readiness unknown, rather than proving its prerequisite open or complete.

## Smallest useful next facts

1. Q-13's evidenced effort on the approved 1–8 scale resolves its comparisons. Effort 1 is the decisive case for a unique highest-importance ready issue; other values can leave a tie
2. The recorded source-use decision resolves Q-17's gate. If it passes, Q-17 would be ready at 19 and outrank currently eligible work; its present gate remains unknown
3. A supplied X-90 record with reliable completion-status evidence resolves Q-20's readiness. Outside lookup is not permitted by this packet
4. An owner decision about the Q-18/Q-19 links is needed to resolve the cycle. No link is silently removed

Q-12's open status is already known; completing it and verifying completion would enable Q-11. This is an enabling option, not a uniquely preferred selection, assignment or delivery promise.

[Input](input.md) · [Verification and limits](verification.md)
