---
name: seeded-contour-print-studio
description: Build a reproducible generative contour-art app that exports physical-size SVG prints, with tested interpolation and path joining. Use for creative vector-print tools rather than geographic or scientific contour claims.
---

# Seeded contour print studio

Create a small instrument for finding imaginary landscapes and exporting editable vector prints. The output is artwork, not an elevation survey. Make the seed and complete rendering recipe reproducible instead of producing an attractive but unrepeatable preview.

## Direction and inputs

Agree on a physical page size, margins, ink palettes, bounded sampling resolution and export format. The worked implementation used A4 portrait, 18 mm centerline margins, 4–40 contours, and a 24–160-column grid. These are design choices, not universal requirements. No live service or personal data is needed.

Keep publication separate from local creation. A request to experiment does not automatically authorize public hosting. If contributing to a skills-only repository, contribute the workflow alone; keep app sources, tests and sample art in a separate deliverable.

## Chronological workflow

1. Start with a seeded scalar field. Use an explicit pseudo-random generator and retain its algorithm version. A useful field combines several Gaussian bumps with low-amplitude sine waves. Normalize sampled values before choosing evenly spaced interior contour levels. Do not put random calls in the rendering loop or regenerate on unrelated UI events.
2. Solve topology before styling. Split each grid cell into two triangles, alternating the diagonal by cell parity. Each triangle has an unambiguous linear field; contour crossings interpolate along its edges. This avoids a marching-squares saddle decision, but the triangulation influences the approximation. Tell users that increasing sampling detail changes geometry.
3. Give intersections logical identities. Use the sorted pair of grid-vertex IDs for an edge crossing. When a crossing lands exactly on a vertex, use that vertex's ID instead. Do not join paths by rounding floating-point coordinates: nearby contours can be accidentally fused. Ignore zero-length segments caused by an exact vertex hit.
4. Stitch segments as a graph. Walk from endpoints or branch nodes until the next endpoint/branch; then consume remaining degree-two loops. Mark every edge used exactly once. A branch should split paths rather than invent a connection. Plateaus at exactly the chosen level need an explicit convention; the worked implementation uses a consistent greater-than-or-equal classification and emits no flat-area contour.
5. Map normalized coordinates into the physical drawing rectangle. SVG width and height use millimeters, while the viewBox matches those units. Preserve the numeric geometry in export. Offer a paper rectangle for presentation and a line-only option for design tools. Line-only export is not a promise of optimized pen travel.
6. Design the app around a preview and a short recipe: seed, contour count, sampling detail, line width and palette. Show continuous-path count and total physical line length. Clearly distinguish procedural art from real geographic data.
7. Make changed controls visibly dirty. Disable exports until a new print is generated. If validation fails, preserve the last valid preview but keep exports disabled so the user cannot accidentally export an old result under new settings. Presets and a new-seed button should update controls and preview together.
8. Export both SVG and a compact versioned recipe. Use validated numeric settings and palette constants when constructing SVG; do not interpolate arbitrary user strings into markup. Keep titles/descriptions useful and free of confidential context. Revoke object URLs after requesting downloads.
9. Render a representative exported SVG with an independent SVG renderer. Inspect actual pixels for broken joins, clipping, unexpected fills and physical proportions. This checks the export, not the entire web interface. Test the UI separately in a real browser when a permitted preview is available.

## Geometry checks that matter

A plane with value x should produce one straight contour at x = level, spanning the vertical domain. A sampled radial field should give a closed interior loop close to the analytical circle. These two fixtures reveal interpolation and joining errors more clearly than random art.

Check edge conservation: the sum of path segment counts must equal the number of generated segments. Every coordinate must stay finite and inside the normalized domain. Test zero/flat fields, levels exactly through grid vertices, open boundaries, closed loops, seed extremes, minimum/maximum resolution, and deterministic reproduction. Changing only ink or line width must not change contour coordinates.

For the interface, test initial generation, dirty export guards, invalid settings preserving the prior print, recovery through a preset, paper on/off, and both download contents. A download status label only proves a request was made; inspect the saved bytes when the browser supports it.

## Worked outcome and limits

Contour Press implemented this workflow with eight Gaussian bumps and two wave terms. Its model checks passed analytical planes, a radial loop, plateaus, seeded reproduction, bounded geometry and segment conservation across 100 seeded contour graphs. Simulated-DOM checks passed initial art, dirty controls, regeneration, line-only SVG, invalid-input preservation, preset recovery and recipe export. The generated A4 SVG was rasterized with CairoSVG and visually inspected: continuous contours, open boundary ends and the intended blank margins were visible.

Actual browser layout, physical printing and pen-plotter behavior were not established by those checks. Keep those limits explicit for a new build. Never label a print physically calibrated merely because its SVG declares millimeters; print scaling and device margins remain user/device settings.

## Delivery

Provide the app and at least one actual SVG with its recipe or seed. State which geometry, interface and rendering checks passed. Publish only to the destination the user approved. A reusable skill contribution should describe the non-obvious construction and verification decisions, not claim the example's test results automatically apply to another implementation.
