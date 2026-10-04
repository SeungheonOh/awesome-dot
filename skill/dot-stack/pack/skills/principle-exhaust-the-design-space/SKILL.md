---
name: principle-exhaust-the-design-space
description: "Compare distinct, concrete alternatives for a consequential novel interaction or architectural choice before committing to an expensive direction."
---

# Explore the design space

Use this when several plausible approaches fit a consequential requirement and the existing codebase does not settle the choice. Exploration should reduce decision uncertainty, not become a quota of prototypes.

## Set up a fair comparison

State the user outcome, hard constraints, unknowns, and the cost of reversing the decision. Pick the smallest evidence-producing representation: a sketch for navigation, a runnable slice for interaction feel, or a load experiment for a storage choice. Two or three meaningfully different alternatives often suffice; variants of the same idea do not test the underlying decision.

Compare on criteria chosen before the result is known:

- Does the main workflow succeed, including an important failure or interruption?
- What complexity, migration burden, accessibility requirement, and operational cost does it introduce?
- Which assumption is each alternative testing, and what evidence would eliminate it?
- Can an existing simpler approach satisfy the same constraints?

Hold representative inputs and environment constant where possible. Keep exploration isolated from production behavior. If parallel workers are available, independent prototypes can save time; sequential sketches are equally legitimate. No tool or model diversity is required to count alternatives.

Choose when the comparison resolves the material uncertainty. Explain the deciding tradeoff and what evidence could change the choice. Preserve useful findings without carrying throwaway prototypes into the production design by accident.

## Example and counterexample

Applies: a complex selection workflow has no precedent. Compare a staged dialog with inline selection using the same keyboard-only task and cancellation scenario. Observe errors and recovery, not just screenshots.

Does not apply: extend a well-established validation rule to one new field, or implement a protocol whose compatibility requirements leave only one viable shape. Follow the constraint and verify it rather than staging an artificial contest.

## Stopping condition

Bound exploration by the decision it must answer and the resources the task allows. If alternatives tie on relevant criteria, prefer the simpler reversible choice. If product priorities or an unapproved scope change determine the winner, present the comparison and ask for that decision; do not keep prototyping indefinitely or silently pick a new product direction.
