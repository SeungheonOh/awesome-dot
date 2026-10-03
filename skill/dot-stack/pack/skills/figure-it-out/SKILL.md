---
name: figure-it-out
description: "Design and execute a bounded, auditable workflow for a complex change when no narrower workflow fits; use explicit hypotheses and acceptance checks."
---


# Figure it out

When the task has no suitable playbook, design one before making consequential changes. Do not turn an ordinary fix into a program of work. [Dot mode](../dot-mode/SKILL.md) offers the pack's shared engineering approach when available; this skill remains usable from the explicit contract below.

## Frame the outcome

State a falsifiable done condition, scope, known units of work, key unknowns, authorized actions, and dependencies. Quantify scope from an inventory where possible; label estimates and their assumptions. Choose rigor from reversibility and impact rather than always choosing maximum ceremony.

For a substantial run, show a short plan and tradeoffs early. Ask only for a material decision or missing authority. Continue independent safe work while an answer is pending. A user stepping away does not grant permissions for publication, credentials, paid services, or destructive actions.

## Design the sequence

Order verifiable units by dependency and uncertainty. Test the riskiest assumption before building its dependents. Capture a baseline using the same method that will measure the result. Use existing project checks before building a new harness.

A unit should have an input revision, a bounded change, an owner, and an observable acceptance condition. For a migration, separate discovery, representative conversion, bulk conversion, compatibility checks, and removal of proven-unused paths. Do not call the migration complete while callers remain on the old path.

Use [architect](../architect/SKILL.md) for consequential open design choices. Parallelize only across real boundaries with isolated outputs; a settled design does not need another competition. If tools for delegation are missing, execute sequentially and state the coverage impact.

## Execute as experiments

For each unit:

1. State the hypothesis and the check that could disprove it
2. Make the smallest authorized change that tests it
3. Run the check on the actual artifact, including a baseline or negative control when useful
4. Keep the change if it meets the predicate; otherwise diagnose, revise, or undo only the run's own change without discarding user work
5. Record the result and any changed assumption before dependent work continues

A passing command without meaningful assertions is not proof. Inspect returned files and results rather than trusting a worker's summary. Seek independent review for significant risk when available; label a self-review honestly. Fix an invalid gate separately and explain why the original gate was wrong, instead of silently relaxing it.

Use Verified, Failed, Unverified, and Blocked for claims. A partial or inconclusive result is not a pass. Repeated failure that challenges the design calls for re-framing; do not accumulate workaround branches.

## Keep a decision trail

Use [show me your work](../show-me-your-work/SKILL.md) for meaningful decisions, pivots, rejected attempts, and proof. Keep it local by default. Log outcome evidence and concise decision rationale, not private deliberation or secrets. Committing or sharing the trail is a separate authorized action.

## Close against the original goal

Run integrated acceptance checks against the final revision, including interactions between units. Compare with the initial predicate and scope; do not silently replace a difficult requirement. Report the custom workflow, why that rigor was appropriate, final artifact, evidence locations, open gaps, and the next needed decision. A blocked external step does not invalidate verified local work, and verified local work does not imply that external step occurred.
