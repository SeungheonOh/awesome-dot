# Design red flags

A flag prompts inspection, not automatic rejection. Show a concrete caller or change that pays the cost.

## Shallow modules

A public interface is shallow when callers learn almost as much policy as the implementation contains. Warning signs include coordinating many methods for one operation, options that expose internal stages, and a wrapper that requires knowledge of the wrapped object. Compare the complexity hidden by the interface with the burden imposed on callers. A deep module can have several methods; a long call chain is not depth.

## Leaked decisions

If changing a storage schema, retry policy, or wire representation requires coordinated edits in unrelated modules, one decision has several owners. Parse external input into a domain value at an explicit boundary. Keep a generated transport type at a public boundary only when that protocol is intentionally the API; do not create a second model merely to hide a name.

## Decomposition by time alone

Separate load, validate, transform, and save modules may repeat the same invariants. Group decisions by the knowledge they protect. Keep stages separate where streaming, transactional behavior, replacement of a component, or independent testing makes that separation useful. Execution order alone is not a sufficient reason.

## Pass-through layers

A method that forwards identical arguments and results adds a hop. Remove it when it adds no policy, adaptation, lifecycle boundary, or stable interface. An intentional seam for a real external dependency can justify forwarding; imagined future use cannot.

## Invariants written only in prose

“Call begin before save” or “duration cannot be negative” deserves a state model, validated constructor, or test when feasible. A numeric field alone does not enforce a numeric constraint. Check that the proposed type actually excludes the invalid value under the project's compiler settings.

## Shared ownership disguised by naming

Two “independent” workers writing one state file still share mutable state. Prefer isolated state and an explicit integration owner when possible. If a shared transaction is inherent to the domain, specify its concurrency and recovery semantics instead of pretending separation solves it.
