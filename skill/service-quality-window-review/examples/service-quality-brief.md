# Lantern lookup: ten-minute quality review

**Whole-window target result: undetermined.** The evidenced population contains 82 terminal noncanceled attempts: 7 errors (8.5366%) and 60 attempts lasting at most 300 ms (73.1707%). Both observed-subset comparisons miss the supplied targets, but birch's 10:04–10:06 UTC reset interval is unresolved. Unknown traffic could change either whole-window fraction. No full-window pass or failure follows from this subset alone. [Calculated result](calculation.json), fields `known_counts`, `latency`, `full_window_verdict`.

All service names, source assertions, telemetry and policies here are fictional. The export is a local exercise; this brief makes no claim about a real service.

## Contract and evidence

Review window: **[2026-09-30 10:00:00, 10:10:00) UTC**, service `lantern-lookup`, environment `exercise`, route `lookup`, expected shards amber and birch. Membership uses terminal-event time, so this is a completion cohort. Each retry is another attempt. Caller cancellations are excluded from the error and latency denominators; server failures and application deadline timeouts are errors. Latency includes successful and error attempts, measured from attempt admission to terminal event in seconds. The targets are error fraction ≤5% and fraction with latency ≤300 ms ≥75%, requiring complete observation of both shards across the window. [Supplied contract](input-contract.md).

| Source | Revision / capture | Exact locators and scope |
| --- | --- | --- |
| [Original export](telemetry.json) | `lantern-export-1`; 10:12 UTC capture | `source_manifest`, `contract`; metric snapshots and interval continuity assertions; no sampling or pagination within asserted complete spans |
| [Snapshot and span records](telemetry.json) | Same export | `snapshots/a00,a05,a10,b00,b04,b06,b10`; `spans/A-00-05,A-05-10,B-00-04,B-04-06,B-06-10` |
| [Selected logical-request records](telemetry.json) | Same export | `diagnostic_requests/r01` through `r06`; six support examples from amber, incomplete and nonrandom |
| [Calculation](calculation.json) | Exact source bytes recorded as `input_sha256` | `accepted_intervals`, `excluded_intervals`, both coverage objects, `known_counts`, `latency`, `diagnostic_ledger` |

The exact boundary snapshots and complete-observation assertions come from the fictional producer contract. They are stronger than a normal scrape's guarantees. [Real-format distinctions and official documentation](../references/telemetry-semantics.md).

## Observation coverage

Amber has 600 of 600 seconds supported; birch has 480 of 600. Counts and latency have the same supported cells in this input: **1,080/1,200 expected shard-seconds = 90%**. Every expected shard is observed simultaneously for **480/600 wall-clock seconds = 80%**. These are observation-time fractions, not fractions of total traffic. Histogram count 82 matching eligible count 82 does not fill the missing birch cell. [Coverage calculation](calculation.json), `count_coverage` and `latency_coverage`.

Birch's epoch changes from B1 at 10:04 to B2 at 10:06. The export supplies neither an exact reset time nor snapshots bracketing the reset. The value 3 at `b06` cannot recover the missing old-epoch tail or the whole two-minute interval. No zero, inferred rate or extrapolated count is assigned to this gap. This reconstruction gap does not establish downtime. The later 10:06–10:10 interval is usable under the explicit B2 continuity assertion despite the absence of intermediate snapshots. [Source](telemetry.json), `spans/B-04-06`, `snapshots/b04,b06,b10`.

## Counts and denominators

Each accepted row is a compatible end snapshot minus start snapshot. Errors and cancellations are disjoint; eligible = attempts − canceled. These rows are disjoint in shard and time. [Interval calculations](calculation.json), `accepted_intervals`.

| Shard and interval UTC | Attempts | Errors | Canceled | Eligible | Source snapshots |
| --- | ---: | ---: | ---: | ---: | --- |
| amber [10:00, 10:05) | 120 − 100 = 20 | 11 − 10 = 1 | 3 − 2 = 1 | 19 | [a00 → a05](telemetry.json) |
| amber [10:05, 10:10) | 150 − 120 = 30 | 14 − 11 = 3 | 4 − 3 = 1 | 29 | [a05 → a10](telemetry.json) |
| birch [10:00, 10:04) | 216 − 200 = 16 | 22 − 20 = 2 | 6 − 5 = 1 | 15 | [b00 → b04](telemetry.json) |
| birch [10:04, 10:06) | Unknown | Unknown | Unknown | Unknown | [b04 → b06](telemetry.json) |
| birch [10:06, 10:10) | 23 − 3 = 20 | 2 − 1 = 1 | 1 − 0 = 1 | 19 | [b06 → b10](telemetry.json) |
| Evidenced total | **86** | **7** | **4** | **82** | [Totals](calculation.json) |

Observed error fraction = (1 + 3 + 2 + 1)/(19 + 29 + 15 + 19) = **7/82 = 8.5366%**. Successful attempts = 82 − 7 = **75**. Neither 86 nor 82 is a distinct logical-request count. The calculation sums compatible counts before dividing; it does not average the four row percentages.

## Latency bounds

Interval cumulative `le` vectors for bounds `[0.1, 0.3, 1, +Inf]` seconds are `[8,15,18,19]`, `[8,21,27,29]`, `[4,10,14,15]` and `[5,14,18,19]`. Their component-wise sum is **[25,60,77,82]**. Differencing adjacent bounds gives the disjoint bins below. Every vector covers the same eligible attempts as its count row; all bucket layouts and units agree. [Histogram calculations](calculation.json), `accepted_intervals/*/latency_cumulative_le` and `latency`.

| Duration bin, seconds | Observed attempts |
| --- | ---: |
| [0, 0.1] | 25 |
| (0.1, 0.3] | 35 |
| (0.3, 1] | 17 |
| (1, +∞) | 5 |
| Total | **82** |

- Fraction ≤300 ms: **60/82 = 73.1707%**, exact for the observed population because 0.3 seconds is a bucket boundary
- p50: rank ceil(0.50 × 82) = 41, therefore **(0.1, 0.3] seconds**
- p90: rank ceil(0.90 × 82) = 74, therefore **(0.3, 1] seconds**
- p95: rank ceil(0.95 × 82) = 78, therefore **strictly greater than 1 second, with no finite upper bound supplied**

These are bounds on empirical quantiles of the evidenced population, not exact percentiles or estimates for the whole service window. No duration sum or raw duration list is supplied, so a mean is unavailable. No percentile averaging or within-bucket interpolation was used.

## Logical requests: separate and partial

The six selected request IDs contain five logical completions in the window: three successful, one error and one cancellation; one request remains unresolved. Their terminal noncanceled logical error fraction is **1/4 = 25%**. Within the same selected records, seven attempts terminate in the window: three successes, three errors and one cancellation, giving **3/6 = 50%** among eligible attempts. Neither rate estimates the full service. [Source ledger](telemetry.json), `diagnostic_requests`; [calculation](calculation.json), `diagnostic_ledger`.

Request r01 fails once and then succeeds, so two attempts become one successful logical request. Request r05's first error at 09:59:59 is outside this completion window, while its successful retry at 10:00:01 is inside. Request r06's unfinished attempt supplies no terminal count. These records are already examples of the counter population where they overlap; they are not added to it.

## Next evidence decisions

1. **Recover birch's missing interval if whole-window assessment is still needed.** Request a complete terminal-event export for [10:04,10:06), or reset-boundary records sufficient to reconstruct both epochs with the same outcome and duration population. This could resolve the unknown cell. Epoch identity alone or the post-reset count alone is insufficient.
2. **Obtain a complete logical-request ledger only if the requested SLI is changed to that unit.** It would need bounded final dispositions, retry identities, cancellation policy and completeness evidence for both shards. The six selected examples cannot answer that question.
3. **Request finer latency evidence only if a narrower p95 matters.** Compatible finer buckets or raw durations for the same accepted cells could refine the bound. A dashboard point estimate without its method and population would not supply an exact percentile.

No owner is identified in the supplied evidence. These are evidence requests for the service's telemetry custodian, not a claim that further data exists or an instruction to change the service.
