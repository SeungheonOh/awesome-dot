---
name: design-api-contract
description: Design a usable API or library interface from consumer requirements, with precise producer and consumer obligations, a contract artifact, and checked behavioral examples. Use before implementation when the interface itself needs to be decided, rather than to document established behavior or audit supplied old and new contracts.
---

# Design an API Contract

Turn concrete consumer needs into an interface that independent producers and consumers can implement consistently. Deliver the actual contract in the requested format and the minimum behavioral reference needed to use it correctly. A list of desirable endpoints, a requirements brief, or a schema without its consequential semantics is not the finished design.

## Ground the design in consumer work

Read the requirements and relevant supplied conventions, interfaces, or consumer code. Establish what each consumer must accomplish, the information it has at the start, and what it needs to know or do afterward. Trace a representative interaction far enough to expose necessary operations and outcomes; do not survey an entire repository to design a bounded interface.

Keep three kinds of evidence distinct:

- Requirements and accepted decisions the design must satisfy
- Existing behavior or caller assumptions observed in identified sources, including their revision and scope
- Proposed choices, defaults, and unresolved decisions introduced by this design

An observed quirk is not automatically a permanent compatibility promise. Identify which existing consumers must continue to work and which behavior they actually depend on. Conversely, a new design is not permission to discard an established requirement. Surface conflicts using a concrete case on which the proposed and required outcomes differ.

Resolve choices that materially change consumer behavior. State a recommended default with its consequence when the request permits design judgment; ask when competing outcomes require a product decision the user has not delegated. Continue the independent parts. Do not hide a consequential unknown in an optional field, a broad type, or a vague promise to handle errors later. A draft may contain an unresolved decision, but say which operations or guarantees depend on it.

## Choose the public boundary

For each necessary operation, identify who supplies the input, who owns the result or resource, and what observable work the operation promises. Include an operation or field because a consumer needs its meaning, a requirement needs it, or compatibility demands it. Avoid mirroring internal tables, worker stages, classes, or convenience helpers unless they are intentionally part of the public model.

Choose the interaction style using the consumer's task and constraints. A function, iterator, asynchronous operation, request/response exchange, or message may be appropriate. Preserve a selected transport or language; do not impose resource-oriented HTTP conventions on every interface. If a consumer cannot complete its task through the proposed boundary without undocumented knowledge or out-of-band access, revise the boundary.

Make responsibility explicit. Decide which party validates, supplies defaults, releases resources, retains state, or retries where those responsibilities affect correct use. For a library, ownership, mutation, lifetime, and synchronous versus deferred failure can matter as much as the return type. For a remote or message interface, identity, correlation, delivery, and completion can be separate concepts. Promise only the distinctions needed for this interface.

## Author the contract and its semantics together

Use the user's requested format or the project's established one. Otherwise choose an appropriate concrete representation, such as a versioned HTTP specification, language-native interface declarations, or message schemas with their exchange rules. State the format and relevant version. Produce complete in-scope definitions with resolvable references; illustrative pseudocode is insufficient when the deliverable is intended for programmatic use.

Keep names and constraints authoritative in one place. Put behavior the format cannot express in a nearby reference linked to the affected operation or type. If prose narrows what a schema allows, make the constraint explicit and explain what must enforce it; do not imply that parsing the schema enforces the whole contract. Keep examples aligned with both.

Specify the distinctions that change an implementation or a caller's next step, to the depth this interface requires:

- **Inputs and results:** Define types, field meanings, units, bounds, presence, and relevant normalization. Distinguish omitted, null, and empty values when they have different meanings. Give a default's actual behavior and the party that applies it; a schema annotation alone does not apply a default. Define how outputs relate to inputs, including order, identity, or cardinality when consumers rely on them.
- **Failure and partial outcomes:** Separate an invalid invocation from an operation that was accepted and later failed. Define the stable information a caller branches on, which values are diagnostic text, and whether any result or effect can accompany failure. For multi-item work, settle whole-call versus item-level failure and how each outcome maps to its original input, including duplicate inputs if allowed. “Partial success” alone does not specify which work happened or what may be retried.
- **State and effects:** Describe externally visible state, allowed transitions, and the point at which an effect is committed when these matter. Distinguish acceptance from completion. If interruption, timeout, cancellation, or overlapping calls is possible, say what the consumer can conclude, what may already have happened, and how it can resolve an uncertain outcome. Do not imply rollback merely because a caller stopped waiting.
- **Repetition and evolution:** When retry or redelivery is relevant, define how repeated work is identified, the scope and duration of any deduplication promise, and what happens when an identity is reused with different input. Define supported extension behavior where it affects consumers, including handling unfamiliar result variants or errors. Distinguish the revision of this design from a promised public version and compatibility policy; do not invent a release or deprecation commitment.

Do not fill these categories mechanically. A pure local function may need no persistent identity or lifecycle, while an asynchronous effect cannot be specified adequately by input and output shapes alone. Avoid unsupported timing, throughput, durability, or exactly-once guarantees. If a requirement calls for one, define its observable scope and identify any feasibility assumption before presenting it as settled.

## Check the design from both sides

Build a small, coherent set of examples around the decisions most likely to produce different implementations. Show concrete inputs, relevant starting state, the expected result or allowed outcomes, effects, and the consumer's next step. Reuse identifiers and state consistently across a sequence. Include a failure or boundary case when it changes how a consumer must use the interface; do not generate a fixed matrix of fixtures for every operation.

Walk each example as both producer and consumer:

- Can the producer decide what it owes using the defined input and state, without inventing a missing rule?
- Can the consumer distinguish outcomes and act correctly using only information the interface exposes?
- Could two implementations satisfy the written clauses yet disagree on an outcome important to the requirements?

Repair the contract when an example needs an unstated rule. Do not change an expected outcome merely to fit a convenient shape. When several outcomes are deliberately permitted, describe the permitted set and how consumers handle it; a single example must not accidentally promise deterministic ordering or a race winner.

Check important requirements against observable clauses and examples. Then check the examples against exact types, constraints, errors, and state rules. Use an available appropriate parser, schema validator, or type checker for the artifact when practical. Report what ran and its limits: syntax or schema validity does not establish behavioral consistency, design suitability, or live provider conformance. If a tool is unavailable, finish the supported manual checks and name the unrun check rather than claiming it passed.

## Deliver a usable design

Return or save the contract artifact in the authorized destination, together with the behavioral reference and examples a consumer needs. Keep material choices, their rationale, and unresolved decisions concise and adjacent to the affected contract. Preserve useful existing content when editing a requested design. Read back the saved artifact and verify its references and example consistency.

State what is proposed, what existing constraints were preserved, and what was actually checked. Distinguish a coherent reviewable proposal from a contract ready to implement when a consequential decision remains open. Do not claim backward compatibility from the design alone; a directional comparison against supplied prior contracts and consumers is separate work when requested.

Contract design does not itself authorize endpoint discovery or calls, implementation, account changes, publication, or deployment. If the user also requested implementation, continue within that authorization once the contract is sufficiently decided; do not create an extra approval gate just because a design artifact now exists.
