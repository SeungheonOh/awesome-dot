---
name: principle-redesign-from-first-principles
description: "Reconsider a design when a new requirement exposes a structural mismatch, then choose the smallest authorized migration toward a coherent target."
---

# Redesign from first principles

Use this when a new requirement strains a core assumption and a local patch would scatter exceptions through the design. Start from the requirement's meaning, then decide how much change is actually justified.

## Separate the ideal model from the delivery plan

Read the affected interfaces, callers, persistence, tests, and documentation. Identify what must remain compatible and what the task permits changing. Ask what a clean design would look like if the new requirement had always existed, while retaining the real constraints rather than imagining a constraint-free system.

Sketch the target around domain concepts, ownership, and invariants. Compare it with a bounded adaptation of the current design. Consider the cost of migration, operational risk, data conversion, review burden, and future changes. A clean-sheet sketch is a reasoning aid; it does not require a clean-sheet implementation.

Choose a coherent boundary where the change belongs. Propagate the selected contract through the affected types, callers, error behavior, tests, examples, and rationale. Avoid adding one boolean at every layer when the domain needs an explicit variant or ownership change. Do not change unrelated layers merely to make the design look uniform.

Deliver through verifiable increments with compatibility and rollback requirements accounted for. Where a transitional adapter is needed, specify its consumer and retirement condition. If the required redesign exceeds the agreed scope, present the smallest viable alternatives and the decision needed before expanding the work.

## Example and counterexample

Applies: a single-owner document system gains collaborative editing. Trace identity, authorization, persistence, and concurrency assumptions; design explicit membership and version semantics before spreading `isShared` checks throughout the code. Then migrate one supported boundary at a time.

Does not apply: an isolated off-by-one defect has a correct existing model. Fix and test the calculation instead of rebuilding the subsystem. Nor does a new optional field automatically justify a new architecture.

## Evidence and stop

Show the violated old assumption, the target invariant, why the chosen change is proportionate, and the checks that establish preserved and new behavior. Include migration-sensitive paths, not only the new happy path. Stop expanding the design when additional change no longer serves the requirement or a demonstrated defect; preserve external contracts unless an authorized migration changes them.
