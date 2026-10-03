---
name: principle-minimize-reader-load
description: "Improve code comprehension by reducing unnecessary indirection and hidden mutable context while retaining boundaries that hide meaningful complexity."
---

# Minimize reader load

Use this when a real maintenance question is difficult to answer from the code. Track two independent costs: the layers a reader must trace and the state they must hold in mind. A single large file full of mutable globals can be as confusing as a chain of thin wrappers.

## Follow a concrete question

Choose a representative question such as “where is this value established?” or “what can change it before this request completes?” Trace the actual path and mark where the reader must switch files, recall earlier mutations, or infer a hidden invariant.

- Collapse a pass-through layer when it adds navigation without changing abstraction, policy, or ownership. One caller is a clue, not proof that a boundary is useless.
- Prefer an interface that hides meaningful decisions behind a smaller contract. A broad surface that mirrors every private operation makes readers learn both layers.
- Shrink mutable scope: return a result where practical, use local state instead of shared fields, and avoid globals when ownership is local. Derive a value rather than synchronizing two copies unless history or performance makes both necessary.
- Name and establish an invariant at its owning boundary. Keep a concise rationale for a surprising constraint rather than relying on repeated explanations in callers.
- Keep related behavior near the domain knowledge it uses. Do not inline a coherent abstraction merely to put everything in one file.

## Example and counterexample

Applies: computing an invoice total requires following four wrappers and remembering a module-level discount flag set by an earlier request. Replace the hidden flag with explicit validated input and collapse the wrappers that only forward it. The calculation becomes locally understandable and request-independent.

Does not apply: a storage adapter shields callers from transactions, retries, and wire errors. Removing it may shorten the trace while forcing every caller to understand those concerns. Preserve that compression.

## Evidence

Repeat the original comprehension question after the change. Record the removed indirections and hidden dependencies, and run behavior regressions. A fresh review can test whether the explanation is now local and accurate; a claimed fixed reading-time threshold cannot establish maintainability by itself. Stop when further flattening would expose more decisions than it removes.
