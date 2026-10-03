---
name: principle-model-the-domain
description: "Replace scattered state assumptions or duplicated rules with a representation that encodes the actual domain, transitions, and access patterns."
---

# Model the domain

Use this when stateful logic relies on booleans that must agree, repeated shape assumptions, duplicated branches, or lifecycle rules spread across modules. First identify what the system must never allow and how callers actually use the data.

## Select a representation for a real problem

Write the valid states, transitions, identities, ownership, and relevant reads and writes. Separate facts from derived values. Then choose a shape that removes a demonstrated failure mode:

- An explicit state machine or tagged union for mutually exclusive phases
- A typed object for values that travel together under one invariant
- A map or registry for a stable key-to-behavior relationship
- A reducer or command/event model when transitions need centralized validation or replay
- A queue, index, normalized collection, graph, or tree when the access pattern warrants it
- A small domain-owned module when the same knowledge is repeated through “load,” “validate,” and “save” phases

Execution order does not determine ownership. Put a rule where the domain concept is defined, then let adapters and workflow steps use it. At external or persistence boundaries, validate or migrate data into the model rather than asserting that old values already comply.

Evaluate the proposed model by what it eliminates: invalid combinations, duplicated decisions, synchronization, expensive repeated scans, or lifecycle ambiguity. Do not add a general state-machine library, event store, or registry merely because one is available. A local conditional can be the clearest representation of a genuinely local choice.

## Example and counterexample

Applies: `isLoading`, `hasData`, and `hasError` permit contradictory UI states. Model idle, loading, ready-with-data, and failed-with-error variants, then define cancellation and retry transitions. If stale data is intentionally visible during refresh, represent that legitimate state rather than forbidding it accidentally.

Does not apply: a pure two-branch formatting function has no shared state or repeated rule. A command bus would add indirection without removing risk.

## Verification

Enumerate legal transitions and at least one formerly possible invalid state. Exercise construction, transitions, persistence round-trips where relevant, and representative caller behavior. Compare branches or rules removed, not just new type names. Stop when the representation expresses the actual contract; retain explicit handling for uncertainty that the domain genuinely contains.
