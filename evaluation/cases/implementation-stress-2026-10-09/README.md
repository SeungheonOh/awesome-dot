# Implementation stress cases: UNRUN

These are author-reviewed test cases, not observed model results. All task scenarios and fixture data are fictional/synthetic. Candidate runs: **0**. No new performance scores are reported. Whole-contract outcomes remain pending; there is no guarantee that a future candidate will score below 100%.

This data-only package contains four task contracts and 881 authored input vectors with expected outputs:

- Async reducer: 35 development + 30 confirmation input vectors, covering request ownership, stale completions, cancellation, captured comparisons, selection/export consistency and detached snapshots
- Partial-order reconciliation: 24 + 16 input vectors, covering revision reconciliation, unresolved evidence, graph provenance, ranks, cycles and query witnesses
- Exact capped allocation: 219 + 198 input vectors, covering exact rational quotas, floors/caps, stable ties, zero-weight fallback, feasibility and large integers
- Unicode merge: 181 + 178 input vectors, covering source-coordinate edits, transitive interactions, endpoint insertions, no-ops, Unicode and newline fidelity

These counts describe authored fixtures, not model attempts. Development and confirmation are historical authoring labels only. Both sets and all expected outputs are now publicly disclosed; neither is a fresh or inaccessible held-out evaluation. Any future evaluation must account for this exposure and establish its own independent held-out material when needed.

## Contents and interpretation

Each task has a TASK.md contract and two gzip-compressed JSON fixture files (.json.gz). cases.json records functions, semantic groups, counts and immutable public-guide links with hashes. provenance.json binds the projections to the source freezes and describes transformations. No operational execution tooling is included. Expected/reference outputs do not constitute an executed evaluator.

Fixtures are compressed deterministically with gzip (mtime=0); decompression restores the original JSON bytes exactly. cases.json and provenance.json record compressed and decoded SHA-256 hashes and byte sizes. The four stateful fixture files are objects with schema_version, phase and checks; each input vector stores id, groups, positional args and expected. Allocation and merge files are arrays of records with id, group, named input and expected. Their successful expected output is wrapped in a value field; allocation exception records use a raises field. These wrappers describe authored outcomes, not observed candidate results. Expected values are retained from the authored source artifacts; packaging did not recompute them or run any candidate, reference, grader or test. Allocation fixtures may describe an expected ValueError for infeasible totals. Partial-order path, cycle and topological-witness examples are illustrative valid expected outputs: the contract accepts other valid witnesses, so literal equality to those witness fields is not a complete validity criterion. Input non-mutation and mutable-alias isolation require execution-based invariant checks; fixtures alone do not establish them. Purity, determinism and runtime requirements also cannot be established by static fixture inspection.

Contracts retain their mathematical and behavioral requirements. The two stateful contracts omit delivery/evaluation-process sections and every contract carries a projection/status note. Source contract hashes and exact suffix boundaries are recorded in provenance.json. The four existing public guides are linked at a pinned repository commit; they are background material, with each task contract governing its additional or more specific rules.

This directory is an authored-case collection, separate from observed studies. It makes no claim about candidate performance, difficulty achieved in trials, or whole-contract correctness.
