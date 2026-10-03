---
name: interrogate
description: "Adversarially review a scoped change with concrete evidence, reconcile independent findings when available, and distinguish defects from speculative concerns."
---


# Interrogate

Challenge the implementation against the user's intent. The deliverable is a reasoned review, not automatically applied changes. Independent reviewers add perspectives when the task warrants them; disagreement or model diversity alone is not evidence of a defect.

## Establish scope and intent

Use the user-specified files, diff, or pull request. Otherwise inspect the actual branch and working tree and identify the relevant base; do not assume a branch name. Bind the review to the candidate revision and any uncommitted diff. Read enough surrounding types, callers, and tests to assess the changed contracts.

State the intended behavior, important constraints, and exclusions. Derive intent from the request and supporting artifacts, labeling any inference. Ask only if ambiguous intent would materially change the verdict. Evidence that the goal itself is unsafe or inconsistent should be raised explicitly, not suppressed to satisfy a review template.

## Review with appropriate independence

A small change may need a single direct review. For broad or consequential work, use available native workers with the [reviewer brief](references/reviewer-prompt.md), the [rubric](references/rubric.md), and [quality lens](references/code-quality-review.md). Give each the same input identity, stated intent, read-only scope, and evidence contract. Reviewers may inspect authorized surrounding context but may not fix, publish, or change settings.

Inherit supported host models unless the user requested available alternatives. Record which reviewers actually returned and whether they were independent contexts or a self-review. If the requested independent or multi-model review cannot be performed, disclose that gap and offer the useful review that is possible. Do not fabricate reviewers or substitute a silently chosen model family.

## Reconcile findings

Read all returned findings, deduplicate by failure mechanism, and verify each meaningful claim against source or a safe reproduction. Shared findings may reflect shared assumptions; a lone finding can still be decisive. Distinguish independent corroboration from repeated quotations of one source.

For each finding, preserve the affected location, reachable triggering conditions, consequence, evidence, confidence, and proposed next check. Separate severity from certainty. A remote catastrophic scenario needing several unverified failures should not outrank a reproduced ordinary defect without a concrete reason.

Apply [lead judgment](references/lead-judgment.md):

- **Act on:** evidenced defects or consequential maintainability regressions within the actual goals
- **Consider:** a real concern whose tradeoff or missing fact needs a decision
- **Noted:** valid context that does not warrant a change now
- **Dismissed:** refuted, duplicate, out of scope, or preference-only findings, with reasons

Do not turn code length, a preferred idiom, or an arbitrary number of abstractions into automatic blockers. Do not dismiss security or correctness evidence just because only one reviewer found it.

## Deliver the verdict

Lead with actionable findings, or say no findings in the reviewed scope. Include the intent, candidate identity, reviewer coverage, concise categorized findings, and unresolved disagreement. Cite actual files and checks. Distinguish checks run from suggested checks. A failed or absent reviewer is a coverage gap, never a pass. A subsequent code edit invalidates affected review evidence until rechecked.

Example finding shape: “Act on, high confidence: the save callback at file:line runs after cancellation and recreates the deleted record. The cancellation fixture reproduces it on revision X. Proposed check: cancel during the pending write and assert the public list remains empty.” Replace all example references with inspected evidence.
