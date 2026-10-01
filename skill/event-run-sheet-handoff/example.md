# Fictional community demonstration run sheet

All names, records and times below are invented. No venue, person or external service was contacted. This is a source-to-handoff illustration.

## Source packet

- **B1, coordinator brief v2**, supplied 2026-11-10 12:00 UTC: demonstration on **2026-11-14, Europe/London**. Access starts 14:00; doors open exactly 15:00; program starts exactly 15:15 and finishes exactly 16:15; handback and departure must finish by 16:45. These are planning inputs, not independently verified reservations. All tasks are non-preemptive; predecessor lags are explicitly zero. The tasks occur in the same working area, with no additional transfer/reset time beyond the listed work. Work may end exactly at an availability end or deadline; a successor may start at its predecessor's finish.
- **B1 duration/assignment annex:** room setup 25 min, Priya; audio check 15 min, Theo/PA; desk setup 15 min, Jo/desk; readiness review 10 min, Priya+Theo+Jo; door briefing 10 min, Priya+Jo/desk; admissions 15 min, Jo/desk; welcome 5 min, Priya/PA; demonstration 40 min, Theo/PA; questions 15 min, Priya+Theo/PA; equipment pack 20 min, Theo+Jo/PA; room restoration 20 min, Priya; handback 10 min, Priya+Theo+Jo. The PA and desk each have capacity one. “Room” is a location, not an additional exclusive resource.
- **B1 dependency annex:** S1 precedes S2 and S3; both precede S4; then S4→O1→O2→P1→P2→P3. P3 releases both C1 and C2; both must finish before C3. S2/S3 and C1/C2 may run in parallel with their listed separate assignments. No task may be dropped or shortened without an approved revision.
- **R1, accepted roster**, supplied 2026-11-11 09:00 UTC: Priya is coordinator and program-change decision owner, Theo audio/demo lead, Jo admissions/equipment lead. Each is available 14:00–16:45 and can do only one listed task at a time. No substitute or alternate venue has been approved. The venue's handback recipient and contact method are still unknown; Priya owns resolving them.
- **G1, acceptance notes**, supplied with B1: readiness review requires room/desk completion evidence and Theo's audio-check report; it includes reviewing audio readiness rather than assuming the report was independently verified. Opening requires Priya's readiness approval and completed door briefing. Handback requires a restoration/equipment record and acknowledgement from the venue recipient. If audio is not acceptable at review, Priya must decide by 14:50 whether to seek a revised program/opening plan. No fallback program or duration is supplied.
- **L1, progress record**, as of 2026-11-14 14:40 UTC: all three roles checked in and accepted the listed tasks. Room setup finished at 14:25; Priya checked the layout against B1 at 14:25. Theo reported audio check complete at 14:40; no independent audio acceptance evidence is present. Jo finished desk setup at 14:40; Priya checked its G1 checklist at 14:40. No later work is reported started. This is a fictional evidence record, not a live observation.

Every displayed time is on 2026-11-14 in Europe/London, UTC+00:00. Comparisons use dated instants. Task occupancy is [start, finish); equality at predecessor/availability/deadline boundaries is allowed by B1. No allowance is added beyond the supplied durations and zero lags.

## Fixed anchors

| Anchor | Constraint | Source |
|---|---|---|
| Access | No task starts before 14:00 | B1 |
| Doors | O2 starts exactly 15:00 | B1 |
| Program start | P1 starts exactly 15:15 | B1 |
| Program end | P3 finishes exactly 16:15 | B1 |
| Handback/departure | C3 finishes no later than 16:45 | B1 |

## Run sheet, revision 1, as of 14:40

The proposed timing satisfies the modeled anchors, dependencies and known capacity-one availability. Operational handback remains conditional because the venue recipient is unknown. The final chain has no modeled slack; the plan does not guarantee live performance.

All durations and assignments below come from B1, availability from R1, gates from G1. Times are planned except where L1 supplies actual completion evidence. All rows retain “approved for planning, B1”; none is a calendar or venue change.

| ID / phase | Task | Planned interval | Min | Finish-to-start predecessors | Roles / exclusive resource | Readiness at 14:40 | Execution evidence |
|---|---|---|---:|---|---|---|---|
| S1 / setup | Room setup | 14:00–14:25 | 25 | — | Priya / — | Not applicable after completion | Verified complete 14:25; Priya, L1 |
| S2 / setup | Audio check | 14:25–14:40 | 15 | S1 | Theo / PA | Not applicable after reported completion | Reported complete 14:40; Theo, L1; independent acceptance pending |
| S3 / setup | Desk setup | 14:25–14:40 | 15 | S1 | Jo / desk | Not applicable after completion | Verified complete 14:40; Priya, L1 |
| S4 / setup | Readiness review | 14:40–14:50 | 10 | S2, S3 | Priya, Theo, Jo / — | Ready for review under G1 and L1 | Not started; no completion implied |
| O1 / opening | Door briefing | 14:50–15:00 | 10 | S4 | Priya, Jo / desk | Blocked on S4 approval | Not started |
| O2 / opening | Admissions | 15:00–15:15 | 15 | O1 | Jo / desk | Blocked on O1 and readiness approval | Not started |
| P1 / program | Welcome | 15:15–15:20 | 5 | O2 | Priya / PA | Blocked on O2 | Not started |
| P2 / program | Demonstration | 15:20–16:00 | 40 | P1 | Theo / PA | Blocked on P1 | Not started |
| P3 / program | Questions | 16:00–16:15 | 15 | P2 | Priya, Theo / PA | Blocked on P2 | Not started |
| C1 / close | Equipment pack | 16:15–16:35 | 20 | P3 | Theo, Jo / PA | Blocked on P3 | Not started |
| C2 / close | Room restoration | 16:15–16:35 | 20 | P3 | Priya / — | Blocked on P3 | Not started |
| C3 / close | Handback/departure | 16:35–16:45 | 10 | C1, C2 | Priya, Theo, Jo / — | Blocked on C1/C2 and unknown recipient | Not started |

## Handoffs and decisions

| Handoff | Sender → recipient | Acceptance / evidence | Decision owner |
|---|---|---|---|
| S4, 14:40–14:50 | Theo and Jo → Priya | Review audio report and room/desk evidence; Priya records a readiness decision under G1 | Priya |
| O1, 14:50–15:00 | Priya → Jo | Completed door briefing and recorded S4 approval before O2 | Priya |
| P1→P2, 15:20 boundary | Priya → Theo | Welcome completes before demonstration starts; no extra transfer duration supplied under B1 | Priya |
| C3, 16:35–16:45 | Priya, with Theo/Jo records → venue recipient **unknown** | Restoration/equipment record and recipient acknowledgement under G1 | Priya |

Unknown recipient availability is outside the completed capacity checks. The 10-minute C3 slot is a proposal until that recipient can accept the handoff; it is not a confirmed appointment.

## Contingencies and unresolved requirements

- **Audio review fails:** S4 cannot release O1/O2. Theo supplies the issue; Priya decides by 14:50 whether to seek an approved revised plan. No fallback duration, changed doors time or cancellation is authorized. Keep the current anchors and unresolved decision visible
- **Either C1 or C2 finishes after 16:35:** C3 cannot both retain its supplied 10 minutes and meet 16:45. Priya must decide what change to seek; do not promise recovery, shorten work or extend hire
- **Venue recipient:** Priya must identify the recipient, confirm their handback availability and resolve acknowledgement evidence before treating C3 as ready. No contact has been initiated by this workflow
- **Actual progress:** The clock reaching 14:50 will not complete S4. A new report or readiness decision is required. Future actuals remain blank

## Checked alternatives and limits

1. **Unknown duration:** Change S2's supplied duration to unknown while leaving its nominal interval unchanged. The checker returns an unresolved input; the 15-minute interval is not evidence of a supplied duration
2. **Dependency cycle:** Add C3 as S1's predecessor. The checker rejects the cycle S1→…→C3→S1 before it evaluates timing
3. **Shared-role conflict:** Add Jo to S2 while retaining Jo on S3. Both require Jo from 14:25 to 14:40: 15 minutes of capacity-one overlap. The checker rejects that candidate without suggesting that the whole event is impossible
4. **Boundary equality:** S4→O1, O1→O2 and the final availability/deadline equality pass because B1 explicitly allows them. Adding a separately supplied one-minute S4→O1 lag makes the proposed O1 start fail
5. **A valid impossibility bound for one changed model:** If R1 instead says Jo cannot perform C1 before 16:25, C1 cannot finish before 16:45 (20 supplied minutes). Mandatory successor C3 cannot finish before 16:55 (10 supplied minutes), later than the 16:45 deadline. Under those non-preemptive tasks, unchanged assignment, mandatory dependency and no permitted substitution, every schedule violates the deadline by at least 10 minutes. This is a dependency/release-time lower bound, not a greedy-search claim

The fixture validator checks this exact proposed schedule. It has no schedule-search or optimization routine and does not evaluate unmodeled staffing, venue rules, safety, actual attendance, variable durations or live conditions. A mathematically consistent plan remains conditional on its inputs and operational gates.

## Executed check

Run from the repository root:

```bash
python3 skill/event-run-sheet-handoff/check_example.py
```

Observed result:

```text
PASS: baseline intervals, anchors, dependencies and capacity
PASS: unknown duration remains unresolved
PASS: dependency cycle rejected
PASS: shared-role overlap rejected (15 minutes)
PASS: explicit boundary equality and lag violation
PASS: exclusive-resource overlap rejected
PASS: availability violation rejected
PASS: changed release-time model has a 16:55 lower bound
PASS: example rows read back and agree with fixture
PASS: unknown documented run-sheet task rejected
10 checks passed; no schedule optimization or live-event assurance
```

The readback check parses the run-sheet table rather than filtering for known task IDs. An extra conflicting task row is rejected, even if every expected row is still present. This checks the printed fixture, not an arbitrary document or live run sheet.
