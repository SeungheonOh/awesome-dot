---
id: retrospective-evidence-pack
title: "Retrospective Evidence Pack"
summary: "Prepare a blameless retrospective packet that separates a sourced timeline, measured outcomes, interpretations, and testable improvement ideas."
category: team-operations
level: intermediate
timebox_minutes: 60
capabilities: ["files"]
tags: ["retrospectives", "evidence", "improvement"]
status: recipe-not-run
---

# Retrospective Evidence Pack

Prepare a blameless retrospective packet that separates a sourced timeline, measured outcomes, interpretations, and testable improvement ideas.

## Scenario

A fictional team has finished a difficult release. The strongest memories concern the final week, while earlier constraints are easy to forget. An evidence pack gives the retrospective a shared starting point without deciding who is to blame or inventing causal explanations.

## Inputs to prepare

- A bounded release or project period and its original goals
- Sanitized milestone records, selected notes, and relevant aggregate metrics
- Known changes in scope or measurement definitions
- The retrospective audience and topics intentionally outside scope

## Copy this prompt into dot

```text
dot, prepare an evidence pack for a retrospective on [PROJECT OR RELEASE] during [PERIOD]. Use [AUTHORIZED RECORDS] and [AGGREGATE METRICS], with [OUT-OF-SCOPE TOPICS] excluded. The audience is [TEAM]. Start by listing source coverage and any missing baseline that would make a comparison misleading.

Create a concise timeline of goals, scope changes, handoffs, outcomes, and notable interruptions. Separate sourced observations, participant interpretations, and hypotheses about causes. For metrics, preserve units, denominators, time windows, and definition changes. Do not infer individual performance, intent, or fault from ticket counts or isolated comments.

Select a small set of discussion prompts where different interpretations are plausible. Propose improvement experiments with an owner role to confirm, a bounded change, an observable signal, and a review criterion. These are proposals, not assigned commitments. Check a disputed event, an apparent improvement caused by a denominator change, and an outcome lacking a baseline; note missing examples honestly.

Return the evidence pack, an uncertainty list, and a neutral review agenda. Keep it private and avoid unnecessary personal details. Do not send invitations, publish findings, change records, or state that the team has agreed to any experiment.
```

## Iterate with a purpose

### 1. Challenge a causal story

```text
Take the strongest proposed causal explanation and list plausible alternatives consistent with the same evidence. Identify an observation that would help distinguish them.
```

### 2. Design one improvement experiment

```text
Expand one proposed improvement into a small reversible experiment. Define the comparison, signal, confounders, and review question without assigning an owner or starting it.
```

### 3. Make disagreement discussable

```text
Rewrite the agenda so that disputed interpretations are presented as answerable questions with shared evidence. Remove language that attributes motives or individual blame.
```

## Expected deliverables

- A sourced project timeline with goals and scope changes
- A metric comparison that preserves definitions and denominators
- A visible distinction between observations, interpretations, and causal hypotheses
- A neutral agenda and a small set of proposed improvement experiments

## Acceptance checks

- The timeline includes earlier constraints rather than only recent memorable events
- Every metric comparison states compatible windows and denominators or explains incompatibility
- A missing baseline prevents a claimed improvement or regression
- A disputed event preserves multiple accounts and their sources
- Improvement ideas include observable review criteria without invented commitments
- No individual performance conclusion is derived from activity counts

## Access, privacy and stop conditions

- Use sanitized records and aggregate metrics; exclude personnel, health, and unrelated private details
- Do not turn participant comments into attributed accusations without the user’s explicit review
- Sharing the packet or initiating an experiment requires a separate bounded request

## Two possible extensions

- Create a facilitator sheet with neutral follow-up questions
- Compare the proposed experiments with a later authorized outcome review
