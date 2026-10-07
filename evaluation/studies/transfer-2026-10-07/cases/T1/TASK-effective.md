# Reconcile the relay metering extract

Fictional, offline engineering task. Juniper Relay's deployment-cost dashboard is being rebuilt after an exporter interruption. Produce `output/report.sql` and `output/reconciliation.json` from the supplied sources. You have 1800 seconds. Use only Python's standard library and SQLite; no network, installs, credentials, production access, or external writes. Read only this packet and an explicitly supplied guide package, if any. Keep inputs unchanged; scratch work belongs in `tmp/`.

The delivery contract below defines the business rules and output fields. Choose any correct implementation. This is an observed-extract report, not an assertion that the entire business population was supplied. Do not fabricate rows, allocate unexplained differences, or use control totals to backfill event amounts.

## Sources and precedence

- `inputs/metering.sqlite`: fixed source tables, not a production connection
- `inputs/schema.sql`: declared table/column definitions; IDs and coverage keys are unique
- `inputs/ledger.json`: exactly the same source rows in JSON, with explicit column order
- `inputs/parameters.json`: the one evaluated reporting interval and as-of cutoff
- `inputs/source-policy.md`: owner-approved definitions, coverage meaning, and control provenance

The policy and source rows are authoritative together. All timestamps are fixed-width UTC; money is signed integer cents. No currency conversion is authorized. SQL target: SQLite 3.40 or newer, the built-in scalar/aggregate/window functions listed in `inputs/allowed-functions.txt` only; no extensions, file functions, table-valued functions, PRAGMAs, scripts, attached databases, or mutable statements.

## SQL output

Return one read-only query accepting `:report_start`, `:report_end`, and `:as_of`. The evaluator uses the public parameter values and a protected copy of the supplied database. At most 100 result rows, 64 KiB SQL, 10 million SQLite VM steps, and five seconds are allowed. CTEs, subqueries, alternative join strategies, column order and row order are all accepted. No query plan or particular keywords are required.

One row per observed eligible workload; no rows for absent workloads or for empty control partitions. Required columns, exactly once each:

- `workload_id`, `tenant`, `currency`: text
- `base_cents`: integer from the workload
- For each prefix `charge` and `credit`: `_rows`, `_null_rows`, `_known_subtotal_cents`, `_total_cents`, `_total_known`
  - rows/null_rows count eligible same-currency events allocated to that workload
  - known_subtotal sums non-null allocated amounts, or 0 if there are none; this may be only a partial subtotal
  - total_cents is that subtotal only when the stream's amount is known under the policy; otherwise SQL NULL
  - total_known is integer 1 or 0 matching that determination
- `net_cents`: base + charge total + credit total when both totals are known, otherwise SQL NULL

All numeric fields except explicitly nullable totals must be integers. Zero is a known value; NULL means unknown here.

## Reconciliation JSON

Use at most 256 KiB of UTF-8 JSON, with unique object keys and finite numbers (non-integer numbers must be representable as finite IEEE-754 binary64 values). Supply ordinary regular output files, not symlinks.

JSON object with `scope` equal to `observed_extract`, `parameters` copied from the public parameter file, and the following arrays. Extra explanatory fields are allowed. Arrays can be in any order, but required natural keys must be unique. Every control partition/feed pair must appear, even a complete-empty partition. `null` represents an unknown amount; do not substitute a subtotal.

`partitions`, keyed by tenant/currency:
- tenant, currency, observed_workloads, expected_workloads, missing_workloads
- observed_base_cents, control_base_cents, base_delta_cents
- population_complete (JSON boolean)
- known_net_workloads, unknown_net_workloads, known_net_subtotal_cents
- observed_net_cents (sum of all observed workload net values only if each is known; otherwise null)
- full_net_cents (observed net only if population_complete; otherwise null)

missing_workloads = expected − observed. base_delta_cents = observed − control. population_complete requires a complete extraction declaration and agreement with both population controls. A complete-empty partition has 0 known/unknown counts and 0 subtotals/totals.

`feed_checks`, keyed by stream/currency, where stream is `charges` or `credits`:
- stream, currency, observed_rows, observed_null_amount_rows, observed_known_subtotal_cents
- control_rows, control_null_amount_rows, control_known_subtotal_cents
- rows_delta, null_rows_delta, known_subtotal_delta_cents (all observed − control)

Include every eligible source event here, even one excluded from the workload report. A known subtotal excludes null amounts; it is not the feed's true monetary total when nulls exist.

`exceptions`, keyed by stream/event_id: every eligible event that cannot be allocated to this observed cohort, with stream, event_id, workload_id (possibly null), currency, amount_cents (possibly null), reason. Classify in this precedence order: missing_key, orphan_key (key absent from the entire workload extract), outside_cohort (workload is present but ineligible), currency_mismatch. Do not list filtered-out pending, future-effective, or post-cutoff events as exceptions.

`unknowns`, keyed by workload_id/stream: every eligible workload stream whose total is unknown, with workload_id, stream, reasons. reasons is the complete set of applicable codes: missing_coverage, partial_coverage, null_amount, currency_mismatch. Missing and partial coverage are mutually exclusive. A currency mismatch affects the corresponding known workload stream even though the mismatched event is not allocated.

## Acceptance

Checks cover safe bounded execution and schema, cohort, known subtotals and null handling, per-stream complete-zero versus unknown totals, signed net values, source dispositions, explicit unknown causes, population/feed control differences, observed-versus-full scope, and complete-empty behavior. All required facts and rules are in this packet. Optional explanatory prose is not mechanically rated; no phrase or style from a guide is required. Do not claim to have queried a live system or repaired the missing data.
