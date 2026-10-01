---
id: kinetic-paper-mobile
title: "Kinetic Paper Mobile Study"
summary: "Create a paper-mobile balance concept with flat patterns and a labeled assembly visualization."
category: 3d-spatial
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files"]
tags: ["kinetic-art", "paper-craft", "balance"]
status: recipe-not-run
---

# Kinetic Paper Mobile Study

Create a paper-mobile balance concept with flat patterns and a labeled assembly visualization.

## Scenario

An art teacher is planning a lightweight paper mobile exercise using fictional shapes and simple balance relationships. They want students to compare arrangements before cutting materials. The prototype should provide flat shapes and a clear balance explanation while leaving real hanging strength, hardware, and classroom safety to human review.

## Inputs to prepare

- [SHAPE SET] and desired overall span
- [PAPER AREAL DENSITY] or measured piece masses
- [ARM LENGTH LIMITS] and attachment positions
- [ASSEMBLY STYLE] and allowable number of tiers

## Copy this prompt into dot

```text
dot, develop a lightweight paper-mobile design study using [SHAPE SET], [PAPER AREAL DENSITY], [ARM LENGTH LIMITS], and [ASSEMBLY STYLE]. The required toolchain is Python for area and torque calculations plus Blender for an optional 3D assembly view. Verify available libraries and Blender before promising outputs; ask before installing software. If only Python is available, deliver the calculations and flat patterns without implying a completed 3D scene.

Propose two arrangements of original simple shapes. Estimate masses from area only when the supplied material assumption supports it, and include the modeled mass of arms and connectors where known. Show each balance equation and flag missing masses. Use a consistent unit system and identify idealized joints and static assumptions. Avoid promising stable real-world motion or load-bearing safety.

Target editable SVG cut patterns with scale markers, a CSV mass-and-lever table, calculation source, and an assembly .blend file or PNG views only if supported. Check torque balance within an explicit tolerance, overlapping cut patterns, zero-mass inputs, attachment points outside an arm, and an impossible span limit. Provide a manual trial-balancing checklist. Keep the design small and lightweight; do not operate cutters, buy hardware, or publish files without approval. Mark untested physical behavior and unsupported exports clearly.
```

## Iterate with a purpose

### 1. Compare material changes

```text
Recalculate the chosen arrangement for a second supplied paper density, keeping geometry fixed and showing which attachment positions change.
```

### 2. Make adjustable prototypes

```text
Add several clearly labeled candidate attachment positions to a paper test template, with instructions for recording observed balance before finalizing the design.
```

### 3. Create an assembly sequence

```text
Produce a numbered assembly visualization that distinguishes supplied measurements from idealized assumptions and flags points needing adult or instructor review.
```

## Expected deliverables

- Two mobile arrangements with balance equations
- SVG flat patterns with calibration marks
- CSV mass, lever-arm, and torque table
- Calculation source and conditional 3D scene or renders
- Physical trial-balancing checklist

## Acceptance checks

- Every included piece has a stated measured or estimated mass source
- Torque residuals are shown with units and compared against the chosen tolerance
- Zero or missing mass is handled explicitly rather than divided through
- Attachment points outside the permitted arm range are rejected
- Flat patterns include a measurable scale marker and do not overlap unintentionally
- An impossible span constraint produces a conflict report
- Rendered views, if available, match the calculation geometry

## Access, privacy and stop conditions

- Static idealized balance does not certify dynamic stability or hanging safety
- Blender views and native scene files depend on available software
- Material estimates omit unprovided glue, string, moisture, and connector variation
- Cutting equipment, installation, purchases, and publication require approval

## Two possible extensions

- Create a classroom worksheet comparing predicted and observed balance
- Explore a freestanding display concept for human safety review
