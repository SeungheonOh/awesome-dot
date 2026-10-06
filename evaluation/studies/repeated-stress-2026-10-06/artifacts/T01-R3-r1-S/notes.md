# Billing report repair

`report.sql` is one read-only SQLite statement accepting `:report_start`, `:report_end`, and `:as_of`.

## Definition and implementation

- Population: issued invoices with invoice dates in the half-open reporting interval and invoice posting timestamps at or before `as_of`.
- Calculation grain: one eligible invoice line. Each event stream is independently summed by line before left joining, so absent events retain the line and multiple events cannot multiply it.
- Output grain: invoice month, customer region, product family, and invoice currency. Invoice counts are distinct within each bucket; they should not be summed across families to obtain a distinct invoice total.
- Events: adjustments must be approved, receipts settled, and fulfillments posted. Both effective date and posting timestamp use inclusive as-of cutoffs. Event dates are not restricted by the invoice reporting interval.
- Amounts remain signed integer cents; quantities retain their signs. Currencies remain separate. No balances or quantities are capped or floored.
- The supplied task identifies the fixture as complete, source measures as non-null, and absent events as zero. Zero-filling is therefore supported for these inputs.

Sources: `TASK.md`, `inputs/schema.sql`, `inputs/billing.sqlite`, `inputs/ledger.json`, and `inputs/scenarios.json`.

## Checks actually executed

Python standard library with SQLite 3.53.1; no external systems, packages, or data. The fixture connection used read-only immutable mode and a restrictive SQL authorizer. A progress handler bounded each query to approximately 50 million VM instructions and five seconds.

All seven SQLite source tables matched the independent JSON ledger. Source row counts, primary-key uniqueness, non-null values, and all declared relationships were checked. Source file hashes were identical before and after execution; the connection reported zero changes.

For all three supplied scenarios, an independent Python row-by-row calculation matched every bucket and all nine measure values exactly. The checks also verified the exact output columns, non-null integer measure types, unique and nonempty grouping keys, and precisely one intermediate row per eligible invoice line.

| Scenario | Reporting interval | As-of UTC | Buckets | Eligible lines | Distinct eligible invoices |
| --- | --- | --- | ---: | ---: | ---: |
| quarter_close | 2026-04-01 through before 2026-07-01 | 2026-07-07T23:59:59Z | 54 | 544 | 194 |
| may_early | 2026-05-01 through before 2026-06-01 | 2026-06-02T12:00:00Z | 18 | 166 | 60 |
| june_late | 2026-06-01 through before 2026-07-01 | 2026-07-20T23:59:59Z | 18 | 162 | 61 |

Observed report execution times were below 0.004 seconds per scenario. Test source and the detailed verification log are disposable artifacts under `tmp/`.

No unresolved material limitation for the supplied fixture and scenarios. Production integration, other database dialects, and data outside the supplied fixture were not tested.
