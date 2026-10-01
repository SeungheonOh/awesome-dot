---
id: tide-locks
title: "Tide Locks Logic Game"
summary: "Build a turn-based water-routing puzzle with reversible moves and inspectable solution paths."
category: web-games
level: intermediate
timebox_minutes: 90
capabilities: ["code", "files", "websites"]
tags: ["logic", "turn-based", "accessibility"]
status: recipe-not-run
---

# Tide Locks Logic Game

Build a turn-based water-routing puzzle with reversible moves and inspectable solution paths.

## Scenario

A community science club wants a browser puzzle about moving water through a miniature harbor. Players should reason about gate order rather than react quickly. The organizer needs a small set of teachable levels, a reliable restart button, and a way to explain why an attempted solution failed.

## Inputs to prepare

- [BOARD SIZE] and maximum number of gates
- [LEVEL COUNT] and desired difficulty progression
- [KEYBOARD OR TOUCH PRIORITY]
- [VISUAL THEME] with two high-contrast palette choices

## Copy this prompt into dot

```text
dot, help me build Tide Locks, a small turn-based browser logic game, if code execution and a suitable browser environment are available. Use [BOARD SIZE], [LEVEL COUNT], [KEYBOARD OR TOUCH PRIORITY], and [VISUAL THEME]. First propose a compact rule sheet and one example board so I can check the water-transfer logic before you implement it.

Each move opens or closes one gate, then resolves water transfer in a fixed documented order. The objective is to fill marked basins to their target levels without overflowing a protected area. Use discrete water units rather than pretending to simulate real fluid dynamics. Include a move counter, undo, restart, level selection, and a text description of the board. Provide keyboard navigation, labeled controls, and symbols in addition to color; animations must be optional.

Deliver editable source, local launch instructions, three worked solution traces, and a verification checklist. Check conservation of water, exact target detection, overflow failure, undo after failure, and restart restoring the original board. Include an intentionally unsolvable fixture for testing, clearly separated from playable levels. Use original simple graphics and no external accounts. Keep any preview private, and ask before publishing or adding analytics. If you cannot run the game, identify unverified checks rather than reporting success.
```

## Iterate with a purpose

### 1. Introduce branching levels

```text
Add two levels where more than one solution exists, and show how their shortest verified solutions differ.
```

### 2. Build a level editor

```text
Add a local-only board editor with validation for missing targets and disconnected basins, plus JSON import and export.
```

### 3. Create a teaching mode

```text
Add an optional step explanation after each move that describes changed water quantities without revealing the remaining solution.
```

## Expected deliverables

- Editable browser-game source and launch instructions
- Rule sheet with water-transfer ordering
- Level files and three solution traces
- Accessibility and state-transition verification checklist

## Acceptance checks

- Every completed transfer conserves the total water quantity
- A level wins only when all targets match and no protected basin overflows
- Overflow shows a readable failure reason and leaves restart reachable
- Undo restores gate positions, water units, move count, and outcome together
- Restart from either win or failure restores the level initial state
- The unsolvable test fixture does not appear among ordinary playable levels

## Access, privacy and stop conditions

- This is discrete puzzle logic, not a fluid-engineering model
- Executable code and browser testing depend on the available environment
- No publishing, telemetry, or account services without separate approval

## Two possible extensions

- Design a community level format with a separate import-validation pass
- Add a color-independent printable puzzle sheet
