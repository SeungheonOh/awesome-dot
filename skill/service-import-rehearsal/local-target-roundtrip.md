# Actual local consumer round trip

This extension consumes the rehearsal's saved `outputs/import-ready.csv` with an original, small SQLite target. It executes real local transactions and reopens the resulting database through fresh connections. The target implements the explicitly fictional asset-registry contract; it is not a real service integration or evidence about any product's importer.

## Reproduce

From this skill's directory, run:

```sh
python3 -B scripts/verify_local_target.py --work local-work --output outputs
```

Alternatively, run the verifier from a separate folder and pass `--package /path/to/service-import-rehearsal`. Python's standard library, including its bundled SQLite module, is sufficient. No network, installation, account, or credentials are used. The verifier leaves all input bytes unchanged, creates temporary database files under `--work`, writes two JSON artifacts under `--output`, reopens those JSON files to verify them, and removes its temporary databases. There is no public binary database.

- `outputs/local-target-readback.json` contains the actual primary target readback, including all records, generated IDs and revisions, and the durable request/receipt ledger
- `outputs/local-target-report.json` identifies input/code hashes, executed runtime versions, passed checks, caller-visible receipts, replay results, rejected stale updates, and limitations

## Observed result

The run on 2 October 2026 passed 24 checks. All five actual CSV rows were consumed: three creates and two updates. The reopened database contained 11 records, including all eight original target records. Both pre-existing records for external ID `0200` were preserved, as were the complete values and revisions of the six original records outside the update set.

| CSV source | Persisted result |
| --- | --- |
| S002 | F-102 changed to `Build cache, east`, details became SQL NULL, status stayed active, revision became v8 |
| S003 | LOCAL-0001 stored `CI spool` and the exact multiline `R&D; café` / `rack B` details |
| S004 | LOCAL-0002 stored `=VERSION()` and `@queue` literally |
| S013 | LOCAL-0003 stored one `0400` record; the source duplicate did not become another import operation |
| S015 | F-106 changed to `Worker 🧪`, details became SQL NULL, status stayed retired, revision became v5 |

The actual source CSV is still the unchanged 16-record fixture. The verifier independently feeds the saved five-row import to the consumer and compares reopened values with the existing adapter's intended values. It does not submit excluded source rows. The supplied fictional partial-result packet is neither loaded nor treated as observed evidence.

## Persistence and recovery checks

Each imported row runs inside `BEGIN IMMEDIATE`. Identity checking, the create or revision-guarded update, and the durable receipt commit together. Different rows can succeed or fail independently. Parameterized SQL stores exact text without formula evaluation, trimming, case folding, or Unicode normalization.

Each readback uses one explicit read transaction, so the ID counter, records and receipt ledger share one snapshot. A deterministic regression enables SQLite WAL mode and commits a create through a second connection precisely after the reader fetches records but before it fetches receipts. The reader still returns the coherent earlier state: eight records, zero operations and next ID 1. A subsequent connection sees the committed state: nine records, one operation and next ID 2. The test uses a SQL trace callback, without timing sleeps. A negative-control run removed the read transaction from a temporary code copy; the regression failed at the intended snapshot-coherence assertion.

There is no unique database index on external ID: such an index would contradict the preserved legacy duplicate records. The only unique record index is the internal record ID primary key. New-create uniqueness is enforced by checking existing keys while holding SQLite's serialized writer lock. Two threaded submissions, each opening its own connection and submitting a different operation key, for the same new external ID produced one applied create and one `external_id_exists` rejection. This guarantee applies to writers using this consumer; arbitrary direct SQL can bypass it.

The primary run deliberately discarded S003's response after the real local commit. A fresh connection found both its record and durable receipt. Replaying the same request one logical minute later returned that original receipt without changing records, revisions, ID allocation, or the operation ledger. Replaying S002 likewise returned its original success before rechecking its now-stale original revision. A changed cell under the same key was rejected. A replay at the 24-hour boundary was held rather than sent as new work.

The local idempotency payload is canonical UTF-8 JSON of the exact decoded CSV cell strings. Alternative CSV quoting that decodes to the same cells produces the same request bytes. Any changed cell produces different request bytes. Keys are scoped to the fictional destination. This is this consumer's explicit local representation, not a claim about a remote service's byte handling.

In a separate target, another connection committed a label/details change and advanced F-106 from v4 to v5 after planning. Consuming the unchanged five-row CSV then committed the first four operations and rejected the fifth with `revision_conflict`. The other writer's values remained intact. Another injected failure aborted receipt insertion after a create; the transaction rolled back the new record and generated-ID allocation together.

Additional probes checked blank details preservation versus explicit clear, create defaults, exact leading-zero distinctions, literal formula-like strings, whitespace and Unicode, new-key duplicate creates, ambiguous legacy updates, preflight duplicate-batch rejection, unchanged input bytes, the actual database indexes, and reopened SQLite integrity.

## Limits

This is a local implementation of supplied fictional rules. Seeding the fixture's eight visible records does not establish completeness of the original truncated export or resolve excluded identities. The test provides no evidence of a real service's parser, permissions, consistency, idempotency, notifications, quotas, or side effects.

Response loss is a deliberate local discard after commit, not a network failure. Replay age uses controlled logical seconds; the run does not wait 24 hours. Expired keys are conservatively rejected. The bounded two-thread submission test and receipt-write rollback demonstrate the exercised transactions, not production stress, every interleaving, process-crash recovery, or power-loss durability. Revision generation supports only this sample's `v`-number fixture format. No new adapter framework, server, or UI is introduced.

The public package also passed the repository's bounded path/process/credential-pattern scan. Its two generated JSON files were reopened and inspected: their metadata contains relative input labels, hashes, runtime versions, a UTC execution timestamp, fictional identifiers, and local test observations. No absolute execution paths, host/user names, account tokens, or binary database metadata are included. The pattern scan is not a proof against every possible disclosure.
