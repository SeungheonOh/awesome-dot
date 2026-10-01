---
id: cross-team-dependency-board
title: "Cross-Team Dependency Board"
summary: "Map cross-team deliverables and acceptance gates into a dependency board with explicit uncertainty, cycle checks, and coordination questions."
category: team-operations
level: intermediate
timebox_minutes: 45
capabilities: ["files"]
tags: ["dependencies", "planning", "coordination"]
status: recipe-not-run
---

# Cross-Team Dependency Board

Map cross-team deliverables and acceptance gates into a dependency board with explicit uncertainty, cycle checks, and coordination questions.

## Scenario

Three fictional teams are preparing a feature launch. Their plans refer to “API ready” and “integration ready” without agreeing what either phrase means. A dependency board can expose mismatched expectations before a status meeting becomes a debate about dates.

## Inputs to prepare

- Sanitized milestone plans from the participating teams
- The launch or project boundary and a common as-of date
- Definitions of readiness, known lead times, and any explicitly agreed dates
- The intended review audience and a limit on the number of dependencies

## Copy this prompt into dot

```text
dot, create a dependency board for [PROJECT] using [AUTHORIZED TEAM PLANS] as of [DATE]. Include only [SCOPE], up to [DEPENDENCY LIMIT] meaningful dependencies. First check which plans are present and state whose coverage is missing. Treat this as a review draft, not a tracker update.

Represent each dependency as a producer deliverable needed by a consumer milestone. Include an identifier, producer and consumer roles, exact acceptance gate, agreed or proposed date, current evidence, confidence limits, and source locator. Separate a real blocking dependency from a useful coordination note. If “ready” is undefined, write the missing definition as a question rather than supplying a false agreement.

Order the dependencies where the sources allow it. Look for circular waits, date conflicts, and one deliverable that several teams describe differently. Do not calculate a precise critical path from unknown durations or label a team late without an agreed baseline. Show how a missing producer update affects interpretation.

Return the board, a compact dependency view, and the few clarification questions most likely to change the plan. Keep named people and confidential project details to the minimum needed. Do not contact teams, assign dates, change tickets, or publish the board without a separate authorized request.
```

## Iterate with a purpose

### 1. Resolve a readiness mismatch

```text
Select a deliverable whose producer and consumer use different readiness definitions. Draft a shared acceptance gate and show which parts need explicit agreement.
```

### 2. Inspect a circular wait

```text
Explain one detected cycle, or construct a clearly fictional cycle if none exists. Identify the smallest decision that could break it without pretending that decision has been made.
```

### 3. Compare a changed plan

```text
Apply this authorized update: [UPDATE]. Show only changed dependencies, consequences for consumers, and questions newly introduced; preserve the prior as-of date in the change record.
```

## Expected deliverables

- A dependency board with producer, consumer, gate, dates, and evidence
- A compact ordered or graph-like view with uncertain links identified
- A cycle and date-conflict review
- A prioritized clarification list tied to dependency identifiers

## Acceptance checks

- Every blocking relationship names a deliverable and a consuming milestone
- An undefined readiness phrase remains an open acceptance question
- A circular wait is detected or the absence of observed cycles is qualified by coverage
- Agreed dates are distinguishable from estimates and proposed dates
- Missing durations do not produce a falsely precise critical path
- An absent team update remains a coverage gap rather than evidence of delay

## Access, privacy and stop conditions

- Provide only plans approved for this review audience; use team roles where possible
- A draft dependency does not assign work, dates, or accountability
- Distribution and tracker changes require a separate instruction with the intended destination

## Two possible extensions

- Add a scenario showing the effects of a single delayed deliverable
- Create a reusable readiness-definition template for future cross-team work
