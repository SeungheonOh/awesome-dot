---
name: validate-svg-print-geometry
description: "Check a supplied generated SVG for physical page size, geometric bounds and independent render behavior before print handoff."
---

# Validate SVG print geometry

## When to use

A vector export looks correct in one preview but needs a reproducible check for intended paper size, margins and paths.

## Required inputs

- The authorized SVG and intended page dimensions/units
- Margin and clipping expectations, including stroke widths
- A permitted independent renderer and output destination

## Workflow

1. Inspect physical width/height, viewBox and coordinate transforms. Distinguish millimeters from user units and avoid assuming a screen pixel equals a physical print unit.
2. Compute or inspect path and stroke bounds under the actual transforms. A centerline inside the margin can still put half its stroke outside; state which bound is being tested.
3. Check for external resources, scripts and missing fonts. Do not execute active SVG content or fetch referenced private resources simply to render it.
4. Render with an independent suitable renderer and inspect actual pixels for clipped paths, missing labels and unexpected scale. A successful XML parse is not visual verification.
5. Return the unchanged original or an explicitly requested corrected copy, plus the page/margin result and unsupported renderer features. Physical printer scaling remains a separate check.

## Output

A print-geometry report and preview with exact page units, tested bounds and remaining renderer/printer limitations.

## Verification and limits

Check at least one known-dimension shape, full page bounds and stroke extents. Do not claim physical print fidelity from a screen preview alone.
