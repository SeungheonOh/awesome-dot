---
name: validate-webhook-receipt-evidence
description: "Check an authorized webhook receiver or selected delivery for raw-body authentication, duplicate semantics and minimized receipt evidence."
---

# Validate webhook receipt evidence

## When to use

An integration needs to determine what a received webhook actually proves before treating it as a successful business action.

## Required inputs

- Provider signature specification and authorized receiver scope
- Raw request bytes and headers through an approved secure handling path, or synthetic test fixtures
- Existing permitted validation capability and the intended metadata/retention policy

## Workflow

1. Establish which bytes the provider signs. For GitHub payload signatures, verify the exact raw body before parsing or storage using the existing approved secret-handling capability; do not request secrets in ordinary chat or print them.
2. Validate signature shape and use a timing-safe comparison. Bound payload size and reject invalid authentication before committing a receipt. Re-serializing parsed JSON changes the signed bytes.
3. Separate body authenticity from header identity, freshness and downstream completion. A valid GitHub body HMAC does not itself authenticate every event/delivery header or prevent replay.
4. Inspect idempotency under the receiver’s stated retention scope. Matching retained delivery ID/body/event can be a duplicate; a changed payload under the same ID must not overwrite evidence. Same body under a new ID is ambiguous, not automatically malicious.
5. Retain only the authorized metadata and test with synthetic payloads where possible. Distinguish receiver acceptance, persistence and completed downstream work. Do not forward or replay real events unless that action and destination are separately authorized.

## Output

A bounded receipt/authentication assessment, duplicate/conflict findings, retained evidence fields and unresolved downstream status.

## Verification and limits

Check a changed byte, malformed signature, duplicate ID, conflicting body, same body/new ID and retention expiry. Do not claim replay protection from HMAC validation alone.

## References

[GitHub payload validation](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)
