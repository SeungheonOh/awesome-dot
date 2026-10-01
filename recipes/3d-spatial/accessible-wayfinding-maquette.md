---
id: accessible-wayfinding-maquette
title: "Wayfinding Signage Maquette"
summary: "Build a spatial signage concept that compares placement, readable text layouts, and route choices."
category: 3d-spatial
level: advanced
timebox_minutes: 150
capabilities: ["code", "files"]
tags: ["wayfinding", "typography", "spatial-prototype"]
status: recipe-not-run
---

# Wayfinding Signage Maquette

Build a spatial signage concept that compares placement, readable text layouts, and route choices.

## Scenario

A public-space design class wants to compare signs at a fictional gallery junction. Different placements may hide destinations or make arrows ambiguous. The class needs a simple spatial model and editable sign layouts, with measured assumptions and a plan for human testing rather than claims of certified accessibility.

## Inputs to prepare

- [JUNCTION DIMENSIONS] and route geometry
- [DESTINATION NAMES] and intended route for each
- [SIGN DIMENSIONS] and mounting-height options
- [VIEWPOINTS] and an approved available font

## Copy this prompt into dot

```text
dot, develop a wayfinding-signage maquette using [JUNCTION DIMENSIONS], [DESTINATION NAMES], [SIGN DIMENSIONS], and [VIEWPOINTS]. The required toolchain is Blender with Python scripting, SVG generation, and an available font I have permission to use. Verify these before promising scene or image outputs; if unavailable, produce placement tables and editable sign-layout specifications. Ask before installing software or downloading fonts.

Begin with one junction and two destinations. Create editable sign SVGs with real text, directional arrows, and a simple room model containing sign planes. Keep sign content separate from placement data so we can change names without rebuilding the room. Compare at least two mounting positions from the same supplied viewpoints. Explain geometric occlusion and viewing angle, while avoiding claims that a render proves real-world legibility or accessibility.

Target sign SVGs, placement JSON, a scene-generation .py script, and conditional .blend and PNG outputs. Check text overflow, long destination names, conflicting arrows, signs behind obstacles, mirrored orientation, and fonts missing at render time. Include a text-only route explanation and a human review checklist for language, contrast, mounting, and actual viewing distance. Do not invent accessibility compliance or minimum legal dimensions. Use fictional places and keep previews private. Ask before publishing, sharing with a venue, or ordering signs; mark unsupported rendering and untested human factors clearly.
```

## Iterate with a purpose

### 1. Test multilingual expansion

```text
Using translations I supply or approve, create longer-text variants and show where the original sign dimensions no longer accommodate the layout.
```

### 2. Compare decision-point placement

```text
Move the same signs before, at, and after the junction, then compare their visibility from each supplied approach viewpoint.
```

### 3. Prepare a user-test kit

```text
Create a neutral route-finding test script and observation sheet for human participants, with no personal-data collection by default.
```

## Expected deliverables

- Editable sign SVGs with text and arrows
- Placement and destination data in JSON
- Scene-generation source and conditional Blender scene
- Viewpoint comparison renders if supported
- Text-only route guide and human-review checklist

## Acceptance checks

- Every destination has one explicit route and matching arrow definition
- Long labels are flagged or reflowed without silently shrinking below the chosen design size
- Missing fonts produce a visible warning and a documented fallback decision
- Signs are oriented toward their intended approach rather than mirrored or backward
- Occluded sign placements are identified from the supplied viewpoints
- Changing sign text preserves stable placement identifiers
- The report distinguishes geometric visibility from untested human legibility

## Access, privacy and stop conditions

- Accessibility and sign-code compliance require qualified human review
- Fonts must be available and licensed for the intended use
- Blender, SVG generation, rendering, and native scene output are toolchain-dependent
- Real venue data, publication, fabrication, and external sharing need approval

## Two possible extensions

- Add a tactile-sign concept with separately reviewed transcription and fabrication requirements
- Compare a second junction using the same destination naming system
