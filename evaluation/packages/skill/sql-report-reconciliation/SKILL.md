---
name: sql-report-reconciliation
description: Turn a bounded business reporting question and authorized relational sources into a defined metric, read-only SQL, and a reconciled result with explicit unknowns. Use for reporting queries and join or total discrepancies, rather than spreadsheet cleanup.
---

# Reconcile a SQL report

Deliver the answer at its agreed grain, the exact query and parameters, source evidence, and a reconciliation explaining what is known, incomplete, or unallocated. A query that runs is not yet a trustworthy report.

## Pin down the question before calculating

Use the supplied business definition and approved source documentation. Resolve only ambiguities that change the result; do not invent an accounting recognition policy, refund policy, or attribution rule.

Record these decisions in the report:

- **Metric and population:** What is being counted or summed? Which entities qualify, including status, exclusions, cancellations, reversals, and deleted records? What is the denominator for a rate?
- **Grain:** The unique entity represented by a source row, each intermediate relation, and the final output row. State the reporting dimensions and whether entities may belong to multiple categories.
- **Time:** The event field, timezone, half-open interval, snapshot/as-of cutoff, and treatment of late arrivals and updates. Distinguish an order cohort from refund activity during a month. Do not silently switch between event time and ingestion time.
- **Units:** Currency, integer minor units or exact decimal scale, sign conventions, and any owner-approved conversion source/date/rounding. Keep currencies separate without an approved conversion rule. Do not average already-averaged rates or add incompatible units.
- **Keys and relationships:** Declared and observed uniqueness, nullable keys, join direction, expected cardinality, effective-date rules, and unmatched-key handling. A table name or column named `id` does not prove uniqueness.
- **Completeness:** Which extracts, partitions, tenants, dates and statuses were supplied; extraction time and truncation limits; coverage evidence for missing child rows; and any independently supplied control counts or totals. An empty relation is not evidence of a zero unless coverage is established.
- **Dialect and version:** Exact target engine/version, timestamp types, decimal behavior, parameter syntax, and available execution controls. SQLite fixture success is not evidence that another engine accepts the query.

If an essential definition is unresolved, return the proposed definition and the smallest question needed. If the population cannot be shown complete, label the result as a result for the observed extract, not the entire business.

## Use only the authorized slice

Prefer supplied schema definitions, extracts, saved reports and existing read-only access. Identify each source by an authorized document/link, table and relevant columns, or extract name and snapshot. Trace every metric field and policy choice to that evidence. Do not put credentials, secrets or unnecessary personal rows in the deliverable.

If existing access permits it, inspect only the named relations and relevant partitions using bounded projection, time/tenant filters and approved result limits. Do not enumerate unrelated databases, search for credentials, acquire broader access, install database software, or write to production. A row limit bounds returned rows, not scan cost; assess the access path, bytes scanned, timeout and resource budget separately.

Before any actual-source execution, inspect the complete statement and its dependencies: CTEs, views, functions, procedures, external tables and exports. A `SELECT` can invoke side-effecting functions or remote services; a leading keyword is not a safety proof. Reject modifying CTEs, `SELECT INTO`, locking clauses, exports, unknown functions and additional statements. Check whether the proposed plan command executes the query; `EXPLAIN ANALYZE` commonly does. Use only documented, already-authorized read-only controls, and do not change security settings to obtain them.

Bind data values as parameters. Choose identifiers from the verified schema rather than interpolating untrusted input. If effects, scope, access or cost cannot be established, supply a reviewed draft and the exact unresolved dependency instead of running it. Never run against a live source merely to test this workflow.

## Build at one grain at a time

1. Define the population once with explicit time/status predicates. Keep its key and currency. Check non-null keys and uniqueness before joining; fail or expose duplicates rather than silently choosing a row.
2. Reduce each one-to-many child relation independently to the population key. Carry source-row counts, null-amount counts, unit mismatches and coverage flags alongside sums. Apply each relation's own event/as-of predicate deliberately.
3. Join the reduced relations to the population. Verify the expected row count and key uniqueness after every join. Joining raw line items to raw refunds produces a many-to-many expansion even though each child is one-to-many from orders. `DISTINCT` or `SUM(DISTINCT amount)` does not repair this.
4. Retain unmatched and unallocatable records in a separate reconciliation with their units, known amounts, reason and source scope. Do not guess an owner, time bucket or allocation. An inner join is not a remedy for missing keys.
5. Distinguish complete zero, unknown, missing value and not applicable. `SUM` ignores nulls; count them explicitly. `COALESCE(..., 0)` is justified only by a documented complete-empty rule. A missing amount or incomplete coverage makes the affected total unknown unless the owner has defined another treatment.
6. Aggregate only after entity-level validation. Include complete/unknown entity counts. Preserve a known subset as a clearly labeled subtotal, never as the population total. Do not replace an unknown group total with the sum of its known members.

For ratios, reconcile numerator and denominator populations separately and specify zero/unknown denominator behavior. For snapshots or slowly changing dimensions, verify that the time-aware join yields at most one eligible row per entity; do not arbitrarily select the latest record.

## Reconcile before reporting

Compare source population counts to the agreed control evidence, child row counts before/after reduction, and final entity counts. Explain discrepancies rather than making totals fit. A sample validates examples, not source completeness. Page through a bounded authorized extract when needed; if pagination, truncation or late-arrival coverage is unresolved, preserve that limitation.

Use boundary cases that exercise the actual definition: exact interval start/end, same-valued rows with different keys, multiple children on both sides, missing children, null amounts, incomplete coverage, unmatched keys, separate currencies, and post-cutoff activity. Where possible compare the result with an independently calculated small example or owner-provided control total, not a second spelling of the same query.

Read [the fictional worked example](references/fictional-example.md) for an executable, self-contained SQLite case. Its in-memory setup and assertions must stay separate from any actual-source query. [The captured run](references/verified-run.md) states exactly what was executed.

## Hand back a reviewable answer

Provide:

- The metric definition, population/grain, interval/timezone, as-of snapshot, units and completeness status
- Source references supporting schema, keys, relationships and owner-defined policy, including unresolved assumptions
- The full query, target dialect/version and parameter values, with read-only effects review and bounded execution scope
- Results by compatible unit, known and unknown entity counts, and explicitly labeled partial subtotals
- The reconciliation: population counts, join multiplicity checks, null/coverage exceptions, unallocated records and differences from controls
- Verification status separated into **executed on supplied data**, **executed on fictional fixtures**, and **unrun integration checks**, as applicable

If a result is incomplete, say what remains unknown and what source or decision would resolve it. Do not manufacture a single headline number.
