---
id: example-project-brief
title: "Example Project Brief"
summary: "Turn a bounded example task into an inspectable draft with explicit checks and limits."
category: engineering-workflows
level: beginner
timebox_minutes: 30
capabilities: ["files"]
tags: ["planning", "review"]
status: recipe-not-run
---

# Example Project Brief

Turn a bounded example task into an inspectable draft with explicit checks and limits.

## Scenario

Replace this paragraph with a concrete situation: who needs the result, what is difficult today, and why this particular artifact would help. Use fictional or sanitized context and avoid claims that the project has already been completed.

## Inputs to prepare

- The specific outcome and intended audience
- A minimal authorized input or synthetic example
- The required format, constraints and review criteria

## Copy this prompt into dot

```text
dot, help me create [SPECIFIC DELIVERABLE] for [AUDIENCE] so they can [CONCRETE OUTCOME]. Use [AUTHORIZED INPUTS] and stay within [SCOPE]. The first version should fit [FORMAT OR SIZE LIMIT], and the most important constraint is [CONSTRAINT].

First check which inputs and capabilities are available. If a missing detail materially changes the result, ask me. Otherwise state a reasonable assumption and make a reversible draft. Do not invent facts, sources, completed actions or evidence of testing.

Produce the smallest complete version with [REQUIRED ELEMENTS]. Explain how each important part uses the supplied evidence. Test [NORMAL CASE], [EDGE CASE] and [REPEATED OR INTERRUPTED ACTION] where possible, and label unrun checks clearly.

Keep the work private. Before any sharing, account change, external action or expansion of scope, identify the destination and consequence and ask for any required decision. Return the artifact, the check results, known limits and the smallest next step.
```

## Iterate with a purpose

### 1. Improve usability

```text
Inspect the draft from the intended reader's perspective. Simplify the hardest step without dropping the required evidence or checks.
```

### 2. Test the main uncertainty

```text
Identify the assumption most likely to change this result. Propose a small test and say what each possible outcome would mean.
```

### 3. Add one bounded capability

```text
Propose one useful extension, explain the new input or access it needs, and wait for my decision before broadening the scope.
```

## Expected deliverables

- A concrete draft in the requested format
- A short evidence and assumption record
- A check report with unrun items clearly marked

## Acceptance checks

- The output addresses the supplied goal and audience
- Important claims can be traced to the provided inputs
- An empty or invalid input has an explicit handling path
- The check report separates observed results from unrun tests

## Access, privacy and stop conditions

- Use only authorized inputs and ask before exposing them to a new audience
- If required access is unavailable, return a reduced draft and explain its limits

## Two possible extensions

- Add a second realistic example after the first one passes review
- Create a reusable checklist from lessons observed in an actual run
