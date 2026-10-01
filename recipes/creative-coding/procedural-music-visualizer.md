---
id: procedural-music-visualizer
title: "Procedural Music Visualizer"
summary: "Create a seeded music-and-motion sketch whose notes and visuals share an inspectable event timeline."
category: creative-coding
level: intermediate
timebox_minutes: 120
capabilities: ["code", "files", "websites"]
tags: ["audio", "generative-art", "synchronization"]
status: recipe-not-run
---

# Procedural Music Visualizer

Create a seeded music-and-motion sketch whose notes and visuals share an inspectable event timeline.

## Scenario

An engineer curious about creative coding wants a small project that connects event scheduling, deterministic randomness, and animation. A generated melody with matching visual marks makes those concepts audible and visible. The first version should use original synthesized notes, predictable controls, and a silent alternative for people who prefer it.

## Inputs to prepare

- [SEED] and finite composition duration
- [TEMPO] and allowed note set
- [VISUAL MAPPING] from notes to shapes
- [PALETTE] and motion-intensity preference

## Copy this prompt into dot

```text
dot, build a procedural music visualizer using [SEED], [TEMPO], [VISUAL MAPPING], and [PALETTE], if coding and browser tools are available. Use browser Web Audio for original synthesized notes and Canvas or SVG for the graphics. First create an inspectable event list for a short finite composition, then make both sound and visuals read from that same list.

Explain how note time, duration, pitch, and intensity map to visible properties. Use deterministic randomness so the same seed and settings reproduce the same events. Provide explicit start, pause, stop, reset, mute, and volume controls. Sound must begin only after a user gesture, start quietly, and have bounded gain. Include a silent mode with text descriptions, reduced motion, and no rapid flashing.

Deliver editable source, parameter presets, the event timeline as JSON, a still-image export where supported, and a test checklist. Check repeated start clicks, pause and resume, background-tab suspension, zero-duration input, invalid note sets, and the final event ending cleanly. Reset must cancel pending sound and animation work before rebuilding the timeline. Do not claim sample-accurate visual synchronization across devices. Use no uploaded music or external audio services by default. Keep previews private and ask before publication or adding analytics. Mark any browser audio checks you cannot execute.
```

## Iterate with a purpose

### 1. Add a compositional structure

```text
Add an original three-section composition with a repeated motif, using explicit section boundaries in the event JSON and visible transitions that respect reduced-motion mode.
```

### 2. Compare mappings

```text
Create two visual mappings from the identical event timeline and a side-by-side silent comparison so musical changes are not confused with visual changes.
```

### 3. Explore local recording

```text
Check available browser recording or offline rendering support and propose a local export workflow; only create supported formats and document timing and codec limitations.
```

## Expected deliverables

- Editable browser audio-and-graphics source
- Seeded parameter presets and event-timeline JSON
- Control and mapping guide
- Conditional still-image export
- Audio lifecycle and synchronization test checklist

## Acceptance checks

- The same seed and parameters reproduce an identical ordered event list
- No audio starts before an explicit user interaction
- Repeated start clicks do not create overlapping playback engines
- Stop and reset cancel pending notes and visible animation
- Invalid note sets and zero duration produce clear validation messages
- Silent and reduced-motion modes preserve the composition structure in readable form
- The finite composition ends without lingering sound or a still-running playback indicator

## Access, privacy and stop conditions

- Audio availability and timing behavior depend on the browser and device
- Visual synchronization is not guaranteed to be sample-accurate
- Use original synthesis or separately authorized audio only
- Recording, external upload, analytics, and publication require appropriate approval

## Two possible extensions

- Add a local preset gallery with export and import validation
- Use an approved MIDI input device only after reviewing browser permissions
