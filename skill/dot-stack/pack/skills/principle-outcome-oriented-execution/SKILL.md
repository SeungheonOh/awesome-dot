---
name: principle-outcome-oriented-execution
description: "Carry a planned local rewrite or migration to explicit verification boundaries without accumulating unnecessary compatibility code or weakening the final acceptance contract."
---

# Outcome-oriented execution

Use this for an agreed rewrite or migration whose target and intermediate boundaries are explicit. It permits carefully isolated intermediate breakage, not broken shared environments or vague promises to fix things later.

## Declare the end state and containment

Before editing, name the target behavior and architecture, preserved contracts, known-good baseline, verification milestones, and rollback or recovery path. Identify where temporary inconsistency is allowed: for example, an isolated working copy during a coordinated signature migration. Shared mainline, deployed services, and independently consumed artifacts retain their own stability requirements.

Group edits by coherent changes. Keep high-signal checks available for areas being actively migrated even when the full suite is temporarily expected to fail. Record which failures are anticipated and why, so a new regression cannot hide inside a general “migration in progress” label.

Do not introduce an adapter solely to keep every keystroke green when the whole controlled caller set will change before the next check. Conversely, retain transitional compatibility when independently deployed versions, external consumers, or rollback require it. End-state simplicity and safe delivery must both be designed.

At each declared milestone, run its acceptance checks and reconcile the actual artifact. Fix unexpected failures before dependent work relies on the result. At completion, rerun the applicable full static, runtime, integration, and artifact checks against the integrated candidate; earlier local passes do not transfer automatically.

## Example and counterexample

Applies: replace an internal return type across a package in an isolated workspace. Update the type and all controlled callers together, then run type checks and caller-level tests at the planned boundary. A throwaway adapter between every edit adds no value.

Does not apply: change a production database column while old application versions are still serving traffic. Use a compatible rollout sequence rather than tolerating broken intermediate deployments.

## Stop and report

Do not redefine acceptance criteria, delete meaningful tests, or suppress errors to declare the target reached. If the end state becomes infeasible or requires expanded authority, stop the affected transition and explain the decision needed. Report planned intermediate failures separately from unresolved final defects. An unverified milestone is not ready for dependent delivery, merge, or deployment.
