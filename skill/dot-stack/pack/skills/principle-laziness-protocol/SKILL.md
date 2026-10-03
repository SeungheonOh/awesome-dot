---
name: principle-laziness-protocol
description: "Reduce maintenance cost during a refactor by removing unnecessary decisions, state, and pass-through layers while preserving the required behavior."
---

# Laziness protocol

Optimize for the least ongoing complexity that satisfies the task, not the fewest characters in a diff. Use this when a design accumulates wrappers, repeated decisions, synchronized flags, or a signal threaded through many layers.

## Look for work the system need not do

- Inspect whether a new behavior can reuse an existing domain boundary instead of introducing another path. Consolidate one decision at its source and pass a meaningful result rather than re-deriving it in every caller.
- Remove proven dead paths and unnecessary pass-throughs. A layer earns its place by hiding a meaningful decision, isolating a dependency, enforcing policy, or making a contract testable. Its file count or number of callers alone is not the test.
- Question new signal threading. Is the signal domain data that belongs in the existing model, local policy that belongs at the edge, or a symptom of misplaced ownership? Do not replace explicit parameters with hidden global state simply to shorten signatures.
- Derive values rather than synchronizing copies when cost and consistency requirements allow. Keep explicit state where it represents history, ownership, or an externally meaningful transition.
- Prefer a focused fix over unrelated cleanup. A slightly larger coherent change can be simpler than a small patch that adds a permanent exception; compare both behavior and future coordination costs.

Retain names, types, guards, and rationale comments that reduce mistakes. “Less code” is not a reason to remove error handling, compatibility, security boundaries, licensing, or a useful test.

## Example and counterexample

Applies: three wrappers merely forward an unchanged request through one-caller modules. Collapse the accidental indirection and keep the one adapter that actually translates the external contract. Verify the same public behavior.

Does not apply: a tiny authorization adapter has one caller but centralizes an important policy and audit boundary. Inlining it across controllers would increase maintenance risk even if today's diff shrinks.

## Proof and stop

Explain which duplicated choice, state synchronization, or navigation burden disappeared. Compare representative paths and regression results, not an arbitrary line-count or three-layer limit. Stop once the requested behavior is coherent and the remaining layers have a clear responsibility; do not use a bounded refactor to chase every imperfection in the repository.
