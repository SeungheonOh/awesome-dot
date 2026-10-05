---
name: build-source-formatter
description: Build or maintain a source formatter or language-specific printer when an established formatter and its configuration cannot meet the requested syntax, preservation or layout. Use for formatter implementation, rather than ordinary formatter use, a source migration or parser construction alone.
---

# Build a Source Formatter

Produce readable source while retaining the meaning and source relationships the project promises. Prefer the language's or project's established formatter, configuration and extension API. When an established formatter appears suitable, check its supported syntax, preservation and layout against the request before choosing printer or adapter work; a formatting command or configuration change can be the complete result. Keep the user's requested output primary.

## Establish what formatting may change

Read the accepted language/version, representative source, project style and relevant parser or formatter implementation. For maintenance, identify the requested change and an existing behavior that should remain. Settle the distinctions that affect this task:

- Accepted syntax and input mode, including supported extensions and the treatment of malformed or incomplete source
- Permitted changes to layout, spelling or punctuation, and required preservation of comments, directives, literals, ordering and grouping
- The useful output: formatted source, a reusable command/API, or integration into an existing editor or build path

Use a few representative before/after examples to make the style concrete. Choose spacing, indentation and break behavior for the actual constructs; add a width policy only when useful. If width matters, establish its units, whether it is a preference or limit, and how indivisible text is handled. Keep small settled decisions in existing tests or documentation rather than requiring another specification.

Reuse the accepted grammar and native APIs. Formatting eligibility need not require name resolution, a dataset or successful program execution. Preserve the project's distinction between syntactic validity and later definition/runtime errors; do not silently repair those errors while laying out source. Follow the actual refusal or recovery policy for unsupported forms, and never drop an unhandled construct as though formatting succeeded.

## Retain enough source to print faithfully

Choose a representation that carries both structure and the source detail required by the contract. A semantic tree may discard comments, parentheses or literal spelling. Retained original spans plus the existing parser can be sufficient for a small printer; a concrete syntax model or the formatter's own tree may be appropriate elsewhere. Do not replace a working grammar or introduce an AST, CST or document algebra merely to follow a standard architecture.

Keep spelling separate from value. Re-encoding a decoded string or number can change escapes, precision or required presentation even when one consumer returns the same value. Retain the relevant original source for literals, ignored regions, embedded text and other protected units, or normalize only what the accepted policy permits. Follow the project's encoding, line-ending and final-newline contract, including where physical newlines are part of a literal. Convert byte, code-point, code-unit or line/column positions against the retained source before slicing or editing it.

Give comments and directives meaningful ownership during reprinting. Determine whether they belong to a preceding or following construct, a particular token gap, or an enclosing region using the language and tooling rules. Retaining comment text and order alone does not establish that a suppression, documentation comment or directive still governs the same thing. Use an existing printer's attachment hooks where suitable; [printer comment interfaces](https://prettier.io/docs/plugins#handling-comments-in-a-printer) illustrate why original locations and attachment decisions can matter outside the semantic tree.

## Choose legal, readable layout

Map each supported construct to its spacing, indentation and legal break opportunities. Keep required lexical separation: joining two spellings must not create a different token. Preserve precedence and associativity when retaining or changing parentheses. Newlines, indentation and comment placement can affect syntax or execution, so establish those rules from this language rather than treating all whitespace as disposable. For example, [Python's line structure rules](https://docs.python.org/3/reference/lexical_analysis.html#line-structure) distinguish logical lines, continuation and indentation.

Choose related breaks together when their readability depends on one another, such as a list with nested elements or an expression with continuations. A straightforward token-span printer can suffice when the grammar makes its choices legal. A document model with groups and alternative layouts is useful when those relationships become complex; it is not mandatory. Use the selected printer API's own representation and invariants when extending an existing formatter.

Account for comments when choosing breaks. A line comment needs a terminator before subsequent code; moving it to fit a width preference must retain its required attachment and effect. Do not split indivisible literals or alter embedded content to force a line to fit. Emit a complete result for every supported form, with an explicit error or authorized preserved region for unsupported input.

Keep choices stable for the same source, configuration and relevant tool versions. Avoid deriving layout from incidental traversal order or mutable state left by a previous call. A newer formatter can intentionally change its output; [native formatting documentation](https://pkg.go.dev/go/format#pkg-overview) gives an example of why version identity matters for repeatable results.

## Honor the requested integration boundary

Whole-document formatting can be a complete task. If range or fragment formatting is requested, establish permitted boundary expansion, surrounding indentation/context and source that must remain unchanged. A fragment is not automatically equivalent to extracting text and formatting it as a whole file. If incomplete editor input is supported, preserve its intended recovery behavior without inventing missing syntax.

For editor integration, calculate edits against the authoritative document snapshot in the client's position units, then inspect the actual applied result. Reuse the existing editor-service machinery for synchronization and stale results. For files or commands, retain the project's write and failure contract; a partial printer result or an older output must not appear to be a newly successful formatting result. These are integration obligations, not a reason to add an editor, cache or new save framework.

## Check the actual formatted result

Exercise the saved formatter through the requested API, command or client. Use expectations grounded in the accepted language and style, independently of the printer's own helpers. Select a few ordinary cases that distinguish the changed behavior, including relevant nesting, source detail or failure boundaries. Check separate promises with evidence suited to each:

- **Syntax and meaning:** Parse the actual output with the appropriate language tooling. Compare structure or tokens only under an equivalence that retains all relevant distinctions. Check the intended consumer where it supplies useful, authorized evidence; one matching runtime result does not establish equivalence for every input
- **Source relationships:** Inspect required literal spellings, comment/directive attachment and protected regions in the saved result. A comment count or equality of trees that omit trivia cannot establish these relationships
- **Readable layout:** Compare actual changed output with the accepted style and representative expectations. Unchanged input can parse and be stable while failing the requested layout improvement
- **Repeat formatting:** Format the produced source again under the same configuration and tool versions, then compare the actual results. Repeating calls on the original input establishes a different property from idempotence

Use only checks justified by the task. For a reusable formatter, a separate ordinary source helps expose input-specific special cases. For a refusal, inspect the reported failure and remaining source/output state. For partial formatting, read the surrounding untouched source as well as the changed region. Keep useful failures, correct the supported cause and rerun affected checks without weakening the accepted meaning or style.

Deliver the requested formatted files, configuration or formatter change with its invocation/integration and concise evidence from the final result. State supported language/input modes and any unverified boundary. Use ordinary implementation and testing guidance for project work; keep source migration, parser construction and editor-service development with their existing owners when those are the actual task.
