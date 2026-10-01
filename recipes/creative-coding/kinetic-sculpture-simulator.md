---
id: kinetic-sculpture-simulator
title: "Kinetic Sculpture Simulator"
summary: "Build a playful kinetic-sculpture simulation with bounded controls and transparent modeling assumptions."
category: creative-coding
level: advanced
timebox_minutes: 180
capabilities: ["code", "files"]
tags: ["simulation", "creative-coding", "motion"]
status: recipe-not-run
---

# Kinetic Sculpture Simulator

Build a playful kinetic-sculpture simulation with bounded controls and transparent modeling assumptions.

## Scenario

You want to explore how a hanging mobile might move before making a paper art project. The goal is visual experimentation, not engineering a load-bearing object. You want a small browser simulation with understandable controls that remains calm and usable when animation is reduced or paused.

## Inputs to prepare

- A sketch or plain-language description of the imagined sculpture
- Preferred visual style and a small set of adjustable motion parameters
- Target browser and whether a simple two-dimensional model is acceptable
- A definition of the visual behaviors to explore and those outside scope

## Copy this prompt into dot

```text
dot, build a browser-based kinetic-sculpture simulator inspired by [AUTHORIZED SKETCH OR DESCRIPTION]. Begin with a simple two-dimensional model unless the available toolchain clearly supports [REQUESTED ALTERNATIVE]. Explain the moving parts, chosen approximations, and controls in plain language before implementing them. This is an artistic exploration, not a physical design, safety assessment, or fabrication plan.

Provide bounded controls for [SELECTED PARAMETERS], a pause button, a reset button, a single-step option, and a way to reproduce a starting state. Include a few clearly labeled example arrangements. Keep movement within the visible stage and respect reduced-motion preferences by starting paused or offering a static view. Show useful qualitative observations without claiming physically accurate forces, material strength, or real-world stability.

Deliver source files, a parameter guide, an assumptions note, and a test log separating executed checks from proposed checks. Test minimum and maximum controls, zero or near-zero damping, rapid pause and reset actions, a resized window, and returning from an inactive browser tab. Prevent invalid numbers from propagating and cap time-step jumps so the display remains usable. If the environment cannot run the project, provide setup instructions and state that limitation. Use only authorized assets, avoid unnecessary external services, and keep any preview private until I approve publication and its audience.
```

## Iterate with a purpose

### 1. Compare motion presets

```text
Add three reproducible presets that illustrate different visual behaviors, explaining which parameters differ and which assumptions stay fixed.
```

### 2. Add a static composition mode

```text
Create a paused composition view with draggable starting positions and a reset path, including keyboard-accessible alternatives for changing positions.
```

### 3. Record a comparison sheet

```text
Produce static snapshots of the approved presets if rendering is supported, labeling parameter values and distinguishing them from physical test results.
```

## Expected deliverables

- Browser-based artistic simulation source
- Bounded controls, pause, reset, and reproducible presets
- Plain-language parameter and assumptions guide
- Motion and numeric-edge-case test record
- Private preview if supported

## Acceptance checks

- All controls enforce documented valid ranges
- Pause, reset, and single-step behave consistently
- Reduced-motion mode can avoid continuous animation
- Returning from an inactive tab does not cause an uncontrolled jump
- Zero or near-zero damping does not create invalid numeric state
- No output is labeled as structural or fabrication validation

## Access, privacy and stop conditions

- Rendering and simulation depend on an available browser and coding toolchain
- The simplified model cannot establish real-world safety, strength, or stability
- No fabrication or load-bearing instructions are produced
- Publication requires approval of assets, content, and audience

## Two possible extensions

- Explore a user-supplied alternate linkage as another artistic model
- Create a gallery of parameter snapshots with documented assumptions
