---
id: plotter-art-workbench
title: "Plotter Art Workbench"
summary: "Create reproducible vector line art with physical dimensions, pen layers, and inspectable path order."
category: creative-coding
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files", "websites"]
tags: ["vector-art", "plotter", "geometry"]
status: recipe-not-run
---

# Plotter Art Workbench

Create reproducible vector line art with physical dimensions, pen layers, and inspectable path order.

## Scenario

A maker wants original line drawings for a pen plotter but would like to inspect the files before connecting hardware. The project is a practical introduction to coordinate systems, clipping, and path ordering. It should produce clean vectors with a repeatable seed and avoid assuming that a preview proves machine compatibility.

## Inputs to prepare

- [PAGE WIDTH AND HEIGHT] in millimeters
- [DRAWABLE MARGINS] and pen-count limit
- [SEED] and preferred geometric motif
- [PEN WIDTH] and minimum line-spacing target

## Copy this prompt into dot

```text
dot, build Plotter Art Workbench using [PAGE WIDTH AND HEIGHT], [DRAWABLE MARGINS], [SEED], and [PEN WIDTH]. Use an available Python or browser vector-generation toolchain and export plain SVG. Confirm what can be executed locally before promising files; ask before installing dependencies. Do not connect to or operate a plotter.

Start with one original geometric motif and a visible page boundary, then add bounded seeded variation. Express the SVG dimensions in millimeters with a matching viewBox and keep the origin convention documented. Represent pen passes as clearly named layers or groups, using strokes rather than filled raster images. Keep all drawing paths inside the approved drawable rectangle and report estimated path length and pen-lift count using a disclosed method.

Deliver editable source, three seed presets, SVG artwork, a path-order preview, and a parameter manifest. Include a calibration square on a separate test sheet. Check zero-length segments, duplicate paths, out-of-bounds coordinates, unsupported curves, impossible margins, and a pen width larger than the requested line gap. Compare optimized and original path order while preserving the actual geometry. Do not generate device commands or claim hardware compatibility without a separately reviewed target format. Keep output private and ask before publication, uploading artwork, purchasing supplies, or operating any equipment. Mark unexecuted export and geometry checks.
```

## Iterate with a purpose

### 1. Compare path-order strategies

```text
Implement two path-order strategies on identical geometry and compare estimated travel distance, pen lifts, and preserved endpoints without operating hardware.
```

### 2. Design a two-pen edition

```text
Add a two-pen version with explicit group names and a registration test sheet, keeping color-independent group labels for review.
```

### 3. Prepare a machine-specific review

```text
After I provide a target device and approved documentation, identify its format and size constraints and prepare a compatibility checklist before proposing any conversion or operation.
```

## Expected deliverables

- Editable vector-generation source
- Three deterministic seed presets
- SVG artwork with physical dimensions and pen groups
- Separate calibration test sheet
- Path-order preview and length-estimation report

## Acceptance checks

- The SVG physical dimensions and viewBox share a consistent scale
- Every drawing path stays inside the supplied drawable rectangle
- Identical seeds and parameters reproduce identical geometry
- Zero-length and duplicate segments are detected before final export
- Impossible margins and incompatible pen-gap choices produce readable validation messages
- Path reordering preserves geometry while reporting travel changes
- No device-control commands or hardware operation occur as part of the recipe

## Access, privacy and stop conditions

- SVG support does not imply compatibility with a particular plotter or driver
- Estimated pen travel omits unmodeled acceleration and mechanical delays
- Physical line spacing depends on paper, ink, pen, and calibration
- Hardware control, purchases, external uploads, and publication require approval

## Two possible extensions

- Create a human-reviewed physical calibration log after an authorized test
- Add a new geometric motif while keeping the same export contract
