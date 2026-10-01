---
id: evidence-linked-decision-log
title: "Evidence-Linked Decision Log"
summary: "Reconstruct a bounded set of team decisions with their rationale, authority, unresolved questions, and supersession history."
category: team-operations
level: beginner
timebox_minutes: 45
capabilities: ["files"]
tags: ["decisions", "traceability", "alignment"]
status: recipe-not-run
---

# Evidence-Linked Decision Log

Reconstruct a bounded set of team decisions with their rationale, authority, unresolved questions, and supersession history.

## Scenario

A fictional platform team has discussed a storage migration across several notes. People remember different outcomes because proposals, approvals, and later reversals are mixed together. A decision log can preserve the disagreement without manufacturing consensus.

## Inputs to prepare

- Sanitized notes for one project and a stated date range
- A list of decisions the team believes were made, if available
- The roles authorized to approve each decision, or a note that authority is unknown
- The audience, maximum log size, and preferred source locator format

## Copy this prompt into dot

```text
dot, create a reviewable decision log for [PROJECT] from [AUTHORIZED NOTES] covering [DATE RANGE]. The audience is [TEAM], and the output should fit [SIZE LIMIT]. Use only supplied or explicitly authorized sources; first identify missing material that would change whether something counts as decided.

Extract candidate decisions and separate approved choices, proposals, deferred questions, and statements whose status is unclear. For each entry include a stable identifier, concise decision, date or unknown date, approving role when evidenced, alternatives considered, rationale, affected work, source locator, and conditions that would reopen it. Do not infer agreement from silence or treat the most recent comment as approval automatically.

Link reversals to the entries they supersede while preserving the earlier context. If sources conflict, quote only the minimum necessary wording and show both locators. Test the log against one explicit approval, one abandoned proposal, and one reversed or undated decision; say when the inputs lack such examples.

Return the draft log, the questions that prevent confident classification, and an evidence check summary. Keep this private. Do not contact participants, change project records, or publish the log without a separate instruction identifying the destination and audience.
```

## Iterate with a purpose

### 1. Resolve one conflict

```text
Take the most consequential contradictory entry and prepare two possible interpretations. Identify the exact evidence or approving role needed to choose between them; do not choose by majority of comments.
```

### 2. Trace implementation consequences

```text
Map each approved decision to the supplied affected work items. Distinguish an explicit dependency from your inference, and identify any work item that still reflects a superseded choice.
```

### 3. Prepare a review agenda

```text
Create a short agenda containing only decisions that need confirmation, ordered by the consequence of getting them wrong. Include the source locator and one answerable question for each.
```

## Expected deliverables

- A decision log with stable identifiers and evidence locators
- A visible distinction between approvals, proposals, deferrals, and unknown status
- A supersession trail and a bounded list of review questions
- A check summary identifying missing examples or unavailable evidence

## Acceptance checks

- Every approved decision has evidence of approval rather than inferred consensus
- A proposal that was discussed but not adopted remains labeled as a proposal
- A reversal points to the earlier entry without deleting its rationale
- Undated decisions retain an unknown date rather than borrowing a nearby timestamp
- Conflicting accounts remain visible with locators for both accounts
- Each reopening condition is evidenced or explicitly labeled as a proposed review criterion

## Access, privacy and stop conditions

- Provide only notes you are authorized to share, with unnecessary personal details removed
- Missing approval evidence blocks definitive classification, not the rest of the draft
- Review the log before any posting or distribution; inclusion in the draft does not assign authority

## Two possible extensions

- Add a change summary when a second authorized batch of notes becomes available
- Create a decision-review checklist tailored to the team’s documented approval process
