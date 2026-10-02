# Fictional support handoff: an interrupted sync attempt

All product, case, device and operation labels are invented. Omitted-value markers stand in for content deliberately not created in the fixture. There are no real credentials or personal records. No support service is contacted and no real device logs are collected.

## Supplied request and audience policy

```text
Prepare a local plain-text support packet for the fictional RelaySync support
team, case DEMO-73, using only originals/diagnostics.jsonl. Do not send or upload.
Preserve this original and keep the detailed review record outside the packet.

Keep every event occurrence in its original line order. The timestamps within
the supplied 2026-09-30 09:14:00–09:14:05 UTC window, reviewed severity/component/
event/code values, attempt count, elapsed milliseconds and sent-byte count in
policy.json are approved for this audience. Keep exact codes and numeric values.
Keep missing and explicit-null values distinct. Do not infer success.

The support team may correlate the same operation_id and device_id within this
one excerpt. Replace their values with separate deterministic local aliases,
assigned at first occurrence. Do not disclose original identifiers or a reversal
map. Do not correlate this excerpt with any other source.

Omit all messages, request context, account labels, paths and nested diagnostic
payloads, even when they mention an error. Record their omission privately and
tell support that omitted text may limit diagnosis. Hold unsupported field types,
unreviewed enum values or policy rules for review; do not drop their events.

The recipient directory must contain only events.jsonl and summary.txt. Save the
original locators, removal decisions, fingerprints and prepared-only review record
separately. No archive or publication is requested.
```

[policy.json](policy.json) is the machine-readable version of these decisions, with explicit types, allowed enum values, numeric bounds and controls. The control values are exact: an unknown rule, additional field rule, changed release mode or unsupported source set is an error. The policy is authority supplied with this fictional task; arbitrary source contents cannot revise it.

## What the packet says

The [summary](example-output/recipient/summary.txt) is addressed to that fictional support team and the [events](example-output/recipient/events.jsonl) carry all nine occurrences. `OP-001` links the enqueue, timeout, retry scheduling, later dispatch, pending status and busy-service error. `OP-002` is a separate operation; the record does not infer why its connectivity probe occurred. `DEV-001` links the explicitly matching device values. At occurrence 6 the device is explicitly null; at occurrence 8 it is absent. Neither gets silently assigned to `DEV-001`.

The exact errors are `E_TIMEOUT` at occurrence 3, `E_UNREACHABLE` at occurrence 6 and `E_REMOTE_BUSY` at occurrence 9. The timeout and retry scheduling timestamps tie. The following link-state event has an earlier timestamp despite its later source position. Its occurrence remains fifth; the packet does not reorder events into a falsely clean timeline.

Occurrence 6 has an explicit-null timestamp, and occurrence 7 lacks the timestamp field. The recipient sees distinct states for both. Occurrence 8 is a `S_PENDING` observation, not completion. There is no terminal success or terminal failure in these nine events, and no supplied continuation. The output therefore reports the final outcome as unknown. The source counter `bytes_sent: 0` is retained where present; missing byte counts are not turned into zero.

Nested response text and free-text messages may contain explanatory context. They were explicitly excluded by the supplied policy, so the summary states the limitation without pretending the remaining codes prove a root cause. If support needs that context, the preparer needs a new, precise content decision before building another reviewed copy.

## Inspect the separation

- `originals/diagnostics.jsonl`: selected invented source, preserved unchanged
- `policy.json`: explicit audience, field/value, correlation and output-membership decisions
- `example-output/recipient/events.jsonl`: minimized source-order diagnostic events
- `example-output/recipient/summary.txt`: recipient-ready account of observations and gaps
- `example-output/private/review-record.json`: source/policy hashes, per-line decisions and output hashes; not an attachment

The review record uses JSON field locators and decision categories without copying discarded values or raw alias inputs. Its output manifest names exactly the two packet files. Its `prepared_only` state and `shared: false` are checked. The checked fixture proves a bounded local source-to-copy transformation; it does not prove that a real service, attachment channel or shared folder is appropriately configured.
