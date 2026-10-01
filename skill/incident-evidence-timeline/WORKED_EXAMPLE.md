# Cedar: a Change, Late Logs and an Incomplete Impact Window

This packet is entirely fictional. Its purpose is to demonstrate evidence reconstruction, including an answer that remains uncertain. The [raw packet](references/fictional-evidence.json) contains all supplied records, source revisions, query descriptions and clock contracts. No external source was queried.

## Contents

- [Scope and source coverage](#scope-and-source-coverage)
- [Reconstructed timeline](#reconstructed-timeline)
- [Impact and actions](#impact-and-actions)
- [Hypotheses and missing evidence](#hypotheses-and-missing-evidence)
- [Executed checks](#executed-checks)

## Scope and source coverage

Question: what can be established about errors in the fictional Cedar preview API, west, across pod-a and pod-b, during `[2026-05-14T13:00:00Z, 2026-05-14T13:04:00Z)`?

The available evidence was captured at `2026-05-14T13:06:00Z`. Revisions below identify the supplied fictional exports. They are not claims of live source authenticity.

| Source and revision | Included evidence | Coverage and limits |
| --- | --- | --- |
| [CHG / changes-r3](references/fictional-evidence.json), `sources.CHG` | One change record, C1; all query pages returned | Full requested event-time window and both-pod query; journal result is not independent runtime verification |
| [LOG / logs-r2](references/fictional-evidence.json), `sources.LOG` | L1, L1-copy, L2; all pod-a query pages returned | Documented window coverage for pod-a; pod-b unavailable. Raw-clock filter includes `[13:00:03Z,13:04:05Z)` buffer under the supplied +3 to +5 second clock bound |
| [MET / metrics-r5](references/fictional-evidence.json), `sources.MET` | Three one-minute rows: M1, M3, M4; all export pages returned | Both pods; 180 of 240 seconds have metric rows. `[13:01,13:02)` missing; M3 denominator missing |
| [NOTE / notes-r1](references/fictional-evidence.json), `sources.NOTE` | One incident-note row, N1 | Original event time has no offset; clock calibration and event-time coverage unknown |
| [TRACE / unavailable](references/fictional-evidence.json), `sources.TRACE` | None | No trace export supplied or read; no revision or capture exists |

Four of five requested sources have supplied data. This is source availability, not an evidence-quality score. Three of four expected metric bins have rows, while only two have usable denominators. Pod-a is one of two named pods, but no 50% traffic-coverage claim follows. Complete pagination does not establish that instrumentation captured every relevant event.

### Time and identity rules supplied with the packet

```text
All dates below are 2026-05-14.
All displayed normalized and ingestion times below are UTC (+00:00).

Clock error = recorded event clock - actual UTC clock.
CHG and MET: [0, 0] seconds, explicitly supplied by this synthetic packet.
LOG: [3, 5] seconds, valid for pod-a event times in the requested window.
NOTE: event clock error unknown; its event timezone offset is also missing.
Additional timestamp representation uncertainty: zero for this fixture.
Ingestion timestamps use a separate exact synthetic UTC receipt clock.

LOG identity namespace: fictional app log export / cedar/west/pod-a/boot-7.
L1 and L1-copy share event ID error-101 and the same event payload.
L2 has event ID error-102 despite identical message text.
```

Those clock assumptions belong to this fixture. A real source needs calibration evidence and precision handling; the example does not establish that real clocks are exact.

## Reconstructed timeline

Summary: the first supplied metric bin records a 6% 5xx rate among completed west HTTP attempts. A change journal entry and the first distinct pod-a error overlap in possible event time, so their order is unresolved. Missing telemetry and a later absent denominator prevent an overall incident rate, exact onset, full-recovery claim or supported root cause.

Event bounds in square brackets are closed possible-time intervals. Metric windows are half-open aggregation intervals. Display position is only for readability; the partial order below defines what can actually be established. Original timestamps and receipts are from the linked raw rows.

| Evidence | Original event time or window | Possible UTC time or metric window | Ingestion UTC | Observation and source |
| --- | --- | --- | --- | --- |
| M1 | `[13:00:00Z,13:01:00Z)` | `[13:00:00,13:01:00)` | 13:01:10 | 12 5xx / 200 completed attempts; [MET / metrics-r5 / M1](references/fictional-evidence.json), `metrics[row=M1]` |
| L1 plus L1-copy | `13:00:34+00:00` | `[13:00:29,13:00:31]` | L1: 13:01:40; copy: 13:01:41 | One distinct `error-101`: “Render queue deadline exceeded”; [LOG / logs-r2 / L1, L1-copy](references/fictional-evidence.json), `events[row=L1 or L1-copy]` |
| C1 | `09:00:30-04:00` | `[13:00:30,13:00:30]` | 13:00:31 | Journal records renderer revision c17 applied to pod-a; [CHG / changes-r3 / C1](references/fictional-evidence.json), `events[row=C1]` |
| L2 | `13:00:39+00:00` | `[13:00:34,13:00:36]` | 13:00:40 | Distinct `error-102` with the same message; [LOG / logs-r2 / L2](references/fictional-evidence.json), `events[row=L2]` |
| Missing metric bin | No row | `[13:01:00,13:02:00)` | Unknown | No zero-error or continuity inference; [MET / metrics-r5 manifest](references/fictional-evidence.json), `sources.MET.coverage` |
| M3 | `[13:02:00Z,13:03:00Z)` | `[13:02:00,13:03:00)` | 13:03:10 | Three 5xx; attempts count unavailable; [MET / metrics-r5 / M3](references/fictional-evidence.json), `metrics[row=M3]` |
| M4 | `[13:03:00Z,13:04:00Z)` | `[13:03:00,13:04:00)` | 13:04:10 | Zero 5xx / 180 completed attempts; [MET / metrics-r5 / M4](references/fictional-evidence.json), `metrics[row=M4]` |

Unplaced evidence: [NOTE / notes-r1 / N1](references/fictional-evidence.json), `events[row=N1]`, records `2026-05-14T09:02:15` without an offset: “Rollback prepared; awaiting decision.” Its receipt is `2026-05-14T13:02:30Z`. Neither the event's absolute position nor a completed rollback follows from that receipt. Keep the note in the packet without inserting it into a claimed event-time sequence.

### Supported partial order

```text
C1 versus L1: unresolved; 13:00:30 lies inside L1's [13:00:29,13:00:31].
C1 before L2: established by 13:00:30 < 13:00:34.
L1 before L2: established by 13:00:31 < 13:00:34.
N1 relative to C1, L1 or L2: absolute order unknown.

Receipt order for the two distinct errors is L2, then L1.
That does not reverse their established event order.
M1 spans C1 and both log events; it does not locate its 12 errors within the bin.
```

The intervals use the supplied [source clock bounds](references/fictional-evidence.json), `sources.*.skew_seconds`, and event timestamps. For L1, `13:00:34 - [3,5] seconds` becomes `[13:00:29,13:00:31]`. The corresponding lower/upper subtraction is deliberate. There is no sequence or trace evidence in the packet that resolves C1 versus L1.

Identity reconciliation: five event/note rows become four unique identities after collapsing one confirmed duplicate. The three log rows represent two distinct log events. Preserve both L1 receipt times and row locators. These counts do not establish the number of failed HTTP attempts or affected people.

## Impact and actions

The [MET contract](references/fictional-evidence.json), `sources.MET.metric_contract`, defines completed HTTP attempts across both west pods, counts retries separately, declares no sampling or resets, and makes 5xx a subset of the same-window attempts denominator.

| Window, UTC | Calculation | Supported result |
| --- | --- | --- |
| `[13:00,13:01)` | M1: `12 / 200 × 100` | 6% of measured completed attempts returned 5xx |
| `[13:01,13:02)` | No metric row | Numerator, denominator and rate unavailable |
| `[13:02,13:03)` | M3: `3 / unknown` | Three recorded 5xx; rate unavailable |
| `[13:03,13:04)` | M4: `0 / 180 × 100` | 0% in this bin; no proof of full service recovery |

No full-window error rate or unique affected-user count is available. The available metrics show 5xx in the first observed bin and again in M3; they do not establish exactly when impact began or that it was continuous. A zero 5xx rate does not assess latency, other error classes, unfinished attempts or later behavior. Individual log errors cannot be mapped to the metric failures without additional evidence.

Recorded action stages:

- C1: the change journal reports the application of revision c17 to pod-a as completed. That records the journal's claim, without independently proving effective runtime state or causal impact
- N1: a rollback was described as prepared and awaiting a decision. Approval, execution and effect are unestablished
- The supplied records do not establish a restart or outreach action. Absence here does not prove none happened

## Hypotheses and missing evidence

| Hypothesis | Support | Limits or alternatives | Smallest missing discriminator |
| --- | --- | --- | --- |
| Revision c17 contributed to the errors | Change C1 and failures are close in time; M1 covers both | C1/L1 order is unresolved; M1 may include errors before C1; traces absent; pod-b logs missing | Existing authorized before/after per-revision failure evidence or a relevant trace showing the failure mechanism |
| Queue pressure occurred independently of c17 | L1 and L2 report queue deadlines | Deadline text does not identify the origin; no queue-depth or upstream evidence supplied | A bounded authorized queue/upstream series tied to the error window |
| A rollback caused the later zero-error bin | N1 mentions rollback preparation; M4 records zero 5xx | N1 is unplaced and proposed-only; no rollback execution record or effect evidence exists | An already-authorized action journal showing whether a rollback happened and a matching runtime observation |

All three remain hypotheses. The packet establishes no root cause or production-safety conclusion. Read additional already-authorized evidence within the boundary when available; request new access or a wider window only if needed, identifying the question it would answer. The trace source's absence and the pod-b gap remain explicit until evidence arrives.

## Executed checks

Executed on 2026-10-01 using local Python 3.12.14 and its standard library, from this skill folder:

```bash
python3 scripts/check-timeline.py
```

Observed output:

```text
PASS: 24 offline checks; Python 3.12.14
Events: 5 raw rows -> 4 unique identities; LOG: 3 rows -> 2 identities
C1: [2026-05-14T13:00:30Z, 2026-05-14T13:00:30Z]
L1, L1-copy: [2026-05-14T13:00:29Z, 2026-05-14T13:00:31Z]
L2: [2026-05-14T13:00:34Z, 2026-05-14T13:00:36Z]
N1: unplaced
Order: C1/L1 unresolved; L1 before L2; N1 absolute position unknown
Sources: 4/5 available; MET: 180/240 seconds covered; missing [13:01,13:02) UTC
M1: 12/200 -> 6%
M3: 3/None -> unknown
M4: 0/180 -> 0%
Completed-action evidence: C1; proposed-only evidence: N1
```

The 24 checks cover offset conversion; missing offsets and clock bounds; positive and negative skew; overlapping, touching and disjoint intervals; reversed receipt order; row reconciliation; same-text distinct IDs; conflicting duplicate payloads; reused IDs in a different namespace; source availability; missing/overlapping/clipped coverage; known, missing and zero denominators; and proposed versus completed action stages. Synthetic mutations exist only in memory; input files are not changed.

Limits: these checks implement this fixture's explicit clock and metric contracts. They do not discover clock calibration, validate live queries, authenticate exports, infer causes, measure a real incident or exercise production systems. Source completeness and the written causal interpretation still require evidence review.
