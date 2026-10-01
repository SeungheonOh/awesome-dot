---
id: tactile-map-model
title: "Tactile Trail Map Prototype"
summary: "Develop a raised-line map concept with separated feature layers and accessible review materials."
category: 3d-spatial
level: advanced
timebox_minutes: 150
capabilities: ["code", "files"]
tags: ["tactile", "mapping", "inclusive-design"]
status: recipe-not-run
---

# Tactile Trail Map Prototype

Develop a raised-line map concept with separated feature layers and accessible review materials.

## Scenario

A visitor-center volunteer wants to explore a tactile map of a fictional nature loop before involving users and a fabricator. The first prototype should distinguish paths, landmarks, and boundaries through height and texture. It needs inspectable dimensions and a clear record of what still requires tactile user testing.

## Inputs to prepare

- [SANITIZED PATH COORDINATES] and map extent
- [LANDMARK LIST] with short plain-language labels
- [TARGET BOARD SIZE] and feature-height ranges
- [FEATURE SPACING TARGET] and intended fabrication method

## Copy this prompt into dot

```text
dot, help me design a tactile trail-map prototype from [SANITIZED PATH COORDINATES], [LANDMARK LIST], [TARGET BOARD SIZE], and [FEATURE SPACING TARGET]. Use an available Python geometry toolchain plus OpenSCAD for solid modeling; verify both before promising meshes. If either is missing, provide layered SVG, dimension tables, and unexecuted modeling source where possible, and ask before installing software.

Create a simplified map with distinct raised paths, landmark shapes, boundary lines, and a clear orientation marker. Preserve connectivity while removing decorative detail that competes with touch. State all units, height levels, minimum gaps, and which supplied scale relationships are intentionally distorted. Do not invent Braille: reserve a separate label area and identify qualified transcription and user review as later requirements.

Target editable SVG layers, parameterized .scad source, a feature legend, and STL meshes only after successful supported export. Include a plain-language route description as an alternative to the visual map. Check disconnected paths, colliding landmarks, labels longer than their reserved area, zero-length segments, and geometry extending beyond the board. Report measurable geometry separately from tactile usability. This is a concept, not a certified accessible navigation product or a safety map. Use fictional or authorized data and ask before uploading, publishing, ordering fabrication, or operating equipment.
```

## Iterate with a purpose

### 1. Compare tactile vocabularies

```text
Prepare two geometric feature vocabularies with the same route data, then create a user-test sheet that asks about distinguishability without assuming either is accessible.
```

### 2. Build a small test coupon

```text
Create a small sample containing each proposed line width, gap, texture, and height so a fabricator and tactile readers can evaluate it before a full map.
```

### 3. Integrate reviewed labels

```text
After I supply approved label text and a qualified Braille transcription if needed, place it in the reserved areas and rerun collision checks.
```

## Expected deliverables

- Layered editable SVG and dimensional feature legend
- Parameterized OpenSCAD source
- Conditional STL mesh exports with export log
- Plain-language route description
- Tactile-review questions and unresolved requirements

## Acceptance checks

- All intended route connections remain connected after simplification
- Raised feature heights and minimum gaps match the parameter table
- Zero-length route segments are identified without generating broken solids
- Landmark and reserved-label overlaps are reported
- No geometry extends beyond the stated board bounds
- The orientation marker is distinguishable in the visual feature legend
- The report separates measured geometry from untested tactile usability

## Access, privacy and stop conditions

- The required geometry and solid-modeling toolchain may be unavailable
- Braille and accessible navigation need qualified review and user testing
- Exported meshes do not certify printability or safe wayfinding
- Use fictional data unless the map owner has authorized its use

## Two possible extensions

- Plan a structured tactile-reader feedback session
- Create a large-print companion map using the same reviewed feature data
