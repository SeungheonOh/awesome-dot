---
name: build-source-analysis-rule
description: Build or revise a report-only source rule for a declared API-usage, style or structural policy. Separate syntax candidates from semantic applicability, retain unknown and excluded coverage, join source evidence where needed, and verify the saved checker and its diagnostic locations. Use for reusable passive source analysis rather than a one-off code review or runtime test.
---

# Build a Source Analysis Rule

Turn an accepted source policy into a usable, rerunnable check with defensible findings. The result should explain which source was assessed, why a rule applies at a particular location, and what remains unknown. A parser that finds matching text is not necessarily a checker for the intended symbol or behavior.

Use the existing compiler, type system, linter or project check when it already owns the policy. Configuring and exercising that owner may complete the task without a new analyzer. General implementation and tests belong with `implement-scoped-change` and `write-behavior-tests`; a human review belongs with `review-code-change`. Keep ordinary HTML structural inspection with `review-html-without-execution`. Do not turn this workflow into a mandatory framework for every small guard.

## Define the rule and its evidence boundary

Read the request, relevant interface or project policy, representative source and existing enforcement. Establish the policy's authority and its intended exceptions. A convention requested by the project is not automatically a language error. If validity depends on contextual judgment that the available evidence cannot settle, keep that judgment visible instead of encoding a brittle ban.

Specify enough of the contract to distinguish a true finding from a nearby legitimate case:

- The source language/version, selected files or entry points, and generated or excluded material
- What source construct or relationship the policy governs
- The facts required to establish applicability and a violation
- What counts as an assessed nonviolation, unresolved case or unsupported form
- The requested report or command interface and any gate that will consume it

A small rule may need only a few sentences and examples. Do not impose an exhaustive language specification, benchmark corpus or separate planning artifact. Settle only material ambiguities; make ordinary implementation choices within the accepted scope.

Choose the necessary analysis strength. A syntactic rule may need tokens or a syntax tree. An imported-API rule may need binding or type facts. A path-sensitive obligation may need control-flow evidence. Prefer the relevant native compiler/linter facilities rather than inferring those facts from spelling. If the available tool cannot establish a required fact, narrow the supported model honestly or report the specific limitation.

## Keep source passive and preserve its identity

Inspect the selected tool and configuration before running it. Parsing source and loading project code are different operations: a tool may execute plugins, configuration files or imports even when its final output is a report. Use a permitted passive path for a passive task. Do not evaluate expressions or run inspected programs merely to make static facts easier to obtain.

Retain the original bytes and the encoding needed to interpret them. Record source identity sufficient to associate a result with the inspected version. For several files, keep their individual identities and any required revision/snapshot relationship. A path alone is not enough when the file can change after analysis.

Honor the authorized source boundary. References or import statements inside source do not independently authorize reading other directories, loading dependencies or contacting services. Decide whether an unresolved dependency remains unknown or whether an already authorized compiler model can resolve it. Do not silently expand a small source check into a repository or dependency crawl.

Handle unreadable files, unsupported encodings, parse failures and limits explicitly. Preserve independent usable results where the task permits partial assessment. An unparsed file is not an empty file with no findings. Keep limit claims precise: a node-count check after parsing does not establish a bound on the parser's earlier allocation, and a cap on reported diagnostics is not a cap on all analysis work.

## Discover candidates, then establish applicability

Keep candidate discovery separate from semantic judgment. Searching for a call spelling or collecting an AST shape can deliberately over-include lookalikes. It should not directly produce a policy finding unless that shape alone establishes the rule's meaning. Comments, string contents, escaped literals and generated nodes must be interpreted according to the selected language and parser, not by an accidental text pattern.

For a symbol-dependent rule, define the supported resolution model: imports and aliases, scope, shadowing, rebinding, receiver identity and any type facts. A same-spelled parameter or unrelated method does not establish an imported API. A declaration later in a scope can also matter; for example, Python's [name-binding rules](https://docs.python.org/3.12/reference/executionmodel.html#binding-of-names) make a function-local binding relevant throughout that function. Use the actual language's rules rather than generalizing one language's lookup order.

Be explicit about facts the model does not infer, such as conditional bindings, indirect callable aliases, reflective updates or runtime module replacement. A conservative model can be useful if its supported cases work and its uncertainty remains visible. Do not label a value definitely unrelated merely because the model failed to resolve it. If a classification means only “outside this direct-binding rule,” say so.

Apply the policy only after establishing the required facts. Distinguish a missing argument from an argument possibly supplied by an unresolved expansion, and a known literal value from an arbitrary expression. Evaluate only the facts the policy needs. A rule about the presence of an explicit option does not necessarily decide whether the option's runtime value is valid or whether the call succeeds.

Keep broad findings separate from unsupported sites and file-level failures. Choose terms appropriate to the task, but preserve their meanings in both the report and any command exit contract. A zero finding count must not silently erase unknown candidates, exclusions or missing input coverage.

## Join declarations and uses when the rule requires it

Some rules compare uses with definitions across files rather than inspecting a call in isolation. Establish which source owns each namespace or declaration set and how that authority is known. Resolve references using the language or supplied contract, preserving scope, exact identity and meaningful occurrences.

Determine whether the available declaration set is complete. A known member of an open set can support a positive membership result, while the absence of an unlisted member may remain undecidable. A failed catalogue parse or unresolved expansion must not become an empty authoritative set. Preserve the known facts that remain useful without claiming the missing facts.

Specify duplicate, override and ambiguous-definition behavior from the real format and policy. Repeated dictionary keys, two competing namespace owners and repeated uses are different situations. Do not apply one universal deduplication rule to all three. Follow defined ordering or replacement semantics when supported; otherwise retain the conflict or uncertainty.

Attach both use-site and declaration evidence to a relationship finding. For a negative claim, explain what makes the searched definition scope complete; there is no source span for a declaration that is absent. Reanalyzing changed declaration inputs should update the affected usage result under the same rule. If caching is requested, include those dependencies in its identity; do not introduce caching merely to complete a small check.

## Produce trustworthy diagnostics

Give each retained finding its rule identity, affected source/version, original location, reason and the evidence that supports applicability. Include a useful excerpt when appropriate. Keep a location in the use separate from a location in its import, declaration or related file. For unknown outcomes, identify the missing fact or unsupported construct instead of presenting an unexplained confidence score.

Respect the parser's position units. Bytes, Unicode code points, UTF-16 code units and displayed columns are not interchangeable. Python AST locations, for example, use [UTF-8 byte columns and explicit end positions](https://docs.python.org/3.12/library/ast.html#ast.AST). Map them to the original source representation before extracting text or presenting a different coordinate system. Account for encoding markers and line endings where they affect that mapping. Do not substitute pretty-printed source for evidence of an original span, and do not invent positions for nodes that lack them.

Keep output usable and proportional. A structured report is useful for a saved command or downstream gate; a requested short answer can show the relevant findings and limits directly. Distinguish findings discovered from those retained or displayed when clipping occurs. Preserve separate source occurrences when they need separate action, while avoiding accidental duplicate reports from repeated traversal.

If the checker has an exit status, define what each outcome means to its caller. Policy findings, incomplete assessment, a command error and an unexpected checker failure are different facts even if some share a nonzero status. Keep detailed outcomes available; a success-looking wrapper must not hide a failed underlying check. State the boundary of “no findings” in terms of the supported source model, not arbitrary runtime behavior or whole-project correctness.

## Exercise the saved checker

Test through the real report/command entry point on the actual final code. Derive expectations from the accepted policy and source semantics, not from the production matcher's own helper. Select checks that distinguish the rule from a plausible wrong implementation:

- A real violation, an accepted use and a close syntactic or naming lookalike
- The relevant alias, scope, rebinding or type boundary for this rule
- An unresolved value or incomplete definition set that must remain unknown
- A parse/input failure alongside independent assessable source, when partial results are supported
- Original-source location readback with relevant Unicode, multiline or newline cases

For a cross-file rule, change a declaration in a separate copy and check the consequence at the actual use. For a reusable command, exercise a small new input/path and repeat an unchanged case to expose fixture-specific answers or unstable output. Do not require every listed language feature for every rule; exclude unsupported constructs honestly and test the boundary promised to the caller.

Inspect the saved report against the original bytes, including its examples and any source excerpt. A successful parser invocation alone does not establish correct applicability or locations. Preserve a useful failed case, correct the relevant implementation and rerun affected checks. A few passing examples support those observed cases, not a measured false-positive rate or completeness claim for unseen projects.

Deliver the usable rule/configuration or checker, requested result, invocation and concise support limits. Keep automatic source fixes separate unless requested and independently justified; detecting a questionable construct does not prove that a particular rewrite preserves its behavior.
