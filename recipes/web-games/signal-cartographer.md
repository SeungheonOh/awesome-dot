---
id: signal-cartographer
title: "Signal Cartographer Deduction Game"
summary: "Create a grid-deduction game where players locate fictional transmitters using consistent clues."
category: web-games
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files", "websites"]
tags: ["deduction", "maps", "constraint-solving"]
status: recipe-not-run
---

# Signal Cartographer Deduction Game

Create a grid-deduction game where players locate fictional transmitters using consistent clues.

## Scenario

A puzzle enthusiast wants a map mystery that can be solved through evidence rather than guessing. Fictional transmitters emit clues about distance, direction, and line of sight. The project needs small boards with unique solutions and an explanation mode that makes the deduction process understandable.

## Inputs to prepare

- [GRID SIZE] and transmitter count
- [CLUE TYPES] to include
- [HINT POLICY] and desired difficulty
- [MAP THEME] using fictional places only

## Copy this prompt into dot

```text
dot, create Signal Cartographer, a finite browser deduction game using [GRID SIZE], [CLUE TYPES], [HINT POLICY], and [MAP THEME], if an appropriate coding environment is available. Begin with one hand-authored board and a formal definition of each clue type. Use fictional coordinates and locations only.

Players place candidate transmitter markers on a grid and eliminate impossible squares using distance, direction, and obstruction clues. Define distance precisely, such as Manhattan distance, and keep every clue consistent with that definition. A correct complete placement wins. An incorrect final submission reports which public constraints are violated and allows revision; exceeding an optional submission limit ends the attempt with a restart option. Include unrestricted practice mode.

Deliver editable source, a small original board pack, machine-readable solutions, and human-readable deduction walkthroughs. Validate that each regular board has exactly one solution under its displayed clues; label ambiguous or inconsistent boards as test fixtures only. Provide keyboard grid navigation, text coordinates, non-color candidate markings, undo, and full reset. Check edge-of-grid clues, zero candidates, multiple transmitters, and removal of a previously placed marker. Do not connect this game to real device tracking or location data. Ask before publication or external score storage, and separate executed solver checks from unverified intended behavior.
```

## Iterate with a purpose

### 1. Add transparent hints

```text
Implement hints that cite one displayed clue and eliminate a provably impossible square, without reading out the full solution.
```

### 2. Build a clue editor

```text
Add a local board editor that reports zero, one, or multiple solutions and prevents accidental publication of answer data in a player export.
```

### 3. Create a difficulty rubric

```text
Rank boards using documented deduction steps rather than raw grid size, then add examples illustrating each difficulty tier.
```

## Expected deliverables

- Grid game source with editable clue definitions
- Original uniquely solvable board pack
- Solution data and deduction walkthroughs
- Ambiguous and inconsistent validation fixtures

## Acceptance checks

- Each ordinary board has exactly one solution under its visible rules
- A completed valid placement wins without requiring a particular placement order
- Invalid submissions identify violated public clues
- Practice mode never locks a player out after repeated mistakes
- The zero-solution and multiple-solution fixtures are detected and labeled
- Undo and reset correctly restore candidate marks and submission counts
- Keyboard users can inspect every coordinate and clue

## Access, privacy and stop conditions

- Coordinates and signals are fictional and must not be replaced with live device tracking
- Solver completeness depends on the explicitly bounded board size and rule set
- Publishing boards and storing external scores require approval

## Two possible extensions

- Add a printable puzzle-and-solution booklet
- Explore a hex-grid variant with a separately defined distance model
