---
name: refactor-code
description: Improve the structure of existing code while preserving its required observable behavior. Use for a requested refactor, consolidation, or simplification, rather than a new feature, bug diagnosis, or dependency upgrade alone.
---

# Refactor Code

Make the code easier to understand or change without silently changing its contract. Choose a concrete structural improvement and verify that real callers still receive the behavior they rely on. A smaller diff or fewer lines is not by itself evidence of a better design.

## Define the improvement and preservation boundary

Read the request, applicable project instructions, relevant code, and current changes. Identify the actual problem: duplicated rules drifting apart, a function mixing unrelated responsibilities, an awkward dependency, or another specific obstacle to maintenance. Preserve the user's chosen scope rather than treating “refactor” as permission to redesign the project.

Determine what must remain observable: outputs and their types, ordering, errors, side effects, persisted formats, public names, or performance constraints that the application actually relies on. Do not assume two implementations are equivalent because their ordinary return values match.

Inspect real callers and relevant tests. A symbol that looks internal can still be used by configuration, serialization, dynamic loading, or an extension interface. Check these paths when the proposed change affects them; do not rename public or persisted identifiers merely to make local names more consistent.

Separate a known bug from the refactor. If fixing it changes observable behavior, make that an explicit part of the request or keep it separate. Existing tests are evidence, not an infallible specification; resolve a material conflict with the intended contract instead of preserving or changing it by accident.

Keep staged, unstaged, and untracked work intact. Use an isolated branch or copy when helpful and authorized, ensuring it includes the inputs the refactor actually depends on. Unrelated dirty work is not a reason to discard changes or stop the whole task.

## Choose a narrow structural route

Prefer the smallest coherent change that addresses the maintenance problem: extract a responsibility, consolidate a rule, simplify control flow, or introduce a useful interface. Explain the dependency direction or ownership that the new structure makes clearer. Avoid adding abstraction layers that merely move complexity out of sight.

Identify the integration point before creating a replacement. A new shared helper is useful only when the intended paths use it, and a moved function must still be reachable through the required public interface. Include necessary imports, generated bindings, and documentation updates without expanding into unrelated cleanup.

Break a large refactor into steps that can be checked meaningfully. Keep a working state between steps where practical. Do not impose a fixed commit count or rewrite everything at once to achieve an ideal architecture.

## Establish useful behavioral evidence

Use existing focused tests and representative inputs to establish the behavior being preserved. Add a small characterization check when a consequential behavior has no coverage. Do not create a large snapshot that freezes incidental output or merely copies the implementation's assumptions.

When comparing old and new behavior, give each version an equivalent fresh input state. Reusing an input mutated by the first run can make the comparison misleading. Include side effects and exceptions when they are part of the contract. Preserve order, multiplicity, types, and missing-value distinctions unless the contract explicitly permits treating them as equivalent.

Select a boundary that could expose the structural change: a second caller with different input conventions, an empty collection, a repeated operation, or a failure partway through, as relevant. Avoid enumerating unrelated edge cases just to enlarge the test suite.

Inspect the effects of commands before running them, and use the project's existing permitted test path. Source inspection can support a limited conclusion when execution is unavailable; it cannot establish that the refactored application ran successfully.

## Refactor and verify the real paths

Make the structural change using the repository's conventions. Keep behavior changes out of the same edit unless they are separately requested and clearly identified. Avoid opportunistic dependency upgrades, broad formatting churn, or new configuration switches.

Run checks that exercise each affected caller, not only the new helper. Verify that the old implementation is no longer used where replacement was intended, while compatibility wrappers or public exports remain where required. Remove unused code only after checking its actual references and supported loading paths.

Some tests may encode an internal structure that the refactor intentionally changes. Update those tests to assert the relevant contract when appropriate; do not weaken a behavior assertion to accommodate a regression. If a comparison fails, explain the difference before deciding it is harmless.

After the final edit, run the justified project checks and inspect the complete diff. Look for accidentally changed constants, defaults, evaluation order, mutation timing, exception behavior, or resource ownership. Check that any claimed performance improvement was actually measured under a stated workload; clearer code alone does not establish faster execution.

## Deliver the refactor

Explain the structural improvement and why it helps the requested maintenance task. Point to the affected code and summarize the evidence that required behavior remains intact. State any blocked check or unresolved compatibility question precisely.

If behavior changed intentionally, identify it separately from the refactor. Preserve existing work, leave a reviewable final diff, and follow the user's established scope for commits or publication. Do not claim deployment, consumer compatibility, or production equivalence from local checks alone.
