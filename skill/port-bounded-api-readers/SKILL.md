---
name: port-bounded-api-readers
description: Move an authorized read-only public-data adapter between server runtimes while preserving fixed destinations, response bounds, provenance and honest cache/rate-limit guarantees. Use when publishing an existing local reader to an edge runtime.
---

# Port bounded API readers

## When to use

A working local reader must run in a different server environment, such as an edge Worker. The goal is to preserve the reader's data and safety contract while adapting lifecycle, fetch and asset-routing behavior. A successful bundle upload alone does not establish that the public-data path works.

## Required inputs

- Approved publication destination and existing deployment identity
- Current reader code, allowed upstream hosts/paths and user-input grammar
- Response schema, byte/work/deadline bounds and provenance requirements
- Cache lifetime, concurrency and retry/refusal behavior
- Target runtime's current fetch, stream, cancellation and asset-binding documentation

Keep credentials opaque in an existing authorized CLI or connector session. Do not copy raw tokens into source, logs, prompts or a public asset directory.

## Workflow

### 1. Separate the portable contract from the server wrapper

Identify pure normalization and validation functions that can run unchanged. Keep them shared with the existing local implementation. List wrapper assumptions: request/response types, connection-close events, timers, filesystem access, persistent process memory, redirect modes and static-file routing.

Define what the client sends. A metadata lookup may need one identifier; private notes and local files need not leave the browser. Reject extra query fields rather than accidentally turning a narrowly scoped reader into a general proxy.

### 2. Keep upstream destinations fixed

Construct requests from a fixed HTTPS provider origin and validated identifiers. Encode a supplied identifier as one path component. Never accept arbitrary upstream URLs, copy client authorization headers or follow a provider redirect without the intended destination policy.

Check redirect support in the actual runtime. Some server Fetch implementations do not accept the same redirect modes as Node or browsers. Where manual handling is supported, inspect the returned status and reject redirects explicitly when the contract forbids following them. Do not switch to automatic following merely to make the request succeed.

### 3. Preserve streaming bounds and cancellation

Check declared content length when present, but also count actual streamed bytes. Stop at the maximum before concatenating or parsing. Reject malformed UTF-8 and unexpected response structure. Apply a deadline covering retrieval and body consumption, with cleanup in every exit path.

Translate cancellation carefully. A client abort may cancel its individual lookup, but should not necessarily abort a shared in-flight feed request serving other clients. Document the chosen behavior. Cancellation cannot undo an identifier already received by a provider.

### 4. Reassess state lifetime and public exposure

An in-memory cache or cooldown in one local process is not a global edge rate limit. State may be per isolate, evicted, duplicated across regions or absent on a cold start. Name the scope accurately and use a separately authorized durable/global mechanism if the task requires stronger guarantees.

Bound cache entries and lifetime, preserve original observation times on cache hits, and reject negative-age clock anomalies. Deduplicate concurrent fixed-feed refreshes where useful. Provider refusals should produce a bounded cooldown and a clear retry-later state, not aggressive automated retries.

Public deployment changes who can call the adapter. Same-origin checks help restrict browser use but do not authenticate direct clients. Keep fixed destinations, small responses and no privileged capabilities; explain relevant quota/billing limits without promising cost-free unlimited use.

### 5. Test the target route, not just the shared model

Use unit tests for destination construction, identifier mismatch, extra query fields, method/origin rejection, streamed over-limit bodies, timeouts, provider refusals, cache expiry and concurrent requests. Mocks should assert important options rather than silently accepting every fetch argument.

Then test the deployed runtime with a small authorized public fixture. Confirm the page loads, the API reaches the expected provider, real timestamps and provenance render, and downloads contain the same normalized result. A mock that accepts an unsupported runtime option can give a false pass.

Verify that API routes reach the Worker while static assets use the intended asset path. Record the actual deployment version and returned public URL. Do not guess a URL from a project name and call it live.

### 6. Reconcile and deliver

Preserve the prior working artifact and local startup path. Update the release catalog only after the public page and its substantive workflow are verified. Re-run aggregate checks against the final source, package it, and test a freshly extracted copy when producing a downloadable collection.

Report unresolved limitations precisely. A live single-fixture test is not load testing, global rate-limit verification or proof of every provider response shape.

## Worked example

A local paper-metadata reader requests one DOI at a fixed provider path. It has a one-megabyte streamed limit, a 20-second deadline, a one-hour cache and a one-request-at-a-time cooldown. Its initial edge port passes mocked tests, but the deployed endpoint rejects the chosen redirect mode.

Inspect the runtime's documented behavior, change the wrapper to manual redirects and reject non-success statuses without following them. Keep the DOI validator and normalizer unchanged. Add a regression for the required fetch option and redirect rejection, then redeploy.

A live lookup returns two known public records with observation timestamps. Download the review and citation export, verify their identifiers and author fields, and confirm a synthetic private note appears only in the review. Describe the cache/cooldown as isolate-local. The successful lookup does not prove a global provider request ceiling.

## References

- [Cloudflare Request API](https://developers.cloudflare.com/workers/runtime-apis/request/)
- [Cloudflare static asset bindings and routing](https://developers.cloudflare.com/workers/static-assets/binding/)

Use the equivalent official documentation for another target runtime; do not assume complete Fetch API behavioral parity.
