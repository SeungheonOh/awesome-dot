---
name: build-incremental-generator
description: Create or repair artifact generation that reuses valid prior outputs and rebuilds affected work after input, configuration, tool or dependency changes. Derive complete dependencies and cache identities, handle missing or retired outputs, and verify the actual incremental result and its consumer. Use when selective regeneration is required; ordinary rerunning and cache-eviction analysis have different goals.
---

# Build an Incremental Generator

Deliver a usable generation workflow whose reuse decisions are correct for its stated inputs and consumer. A fast run, an unchanged timestamp or a reported cache hit does not establish that an artifact represents current inputs.

Start with the existing build mechanism and a correct ordinary generation. Prefer the project's supported dependency and cache features. A small wrapper may be sufficient for a bounded local transformation; do not invent a build framework, remote cache or scheduler. When selective reuse is not required and a full rebuild is simpler, explain that tradeoff and use the simpler correct route.

## Establish the artifact and consumer contract

Identify the selected source scope, transformations, outputs and actual reader or downstream command. Determine which outputs must agree as a set and whether users read stable filenames, a manifest, an archive or a selected generation. Keep authoritative source, reusable computed results, cache metadata and currently published outputs distinct.

Establish the expected semantics before optimizing reuse. A clean generation needs a meaningful content check, including ordering, identities, omitted inputs and relevant error behavior. Preserve the existing transformation unless changing it is requested. A cache must not make an invalid transformation look reliable by repeating its old result.

Define the requested unit of reuse. It may be one document, an output pair, a whole archive or an aggregate over many items. One source can produce several outputs; several sources can determine one output. Do not choose one file per action merely because filenames are convenient. Ordinary automation and implementation guidance still supplies ownership, execution and recovery; the additional obligation here is justifying reuse.

## Derive all output-affecting dependencies

Trace the actual read path, including transitive reads. Consider source content, shared templates, configuration, flags, included fragments, transformation code, relevant runtime/tool behavior and output-affecting environment values. An input can matter without appearing on the command line. The [Ninja dependency documentation](https://ninja-build.org/manual.html#ref_dependencies) illustrates this distinction between declared command inputs and other files a command reads.

Include selection itself. An aggregate over a directory depends on the defined membership rule and current selected names, not only the hashes of files known last time. An optional file can affect output when it changes from absent to present. Record that absence or query result where it matters. Keep excluded files outside the dependency set when the transformation truly does not use them.

For includes or discovered inputs, distinguish unique dependency identity from output occurrence semantics. A shared fragment may be read once for identity while deliberately contributing content several times. Do not deduplicate output merely because the same source is reachable by two paths. Preserve meaningful include order and namespaces.

Choose a supported way to obtain dependencies: an explicit manifest, a format-aware scan, a compiler dependency receipt or a narrowly inspected transformation. A previous receipt describes the previous action; revalidate its inputs and account for changes that could discover a different dependency set. If coverage is unknown, use a conservative dependency boundary, rebuild or report the unsupported reuse claim. Hashing an incomplete list does not make it complete.

Separate value dependencies from ordering constraints. A prerequisite needed only to establish a directory or generated tool need not mean every change to it changes every output, while an included value must invalidate its consumers. Follow the actual build engine's semantics rather than treating every edge as interchangeable. Resolve a dependency cycle or required bootstrap explicitly instead of inventing a topological order.

## Define an unambiguous action identity

Specify the information under which a prior result can be reused: relevant input identities, transformation/version, options, toolchain properties and output contract. Use a versioned representation with clear field boundaries, such as structured canonical data or length-delimited fields. Concatenating strings without boundaries can give different actions the same apparent key.

Use content identities when the contract requires detecting edits that preserve size or timestamp. Keep original path spelling, case and namespaces unless their equivalence is established. Normalize only documented semantic equivalents; conservative misses are preferable to conflating distinct inputs. A repository commit alone does not account for dirty files, external templates or changed tools.

Remove or make explicit ambient dependencies such as current time, locale, random state or a tool found through an uncontrolled search path. Do not call an action deterministic merely because one repeat matched. For an existing cache, inspect what the engine actually includes in its key instead of assuming it tracks every executable or environment value.

The [Bazel cache documentation](https://bazel.build/remote/caching) distinguishes action-result metadata from stored output bytes and describes action inputs, commands and environment. Those are useful concepts; using a similar local design does not establish Bazel compatibility or require a remote service.

## Decide reuse from metadata and actual outputs

A hit needs both a matching valid action identity and the required usable result. Reopen or otherwise verify the expected output set under the cache's supported integrity contract. A file that exists can be missing content, corrupted, from another action or only one member of a required group. If cached bytes can legitimately be materialized elsewhere, verify their identity and the materialized result.

Validate cache metadata and its format/version. Preserve an unsupported or damaged state for diagnosis and rebuild safely when that is allowed; do not silently reinterpret it as successful current work. A missing cache is different from an invalid current source. Never hide a new source error behind a prior hit.

Propagate invalidation through the real dependency graph. A leaf change can affect its output and downstream aggregates while leaving unrelated work reusable. Shared configuration or tool changes may affect many actions. Added and removed sources change the selected inventory; obsolete generated files must not remain selected as current. Missing or altered output can require regeneration even when all inputs match.

Keep the reasons inspectable when they help explain behavior: changed input, changed tool/options, discovered dependency, absent result, damaged output or valid reuse. Do not infer actual work skipped from output equality alone; a command can regenerate identical bytes and still claim a misleading hit. Correctness matters before hit rate, and a conservative rebuild need not be a defect unless it violates the requested reuse contract.

## Publish a coherent result

Use a consistent source snapshot or the build system's supported change-detection behavior. If sources may change during capture or execution, establish what detects that change and whether the candidate is discarded or remains labelled for a captured version. A list of separately read hashes is not automatically an atomic source snapshot.

Preserve the distinction between finished computation, reusable cache entries and the selected output generation. Advance success metadata only after the corresponding outputs are complete and verified. A failed or abandoned stage must not later be called a completed hit without reconciliation.

Choose publication at the consumer's required granularity. A single file may need one supported atomic replacement; a group may need an immutable generation plus selector, a transaction or the application's own mechanism. Independent replacements of a catalog and its referenced files do not create one atomic set. Check that the real reader resolves the intended consistent generation, including a reader that began before a switch when that case matters.

Keep source, state and output ownership explicit. Preserve unrelated files and unknown prior work. Retired outputs may be omitted from the current selection while historical generations remain; deletion or garbage collection is a separate ownership and reader-lifetime decision. Use existing single-writer or concurrency controls appropriate to the task. State untested filesystem, interruption and durability properties instead of equating atomic visibility with power-loss safety.

## Verify freshness and genuine reuse

Exercise the actual public build command and saved consumer. Check a cold result against independent expected content. Repeat unchanged work and establish that the intended transformation was skipped, using a supported action report, invocation record or bounded test seam rather than a self-reported counter alone.

Choose mutations that challenge the declared dependencies: one source, a shared template or option, relevant transformation code, a discovered or optional input, membership addition/removal and a missing member of an output group. Use a same-size or unchanged-mtime edit when it distinguishes the proposed freshness mechanism. Select the cases the actual workflow needs; a small single-output generator does not need every possible build-system scenario.

Compare incremental output with clean generation under the same inputs and tools. Also keep an independent content or behavioral expectation: both paths can share the same transformation defect. Compare semantic content when incidental metadata is explicitly allowed to vary, and exact bytes when byte identity is the contract.

Exercise the meaningful failure boundary in an isolated copy. Inspect the actual selected output and cache state after failure, then retry and verify what was reused, rebuilt or retained as incomplete. A controlled stop before publication proves that boundary, not every possible crash. Preserve useful failed evidence and avoid running arbitrary cached commands or unreviewed transformation code merely to test the cache.

Deliver the runnable workflow or scoped repair, its invocation and required inputs, the selected usable result, and a short account of dependency/key choices and observed reuse. Include maintenance instructions for source additions, tool changes and invalid state where needed. Keep performance claims separate: fewer transformations can be observed without claiming a measured end-to-end speedup. State the actual consumer, concurrency and platform coverage.
