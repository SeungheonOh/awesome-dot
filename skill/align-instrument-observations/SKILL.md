---
name: align-instrument-observations
description: Align time-series measurements from multiple instruments while preserving source identity, missing values, quality exclusions and observation age. Use for a measurement dashboard or analysis that combines streams; not for forecasting or treating nearby samples as simultaneous without a defined rule.
---

# Align instrument observations

## When to use

Use when several feeds describe the same physical system but differ in timestamps, source instruments, quality flags or coverage. Deliver an aligned dataset and visualization whose gaps and provenance remain visible. A convenient join is not necessarily a scientifically meaningful one.

## Required inputs

- Named provider endpoints or supplied instrument exports
- Timestamp convention, source identity, measured fields and units
- Provider meanings for active-source and quality flags, where available
- Analysis window and chosen matching rule
- Retrieval time and a freshness threshold appropriate to the intended use

If the quality vocabulary is incomplete, state exactly which flags are filtered and which remain uninterpreted. Do not turn a convenient numeric zero into a universal assertion of data quality.

## Workflow

### 1. Verify the current feed contract

Check the provider's current schema and service-change notices before relying on a remembered endpoint. A replacement may change arrays to objects, numeric strings to numbers, field names, source identity or window duration. A successful response alone does not establish that the old endpoint remains the intended product.

Retrieve only the bounded records needed for the task. Keep provider identity and local retrieval time alongside the data. Do not put secrets or user location into public-feed requests. A historical fixture may help test a parser but must never substitute silently for a failed live fetch.

### 2. Normalize individual streams before joining

Parse timestamps with an explicit timezone contract. Reject malformed and impossible calendar timestamps; do not let permissive date parsing roll an invalid day into the next month. Preserve source time precision and keep it separate from retrieval time.

Validate numeric types and missing values before arithmetic. Null, an empty string and an absent field are not measurements of zero. Apply the chosen active-source and quality policy per record, then count excluded rows by meaningful category. Label a combined exclusion counter as combined rather than calling every excluded row corrupt.

Define identity as the instrument/source plus timestamp, adding sequence or channel identity when the provider requires it. When conflicting records share an identity, exclude or reconcile them under a documented provider rule. Do not silently keep whichever arrived last in an unordered response.

### 3. Choose and expose the temporal join

Prefer an exact timestamp and source match when the task has no scientifically justified tolerance. This may leave fewer paired samples, which is useful information. Different instruments or satellites at the same time are not automatically interchangeable.

If nearest-neighbor matching, resampling or interpolation is required, establish the permitted tolerance, direction, tie rule and whether future observations may be used. Retain the original timestamps and time offsets. For online decision support, using a future observation can introduce look-ahead bias even if it makes an offline plot smoother.

Keep unmatched observations available as their own stream where useful. A magnetic observation without a simultaneous plasma record can still belong on its own trace; it must not acquire an invented paired plasma value.

### 4. Separate freshness from history

Compute freshness for each instrument independently at the time the result is viewed. A recently downloaded response may contain old measurements. A cached response must retain its original retrieval time.

When multiple active sources claim the same newest timestamp and no authoritative preference exists, mark the latest-value summary ambiguous. Do not use lexicographic source order as an undocumented scientific selection rule.

Historical plots may remain useful after the latest tile becomes stale. Label stale or missing current observations without deleting the historical evidence. A failed refresh should preserve the previous snapshot and its dates, not produce a false all-clear or an invented zero.

### 5. Render discontinuities honestly

Use real timestamps on the horizontal axis, not row positions. Keep field names and units on separate traces when their scales differ. Include zero where it is a meaningful reference, such as a signed field component.

Break lines at missing values, material time gaps, source changes and non-increasing timestamps. Show isolated points rather than drawing an invisible one-point path. Do not connect over missing intervals merely because a charting library does so by default.

Report the number of displayed samples, unpaired rows, conflicting identities and policy exclusions. Keep plot-window counts separate from whole-response counts. A lower sample count is not by itself a real-world change in the physical system.

### 6. Verify against an independent alignment oracle

Use original fixtures with exact matches, near-but-not-equal timestamps, different sources at the same time, null fields, conflicting identities, inactive records, nonzero quality flags, future dates and gaps. Compute expected matches by an independent direct lookup or small hand-worked table, not by calling the production join twice.

Test stale transitions using a controllable clock without refetching. Verify refresh failure retains the dated snapshot. Inspect a rendered chart or export for misleading continuity and axis labels. Distinguish programmatic geometry checks, artifact rendering, real-browser interaction and live-provider retrieval.

## Worked example

Suppose a plasma stream has source A at 09:58 and 09:59 UTC. A magnetic stream has source B at 09:58 and source A at 09:59. An exact source/time join pairs only the 09:59 records. The 09:58 plasma row keeps a null magnetic value; source B's magnetic measurement remains visible on the separate magnetic trace. It is not borrowed merely because its timestamp matches.

A real implementation used NOAA SWPC's replacement RTSW endpoints after checking Service Change Notice 26-21. The older products omitted source/active metadata and were scheduled for retirement in April 2026. The replacement wind field is `proton_speed`, not the old `speed` name.

On October 3, 2026 at 10:52:29.771 UTC, the local reader retrieved 3,886 magnetic and 3,937 wind records. Its explicit policy retained active records with `overall_quality = 0`, finite required values and timestamps within its bounded window; 2,450 magnetic and 2,536 wind rows were excluded by the combined policy. No conflicting accepted identities remained and no accepted wind rows lacked an exact magnetic match. The selected six-hour view contained 348 wind and 354 magnetic samples.

The newest paired record was source SOLAR1 at 10:46:00 UTC: speed 288 km/s, density 7.53 particles/cm³ and GSM Bz 0.07 nT. This was an upstream observation, not a forecast of conditions at Earth or the user's location. Other instrument flags were not interpreted, so the filtering was not a full quality certification.

Validation included 100 independently checked source/time fixture sets, stale-clock transitions, ambiguity handling, a real loopback HTTP request reaching the NOAA feeds, and a rendered three-trace SVG inspected for geometry. Simulated-DOM tests did not establish real-browser layout. No propagation or aurora model was validated.

## Deliverable

Provide the aligned rows or chart, exact matching/filter policy, source and retrieval times, per-stream freshness, excluded/unmatched counts, and remaining interpretation limits. Keep observations separate from derived predictions. Stop once the requested analysis is reproducible and its uncertainty is visible.

## References

- [NOAA real-time solar wind](https://www.swpc.noaa.gov/products/real-time-solar-wind)
- [NOAA Service Change Notice 26-21](https://www.weather.gov/media/notification/pdf_2026/scn26-21_Data_Format_Changes_Impacting_SWPC_Products.pdf): replacement endpoints, fields and source metadata
