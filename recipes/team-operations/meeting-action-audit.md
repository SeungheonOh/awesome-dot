---
id: meeting-action-audit
title: "Meeting Action Audit"
summary: "Turn meeting records into a deduplicated action audit that distinguishes commitments, suggestions, completion evidence, and unresolved ownership."
category: team-operations
level: beginner
timebox_minutes: 30
capabilities: ["files"]
tags: ["meetings", "commitments", "follow-through"]
status: recipe-not-run
---

# Meeting Action Audit

Turn meeting records into a deduplicated action audit that distinguishes commitments, suggestions, completion evidence, and unresolved ownership.

## Scenario

A fictional product team has held three launch meetings. A task mentioned repeatedly looks like three separate commitments, while a proposed task has acquired an apparent owner through retelling. An audit makes the actionable record reviewable before anyone receives a reminder.

## Inputs to prepare

- Sanitized notes or transcripts from a bounded set of meetings
- The meeting dates and any later status updates already available
- A definition of completion for the relevant work, if one exists
- The review audience and a rule for resolving ambiguous names

## Copy this prompt into dot

```text
dot, audit the actions in [MEETING RECORDS] for [PROJECT] during [DATE RANGE]. Produce a private review draft for [AUDIENCE], using the supplied meeting dates and [STATUS UPDATES]. Check that you can read the inputs; if records are incomplete, label the coverage rather than suggesting the audit is exhaustive.

Distinguish explicit commitments from suggestions, questions, and decisions that create no action. Give each candidate action a stable identifier, precise deliverable, source locator, stated owner, due date, dependencies, and current status supported by evidence. Keep owners and dates unknown when they were not agreed. Preserve the original wording of relative dates alongside any resolved calendar date and state the reference date used.

Deduplicate repeated discussion of the same deliverable, but do not merge similar actions for different systems or audiences. Treat a statement of progress as different from evidence of completion. Review one duplicated action, one ownerless action, and one action reported complete without an attached result; identify cases not present in the material.

Return the audit, proposed clarification questions, and a short check report. Do not send reminders, assign work, update trackers, or schedule anything. Ask for a separate instruction before sharing the draft with named recipients.
```

## Iterate with a purpose

### 1. Resolve ambiguous commitments

```text
Show the exact passages behind uncertain commitments. For each, write a neutral clarification question and explain how either answer would change the audit.
```

### 2. Reconcile completion evidence

```text
Compare the audit with this additional authorized status update: [UPDATE]. Record which items now have deliverable evidence, which have only self-reported progress, and which remain unresolved.
```

### 3. Reduce meeting overhead

```text
Propose a five-minute closing checklist that would prevent the specific ownership, date, or completion ambiguities found here. Keep it separate from the historical record.
```

## Expected deliverables

- A deduplicated action audit with sources, owners, dates, and evidence-based status
- A record of merges and intentionally separate look-alike actions
- A clarification list for unresolved commitments
- An explicit statement of meeting coverage and checks performed

## Acceptance checks

- Each action is traceable to a particular passage and meeting
- Repeated mentions of one deliverable do not inflate the action count
- Two similarly named tasks for different systems remain distinguishable
- An unstated owner or due date stays unknown
- A relative deadline includes its reference date or remains unresolved
- Reported completion without evidence is not presented as verified completion

## Access, privacy and stop conditions

- Use authorized meeting records; omit unrelated personal remarks and sensitive attendee information
- Ambiguous attendee names require clarification before any person-directed action
- This recipe produces an audit only; reminders, tracker writes, and invitations need separate instructions

## Two possible extensions

- Apply the closing checklist to a fictional future meeting example
- Compare two meeting periods to identify recurring causes of unclear commitments
