---
name: public-feed-revision-explorer
description: Build a public-data explorer that retains dated snapshots, distinguishes rolling-feed absence from deletion, and compares stable event IDs with honest freshness and failed-refresh behavior. Useful for USGS-style catalog feeds and revision-aware data dashboards.
---

# Public feed revision explorer

Design for changing observations rather than a permanently correct live feed. A successful HTTP response establishes receipt, not completeness, timeliness, causal relationships or real-world safety.

## Chronological build path

1. Read the provider's actual schema and choose a fixed public endpoint. The worked implementation used the [USGS GeoJSON summary schema](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php) and past-day feed. Distinguish real earthquake catalogs from scenario feeds. Fetch one real dated response and retain it as a test fixture with attribution, not an automatic fallback presented as current data.
2. Normalize at the boundary. Require a bounded FeatureCollection, valid generation time, stable unique IDs and expected Point coordinates. Longitude comes before latitude; depth is in kilometers. Preserve unknown magnitude as null, including its distinction from zero or negative magnitude. Reject ambiguous duplicate IDs. If excluding malformed records, show their count rather than silently calling the remainder complete.
3. Keep event time, provider update time, feed generation time and local observation time distinct. Display absolute UTC values and qualify freshness at the time checked. An imported timestamp is a file claim, not verified provider provenance. A static “fresh” badge must not imply continuing observation after the page sits idle.
4. Use stable IDs for comparisons. Classify newly present IDs, changed retained records and IDs absent from the newer snapshot. A rolling-window absence is not evidence that the provider deleted an event. Include the fields used by comparison in the explanation; a changed update timestamp can count as a revision even if magnitude is unchanged. Do not infer aftershocks, risk or causation from spatial proximity.
5. Make filters operate on one normalized snapshot. Use the snapshot's generation time as the rolling-window anchor, not the current clock, so old imports remain inspectable. Handle unknown magnitudes explicitly. Derive counts, maps, timelines, paginated rows and exports from the same filtered array to prevent contradictory totals.
6. Keep geometry honest. A longitude/latitude plot is an equirectangular coordinate atlas, not an equal-area map. Label the projection and axes. Explain what marker radius and color encode; magnitude is not felt area, damage or linear energy. Provide an accessible event ledger alongside pointer-selectable SVG points. Handle longitude wrapping explicitly when computing distances.
7. Bind each request's abort timeout to that request's controller. A timeout that reads a mutable shared controller can abort a later request. Use generation tokens so a slow fetch cannot overwrite a newer import; clear its timer in finally. A failed refresh preserves the previous snapshot and its dates, with a clear error. Never insert a synthetic dataset as a successful recovery. Avoid automatic refresh unless the user wants it.
8. Treat provider and imported strings as untrusted data. Render places, IDs and statuses with textContent. Only expose validated provider event links; do not allow arbitrary schemes or credentials in URLs. A fixed API avoids making a general URL-fetch proxy or accidentally transmitting account material.
9. Export exact received GeoJSON separately from a selected normalized CSV. Label which one is being saved. Protect spreadsheet-bound text fields against formula interpretation without prefixing negative numeric coordinates as text. Make the included fields and source dates inspectable. Saving a public feed does not authorize publishing other user files or configuring a webhook.

## Verification that matters

Test real fixture normalization and reconciliation of input count, accepted rows and rejected rows. Add null magnitude, zero magnitude, invalid coordinates, duplicate IDs, missing timestamps, negative depth, hostile links and markup-like strings. Test exact time-window boundaries and histogram totals against filtered-event counts. Compare known great-circle distances, including a date-line crossing, if implementing distance.

Revision tests should include identical snapshots, added events, changed values, update-only revisions and rolling-window absence. Preserve the distinction between absent and confirmed deleted.

Interaction tests should cover no unsolicited fetch, successful loading, pagination, filters, event details, dated-data preservation after failure, import superseding a pending fetch, future/old imported timestamps and raw/CSV export bytes. Exercise timeout races with captured per-request controllers. Simulated-DOM tests prove state transitions but not browser CORS, responsive layout, actual downloads or pointer/keyboard ergonomics.

## Worked result

Seismic Window fetched the real USGS past-day feed generated October 2, 2026 at 11:25:15 UTC and validated all 220 records. Its model tests passed null magnitude, malformed record accounting, duplicate rejection, provider-link restrictions, revision classification, date-line distance and histogram reconciliation. Its simulated-DOM checks passed empty startup, loading, pagination/filter/details, failure preservation, text-only rendering and import supersession. The successful fetch was a command-line check; actual browser CORS and page layout remained unverified. The saved sample is a dated fixture, not a live feed.

The UI explicitly says it is not an emergency alert or earthquake prediction service. Counts reflect reporting coverage and are not a regional risk score. These domain limits belong alongside the map, not only in a buried README.

Deliver the app and tests separately from a skills-only contribution. Publish only the reusable procedure to a skills-only repository, and obtain the user's chosen destination before public app deployment.
