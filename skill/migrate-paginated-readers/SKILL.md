---
name: migrate-paginated-readers
description: "Update a read-only API consumer after an endpoint or pagination change while preserving filters, bounded request scope and honest coverage reporting."
---

# Migrate a Paginated API Reader

## When to use

Use this when an existing public or authorized read-only integration stops working after an API retirement, or when a replacement endpoint changes an all-results response into pages. The goal is a working reader whose output still means what the user expects, not merely a successful HTTP response.

## Required inputs

- The current reader and its assumptions about response size and completeness
- Official provider migration documentation and the target API version
- The requested query/filter scope and whether it needs a sample or full coverage
- Request, page, record, time and response-size budgets
- Representative successful, empty, partial and error fixtures

Do not infer a service outage from one retired endpoint. Conversely, a new documented read endpoint does not grant account access or expand the permitted data scope. Stop for a new authentication or permission requirement rather than provisioning access implicitly.

## Workflow

1. **Classify the actual failure.** Record the HTTP status and bounded error body. Compare them with current official documentation. A410 retirement differs from a429 rate limit, an authentication failure, a temporary5xx response or a network restriction; the recovery action should match the evidence.
2. **Write down the old contract.** Identify whether downstream code assumes every matching ID arrived in one response, whether a total means global matches or page length, and which filters are material to the task. Find counters, exports and UI wording that depend on those assumptions.
3. **Map the replacement contract.** Verify endpoint version, parameter names, default/max page size, offsets or cursors, reachable-result caps and empty-response shape. Preserve required filters and their case sensitivity. Do not silently drop a filter because the new endpoint accepts the request without it.
4. **Choose coverage deliberately.** For a bounded gallery or sample, fetch the agreed page/record budget and label it as a sample. For full retrieval, follow the documented continuation until a proven terminal condition, subject to the user's bounds. If the provider exposes only a capped window, explain that full coverage is unavailable through that route and use a documented export/dataset only when authorized and appropriate.
5. **Validate each page and record.** Check identity types, duplicate IDs, maximum page length and consistency with reported totals where applicable. A positive total with an unexpectedly empty first page should be investigated rather than treated as no matches. When a secondary object fetch is necessary, validate the returned identity and required per-object fields; a search filter alone may not guarantee those fields.
6. **Bound and cancel work.** Apply whole-operation deadlines and response-size limits. Use modest concurrency or sequential requests appropriate to the provider. Cancel obsolete requests when the query changes. Distinguish a normal missing object from an interrupted operation; do not silently skip broad classes of errors and then claim complete coverage.
7. **Preserve provenance through selection.** Keep query, version, retrieval time, provider total, candidate-page size, records actually examined and output count. These are different quantities. If selecting records by additional eligibility rules, state those rules and count rejected or unavailable records when useful.
8. **Test the new meaning, not just status200.** Use a fixture whose global total exceeds its page length. Verify offset/cursor handling, final short page, empty results, duplicates, missing fields, identity mismatch, cancellation and budget exhaustion. Check every completeness label and export after the migration. Perform one bounded live read if available and distinguish that observation from mocked tests.

## Worked example

An old reader receives all100 matching IDs at once. Its replacement returns24 IDs by default while retaining total=100. Code that loops over the returned array still “works,” but it now processes only24% of the matching IDs.

For a task needing at most six eligible records, request one page explicitly with limit24 and offset0. Fetch details only until six eligible records are found or that page is exhausted. Report “100 total matches;24 candidate IDs in the page;8 records examined;6 selected.” Do not call those six the complete result set.

For an authorized full retrieval under a sufficient budget, offsets0,24,48,72 and96 would cover100 stable IDs if the provider documents this offset model and the result set remains stable. If records can move while paging, describe the consistency limitation or use an available snapshot/cursor contract rather than claiming a point-in-time complete export.

## Provider example and reference

On October2,2026, the Met Collection API's documented legacy `/public/collection/v1/search` returned410, while its documented `/public/collection/v1.1/search` accepted explicit offset/limit parameters. Its global total and returned Object ID count had to be treated separately. Per-object public-domain, image and date checks were still necessary for a selected-artwork task. This is a dated migration example; consult the current [official API documentation](https://metmuseum.github.io/) before implementing a new reader.

## Deliverable

Return the contract changes, implementation/test evidence, exact query scope, observed coverage and remaining limits. Preserve prior results as explicitly dated snapshots when useful; never relabel them as a successful fresh fetch after an error. Migration completion means the requested semantics and coverage are verified, not just that the new URL responds.
