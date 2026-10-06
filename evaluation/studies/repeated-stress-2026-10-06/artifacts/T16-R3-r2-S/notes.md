# Monthly billing reconciliation repair

`report.sql` is one read-only, parameterized SQLite statement. It returns exactly the four grouping columns and nine required integer measures.

## Definition and source evidence

- Population: issued invoices with `report_start <= invoice_date < report_end` and invoice `posted_at <= as_of`; each qualifying invoice line contributes once.
- Grain: one row per nonempty invoice month, customer region, product family, and invoice currency. Invoice counts are distinct within each bucket, so a multi-family invoice can appear in multiple bucket counts.
- Event eligibility: the specified approved/settled/posted status, effective date no later than the date portion of `as_of`, and posting timestamp no later than `as_of`. Both as-of boundaries are inclusive. Events are not restricted to the invoice reporting interval.
- Amounts remain signed integer cents; quantities remain signed integer units. There are no conversion rates, caps, or floors. Currencies remain separate.
- Each event table is independently summed by line ID before left joining to the cohort. Missing events contribute zero under the supplied complete-fixture contract; missing events never remove a line.
- Definitions and completeness come from `TASK.md`; columns and declared primary keys come from `inputs/schema.sql`. All seven database tables were reconciled against the independently supplied arrays in `inputs/ledger.json`.

## Verification actually executed

Used Python's standard library and SQLite 3.53.1. The fixture was opened with read-only, immutable connection options. A restrictive SQLite authorizer allowed only SELECT, reads of the seven supplied tables, and the four reviewed deterministic SQL functions. Each execution had a five-second/progress-instruction bound and a 10,000-row limit.

An independent Python source-row calculator assigned every qualifying line to its bucket, accumulated each qualifying signed event directly from the JSON arrays, and counted invoice IDs with per-bucket sets. All output keys and all nine measures matched exactly in every supplied scenario. Output names, unique grouping keys, non-null integer measures, and total qualifying line counts passed.

| Scenario | report_start | report_end | as_of (UTC) | Buckets | Lines | Distinct cohort invoices |
|---|---|---|---|---:|---:|---:|
| quarter_close | 2026-04-01 | 2026-07-01 | 2026-07-07T23:59:59Z | 54 | 544 | 194 |
| may_early | 2026-05-01 | 2026-06-01 | 2026-06-02T12:00:00Z | 18 | 166 | 60 |
| june_late | 2026-06-01 | 2026-07-01 | 2026-07-20T23:59:59Z | 18 | 162 | 61 |

Distinct cohort invoice counts above are across the whole scenario; they are not sums of per-bucket invoice counts.

Source control counts matched: 12 customers, 9 products, 244 invoices, 689 lines, 1,009 adjustments, 1,381 receipts, and 1,060 fulfillments. Primary keys were unique, and no null source values or orphan foreign keys were observed. All database rows exactly matched their JSON counterparts.

The tested scenarios included lines missing qualifying events and lines with multiple qualifying events in each event table. For example, quarter_close retained 182 lines without qualifying receipts and correctly aggregated 231 lines with multiple qualifying receipts.

Measured report execution times were approximately 0.0027, 0.0011, and 0.0014 seconds respectively, with approximately 147,000, 81,000, and 111,000 VM instructions. The query is 2,333 bytes. Database change count was zero, and before/after SHA-256 comparisons confirmed that every input file remained unchanged.

## Limits

No unresolved material limitation for the supplied fixed fixture and three scenarios. Verification applies to this offline SQLite task; no production source, live integration, other SQL engine, or unseen dataset was tested.
