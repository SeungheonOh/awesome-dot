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

### Keep the evidence ladder explicit

Use an existing authorized authentication path; synthetic fixtures can test validation behavior without provisioning production credentials. Keep raw bytes and secret material out of ordinary reports. Record only the permitted delivery identity, digest, received time, validation outcome and downstream evidence references.

Treat authentication, deduplication, persistence and processing as separate checkpoints. A receiver 200 response may establish acceptance under that endpoint’s contract, but it does not prove a downstream job committed its business action. Inspect the actual durable receipt and processing result only within the granted scope.

## Output

A bounded receipt/authentication assessment, duplicate/conflict findings, retained evidence fields and unresolved downstream status.

## Verification and limits

Check a changed byte, malformed signature, duplicate ID, conflicting body, same body/new ID and retention expiry. Do not claim replay protection from HMAC validation alone.

## References

[GitHub payload validation](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries)

## Stop and ask

Stop before replaying an event, forwarding it to a new destination, creating production secrets or changing receiver access. If exact signed bytes are unavailable, report authentication as unverified rather than validating reserialized JSON and calling it equivalent.

## Worked example

The fictional receiver receives delivery D1 with body digest H1 and a valid signature. It stores an allowed metadata receipt. A retry with D1,H1 and the same event label is classified as the same retained receipt, with no second processing action under the specified idempotency rule.

A later request reuses D1 but has digest H2. That is a conflict: retain the original receipt and investigate instead of overwriting it. Another request uses D2 with H1; the repeated body is visible, but its meaning is unresolved because delivery headers/freshness are not established by body HMAC alone.

The output distinguishes these three cases and states whether downstream completion evidence exists. This is a synthetic decision example, not a claim that any production webhook was authenticated, replayed or processed.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
