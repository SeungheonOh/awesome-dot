---
name: develop-language-processor
description: Build or maintain a small DSL, expression engine, interpreter or source-to-target generator while carrying accepted meaning and original locations through definition checks and the actual consumer. Use for processor behavior across these boundaries, rather than parser composition alone, a source-analysis rule, a codemod or an editor service.
---

# Develop a Language Processor

Carry the accepted source meaning through the processor to a result its intended consumer can use. A successful parse, a valid definition, a successful evaluation and an eligible output establish different things. Preserve those distinctions without requiring separate passes or a particular compiler architecture.

## Start from the intended use

Read the language contract, representative source, relevant implementation and actual caller or output consumer. For maintenance, identify the behavior being changed and retain an unchanged consumer case when compatibility matters. For a new processor, settle the smallest useful source-to-result path before adding syntax.

Prefer an existing format, expression facility, query language or library when it already meets the request. A data transformation may need ordinary SQL; a settings file may need a schema and a decoder. Building a new language is justified by the user's requirements, not by the availability of a parser framework.

Make consequential meanings explicit: names and scope, operator precedence, value domains, missing values, defaults, ordering and failure behavior where they affect the requested result. Distinguish accepted rules from implementation choices. Resolve a material ambiguity with a concrete input on which the possible meanings disagree; keep a small settled task's contract in its existing tests or documentation rather than demanding a separate specification.

Choose a representation sufficient to carry the needed facts. Parsed records, tokens with values, a syntax tree or a resolved model can all be appropriate. Share authoritative resolution and semantic decisions between checking, evaluation and generation; independent implementations of name lookup or coercion can silently disagree. Introduce an AST, IR or type system only when it earns its place.

## Keep meaning attached to the original source

Retain the accepted source and the locations needed to explain its constructs. Follow the actual input contract for decoding, character repertoire and normalization. Do not narrow accepted text merely because a location helper or output serializer uses a different encoding.

Keep source spelling and semantic value distinct. An escaped string, normalized identifier or expanded abbreviation can have a value unlike its original text. Carry its origin through those changes. Convert byte, code-point, code-unit or line/column positions against the original accepted text, including relevant newline and encoding-marker behavior. A position in pretty-printed or generated text is not an original-source location.

When a later error arises from a resolved reference or derived operation, retain enough origin information to identify the responsible source construct and a related definition when useful. Mark synthetic or source-wide diagnostics honestly instead of inventing a precise span. Verify a reported range by reading the intended text from the retained source using the declared units.

## Separate definition checks from input-dependent work

Parsing establishes that the source has an accepted form. Check the definition's further obligations where the language requires them: for example, reference resolution, duplicate declarations, argument shape, dependency cycles or incompatible operands. Use the specified scope and override rules; neither repeated spelling nor declaration order has a universal meaning.

Perform checks that are independent of records or runtime inputs even when there is nothing to evaluate. An empty dataset must not make an invalid definition appear valid. Conversely, do not reject a permitted runtime-dependent expression because its value is unavailable during definition checking. Classify only what the language allows the processor to know at that point.

Then evaluate against the actual input or lower to the chosen target using those established decisions. Keep definition errors, runtime failures and legitimate empty or false results distinguishable to callers. If the processor supports partial results, define which work remains usable and which result or effect may accompany an error. A caught exception converted to null is a semantic change unless the language specifies it.

Existing frameworks may already own these dependencies. For example, [Langium's document lifecycle](https://langium.org/docs/reference/document-lifecycle/) separates parsing, scope computation, linking and validation. Use the selected framework's actual lifecycle when relevant; this is not a requirement to adopt its stages or data structures.

## Preserve the computation and the consumer contract

For interpretation, preserve the language's evaluation count and order, conditional or short-circuit behavior, error timing and consequential effects. For transformations or generation, preserve those same properties in the target. Repeating an expression in generated text can evaluate it twice; collecting an iterator early can move work and failure before a filter or limit. Introduce saved intermediates or materialization only where the accepted semantics require them.

Keep source validity separate from target representability. A valid value may exceed the chosen output's number range, name rules, encoding or structural limits. Apply the selected consumer's explicit conversion, escaping or rejection policy at that boundary. Do not silently round values, replace characters, collapse duplicate fields or reinterpret missing values to make serialization succeed. Do not impose one target's restrictions on unrelated consumers.

For a generator, construct target syntax with a suitable printer, escaping or parameterization mechanism. Treat source text as language data; do not use host-language evaluation as a shortcut for its semantics. Emitting code is distinct from executing it. If execution is part of the requested verification, use the intended target runtime and authorized inputs and effects.

Make output eligibility reach the real caller. A preview, saved result or downstream action must use the result and status produced for the relevant source, input and consumer. An error must not leave an older successful output presented as the new result. Define when output or effects become visible and what may remain after failure; staging one file does not make a collection of writes transactional.

Apply resource policies in proportion to the language and exposure. When source size, nesting, expansion, evaluation or generated output can grow materially, bound the relevant work and report exhaustion distinctly from a valid empty or truncated result. Apply a whole-request budget across contributing constructs rather than resetting it for every expression. A returned-row limit alone does not bound earlier computation, and a check after allocation cannot protect that allocation.

## Verify through the useful boundary

Exercise the saved processor through the intended caller or target consumer. Derive expected outcomes from the accepted meanings, not from the processor's own resolution or conversion helper. Select a few cases that distinguish the changed behavior, such as:

- Valid syntax whose definition is invalid, including an empty-input case when relevant
- A valid definition whose runtime result or failure depends on the supplied input
- An order, short-circuit or materialization boundary that would expose an altered computation
- A later-stage diagnostic that selects the correct original text after a relevant escape, Unicode or newline boundary
- A semantically valid result that the selected consumer must convert or reject explicitly

Use only the cases the task needs. Parsing generated output checks target syntax; consuming or executing it establishes different behavior. Inspect the actual saved or applied result, including error status and eligibility. For a reusable processor, a separate small input helps reveal source-specific special cases. Preserve a useful failure, fix the supported cause and rerun affected checks without changing the expected meaning just to pass.

Return the usable processor change, invocation or integration, and concise evidence of what the real consumer accepted. Identify unsupported semantics and unexercised boundaries. Keep editor/LSP features, source migrations, report-only static rules, formatting, optimization and incremental reuse as separate work when requested. If caching is introduced, invalidate on the actual semantic dependencies; do not add it to complete an otherwise small processor.
