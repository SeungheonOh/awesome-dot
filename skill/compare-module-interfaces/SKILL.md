---
name: compare-module-interfaces
description: Inspect and compare authorized compiled-module artifacts by exact byte identity, declared imports and exports without executing their code; separate interface inventory from compatibility and safety conclusions.
---

# Compare module interfaces

## When to use

Use before integrating a supplied compiled module, reviewing a build-artifact change or documenting host dependencies. The task is to establish what the artifacts declare and what changed, while avoiding execution as an accidental side effect of inspection.

## Required inputs

- Authorized artifact bytes and the expected container/module format
- Ordered before/after identities when comparing revisions
- The target runtime and enabled features, if compatibility with one runtime matters
- Which interface fields are required: names, kinds, signatures, limits or behavior
- Resource limits and whether names or metadata may appear in exported evidence

If the available inspector only exposes names and kinds, explicitly narrow the conclusion to those fields. Do not infer signatures from function names or compatibility from identical export names.

## Workflow

### 1. Freeze exact artifact identities

Hash the original bytes and associate the hash with the before/after role. A filename, build label or modification time is not enough to identify a binary. Bound input size before hashing or compiling, and preserve the original artifact.

Validate the format header before using format-specific APIs. For WebAssembly, distinguish a core binary from a component binary rather than sending both through a reader that assumes the same grammar.

### 2. Inventory framing without executing payloads

Read record lengths with checked offsets and format-correct integer decoding. WebAssembly unsigned 32-bit LEB128 may use padded encodings within its five-byte bound; do not incorrectly require the shortest encoding. Reject overflow, continuation beyond the bound and lengths crossing the containing record.

Bound record count and names, decode UTF-8 strictly, and preserve meaningful characters such as an initial byte-order-mark character in a name. Custom-section data can remain opaque. Report offsets, lengths and labels without including entire debug payloads or code bytes when they are unnecessary.

Framing inspection does not validate every section grammar. Keep that distinction visible rather than calling a bounded ledger a full validator.

### 3. Use a non-executing interface API

Choose a documented API that reads or validates module metadata without instantiation. For WebAssembly in JavaScript, compilation into WebAssembly.Module allows import/export inspection; constructing WebAssembly.Instance or calling instantiate is a different operation that can invoke a start function.

Run expensive parsing/compilation in a cancellable worker with a deadline. Do not satisfy imports, run initialization, call exports or follow module-provided URLs merely to discover the interface. Record a declared start index as a warning about future instantiation, not as proof that code ran.

A runtime can reject a valid artifact because it lacks a feature. Separate format errors, application inspection limits and runtime rejection. Runtime acceptance establishes neither safety nor portability.

### 4. Compare structured keys and multiplicity

Represent imports with their namespace/module, name and kind; represent exports with their name and kind. Use tuples or structured serialization rather than an ambiguous delimiter-concatenated key. Preserve repeated import declarations as counts instead of losing them in a set.

Report additions and removals under the stated identity policy. A changed kind can be represented as a removed old tuple and an added new tuple. Do not treat source-order changes as interface changes unless order matters to the task.

An unchanged tuple can hide a new signature, memory limit, calling convention or implementation. Mark those dimensions unexamined when the inspector does not cover them. Numeric function indices are local to a module and are not durable cross-build identities.

### 5. Export bounded, reviewable evidence

Include exact hashes, inspection scope, runtime acceptance or rejection, declared interfaces and the comparison policy. State the runtime version/features when known; otherwise disclose that engine identity or cross-engine behavior was not established.

Avoid original filenames, source paths and opaque payloads unless needed and authorized. Names, sizes and hashes can still reveal project details. A report is not automatically anonymous or approved for external distribution.

Limit visible rows and long labels while keeping any complete bounded export clearly identified. Invalidate old exports when inputs change, and prevent late worker replies or canceled file reads from replacing newer results.

## Worked example

The before module imports ("env", "log", "function") and exports ("tick", "function"). The after module imports ("env", "record", "function") and exports ("run", "function"). The name/kind comparison reports two removed tuples and two added tuples, tied to the two SHA-256 hashes.

Both declare start index 1. Report the index as unchanged, but do not claim the start function's implementation or identity is unchanged. Neither start function was run during metadata inspection.

A third build can keep exactly the same import/export tuples while changing a function's parameter types. A names-and-kinds-only report correctly says no change in the examined fields and leaves ABI compatibility unresolved.

### Optional: distinguish byte changes from interface changes

When the question includes what changed inside an artifact, hash each complete encoded section after bounding its framing. State whether the hash covers payload only or the ID and encoded length as well. Alternate legal length encodings can change the latter hash without changing payload semantics.

Compare fingerprints as a multiset so duplicate custom sections retain their counts. Check the ordered fingerprint sequence separately: equal multisets with different ordering are a reorder, not identical binaries. Do not pair same-named sections as if their names were unique identities. A changed section can be represented as a removal plus an addition. This byte-level comparison can remain available after runtime rejection, provided independent framing succeeded; it does not make rejected interfaces available.

Worked example: before has custom sections A, B, B; after has B, A. The report records one removed B and a changed sequence. If after instead has B, A, B, the multiset is unchanged but the order differs. Neither outcome establishes behavioral equivalence. Verify complete section hashes against an independent digest implementation and include duplicate, reorder, padded-length and invalid-code fixtures.

## Verification and stopping conditions

Test known module fixtures, malformed lengths, integer boundaries, padded encodings, invalid UTF-8, duplicate imports, unknown runtime features and changed bytes with unchanged interfaces. Replace instantiation APIs with throwing stubs during inspection tests to catch accidental execution paths. Also test worker deadlines, replacement-file races, cancellation and stale export controls.

Stop before executing a module when the task only authorizes inspection. Ask for the intended runtime or deeper interface requirements when they materially change the conclusion. Do not turn absence of suspicious names into a safety verdict.

## References

- [WebAssembly binary modules](https://webassembly.github.io/spec/core/binary/modules.html)
- [WebAssembly binary values](https://webassembly.github.io/spec/core/binary/values.html)
