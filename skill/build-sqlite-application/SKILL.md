---
name: build-sqlite-application
description: Build or maintain a durable SQLite application, carrying one application contract through schema, public operations, imports, reads, saved-file evolution, and reopened caller checks. Use for working local software with retained data; a standalone model design, reporting query, or migration rehearsal has a narrower workflow.
---

# Build and maintain a SQLite application

Deliver the user's useful operation, a database that survives reopening, and a consumer that can keep using it. Start with one write and one useful read. Add the parts of an application lifecycle that the actual task needs.

Preserve the chosen language, driver, interface, and project conventions. A CLI or callable module can be the whole application. SQLite suits application-local storage; shared files accessed directly across machines or many writers that cannot take turns warrant a separate storage decision. Consult [SQLite's intended uses](https://www.sqlite.org/whentouse.html) when fit is uncertain. Do not add an ORM, server, UI, event store, or migration framework merely to organize a small local app.

## Carry one application contract

Read the existing schema and actual callers for maintenance work. Identify the selected database, who owns it, and what the requested change must preserve. For new work, choose the first operation from a concrete user task. Distinguish choices delegated to the developer from unresolved meanings that would change the user's result.

Keep the consequential decisions together in the application's existing README or specification. A few paragraphs can suffice; this is not a second schema. Link to the authoritative SQL and operations as they are implemented.

| Decision | Record only what changes behavior |
| --- | --- |
| Meaning and identity | What one entity and one occurrence represent; stable key and its scope; whether equal values can be separate occurrences; which facts may be corrected |
| Values and rules | Required values, absence versus empty or zero, units/time interpretation, relationship and lifecycle rules; storage constraint or operation responsible for each |
| Operations | Public inputs and outcomes; validation/default owner; effects that commit together; connection/transaction owner; repetition or conflict policy when relevant |
| Reads and interchange | Included population, output grain, order/ties, unknown values, and any coherent-snapshot requirement; exported identity and deliberate omissions |
| File lifecycle | Explicit database path; create/open behavior; supported schema/runtime capabilities; controlled upgrade and recovery behavior when needed |
| Evidence | Actual public invocation, meaningful expected result, reopened observation, and candidate/input identity sufficient to reproduce the check |

Follow a consequential distinction through the whole application. For example, two measurements with equal displayed values may still be separate observations. That decision affects their keys, a repeated add command, import matching, counts, export identifiers, and what an upgrade must preserve. Conversely, replaying a previously accepted source record may refer to the same observation. Do not let separate modules decide these meanings independently.

Update the affected contract clause when behavior changes, then update its schema/operation/read and evidence. Do not require a ledger or manifest when stable keys, ordinary constraints, and a short README already express the promise.

## Finish the first durable path

1. **Resolve the real consumer and file.** Choose one public command or function, the database path it uses, and a useful returned result. For an existing application, demonstrate the relevant current behavior on an authorized isolated copy before changing it. Preserve valuable source data and use the [evolution and delivery reference](references/evolution-and-delivery.md) before a transformation.
2. **Write the actual storage definition.** Derive keys, relationships, types, nulls, and constraints from the contract. Implement only the records needed by this path. Inspect the runtime library used by the consumer, not just a separately installed SQLite command. Check the particular capabilities the schema needs; an available newer version is not a reason to raise every consumer's minimum.
3. **Establish one connection and transaction policy.** Make initialization common to CLI, library, importer, and maintenance entry points. Choose the driver mode deliberately and put the commit boundary at the public operation promising the effects. Use the [operations reference](references/operations-and-connections.md) when implementing this seam or changing its ownership.
4. **Write and read through the public boundary.** Bind values, perform the domain write, finish the transaction, and return a meaningful result. Implement the read at its agreed population and grain. Expose expected invalid input, missing identity, or conflict outcomes in a way callers can act on.
5. **Close, reopen, and challenge it.** Exit the CLI process or close all owned connections; reopen the saved file through the intended consumer and check the actual values and identities. Exercise a nearby invalid operation and inspect its promised failure effects after reopening. For multi-write operations, fail after a meaningful earlier write to distinguish full rollback from merely rejecting the last statement.

Do not defer reopening until the entire application is built. A plausible in-memory result can hide the wrong file, missing commit, disabled enforcement, or startup that recreates data. Once this path works, extend it with the next user operation, preserving the same contract.

## Make SQLite enforce what the contract claims

An ordinary declared type uses SQLite's affinity rules; it is not strict input validation. `STRICT` tables, supported since SQLite 3.37.0, constrain stored types but permit lossless coercion. Choose them when compatible with the intended consumers. Use explicit domain ranges and application parsing for meanings a stored type cannot establish, such as a calendar date or an exact textual identifier. [SQLite strict typing](https://www.sqlite.org/stricttables.html)

Check these differences when writing real DDL:

- `UNIQUE` permits multiple NULLs; require `NOT NULL` when missing identity is forbidden
- A `CHECK` evaluating to NULL does not reject the row; specify requiredness separately from a range
- Ordinary primary keys have nullability exceptions; make required keys explicit. `INTEGER PRIMARY KEY` has special rowid/allocation behavior, so choose it deliberately
- `CREATE TABLE IF NOT EXISTS` does not reconcile an existing table with the desired definition

These are [SQLite table semantics](https://www.sqlite.org/lang_createtable.html), not reasons to use one universal key strategy. State whether identifiers can be reused after deletion or need to remain stable outside the file. Constrain genuine domain uniqueness without merging distinct occurrences that happen to look alike.

For relations, set and read back `PRAGMA foreign_keys = ON` on every relevant connection before starting a transaction. Enabling it within an active transaction has no effect; a schema containing `REFERENCES` alone does not establish enforcement. [SQLite foreign-key initialization](https://www.sqlite.org/foreignkeys.html#fk_enable)

Put rules spanning several rows in the operation that can enforce them together when a suitable constraint cannot. For example, “a collection has exactly one preferred member when nonempty” needs more than a foreign key. Identify whether all writers must use that operation, and do not claim arbitrary direct SQL is covered by an application-only rule.

Verify the consequential constraints on a disposable copy through a freshly initialized connection: attempt a relevant duplicate, missing required value, invalid type/range, or orphan as the schema warrants. Inspect the actual rejection and leave the probe uncommitted. A caller rejecting input before SQL is useful boundary evidence, but does not prove the database constraint is active.

## Extend only the branches the task needs

- **Imports, exports, or richer reports:** Read [identity, import authority, and read models](references/imports-and-read-models.md). Reuse domain rules while selecting the appropriate whole-batch or item-level commit owner
- **Several reads that must describe one state, composed writes, or competing writers:** Read [operations and connections](references/operations-and-connections.md). Establish resource lifetime, conflict/retry behavior, and any needed controlled interleaving
- **An existing saved file needs a change or a recoverable copy:** Read [evolution and delivery](references/evolution-and-delivery.md). Keep normal opening, upgrading, backup restoration, and old-code compatibility distinct
- **Portable distribution or a measured performance requirement:** Use the corresponding conditional section of [evolution and delivery](references/evolution-and-delivery.md). Neither branch is required for every local script

Keep focused methods in their roles when they are available: `design-data-model` and `design-api-contract` resolve substantial design questions; `service-import-rehearsal` establishes an external destination's rules; `schema-change-rehearsal` handles a consequential isolated transition; `implement-scoped-change` owns ordinary implementation; `release-artifact-verification` verifies a received distribution. This toolkit connects those decisions for a SQLite application. Do not make reading that entire chain a prerequisite for a small app.

## Deliver the application the user can continue using

Return runnable source, authoritative schema, concise usage/contract, and the retained database or supplied-data candidate requested by the task. Include the actual useful output, not only a test log. Keep demonstration and failure-test data out of the user's continuing file unless explicitly part of its intended contents.

Record the consumer/runtime, relevant code and input identities, commands, observed results, and any blocked checks in proportion to the task. A small deterministic public-caller check with independent expected records is often enough; a large evidence directory is not inherently stronger.

Exercise any promised export with its actual parser and any promised restored file with its intended app. State separately what was observed, what remains a design assumption, and what was not exercised. Local reopening and ordinary failure checks establish those paths on the identified candidate; they do not establish power-loss durability, every writer interleaving, production readiness, or an untested platform.
