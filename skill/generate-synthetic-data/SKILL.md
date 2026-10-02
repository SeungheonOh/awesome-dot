---
name: generate-synthetic-data
description: Create a usable fictional dataset or reusable data generator for a stated downstream use, with coherent relationships, requested distributions and cases, and verified saved output. Use when synthetic data is the main deliverable, rather than incidental test fixtures, analysis or cleanup of real records, or deciding a data model.
---

# Generate Synthetic Data

Deliver the requested data in a form its intended consumer can use. Make its invented status clear, preserve the meanings and rules the task depends on, and check the actual saved artifact. Plausible-looking rows alone do not establish a useful dataset.

## Establish the data contract

Start from the downstream use: a demonstration, teaching exercise, import rehearsal, benchmark input, or another stated purpose. Inspect the supplied schema, accepted example, and relevant consumer requirements before inventing fields. Preserve the requested format, field names, table structure, scale, and practical limits. Do not redesign an established model merely to simplify generation.

Settle the details that affect this use:

- What one row or object represents, identifier scope, relationships, and expected counts for each entity or record type
- Field types and meanings, units, precision, time interpretation, allowed categories, and missing-value conventions
- Rules that make ordinary records valid, including uniqueness, cardinality, temporal order, conditional fields, and derived values
- Requested patterns, proportions, correlations, rare cases, and whether they are exact requirements or sampling targets
- Whether delivery is a one-time dataset or a reusable generator, and whether reproduction of the same result matters

Use reasonable, disclosed assumptions for ordinary unspecified details. Ask when a missing choice changes the dataset's meaning or makes it unusable, such as whether a repeated ID denotes a second event or an invalid duplicate. Detect conflicting constraints early: a requested unique population may exceed the available value space, or required category counts may exceed the total. Do not silently relax a requirement to make generation succeed.

## Make invented records explicit

Generate original fictional records. Use authorized reference material to understand structure or supplied summary targets; distinguish those sources from assumptions introduced for the simulation. Do not copy sensitive real rows into an output described as fictional, or treat changing names as sufficient anonymization.

Mark the delivered dataset as synthetic in a filename, accompanying description, or format-supported metadata. Keep that notice visible without adding an unrequested column or comment that breaks the consumer's schema. Choose fictional identifiers and clearly designated placeholders for contact fields; do not accidentally present invented details as a real person's contact information. Generated free text must not masquerade as collected interviews, actual customer feedback, or observed events.

Explain material simplifications and any use of real-data summaries. Synthetic status alone does not establish anonymity, statistical representativeness, or a privacy guarantee. If the request depends on such a guarantee, identify the evidence or additional work needed instead of claiming it from the generation method's name.

## Build coherent records and deliberate variation

Generate related entities and events together. Establish parent identities before references, preserve relationship cardinalities, and let meaningful state or time sequences constrain later values. Sampling every column independently can produce individually plausible values that contradict one another. Derive dependent values from their defining quantities and rules; do not independently randomize a total and its components.

Choose variation for the requested use. A demonstration may need readable, diverse examples; an analytical exercise may need a specified association; a performance input may depend on skew, record size, or repeated keys. Label designed patterns as designed. Do not invent empirical frequencies or causal evidence to justify them.

Distinguish hard coverage from chance. Allocate exact category counts or required edge cases directly when the contract demands them. For sampled targets, establish a suitable tolerance or report the realized distribution; a seed does not make a small sample match its population probabilities. Respect conditional distributions and missingness rules when relevant. Check that enforcing a range, uniqueness, or another constraint has not materially changed a requested pattern.

Keep ordinary valid data separate from deliberate invalid cases. Add invalid cases only when requested or clearly part of the stated deliverable. Use distinct files, a companion case index, or an agreed field to label them without breaking the target format. For each intentional violation, state the violated rule and independently defined expected property, such as rejection by a specified validation rule. Avoid unrelated defects that make it unclear what the case demonstrates. Do not call a valid extreme value invalid merely because it is unusual.

## Make repetition useful when requested

For a one-time dataset, deliver the dataset; do not require a generator or programming framework. When a reusable generator is requested, deliver runnable source plus representative sample output in the requested format. Expose the inputs that actually need to vary, such as size, output location, selected scenario, or seed. Validate incompatible settings and keep defaults within practical resource limits.

Where reproducibility matters, control relevant randomness, time inputs, ordering, and identifier generation. Record the seed, configuration, and dependency versions needed to reproduce the output. Do not promise identical output across unspecified environments or changing generator versions. A fixed seed cannot compensate for an implicit current date or an uncontrolled random source.

Use the requested language and available environment; avoid unnecessary dependencies. Make the documented invocation work from the delivered files without relying on hidden working state. Check a representative run and, when exact repeatability is promised, rerun it and compare the relevant output. Keep generated files within the authorized destination and avoid replacing unrelated files.

## Validate the saved result

Write the artifact, then reopen it with an appropriate parser or reader. Check the serialized result rather than only the in-memory objects or the generator's success message. Focus verification on properties that determine whether the downstream use works:

- Schema, actual record counts, parseability, and consequential representations such as identifier text, precision, nulls, dates, and quoted text
- Key uniqueness, valid references, required relationships, and cross-field or temporal invariants
- Realized distributions and required cases, including the separation and labels of intentionally invalid records
- Independently recomputed derived values or control totals where they establish a meaningful rule

Derive expected properties from the contract, not by calling the same generation helper on both sides of a check. For intentional invalid cases, confirm the advertised violation and the other rules meant to remain valid. Inspect representative saved records for semantic contradictions that type checks would miss. Use an authorized local consumer or disposable import target when requested and available; otherwise state what format-level validation establishes.

For large outputs, use full streaming checks for feasible structural invariants and disclose which expensive or qualitative checks were sampled. Do not claim a whole-file check from a preview. If saving or validation fails, fix the affected generation or serialization and check the resulting artifact again. Report unavailable checks instead of implying they ran.

## Deliver the usable artifact

Provide the actual dataset and, when requested, its generator and invocation. Include concise field meanings, assumptions, synthetic status, designed patterns or invalid-case labels, and the validation results needed to use it correctly. Keep documentation proportional to the task and preserve the requested delivery format.

State what was actually generated and checked, including material limits. A generated scenario can support a demonstration or exercise under its stated assumptions; it does not prove production behavior, predictive accuracy on real populations, or acceptance by an untested live importer. Creating an import file does not authorize loading it into a live service or publishing it.
