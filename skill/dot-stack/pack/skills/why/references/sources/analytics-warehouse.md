# Product and warehouse evidence

## Useful evidence

Product events, usage aggregates, experiments, feature-flag exposure, pipeline lineage, query history, and data migrations may explain a threshold or product-driven design. These describe user/data behavior; they differ from service-level runtime metrics. A warehouse schema is organization-specific.

## Discover before querying

Use an authorized read-only interface. Inspect available catalogs, table metadata, column meanings, retention, refresh cadence, and the relevant time field. Prefer curated typed and deduplicated models when their semantics match the question. Do not assume table names, property conventions, system tables, or notebook access from a provider name.

If a tool returns a query job ID, use its documented result-retrieval operation instead of submitting the same expensive query repeatedly. Authentication failure or forbidden data remains a blocker. Do not seek alternative credentials or mutate a table to aid an investigation.

## Bound cost and disclosure

Every query should have a relevant time range and scope, selecting only needed columns or aggregates. Use actual partition/filter columns and read the execution constraints before scanning a large dataset. Aggregate before exporting. Avoid personal identifiers unless necessary for the authorized question, and keep sensitive raw rows out of the report.

An illustrative query shape, only after the actual table and columns are verified, is:

```sql
SELECT event_day, COUNT(*) AS event_count
FROM verified_event_table
WHERE event_day >= :start_day AND event_day < :end_day
GROUP BY event_day
ORDER BY event_day;
```

The identifiers and bind syntax are schematic. Replace them through the current tool's documented parameterization and actual metadata; do not run this as if a table with that name exists. A copied sample query is not a data result.

## Investigation patterns

- Usage trajectory: compare counts or rates before and after the actual release, accounting for instrumentation changes
- Threshold origin: examine the relevant pre-change distribution, units, percentile method, denominator, and sample size; a matching percentile is a clue rather than proof of intent
- Experiment decisions: inspect exposure and outcome records for the correct flag, variants, eligibility, and period; a “shipped” record may directly state a decision if its semantics are documented
- Expensive query or migration: examine authorized query-history aggregates in a narrow interval and connect them to a documented performance or migration decision
- Lineage: identify producers and consumers of an affected field or model, returning code-history leads to the relevant investigator

## Guard against misleading data

A spike may reflect a new event name or logging change rather than behavior. Raw data may contain retries and duplicate IDs. Curated models may lag recent events or rewrite historical definitions. A property visible now may not have existed then. Retention expiry and unqueried notebooks are gaps, not null findings.

Before claiming an improvement, check denominator, release timing, experiment assignment, concurrent changes, sampling, and data completeness. Data correlated with a code change cannot by itself prove why the author chose that implementation.

## Return

Record the actual fully qualified table or source identity, exact authorized query or saved job, time range, schema/refresh assumptions, and compact numerical summary. Include counts, units, percentiles, or first/last-seen times only when actually computed. Explain relevance and strength, name alternative readings, and preserve all access/retention gaps. Never substitute plausible numbers for missing results.
