---
name: reconcile-identifier-lookups
description: Resolve a bounded list of identifiers through a named read-only metadata service while preserving every input row, duplicate, failure and source timestamp. Use for DOI or registry lookup reviews, not fuzzy research discovery or validation of the underlying claims.
---

# Reconcile identifier lookups

## When to use

Use when a person has a list of identifiers and needs a reviewable metadata result rather than a best-effort list of successes. The useful deliverable is a row-by-row reconciliation: what was found, what was not completed, and what the provider actually supports.

## Required inputs

- Original identifiers and their stable row positions
- The intended registry or provider, its identifier rules and read-only endpoint
- Fields needed for the review and intended export format
- A finite batch size, request deadline and response-size bound
- Whether sending these identifiers to that provider is within the user's authorized task

Use only the requested provider unless another source is authorized. A registry miss is not evidence that the identifier does not exist elsewhere. If the identifiers expose private projects, people, account records or unpublished work, resolve the sharing boundary before submitting them.

## Workflow

### 1. Preserve the input before normalization

Retain the original text and row number. Normalize only equivalences supported by the identifier scheme. For a DOI, a supported `doi:` prefix or DOI resolver URL can be separated from the identifier, and case can be normalized for matching. Do not silently remove trailing punctuation: it may be part of the DOI suffix. Ambiguous prose citations should be marked for review rather than guessed into identifiers.

For resolver URLs, verify the hostname and reject unexpected credentials, ports, queries and fragments unless the format explicitly supports them. Decode the path once and validate the resulting identifier. Never accept an arbitrary pasted URL as the request destination.

Record invalid rows without dropping them. Deduplicate requests by normalized identifier, but retain duplicate input rows pointing to the original occurrence. The number of reviewed rows should still reconcile to the submitted nonempty rows.

### 2. Establish the provider contract

Read current official endpoint, access and rate-limit documentation. Distinguish public metadata access from paid or authenticated access. Do not introduce an email address or API key solely to obtain a more generous request pool.

Build requests from a fixed provider origin and encoded identifier. Decide how redirects will be handled; refusing them with a clear result is safer than silently following an unbounded destination. A changed identifier or provider needs explicit reconciliation, not a fabricated exact match.

Set the batch limit, request count, concurrency, cooldown and timeout before execution. Respect response-specific limits and refusal instructions. With a single-request public pool, serial requests and a conservative gap are preferable to a large concurrent fan-out.

### 3. Keep an outcome for each attempted lookup

Distinguish at least found, malformed input, duplicate, provider miss, service error, cancelled and not attempted. Preserve HTTP status or a bounded useful error, source URL, observation time and cache provenance where available.

Bound response bytes while reading, not only through Content-Length. Decode strictly and validate the response envelope and returned identifier before accepting metadata. An HTTP 200 response for a different record is a mismatch, not success. Trim or omit fields deliberately and disclose meaningful truncation; do not pass through arbitrary HTML into a rendered page.

Stop or pause according to the provider's refusal. Do not convert a rate limit into “not found,” change network identity, or silently switch registries. A later authorized retry should retain earlier outcomes and avoid repeating successful requests unnecessarily.

### 4. Keep cancellation and editing coherent

Associate the batch with a generation or equivalent ownership token. When the user stops, replaces the input or clears the review, cancel the active request where supported and invalidate older completions. Completed results may remain, but queued and active rows need an explicit incomplete status.

Cancellation prevents further local work; it does not undo identifiers already received by a provider. Test a late response after cancellation and after starting a replacement batch. It must not overwrite the newer view or become exportable as evidence for different input.

### 5. Review metadata without overstating it

Show missing fields as unknown or not supplied. Preserve date precision: a year or year-month must not acquire an invented day. Keep publication dates distinct from lookup timestamps and source record update dates.

For scholarly metadata, title, authors, publisher and DOI do not verify the paper's conclusions, peer review, authenticity, current availability or retraction status. An absent correction field only means no such field was returned. Labels such as “verified paper” require different evidence.

When displaying externally supplied strings, use text nodes or an appropriate safe representation. Linking a DOI resolver does not authorize fetching its full text or following every linked resource.

### 6. Export and reconcile

Export all input-row outcomes alongside selected metadata and provenance. Separate the original input from normalized identifiers. Preserve successful rows, duplicate links, misses, cancellation and unattempted rows; do not export only the successes under a misleading “complete” label.

Before delivery, check that each submitted row appears exactly once, duplicate references target an existing original row, and every successful record matches its requested normalized identifier. Tie the export to the current reviewed input; edits should invalidate an earlier export until reconciled.

If the artifact will be reused, state its schema, retention behavior and how to refresh it. A cached observation should retain its original timestamp, not masquerade as a new provider response.

## Worked example

A local DOI reviewer accepted these three nonempty lines:

1. `10.1038/nphys1170`
2. `https://doi.org/10.1038/NPHYS1170`
3. `not-a-doi`

The first two normalize to one DOI. The review retains three rows: one lookup, one duplicate referring to line 1, and one malformed-input result. Only one provider lookup is needed. If Crossref returns 404, line 1 becomes “not found in Crossref”; neither the duplicate nor the malformed row should disappear, and the result must not claim global nonexistence.

An actual local-service check on October 3, 2026 at 10:36:18.965 UTC requested `https://api.crossref.org/works/10.1038%2Fnphys1170`. Crossref returned HTTP 200 for the exact DOI, title “Measured measurement,” author Markus Aspelmeyer, container Nature Physics and publication date parts `[2009,1]`. The review kept year-month precision and a separate observation timestamp. No full text or abstract was retrieved, and this result did not establish the article's claims or retraction status.

The exercised implementation used Node 24.19, one upstream request at a time, a 1.1-second gap, a 20-second deadline, a 1 MB streamed-body limit and a 100-entry one-hour memory cache. Local tests used original synthetic records to check mismatched DOI responses, registry 404, rate-limit pause, oversized responses, timeout recovery, duplicate conservation, literal rendering and cancellation races. Real provider access through the local service succeeded; simulated-DOM tests did not prove real-browser layout or a user's completed download. These limits describe that implementation, not mandatory values for every provider.

## Completion evidence

Return the reconciled artifact, attempted and unattempted counts, provider and lookup times, any retryable failures, and the exact remaining verification boundary. Do not repeatedly query unchanged successful records merely to make the result appear fresher.

## References

- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/): metadata coverage and endpoint use
- [Crossref access and request limits](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/): choose a supported access pool and current limits
