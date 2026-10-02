# Executable supplement: shelf export contracts and clients

A response can satisfy both schema versions and still make an old client silently lose records. In this example the old client returns two of six records as a successful export after a provider default changes. A second witness starts with an empty nonfinal page; setting an explicit page size alone still loses all six records.

This is an original, separately authored fictional example for `GET /shelf-records`. It does **not** complete, reinterpret or replace the normalized `GET /deliveries` extracts in [example.md](example.md). In particular, that earlier C1 has no fixed-page-size requirement and its old unknown-query handling remains unknown. The clients here are separately named C-S1 and C-S2.

The supplied files are runnable local source material, including complete JSON Schema 2020-12 definitions for the scoped request object and successful response body. They are not an OpenAPI document or a full specification of HTTP transport, authentication, error responses, retries or concurrency. Those aspects are outside this example.

## Start with the result

The required original overlap cannot be approved: C-S1 with v2 produces incomplete output. The adapted C-S2 passes the executed v1/v2 fixtures, including sparse pagination and the new status, but this does not repair an old client that remains deployed.

| Required combination | Executed ordinary six-record export | Decision supported by this evidence |
| --- | --- | --- |
| C-S1 with v1 | Six rows, two calls, complete | Baseline works for this fixture |
| C-S1 with v2 | Two rows, one call, reported success; records 3–6 absent | Incompatible; required overlap fails |
| C-S2 with v1 | Six rows, two calls, complete | Adaptation works for the executed old-provider fixture |
| C-S2 with v2 | Six rows, two calls, complete | Adaptation works for the executed new-provider fixture |

Every call above is an in-memory function invocation. No HTTP request or deployed-provider integration ran. [The verification report](schema-consumer-verification.md) gives the command, environment and further negative controls. [The retained JSON](schema-consumer-fixture/observed.json) includes actual rows, requests, responses, validation errors and input hashes, rather than only expected pass flags.

## Source manifest and authority

All application content below is original fictional material, revision `shelf-example-r1`, authored for this example on 2026-10-02. The library/documentation sources explain validation semantics; they do not authorize application behavior. Relative files and JSON pointers identify each claim. The retained output hashes the executable inputs so a changed file can be distinguished from the observed run.

| Source | Role and completeness |
| --- | --- |
| [request-v1.json](schema-consumer-fixture/schemas/request-v1.json), ID `urn:shelf-example:request:1` | Complete v1 parsed-query object schema |
| [request-v2.json](schema-consumer-fixture/schemas/request-v2.json), ID `urn:shelf-example:request:2` | Complete v2 parsed-query object schema |
| [response-v1.json](schema-consumer-fixture/schemas/response-v1.json), ID `urn:shelf-example:response:1` | Complete v1 200 body schema |
| [response-v2.json](schema-consumer-fixture/schemas/response-v2.json), ID `urn:shelf-example:response:2` | Complete v2 200 body schema |
| [common.json](schema-consumer-fixture/schemas/common.json), ID `urn:shelf-example:common:1` | Complete local cursor and record-ID definitions |
| [behavior.json](schema-consumer-fixture/behavior.json), `shelf-behavior-r1` | Explicit omitted-limit behavior, final-page convention and original records |
| [Explicit behavior and consumer requirements](#explicit-behavior-and-consumer-requirements), `shelf-behavior-prose-r1` | Additional normative fictional source for opaque cursors, stable-snapshot behavior, completeness and failure requirements |
| `behavior.json#/consumer_policy`, `shelf-consumer-policy-r1` | Fictional owner-supplied requirements for adaptation and version overlap |
| [consumers.py](schema-consumer-fixture/consumers.py), `legacy_export` and `adapted_export` | Entire original local consumers C-S1/C-S2; no unavailable production client implied |
| [cases.json](schema-consumer-fixture/cases.json), `shelf-cases-r1` | Thirty-two distinguishing request/response instances with version-specific expectations |
| [run.py](schema-consumer-fixture/run.py), `LocalPages` and `main` | Local provider model, scripted scenarios and executable verification |

## Exact contract boundary

The request object represents already parsed, typed query arguments. It is not a query string: coercion from HTTP strings, repeated parameters and percent encoding are untested. Both versions allow only optional `limit` and `cursor`. `limit` is an integer from 1 through 4; `cursor` is a nonempty string of at most 64 characters. Unknown properties are rejected in **this** separately authored contract. The default annotations are 4 in v1 and 2 in v2. The assertion sets are otherwise identical.

Both response bodies require an `items` array of zero through four records. Each record requires `id` and `status`; unknown item and response properties are rejected. IDs match `record-` followed by a positive decimal integer. The v1 statuses are `ready` and `retired`; v2 adds `held`. A nonterminal `next_cursor` is a nonempty string of at most 64 characters. V1 requires the property and permits explicit null; v2 permits omission and rejects null.

These schemas constrain individual messages. They do not prove that records are complete, sorted, unique across pages or returned within a finite number of calls. They also do not express the relationship between a request's limit and its response length. Those constraints belong to the behavioral source and consumer checks.

## Explicit behavior and consumer requirements

This section is the normative fictional source `shelf-behavior-prose-r1`, alongside the machine-readable subset in `behavior.json`. Together they supply the following rules; none is inferred from a `default` keyword:

- An omitted limit means four items in v1 and two in v2. An explicit allowed limit is honored as an upper bound
- A missing request cursor starts a traversal. Nonterminal cursors are opaque continuation tokens. A syntactically valid but unknown token is not guaranteed to identify a page
- V1 fills every nonfinal page to the effective limit and uses `next_cursor: null` on the final page
- V2 may return short or empty nonfinal pages. A present cursor requires another request; omission is the only v2 final-page marker
- The successful fixture traversals describe one stable snapshot, return each expected record exactly once, preserve fixture order and terminate. Repeated cursors and duplicate IDs deliberately contradict those guarantees in the negative cases

C-S1 is the original client in `legacy_export`. It requests no explicit limit by default, labels only `ready` and `retired`, treats fewer than four rows as final, and otherwise reads `next_cursor` and recognizes null. This works with the v1 behavior for its default request. Its optional `explicit_limit=True` mode requests four rows; the runner uses that mode only to isolate failures that remain after a page-size-only patch. The required C-S1/v2 baseline uses the unchanged default mode.

The separately supplied `shelf-consumer-policy-r1` explicitly authorizes C-S2 to request `limit: 4`, label `held` as “On hold”, recognize the appropriate final marker for each known provider version, and continue after any short or empty nonfinal page. The client must export all expected rows, not silently discard unfamiliar statuses or return an incomplete export as success. The local validation boundary is given the provider version; version discovery or negotiation is not implemented.

The example sets a four-call budget for both clients. C-S2 also detects repeated cursors and duplicate records; C-S1 has no such checks. In C-S2, any of these failures raises an explicit error with no successful partial return. Four is a **fixture policy**, not a universal pagination limit: legitimate larger or sparser traversals can exceed it. Choosing a production limit, retry policy or partial-result contract requires separate product evidence.

The original overlap requirement includes C-S1/v1, C-S1/v2, C-S2/v1 and C-S2/v2. A successful C-S2 adaptation therefore does not by itself satisfy the requirement. The owner must either preserve the old behavior for C-S1 or authorize changing the rollout requirement and retiring C-S1 before v2 exposure. This example makes neither decision.

## Directional change ledger

| ID | Old and new evidence | Direction | Finding and distinguishing evidence | Source-authorized adaptation or open decision |
| --- | --- | --- | --- | --- |
| S01 | Request schemas `#/properties/limit/default`; `behavior.json#/versions/v1/omitted_limit` → `#/versions/v2/omitted_limit` | Old request → new provider acceptance | Structurally compatible: after removing `$id` and the `default` annotation, the entire request schemas are equal. Q01–Q15 exercise ordinary and boundary instances | Separate acceptance from behavior; C-S2 requests the supplied explicit limit |
| S02 | Same default sources; `legacy_export` short-page return | New-provider behavior → old client | Incompatible: the ordinary v2 run returns two rows and a cursor; C-S1 stops with four records missing. The first page is valid against **both** response schemas (P01 has the same shape) | Explicit size addresses this specific default-dependent witness, but is insufficient for S03–S05 |
| S03 | `behavior.json#/versions/v1/full_nonfinal_pages` → `#/versions/v2/full_nonfinal_pages`; both response schemas `#/properties/items` | New-provider behavior → old client | Incompatible even with explicit limit 4: `legacy-explicit-v2-sparse` returns zero of six records after an empty page with a cursor. P04 is structurally valid under both schemas; that does not establish compliance with v1's full-nonfinal-page behavior | C-S2 follows the cursor; `adapted-v2-sparse` returns six rows in three calls |
| S04 | Response schemas `#/properties/items/items/properties/status/enum`; C-S1 labels | New response → old client | Incompatible: `held` is allowed by v2 and rejected by the old consumer; P06 isolates the schema change and `legacy-explicit-v2-held` executes the failure | The explicit consumer policy maps `held` to “On hold”; C-S2 produces that row. No rule for unknown future statuses is invented |
| S05 | Response schemas `#/required` and `#/properties/next_cursor`; behavior `#/versions/*/terminal` | New response → old client, after the default issue is isolated | Incompatible: a full four-record final page with omitted cursor makes the explicit-limit old client fail `missing-next-cursor`. A short final page would mask this because C-S1 returns earlier | C-S2 accepts omission only after validation as v2, and null only after validation as v1 |
| S06 | Identical request assertion sets; `adapted_export` request construction; both terminal rules | Adapted client → old provider and old response → adapted client | Compatible on the inspected request construction and executed fixture: limit 4 and returned nonempty cursors are accepted; the old explicit-null final page yields all six records | Retain the old-provider branch while overlap is required. Arbitrary old-provider behavior is not established by the fixture |

No whole-response-schema inclusion claim is made: the enum broadens, but v2 removes explicit null and the requirement for a cursor property. The meaningful client question is whether its actual decoding and traversal handle the permitted messages for the selected version.

## What the witness actually returned

The ordinary v2 model applied its explicit behavior rule, effective limit 2, to `{}`. Its first response was:

```json
{
  "items": [
    {"id": "record-1", "status": "ready"},
    {"id": "record-2", "status": "retired"}
  ],
  "next_cursor": "offset-2"
}
```

C-S1 returned only `record-1/Ready` and `record-2/Retired`. The retained run identifies `record-3`, `record-4`, `record-5` and `record-6` as missing. Both validation and client execution succeeded at their own level; the export requirement failed.

C-S2's ordinary v1 and v2 outputs each contain, in order, `record-1/Ready`, `record-2/Retired`, `record-3/Ready`, `record-4/Ready`, `record-5/Retired` and `record-6/Ready`. In the sparse v2 run it first receives zero items with `page-2`, continues, receives four items with `page-3`, and finally receives two items without a cursor. The trace demonstrates the requested migration behavior in the local fixture.

## Apply the lesson without importing this fiction

For another audit, replace all schemas, behavior notes, consumers, overlap policy and expected records with authorized sources. Keep a distinction between input acceptance, allowed output shapes and consumer completion. A schema-only success cannot establish traversal completeness. Conversely, do not change an existing audit's unknown rules merely to make an executable example possible.

Missing definitions hold the dependent judgment. An unresolved response item reference remains held even for an empty sample that never exercises the item schema. Finish unrelated checks whose sources remain complete. The companion runner is intentionally limited to these authored, absolute-reference schemas; it is not a general schema comparison, network resolution or migration approval tool.
