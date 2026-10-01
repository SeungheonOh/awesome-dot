---
id: ceramic-profile-lab
title: "Ceramic Profile Shape Lab"
summary: "Create a family of rotational vessel concepts from editable cross-section profiles."
category: 3d-spatial
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files"]
tags: ["parametric", "surfaces-of-revolution", "craft-study"]
status: recipe-not-run
---

# Ceramic Profile Shape Lab

Create a family of rotational vessel concepts from editable cross-section profiles.

## Scenario

A ceramics hobbyist wants to compare vase silhouettes before spending time on clay prototypes. They have a few height and width targets but no CAD background. A profile-based model makes the relationship between a simple curve and a three-dimensional form visible, while keeping practical ceramic production questions separate.

## Inputs to prepare

- [PROFILE POINTS] or a plain-language silhouette description
- [HEIGHT AND DIAMETER LIMITS] in millimeters
- [WALL THICKNESS] and base thickness
- [VARIANT COUNT] and optional supplied shrinkage assumption

## Copy this prompt into dot

```text
dot, help me build Ceramic Profile Shape Lab from [PROFILE POINTS], [HEIGHT AND DIAMETER LIMITS], [WALL THICKNESS], and [VARIANT COUNT]. The required 3D toolchain is Blender with Python mesh generation; verify availability first. If unavailable, prepare profile SVGs, parameter JSON, and unexecuted generation source, and ask before installing software.

Begin with one labeled cross-section and explain how rotating it around an axis creates the outer surface. After I approve the profile, create a small family of distinct silhouettes while preserving the stated size limits. Model an inner cavity and base explicitly rather than presenting a solid exterior as a usable vessel. Document how radial wall offsets differ from true normal thickness on sloped walls, and avoid unsupported thickness guarantees.

Target editable profile SVGs, parameter JSON, a .py generator, and a .blend scene with OBJ or STL meshes only when supported exports succeed. Provide common-view PNG comparisons if rendering is available. Check reversed point order, self-crossing profiles, zero-radius sections, a neck narrower than twice the requested wall offset, and a base thicker than the vessel height. Report mesh closure and dimensions where tools permit. Any shrinkage scaling must use my supplied assumption and remain provisional. This is a visual form study, not food-safety, kiln, or structural advice. Ask before fabrication, external upload, or publication.
```

## Iterate with a purpose

### 1. Compare curvature changes

```text
Create three variants that change only one profile control point and explain the resulting silhouette differences using the same scale and camera.
```

### 2. Measure approximate capacity

```text
If a closed valid cavity mesh is available, estimate its volume with a disclosed method and units, then compare it against a simple cylinder fixture.
```

### 3. Prepare a physical study sheet

```text
Create a dimensioned sheet for small clay test pieces with spaces to record measured shrinkage and observed wall thickness before any full-size build.
```

## Expected deliverables

- Editable cross-section SVGs and parameter JSON
- Readable surface-generation Python source
- Conditional Blender scene and OBJ or STL meshes
- Consistent-view comparison renders if supported
- Geometry checks and physical-production caveats

## Acceptance checks

- Every variant respects the stated height and maximum diameter limits
- The inner cavity and base are represented separately from the outer silhouette
- Self-crossing or reversed profiles receive a clear validation response
- An impossibly narrow neck is rejected rather than silently closing the cavity
- Reported thickness distinguishes radial offset from surface-normal thickness
- Supported mesh exports have documented units and checked dimensions
- Any shrinkage-adjusted variant identifies the exact supplied factor

## Access, privacy and stop conditions

- A visual mesh is not native manufacturing CAD or a validated ceramic process
- Wall offsets, clay shrinkage, firing, and material suitability require physical review
- Blender and export support may be unavailable
- Food safety, kiln operation, fabrication, and publication are outside the unapproved scope

## Two possible extensions

- Create a handle concept as a separate attachment study
- Compare supplied measurements from real test pieces against the parameter assumptions
