# Monthly billing reconciliation repair

`report.sql` is one read-only SQLite statement accepting `:report_start`, `:report_end`, and `:as_of`.

## Definition and repair

The supplied `TASK.md` defines the complete fictional invoice cohort. Eligible invoice lines belong to issued invoices dated within the half-open reporting interval, with invoice posting timestamps at or before the UTC as-of timestamp. The output grain is invoice month, customer region, product family, and currency. Distinct invoices are counted separately within each bucket.

Each event table is reduced independently to one row per line before joining to eligible lines. This prevents cross-event multiplication. Left joins retain lines without events; absent events contribute integer zero under the task's complete-fixture contract. Adjustment approval, receipt settlement, and fulfillment posting statuses are applied alongside inclusive effective-date and posting-time cutoffs. Event dates are not constrained to the invoice month. Signed corrections, refunds, and returns remain signed, with no caps or floors. Currencies remain separate.

Schema and relationships come from `inputs/schema.sql`; the source rows are `inputs/billing.sqlite` and `inputs/ledger.json`. Observed primary keys are unique, all referenced keys exist, and source fields are non-null. All seven SQLite tables matched the corresponding JSON rows exactly. Confirmed source counts: 12 customers, 9 products, 244 invoices, 689 lines, 1,009 adjustments, 1,381 receipts, and 1,060 fulfillments.

## Executed verification

Executed on the supplied fictional fixture with Python's standard-library SQLite 3.53.1. An independent Python calculation accumulated base lines and events directly into report buckets from the JSON ledger. Every grouping key and all nine measures matched the query exactly in all supplied scenarios.

| Scenario | Report interval | As of (UTC) | Buckets | Eligible lines | Eligible adjustments / receipts / fulfillments |
|---|---|---|---:|---:|---:|
| quarter_close | 2026-04-01 to 2026-07-01 exclusive | 2026-07-07T23:59:59Z | 54 | 544 | 532 / 719 / 583 |
| may_early | 2026-05-01 to 2026-06-01 exclusive | 2026-06-02T12:00:00Z | 18 | 166 | 83 / 118 / 106 |
| june_late | 2026-06-01 to 2026-07-01 exclusive | 2026-07-20T23:59:59Z | 18 | 162 | 129 / 203 / 164 |

Selected currency control totals, in integer cents:

| Scenario | Currency | Gross | Adjustment | Net | Received | Balance |
|---|---|---:|---:|---:|---:|---:|
| quarter_close | EUR | 4,997,231 | 36,673 | 5,033,904 | 1,350,727 | 3,683,177 |
| quarter_close | USD | 5,179,953 | 26,392 | 5,206,345 | 1,558,295 | 3,648,050 |
| may_early | EUR | 1,322,205 | 2,431 | 1,324,636 | 234,443 | 1,090,193 |
| may_early | USD | 1,774,102 | 3,660 | 1,777,762 | 289,023 | 1,488,739 |
| june_late | EUR | 1,741,344 | 18,612 | 1,759,956 | 435,284 | 1,324,672 |
| june_late | USD | 1,306,039 | 2,335 | 1,308,374 | 185,157 | 1,123,217 |

Additional checks confirmed the exact 13 output columns, unique and exact bucket keys, non-null integer measures, and complete cohort line counts. Query execution used a read-only immutable database connection, an authorizer allowing only the seven tables and reviewed scalar/aggregate functions, and a progress/time limit. Each scenario completed in under 0.003 seconds and fewer than 150,000 approximate VM instructions. The query is 2,385 bytes. Database change counts remained zero, and the tested input files' SHA-256 hashes were unchanged.

The test source and machine-readable check results are disposable files in `tmp/`. No network, installations, live systems, or other dialects were tested. There are no unresolved material limitations within the supplied fixed-fixture task; this verification makes no production integration claim.
