# Verification record

The packet, ledger and recovery plan are wholly fictional. The executed checks test evidence accounting and conservative decision behavior. They do not connect to a service or perform a recovery.

## Executed result

Run on 2026-10-02 with Python 3.12.14 from this skill folder:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/check_recovery.py --output outputs
PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_recovery.py
```

Both commands exited 0. The checker reported:

```json
{
  "candidate_allowlist": ["ev-002"],
  "live_changes_performed": 0,
  "outcomes": {
    "applied_once": 2,
    "duplicate_effect": 1,
    "not_dispatched": 1,
    "terminal_not_applied": 3,
    "unknown_conflicting": 1
  },
  "source_events": 8,
  "status": "conditional_plan_only_not_executable"
}
```

The decision suite ran 26 tests and returned `OK`. Both saved output files were reopened with Python's JSON parser and compared to a fresh call of the reconciliation function with the exact same input hash; both matched exactly.

Input SHA-256 for [fixtures/packet.json](fixtures/packet.json):

```text
f41d6a832425d47a5c5266b193876372e8b7f628f73882815de4df72d9194ffb
```

The generated [ledger](outputs/reconciliation.json) and [plan](outputs/recovery-plan.json) each retain this hash. If the packet changes, rerun the commands and update this record instead of retaining a stale verification claim.

## Decision boundaries exercised

| Check | Observed result |
| --- | --- |
| Full event accounting | Eight ledger rows, outcome counts sum to eight; only ev-002 is a candidate |
| HTTP acceptance versus completion | ev-002 has 202 and durable receipt, yet terminal nonapplication is preserved |
| Repeated transport | ev-001 has two attempts and one committed effect, so no replay is proposed |
| Repeated effect | ev-007 has one delivery and two committed creates; cleanup stays separate |
| Newer target edit | ev-003's revision-8 expectation cannot overwrite human-edited revision 10 |
| Deletion and ordering | ev-004 stays held; ev-005's committed delete and matching version-5 tombstone are recognized |
| Missing history with matching current state | ev-006 remains unknown despite its matching title/status |
| Unsent source event | ev-008 remains a first-delivery decision, not a retry |
| Observed receipt without verified durability | A pending receipt with no run is labeled receipt_observed; only a durable state advances it to durable_receipt |
| Missing effect coverage or retained receipt | ev-002 leaves the candidate list; absent evidence is not filled in |
| Active automatic retry | ev-002 is pending and excluded |
| Source changes after evidence capture | A newer source version holds the candidate |
| Incomplete lookup or newly existing target | The absent-target create is excluded |
| Wrong run/event parent | Conflicting lineage yields unknown |
| Orphaned effect and deletion records | Unmatched rows remain in the orphan register |
| Orphaned effect contradicts a known candidate run | Both the conflict and row locator reach that event; the candidate is excluded |
| Event-to-target entity mismatch | Conflicting originating-event provenance blocks dependent recovery |
| Multiple retained receipts for one event | The contract conflict blocks selection; the helper does not choose the first receipt |
| Changed target title, status or source version | Readback is not claimed verified |
| Committed action differs from source event type | The effect is not accepted as matching application |
| Conflicting event identity | The helper rejects ambiguous input instead of choosing a row |
| Changed immutable payload | The saved event digest changes |
| Input preservation | Reconciliation leaves the in-memory input unchanged |

The helper reads the local packet and writes only the two requested JSON artifacts. Its reconciliation function has no network or mutation code. The test suite uses in-memory copies for changed-evidence cases; it does not edit the packet.

A separate guide-only rehearsal used a different fictional contract in which a task write and a notice were two intended effects. It kept their results separate, held the missing notice after the task had committed, and did not classify two different intended effects as a duplicate. It also placed a non-durable 202 receipt below durable acceptance. That review prompted explicit expected-effect/cardinality and transient-receipt guidance. The bundled checker remains limited to its own one-effect-per-event contract; the broader case did not turn it into a multi-effect interpreter.

## Reviewed limitations

- This is a bounded interpreter for the bundled schema and its explicit one-effect-per-event contract. It is not an integration parser or a proof of a real product's behavior
- Coverage fields and contract assertions are supplied fictional evidence. The helper cannot authenticate them or establish completeness from logs by itself
- The helper checks target identity, originating event, source version, intended title/status and committed action. It conservatively leaves a divergent readback unknown; a real later edit requires additional history before distinguishing historical application from current-state agreement
- Comments on both duplicate targets are retained as a reason to hold cleanup. The helper does not merge, delete or choose a survivor
- The v2 mapping and guarded recovery route are proposals. No implementation, atomicity, lock ownership, deployment, live replay, real idempotency behavior or side-effect suppression has been verified
- No real provider documentation is cited or implied; every product contract in this example is fictional
- Passing local checks does not authorize any live action. The one-event candidate still requires actual implementation evidence, current preconditions, applicable authority and verified terminal/readback results
