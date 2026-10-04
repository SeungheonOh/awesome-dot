---
name: principle-foundational-thinking
description: "Choose the minimum data shapes, ownership rules, and test scaffolding that make the next planned implementation steps simpler and verifiable."
---

# Foundational thinking

Use this before a change whose downstream logic depends on data layout, shared ownership, or missing verification infrastructure. Invest in foundations that have a concrete near-term consumer, not speculative flexibility.

## Work backward from the next increments

- List the domain invariants, dominant reads and writes, data volume, and lifecycle. Choose structures that make those paths direct: an index for repeated lookup, explicit variants for mutually exclusive states, or one owner for mutable resources.
- Trace concurrent actors before sharing anything. Identify what each may read or mutate, and what happens if another actor changes it between observation and use. Separate independent state; use actual synchronization when a shared invariant requires it.
- Identify the smallest missing scaffold that multiple planned steps rely on. Examples include a fixture harness for a bug fix, a schema parser for new callers, or a focused static check. Prefer existing infrastructure and avoid bootstrapping a platform for one feature.
- Consolidate domain structure and repeated decisions rather than every similar line. Three explicit statements can be clearer than a premature general-purpose abstraction.
- Deliver an increment that establishes a coherent contract and a real consumer or test. Avoid distributing one invariant across many callers as informal coordination.

If proven dead code directly obscures the change, remove it in an authorized, verifiable unit first. Subtraction is not a prerequisite to unrelated progress, and “scaffold first” is not permission to expand CI, dependencies, or deployment configuration without need.

## Example and counterexample

Applies: a scheduler is gaining retries. Define job identity, attempt state, and ownership before adding another retry boolean. Build a controlled-clock test around the transition so later queue and restart work use the same invariant.

Does not apply: correcting a known arithmetic error in one pure function does not require a new repository-wide architecture or replacement test runner. Add the smallest regression and fix the calculation.

## Evidence and stopping condition

Show which planned steps the foundation enables, how the selected data shape supports actual access patterns, and the check that proves its contract. Stop adding infrastructure once the immediate dependent work can proceed safely. A type diagram alone does not establish concurrency correctness; exercise races or explicitly leave that property unverified.
