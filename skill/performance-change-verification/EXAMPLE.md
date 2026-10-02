# A faster observation summary that still counts occurrences

The aggregate candidate met the exercised contract and took less elapsed time than the repeated-scan baseline in every measured batch block. The tiny in-memory JSON comparison was noisy and does not establish a reliable small-input benefit. The last-record control was actually measured and was usually quicker, but it loses required occurrences and is rejected regardless of timing.

These are real local measurements of original fictional data, not authored duration fixtures. They describe two brief attempts on one shared machine, not a production service, a population of machines, human time saved, or dot productivity.

## The task and its contract

Given observation records and an ordered request list, return one summary for every request occurrence. The fields are the unchanged string `id`, total `matches`, number of known values `known`, and sum `total`. Missing or null values are unknown; integer zero is known. The total is null only when no known values exist. Both duplicate observations and repeated requests count. A known sum of zero must remain distinguishable from unknown.

[The contract](example/contract.json) was written before timing, including explicit expected outputs. It exercises distinct `07` and `7`, upper/lower case, an empty string ID, missing IDs, empty inputs, duplicate records, repeated requests, unknowns, zeros, negatives and cancellation to zero. Inputs are already valid; validation is outside both measured boundaries. Invalid types, floats, concurrent callers and a remote protocol are outside this example.

[The implementation](example/summary.py) contains three local functions:

- `baseline` scans all records for each request
- `candidate` aggregates all occurrences by exact ID once per invocation, then emits summaries in request order. Every timed call includes constructing this index; no persistent cache is reused
- `wrong_last_record` indexes each ID to only its last record. This tempting shortcut silently discards earlier occurrences

The wrong control returns one match and total 3 for `07`, where three occurrences, three known values and total 6 are required. It also changes `cancel` from two known values totaling zero to one value totaling 2. Its exact four row mismatches are saved in each run's `correctness.negative_control_differences`. Speed cannot repair these failures.

For each accepted implementation, the executed gates were three explicit cases, all 259 record sequences of length zero through three over six diagnostic observations, both timing workloads, and six metamorphic checks. The broader oracle selects matching records and reduces known values without using the candidate's aggregate index. Input mutation and exact output fields/types were also checked. This covers a bounded domain; it is not a proof for every possible input.

## Workloads and timing boundaries

[workloads.json](example/workloads.json) preserves the exact raw data:

| Workload | Record occurrences | Request occurrences | Calls per timed batch |
| --- | ---: | ---: | ---: |
| tiny | 12 | 10 | 100 |
| batch | 1,812 | 250 | 2 |

The larger input adds 120 fictional IDs with 15 observations each and requests those IDs twice in a fixed permutation. Its duplicate-heavy shape favors doing aggregation once. No usage-frequency evidence justifies weighting these two inputs into a single overall result.

Each workload and boundary used 12 blocks. Every block measured all three variants, using each of the six possible variant orders twice. This was deterministic order balancing, not randomization. Each variant received one untimed warmup for each workload/boundary; correctness checks had already touched the code and inputs. All measurements within an attempt used the same warm Python process with inherited automatic GC enabled.

- **Algorithm only:** parsed lists through construction of the returned list. Index construction, allocation, common function-wrapper and loop overhead are included. Parsing and serialization are excluded
- **In-memory JSON pipeline:** pre-existing canonical UTF-8 JSON bytes through decoding, the summary function, canonical JSON encoding and UTF-8 output bytes. There is a fresh parse per call. File reading/writing, transport, startup and validation are excluded

The second boundary is an end-to-end measurement of that named in-memory pipeline only. It is not application or service end-to-end latency. Output checks and hashing occur outside the timer. Within a timed batch, all calls execute, and the last output is checked afterward; correctness preparation separately checks every variant/workload. The functions have no external effects or persistent cache.

No install or build was performed. In the successful attempt, separately recorded loading of the contract/workload files took 0.677 ms and correctness checks took 98.257 ms. Interpreter startup, module imports, authoring/generating the workload, warmup and evidence formatting/readback were not individually timed. These preparation observations are not a full adoption or setup-cost estimate.

## Observed results

The successful measurement record is timestamped 2026-10-02 at 04:54:58 UTC, after its initial correctness preparation. The harness through sampling and summary construction took 0.875 seconds; the command including readback took about 1.39 seconds. Values below are microseconds per call: elapsed batch time divided by its fixed call count, then minimum / median / maximum over 12 batches. They are not individually timed request latencies or confidence intervals.

| Workload and scope | Baseline µs | Correct candidate µs | Wrong control µs, rejected |
| --- | ---: | ---: | ---: |
| tiny, algorithm | 4.174 / 4.207 / 4.546 | 2.710 / 2.758 / 23.421 | 2.138 / 2.161 / 2.652 |
| tiny, JSON pipeline | 15.092 / 15.436 / 46.055 | 14.015 / 14.346 / 34.980 | 13.250 / 13.618 / 34.287 |
| batch, algorithm | 10,189.424 / 10,330.031 / 12,633.272 | 272.010 / 283.469 / 335.149 | 98.558 / 101.821 / 127.121 |
| batch, JSON pipeline | 10,671.636 / 11,160.676 / 13,269.466 | 800.961 / 836.423 / 1,156.866 | 614.375 / 645.078 / 720.585 |

On the batch input, the median matched-block baseline/candidate ratio was 36.62 for the algorithm and 13.29 for the JSON pipeline. The candidate took less elapsed time in all 12 blocks at both boundaries. Those are observed ratios for this workload and environment, not fixed requirements, hardware-independent guarantees, or expected deployment benefits. They do not account for memory; the candidate retains one aggregate per distinct ID, and peak memory was not measured.

On the tiny input, the candidate took less elapsed time in 10 of 12 algorithm blocks and 9 of 12 pipeline blocks. The median matched-block pipeline ratio was 1.061, but the observed paired ratio ranged from 0.440 to 2.542. The slow candidate algorithm batch (23.421 µs per call) remains in the data. These small, noisy comparisons do not justify a reliable tiny-input improvement claim. No sample was removed.

[run.json](evidence/run.json) contains all 144 raw samples, their execution order, loops, output hashes and contract status, plus the exact source/input manifest, environment and computed summaries. There are 96 accepted-variant samples and 48 rejected-control samples. Repeated calls inside a sample are not additional independent samples.

## Initial attempt and retry

The first measurement record is timestamped 04:54:07 UTC and contains all 144 timing samples and in-memory correctness/readback checks. Its final saved-object comparison failed because order permutations were tuples in memory and lists after JSON roundtrip. Only the representation of `design.orders` was corrected; the summary implementations, contract, workload, timing boundary, sample count and loop count were unchanged. The retry was required by a serialization failure, not by a performance result.

[initial-run.json](evidence/initial-run.json) retains every initial sample. Its median microseconds per call were:

| Workload and scope | Baseline | Candidate | Wrong control, rejected |
| --- | ---: | ---: | ---: |
| tiny, algorithm | 4.326 | 2.933 | 2.318 |
| tiny, JSON pipeline | 16.699 | 14.574 | 13.521 |
| batch, algorithm | 10,306.355 | 285.973 | 102.725 |
| batch, JSON pipeline | 11,020.184 | 816.707 | 624.913 |

The initial run also showed a lower candidate time in all 12 batch blocks at both boundaries. Its tiny pipeline candidate was lower in 11 of 12 blocks, compared with 9 of 12 in the retry. Both attempts support keeping the small-input conclusion cautious. They are separate nearby attempts on the same host, not independent experimental replications.

The exact initial harness can be reconstructed from the current source with the single reverse replacement in [initial-harness-change.json](evidence/initial-harness-change.json). That file records both complete-file SHA-256 values; reconstruction was checked against the retained initial source. No duplicated implementation is needed in this packet. The verification record describes what was rechecked.

## Environment and limits

Execution used CPython 3.12.14 on Linux x86-64. The guest reported an AMD EPYC 9V74 CPU and nine visible/affinity CPUs. The counter reported `clock_gettime(CLOCK_MONOTONIC)` with 1 ns resolution; nanosecond units do not establish nanosecond measurement accuracy.

This was a shared environment with intermittent LibreOffice/Poppler document-rendering activity during the broader collection period. Exact overlap with individual samples was not measured. CPU frequency, scheduling, contention, thermal state, page cache and allocator state were not controlled. The host was not isolated or dedicated, and no cause is assigned to a particular outlier.

No cold-cache or fresh-process performance comparison, peak-memory measurement, CPU-time measurement, sustained throughput test, tail-latency study, concurrency test, production profiling, network operation, external account or service, install, UI action, or deployment was performed. Neither attempt establishes a production benefit, dot effectiveness, human time savings, financial savings or a universal speedup threshold.

The supported local decision is to retain the correct aggregate implementation as a candidate for this bounded batch operation, reject the last-record control, and keep a production or small-input adoption decision open if it requires evidence beyond these measurements.
