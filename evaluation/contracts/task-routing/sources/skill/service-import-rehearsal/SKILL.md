---
name: service-import-rehearsal
description: "Rehearse a bounded CSV import against a service's actual import rules and target identities, produce an import-ready subset plus rejects, and reconcile partial success before any retry."
---

# Rehearse a Service Import and Account for Every Row

Turn a proposed CSV import into a concrete create/update/no-op/reject/ambiguous plan before it changes an account. The outcome is an import-ready subset tied to target identities and a readable explanation of every excluded row. This is about how a particular service will interpret the upload, not general spreadsheet cleanup or comparing API versions.

## Minimum inputs

- Source CSV or authorized export, its record scope, and the intended destination account and collection
- The service's import contract: accepted columns, identity or upsert keys, types, create/update rules, blank and clear behavior, allowed values, error handling, and available preview/readback methods
- An authorized target snapshot or read access to resolve identities, with pagination, filters, retrieval time and completeness recorded
- Desired result: rehearsal only, or a specific already-authorized bounded import with the permitted creates, updates and field changes

Inspect the supplied files and any relevant already-authorized destination access before asking for missing details; honor an explicit supplied-packet-only or offline limit. If the service's rules are unknown, finish source inventory and mapping proposals, but withhold dependent rows from the import-ready subset. A plausible column name does not establish import behavior. When using a real product, read its current official import documentation and the actual import screen or supported interface; record the relevant version or retrieval date. Do not substitute this skill's fictional rules.

## Workflow

### 1. Freeze the intended operation and its evidence

Record source hash, encoding, delimiter, column order, CSV record count, destination account/collection, and the specific import mode. Retain an untouched input. Assign stable source IDs from the source hash and record ordinal; quoted multiline fields count as one CSV record.

Capture target record IDs, revisions and the identity lookup evidence. An export may omit filtered, archived, deleted, permission-hidden or not-yet-fetched records. Absence from a truncated export is not proof of nonexistence. Resolve missing keys through an authoritative exact lookup or complete export of the relevant identity scope, including archived records if they reserve the same key. If uniqueness itself is unproved, even one visible match can be ambiguous.

Record whether the importer is atomic, allows partial success, triggers notifications or other side effects, exposes per-row receipts, enforces uniqueness or version preconditions, and supports idempotency. An undocumented property remains unknown. A local rehearsal is not evidence that the service implements these safeguards.

### 2. Write the source-to-target mapping and value rules

Produce a mapping artifact with source column, target field, type, conversion, requiredness, missing-value meaning and the rule's evidence. Include unmapped source columns and deliberate omissions. Do not silently drop unknown columns that could contain required identity or scope.

- Parse identifiers as text; preserve leading zeros and long IDs. Keep source identity separate from the service's internal record ID
- Preserve Unicode, quoted commas, embedded newlines and significant whitespace. Case folding, trimming and Unicode normalization are matching rules only when the destination establishes them
- Distinguish omitted column, empty CSV cell, whitespace, zero, explicit clear token and literal text that resembles a clear token. A blank may mean ignore on update but default on create; some services instead erase existing data
- Establish the spelling and escaping of every reserved control token, including explicit clear and leave-unchanged tokens. If a literal value cannot be represented without becoming an operation or omission instruction, reject that row rather than changing its meaning
- Treat formula-like values as text while parsing. Confirm the target's documented behavior. Preserve literal machine-import values when the target stores text; use a separate JSON or text-safe review artifact. If the target evaluates them and literal storage cannot be assured, hold those rows. Do not prepend an apostrophe unless that target explicitly requires it
- Preserve unsupported values in the reject artifact with source IDs and reasons. Do not invent status aliases, defaults, or replacement values

### 3. Resolve identities and classify every source record

Use the contract's exact identity key within the destination scope. Names, labels and similar-looking text are not stable IDs. If both a source external key and a target record ID are present, verify that they point to the same record. Never let one silently override the other.

Assign exactly one primary disposition to each source record:

| Disposition | Evidence needed | Submission behavior |
| --- | --- | --- |
| Create | Authoritative absence and valid required create values; the selected mode permits creation | Include with the documented identity and duplicate prevention |
| Update | One proven target identity, authorized field differences, and any required revision condition | Include intended changes plus the identity, revision and unchanged fields the real importer requires; identify those separately |
| No-op | Existing intended values already agree, or a documented duplicate-export rule suppresses an exact repeated source record | Exclude; distinguish already-equal from duplicate-suppressed |
| Reject | A known import constraint fails, such as missing identity, unsupported enum or unrepresentable value | Exclude with the exact failed rule |
| Ambiguous | Unknown existence, multiple matches, conflicting source identities, contradictory mapping evidence or unresolved meaning | Exclude with the smallest needed decision or lookup |

Group duplicate source external keys and repeated explicit target IDs before generating operations. Conflicting rows must not compete through an accidental first-row or last-row winner. Collapse exact source repeats only when an established export or user rule says they are duplicated representations of one object; preserve their lineage. Without that rule, keep same-key repeats ambiguous rather than choosing a representative or calling the rest no-ops. A repeated event can be legitimate. Duplicate target identities remain ambiguous even when one visible record looks more complete.

For each proposed create/update, retain before and intended-after values, source IDs, target ID if present, exact changed fields, revision condition and payload digest. Distinguish actual changes from unchanged values or control fields that the importer requires in its payload; omitting such a field can itself change behavior. If the service provides a genuine idempotency key, derive and retain a stable operation key for that immutable payload. A locally invented column does not make an importer idempotent. Keep unsupported guard mechanisms in the plan, not in an upload that would ignore or misinterpret them.

### 4. Write and reopen the actual deliverables

Generate the service-compatible import-ready file containing only supported, unambiguous, authorized operations. If create and update require separate modes or files, split them explicitly. Write the mapping, full row plan, reject/ambiguity register and reconciliation report alongside it. For a small task, combine these supporting sections into one report; separate machine-readable files only when they help the user or downstream consumer. Use a review format that cannot accidentally execute formula-like text.

Reconcile these independently:

```text
source records = create + update + no-op + reject + ambiguous
import-ready records = create + update
unique submitted identities = import-ready records
```

Document exceptions for services that legitimately require multiple operations on one object; do not force this one-record-per-identity model onto them. Every excluded row must remain traceable. Never add filler rows or silently reclassify ambiguity to make counts agree.

Reopen the saved files with their intended parser. Verify schema, row counts, exact IDs, leading zeros, Unicode, multiline fields, clear tokens, changed fields and operation/payload relationships. Confirm the untouched source hash. Inspect the real service preview when available and authorized. Any mismatch between local plan and service preview blocks only dependent operations until understood.

### 5. Apply a bounded authorized import when requested

A rehearsal request ends with the files and decisions. It is not permission to change an account. If the user has already authorized this destination, source population and bounded changes, proceed through the supported import route without asking again solely because the rehearsal finished. Reconfirm only a material change in account, fields, identity handling, scope, side effects or other required authority.

Immediately before submission, refresh affected identities and revisions. Replan concurrent changes. Submit only when the route supports the required semantics and post-import readback is possible. If the interface cannot enforce a needed condition, explain the specific risk and stop that portion; do not imply the CSV's unused columns provide protection. Avoid a live "test row" unless the user authorized creating or changing it and any resulting side effects.

Retain the exact submitted bytes, job/batch ID, operation IDs where supported, receipts and submission time. An accepted upload or HTTP success is not proof that every row applied. Poll a job through its documented terminal state and gather per-row outcomes where available.

### 6. Reconcile readback before retrying

Read affected records through stable identities; resolve created IDs through an authoritative exact lookup. Compare intended values and any contract-defined canonicalization, plus untouched fields that must survive. Record the observed revision and readback time. A matching value proves observed state; without a receipt or operation history, it may not prove which operation caused that state. If effects such as sending a notification matter, value readback alone does not prove whether they occurred.

For partial success or lost responses, classify each submitted row independently:

- Confirmed applied: operation evidence and readback agree; exclude it from retries
- Observed desired state without sufficient operation evidence: record that distinction; do not blindly repeat the operation or its side effects
- Confirmed rejected: retain the exact service error; fix the stated issue only within authorized scope and produce a new payload/rehearsal
- Authoritatively not applied: a documented retry may be possible, using the same immutable payload and valid idempotency key when supported
- Unknown or conflicting: incomplete/stale readback, elapsed idempotency retention, changed revision or contradictory receipt; hold the row and obtain stronger evidence

Do not resubmit the whole CSV after a timeout. Before retrying, establish the service's idempotency retention, same-key/same-payload rule, uniqueness enforcement, concurrency conditions and side-effect behavior. Without those guarantees, investigate through supported job history or exact readback; a newly generated key is a new operation. Even absence after deletion may not prove an earlier create never happened. Avoid automatic rollback of applied rows: later user edits and external effects may make it unsafe.

## Deliverable and completion check

Return the actual import-ready subset, mapping, full operation plan, reject/ambiguity register and row reconciliation. If a live import was authorized and performed, also provide the submitted file identity, service job reference, confirmed readback results and a per-operation retry/hold ledger. State what changed, what remains excluded and the smallest action that resolves it.

Check that all source records have one disposition, every submitted identity is unambiguous, leading-zero and Unicode values survived saved-file readback, clears differ from blanks, every update preserves unintended fields, and every retry decision cites actual service evidence. Do not present a successful file parse as a successful import.

## Worked rehearsal

[The example](example.md) uses a wholly fictional asset registry. Its [contract](fixtures/import-contract.json), [source CSV](fixtures/source.csv), [target snapshot](fixtures/target-before.json), and [partial-result evidence](fixtures/partial-result.json) are synthetic. No names, contacts, credentials or live account records are needed.

The included [offline helper](scripts/rehearse.py) implements only that fictional contract. Its useful reusable parts are record-based CSV parsing, exact identity grouping, immutable operation digests, before/after plans and readback accounting. Inspect and adapt the contract adapter before using it for a real service; it never submits a request. Run the example and its behavioral checks from this folder:

```sh
python3 scripts/rehearse.py --fixtures fixtures --output outputs
python3 scripts/verify.py
```

The committed outputs are actual generated artifacts, not an empty template. [Verification](verification.md) records what was executed and the boundaries of the evidence.

The separate [local consumer round trip](local-target-roundtrip.md) actually imports this saved candidate into an isolated SQLite sample target and reopens persisted records and receipts. It tests the fictional rules through a second implementation, including lost-response replay, revision guards and coherent readback. This is optional worked evidence for the pattern, not a service connector or proof that a real destination has the same guarantees.
