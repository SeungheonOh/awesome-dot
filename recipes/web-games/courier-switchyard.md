---
id: courier-switchyard
title: "Courier Switchyard Routing Game"
summary: "Create a pauseable routing game that teaches planning through package queues and track switches."
category: web-games
level: advanced
timebox_minutes: 120
capabilities: ["code", "files", "websites"]
tags: ["routing", "simulation", "queue-management"]
status: recipe-not-run
---

# Courier Switchyard Routing Game

Create a pauseable routing game that teaches planning through package queues and track switches.

## Scenario

A workshop facilitator wants a game where players experience bottlenecks without needing fast reflexes. A miniature delivery yard offers a concrete setting: route parcels to matching depots, avoid collisions, and recover from congestion. The prototype should make every simulation step visible and support a calm turn-by-turn mode.

## Inputs to prepare

- [YARD SIZE] and number of depots
- [PARCEL TYPES] represented by symbols and labels
- [ROUND LENGTH] measured in simulation ticks
- [DIFFICULTY TARGET] and preferred input devices

## Copy this prompt into dot

```text
dot, create a small Courier Switchyard browser prototype using [YARD SIZE], [PARCEL TYPES], [ROUND LENGTH], and [DIFFICULTY TARGET], conditional on available coding and browser tools. Start with a written tick-order specification and a single junction. I want to approve understandable rules before the yard gets larger.

Players set track switches and release waiting parcels toward labeled depots. A round ends successfully when its finite manifest is delivered correctly within the tick budget. A collision, wrong-depot delivery, or exhausted budget produces a specific failure explanation. Provide pause, single-step, normal speed, restart, and a seeded practice round. Avoid endless spawning or an unwinnable random manifest: generate a delivery schedule from a known valid route plan.

Show queue lengths and intended next positions in an inspectable overlay. Support keyboard and pointer controls, distinct parcel shapes, reduced motion, and a practice mode without a timer. Deliver editable source, manifest data, a reference route plan, and test notes. Verify simultaneous junction arrivals, an empty manifest, a blocked depot, pause stability, and reset of every queue and timer. Keep the prototype local or in a private preview; ask before publishing, recording player behavior, or introducing networked scores. Report any browser checks you could not actually run.
```

## Iterate with a purpose

### 1. Compare dispatch policies

```text
Add a replay that compares first-in-first-out dispatch with a player-created priority rule on the same seeded manifest.
```

### 2. Expose bottlenecks

```text
Add a post-round diagram of maximum queue length per segment, using patterns and labels as well as color.
```

### 3. Design cooperative planning

```text
Create a shared-device planning phase where two players assign distinct yard zones before stepping the simulation together.
```

## Expected deliverables

- Browser prototype with pause and single-step controls
- Documented event ordering and failure rules
- Seeded manifest and reference route schedule
- Queue, collision, and reset test checklist

## Acceptance checks

- Two parcels entering the same exclusive segment on one tick trigger the documented collision outcome
- The reference plan completes its manifest within the stated budget
- Paused simulation advances neither parcels nor budget
- Wrong-depot delivery identifies the parcel and expected destination
- Empty manifests resolve immediately without spawning phantom parcels
- Restart clears queues, deliveries, switch settings, and tick count
- All route switches can be operated without a mouse

## Access, privacy and stop conditions

- The yard is a teaching simulation, not logistics optimization advice
- Private previews and code execution depend on available tools
- Networked leaderboards, behavioral tracking, and publication require approval

## Two possible extensions

- Add a level pack centered on different bottleneck structures
- Export a route replay as a local JSON file
