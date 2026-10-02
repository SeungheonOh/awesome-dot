---
name: authenticated-webhook-receipt-ledger
description: Build a small server-backed GitHub webhook receipt ledger with raw-body HMAC validation, bounded SQLite retention, authenticated metadata inspection, and real local HTTP tests. Use for inbound observability tools, not webhook forwarding or automated event execution.
---

# Authenticated webhook receipt ledger

Build an actual receiver and viewer, rather than a dashboard populated with illustrative deliveries. Keep receipt evidence separate from claims about sender identity, event freshness, downstream processing or successful business actions.

## Scope and prerequisites

The worked design uses Node24+, built-in SQLite, and an ordinary browser frontend. Run integration tests against an ephemeral loopback server with synthetic payloads and temporary test credentials. Do not register a real repository webhook, expose a public endpoint, provision production secrets or deploy the service without the owner's explicit authorization.

Use two distinct secrets: one for GitHub payload HMAC and one for read-only viewer access. Never bundle real secrets, credential stores or databases in a deliverable. Refuse startup if required configuration is absent. Length checks catch obvious mistakes but do not prove entropy; owners should provision secrets through their approved secret manager.

References: [GitHub payload validation](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries), [GitHub webhook best practices](https://docs.github.com/en/webhooks/using-webhooks/best-practices-for-using-webhooks), [Node SQLite API](https://nodejs.org/download/release/v22.13.1/docs/api/sqlite.html).

## Build sequence

1. Specify the stored evidence first. Prefer a narrow summary: repository name, action, ref, issue/PR number and state, merged flag, and commit count. Keep the delivery ID, event header, raw-body digest and server receipt time separately. Avoid raw bodies, headers, commit messages, titles and user profiles unless the user needs and authorizes them. Selected metadata can still be private; do not label it anonymous.
2. Authenticate exact bytes before parsing JSON or writing storage. Validate the `sha256=` signature shape, compute HMAC-SHA256 over the unchanged body, and use a timing-safe comparison. Bound body size, headers and request duration. Do not verify a reserialized JSON object: whitespace and byte encoding are part of the signed payload.
3. Treat headers honestly. GitHub's HMAC covers the body, not the event/delivery headers or freshness. A valid payload signature is not proof that every accompanying header is authentic, and does not prevent replay. Do not execute instructions or follow URLs from incoming content.
4. Define retry semantics explicitly. A retained delivery ID with matching body digest and event header is idempotent. A reused ID with different content/event is a conflict and must not overwrite the old receipt. An identical body under a new ID may be a legitimate event or replay; expose a repeated-body flag rather than silently deciding its meaning.
5. Use parameterized SQLite statements and a transaction around insertion/retention changes. Give receipts a monotonic sequence for pagination. Keep only a bounded number of newest records, and explain that deduplication only covers retained IDs. Ordinary deletion is not secure erasure, and SQLite files are not encrypted merely because the viewer is authenticated.
6. Separate ingest authorization from viewer authorization. Protect metadata APIs with the viewer secret; keep tokens in browser memory rather than localStorage. Serve assets from an exact allowlist, set no-store and restrictive browser headers, and omit permissive CORS. Default to loopback binding. A public deployment additionally needs reviewed HTTPS ingress, rate controls, host protection and secret provisioning.
7. Build the viewer against the real API. Start empty and label missing server setup; never substitute synthetic deliveries after a request failure. Include retained counts, UTC receipt time, event filtering, stable cursor pagination, detail inspection and an explicit metadata export. Render all metadata as text, not HTML.
8. Guard asynchronous UI state. Lock increments a request-generation token, clears the viewer secret and visible metadata, and invalidates in-flight responses. A delayed success cannot reopen the locked view. A failed refresh should produce an accurate error without fabricating a fresh receipt list.
9. Export only the current selected metadata view, with a privacy notice. Do not add outbound forwarding, retry-to-arbitrary-URL or event execution as incidental features; those expand both authorization and attack surface.

## Tests before calling it functional

Run real HTTP requests against the actual server and database, using temporary credentials and a temporary database. Verify invalid HMAC writes nothing; a changed byte invalidates an otherwise correct signature; viewer requests without the correct token fail; malformed/oversized payloads are rejected; duplicate and conflict outcomes are distinct; and same-body/new-ID behavior is visible.

Exercise pagination beyond one full page, event filtering, invalid cursor/filter inputs, static-route traversal rejection, response headers, restart persistence and retention pruning. Verify forbidden fixture fields are absent from API/export output and the stored database. Close the server and remove only the test-owned temporary directory afterward.

Simulated-DOM checks should cover no unsolicited requests, login failure/recovery, escaped metadata, detail close, export, and Lock during an unfinished refresh. These do not establish real browser layout or an actual GitHub-to-server delivery.

## Worked outcome

Webhook Ledger accepted105 synthetic signed deliveries through a real loopback HTTP server, paginated them100+5 without duplicate IDs, and preserved them across a database reopen. Tests passed HMAC rejection before storage, viewer authentication, conflict handling, repeated-body detection, payload bounds, private-field omission and bounded retention. Its DOM tests passed text-only rendering and stale-response suppression after Lock.

The service was not connected to a real GitHub webhook or publicly deployed. No production credentials were created, no external events were replayed, and public ingress/device-browser behavior remained unverified. Its single-process synchronous SQLite design is intended for a small local tool, not a distributed queue or a high-throughput service.

## Delivery

Ship the server, frontend, setup instructions and test commands separately from a skills-only repository contribution. Explain which node/runtime is required, which secrets the owner must provide, where metadata persists, and which integration/deployment steps remain. Do not publish a static-only deployment configuration that makes the frontend appear to be a functioning server-backed app.
