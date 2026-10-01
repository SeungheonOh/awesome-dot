---
id: knowledge-base-gap-map
title: "Knowledge Base Gap Map"
summary: "Map real team questions to existing documentation and prioritize missing, stale, conflicting, or hard-to-find answers."
category: team-operations
level: beginner
timebox_minutes: 45
capabilities: ["files"]
tags: ["knowledge-base", "documentation", "discoverability"]
status: recipe-not-run
---

# Knowledge Base Gap Map

Map real team questions to existing documentation and prioritize missing, stale, conflicting, or hard-to-find answers.

## Scenario

A fictional engineering team answers the same setup and support questions repeatedly. The problem may be missing content, but it may also be a correct page with an unhelpful title or two pages that disagree. A gap map separates those cases before anyone writes more documentation.

## Inputs to prepare

- A sanitized sample of recurring team questions and their context
- An authorized document inventory or a bounded collection of pages
- The intended reader roles and tasks they need to complete
- A priority rule such as frequency, task impact, or onboarding delay

## Copy this prompt into dot

```text
dot, build a knowledge base gap map for [TEAM] using [QUESTION SAMPLE] and [AUTHORIZED DOCUMENT COLLECTION]. Limit the review to [SCOPE] for [READER ROLES]. First report which documents you can actually inspect; a title-only inventory is not evidence that a page answers a question.

Group equivalent questions without losing important differences in prerequisites or reader roles. For each question, identify the best existing answer and source locator, then classify the issue as missing content, stale content, conflicting guidance, discoverability, or insufficient evidence. Explain each classification with a concrete example. Do not assume that an old publication date alone makes guidance wrong.

Prioritize gaps using [PRIORITY RULE], distinguishing observed frequency from estimates. For the highest-impact gaps, propose a minimal repair: a better entry point, a clarified paragraph, a missing example, or a new page outline. Check one question with several conflicting answers and one page available only by title; keep uncertainty visible.

Return the gap map, a ranked repair backlog, and two sample page outlines or navigation fixes. Do not edit the live knowledge base, delete pages, change permissions, or ask colleagues questions. Keep the draft within the authorized audience and explain any access-limited coverage.
```

## Iterate with a purpose

### 1. Test findability with a novice

```text
Use three representative questions to simulate a first-time reader’s route through the supplied inventory. Identify the exact label or prerequisite that makes the route confusing.
```

### 2. Draft one minimal repair

```text
Choose the highest-impact gap and draft the smallest self-contained repair. Tie each factual statement to supplied evidence and leave placeholders where the team must confirm practice.
```

### 3. Recheck after a revision

```text
Compare this authorized revised page, [PAGE], with the original gap criteria. Mark which questions it now answers and which remain blocked; do not declare the entire knowledge base fixed.
```

## Expected deliverables

- A question-to-document map with evidence-based gap classifications
- A ranked documentation repair backlog using an explicit priority rule
- Two small proposed repairs or outlines
- A coverage statement distinguishing inspected pages from inventory-only entries

## Acceptance checks

- Equivalent questions are grouped without merging different reader prerequisites
- A title-only page is not counted as a verified answer
- Conflicting guidance is shown with both source locators
- Publication age alone does not establish staleness
- Ranking separates observed frequency from estimated impact
- Each proposed repair addresses a specific mapped gap

## Access, privacy and stop conditions

- Use sanitized questions and only documentation authorized for this review
- Restricted pages may remain listed as unavailable but must not be accessed through another route
- Live edits, deletions, permissions, and publication are outside this draft-only scope

## Two possible extensions

- Create a small task-based usability checklist for future documentation reviews
- Repeat the bounded review after a documented set of repairs is approved
