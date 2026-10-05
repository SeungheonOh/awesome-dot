---
name: develop-command-line-tools
description: Build or maintain a command-line tool around real callers, consistent input and output semantics, dependable file effects, and checked delivery. Use for CLI development, including changes to scripts used by other programs; not merely running an existing command.
---

# Develop command-line tools

Make one useful command work for its actual caller, then carry the same promises through changes and delivery. The working unit is a command contract: what the invocation means and what the caller can conclude from its output, status, and effects. Existing README prose, examples, and tests can hold that contract. A new specification format or receipt system is unnecessary.

## Start with the caller

Read the requested outcome, relevant project instructions, command implementation, and one real caller or representative intended invocation. Establish what that caller needs to decide or save. If choosing a mechanism is still part of the task, consider whether an existing command or small composition already does the job. When building a tool is the agreed work, start with one command and one useful path through it.

For an existing tool, observe the affected behavior before editing. Distinguish accepted promises, caller dependencies, and incidental implementation details. A bug is not a promise just because the current command exhibits it. Resolve a consequential conflict between documentation and callers with a concrete differing outcome.

Keep only the contract details that change a decision:

| Part | Record in the project's existing form |
| --- | --- |
| Caller and invocation | Actual task, public command/runtime, supported operands and options |
| Effective inputs | Sources, precedence, absent versus explicit values, path origins, consequential input rules |
| Result and completion | stdout format, stderr role, exit meanings, whether output may precede failure |
| Effects | Permitted changes, publication point, prior state after failure |
| Compatibility | Existing calls and consumed behavior to preserve, or controlled callers to migrate |
| Delivery | Requested source/package form and the same caller case to exercise there |

Use this note to choose the implementation, assertions, and usage example. Update the affected clause when a decision changes; do not fill it in afterward as a disconnected checklist. Ordinary success and the nearest consequential failure often provide enough examples to settle a small command.

## Resolve the invocation before doing the work

Use the project's parser or a suitable native framework. Keep grammar, help, and option handling there; pass validated domain values into a small core and translate results and errors at the process boundary. One file can have these responsibilities without requiring a class hierarchy or multiple packages.

Settle supported defaults, repeated options, missing values, and relative-path bases before opening output resources. Preserve explicit false, zero, or empty values when valid: truthiness is not presence. If configuration exists, distinguish an absent CLI option from a parser-supplied default so it cannot accidentally hide a configured value. A deliberately selected malformed configuration should produce a useful error, not silently behave as though no configuration was selected.

Resolve a path using the origin defined for that source. A command-line path can be relative to the caller's working directory while a value from a config file can be relative to that file. Preserve the established rule and test from another directory when it matters. Do not make paths depend on a source checkout or installation location by accident.

Load only configuration needed by the supported invocation, after handling syntax and informational requests. Help and version should not require opening task inputs or outputs. See [effective inputs](references/effective-inputs.md) when multiple sources, presence rules, or path origins need design work. Do not add configuration discovery, environment variables, or interactive prompts merely to use this reference.

## Choose what completion means

Treat `(stdout, stderr, exit status, saved effects)` as one result. Reserve machine-output stdout for its declared data format; send diagnostics elsewhere. Define framing, encoding, relevant ordering and identity, and the meaning of a valid empty result. Keep human formatting separate only when the callers need separate modes. Add colors, progress displays, or terminal detection only for an actual terminal workflow, without changing machine data.

A negative reported business state can be a successfully produced result. A reporting command may exit successfully after describing problems; a predicate command may use a distinct nonzero status for its negative answer. Preserve or choose those meanings explicitly. Invalid invocation, inability to complete the work, and a valid negative result should not collapse into a misleading success or an undocumented failure. Avoid making callers scrape incidental diagnostic wording.

Choose the destination promise before writing:

- **Incremental stdout:** a consumer may receive a valid prefix before later failure. The consumer needs the producer's final status before treating the whole job as complete
- **Complete document on stdout:** finish required computation and serialization before emission when practical within the supported bounds. A later write or flush can still fail after some bytes escape; stdout cannot be rolled back
- **Explicit saved output:** when the promise is replacement of a complete result, stage privately and replace the destination only after required work succeeds. Preserve the prior file on a pre-publication failure
- **Caller shell redirection:** the shell owns opening and possible truncation. Application buffering does not protect a prior file targeted by `>`. Give callers a supported explicit-output route or a caller-owned staging procedure when preservation matters

Read [output, processes, and file effects](references/output-and-effects.md) for a streaming or saved-output command. It covers pipeline status, publication, and conditional early-close or interruption behavior. Keep an established stream incremental when repairing a separate file mode; silently buffering both can break its callers.

## Build and check the actual use

Implement a narrow path from effective inputs through the core to the promised result. Expand only for demonstrated needs. Subcommands, concurrency, completion scripts, logging infrastructure, and packaging are optional choices, not a starter kit every CLI must adopt.

Use the existing test approach for domain calculations and the public process boundary for command behavior. Derive expected values independently of the implementation. Inspect parsed results or promised bytes, status, and resulting files; a passing help command cannot establish any of those outcomes.

Exercise the real consumer when one is supplied. Pass arguments as separate values in a subprocess API, or quote them for the actual shell. Keep stdout and stderr separate. For a pipeline, retain meaningful producer and downstream results; a downstream parser can accept a partial prefix even though the producer failed. A downstream policy decision is also distinct from a producer execution error.

Select checks from the contract, not a universal matrix. A layered setting needs a distinguishing precedence case; a path-origin change needs another working directory; a snapshot guarantee needs a failure after work has begun and a comparison with the prior output. Preserve a nearby unchanged caller case during maintenance. Reopen the saved deliverable and check what the consumer uses, rather than asserting only that a file exists.

## Carry the contract through maintenance and delivery

For maintenance, compare the affected old and new clauses, preserve a useful failing-before observation when available, and check the actual callers after the repair. An added field, changed default, or newly buffered stream can break a caller despite unchanged option names. Migrate callers under your control when the change allows it; do not assume unknown external callers can move with them.

For delivery, use the requested native format and existing toolchain. A source invocation, an extracted copy, and an installed public command establish different things. If installation is part of the authorized work, identify the exact package, inspect it, install it in a fresh disposable consumer environment, and repeat the same meaningful caller case outside the source tree. See [maintenance and delivery](references/maintenance-and-delivery.md) for this conditional branch. A source-only task ends with source evidence and its stated limits.

Return the useful command or requested artifact, concise usage, the consequential contract choices, checks actually run, and remaining limitations. A changed package needs evidence tied to its changed bytes. Do not infer another operating system, shell, runtime, or installation route works from one local run. Building or checking a tool does not itself authorize publishing it or installing it globally.

## Related methods

This toolkit brings several existing methods together at the command boundary. `design-api-contract` develops consumer obligations; `dot-stack` provides caller-led architecture, boundary discipline, and evidence tied to the candidate; `write-behavior-tests` develops distinguishing assertions; `api-contract-change-audit` contributes directional consumer compatibility; and `release-artifact-verification` owns deeper package and installed-consumer checks. `bound-stream-transforms` adds resource and integrity controls when input size does not bound transformed output. Those are optional deeper resources when available; the essential CLI decisions above do not depend on installing them.
