---
id: stakeholder-launch-faq
title: "Stakeholder Launch FAQ"
summary: "Draft an evidence-backed launch FAQ that gives different stakeholder groups consistent answers while exposing unknowns and approval-sensitive commitments."
category: team-operations
level: beginner
timebox_minutes: 45
capabilities: ["files"]
tags: ["stakeholders", "launches", "faq"]
status: recipe-not-run
---

# Stakeholder Launch FAQ

Draft an evidence-backed launch FAQ that gives different stakeholder groups consistent answers while exposing unknowns and approval-sensitive commitments.

## Scenario

A fictional internal analytics feature is approaching launch. Support, sales, and operations need answers, but draft notes disagree about eligibility and timing. A reviewable FAQ can reduce repeated questions while preventing a tentative date from becoming a public promise.

## Inputs to prepare

- Authorized launch notes, scope statements, and approved product descriptions
- The stakeholder groups and questions they are likely to ask
- Known exclusions, rollout stages, and support boundaries
- The intended use of the draft and who can approve external claims

## Copy this prompt into dot

```text
dot, draft a stakeholder FAQ for [LAUNCH OR CHANGE] using [AUTHORIZED MATERIALS]. Serve [STAKEHOLDER GROUPS] and focus on [QUESTION THEMES]. The output is a private review draft for [REVIEWER], not approved messaging. First identify missing or conflicting facts that could change eligibility, timing, support, or commitments.

Write concise questions and answers grouped by the reader’s practical needs: what changes, who is affected, what action is required, what remains unchanged, and where unresolved issues should go. Include a source locator and confidence limit for each substantive answer. Distinguish documented facts from proposed wording and unanswered questions. Use the same underlying fact consistently across audience-specific explanations.

Mark claims about dates, availability, guarantees, pricing, policy, or contractual obligations for review when the sources do not show approval. Do not turn aspirations into promises. Check an ineligible user, a delayed rollout, and a question the materials cannot answer. Preserve exclusions even when they make an answer less upbeat.

Return the FAQ, a fact consistency check, and an approval queue containing only material unresolved claims. Do not publish, email stakeholders, invent a support address, or state that any reviewer has approved the content. Ask before adapting it for a new audience with different disclosure permissions.
```

## Iterate with a purpose

### 1. Challenge the eligibility answer

```text
Test the FAQ against three fictional reader profiles near the eligibility boundary. Explain where the current wording gives a clear answer and where source evidence is missing.
```

### 2. Create a short frontline version

```text
Condense the draft into a quick-reference version for [AUTHORIZED AUDIENCE]. Preserve exclusions, uncertainty, and escalation limits while removing background they do not need.
```

### 3. Reconcile an approved change

```text
Apply this authorized approved statement: [STATEMENT]. Show every answer it changes and flag downstream contradictions; do not treat approval of one claim as approval of the whole FAQ.
```

## Expected deliverables

- A stakeholder FAQ with concise answers and evidence locators
- An explicit list of unknowns and conflicting launch facts
- A consistency check across audience-specific answers
- A bounded approval queue for consequential or unsupported claims

## Acceptance checks

- Eligibility answers preserve documented exclusions
- A delayed or staged rollout is not described as universal availability
- An unanswered question is marked unknown rather than answered plausibly
- Dates, guarantees, and policy claims match supplied approval evidence
- The same fact remains consistent across stakeholder sections
- Support destinations are supplied and verified or left as placeholders

## Access, privacy and stop conditions

- Use only material authorized for the review audience and avoid customer-specific examples
- External publication or a new audience requires a separate disclosure decision
- A source document’s optimistic language does not authorize commitments or guarantee claims

## Two possible extensions

- Create a sanitized fictional example that illustrates the hardest FAQ answer
- Prepare a change log when the approved launch scope is revised
