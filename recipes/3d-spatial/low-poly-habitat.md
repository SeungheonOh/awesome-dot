---
id: low-poly-habitat
title: "Low-Poly Habitat Scene"
summary: "Build an original low-poly scene with organized objects, a performance budget, and conditional web-ready exports."
category: 3d-spatial
level: beginner
timebox_minutes: 100
capabilities: ["code", "files"]
tags: ["low-poly", "scene-design", "asset-pipeline"]
status: recipe-not-run
---

# Low-Poly Habitat Scene

Build an original low-poly scene with organized objects, a performance budget, and conditional web-ready exports.

## Scenario

A software team wants a friendly first project for learning how small 3D assets are organized and exported. An imaginary habitat can combine terrain, shelter, and vegetation without needing photorealism. The team cares about editable geometry, a modest polygon budget, and a reliable way to check what survives export.

## Inputs to prepare

- [HABITAT THEME] and three focal objects
- [POLYGON BUDGET] and texture-size limit
- [PALETTE] and intended viewing angle
- [TARGET VIEWER] and desired scene dimensions

## Copy this prompt into dot

```text
dot, create an original low-poly habitat study using [HABITAT THEME], [POLYGON BUDGET], [PALETTE], and [TARGET VIEWER]. The required modeling toolchain is Blender with Python scripting and a working glTF exporter. Check availability before committing to scene files or exports; if unavailable, deliver an asset list, scene specification, and unexecuted generation script. Ask before installing software or fetching asset libraries.

Start with a three-object gray-box layout so I can review scale and composition. Then build simple original meshes for terrain, shelter, and vegetation, using a small material palette and clear object names. Keep every object editable and group related pieces. State units, up axis, origin, pivot choices, triangle-count method, and whether the budget includes hidden geometry.

Target a .blend scene, a readable .py generation script, an asset inventory CSV, and a GLB file only if export succeeds. Render PNG overview images where supported. Reopen the exported file in an available compatible viewer and compare object count, bounds, material appearance, and transparency; do not assume source and export match. Check missing materials, inverted faces, empty meshes, and one intentionally over-budget variant. Avoid unlicensed assets, copied franchise designs, and hidden network dependencies. Keep previews private and ask before publishing. Mark viewer, export, or rendering checks that remain unverified.
```

## Iterate with a purpose

### 1. Create a day-night variant

```text
Add a second lighting setup using the same geometry and materials, then compare visibility and export behavior without doubling the asset inventory.
```

### 2. Reduce geometry deliberately

```text
Create a lower-detail variant, report triangle savings per object, and compare silhouettes at the intended viewing distance.
```

### 3. Build an inspection page

```text
If web tools are available, prepare a private local viewer with orbit controls, a reset camera button, and an asset-information panel before asking about publication.
```

## Expected deliverables

- Gray-box layout and original asset plan
- Editable generation script and conditional Blender scene
- Asset inventory with dimensions and triangle counts
- Conditional GLB export and PNG overview images
- Source-versus-export comparison log

## Acceptance checks

- The counted scene triangles remain within the chosen budget or an explicit exception is reported
- Every scene object has a stable descriptive name and inventory row
- Empty meshes and missing materials are flagged before export
- The exported scene, if reopened successfully, retains expected bounds and orientation
- Inverted-face test geometry is detected or clearly identified as an unverified check
- No external asset or font dependency is silently introduced
- The camera can return to the documented overview position

## Access, privacy and stop conditions

- Blender, glTF export, and a compatible viewer must be available for the full pipeline
- Material and lighting appearance can vary across viewers
- GLB is a scene-delivery format, not guaranteed native CAD
- External assets, software installation, and publication require approval

## Two possible extensions

- Add one simple animation with an explicit loop and export test
- Create a second habitat sharing the same scale and material conventions
