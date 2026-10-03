---
name: arena
description: "Compare independently produced candidate artifacts against a task-specific rubric, choose a base, and verify a coherent synthesis."
---


# Arena

Use competing attempts when design uncertainty warrants the cost. Do a simple, determined task directly. Arena produces an artifact and a synthesis record; it grants no authority to publish or change unrelated settings.

## Frame a fair comparison

Name the artifact, exact inputs or source revision, constraints, allowed side effects, and a falsifiable done condition. Choose a few task-specific criteria before seeing candidates: for example, correct recovery after interruption, compatibility with named callers, and understandable ownership. Share all acceptance requirements with candidates. Keep judge scoring and candidate identities separate to reduce anchoring, not to hide requirements.

Set the candidate count from the real design space, user budget, and available concurrency. Two materially distinct designs can be enough. Prefer inherited models. Use explicit supported model choices only when relevant; report absent model diversity honestly.

Give each writer a separate directory or worktree and one output owner. If isolation cannot be established, return proposals rather than overlapping edits. Do not assume a particular delegation API, background flag, cloud workspace, or persistent worker.

## Produce candidates

Give each the same task and grounding, a separate output path, and an instruction to return the artifact plus rationale and verification evidence. Candidate work is independent only when another execution context actually performs it. With no delegation, produce serial alternatives and label them self-comparison; if the user required independent comparison, report that requirement unverified.

Track workers to terminal results. A failed or missing output is a dropout, not a low-scoring complete candidate. Continue useful work, retry a recoverable failure within the original boundary, or record the missing coverage. Never count an unfinished worker as agreement.

## Judge completed artifacts

Freeze candidate outputs before judging. Remove author/model labels when practical. Read every candidate in full. An independent read-only judge can evaluate all artifacts using the fixed rubric; otherwise document self-review. A different model is optional and is separate from execution independence.

Score each criterion with a concrete artifact citation or executed check. A confident rationale cannot substitute for a working artifact. Resolve disagreements by reading the underlying evidence. Prefer the design a maintainer can extend without breaking its invariants, not the most polished writeup.

## Select, adapt, verify

Choose one base and explain why. Revisit the others for useful isolated ideas. Adapt a borrowed idea into the base's data model and ownership; do not mechanically concatenate incompatible designs. Record each adopted and rejected idea. Convergence can mean a well-constrained task or shared bias, so it still needs verification. Major unexplained divergence may require clarifying the brief.

Run checks against the synthesized artifact, including interaction-sensitive checks affected by every borrowed change. Passing candidates do not imply a passing synthesis. A failed check returns the work to the relevant design decision or change; do not weaken the rubric to obtain a pass.

## Synthesis record

Return the final artifact or unapplied draft, input identity, rubric results, base, adopted changes, rejected alternatives, dropouts, reviewer independence, and verification status. For example: “Candidate B owns retries at the write boundary. Adapted A's stable request ID. Rejected A's second cache. The combined duplicate-request test is unverified because no runtime is available.” That example illustrates reporting, not an executed result.
