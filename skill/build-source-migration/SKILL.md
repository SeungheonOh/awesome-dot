---
name: build-source-migration
description: Build or revise a reusable source transformer for an accepted API or syntax migration. Establish rewrite eligibility, preserve evaluation and binding behavior, retain meaningful source formatting, preview exact changes, and verify real changed consumers and unresolved sites. Use for a rerunnable codemod rather than a report-only rule or a small manual edit.
---

# Build a Source Migration

Turn an accepted code change into a usable transformation that can be previewed, applied within its authorized scope, and run again. Finding the intended symbol establishes where a migration may apply; it does not establish that a particular rewrite preserves the caller's behavior. The useful result is changed source with a defensible account of what migrated and what still needs attention.

Prefer an existing project, compiler, language-service or maintained codemod facility when it already implements the needed transformation. Configure and exercise it before inventing another tool. Keep a small direct refactor with `refactor-code`, ordinary implementation with `implement-scoped-change`, and report-only source checks with `build-source-analysis-rule`. `verify-exact-text-patches` owns exact patch application; a matching patch is not a semantic justification for the code it inserts. Dependency/version decisions belong with the applicable upgrade and API-contract guidance.

## Establish the accepted change

Read the actual old and new contracts, relevant implementations or authoritative migration notes, controlled callers and project instructions. Identify the requested outcome: a preview, a reusable command, changed files, or a migration integrated into an existing tool. Do not require a custom framework for a few routine edits.

Settle the consequential mapping before changing source:

- Which API, declaration or syntax form is changing, including relevant language and library versions
- Which observable behavior must survive and which differences are explicitly accepted
- The runtime domain in which the mapping is valid, including defaults, missing values, errors and side effects
- The authorized source set, generated or protected material, and the intended write mode
- Required supported cases, cases that may remain unresolved, and what would count as completion

A new parameter with a similar name may have different units, bounds or default behavior. An omitted option, an explicit null, false and zero can mean different things. If an old omitted default differs from the new one, migrating an old call may require making its old meaning explicit while leaving already-new calls alone. Resolve a material contract ambiguity rather than choosing a convenient conversion.

Inspect existing work and preserve the original inputs. Use the authorized copy or checkout and identify exactly which source version the transformation reads. A request to write a reusable migrator does not authorize running it over unrelated repositories or changing external consumers.

## Separate target recognition from rewrite eligibility

Use the language's parser and relevant binding or type information to identify the intended sites. Reuse the compiler's or linter's established model where available. Imports, aliases, shadowing, receiver identity and scope can distinguish a real API use from a same-spelled unrelated function. A text match is sufficient only when the accepted source model makes that inference valid.

Then decide whether the proposed replacement is justified at each identified site. A known old call can still be unsuitable for automatic rewriting because of an unresolved value, unsupported argument form, context-dependent behavior or insufficient type information. Report that distinction. Do not treat failure to recognize a site as proof that the source is already migrated.

Keep the supported model explicit and proportionate. A transformer may deliberately support ordinary calls while leaving reflective access or dynamic bindings for review. Required supported inputs must still make useful progress; declaring every difficult case unsupported is not a completed implementation of an agreed transformation. Parsing source should remain passive unless executing the relevant consumer is separately part of the authorized verification.

## Preserve the computation, not just its result on one input

Work through the expression and control-flow consequences of the mapping before choosing replacement text. Check whether it changes:

- How many times an expression, receiver or argument is evaluated, and in what order
- Whether evaluation is conditional, short-circuited, deferred or repeated by a surrounding loop
- When an exception occurs and which earlier effects remain visible
- Which names a reference resolves to, including any new imports or temporary bindings
- Types, overload selection, mutation, ownership or validation behavior that the contract relies on

For example, replacing a start-and-length call with an exclusive-end call may need the start value twice. Copying a source expression into both positions can execute it twice. Rearranging keyword arguments into signature order can also change their observable evaluation. Python documents its [expression evaluation order and call behavior](https://docs.python.org/3.12/reference/expressions.html#evaluation-order); other languages need their own rules.

Choose a realization that preserves the required computation. A direct substitution may suffice for a literal or an independently established pure expression. Another site may need saved intermediate values, a suitable existing helper, or a different transformation boundary. Do not introduce temporaries or wrappers universally. Moving work out of a conditional, generator, asynchronous boundary or exception region can change when it happens even if the final expression looks equivalent.

If introducing names, determine their actual scope and avoid capture, shadowing and collisions with existing references or language-managed names. Merely adding a long prefix does not prove freshness. Check the affected scope and the assumptions under which generated names remain safe. A helper that silently calls the deprecated implementation does not complete a migration whose contract requires the new API.

Keep intentional compatibility limits visible. A mapping established for exact built-in values does not automatically cover subclasses, overloaded operators or arbitrary invalid arguments. Conversely, do not label a valid caller unsupported merely because a fixture did not contain it; use the declared transformation conditions.

## Realize the change in the source representation

Choose a representation that can preserve what the user asked to keep. A conventional AST is useful for semantic structure but may omit comments, whitespace and literal spelling. A suitable concrete-syntax tool can retain that information; [LibCST describes this distinction](https://libcst.readthedocs.io/en/latest/why_libcst.html). A bounded AST-guided edit over retained original spans can also work. Use the existing suitable facility rather than assuming one parser or printer fits every language.

Define the edit boundary deliberately: an expression, statement, import list or other complete construct. Preserve source outside it, and decide where comments and separators inside it belong. Moving or deleting a node must not silently detach a meaningful comment or leave invalid syntax. Keep required encoding, line endings, literal spelling and final-newline state. A normalized review diff can be useful, but it is not the actual byte-preserved file.

Map parser coordinates to the original representation before using them as edit offsets. Check byte versus character units and retained encoding markers. Plan edits against one immutable source version, detect overlap, and define ordering when several insertions share a boundary. A later edit must not accidentally use offsets from an earlier modified buffer.

Handle imports, declarations and generated support code as part of the transformation. Respect language-required placement, existing aliases and initialization effects. Keep an old import when unresolved callers still need it. Remove a declaration only when the accepted consumer scope supports that conclusion; absence from a simple search is not proof about dynamic or external callers.

## Preview and apply with an honest write contract

Show the proposed changes and unresolved sites before a consequential batch write when the task calls for review. Preview must not change target source. If apply is already authorized, complete it after the relevant checks rather than adding an unnecessary confirmation step.

Validate selected paths and the full edit plan before writing. A path found in source text does not expand the authorized target set. Recheck the source identity on which the plan depends; if it changed, recompute or report the conflict instead of overwriting intervening work.

Keep write guarantees precise. Planning a batch before writing does not make several file replacements a transaction. State whether a failure can leave a partly applied set and how the actual tool reports that state. Preserve recoverable originals or use the project's existing recovery mechanism when appropriate. Do not claim safe concurrent editing or crash recovery from a simple pre-write digest check.

## Exercise the actual migration and changed callers

Use expectations derived from the accepted contracts, not only the transformer's own matcher. Check meaningful cases through the saved command or native migration entry point:

- A supported migration and a close unrelated or shadowed form that must stay unchanged
- Relevant default, evaluation-order, repeated-expression or exception behavior that could distinguish a plausible wrong rewrite
- An unresolved old site that remains visible after other sites migrate
- The requested source-preservation boundary, including actual saved byte regions or native syntax/trivia relationships
- A changed input or separate caller that rules out fixture-specific edits, when reuse is requested

Parse or compile the changed source as appropriate, then exercise its real consumer. Give old and new versions equivalent fresh state when comparing them. Observe the contract's side effects and failures as well as return values. A syntactically valid program or a count of replacements does not establish compatibility.

Run the migration again on its actual changed output. No further edits can establish the relevant idempotence property, while unresolved old sites may still make the overall migration incomplete. Preserve that distinction in the report and command status. Check that migrated sites use the intended replacement, rather than a compatibility path that conceals continued old behavior.

If verification exposes a defect, retain a useful failed case, fix the relevant transformation and repeat the affected checks. A finite set of successful cases supports those observations; it is not a proof of equivalence for arbitrary programs. Do not run unrelated test suites or build a benchmark framework merely to enlarge the evidence count.

## Deliver the usable migration

Return the requested transformer or configuration, invocation, preview or changed files, and a concise account of migrated, already-current, unresolved and failed work as relevant. Explain any supported-language or runtime-domain limits and any partial-write state. Keep a small task's handoff small; a separate ledger or large source inventory is not automatically required.

Distinguish a verified local migration from retiring an API across all consumers, upgrading a dependency, publishing a package or deploying an application. Follow the established ownership and rollout contract for those later actions.
