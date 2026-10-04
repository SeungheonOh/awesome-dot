---
name: principle-migrate-callers-then-delete-legacy-apis
description: "Coordinate an internal API replacement by inventorying consumers, migrating the controlled caller set, and removing the old path only when compatibility permits."
---

# Migrate callers, then delete legacy APIs

Use this when an agreed new internal contract should replace an old one and the relevant consumers can move together. Avoid keeping two permanent paths solely because caller migration was left unfinished.

## Establish the migration boundary

Inventory direct calls, imports, wrappers, generated clients, tests, documentation, examples, configuration references, and dynamic registration where relevant. Identify public or independently deployed consumers; a text search with no matches does not prove their absence. State which callers are controlled and what compatibility guarantees apply.

Write the new contract and behavioral equivalence or intentional change before editing. Then:

1. Introduce the replacement with tests for its observable contract.
2. Migrate the known controlled callers, including failure paths and boundary conversions.
3. Run caller-level and integration checks against the same candidate. Update examples and documentation that teach the old path.
4. Verify no required caller still depends on the old entrypoint. Remove obsolete implementation and implementation-specific tests while retaining tests for behavior that still matters.
5. Check the resulting exported surface and the requested deployment sequence before declaring the old API retired.

If an adapter is temporarily necessary, give it a concrete owner, consumer list, compatibility purpose, and removal condition. Prefer one boundary adapter to scattered dual-path branches. “Temporary” without a retirement condition is an architectural decision in disguise.

## Example and counterexample

Applies: all three callers of an internal formatter live in one package. Migrate them to a typed result, verify their output, remove the old nullable function, and update its examples in one reviewable wave.

Does not apply: a public SDK method has unknown external consumers, or an old service version must coexist during rollout. Preserve the promised compatibility through versioning or an expand/migrate/contract plan. Do not remove the old method merely because the repository has no remaining callers.

## Stop and evidence

Stop deletion when consumer ownership, rollout order, or compatibility is unresolved. Continue preparing and testing the migration locally. Return the caller inventory, explicit compatibility decision, remaining adapter obligations, and checks run. A local refactor does not itself authorize publishing a breaking release or changing production traffic.
