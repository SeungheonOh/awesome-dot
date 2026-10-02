# Lantern lookup: supplied review contract

Everything in this example is fictional, including the service, telemetry, attestations and policy. The decision is whether the supplied evidence establishes the agreed service-quality targets for one ten-minute window. It does not request a repair, chronology, benchmark or live investigation.

## Window and expected population

- Service `lantern-lookup`, environment `exercise`, route `lookup`, shards `amber` and `birch`; these shards are an exhaustive, disjoint ownership partition for attempts
- Window `[2026-09-30T10:00:00Z, 2026-09-30T10:10:00Z)`, selected by attempt terminal-event time; no timezone conversion or clock uncertainty in this fictional export
- Atomic cumulative snapshots at `t` contain all qualifying terminal events strictly before `t` in that producer epoch; both endpoints are required for an exact interval delta
- Evidence captured at `2026-09-30T10:12:00Z`, after the producer's stated two-minute finalization delay; no pagination, row limit, downsampling or sampling for the stated complete metric intervals
- No late corrections or lost instrumentation are asserted within a complete interval. Reset/epoch continuity is separately required. These are supplied facts in the exercise, not properties the calculator can authenticate

## SLI and target policy

Every terminal attempt has exactly one outcome. `success` means a successful application reply; `error` means a server failure or application deadline timeout; `canceled` means a caller cancellation. Other states cannot be silently mapped. Errors and cancellations are disjoint.

Primary error SLI: terminal error attempts divided by terminal noncanceled attempts, including each retry as another attempt. Cancellations are counted separately and excluded from both primary numerator and denominator. An unfinished attempt has no terminal observation yet and does not enter this completion cohort. The result says nothing about all attempts admitted during the window.

Primary latency SLI: the fraction of those same terminal noncanceled attempts whose duration is at most 0.3 seconds. Measure from attempt admission to its terminal event, including the duration of error attempts, excluding canceled and unfinished attempts. Durations are finite and nonnegative, measured in seconds. Equal bucket boundaries and the same observation population apply to every pooled interval. Histogram membership and outcome recording are atomic under this fictional contract.

Targets apply to the entire window and both expected shards: error fraction `<= 0.05`, and latency fraction `>= 0.75`. A target verdict requires 100% evidenced cohort-time coverage for the relevant counts and histogram, plus their population agreement. An incomplete result is `undetermined`; still show observed-subset comparisons. No longer SLO horizon, error-budget policy or traffic upper bound is supplied.

Quantiles are descriptive. Use the empirical nearest-rank convention: rank `ceil(q × n)` for `0 < q <= 1`. Report the containing bucket interval, not an assumed within-bucket distribution. Do not average the shard percentiles.

## Source locators and continuity

All input locators refer to [telemetry.json](telemetry.json), revision `lantern-export-1`. A locator such as `snapshots/a05` or `spans/B-04-06` identifies the corresponding ID within that file. `contract` and `source_manifest` record the policy and export provenance.

| Span ID | Snapshot IDs | Producer assertion | Disposition before arithmetic |
| --- | --- | --- | --- |
| A-00-05 | a00 → a05 | amber epoch A1 continuously counted; complete | Eligible for exact delta |
| A-05-10 | a05 → a10 | amber epoch A1 continuously counted; complete | Eligible for exact delta |
| B-00-04 | b00 → b04 | birch epoch B1 continuously counted; complete | Eligible for exact delta |
| B-04-06 | b04 → b06 | epoch changed, no boundary samples or exact reset time | Unknown; neither subtraction nor reset-value addition recovers the whole span |
| B-06-10 | b06 → b10 | birch epoch B2 continuously counted; complete | Eligible for exact delta despite no intermediate snapshot |

The birch gap is a reconstruction gap. It does not prove the service was unavailable. The new-epoch starting value cannot supply the missing pre-reset tail or establish exact coverage for the two-minute interval.

## Separate diagnostic logical-request ledger

The export includes six deliberately selected request IDs from amber. This is a convenience sample of support examples, not a complete ledger, random sample or second measurement to add to the counters. All attempts for those selected IDs known at the capture are listed, including an earlier out-of-window attempt and one unfinished attempt. Logical IDs are scoped to `lantern-lookup/exercise`; attempt IDs are unique in that scope.

For this diagnostic ledger only, a request's final disposition is supplied by the application, not inferred from its last failed attempt. A logical completion in the review window is `success`, `error` or `canceled`; an unresolved request has no final timestamp. Count logical error fraction over terminal noncanceled logical completions. It is a sample description and cannot replace the primary attempt SLI. A retried request that finally succeeds illustrates why the units differ.
