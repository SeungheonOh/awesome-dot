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

### Keep location and hour lineage

Record the selected geocoding result with country/region, coordinates and provider identity. For each requested variable, retain the provider’s unit rather than inferring it from a plausible numeric range. Check that the requested UTC interval exists in each response; a forecast may end before the desired window.

Build a timestamp-keyed join and preserve per-city gaps. If one city refreshes and another fails, keep separate retrieval dates and status. When a user changes the city selection during a request, discard the obsolete response instead of attaching it to the new city’s label.

## Output

An aligned table or structured snapshot with location identity, UTC timestamps, units, gaps, fetch provenance and source attribution.

## Verification and limits

Check duplicate hours, omitted variables, unexpected units, multi-city offset differences and stale-response replacement. A successful server fetch does not establish browser CORS.

## References

[Open-Meteo geocoding](https://open-meteo.com/en/docs/geocoding-api) · [Hourly forecast documentation](https://open-meteo.com/en/docs)

## Service failure handling

Keep the exact failed location/variable and response status. A rate limit does not authorize aggressive retries or another account. Return useful completed locations without falsely marking the whole selection refreshed.

## Worked example

Two fictional normalized responses cover 08:00 and 09:00 UTC. City A has temperature 20°C then 21°C; City B has null then 18°C. Both use the requested Celsius unit, but City B’s first value is unavailable.

The aligned output contains two timestamp rows. At 08:00, A=20 and B=missing; at 09:00, A=21 and B=18. A downstream two-city average is unavailable at 08:00 unless the user explicitly requests an available-city average with denominator 1. It is 19.5°C at 09:00.

If City B’s response instead declares Fahrenheit, reject or perform an explicitly documented conversion before joining. Do not relabel 18°Fas 18°C. The example is supplied synthetic data and establishes normalization decisions, not current weather.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
