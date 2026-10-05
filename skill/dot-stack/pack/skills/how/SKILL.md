---
name: how
description: "Explain a code path, subsystem, or ownership boundary from actual source, with a coherent runtime flow and precise references."
---


# How

Build a working mental model of the code. This is read-only exploration and explanation, not a refactor request. Use [why](../why/SKILL.md) for historical motivation when needed; do not infer original intent from a function name.

## Choose the smallest useful route

Interpret the question using visible context and identify the source revision or supplied artifact. For one function or module, read it and its relevant callers directly. For a subsystem, identify distinct angles such as input-to-output flow, state lifecycle, and integration boundaries. Delegate those angles only if actual native workers improve coverage. Otherwise follow them sequentially. No model selection or fixed worker count is required.

If source is missing, use supplied material and explain what cannot be traced. Ask for the minimal additional files if they are essential. Do not pretend a URL, catalog name, or repository name is the contents of a file.

## Trace, do not guess

Use [the explorer contract](references/explorer-prompt.md) as needed. Find the entry point and follow actual calls, transformations, decisions, and side effects. Read implementations and type definitions, not only symbol matches. Trace failure, cancellation, retry, and cleanup when relevant. Identify ownership of validation and state.

For “where should this live?”, compare the owning invariants and dependencies of candidate modules. Distinguish where the code currently lives from your recommendation. A file map without a data or control flow does not answer how the system works.

## When a general argument is requested

When explicitly asked for a general correctness or termination argument, state the claimed property, actual input domain, and what counts as the same output or item. Trace which premises validation establishes and which depend on callers or the environment. Account for normalization, representation, and equality in the inspected code; do not silently substitute an idealized contract.

Choose an invariant, induction, or case argument suited to that property. Tie each step to source: establish the starting condition, show why every relevant update or branch preserves the needed conditions, and derive the result at exit. Where termination matters, justify progress separately, using a well-founded measure or another appropriate argument, and cover relevant failure or early-exit paths.

Keep this route proportional to the requested argument; ordinary how questions do not require a formal proof framework or execution. Distinguish selected traces or tests from general reasoning, and limit exhaustive enumeration to the domain it actually covers. State unresolved premises or steps, and do not present a source-derived argument as execution evidence or security assurance.

## Reconcile and explain

Use [the explainer contract](references/explainer-prompt.md). Check conflicting findings against source and preserve unresolved gaps. Do not relay a worker's speculation as verified runtime behavior. Source reading establishes what the inspected code implements; actual execution evidence is a separate claim.

Start with what the subsystem does, then trace a representative operation. Include the few types or concepts needed to follow it, a short map of relevant files, and surprising constraints. Use a small diagram only if it clarifies the flow and the output medium supports it. Scale detail to the question.

Example of the desired precision: “The request handler parses the body, passes a domain command to the repository, and waits for the write before replying. The timeout path is unverified because the supplied excerpt omits the repository implementation.” Replace that example with real symbols and references for the user's code.

Return the explanation itself with source pointers and coverage limits. Do not claim to have run checks, opened files, or inspected services without the corresponding evidence.
