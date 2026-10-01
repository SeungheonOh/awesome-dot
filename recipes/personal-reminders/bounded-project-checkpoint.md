---
id: bounded-project-checkpoint
title: "Project Checkpoints with a Finish Line"
summary: "Schedule finite project review prompts that ask for evidence and decisions while keeping the project\u2019s end date visible."
category: personal-reminders
level: beginner
timebox_minutes: 25
capabilities: ["scheduling", "files"]
tags: ["project", "checkpoint", "bounded-series"]
status: recipe-not-run
---

# Project Checkpoints with a Finish Line

Schedule finite project review prompts that ask for evidence and decisions while keeping the project’s end date visible.

## Scenario

A volunteer is preparing a small community event over six weeks. Weekly status prompts could help, but an indefinite reminder would outlive the event. Each checkpoint should ask for the next decision and concrete evidence, then stop at the planned finish.

## Inputs to prepare

- Project label, outcome and current milestone list
- First checkpoint date, cadence and final checkpoint or project end date
- IANA timezone, local delivery time and personal destination
- Three checkpoint questions and what evidence the user can provide
- Known blackout dates and what to do with a checkpoint on the final day

## Copy this prompt into dot

```text
dot, set bounded review prompts for [PROJECT LABEL], whose intended outcome is [OUTCOME]. Begin [FIRST CHECKPOINT DATE], repeat [CADENCE] at [LOCAL TIME] in [IANA TIMEZONE], and end on [FINAL CHECKPOINT DATE]. Notify only me at [DESTINATION]. Exclude [BLACKOUT DATES] and do not extend the series when progress is slow.

Build each checkpoint around three questions: what changed against [MILESTONE LIST], what evidence supports that change, and what decision or next action is needed before the next checkpoint? Keep the message useful even if no source is connected. Do not claim to know project status from silence, reminder delivery or inaccessible documents.

Verify actual scheduling and destination support. Preview every checkpoint date or the bounded recurrence, including how the final date and exclusions are handled. Check for an existing series for this project so setup retries cannot duplicate it. If exceptions are unsupported, use a supported finite alternative or provide an unscheduled plan. Read back the saved timezone, start, stop and destination, and distinguish schedule creation from successful future delivery. Return a concise checkpoint template, the dated series and a final review prompt that asks whether the project is complete; it must not automatically create a new series.
```

## Iterate with a purpose

### 1. Sharpen the evidence questions

```text
Use [PROJECT MILESTONES] to replace generic status questions with observable completion evidence. Preserve the existing cadence and final date.
```

### 2. Handle a slipping milestone

```text
The milestone [LABEL] moved to [DATE]. Update the remaining checkpoint text while keeping the schedule end unchanged, then ask whether a separate extension is wanted.
```

### 3. Prepare the closing review

```text
Create a final review template covering achieved outcome, unfinished work, reusable lessons and explicit next decisions. Do not create reminders beyond the agreed finish line.
```

## Expected deliverables

- A project-specific three-question checkpoint template
- A finite dated checkpoint sequence with blackout handling
- A final review prompt that does not auto-renew
- A verified setup record or clearly unscheduled plan

## Acceptance checks

- Every checkpoint asks for evidence tied to a named project milestone
- The first and final checkpoint dates match the requested boundaries
- A blackout on the final date receives an explicit resolution
- No progress or completion is inferred from silence
- A repeated setup leaves one project series
- A slipping milestone does not silently extend the schedule

## Access, privacy and stop conditions

- Notifications go only to the user; team status requests require separate authorization
- Reading project sources is optional and must stay within authorized access
- Stop if the specified cadence produces no valid checkpoint before the project ends

## Two possible extensions

- Add a user-approved private evidence log for checkpoint replies
- Create a separate retrospective after the final review if requested
