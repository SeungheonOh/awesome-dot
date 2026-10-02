---
name: forecast-to-midi-instrument
description: Build a service-connected musical instrument that turns aligned hourly weather forecasts into a playable score, reproducible source snapshot, and standard MIDI export.
---

# Forecast-to-MIDI Instrument

Build an expressive instrument whose inputs come from a real public weather service. Keep the distinction between measured data, model forecasts, and artistic mappings visible. This is a creative tool, not a weather-alert system. Keep product source, examples, tests, and deployment files outside this skills contribution.

## Inputs and useful scope

Choose one to three cities, a shared 24-hour UTC window, and a tempo. Use a public city-search service and hourly forecast endpoint, subject to their current usage terms. The reference implementation used [Open-Meteo geocoding](https://open-meteo.com/en/docs/geocoding-api) and [hourly forecasts](https://open-meteo.com/en/docs). Verify the actual endpoint response and browser CORS behavior before building around it; do not assume a successful server request proves a browser can read the response.

## Chronological construction

1. Define a deterministic musical mapping before designing the interface. One useful example assigns temperature to scale degree, wind speed to pulse density, cloud cover to note velocity, and precipitation probability to percussion density. The mappings are creative choices, not scientific equivalences. A rain-probability tap does not mean rain will occur at that instant.
2. Normalize service responses once at the boundary. Verify the exact requested units, aligned array lengths, consecutive UTC timestamps, finite values, and percentage ranges. Keep missing records as gaps. Never turn null temperature or probability into zero to make the score look complete.
3. Align all cities to the same UTC timestamps. Select each city's record by timestamp rather than by array index. Preserve its fetch time independently. A city with an unavailable forecast stays visibly unavailable; do not silently supply example weather or claim that all selected cities contributed.
4. Write a pure composer returning one event list with beat, duration, pitch, velocity, channel, and event kind. Use the same list for browser playback and MIDI export. Keep the mapping version and source metadata in the saved snapshot so the composition can be reproduced.
5. Start with a bounded, legible mapping. The reference used four beats per forecast hour, 24 bars, tempo 60–140 BPM, and up to four pulses per city per bar. At 96 BPM, 96 beats last one minute. Temperatures outside the chosen musical range clamp in pitch while retaining their original displayed weather values. Explain these choices rather than implying a universal mapping.
6. Design a score view, an hourly data inspector, and per-city provenance cards together. A selected bar should show the actual temperature, wind, cloud cover, and precipitation probability behind the sound. Mark missing bars and show UTC dates, snapshot age, and whether data was imported or fetched.
7. Build audio around the audio clock. After an explicit Play gesture, resume AudioContext, schedule notes slightly ahead using absolute audio times, and animate from that same clock. A short interval should fill the scheduling horizon, not directly play every beat. Skip events missed during a long main-thread stall instead of emitting a burst of late notes.
8. Keep the audio lifecycle reversible. Stop scheduled voices on Stop, changes to the composition, hidden tabs, and page exit. Guard an unresolved AudioContext.resume() with a generation token so a stale promise cannot restart audio after Stop. Use a conservative master level, envelopes with short attacks/releases, and bounded polyphony; a compressor does not replace gain discipline.
9. Export a standard MIDI file from the event list. A practical layout is format 1 with a conductor tempo track, one track/channel per city, and a percussion track on MIDI channel 10. Use variable-length delta times, sort note-offs before note-ons at the same tick, and terminate every track at the same intended score length. Include source attribution in metadata. Browser synthesis and a General MIDI player may have different timbres; do not promise identical audio.
10. Add snapshot export/import and graceful service failures. Import into a temporary validated model, then replace the visible score atomically. Retain original units and source timestamps. Imported data must remain labeled imported even if a later partial refresh updates another city from the API. A single global “live” flag is insufficient for mixed provenance.
11. Serialize or cancel overlapping work deliberately. A slow file import must not overwrite a newer tempo change or city selection. Failed or cancelled requests preserve prior city snapshots with their original timestamps. Do not automatically retry rate limits or continuously poll when no user action requires it.
12. Persist lightweight city/tempo preferences locally if useful. Make clear which queries and city coordinates go to the service. Provide a portable snapshot rather than treating browser storage as durable backup. Keep publication separate from construction when the user wants to choose what goes live.

## Verification

- Check the composer with fixed fixtures: deterministic events, pitches and velocities in range, positive durations, no notes past the score end, and exact UTC alignment across cities.
- Delete one required hourly value and verify that its city rests for that bar. Change °C to °F or duplicate a timestamp and verify rejection rather than silent reinterpretation.
- Parse the generated MIDI using an independent implementation such as [Mido](https://mido.github.io/mido/files/midi.html). Check file type, track count, ticks per beat, total duration, note counts, nonnegative deltas, and balanced note-on/note-off events. Consult the [MIDI Association's file specification](https://midi.org/standard-midi-files-specification) when implementing serialization.
- In interaction tests, exercise first use with no automatic request, city search, escaped service-provided names, adding/removing voices, hour selection, tempo changes, export initiation, missing-service data, cancellation, and storage/import failures.
- Test invalid imported units and timestamps before state replacement. Test a delayed import resolving after a newer user action. Test a mixture of imported and newly fetched snapshots and inspect each provenance label.
- Mocked audio tests can verify scheduling and cleanup, but they do not establish subjective sound quality, device latency, or real-browser autoplay behavior. Listen at a comfortable level and inspect desktop/mobile layouts when the environment permits; report unverified stages accurately.

## Reference-build result

Weather Choir fetched real hourly forecast and geocoding responses and verified CORS headers from both services. A real Tokyo snapshot produced a complete 24-hour score with no missing hours; its exact note count reflects that snapshot, not a fixed benchmark. Pure-model and simulated-DOM/audio tests passed, including mixed-provenance and stale-import cases. An independent MIDI parser verified the fixture's 60-second duration and balanced note events. Real-browser visual QA and subjective listening were not completed at contribution time.

## Delivery and attribution

Deliver the runnable app separately, its source snapshot/MIDI capability, and the meaningful verification limits. Retain provider attribution and license links in the interface and portable outputs, and check current service-use terms before public or commercial deployment. For this repository contribution, publish only SKILL.md. Do not include product code, test files, account details, or build notes here.
