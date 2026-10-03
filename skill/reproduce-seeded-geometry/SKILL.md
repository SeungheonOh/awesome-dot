---
name: reproduce-seeded-geometry
description: Reproduce and compare a bounded procedural geometry run from an explicit recipe, separating numerical behavior, rendered output and export fidelity. Use for seeded generative art, streamline drawings or similar deterministic visual tools.
---

# Reproduce seeded geometry

## When to use

Use when a generated shape or drawing must be regenerated, compared after a parameter change, or exported without silently changing the geometry. The task is reproducibility and evidence for the declared model, not a claim that an artistic field predicts a physical system.

## Required inputs

- Versioned algorithm and recipe schema
- Seed, all numerical parameters, coordinate system and boundary behavior
- Desired output format and precision
- Maximum work, output size and cancellation behavior
- A known case or independent property that can check the model

A seed alone is not a complete recipe. Random-number algorithm, random-consumption order, integration method, thresholds, units and serialization precision can change the result.

## Workflow

### 1. Normalize a complete recipe

Validate finite numbers, integer-only fields, ranges and bounded arrays before generating geometry. Reject unknown algorithm revisions rather than interpreting them using today's defaults. Copy accepted data into a normalized recipe so unrelated imported fields cannot become rendering instructions.

Distinguish a blank control from numeric zero. Preserve partially edited controls while invalidating exports derived from the previous complete recipe. If importing from a file, enforce a size limit and apply the new recipe atomically only after validation.

### 2. Make randomness and coordinates explicit

Use a deterministic local PRNG for artistic variation and record its algorithm as part of the versioned model. Do not use it for credentials, security decisions or unpredictable identifiers. Keep iteration order stable so the same seed consumes the same random sequence.

Declare the drawing coordinates separately from CSS pixels and physical page units. Pointer placement must map the displayed plot into those coordinates, accounting for any letterboxing or transforms. Offer numeric or keyboard alternatives to a pointer-only editor.

### 3. Define the numerical process and stopping rules

Write down what one step represents. Following normalized field direction at fixed spatial steps differs from integrating velocity over time. A named numerical method does not by itself establish physical accuracy.

For each path, bound the number of steps and total generated points. Handle zero or near-zero direction explicitly, and stop or clip at the declared domain boundary. If a close return to the starting point is used as a loop heuristic, label it as such; proximity is not a general proof of a mathematical periodic orbit.

Use a cancellable worker when computation could delay the interface. A deadline and step cap provide different protections. Ignore results from an older generation after the user edits, imports or cancels. Do not offer a stale export just because it is still visible on screen.

### 4. Check simple truths before complex pictures

Start with a constant field whose exact displacement is known. For a radial or circular field, compare against a simple analytic property using an explicit numerical tolerance. Test zero fields, boundary exits, both direction signs and invalid parameters.

Repeat the same full recipe and compare geometry. Change only the seed to verify the intended variability; change only a rendering palette to verify that it does not alter the field geometry. Check every output coordinate for finiteness and declared bounds. These tests support the implemented model but do not prove stability or accuracy for every permitted parameter combination.

### 5. Bind preview and export to one result

Render the preview and export from the same completed normalized recipe and geometry. Make serialization rounding explicit. A preview using full floating-point coordinates and an export using rounded ones can otherwise differ.

Generate SVG from validated numeric coordinates and a fixed or validated style vocabulary. Avoid injecting arbitrary recipe strings as markup, external URLs or scripts. Retain the recipe alongside the visual output so the drawing can be regenerated. Refer to [SVG print geometry validation](../validate-svg-print-geometry/SKILL.md) when physical page size or print margins are part of the requested contract.

### 6. Inspect the actual exported artifact

Render the exported SVG with an independent permitted renderer and inspect the resulting pixels for missing paths, clipping, unwanted overlaps and unexpected scale. Label this as export-render evidence, not real-browser interaction or physical printing verification.

Keep platform limits honest: reproducible within a declared implementation is narrower than byte-identical output across every browser and future algorithm version. If the model changes, version the recipe interpretation or provide an explicit migration rather than silently changing old drawings.

## Worked example

A recipe defines a 1000×700 drawing plane, seed 1729, 180 starting points and a fixed spatial step of five units. A uniform unit field at angle zero should move an interior point from (500,350) to (505,350) in one forward step and to (495,350) backward. That exact case checks the step interpretation independently of a visually pleasing result.

A softened single-vortex field with no wind should follow a circle away from its center when its direction is normalized. After 100 unit steps from radius 100, compare the measured radius with 100 within the chosen tolerance. The center itself has no direction and should stop cleanly rather than produce NaN coordinates.

The final artwork uses the completed paths rounded to three decimal places for both preview and SVG. A separate JSON recipe records the algorithm revision and all inputs. Rendering the actual SVG confirms the exported drawing is visible, while browser layout and printer scaling remain separate unverified stages.

## Evidence status

This workflow was exercised with constant-field and circular-field cases, fixed-seed comparisons, 80 bounded recipe/property fixtures, cancellation tests and an independently rendered SVG. These checks are implementation evidence for the stated artistic model, not a general numerical-analysis or physics certification.
