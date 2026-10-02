---
name: compare-public-feed-snapshots
description: "Retrieve or inspect a bounded public feed and compare stable records across snapshots without mistaking rolling-window absence for deletion."
---

# Compare dated public-feed snapshots

## When to use

A dashboard or automation needs to know what changed in a public catalog and how fresh the evidence actually is.

## Required inputs

- Approved fixed feed endpoint or supplied snapshots
- Stable record identity, schema and rolling-window semantics
- Required fields, units, as-of time and output audience

## Workflow

1. Read the provider schema and verify the endpoint is the intended live catalog rather than a scenario/example feed. Retrieve only the approved scope and retain raw source identity and observation time.
2. Normalize required fields with explicit missing-value semantics. Preserve null versus zero, reject duplicate identities, and count malformed excluded rows. Never call a partial normalized result complete without qualification.
3. Keep event time, provider update time, feed generation time and local observation time separate. Imported source names/timestamps remain claims from that file. Qualify freshness at the time checked.
4. Compare stable IDs as newly present, revised and absent. State which fields count as a revision. An absent record in a rolling feed is not a verified deletion; changed coverage does not prove a real-world trend.
5. On failure preserve the last snapshot with its original dates and an explicit error. Do not substitute synthetic data or quietly label cached data current. Ensure late responses cannot overwrite a newer snapshot.

## Output

A dated change set, field-level revisions, missing/excluded counts and provenance, plus any unresolved completeness or freshness limits.

## Verification and limits

Reconcile selected counts, identical snapshots, null values, update-only revisions, rolling-window expiry and failed refresh. A successful server fetch does not establish browser access or downstream processing.

## References

[USGS summary-feed example schema](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)
