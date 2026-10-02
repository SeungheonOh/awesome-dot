# Worked reconciliation: accepted tasks missing from the board

This is an original fictional case. Larkspur Track, Lantern Board, their contracts, IDs, logs and values exist only in this example. No live service, private account or real person's record was used. The requested work is diagnosis and a bounded recovery plan. No real handler was patched and no event was replayed.

## Completed finding

The eight source events map to eight transport attempts, six observed durable receipts and five current target records; the mapping is not one-to-one. The evidence establishes three terminal transformation failures, two events applied once, one duplicate effect, one event never dispatched and one outcome that remains untraceable. Only **ev-002** belongs in a conditional recovery candidate list. Its execution remains blocked until the proposed repair route is implemented, verified and authorized in an actual environment.

The accepted receipts for ev-002, ev-003 and ev-004 are real within this fictional packet, but their jobs failed before target application. Replaying all three would be wrong: ev-003 would collide with a newer human edit, while ev-004 has been superseded by deletion. Re-sending the original HTTP delivery would also be the wrong recovery path: the fictional inbox deduplicates those already-accepted event IDs and does not restart dead-letter jobs.

The machine-readable completed artifacts are [the reconciliation ledger](outputs/reconciliation.json) and [the bounded recovery plan](outputs/recovery-plan.json). Their input SHA-256 binds them to the exact [evidence packet](fixtures/packet.json). Evidence labels such as `W03` refer to that packet's unique `row_id` values; `packet.json#W03` in generated JSON is a row locator, not a browser anchor.

## Scope and evidence manifest

- Integration: `link-17`, source account `larkspur-demo`, target project `lantern-demo`
- Source event population: 2026-05-12 09:00:00 UTC inclusive to 09:10:00 UTC exclusive
- Source/target/job-state reconciliation as of 2026-05-12 10:00:00 UTC
- Relevant event identity: `(source account, integration ID, event ID)`
- Relevant object identity: source entity ID; source object version and target revision are different counters
- Authorization: local evidence review and conditional-plan construction only

| Evidence | Packet location | Coverage and limitation |
| --- | --- | --- |
| Fictional behavior contract | `contract`, C01 | Version 1; includes actual v1 mapping and a clearly proposed v2 mapping/route |
| Source event export | `events`, S01–S08 | Complete population of eight events in the stated source interval |
| Current source state | `source_current`, SC01–SC08 where present | Complete exact lookups for seven source entities; CR-104 is now deleted at version 5 |
| Source dispatch history | `dispatch`, DS01–DS08 | Complete within event scope; ev-008 is explicitly unsent |
| Transport attempts | `deliveries`, D01–D08 | Eight attempts observed; seven 202 responses and one timeout |
| Durable inbox receipts | `receipts`, I01–I07 where present | Six unique receipts; receiver segment for ev-006 unavailable |
| Worker run export | `runs`, W01–W08 | Eight observed runs; complete for every scoped event except ev-006 |
| Target commit journal | `effects`, E01–E04 | Four observed committed mutations; event-scoped coverage complete except ev-006 |
| Target exact readback | `targets`, T01, T03, T06, T07A, T07B; `tombstones`, TB04 | Complete lookup for all seven entity identities, including archived/deleted state; five active records and one deletion marker |
| Coverage attestation | `coverage`, CV01 | Names missing receiver/worker/effect evidence for ev-006; absence there cannot establish nonapplication |

Completeness here is a declared property of the supplied fictional exports. The local checker does not authenticate it. A real investigation must obtain that coverage evidence from the actual query, pagination, retention and source behavior.

## Event-to-effect ledger

| Event | Delivery → receipt → processing | Target effect/readback | Finding and disposition | Decisive rows |
| --- | --- | --- | --- | --- |
| ev-001 / CR-101 v1 create | Two 202 attempts → ib-001 → one applied run, one suppressed run | One create tx-001 → LT-101, source version 1 | Applied once; no replay. Transport duplication did not become a second effect | S01, D01–D02, I01, W01–W02, E01, T01 |
| ev-002 / CR-102 v1 create | One 202 → ib-002 → run-002 dead-letter at transformation | No journal effect; complete lookup finds no target or tombstone | Terminal not applied; candidate only after transformation repair and guarded recovery implementation | S02, D03, I02, W03, SC02, CV01 |
| ev-003 / CR-103 v3 update | One 202 → ib-003 → run-003 dead-letter at transformation | No effect from this event; LT-103 now revision 10, human-edited to Blocked; event expected revision 8 | Terminal not applied; hold to preserve the newer human edit | S03, I03, W04, T03, SC03, CV01 |
| ev-004 / CR-104 v4 update | One 202 → ib-004 → run-004 dead-letter at transformation | No effect from this event; LT-104 has deletion marker for source v5 | Terminal not applied; stale replay blocked by deletion and superseding source version | S04, I04, W05, TB04, SC04, CV01 |
| ev-005 / CR-104 v5 delete | One 202 → ib-005 → run-005 applied | Committed deletion tx-005 and corresponding LT-104 tombstone | Applied once; no replay and no recreation | S05, I05, W06, E02, TB04 |
| ev-006 / CR-106 v1 create | One timed-out attempt → missing receipt/run segment | LT-106 has the desired title/status, but no source version or originating-event provenance; effect history unavailable | Unknown. Existing desired state cannot establish the event's effect or justify another create | S06, D07, T06, CV01 |
| ev-007 / CR-107 v1 create | One 202 → ib-007 → two applied runs | Two distinct committed creates tx-007a/b → LT-107A/B; both now have independent comments | Duplicate effect confirmed; hold for cause repair and separately authorized preservation/cleanup decision | S07, D08, I07, W07–W08, E03–E04, T07A–T07B |
| ev-008 / CR-108 v1 create | Dispatcher explicitly unsent; no attempt, receipt or run | Complete lookup finds no target or tombstone | Not dispatched. First delivery is a separate action, not a replay | S08, DS08, SC08, CV01 |

There are no unmatched downstream event IDs in this packet. The checker preserves such rows in an orphan register when present, instead of silently dropping them.

## Counts that answer different questions

| Unit | Observed count | Meaning |
| --- | ---: | --- |
| Source events | 8 | Includes both an update and a later delete for CR-104 |
| Distinct source entities | 7 | Six currently active, one deleted |
| Transport attempts | 8 | ev-001 sent twice; ev-008 not sent |
| HTTP 202 responses | 7 | Two refer to the same ib-001 receipt |
| Transport timeouts | 1 | Does not prove failed receipt or failed application |
| Distinct durable receipts observed | 6 | ev-006 remains unknown; ev-008 has not been sent |
| Processing runs observed | 8 | Includes suppressed and repeated processing |
| Committed effects observed | 4 | Three creates and one delete; excludes unknown ev-006 history |
| Active target records | 5 | Cover only four distinct active source entities because CR-107 has two records |
| Deletion markers | 1 | CR-104, source version 5 |

The primary outcomes reconcile as `2 applied once + 3 terminal not applied + 1 duplicate effect + 1 not dispatched + 1 unknown = 8 events`. Current target count alone would hide the two absent active entities CR-102/CR-108, the duplicate CR-107, the divergent manual status on CR-103 and uncertain provenance on CR-106. A count of missing records is not a replay list.

## Broken boundaries and supported mechanisms

1. **Transformation before target write:** C01's v1 table does not contain `queued`. W03–W05 record `unmapped source status: queued` at the transformation stage. The fictional contract places that failure before any target write or notification, and the complete event-scoped journal confirms no effects for those three events. This supports the mapping defect for those rows. The supplied domain requirement maps queued to Open. The proposed v2 table is a repair proposal, not a deployed fix
2. **One event produced two target creates:** W07–W08, E03–E04 and T07A–T07B establish the duplicate effect for ev-007. They do not establish why two processing runs were created or why their guards failed. C01 explicitly gives worker-1 no general effect-idempotency guarantee. Investigate the actual scheduling and write path before claiming a root cause or running cleanup
3. **Source never dispatched:** DS08 records that integration scheduling was paused before ev-008 was scheduled. This establishes the source-to-delivery break for that event; it does not establish the integration's present enabled/disabled state
4. **Unknown boundary:** D07 establishes only that a delivery was attempted and timed out. T06 establishes that the desired current record exists. Missing receiver/worker/effect evidence prevents joining those observations. Do not call it failed, recovered, applied exactly once or safe to replay

## The bounded recovery plan

The actual saved plan selects ev-002 and has a maximum of one recovery event. It records the immutable event digest, ib-002 and run-002, exact destination, current source expectation and intended values. The generated plan is deliberately marked `conditional_plan_only_not_executable`, with zero live changes.

Proposed outcome for ev-002:

- Source identity remains CR-102, version 1, current event ev-002, not deleted; payload remains identical to the saved digest
- Target exact lookup still returns zero matching active/archived records and zero deletion markers
- The original job remains terminal with no scheduled retry; effect history remains complete and empty for this event
- Intended create values are external_source_id CR-102, title Asset handoff, status Open
- The approved transformation change and a recovery route with real atomic target-state guards must exist and pass checks before execution
- The recovery must own the job exclusively, use a stable recovery operation identity, and commit the target effect and its journal together under the evidenced route's contract
- Readback must show one exact target identity with the intended fields and a matching committed effect; the terminal processing result and relevant side-effect evidence must agree

The example does not pretend the existing interface supports these protections. `retry_dead_letter_v2` is a proposed route whose implementation remains a prerequisite. A preflight snapshot or a custom idempotency-looking token is not an atomic write guard. If the actual destination cannot provide required protections, this action stays held while a supported approach is chosen.

Do not replay ev-002 through the original accepted ingress: C01 says the retained inbox receipt would be returned without restarting the failed job. Do not use a brand-new event ID to bypass that deduplication. A real supported dead-letter retry may be suitable only after its exact semantics and authority are established.

## Remaining decisions and smallest useful evidence

| Item | Preserve now | Next evidence or decision |
| --- | --- | --- |
| ev-003 | LT-103 revision 10 and human Blocked status | Owner's desired final state and the actual authorized write rule; do not automatically reapply revision-8 expectations |
| ev-004 | LT-104 deletion and source version 5 | No recovery needed for stale v4; preserve the exclusion when any later batch is built |
| ev-006 | LT-106 and uncertainty about its origin | Recover the specific receipt/worker/effect segment or authoritative provenance that can join this record to the event; if unavailable, leave unknown |
| ev-007 | Both targets and their independent comments | Inspect repeated-run mechanism; inventory links, comments and attachments, choose preservation/survivor policy with authority, then prepare exact cleanup separately |
| ev-008 | No fabricated replay attempt | Verify current scheduling state and authorize a bounded first delivery, with its own identity and current-target guards |
| ev-002 | One conditional candidate | Implement and validate the repair route, obtain scoped recovery authority, refresh every precondition, perform once and reconcile readback |

Do not broaden the selected event to all dead-letter jobs or the entire time window. Stop on any new target, changed payload/source version, deletion marker, pending retry, ambiguous effect, absent atomic guard, expanded side effect or unknown terminal/readback result.

## What was actually verified

The local [checker](scripts/check_recovery.py) generated both JSON artifacts from the packet. [Decision tests](scripts/test_recovery.py) exercise the decisive differences and changed-evidence cases, including lost coverage, active retries, newer source state, new targets, conflicting receipt/run lineage, orphaned effects and immutable payload identity. See [verification.md](verification.md) for the executed commands and limits.

These checks establish the fictional packet's accounting and decision behavior. They do not prove a real service's idempotency, locking, side effects, repair deployment or recovery success.
