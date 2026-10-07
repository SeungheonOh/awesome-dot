---
name: bug-reproduction-triage
description: "Turn a reported correctness problem into a minimal, repeatable experiment with independent expectations, reset steps and evidence for the next decision."
---

# Turn a Bug Report into a Reproduction Brief

Use this skill when a report says that a normal product action gives the wrong result, but the starting state, exact sequence or evidence is unclear. The result is an experiment another engineer can repeat and a ticket that separates what happened from what might explain it. This applies to interface state, saved data, calculations, exports, batch operations and similar correctness behavior.

## Required inputs

- The authorized report, including expected and reported behavior without removing uncertainty
- Relevant requirements, user-confirmed expectations or another independent basis for the expected result
- The smallest safe example of the relevant starting state: a test account, sample file, form values, sequence, record set or function arguments, as appropriate
- Application revision, environment and useful timestamps; unknown fields can remain unknown
- The permitted investigation scope, available repository or disposable fixture, and existing test instructions

Do not demand a dataset for a state-transition problem or an account for a pure function. Read the supplied evidence first. Ask about a missing rule only when it changes the expected result or whether an experiment is permitted.

## Workflow

### 1. Normalize the claim and its evidence

Create a case record with an ID, component, revision, environment, reported starting state, triggering actions, expected result, reported result and supporting locators. Label each item as a reporter statement, a directly inspected artifact, a local observation or an inference. Keep date and timezone context where timing affects the behavior.

Identify the contract being tested. “Cancel should not save changes” may be a supplied requirement; “Cancel always clears the draft from every screen” is a different claim and must not be invented. A screenshot of an unexpected total does not prove that the underlying records are wrong. If there is no agreed expected behavior, first prepare the competing interpretations and the one decision needed to choose between them.

### 2. Define the experiment state

Choose the smallest relevant state representation and an independent expected-result check:

- **Interface state:** initial saved values, current draft, selected view and navigation history; observe visible state separately from persisted state
- **Calculation or transformation:** a small input with a hand-checkable result, preserving units, ordering and missing values
- **Data selection or export:** stable record IDs, selection rules and expected included IDs before calculating totals
- **Repeated or batch operation:** initial records, operation identity and the specified duplicate/retry behavior
- **Timing-dependent behavior:** event order and documented completion signals; distinguish elapsed time from local clock labels where relevant

Use synthetic or sanitized material when it preserves the behavior. Explain any limitation introduced by substitution. Do not make a sample so small that it removes the sequence or boundary that triggers the report.

### 3. Establish a reproducible baseline and reset

Write numbered setup steps: restore the fixture, establish the initial saved state, start the required session or process, and reach the intended screen or entry point. State how the investigator knows loading or background work has completed. If no completion signal is known, record that uncertainty; an arbitrary delay is not proof of completion.

Define a reset that restores all state relevant to the hypothesis, including saved data, draft state, caches, pending work and counters where applicable. A visual refresh alone may not reset persisted state. If a reset would affect real records, replace it with a disposable fixture or stop for a safe scope decision.

### 4. Specify and reduce the triggering sequence

For each action, record the exact input, observable completion condition and evidence to capture. Keep expected and actual values in separate fields. Verify the expected result from the contract or independent calculation rather than copying the possibly incorrect screen.

Preserve the important order. A defect that appears only after canceling twice needs that sequence; a defect after changing a filter needs both the old and new selection. Remove unrelated actions one at a time and retain the last sequence that still shows the mismatch. Record a failed reproduction as a tested set of conditions, not proof that the original report is false.

When the task is to shrink an established failing input or replay, define what counts as the **same** failure and which simplifications are allowed. A different wrong record, an exception or an invalid replay does not automatically preserve the reported defect. Keep prerequisites and reference relationships in mind: deleting a setup action may make later actions impossible. A coherent group deletion or coordinated edit can be useful when permitted. Do not invent replacement actions or change identities outside the permitted transformations; keep repairing the target separate from reducing its failing input.

Evaluate candidates from a fresh relevant state through the actual target. Distinguish a successful reproduction, valid non-reproduction and an invalid or unrun candidate; never attribute an earlier output to a rejected replay. Count attempted candidates, including rejected ones, against any declared observation or time budget. Use direct reasoning or a small fixed-task helper as appropriate; automation is not required for a short sequence.

State what the search established. Checking every single-command deletion can establish that none of those deletions preserves the failure; it does not prove a globally smallest case or exclude useful combined changes. Name the checked simplifications and any limit that stopped the search. Confirm the final saved candidate with the same reset and failure check before reporting it as a working reproducer.

### 5. Choose relevant neighboring cases

Add a small matrix that tests the reported case, one normal neighboring behavior, and a repeated, interrupted or reset path relevant to the contract. Add empty, boundary or invalid inputs only when those concepts apply. Mark irrelevant cases as such rather than inventing rows, filters or totals for every product.

Examples of useful distinctions are Cancel versus Save; first call versus repeated call; no matching records versus one matching record; and a resumed operation versus a fresh session. Each case needs a reset, expected outcome and observation that would distinguish plausible explanations. Avoid changing several dimensions at once.

### 6. Run authorized checks and evaluate hypotheses

Use an available authorized test environment and inspect the documented side effects before executing the existing relevant test or disposable fixture. Do not install dependencies, modify product code, access another environment or trigger consequential effects merely to obtain evidence when those actions are outside the request.

Log case ID, exact revision, environment, reset, action sequence, expected result, actual result and evidence reference. If execution is unavailable, deliver the same experiment with actual-result fields marked unrun. An executable procedure is useful; it must not be presented as an observation.

Maintain a hypothesis table: possible cause, supporting observation, contradicting observation and next discriminating check. For example, an unsaved value visible only in a reused editor differs from that value appearing in a fresh read of the saved record. Both can look like “Cancel saved my change” to a reporter. Trace the responsible behavior before naming a root cause.

### 7. Deliver the brief and the next decision

Return a concise ticket, reproducible procedure, case matrix, evidence ledger and hypothesis table. Make clear whether the defect was reproduced, not reproduced under the attempted conditions, or not run. A resolution claim needs the formerly failing sequence, relevant neighboring behavior and evidence from the actual fixed revision.

If the user already requested filing the ticket in a named authorized destination, create or update it within that scope and read back the saved content. On an uncertain response, inspect existing state before retrying. Otherwise return a private ready-to-use draft. Keep proposed fixes separate from the reproduction result unless implementation was also authorized.

## Deliverable record

```text
case_id:
component_and_revision:
environment_and_coverage:
contract_and_source:
starting_state:
reset_steps:
triggering_actions:
completion_signal:
expected_result_and_independent_basis:
observed_result_or_unrun_reason:
evidence_references:
relevant_neighbor_cases:
hypotheses_and_discriminating_checks:
next_decision:
```

## Verification

- Another engineer can follow the setup and reset without choosing hidden starting values
- The expected outcome has an independent source or calculation
- UI appearance, stored state, reported behavior and direct observations remain distinct
- The repeated/reset case tests a plausible source of state leakage or ordering error
- Every actual result names the environment and revision on which it was observed
- Missing evidence and unsuccessful reproduction remain visible
- No root cause, fix, ticket publication or test success is invented

## Stop and ask

Stop the dependent experiment when expected behavior is undecided, the permitted environment is unclear, or the test would require new access, credentials, identifying production data, destructive changes, notifications or charges. Continue the safe brief and name the smallest missing input. Ordinary already-authorized reads and routine ticket placement do not need duplicate approval.

This workflow addresses bounded correctness reports. A request for broader access or a different class of investigation is a scope change, not a reason to improvise a risky experiment.

## Worked examples

[Two different report types](WORKED_EXAMPLE.md) show a Cancel-state investigation and a filtered export investigation. The same procedure works without forcing a tabular-data model onto the first case.

## Example request

```text
dot, turn [REPORT] into a reproduction brief for [COMPONENT]. Use [AUTHORIZED EVIDENCE] and [RELEVANT SAFE STARTING STATE]. Stay within [INVESTIGATION SCOPE].

Separate the contract, reported facts, direct observations and hypotheses. Define setup, reset, exact actions, completion signals and an independently justified expected result. Choose neighboring and repeated-action cases that fit this behavior, rather than adding irrelevant tests.

Run the permitted checks if the required environment is available; otherwise mark them unrun. Return a concise ticket, case matrix and the observation that would best distinguish the leading explanations. If I already requested filing the ticket in [DESTINATION], do so within that scope and verify the saved result. Do not expand access or claim a cause or fix without evidence.
```

## Evidence status

The worked examples are synthetic investigation designs. They do not establish a defect in a real product or a completed application test. Report the actual evidence and execution limits for each use.
