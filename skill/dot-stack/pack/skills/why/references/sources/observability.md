# Runtime observability

## Useful evidence

Metrics, monitors, dashboards, traces, log patterns, and incident timelines describe operational conditions around a change. They can explain the constraints an engineer faced, but a graph alone seldom proves author intent or causation.

## Orient before querying

Discover the actual read tools and identify the owning service, environment, release, relevant units, tags, and time zone. A development spike is not production evidence. Inspect dashboard and monitor definitions to understand numerator, denominator, aggregation, and thresholds before reading the chart.

Start from a bounded period around the target incident or change. Narrow logs by service, error class, route, trace, and time. Prefer counts or representative patterns over raw sensitive payloads. Respect retention, sampling, query cost, and result limits. Do not run expensive unconstrained scans or create new monitors for this investigation.

## Productive sequence

1. Identify the service and relevant upstream/downstream dependencies
2. Read existing dashboards and alerts tied to that service or behavior
3. Verify metric meaning and units, then inspect the appropriate time series
4. Aggregate matching log/error patterns and examine a minimal representative sample
5. Inspect a trace when cross-service timing or retry behavior matters
6. Read any explicitly linked incident or investigation record

These are capabilities to map to exposed tools, not fictional function names. If only an exported chart is supplied, report what is visible and its timestamp; do not imply access to underlying logs.

## Strong and weak connections

A dated incident action item naming the defensive check is strong motivation evidence. A monitor threshold matching a constant is a lead that may reflect a common limit or later copy. A drop after deployment is consistent with an effect, but concurrent changes, traffic shifts, altered sampling, or instrumentation changes can explain it too.

Compare meaningful rates as well as counts. A lower error count can result from lower traffic. Check the actual deployment date, not only merge time. Current monitor settings may differ from the historical values in question.

## Return

For each useful item give type, ID/link, service/environment, owner/date if known, time window, exact query or accessible definition, units/aggregation, concise numeric observation, and its inferred relation to the code. Preserve correlation language. Name unavailable historical data, renamed metrics, sampling, and unsearched areas. Do not export secrets or raw customer records into the report.
