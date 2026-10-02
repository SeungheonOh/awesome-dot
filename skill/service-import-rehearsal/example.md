# A bounded asset import with partial success

Everything in this example is fictional. The asset registry is an invented service used to specify and test import behavior; these files make no claim about any real product. The scripted run reads and writes local files only.

## Request and scope

> Rehearse this asset export for the synthetic account's asset registry. Use the supplied import contract and target evidence. Show creates, field changes, equal records, rejects and ambiguous matches. Keep IDs exact, allow the documented detail clear, and suppress only the documented exact export duplicate. Produce a machine-import subset and reconcile the supplied fictional partial-result evidence. Do not submit anything.

The [contract](fixtures/import-contract.json) makes this target unusually explicit: external keys are exact text, updates require a revision, creates enforce unique keys, text cells are literal, rows can partially succeed, and replaying the same operation key and payload has a 24-hour deduplication window. Those are fictional premises, not features a real importer can be assumed to have.

The [target export](fixtures/target-before.json) is truncated. Its separate complete exact-key lookup evidence establishes the relevant identity matches. There is no such evidence for `0500`, so its absence from the visible export cannot authorize a create. `0200` has two proven matches and stays ambiguous.

## Actual generated result

[The import-ready CSV](outputs/import-ready.csv) contains five operations, with original UTF-8 text and stable operation keys. It is for the fictional machine importer. Review the [JSON operation plan](outputs/operation-plan.json), not a spreadsheet that could interpret the literal formula-like cell.

| Source record | Exact external ID | Disposition | Result |
| --- | --- | --- | --- |
| S001 | 0007 | No-op | Label and status agree; blank note preserves `preserve me` |
| S002 | 0042 | Update | Rename cache to `Build cache, east`; explicitly clear details; preserve active status; require F-102 revision v7 |
| S003 | 0099 | Create | Preserve the leading-zero key and multiline `R&D; café` note |
| S004 | 0100 | Create | Store `=VERSION()` and `@queue` literally under the fictional text rule |
| S005 | 0008 | No-op | Blank label and note preserve the retired asset's existing values |
| S006 | 0101 | Reject | `sleeping` is outside the allowed status values |
| S007 | 0102 | Reject | Create lacks a required label |
| S008 | 0200 | Ambiguous | Two target records share the external identity |
| S009 | 0300 | Ambiguous | Conflicts with S010's label for the same source identity |
| S010 | 0300 | Ambiguous | Conflicts with S009; no implicit winner |
| S011 | 0009 | Ambiguous | Supplied F-105 belongs to external ID 0900, while 0009 resolves to F-104 |
| S012 | Empty | Reject | Required external identity is missing |
| S013 | 0400 | Create | First representative of the documented exact export duplicate |
| S014 | 0400 | No-op | Exact duplicate suppressed under the supplied export rule; lineage points to S013 |
| S015 | 0006 | Update | Set `Worker 🧪`, clear details, preserve retired status; require F-106 revision v4 |
| S016 | 0500 | Ambiguous | Export is incomplete and authoritative exact-key evidence is missing |

The source has 16 logical CSV records despite the newline inside S003's note. [Reconciliation](outputs/reconciliation.json) proves `16 = 3 creates + 2 updates + 3 no-ops + 3 rejects + 5 ambiguous records`; the submitted candidate is `3 + 2 = 5` unique identities. Two no-ops are existing equal records; one is a duplicate source representation. Eight excluded problem records remain in [rejects and ambiguities](outputs/rejects-and-ambiguities.json).

The [mapping](outputs/mapping.json) distinguishes blank behavior on create and update for every field. The [manifest](outputs/manifest.json) binds the source, contract, target evidence, synthetic partial result and saved import files with SHA-256 hashes. The plan includes source hash plus logical record ordinal for lineage, exact raw cells, before/intended values and per-operation payload hashes.

## Fictional lost-response outcome

The [partial-result fixture](fixtures/partial-result.json) imagines submission at 10:00 UTC and readback at 10:01 UTC on 12 January 2026. It binds receipts to fixture source ordinals for offline evaluation only. These are not observed live receipts. A real run must bind independently returned receipts to its actual job, submitted operations and destination.

| Submitted record | Evidence | Decision |
| --- | --- | --- |
| S002 | Applied receipt plus matching F-102 readback | Confirmed applied; exclude from retries |
| S003 | Applied receipt plus matching new F-201 readback | Confirmed applied; exclude from retries |
| S004 | Response lost; complete exact lookup currently empty | Eligible to replay the identical operation key/payload within the fictional retention window; absence alone does not prove it never ran |
| S013 | Explicit service rejection and empty readback | Confirmed rejected; preserve the error and investigate the collection restriction before proposing a corrected operation |
| S015 | Response lost; target now has a different label at revision v5 | Hold conflict; it may have failed, or applied and been changed afterward; neither blind replay nor rollback is justified |

[Partial-result reconciliation](outputs/partial-result-reconciliation.json) accounts for all five candidate operations: two confirmed applied, one eligible same-key retry, one confirmed rejected and one held conflict. [The retry candidate](outputs/same-key-retry-candidate.csv) contains only S004 copied with its original operation key and unchanged payload. It represents the fictional evaluation time, not an indefinitely valid retry file. No submission or retry was executed.

The rejection for S013 also shows a rehearsal's limit: a service may reject an otherwise valid candidate because of a runtime restriction missing from supplied contract evidence. Do not report that candidate generation guarantees acceptance.

## Run or adapt

From the skill folder:

```sh
python3 scripts/rehearse.py --fixtures fixtures --output outputs
python3 scripts/verify.py
```

The helper uses only the Python standard library. It deliberately rejects another adapter name, another target scope, contradictory lookup records, duplicate headers and ragged records. The JSON contract contains human-readable semantics; its prose is not an executable rule language. Changing that prose alone does not change the adapter. To use the pattern for a real service, replace and review the adapter against current official rules, accepted file syntax, actual identity evidence and the user's bounded authorization, then test distinguishing cases before any live import.

Retain original operation keys and bytes for recovery. Editing the source creates a new input identity; regenerating the plan is not a substitute for recovering an uncertain earlier job. Never treat the generated idempotency column as protection unless the real service actually supports it.
