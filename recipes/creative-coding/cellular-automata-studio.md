---
id: cellular-automata-studio
title: "Cellular Automata Studio"
summary: "Make an inspectable grid-simulation studio with reproducible rules, boundary choices, and reference patterns."
category: creative-coding
level: intermediate
timebox_minutes: 120
capabilities: ["code", "files", "websites"]
tags: ["simulation", "state-machines", "grid-systems"]
status: recipe-not-run
---

# Cellular Automata Studio

Make an inspectable grid-simulation studio with reproducible rules, boundary choices, and reference patterns.

## Scenario

An engineering group wants a visual introduction to state updates and repeatable tests. A cellular automaton turns a simple local rule into changing patterns, but small implementation mistakes can hide behind attractive animation. The studio should make each generation inspectable and compare its behavior with known tiny examples.

## Inputs to prepare

- [GRID WIDTH AND HEIGHT] and cell-size preference
- [BIRTH AND SURVIVAL COUNTS] for a two-state rule
- [BOUNDARY MODE] fixed-dead or wraparound
- [INITIAL PATTERN OR SEED] and speed range

## Copy this prompt into dot

```text
dot, build Cellular Automata Studio using [GRID WIDTH AND HEIGHT], [BIRTH AND SURVIVAL COUNTS], [BOUNDARY MODE], and [INITIAL PATTERN OR SEED], if a suitable coding environment is available. Begin with a tiny grid and a written next-generation rule before adding animation. Explain that every cell must read the same old grid so update order does not change the result.

Provide play, pause, single-step, speed, draw, erase, reset, and state import/export controls. Make fixed-dead edges and wraparound edges explicit choices. Bound grid size and playback rate to keep the browser responsive. Include keyboard cell navigation, text coordinates, a live-cell count, reduced motion, and a way to inspect the grid without running it.

Deliver editable source, JSON state and rule files, optional PNG snapshots, and reference tests. Include a stable block and a two-step oscillator under the stated standard rule, plus a corner-crossing fixture that distinguishes boundary modes. Check an empty grid, one-cell dimensions, malformed imports, repeated pause clicks, and reset during playback. Import validation must reject oversized grids or impossible cell values before changing the current state. Describe cycle detection as an optional bounded feature rather than claiming all patterns eventually repeat. Keep everything local by default and ask before publishing or adding external storage; mark tests that were not executed.
```

## Iterate with a purpose

### 1. Add bounded cycle detection

```text
Implement state-hash tracking with a user-visible memory cap, report detected periods, and explain when the cap prevents a conclusion.
```

### 2. Compare rule families

```text
Add a side-by-side comparison that starts two different rules from the same initial grid and keeps their generation counters synchronized.
```

### 3. Create a pattern workshop

```text
Add a local pattern library with explicit rule compatibility, original or appropriately credited examples, and validated JSON import and export.
```

## Expected deliverables

- Editable grid-simulation source
- Rule and state JSON schema with sample files
- Stable, oscillating, and boundary-sensitive fixtures
- Optional PNG snapshots
- Deterministic state-transition and import-validation tests

## Acceptance checks

- The stable block remains unchanged under the documented standard rule
- The two-step oscillator returns to its initial state after exactly two generations
- All cell changes use the previous generation rather than partly updated neighbors
- The corner fixture distinguishes fixed-dead and wraparound behavior
- Malformed or oversized imports leave the existing grid unchanged
- Pause and reset prevent delayed updates from advancing the wrong state
- An empty grid and one-cell dimensions remain valid and do not crash

## Access, privacy and stop conditions

- Large grids and rapid playback are constrained by available browser resources
- Finite test patterns do not prove every rule implementation property
- Imported files must be validated and treated as data, not executable code
- Publication and external persistence require approval

## Two possible extensions

- Add a short tutorial linking rule changes to observed behavior
- Explore a multi-state automaton as a separately specified model
