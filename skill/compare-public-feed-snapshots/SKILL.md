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

## Joining a catalog to changing status

Some public services separate stable location/identity records from operational status. Validate uniqueness in both feeds and join by the documented ID. Report missing status, unmatched status and malformed rows separately; do not convert an absent count into zero or silently discard coverage differences.

Carry both the feed update time and the individual record's last-report time. Fetching a fresh file does not make every contained observation fresh. Define an explicit age threshold suited to the task and the provider's TTL, with a visible rule for future-dated observations or clock disagreement. Decode timestamps according to the selected schema version rather than guessing seconds versus milliseconds or treating a new version as the old schema.

For availability views, combine freshness with the relevant operational flags. A positive count at a closed or non-renting station is not evidence that a user can obtain a vehicle there. A filtered availability total should say which rows it excludes. Re-evaluate age as time passes even when the interface does not fetch again.

A short in-memory server cache can reduce repeated public requests, but it must preserve the original observation and provider dates. Concurrent requests may share a fetch; a cache hit must not reset evidence age. A failed refresh should retain the dated prior snapshot, not report a newly observed zero.

### Additional worked example

A status feed was generated at 20:00, but one station last reported at 19:40. The application uses a 180-second age limit. That station's three reported vehicles are excluded from current pickup availability even though the file itself is fresh. A second station reported at 19:59 with three vehicles but has renting disabled; it is excluded for a different reason. Keep both explanations available rather than collapsing them into “no vehicles.”

### Executed checks

A bounded local HTTP service was tested against synthetic catalog/status feeds for exact-ID joins, duplicate rejection, missing and invalid status, future timestamps, age expiry, operating flags, cache reuse and simultaneous-request deduplication. Simulated-interface tests verified that displayed freshness expired without a new network request and that a failed or late refresh could not replace the accepted newer snapshot.

A separate authorized public-feed check joined 2,520 information records to 2,520 status records with no unmatched or malformed rows at the time observed. It still found stale and closed stations; successful transport was not treated as universal availability. The same fixed-endpoint reader was verified through its local HTTP interface. Real-browser rendering and future provider uptime were not established.


## Provider-reported service status

When combining public status pages, retain a per-provider success or failure rather than declaring the whole collection healthy or unavailable. A summary's status is the provider's report, not a direct measurement of a particular customer's service or a diagnosis of an unrelated local error. Keep scheduled maintenance distinct from incidents and preserve group-component labels so a parent plus its children is not counted as independent services.

A page-change timestamp may remain old until metadata changes; it is not necessarily a heartbeat. Show it separately from retrieval time and qualify any freshness inference. Fresh transport does not establish a fresh measurement, and an old change timestamp alone does not prove outage. Apply the chosen age threshold to the appropriate evidence clock. If the interface ages a snapshot without refetching, update the freshness text without discarding the reader's expanded details or focus.

Fixed-endpoint readers should bound streamed bytes and total time, reject redirects where destination scope is fixed, preserve failure dates and coalesce concurrent requests. A short cache must not turn a failed fetch into a healthy zero or reset observation time. Render upstream descriptions as text and qualify truncated updates as excerpts; constrain outbound links to the intended source hosts.

A worked two-provider local service passed synthetic normalization, identity/timestamp/link limits, real local HTTP cache/coalescing and request guards, partial/all-failure recovery, a deadline against an abort-ignoring stub, and superseded/cancelled UI refresh cases. Its October 6, 2026 20:11:34 UTC check fetched both public feeds: 12 listed components from GitHub and 480 from Cloudflare. Cloudflare supplied an August 27 page timestamp; this was preserved instead of being overwritten with the fetch time. These results establish that bounded retrieval and normalization at that moment, not provider uptime, account access, future availability or real-browser rendering. The endpoint contracts are documented by [GitHub](https://www.githubstatus.com/api) and [Cloudflare](https://www.cloudflarestatus.com/api).

In a multi-source view, keep comparison baselines per source. One failed provider should neither erase its previous success nor block a successful independent provider. Label a cache hit as the same observation, not a newly verified lack of change. Reject an older observation or conflicting payload with the same observation timestamp, retaining the accepted baseline and an explicit warning. Separate substantive selected-field revisions from timestamp-only changes, and qualify absence from an incident summary as absence rather than confirmed resolution. A worked implementation checked 100 reordered-ID comparisons and interface cases covering failure gaps, cache identity and rejection without loss of the last accepted observation.

Separate an optional display filter from the accepted source snapshot. Preserve the complete denominator and say when zero matches are only a view result, not proof of service health or source absence. Unknown operational status should not silently pass an operational-only test. For grouped component feeds, make exclusion of group rows an explicit view choice rather than changing the source count. A worked interface verified that name/status/group filters issued no new requests, preserved expanded details and left full-source exports intact with separate view settings.
