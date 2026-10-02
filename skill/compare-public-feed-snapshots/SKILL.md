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

### Define the comparison window and authority

Record both snapshots’ generation times, retrieval times and source status. A file’s claimed provider URL does not authenticate its origin. Compare only fields selected for the task, retaining raw snapshots separately where authorized. Check changed window boundaries before attributing count differences to new events.

Keep per-record revision detail: old/new selected values and update times. An update-only timestamp change is different from a changed measurement even when both count as revisions. If a response arrives out of order, preserve the newer accepted snapshot or explicitly open the older one as historical data; do not silently move the live view backward.

## Output

A dated change set, field-level revisions, missing/excluded counts and provenance, plus any unresolved completeness or freshness limits.

## Verification and limits

Reconcile selected counts, identical snapshots, null values, update-only revisions, rolling-window expiry and failed refresh. A successful server fetch does not establish browser access or downstream processing.

## References

[USGS summary-feed example schema](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php)

## Example request

“Compare these two dated feed snapshots using their event IDs. Show added, revised and absent records with field changes, distinguish rolling-window expiry from deletion, and keep unknown values explicit.”

## Worked example

Two fictional rolling 24-hour snapshots are supplied. The 10:00 snapshot contains A (magnitude 2.0), B (3.1) and C (1.5). The 11:00 snapshot contains B (3.2), C (1.5) and D (2.4), with B’s provider update time advanced.

The change set is newly present D, revised B with magnitude 3.1→3.2; unchanged C; absent A. Preserve these record identities rather than comparing sorted row positions. A’s absence may be rolling-window expiry and is not a verified deletion.

If the 11:00 fetch fails instead, keep the 10:00 snapshot dated and report no verified new change set. Do not report “zero new events” from a failed request. This example uses supplied fictional records, not current earthquake data.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
