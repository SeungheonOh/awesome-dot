# Repair the monthly billing reconciliation report

This is an explicitly fictional, offline benchmark. You are maintaining a reporting query for Larch Harbor Services. Finance found inflated invoice revenue, missing unpaid lines, and inconsistent credits after the settlement feed changed to multiple events per invoice line. Repair `output/report.sql` within 900 seconds. Use Python's standard library and SQLite only. There is no network or production system.

## Deliverable and working boundary

Only `output/report.sql` is graded. Return one read-only SQLite query that accepts named parameters `:report_start`, `:report_end`, and `:as_of`. CTEs and subqueries are fine; do not create views or temporary tables. Keep input fixtures unchanged. Put any disposable local test files under your packet's `tmp/`; inspect any code and its effects before running your own bounded local checks. Do not read outside this packet. You may add an optional explanation in `output/notes.md`; it is not scored. No skill-specific phrase, particular query structure, formatting, or row ordering is required.

## Inputs

- `inputs/billing.sqlite`: the complete, fixed SQLite fixture
- `inputs/schema.sql`: schema reference
- `inputs/ledger.json`: the same source rows as arrays in schema column order, for independent reconciliation
- `inputs/scenarios.json`: all three evaluated parameter scenarios
- The existing query in `output/report.sql` is representative defective starting code

The fixture contains 244 invoices, 689 lines, 1,009 adjustments, 1,381 receipt allocations, and 1,060 fulfillment events, plus customer/product dimensions. It was authored with Python Random seed 810327, then explicit boundary and multi-event rows were appended. No randomness occurs during evaluation. The fixture deliberately includes lines without events, multiple events in every child table, multiple lines in the same invoice/family, negative corrections/refunds/returns, draft/void invoices, pending events, late postings, and date-boundary rows. All currencies are integer cents and must remain separate. There are no orphan foreign keys.

## Reporting contract

Select invoice lines whose invoice has status `issued`, invoice_date >= report_start and < report_end, and posted_at <= as_of. The report is an invoice cohort: its events are not restricted to the invoice month or report_end. An event is eligible only when its effective_date <= the date portion of as_of AND its posted_at <= as_of. Adjustments also require `approved`, receipts `settled`, and fulfillments `posted`. Dates use ISO YYYY-MM-DD; timestamps use fixed-width UTC YYYY-MM-DDTHH:MM:SSZ, so lexical comparison is valid. Equality at the as_of boundary is included.

Return one row for each nonempty `(report_month, region, family, currency)` bucket of eligible lines. report_month is the invoice_date's YYYY-MM. Region/family come from customer/product tables. No empty buckets. Every eligible line contributes exactly once irrespective of its event coverage or fanout. Amounts and quantities in event tables are already signed; retain their signs. There are no caps or floors on overpayment, negative balances, or fulfilled quantities.

Required columns (column order and row order do not matter):

- report_month, region, family, currency: the grouping key
- line_count: number of eligible lines
- invoice_count: distinct invoices represented within that particular bucket; an invoice may count in multiple family buckets
- billed_units: sum of invoice-line quantity
- gross_cents: sum of quantity * unit_price_cents
- adjustment_cents: sum of all eligible signed adjustments allocated to these lines, zero when absent
- net_cents: gross_cents + adjustment_cents
- received_cents: sum of all eligible signed receipt allocations, zero when absent
- balance_cents: net_cents - received_cents
- fulfilled_units: sum of eligible signed fulfillment quantities, zero when absent

All measure values must be non-null integers. Output exactly these columns with the stated names.

## Acceptance

Twelve predeclared outcome checks cover: bounded read-only execution in all three public scenarios; output schema/types; exact and unique grouping keys/cohort; each of the nine measure columns above. The expected values are independently calculated from source rows, not from a reference SQL query. There is no style score.

Evaluation permits SELECT/CTEs over the seven supplied tables and common deterministic SQLite scalar/aggregate functions (including sum, count, coalesce, substr, strftime, date, datetime, min, max, abs, round, cast syntax, nullif, ifnull, printf, lower, upper, length). It forbids writes, ATTACH, PRAGMA, extension loading, schema reads, and external files. The query is limited to 64 KiB, 50,000,000 VM progress instructions (approximately), 5 seconds per scenario, and 10,000 returned rows. Ordinary solutions fit comfortably.
