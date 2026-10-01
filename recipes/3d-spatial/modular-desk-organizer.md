---
id: modular-desk-organizer
title: "Parametric Desk Organizer Study"
summary: "Develop a dimensioned parametric organizer concept with editable source and conditional mesh exports."
category: 3d-spatial
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files"]
tags: ["parametric", "desktop", "fabrication-study"]
status: recipe-not-run
---

# Parametric Desk Organizer Study

Develop a dimensioned parametric organizer concept with editable source and conditional mesh exports.

## Scenario

A maker wants shallow trays that fit an awkward desk drawer and hold a few measured objects. They need to compare compartment arrangements before printing anything. The useful outcome is a clearly dimensioned design study with adjustable walls and gaps, rather than a promise that an untested model will fit or print.

## Inputs to prepare

- [DRAWER INNER DIMENSIONS] in millimeters
- [OBJECT DIMENSIONS] for three to six items
- [WALL THICKNESS] and desired clearance
- [MODULE COUNT] and preferred compartment layout

## Copy this prompt into dot

```text
dot, help me create a parametric desk-organizer study using [DRAWER INNER DIMENSIONS], [OBJECT DIMENSIONS], [WALL THICKNESS], and [MODULE COUNT]. The required modeling toolchain is an available OpenSCAD installation with command-line rendering; verify availability before promising geometry or exports. If it is missing, deliver the parameter table, dimensioned design brief, and editable source as unexecuted code, and ask before installing software.

Use millimeters throughout. Propose two compartment layouts and explain the tradeoff between storage area, finger access, and wall thickness. After I choose, create readable .scad source with named dimensions and assertions for impossible combinations. Target separate STL mesh files per module and a top-view SVG only if the installed toolchain supports successful export. Do not imply that these are native mechanical CAD files or manufacturing-approved parts.

Include a dimension schedule, source-editing guide, and export log. Where tools permit, inspect bounding boxes, positive wall thickness, nonintersecting compartments, and mesh closure. Test an object wider than its compartment and a drawer too small for the requested modules. Label checks that need physical measurement or a trial print. Use generic objects without logos or personal labels. Keep files private and ask before upload, publication, fabrication orders, or printer operation.
```

## Iterate with a purpose

### 1. Compare clearance variants

```text
Generate three parameter variants around my chosen clearance, preserving outer dimensions, and show the resulting usable compartment sizes.
```

### 2. Add label inserts

```text
Design removable label-slot concepts with separate source parameters and a small fit-test coupon before changing the main trays.
```

### 3. Prepare a trial-print plan

```text
Create a low-material test plan for one corner and one divider, with the measurements I should record before printing complete modules.
```

## Expected deliverables

- Editable .scad source with a parameter table
- Two layout concepts and chosen dimension schedule
- STL modules and top-view SVG if successfully supported
- Export and geometry-check log with unverified items labeled
- Physical fit-test checklist

## Acceptance checks

- The documented outer dimensions fit within the supplied drawer dimensions with the requested clearance
- Changing module count updates the layout without silently overlapping modules
- Nonpositive wall thickness and impossible object sizes produce clear validation errors
- Exported mesh bounds match the source unit convention
- Where mesh tools are available, closure and self-intersection checks are reported explicitly
- Any unexecuted export is listed as pending rather than represented as a completed file

## Access, privacy and stop conditions

- OpenSCAD and mesh inspection must be available; installation needs authorization
- STL is a mesh format, not guaranteed native CAD or manufacturing certification
- Printer tolerances, material strength, and real fit require physical testing
- Uploading files or operating fabrication equipment requires separate approval

## Two possible extensions

- Explore a removable divider system after a successful fit test
- Create a parameter preset for a second measured drawer
