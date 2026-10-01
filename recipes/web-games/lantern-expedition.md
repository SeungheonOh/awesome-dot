---
id: lantern-expedition
title: "Lantern Expedition Resource Game"
summary: "Create a seeded turn-based exploration game with meaningful resource choices and recoverable failure."
category: web-games
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files", "websites"]
tags: ["exploration", "resource-management", "seeded-worlds"]
status: recipe-not-run
---

# Lantern Expedition Resource Game

Create a seeded turn-based exploration game with meaningful resource choices and recoverable failure.

## Scenario

A tabletop fan wants a short browser expedition where every move trades exploration against dwindling supplies. A lantern-lit fictional island offers a small, readable setting. The player should be able to inspect costs before committing, replay the same map, and understand whether a loss came from a decision or an impossible setup.

## Inputs to prepare

- [MAP SIZE] and terrain types
- [STARTING SUPPLIES] and movement costs
- [OBJECTIVE COUNT] and extraction rule
- [SESSION LENGTH TARGET] in turns

## Copy this prompt into dot

```text
dot, create Lantern Expedition, a turn-based browser exploration game, using [MAP SIZE], [STARTING SUPPLIES], [OBJECTIVE COUNT], and [SESSION LENGTH TARGET]. Use available coding tools and keep the first version deliberately small. First show me the resource rules and one worked route before generating a map pack.

The player explores a fictional island, collects a fixed set of relics, and returns to an extraction tile. Movement and optional scouting consume clearly displayed supplies. Reveal action costs before confirmation and allow canceled actions at no cost. The player wins only by returning with all required relics; depleted essential supplies away from a recovery point or a reached turn limit causes a specific failure. Provide a forgiving practice mode, keyboard movement, text terrain labels, and non-color resource indicators.

Generate seeded maps from routes that have known feasible solutions, then verify those solutions under the actual game rules. Deliver source, seeds, route certificates, a control guide, and edge-case notes. Test zero-cost terrain, blocked extraction, repeated relic visits, resource use at exactly zero, and reset after failure. Replay must reproduce the same map and starting inventory. Do not present generated solvability as guaranteed unless checked. Ask before publishing or storing player sessions externally; label any unrun tests.
```

## Iterate with a purpose

### 1. Introduce equipment tradeoffs

```text
Add two optional equipment choices with different movement and scouting costs, then verify at least one feasible route for each choice on each included map.
```

### 2. Build a route replay

```text
Add an endgame replay of visited tiles and resource changes, including the exact action that caused a failure.
```

### 3. Create a map workshop

```text
Add a local map editor that checks extraction reachability and resource feasibility before marking a map ready to play.
```

## Expected deliverables

- Turn-based exploration prototype
- Seeded maps and feasible route certificates
- Resource rules and action-cost guide
- Win, failure, replay, and reset test checklist

## Acceptance checks

- Every included ordinary map has a verified route completing collection and extraction within its budgets
- Canceling a proposed move spends no supplies and advances no turns
- Revisiting a collected relic does not duplicate it
- Exact-zero resource states follow a documented rule without negative inventory
- Blocked-extraction fixtures are detected and excluded from normal play
- Replay of the same seed reproduces terrain, objectives, and inventory
- Restart after failure clears discovery, route history, supplies, and outcome

## Access, privacy and stop conditions

- Procedural generation alone does not prove every map is solvable
- Gameplay uses fictional survival rules and is not wilderness guidance
- External session storage, accounts, and publication require approval

## Two possible extensions

- Add a daily-style local seed picker without scheduled delivery
- Create a printable planning map with hidden objectives on a separate sheet
