---
name: review-code-change
description: Review a concrete code change for correctness, regressions, maintainability, and meaningful test coverage, then return actionable findings grounded in the affected behavior. Use for review itself, rather than preparing a change summary or implementing requested fixes.
---

# Review a Code Change

Find problems that matter to the changed behavior and explain them clearly enough to act on. A useful review can have no findings. Do not invent issues, restate the diff, or turn personal style preferences into blockers.

## Establish the review subject

Identify the requested diff, its base and head, the intended behavior, and applicable project instructions. For a working-tree review, include the requested staged, unstaged, and untracked changes explicitly; a commit identifier alone does not describe them. If the user supplied a patch, check whether the surrounding source matches its base before reasoning about execution.

Read the change description and relevant tests, but do not treat either as proof that the implementation satisfies the request. Note which requirements are explicit and which behavior you are inferring. If the subject changes during review, inspect the affected delta again before presenting findings against the final version.

Keep the operation within review scope. Reading and permitted local checks do not require editing the patch. Do not change files, post comments, approve, merge, or publish merely because you found something; complete those actions only when the request covers them.

## Trace behavior through the change

Read the full diff, then the relevant surrounding functions, callers, state, and tests. Follow the path from a real input or entry point to its observable effect. Focus on contracts the change could disturb, rather than scanning unrelated parts of the repository.

Consider the consequences of changed assumptions:

- Can existing callers still supply the expected values and interpret the result?
- Do omitted, empty, or explicit values have different meanings that the change collapses?
- Are old persisted records or defaults still read correctly when a writer changes?
- Does a failure, retry, repeated operation, or partial completion leave a valid state?
- Does the real consumer use the new behavior, or does only an isolated helper work?
- Does an apparently local change alter ordering, aggregation, ownership, or compatibility elsewhere?

Use the questions that fit the diff; do not manufacture a finding in each category. Check generated files and configuration when they affect the actual result. Avoid requesting a broader abstraction merely because the patch introduces a small amount of duplication; explain the concrete maintenance consequence if a design change is warranted.

Separate newly introduced problems from pre-existing behavior. The same limitation may become relevant if the change newly exposes it, but state that path. Do not attribute an unrelated existing defect to the patch without evidence.

## Test a suspected issue before reporting it

For each candidate finding, identify a realistic triggering input or state, trace why the changed code reaches the problematic result, and compare it with the intended behavior. Check whether surrounding validation, a caller guarantee, or a different branch already prevents the problem.

Use targeted local checks when they are useful and permitted. Inspect commands and setup before running them, especially if they may install software, contact services, or change data. Prefer an isolated original input or an existing suitable test over a large new harness. Do not alter assertions or product code to make a demonstration succeed.

Execution is not always necessary: a clear unreachable branch or incompatible interface can be established from source. State the evidence actually available. When uncertainty remains, explain the missing condition as a focused question rather than presenting a hypothetical failure as confirmed.

Assess tests by what they protect. A test that calls a new helper may miss the public path; a large snapshot may not distinguish the wrong behavior. Suggest a meaningful missing case when it would catch a specific defect or protect an important changed contract. Do not demand new tests for every formatting change or prescribe a different testing style without a project reason.

## Return actionable findings

Lead with the issues that most affect correctness or user-visible behavior. For each substantive finding, include:

- A precise location in the reviewed version
- The condition under which the problem occurs
- The observable consequence and why it conflicts with the requirement or established contract
- Supporting source or executed-check evidence, with uncertainty stated
- A concise correction direction when useful, without prescribing an unneeded rewrite

Keep findings independent. Combine multiple symptoms of one cause, and avoid repeating the same issue at every call site. Use the project's severity convention if provided; otherwise explain impact directly. Optional maintainability suggestions should be visibly separate from defects that affect acceptance.

If there are no substantiated findings, say so and identify the meaningful review scope and remaining limitations. Do not equate a clean review with proof that no defect exists. A short note about an untested integration can be useful; a generic disclaimer list is not.

Before finishing, recheck locations and evidence against the reviewed files. Report checks that passed, failed, or could not run accurately. If posting review comments was requested, use the verified change and destination, avoid duplicate comments after an uncertain response, and confirm the result. Otherwise deliver the review to the user without external side effects.
