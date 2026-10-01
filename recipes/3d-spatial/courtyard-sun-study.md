---
id: courtyard-sun-study
title: "Courtyard Shadow Study"
summary: "Build a reproducible conceptual shadow comparison using explicitly supplied solar directions."
category: 3d-spatial
level: advanced
timebox_minutes: 150
capabilities: ["code", "files"]
tags: ["lighting", "architecture-study", "shadows"]
status: recipe-not-run
---

# Courtyard Shadow Study

Build a reproducible conceptual shadow comparison using explicitly supplied solar directions.

## Scenario

A design student is comparing where to place seating in an imaginary courtyard. They want to understand how walls and trees change shade across several sun positions. A useful study should expose its assumptions and compare the same geometry consistently, without claiming site-accurate daylight or thermal performance.

## Inputs to prepare

- [COURTYARD GEOMETRY] and obstruction heights
- [SOLAR AZIMUTH AND ELEVATION PAIRS] in degrees
- [SEATING OPTIONS] as coordinates and footprints
- [MATERIAL ASSUMPTIONS] and image resolution

## Copy this prompt into dot

```text
dot, create a conceptual courtyard shadow study using [COURTYARD GEOMETRY], [SOLAR AZIMUTH AND ELEVATION PAIRS], [SEATING OPTIONS], and [MATERIAL ASSUMPTIONS]. This requires an available Blender Python toolchain and renderer. Confirm support before promising a scene or images; if missing, provide a coordinate table and unexecuted scene script, and ask before installing anything.

Use my supplied solar directions instead of inventing location-accurate sun positions. State azimuth orientation, elevation convention, units, north direction, and whether trees are opaque proxy volumes. Create one consistent camera and render settings across all variants. Compare the same seating footprints under each light direction, with labeled shadow views and a summary of approximate shaded area where a reproducible measurement method is available. Otherwise report a qualitative comparison and its limits.

Target readable input JSON, an editable scene or scene-generation .py script, and PNG comparison images only when rendering succeeds. Include the calculation or sampling method behind any percentages. Test a sun below the horizon, zero-height obstacles, duplicate seating coordinates, and swapped north orientation. Separate geometry checks from physical daylight claims. This is not an energy, glare, heat-safety, or building-code assessment. Use fictional or sanitized geometry; ask before publication, external sharing, or uploading site plans. Clearly label unrendered outputs and unverified checks.
```

## Iterate with a purpose

### 1. Compare shade structures

```text
Add two conceptual canopy geometries and compare them using the unchanged solar directions, camera, and measurement method.
```

### 2. Run a sampling sensitivity check

```text
Repeat shaded-area estimates at two sampling resolutions and report how much the result changes before recommending a working resolution.
```

### 3. Prepare a critique board

```text
Arrange the successful renders into a labeled comparison board with assumptions and unanswered design questions, keeping approximate results clearly marked.
```

## Expected deliverables

- Coordinate and solar-direction input JSON
- Scene-generation Python script and supported editable scene
- Consistently framed PNG comparisons if rendered
- Reproducible shade-measurement method or qualitative limits
- Assumption and edge-case report

## Acceptance checks

- Every image identifies its azimuth, elevation, north convention, and seating option
- All comparisons preserve camera, geometry scale, and render settings except the intended variable
- Below-horizon sun inputs are rejected or explicitly classified without false daytime shadows
- Zero-height obstructions produce no unintended elevated geometry
- Any shaded-area percentage is traceable to a disclosed sampling method
- Reversing north changes the light orientation predictably in a test case
- Unsupported rendering and measurement steps remain marked unverified

## Access, privacy and stop conditions

- Site-accurate solar positions are not assumed from fictional inputs
- Blender and rendering support must be available; outputs are conditional
- Opaque tree proxies omit foliage, seasonal, and atmospheric effects
- The study is not professional daylight, thermal, or code-compliance advice

## Two possible extensions

- Replace fictional solar directions with independently verified site inputs
- Add a seasonal comparison only after its assumptions are reviewed
