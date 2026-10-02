---
name: design-data-model
description: Design a usable domain and storage model from requirements, including identities, relationships, constraints, history, and representative reads and writes. Use when the model itself needs to be decided before implementation, rather than to define a public API contract or execute a migration of a supplied model.
---

# Design a Data Model

Turn the required behavior into a model that can represent the right facts and answer the intended questions. Deliver the actual conceptual or logical model, requested storage definitions, and coherent examples of how data changes and is read. An entity list or diagram without meanings and rules is not a completed design.

## Start with the facts the model must preserve

Read the requirements and relevant existing models, example data, and read/write code supplied for this task. Identify what must be recorded, what can change, and what users must be able to recover or distinguish later. Keep accepted requirements, observed conventions, and proposed choices distinguishable. An existing field name is evidence about the current representation, not a complete definition of its meaning.

Work from concrete cases: who or what exists before a write, what new fact the write records, and what a later reader must see. Include history only to the depth required by the work. “Show the current owner,” “show who owned it on a date,” and “show what we believed its owner was when a report ran” require different stored facts.

Preserve the chosen engine, model style, and project conventions unless the task asks to reconsider them or they cannot satisfy a requirement. If no storage target is chosen, produce a useful logical model without disguising SQL as a neutral default. Recommend a target only when choosing one is in scope; identify any physical design decisions that depend on it.

Resolve domain ambiguities by their consequences. Recommend and label a reasonable default when design judgment is delegated. Ask when a choice changes a material business meaning the user has not settled, such as whether two registrations for the same person count as a duplicate or two attendances. Continue independent parts and mark the affected rules and examples as provisional. Do not hide that choice in a nullable field or an unconstrained status string.

## Represent distinctions that change the outcome

Settle the following where they affect this model; do not add fields or machinery just to cover every category:

- **Identity and occurrences.** State what one record represents and what makes it the same thing over time. Distinguish a person from their membership, a reservation from each scheduled occurrence, or an observation from a retry of its ingestion when those distinctions matter. Define identifier scope, meaningful uniqueness, and whether a business identifier can change or be reused. A generated ID alone does not prevent two records for the same domain fact. Conversely, equal values do not necessarily identify a duplicate.
- **Relationships and ownership.** Give both directions' cardinality and optionality, including any minimum participation the requirements need. A foreign key or reference need not establish that a parent has at least one child. Model a relationship as its own fact when it has attributes, independent identity, or history. Define what happens when an owner is removed, an object is reassigned, or the link ends; distinguish deleting a relationship from deleting either participant. Choose embedding or referencing with the actual lifetime, sharing, and update boundary in view.
- **State and history.** Identify the authoritative current state and which past facts must survive. Specify whether a change overwrites a value, ends a validity interval, appends an event, or creates a revision. Define restricted state transitions and the facts needed to enforce them when relevant. Distinguish an event's occurrence time, a fact's effective time, and the time it was recorded when requirements depend on more than one. Explain corrections, late-arriving facts, and ties only when they affect required answers. An updated timestamp is not a history model; retaining every event does not by itself define current state.
- **Missing values.** Give absence a domain meaning: unknown, not applicable, not yet collected, or deliberately cleared, as applicable. Distinguish missing, null, empty, and zero only where the domain needs them, and ensure the selected representation preserves those distinctions. State when defaults apply and who applies them. A convenient default must not turn an unknown quantity into a known zero or invent a historical date.
- **Quantities and time.** Specify units, precision, allowed ranges, and relevant rounding or conversion rules. Preserve the currency or unit needed to interpret an amount. Distinguish instants, local calendar dates, recurring wall-clock times, and elapsed durations; define time zones and interval boundaries where they change meaning. Choose representations from the required arithmetic and comparisons, not from a display format.

Keep the model no more elaborate than these distinctions require. Normalization, denormalization, event sourcing, and document embedding are choices with consequences, not universal quality gates.

## Put each rule where it can be enforced

For consequential invariants, state the rule precisely, its scope, and the layer responsible for enforcing it. Separate rules encoded in the proposed storage definition from rules enforced by an application write path or transaction. A rule checked or reconciled later has a window in which violations can exist; say whether that is acceptable. Do not imply that a type declaration, comment, front-end validation, or diagram enforces a rule at the database boundary.

Consider competing writes where they can break an invariant. “Check that no reservation exists, then insert” does not explain how two simultaneous writers preserve a capacity limit. Identify the required atomic boundary or coordination assumption and whether the selected storage supports it; leave feasibility explicitly unresolved if it has not been established. Do not promise a concurrency guarantee merely because the single-writer example is consistent.

Where values are stored in more than one place, identify the authoritative source, how derived copies are maintained, and whether readers may see them lag. A historical snapshot can intentionally preserve an old value; a current projection has a different obligation. Avoid silently keeping multiple independently editable versions of one fact.

Use the chosen engine and relevant version to decide what a declaration can express. Verify engine-specific claims against primary documentation or inspected behavior and cite the applicable source. If a required constraint cannot be represented directly, name the remaining enforcement obligation rather than presenting a broader schema as sufficient.

## Shape storage around the required work

Trace the important writes and reads through the proposed model. A read description should identify its population, filters, ordering, time interpretation, and expected result shape where relevant. A write should identify the records or documents affected and the invariants that must hold together. Resolve ambiguous phrases such as “latest” or “active” using the domain rules.

Use those operations to motivate keys, indexes, embedding boundaries, projections, or partitioning only as needed. State the workload assumptions behind consequential choices, such as an unbounded child collection, a frequently updated shared value, or reads spanning owners. A plausible access path is not measured performance; do not invent volume, latency, or throughput claims. If a requested read requires an expensive or awkward reconstruction, explain the tradeoff rather than silently changing its meaning.

Author complete in-scope definitions in the requested format. For a physical model, use the selected engine's schema or storage conventions, including the keys and constraints the design relies on. For a logical model, provide precise types, identifiers, relationships, and rules without claiming they are executable. Keep names and meanings consistent across definitions, diagrams, prose, and examples; do not let an illustrative diagram become a conflicting second specification.

## Walk the model with coherent data

Use a small connected set of representative records to show the writes and reads the user needs; use realistic fictional values when fresh examples are needed. Show the relevant starting data, the write, resulting state, and concrete read result. Include a boundary or rejected write when it demonstrates a consequential distinction, such as a second legitimate occurrence, an invalid ownership change, or a correction that must preserve history. Choose cases from the requirements rather than generating a fixed matrix.

Use target-native statements or definitions when requested; otherwise clearly label explanatory pseudocode. Keep IDs, units, times, links, and state changes consistent across the sequence. Distinguish expected results from outputs actually observed by execution.

Check that the examples can be represented without inventing an extra field, losing a required distinction, or relying on an unstated rule. Verify the reverse direction too: can the required read reconstruct its answer from stored facts alone? If two materially different domain situations collapse to the same stored state, either establish that the distinction is intentionally irrelevant or revise the model.

Use an available parser or schema checker when appropriate for the artifact. Execute examples only when that work is authorized and the target is suitable; a model-design request alone does not call for live database changes. Report which checks ran and what they establish. Syntax validity does not prove runtime enforcement, query performance, or migration safety.

## Deliver the model and its remaining decisions

Return or save the requested model and definitions, the meanings and enforcement obligations needed to implement them, and the representative write/read examples. Keep material design tradeoffs and unresolved decisions beside the parts they affect. Read back saved artifacts and check references and example consistency.

State whether this is a reviewable proposal or a model ready for implementation, based on the remaining domain and feasibility decisions. Designing a new representation does not establish that existing data can migrate into it, that deployed readers accept it, or that a live system enforces it. If implementation or migration is also requested, continue within that scope using the established model; do not invent a new approval gate simply because the design is complete.
