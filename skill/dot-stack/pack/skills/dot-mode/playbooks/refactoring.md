# Refactoring

Use for a focused or medium structural change with unchanged intended behavior. Read the [execution contract](../references/execution-contract.md). A behavior change discovered during cleanup is a separate decision, not a hidden part of the refactor.

## Inputs

The structural problem, consumer contract to preserve, caller inventory, target shape, and authorized scope. For broad migrations, add [Multi-phase plan](multi-phase-plan.md) or a bounded bespoke workflow.

## Steps

1. Pin behavior before moving structure. Use a characterization test, baseline replay, snapshots with known meaning, or an equivalence harness. Typecheck and lint alone do not pin runtime behavior. Record existing failures and unsupported cases.
2. State the target module/type/call-graph shape and why it lowers reader load or eliminates invalid states. Leave straightforward local code alone when the proposed abstraction adds only indirection.
3. Inventory consumers beyond imports: strings, dynamic registries, generated inputs, documentation examples, tests, configuration, and external/public contracts. Verify dead code is actually unused before deleting it. Preserve legal and explanatory comments that carry real constraints.
4. Move in small behavior-preserving units, checking the pin after each. Migrate internal callers and remove the old internal API in the same coherent wave when feasible. A public compatibility obligation may require a staged adapter and retirement condition; do not break an external contract to obey an aesthetic rule.
5. Keep one writer per affected file/worktree. Delegate mechanical disjoint edits when useful, supplying exact rename mappings and invariants. Inspect the final integration for missed aliases and stale generated artifacts.
6. Run equivalence at the consumer boundary on baseline and candidate. Include error behavior, ordering, serialization, persistence, and timing contracts where relevant. On a UI reshape, replay meaningful interactions; on a library change, exercise the public API.
7. Assess whether the change earned its cost. Identify fewer concepts, narrower mutable scope, clearer ownership, or removed duplication with evidence. Revert unnecessary owned work if it does not improve the target. Deliver locally or publish only within authorization.

## Failure and completion

If a behavior pin fails, determine whether it exposes a refactor defect, an unreliable pin, or an intentional new requirement. Do not update expected values just to pass. Stop or route a new behavior request explicitly. Return the structure changed, pinned contract, equivalence result and candidate identity, reader-load benefit, and any deferred caller or compatibility limitation.
