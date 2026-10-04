---
name: principle-sequence-verifiable-units
description: "Organize multi-step edits or migrations into coherent dependency-aware units with explicit before-and-after checks and final integration evidence."
---

# Sequence verifiable units

Use this for a sweep, migration, broad refactor, or delivery containing several dependent changes. Choose units that each establish an observable result rather than arbitrary file counts.

## Build a sequence that explains itself

Establish the actual baseline: candidate revision, relevant existing failures, and checks that currently work. Inspect local modifications before any synchronization. A clean baseline is useful; rebasing, resetting, committing, or rewriting shared history requires the applicable authority and is not a hidden prerequisite.

For each unit, specify:

1. The invariant or behavior being changed
2. Inputs and dependencies it assumes
3. The focused check that will distinguish success from failure
4. Its expected output and recovery boundary

Order units to expose mistakes early: reproduce before repair, capture a baseline before comparison, remove proven dead structure before reshaping it, or establish a needed contract before migrating callers. Keep a failing regression demonstrably red before the fix when feasible, but do not require publishing a deliberately failing commit to a branch that must stay green.

Verify the coherent unit before dependent units rely on it. Stop and diagnose an unexpected failure rather than stacking more changes on an unexplained state. Truly independent units may proceed in parallel with disjoint ownership; reconcile their results and rerun integration-sensitive checks afterward.

A coordinated signature change may require several files to form one compilable unit. Do not insert throwaway compatibility code solely to make each individual file edit pass. If intermediate breakage is planned in an isolated workspace, define where the unit becomes green and do not deliver it earlier.

## Example and counterexample

Applies: migrate a configuration format by first testing the old fixtures and target parser, then converting a representative subset, then the full controlled set, then verifying consumers and removing the obsolete path.

Does not apply: checking only after every thousand unrelated replacements leaves a failure unlocalizable. The opposite extreme, running the entire expensive suite after each character edit, adds cost without useful evidence.

## Delivery evidence

Present the unit sequence, check results, expected versus unexpected failures, and final candidate checks. If commits or pull requests are requested, organize them to reflect this argument while honoring repository policy. Local milestones do not authorize pushes or guarantee that the integrated result passes.
