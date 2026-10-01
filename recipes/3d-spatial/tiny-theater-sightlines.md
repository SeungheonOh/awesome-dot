---
id: tiny-theater-sightlines
title: "Tiny Theater Sightline Explorer"
summary: "Build a geometric sightline study that makes seat, eye-height, and obstruction assumptions inspectable."
category: 3d-spatial
level: advanced
timebox_minutes: 150
capabilities: ["code", "files"]
tags: ["ray-testing", "seating", "geometry"]
status: recipe-not-run
---

# Tiny Theater Sightline Explorer

Build a geometric sightline study that makes seat, eye-height, and obstruction assumptions inspectable.

## Scenario

An engineering study group wants a concrete introduction to geometric intersection tests. A fictional tiny theater provides seats, viewing points, and simple obstructions. The goal is to compare layouts and explain blocked lines of sight, not to certify a real venue or infer what every audience member can see.

## Inputs to prepare

- [ROOM AND STAGE DIMENSIONS] in meters
- [SEAT COORDINATES] with stable seat identifiers
- [EYE HEIGHT OPTIONS] and stage target points
- [OBSTRUCTION GEOMETRY] and desired comparison layouts

## Copy this prompt into dot

```text
dot, create Tiny Theater Sightline Explorer using [ROOM AND STAGE DIMENSIONS], [SEAT COORDINATES], [EYE HEIGHT OPTIONS], and [OBSTRUCTION GEOMETRY]. The required toolchain is Blender with Python scripting and segment-intersection support. Verify it is available; otherwise provide input templates, diagrams where supported, and clearly unexecuted calculation source. Ask before installing anything.

Start with one seat, one stage target, and one rectangular obstruction so the intersection rule is easy to review. Then extend the same rule to all seats and supplied eye heights. Test only the finite segment between each eye point and target, not an infinite ray. Report which obstruction blocks each segment and preserve stable seat identifiers across layouts. Do not interpret geometric visibility as guaranteed human visibility or regulatory compliance.

Target editable JSON geometry, a Python scene-and-analysis script, per-seat CSV results, a top-view SVG, and a Blender scene or PNG views only if supported. Use meters consistently and show assumptions for head proxies, if any. Check targets behind the viewer, eye points inside an obstruction, duplicate seat identifiers, touching-edge tolerance, and an empty seating list. Include a simple manually calculated fixture to compare with software results. Keep all venue information fictional or sanitized. Ask before sharing, publication, or making real seating changes; label unexecuted checks.
```

## Iterate with a purpose

### 1. Compare eye-height assumptions

```text
Run the same layout across my supplied eye-height range and show which seats change classification, without assigning those heights to demographic groups.
```

### 2. Explain blocked paths

```text
Add a selected-seat view that highlights the first intersected obstruction and labels the exact segment endpoints and tolerance.
```

### 3. Compare layout tradeoffs

```text
Compare two supplied seating layouts using the same targets and obstruction model, showing seat count and blocked-path counts without declaring legal compliance.
```

## Expected deliverables

- JSON geometry and stable seat identifiers
- Editable Python analysis and scene script
- Per-seat, per-target CSV visibility results if executed
- SVG plan and conditional scene or PNG views
- Manual fixture and tolerance-validation notes

## Acceptance checks

- The one-seat fixture matches its independently calculated blocked or clear result
- Objects beyond the target do not incorrectly block a finite sightline
- Duplicate seat identifiers are rejected before results are joined
- An empty seating list yields a valid empty result with a helpful explanation
- Eye points inside obstructions are flagged as invalid input
- Touching-edge cases follow a stated tolerance rule
- Every reported blockage names the seat, target, eye height, and obstructing object

## Access, privacy and stop conditions

- Geometric segments do not model perception, crowd movement, or all body shapes
- Results do not certify accessibility, occupancy, or venue safety
- Blender, intersection support, and exports depend on the available environment
- Real venue plans and external sharing require appropriate authorization

## Two possible extensions

- Explore stepped seating as a separate geometry study
- Create a worksheet explaining finite-segment versus infinite-ray tests
