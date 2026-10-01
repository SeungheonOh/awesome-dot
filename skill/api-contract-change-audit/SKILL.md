---
name: api-contract-change-audit
description: "Compare versioned API contracts and known consumers, produce directional compatibility findings and synthetic fixtures, and deliver a traceable migration report."
---

# Audit an API Change for Consumer Impact

Use this skill before changing a request, response or documented API behavior. Complete a consumer-aware comparison of the authorized inputs and produce findings another engineer can act on. A schema addition can still break an exhaustive client; a schema-compatible change can still alter pagination or retry behavior.

## Required inputs

- Old and proposed specifications with exact versions or immutable revisions, plus the operations in scope
- Authorized behavior notes, examples and relevant consumer code or documented assumptions
- Compatibility policy and supported old/new client-provider combinations, if defined
- Output instruction: return a report, create files, update a named document or post to an authorized review destination
- Available local validation commands and allowed execution environment, if validation is requested

A static audit can finish without a running service. Missing consumer code limits consumer conclusions; it does not prevent a structural comparison. Ask for old/new ordering or an operation boundary if ambiguous. Keep unspecified compatibility policy separate from source-established facts.

## Workflow

### 1. Fix the comparison identity and source coverage

Build a manifest with source ID, contract or consumer role, revision, file or URL, format, retrieved or supplied date and completeness. Identify which behavior notes govern each version. Preserve the original files; produce normalized extracts separately when file creation is authorized.

Inspect only relevant authorized inputs. If a specification contains credentials or identifying payloads, omit those values from artifacts and request sanitized material where needed. Resolve local references and already-authorized documentation references. Record unresolved references, missing schemas or ambiguous versions; do not replace them with guessed definitions or treat them as equal between versions.

If an existing permitted parser is available, parse both contracts and record its result. Parser failure means structural extraction is incomplete, not that the API itself is broken. A manual comparison of bounded visible operations remains useful when the parser or toolchain is unavailable.

### 2. Build comparable operation and field records

Match operations by HTTP method and path. Keep an explicit supplied rename mapping when paths change; similar operation names alone do not establish equivalence. Preserve content type, response status and parameter location, since a query parameter and a header with the same name are different inputs.

Record each field as:

`operation`, direction, location, status/content type where relevant, schema path, type, requiredness, nullability, allowed values, range or length constraints, default, additional-property rule and source locator

Include nested required fields, array element contracts, error responses and relevant union alternatives. Preserve absent, explicit null, empty string, empty array and empty object as distinct cases. Normalize cosmetic object-key ordering; do not normalize ordered enums, lists or examples when the documented behavior makes order meaningful. Keep documented defaults separately from validation defaults: a schema default annotation alone does not prove the server applies it.

### 3. Evaluate compatibility in the correct direction

Build one ledger row per material change, with old and new source locations. Apply these questions separately:

1. **Old client to new provider:** does the new provider still accept every supported old request? Adding a required request field, removing an allowed value or tightening a limit can reject an old request. An optional new field does not by itself invalidate old requests
2. **New provider to old client:** can the old client handle every response the new provider may emit? Removing a guaranteed field, adding an enum outcome or changing nullability can break the client. Adding a response property depends on whether the consumer ignores unknown properties or enforces a closed shape
3. **New client with old provider:** evaluate this separately only if that mixed-version state must be supported. A new optional request field may still fail an old provider that rejects unknown inputs

Use statuses such as compatible on inspected evidence, incompatible, conditional and unresolved. These statuses apply to a direction and a bounded change, not to the whole system by default. Where a specification permits behavior broader than observed examples, compare the permitted behavior. A few successful examples cannot establish the entire contract.

For complex unions or reference gaps that the available tools cannot resolve reliably, name the uncertain alternatives and the smallest required check. Avoid reducing a difficult schema to a reassuring type-name match.

### 4. Trace changes into known consumers and behavior

For each affected consumer, inspect the relevant request construction, response decoding, switches, pagination loop, error handling and retries. Record exact locations or attributed assumptions. Distinguish observed code behavior from a developer's expectation. An unavailable consumer is unassessed, not unaffected.

Review documented ordering, page-size defaults, cursor termination, status-code meanings, idempotency and retry rules alongside the schema diff. A new default page size may be structurally valid but alter a client that requests only one page. A nullable cursor becoming optional changes the final-page condition even if both versions express “no next page.” If schema, prose and consumer behavior disagree, preserve the conflict and identify the owner decision required.

Do not infer live behavior, undocumented timing guarantees or complete consumer coverage from static files. Keep unsupported consumers and unrelated endpoints outside the judgment.

### 5. Create distinguishing fixtures and verify the findings

For every incompatible or conditional change, create the smallest synthetic request or response that distinguishes the contracts or the consumer behavior. Give each fixture an ID, relevant change IDs, payload, expected old-provider result, expected new-provider result and expected known-consumer result. Mark a result not applicable when the fixture is only a request or only a response.

Include ordinary, omitted, null and empty values where meaningful; an added enum member; and empty/final pagination pages. Include a retry fixture only when the supplied contract defines a relevant repeated-operation rule. Do not invent an idempotency guarantee to fill the matrix.

Use an existing authorized local validator or consumer test harness when it is available and safe for the requested work. Record command, revision, environment, exit result and what the check actually proves. Without it, evaluate the extracts explicitly and label application or schema-tool execution unrun. Never turn a hand-evaluated fixture into a claimed endpoint test.

Check each finding in reverse: identify a concrete old request rejected by the new provider, or a permitted new response the old consumer cannot handle. If none is established, downgrade an asserted break to conditional or unresolved. Structural validation alone does not resolve behavioral compatibility.

### 6. Deliver the report and requested artifacts

Lead with the changes that require a decision before release. Return a ledger containing change ID, operation, old/new locations, compatibility direction, result, consumer impact, fixture IDs, proposed adaptation and unresolved decision. Attach the version-combination grid, source manifest and fixtures. Explain the smallest migration option without applying it to product code unless that action is separately within the user's request.

Place the report and files in the already-authorized destination. Before updating a document or review thread, verify its identity and audience and preserve unrelated content. Do not ask again solely because the user requested an external destination. After placement, read back the artifact, check that locations and caveats survived, and provide a verified link when available. If the result is uncertain, inspect before retrying; if access is blocked, return the completed report with the precise remaining delivery step.

## Deliverables

- A source-linked change ledger with separate judgments for each supported compatibility direction
- A known-consumer impact map that exposes missing coverage
- Synthetic fixtures with explicit expected outcomes and recorded check methods
- Migration actions, policy decisions and mixed-version limits
- The actual report or authorized destination link, with unavailable checks clearly stated

## Verification

Reconcile every in-scope changed operation to a finding or an explicit no-material-change note. Inspect request and response requiredness in opposite directions. Confirm omitted and null states remain distinct, and check added enum values against actual exhaustive consumers. Ensure every incompatibility has a distinguishing fixture or direct source-established contradiction. Verify every proposed adaptation cites the upstream change and consumer assumption it addresses. Separate parser validation, consumer execution and endpoint execution in the check report.

[The fictional worked example](example.md) includes a new request requirement, an additive response enum, a default change and a final-page shape change. Its expected results are based on supplied contract extracts and a fictional consumer rule set.

[The repeatable check](verification.md) evaluates those bounded request, response and consumer predicates separately, retaining unknown old-provider query handling. It is not a complete schema validator or a live endpoint test.

## Stop and ask

- Ask when field meaning, version overlap, policy authority or contradictory source evidence changes a release recommendation
- A missing reference blocks only the dependent judgment; finish the comparisons supported by available material
- Product edits, live endpoint calls, package installation, new access or a broader audience must be within the user's requested scope and applicable permissions before proceeding
- Do not expose private contracts to an unapproved destination or treat publication of the audit as permission to release the API

## Example request

```text
dot, compare API contract v1 with proposed v2 for these operations and inspect the supplied client excerpt. Produce a directional compatibility ledger, synthetic fixtures and the smallest consumer migration actions. Put the completed report in [AUTHORIZED DESTINATION]. Use available local checks, report exactly what ran, and leave live endpoint calls and product edits outside this audit.
```

## Evidence status

This skill completes an audit on the inputs actually available. The included example is fictional; its local consistency checks are not evidence of application compatibility or a deployed endpoint test. Report unknown references, uninspected consumers and unrun checks explicitly.
