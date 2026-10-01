# Three fictional errands with different cutoffs

Everything below is supplied fiction: points, service rules, travel times and source timestamps. There are no addresses or real businesses. This is not current traffic, live opening-hour evidence or a recommendation to travel.

## Request and evidence

```text
Plan these three selected errands for 2026-10-03 in Etc/UTC (UTC+00:00).
Leave point S at 09:00 and reach the different end point E by 11:15.
A and B are required. Include optional C if all hard constraints still pass.
Use this supplied, constant travel-time matrix and add my five-minute
planning buffer to each traveled leg, including the final leg to E.
Waiting is allowed at all three stops, including before opening; there is
a permitted waiting area. Do not change appointments or start navigation.
```

Supplied fictional evidence, all applicable only to this sample date:

| Reference | Supplied/checked timestamp | Facts supplied |
| --- | --- | --- |
| F1: user trip constraints | 2026-10-01 18:00 UTC | Fixed 09:00 departure, E by 11:15 inclusive, mode fixed for the matrix, priorities above, five-minute leg buffers and waiting permission |
| F2: A service card | 2026-10-01 18:05 UTC | Required parcel hand-in; open 09:00–10:05; entire 15-minute service must finish by 10:05 inclusive |
| F3: B appointment card | 2026-10-01 18:06 UTC | Required repair collection visit; premises open 09:00–10:45; arrive by 10:05 inclusive; fixed service start 10:10; service lasts 20 minutes and must finish by 10:45 |
| F4: C pickup card | 2026-10-01 18:07 UTC | Optional stationery pickup; open 09:40–11:00; arrive by 10:45 inclusive; service lasts 10 minutes and must finish by 11:00 |
| F5: travel matrix | 2026-10-01 18:10 UTC | Directional minutes for the sample mode, constant throughout 09:00–12:00; includes access walking, excludes the user's five-minute planning buffer |

These timestamps are fixture values, not a claim that an official site was visited. All service durations are supplied by F2–F4. The appointment's early-arrival rule is a cutoff, not a separate five-minute check-in task. No additional queue or check-in duration is specified. A real visit would need any such material gap resolved rather than silently assigning zero effort.

Complete directional matrix, in minutes; read each row as the origin and each column as the destination. S and E are different points. Reverse directions are deliberately unequal.

| From \ To | S | A | B | C | E |
| --- | ---: | ---: | ---: | ---: | ---: |
| S | 0 | 12 | 20 | 15 | 25 |
| A | 14 | 0 | 18 | 20 | 16 |
| B | 24 | 28 | 0 | 8 | 18 |
| C | 17 | 16 | 15 | 0 | 14 |
| E | 22 | 19 | 21 | 16 | 0 |

## Result

Feasible under the supplied fiction: S → A → B → C → E, arriving at E at 11:12. It includes both required stops and optional C. The tightest moving cutoff is C's arrival deadline, with only two minutes of slack after the included buffers. This is fragile to additional delay, not a guaranteed arrival.

All times below are 2026-10-03, Etc/UTC (UTC+00:00).

| Stop | Status | Incoming travel + buffer | Arrival | Wait | Service | Relevant remaining slack |
| --- | --- | --- | --- | --- | --- | --- |
| A | Required | 12 + 5 min | 09:17 | 0 min | 09:17–09:32 | Completion cutoff 10:05: 33 min |
| B | Required | 18 + 5 min | 09:55 | 15 min | 10:10–10:30 | Arrival cutoff 10:05: 10 min; exact start met; closing: 15 min |
| C | Optional, included | 8 + 5 min | 10:43 | 0 min | 10:43–10:53 | Arrival cutoff 10:45: 2 min; closing: 7 min |
| E | Required endpoint | 14 + 5 min | 11:12 | — | — | End deadline 11:15: 3 min |

B's 15-minute wait is real calculated waiting before the fixed appointment, separate from the five-minute allowance on the incoming leg. C may finish after its 10:45 arrival cutoff because its separate completion limit is 11:00.

Required-only alternative: S → A → B → E reaches E at 10:53. Including C adds 19 minutes to end arrival and leaves only three minutes before the user's end deadline. The stated selection rule prefers including C, so the all-stop option is selected, with this tradeoff visible.

There are two required-only permutations and six all-stop permutations. Of those eight, only A–B and A–B–C pass this fixed-departure model. This establishes the result only for the supplied complete, constant matrix and stated constraints. It does not establish a globally optimal real-world route or account for changing traffic, route alternatives, queues or unavailable service.

## Explain rejected orders

- **B → A → C:** Reach B at 09:25, wait until 10:10 and finish at 10:30. B→A takes 28 minutes plus the five-minute buffer, so arrive at A at 11:03 and finish at 11:18. A's 10:05 completion cutoff is missed by 73 minutes. Arriving at B earlier does not move its fixed appointment
- **A → C → B:** Finish A at 09:32, reach C at 09:57 and finish C at 10:07. C→B takes 15 minutes plus five buffer minutes, giving 10:27 arrival, 22 minutes after B's 10:05 arrival cutoff

Do not repair these orders by making A optional, changing B's appointment or using the shorter B→C value for C→B.

## Boundary and incomplete-evidence cases

1. Add two minutes only to B→C: C arrival becomes 10:45, exactly its inclusive arrival cutoff; C finishes 10:55 and E arrival is 11:14, so the fixture still passes. Add three minutes instead: C arrival is 10:46, so reject C even though E would still be reached at 11:15. The end deadline alone is not a sufficient test
2. Replace C's opening time with unknown: show A–B–E as feasible under the remaining fixture evidence, with C unresolved pending its applicable hours. Do not treat unknown hours as an all-day opening
3. Mark required A closed: no complete plan containing both required stops is feasible on that date. Ask whether the user wants to change the day or explicitly change the required-stop set; do not silently produce B–C as a complete plan
4. Remove A→B travel: the proposed A–B–C plan becomes unresolved on that leg even though B→A exists. Another independently supported order may still be checked
5. Disallow waiting: the displayed 09:00-departure timing fails at B because it needs 15 minutes of waiting. The checker does not search later departure or earlier-point holds. A real task should ask whether those are allowed and recompute if authorized, rather than declaring every possible timing impossible
6. Remove A's service duration: leave A-dependent plans unresolved. Do not replace it with a guessed duration

## Reproduce the check

From the repository root, run:

```bash
python3 skill/errand-window-plan/check_example.py
```

The checker uses only Python's standard library and its embedded fictional data. It neither reads source records nor writes files. The observed output is:

```text
PASS: complete matrix; 8 orders; feasible AB and ABC; cutoff, waiting, closure and unknown checks
A: arrive 09:17, wait 0m, service 09:17-09:32
B: arrive 09:55, wait 15m, service 10:10-10:30
C: arrive 10:43, wait 0m, service 10:43-10:53
E: arrive 11:12; required-only E: 10:53
Rejected BAC: A finish 11:18 > 10:05
```

Observed on 2026-10-01 UTC using Python 3.12.14 on Linux, with exit status 0. The check's scope is one same-zone date, constant travel/service durations, fixed departure, permitted waiting, one optional stop and the listed boundary/gap variants. It does not validate a live routing provider, daylight-saving conversion, split hours, transit schedules or continuous departure-time optimization.

Source records unchanged. No addresses disclosed, navigation started, items bought, appointments changed or bookings submitted. For a real errand request, current applicable official hours and authorized time-specific routing evidence must replace this fixture.
