---
name: retrieve-aligned-hourly-forecasts
description: "Retrieve and normalize a bounded set of city forecasts into a shared UTC window with per-location units, gaps and provenance."
---

# Retrieve aligned hourly forecasts

## When to use

A downstream analysis, visualization or automation needs comparable weather inputs from a public forecast service.

## Required inputs

- Named places or approved coordinates and a shared time window
- Required weather variables and units
- Permitted provider and the intended output or downstream use

## Workflow

1. Resolve ambiguous place names before fetching. A city name match is not enough when several regions share it. State which city queries or coordinates go to the provider; do not substitute device location.
2. Check the provider documentation and request explicit units and a UTC timeline. Keep forecast model values distinct from observed weather.
3. Validate response units, finite values, percentage ranges, timestamp uniqueness and array alignment. Preserve missing records as gaps rather than converting null to zero.
4. Join locations by actual UTC timestamp, not array index. Retain each location’s fetch time and provider/source metadata separately, including mixed imported and newly fetched data.
5. On partial failure keep prior snapshots dated and identify unavailable cities. Do not replace missing weather with synthetic values or mark all locations live after one succeeds. Respect service terms and requested refresh cadence.

## Output

An aligned table or structured snapshot with location identity, UTC timestamps, units, gaps, fetch provenance and source attribution.

## Verification and limits

Check duplicate hours, omitted variables, unexpected units, multi-city offset differences and stale-response replacement. A successful server fetch does not establish browser CORS.

## References

[Open-Meteo geocoding](https://open-meteo.com/en/docs/geocoding-api) · [Hourly forecast documentation](https://open-meteo.com/en/docs)
