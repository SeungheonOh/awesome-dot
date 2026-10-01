---
name: bug-reproduction-triage
description: "Separate a reported correctness defect from hypotheses and define the smallest safe experiment that could reproduce it."
---

# Turn a Bug Report into a Reproduction Brief

Separate a reported correctness defect from hypotheses and define the smallest safe experiment that could reproduce it.

## When to use

A support ticket for the fictional Fieldboard dashboard says that changing a date filter updates the table but leaves an old total in the exported report. The engineer receiving the ticket has no recording, reliable reproduction steps or confirmed environment. A useful first result is a testable investigation brief, not a guessed fix.

## Required inputs

- A sanitized report with expected and observed behavior, preserving any uncertainty
- A tiny fictional dataset with known totals and at least one empty-result filter
- Available application version, environment and timestamps, with unknown fields labeled
- The authorized local repository or test fixture, if any, plus its existing test instructions
- A boundary for permitted work, such as analysis only or local disposable test execution

## Workflow

### Normalize the report

Build a case record with report identifier, component, application revision, environment, timezone, starting state, action sequence, expected behavior and reported behavior. Use `unknown` for missing fields. Keep reporter statements separate from artifacts you can inspect and observations produced during this task. Establish whether the work is analysis-only or permits a particular disposable local fixture. If the expected result depends on an unspecified date boundary, timezone or aggregation rule, ask that question before calculating the affected case.

### Construct the smallest discriminating experiment

1. Create a synthetic dataset with stable row identifiers and independently calculable totals. Use at least two filter ranges with different totals and one range with no rows. Write the expected included row set before computing each total; this exposes off-by-one date and duplicate-row errors.
2. Define a baseline: load the fixture, open a fresh session, select the initial filter, wait for the documented completion signal and capture the visible rows and total. State how to reset the fixture and session between attempts. If no reliable completion signal exists, name that uncertainty rather than inserting an arbitrary wait as a guarantee.
3. Specify the changed-filter experiment as numbered actions. Capture selected dates, displayed row identifiers, displayed total, exported rows and exported total. Derive expectations from the fixture rather than from the application's display, which may itself be wrong. Repeat export without changing the filter to test stability.
4. Add separate cases for empty results and a fresh session. Change one dimension at a time. If a mismatch occurs only after a prior export, preserve that sequence while removing unnecessary rows and actions. If it does not occur, retain the attempted conditions and do not label the ticket invalid.
5. Build a hypothesis table whose rows name a possible correctness cause, supporting evidence, contradicting evidence and the next distinguishing observation. For example, correct exported rows with a wrong summary differs from an export containing the previous row set. Do not promote either pattern to a root cause without tracing the responsible behavior.

### Execute within bounds and hand off

Run only the expressly permitted existing test or local fixture after checking its documented side effects. Otherwise return the exact experiment with execution marked unrun. Log each attempt with case ID, revision, environment, reset performed, expected values, actual values and evidence filenames or references. Produce a concise ticket containing the reproducible sequence, mismatch and impact, followed by the case matrix and hypothesis log. Recalculate synthetic totals independently and confirm another reader can follow the reset without hidden session state. Resolution evidence must include the formerly failing sequence and a neighboring unchanged behavior. Stop if reproduction requires production access, identifying data, credentials or unapproved writes; report the minimal safe substitute needed.

## Deliverables

- A ticket draft with environment, expected behavior and reported behavior kept separate
- A minimal reproduction procedure with setup, reset and evidence-capture steps
- A case matrix with exact expected outputs from the fictional data
- A hypothesis log and check report distinguishing execution from proposed tests

## Verification

- A second engineer can follow the procedure without choosing an unstated initial filter or dataset
- Expected totals can be recalculated from the supplied fictional rows
- The empty-result case specifies whether the report is empty, zero-valued or intentionally unavailable
- Repeating an export after a filter change has a distinct expected result and a reset path
- An unsuccessful reproduction is recorded as such rather than interpreted as proof that no defect exists
- No hypothesis is promoted to a confirmed cause without identifying the supporting observation

## Stop and ask

- Use fictional records or approved sanitized samples; remove customer identifiers, credentials and session tokens
- Local execution requires an available authorized environment and the project's toolchain; a text-only brief is still useful
- Stay within the requested reproduction scope. New dependency installation, product-code edits or an additional environment require applicable authorization. If filing the resulting ticket in a named destination was already requested, do it once and verify the saved content rather than asking again
- Stop if a proposed test could delete records, send notifications or incur charges; request a safer fixture

## Example request

```text
dot, turn [SANITIZED BUG REPORT] into a reproduction brief for the engineer responsible for [COMPONENT]. Use [SYNTHETIC DATA] and [AUTHORIZED FILES], and limit the investigation to the reported correctness behavior. The output should let a colleague attempt the same experiment without this conversation.

Begin with separate lists of reported facts, observed evidence, unknowns and hypotheses. Identify the minimum starting state, exact user actions, expected result and evidence to capture. Specify how to reset between attempts so a previous filter or cached result cannot silently change the experiment. Ask about a missing detail only when it changes the expected behavior or the permitted environment.

Build a small test matrix covering the normal case, an empty result, a changed filter followed by a repeated export, and a fresh session. Give each case an expected value derived from the supplied rows. Rank possible causes by the observations that would distinguish them, rather than asserting a root cause.

If I have authorized local execution and the required toolchain is available, run only the existing relevant test or disposable fixture and record its command, environment and result. Otherwise return executable instructions with checks marked unrun. Use the evidence sources and local execution already authorized for this task. Do not install software, edit product code or expand to another environment without applicable authorization. If I explicitly requested filing the ticket in a named destination, complete that routine handoff and verify it; otherwise return a private draft. Stop before production data or credentials are needed. Finish with a concise ticket draft and the evidence needed to call the issue reproduced, then resolved.
```

## Focused follow-ups

### 1. Shrink the reproduction

```text
Reduce the synthetic dataset and action sequence while preserving the reported mismatch. Explain why each remaining row and step is necessary, and retain a reset instruction.
```

### 2. Incorporate one observation

```text
Use [NEW SANITIZED OBSERVATION] to update the hypothesis list. Identify what it rules out, what it supports, and the one next observation with the most diagnostic value.
```

### 3. Define resolution evidence

```text
Write acceptance criteria for a proposed fix without implementing it. Include a formerly failing case, a neighboring behavior that must remain correct, and the evidence a reviewer should request.
```

## Evidence status

This is an implementation guide. End-to-end execution has not been established; report actual checks and unrun steps for each use.
