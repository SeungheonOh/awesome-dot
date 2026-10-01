---
id: exploded-lamp-study
title: "Exploded Lamp Assembly Study"
summary: "Create a reversible exploded-view illustration from a fictional nonfunctional lamp assembly."
category: 3d-spatial
level: intermediate
timebox_minutes: 120
capabilities: ["code", "files"]
tags: ["assembly", "technical-illustration", "hierarchies"]
status: recipe-not-run
---

# Exploded Lamp Assembly Study

Create a reversible exploded-view illustration from a fictional nonfunctional lamp assembly.

## Scenario

An engineer learning 3D communication wants to explain how a small product is arranged without producing a manufacturing drawing. A fictional lamp-shaped object has a base, stem, shell, and decorative cover. The study should preserve part identity between assembled and exploded views and make the illustration easy to revise.

## Inputs to prepare

- [PART LIST] with simple dimensions and stable identifiers
- [ASSEMBLY ORDER] and parent-child relationships
- [EXPLOSION DIRECTION] and spacing limits
- [LABEL STYLE] and intended page dimensions

## Copy this prompt into dot

```text
dot, create an exploded-view illustration of a fictional nonfunctional lamp-shaped assembly using [PART LIST], [ASSEMBLY ORDER], [EXPLOSION DIRECTION], and [LABEL STYLE]. The required toolchain is Blender with Python scripting and a supported renderer; verify it first. If unavailable, deliver part data, an illustration plan, and clearly unexecuted scene source. Ask before installing software.

Use simple proxy geometry for a base, stem, shell, and decorative cover. Do not design wiring, mains connections, heat management, or load-bearing hardware. Assign stable part identifiers and store assembled transforms separately from explosion offsets. Start with a four-part proof of concept, then add only parts I explicitly supply. A single parameter should move the model between assembled and exploded states without changing dimensions or creating duplicate parts.

Target editable part JSON, a generation .py script, a .blend scene if supported, labeled PNG views if rendered, and a parts-list CSV. Use the same camera and scale for assembled and exploded comparisons. Check duplicate identifiers, missing parent references, zero explosion distance, negative spacing, overlapping labels, and exact restoration of assembled transforms. Include an unlabelled view for checking geometry separately from typography. Keep files private and ask before uploading or publishing. This is a communication prototype, not an electrical design, assembly instruction approved for real hardware, or guaranteed native CAD export.
```

## Iterate with a purpose

### 1. Compare explosion layouts

```text
Create axial and stepped explosion variants from the same stored transforms, then compare label crossings and view clarity.
```

### 2. Add a reversible animation

```text
If animation tools are available, produce a short assembled-to-exploded loop and verify that both endpoints match the corresponding still states.
```

### 3. Prepare a technical review sheet

```text
Create a two-view review sheet with the parts list, orientation references, and explicitly unresolved dimensional questions for human review.
```

## Expected deliverables

- Stable part inventory and assembly relationships in JSON
- Readable scene-generation source
- Conditional editable Blender scene and labeled PNG views
- Parts-list CSV and unlabeled geometry view
- Transform-restoration and label-check report

## Acceptance checks

- Every supplied part identifier appears once in the scene and parts list
- Missing parent references and duplicate identifiers are rejected
- Zero explosion distance reproduces all stored assembled transforms
- Changing explosion spacing preserves part dimensions and orientation unless explicitly specified
- Negative spacing is rejected or handled by a documented intentional rule
- Labels remain associated with their original parts in each view
- Assembled and exploded images use the same camera and scale

## Access, privacy and stop conditions

- The fictional object is nonfunctional and contains no validated electrical design
- Blender scenes and renders depend on available software
- Illustrative geometry is not manufacturing CAD or hardware assembly approval
- Animation, uploads, publication, and software installation require available tools and appropriate approval

## Two possible extensions

- Apply the same transform system to a different supplied educational assembly
- Create a print-friendly monochrome illustration variant
