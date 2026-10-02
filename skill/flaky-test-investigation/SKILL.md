---
name: flaky-test-investigation
description: "Investigate inconsistent test results with bounded, reproducible runs, distinguish product defects from test or setup assumptions, and verify authorized fixes without weakening failure detection."
---

# Investigate a Flaky Test Without Hiding the Failure

Use when a test sometimes passes and sometimes fails, or differs between local and CI runs. Establish what varied, preserve all relevant outcomes, and identify the narrowest supported cause. When the user authorizes a fix, apply and verify it in the requested environment. “Passed after retry” is an observed sequence, not evidence that the failure is resolved.

## Intake and authority

Resolve the repository/worktree, exact test selector, relevant code revision and dirty diff, original failing run, available logs/artifacts, environment and requested outcome. Distinguish investigation from permission to edit, commit, push or change CI policy. A request to fix the named test already authorizes a scoped code edit and relevant safe tests; do not demand a separate approval for each local change. It does not authorize disabling coverage, changing production semantics or applying unrelated refactors.

Read repository instructions and the test's data/service requirements before execution. Use the user-selected environment and existing project tooling. If a run would mutate a shared service, consume paid capacity, expose private records or require new access, establish the necessary authorization before that run. Prefer isolated fixtures and disposable resources. Do not copy secrets into commands, logs or reports.

If the failure is known to concern security behavior, preserve the security assertion and use an appropriate defensive review. Do not reproduce an exploit or probe a third-party target as part of this workflow.

## 1. Preserve the original observation

Capture the first available failing run before rerunning anything:

- Commit/revision plus dirty diff digest; test-file revision separately when useful
- Full test selector and invocation, runner version, relevant dependency/lockfile state
- Seed or explicit “not recorded/not randomized,” test order, worker count and retry configuration
- OS/runtime, timezone, locale, clock control, environment flags and fixture/service versions relevant to the failure
- Exit status, failed assertion or setup stage, expected/actual values, and log/artifact references
- Run identity, attempt identity and any enclosing CI job identity

Use allowlisted environment fields; never dump the entire environment or credential-bearing URLs. Preserve useful logs before cleanup can erase them. A setup crash, timeout, cancellation, skip or runner error is not an assertion failure and is not a pass.

A runner may hide automatic retries behind one final green result. Inspect its configuration and available attempt artifacts. Disable hidden retries in an isolated diagnostic invocation when supported and safe, without changing shared CI policy. If the original attempt denominator cannot be recovered, mark it unknown rather than inferring it from the final badge.

## 2. Define a bounded experiment before running it

State a hypothesis, the smallest test scope, controlled variables, variables to vary, and the run budget. Choose the budget based on cost and the question: a short seeded matrix, an exact finite permutation set, or a limited original-seed replay may be enough. Honor any user limit. Record it before looking at results.

Define stop conditions: budget exhausted; decisive assertion evidence obtained; an unsafe side effect or environment fault blocks valid testing; or a required dependency becomes unavailable. Do not extend retries merely to obtain a pass. A new experiment can follow when a specific next hypothesis justifies it within the original task; give it a separate budget and keep earlier runs in the record.

For every experiment preserve:

| Field | Meaning |
| --- | --- |
| Planned slots | The predeclared attempts and their seeds/variants |
| Attempted slots | Every launched attempt, including setup failures and canceled attempts |
| Outcome ledger | Assertion pass, assertion fail, setup/runner error, timeout, cancellation or skip for each slot |
| Completed comparisons | The denominator for pass/fail assertions, distinct from all attempts |
| Unrun slots | Slots not launched because the experiment stopped, with the reason |

Report the observed failure ratio with its denominator and experiment conditions. Do not pool different revisions or environments into one rate, drop failed retries, or interpret a small chosen seed sample as an estimated production failure probability.

## 3. Isolate the cause with controlled comparisons

Start by reading the failing assertion and the product contract it intends to enforce. Identify the earliest divergence, not merely the final exception. Inspect the relevant code and fixture setup before launching a broad suite.

Then choose the branch supported by the evidence:

| Evidence or hypothesis | Next comparison | Interpretation boundary |
| --- | --- | --- |
| The same input and environment produce different allowed output order | Compare the full records ignoring only order, against the documented contract | Unspecified order may be a test assumption; do not add production sorting just to make the test green |
| Output sometimes violates a required product invariant | Replay the smallest captured input, seed and execution conditions | Treat this as a product defect until contrary evidence exists, even if retries usually pass |
| Failure depends on another test or parallel execution | Compare isolated vs a recorded predecessor/order, then worker count | Check shared fixtures, mutable globals, resource collisions and cleanup; isolation alone does not prove the product is correct |
| Boundary failures involve wall time, randomness or async completion | Control one source at a time; inspect an actual readiness/event condition | A larger sleep or timeout can mask the cause; preserve genuine timeout and deadline semantics |
| Setup differs across machines or CI | Compare runtime, dependency lock, locale, timezone, service version and fixture state | A setup failure belongs in the environment outcome category; do not “fix” it by relaxing assertions |
| A remote dependency responds inconsistently | Separate the integration contract from an isolated deterministic fixture | Keep the integration failure visible; a mocked test does not prove the remote path is healthy |
| All bounded replays pass | Review original artifacts and uncontrolled variables | Conclude “not reproduced under these conditions,” not “fixed” or “the original failure was noise” |

Change one meaningful variable per comparison where possible. Preserve the original failing seed/order before minimizing. If minimization changes the outcome, retain both the working and failing reproductions; do not claim the smaller case reproduces the original defect. If evidence supports multiple causes, keep them separate.

## 4. Choose and apply a scoped repair when authorized

Write down the invariant the test must continue to enforce, the evidence for the cause, the intended edit and the expected before/after behavior.

- **Product invariant violated:** repair the responsible behavior and retain or strengthen the regression assertion. Do not move the expectation to match erroneous behavior.
- **Test demands behavior the contract does not promise:** adjust only that assumption. For unordered records, compare a multiset of complete contract-relevant records, preserving multiplicity and field values.
- **Fixture/setup isolation defect:** correct ownership, deterministic setup or cleanup at the smallest appropriate scope, then check the relevant interaction again.
- **Cause not established:** present evidence and a bounded next experiment. Do not make a speculative relaxation and label it a fix.

For order-insensitive checks, a lossy set is usually wrong: it discards duplicate counts. Sorting can work only with an appropriate complete key and unchanged multiplicity. A multiset comparison requires a well-defined canonical representation; validate schema/types and include every field relevant to the contract. Do not silently strip volatile-looking fields, round values or coerce types simply to make records equal. If a field is intentionally excluded, cite the contract or explicit test design that permits it.

Avoid blanket exception handling, skip/xfail markers, deleted assertions, broad tolerance increases and extra retries as substitutes for a repair. Quarantining a test or changing CI retry policy is a separate decision with visible failure reporting and an owner; do not do it implicitly during investigation.

If only investigation is authorized, provide the narrow proposed diff and its verification plan without changing the worktree. If edits are authorized, inspect the actual diff afterward and confirm that only intended behavior changed. Follow the user's separate instructions for committing or opening a PR; do not infer those from permission to edit.

## 5. Verify that the fix still detects defects

Use independent checks, not a green rerun alone:

1. Replay the original failing seed/order/environment as closely as possible. State any unavailable condition. Keep before and after results under distinct revision labels.
2. Re-run the same predeclared input matrix on the changed revision. Preserve every attempted outcome and stop under the experiment's bounds.
3. Exercise another relevant dimension suggested by the cause, such as a finite set of record permutations or the interfering predecessor test. Do not imply exhaustive coverage unless the allowed space was actually exhausted.
4. Supply deliberately invalid fixture outputs or an isolated temporary mutation and verify that the assertion fails. For unordered records, include a missing record, an extra record, an added duplicate, a same-length duplicate substitution and a changed field. Do not introduce these defects into shared production or persistent source files.
5. Run the affected nearby tests or suite slice, when safe and within scope. Record broader tests as unrun if unavailable. A toy example or unit test cannot stand in for integration/CI evidence.
6. Inspect cleanup and the final diff. Ensure test data, temporary mutations and diagnostic flags did not leak into the proposed repair. Preserve the original failure artifacts.

If the intended negative control passes, the assertion is too weak or the control is wrong; investigate before calling the fix verified. If failures persist, retain them and continue the relevant authorized diagnosis rather than counting only the successful attempts.

## Output record and completion

Return:

- **Finding:** product nondeterminism, unsupported test assumption, setup/environment defect, mixed causes or inconclusive, with exact supporting evidence
- **Reproduction:** command/selector, revisions, environment, seeds/orders and minimal fixture references
- **Run ledger:** separate experiment budgets and denominators; all passes, failures and other outcomes; links to raw evidence
- **Repair:** authorized diff or unapplied proposal, preserved contract and scope of change
- **Verification:** original replay, before/after matrix, negative controls, relevant broader tests and unverified conditions
- **Next decision:** only the specific access, consequential edit or unresolved evidence needed to proceed

Use calibrated completion language: “the order assumption was repaired and the scoped checks passed” is supported by a verified test edit; “the suite can no longer flake” is not. Stop when the requested investigation or authorized fix is complete with its limits clear, or when a specific blocker requires the user's decision.

## Worked example

Read [example.md](example.md) for a fictional unordered-record response whose test accidentally requires list order. Run `python3 check_example.py` from this folder to compare the original assertion with a multiplicity-preserving repair, execute every permutation of the small fixture, and prove invalid records still fail. [example-results.json](example-results.json) contains the actual local outcomes, denominator, seeds, implementation digests and environment. The demonstration makes no claim about a live repository or CI service.

For a product-logic concurrency defect, read [the controlled lost-addition companion](concurrency/example.md). It keeps the exact-total assertion while comparing a shared-lock repair under forced interleavings and ordinary local runs. The actual result ledger separates expected before-repair failures from runner errors and bounds the repair to one owner on one event loop.
