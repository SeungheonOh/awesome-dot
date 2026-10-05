---
name: analyze-algorithm-cost
description: Derive and explain time and storage costs from actual source and caller behavior. Use when a question needs a defensible bound, a repeated-operation cost, or an account of live and retained storage; implementation changes and empirical performance comparisons have separate workflows.
---

# Analyze Algorithm Cost

Explain what work the requested operation performs, why it has the stated cost, and which assumptions make that conclusion valid. A useful answer can be a tight bound, a conservative upper bound, or a parameterized expression with an unresolved dependency. Produce the explanation itself, scaled to the question.

Ordinary source exploration belongs to [dot-stack/how](../dot-stack/pack/skills/how/SKILL.md). This method adds cost modeling and composition when that is the question. Source reasoning can finish without executing code. Use [performance-change-verification](../performance-change-verification/SKILL.md) when the requested result is an empirical comparison; a static bound alone establishes neither a runtime improvement nor a numerical capacity limit. An explanation request does not authorize an optimization or benchmark.

## Establish the operation and its cost model

Read the relevant implementation, types and actual caller at the same revision or supplied artifact. Identify the accepted input domain and the operation's start and end. Include preprocessing, traversal, callbacks, output construction and cleanup only as the caller's boundary requires. Creating an iterator and consuming it are different operations. Distinguish a first call, reuse of existing state and a sequence of calls when they perform different work.

Choose parameters for quantities that can vary independently: input occurrences, distinct keys, query count, nesting depth, text or numeric representation length, and output size as relevant. State their relationships before eliminating a dimension. A balanced tree, bounded key length or fixed number of queries needs a supplied constraint; it does not follow from the name of a data structure. A bound in a numeric value can be very different from a bound in its encoded length.

Name the charged primitives and units: comparisons, reference copies, word operations, bytes or another useful measure. Specify which operations are constant under the chosen model. Inspect or consult the applicable implementation documentation for consequential library assumptions; interface names do not determine costs. Equality, hashing, key construction, slicing and serialization may inspect or copy growing values. Treat arbitrary callbacks and variable-size arithmetic explicitly, using a symbolic cost when no bound is supplied. Do not turn a count of additions into total time without accounting for operand size. [MIT's computation-model notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/477c78e0af2df61fa205bcc6cb613ceb_MIT6_006S20_lec1.pdf) distinguish elementary-operation counts from the model making those operations constant.

## Compose the work the source actually repeats

Use the argument that fits the code; there is no need to apply every technique.

- **Loops and pipelines:** Sum the body's cost over the iterations that execute, including helper calls and materialization. Nested syntax alone does not establish multiplication: an inner cursor may advance only once across the whole operation, or restart for every outer item. Charge repeated copying by the lengths copied at each step. Keep a shape-dependent sum when replacing it with a loose maximum would obscure the mechanism.
- **Recursion:** Relate each call to the actual child subproblems and its own work, with base cases and a decreasing measure or other termination premise. Include splitting, copying, merging and result construction in the local term. Check whether subproblems overlap and are recomputed. Recursion depth bounds live frames, not total calls; branching can change work without changing depth.
- **Memoized or iterative state:** Count reachable states and transitions, with the work of generating, comparing and combining them. A possible-state count is an upper bound unless reachability is established. Count repeated relaxations or passes when state can change. “Computed once” requires a valid cache entry that remains available; eviction, invalidation or overlapping computations can require more work. Cache hits can still build keys, copy results or perform caller work. [MIT's recursive-analysis notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/9eb3e9a51a7b5b60b0f67c2277f8b0ee_MIT6_006S20_lec15.pdf) develop total work from per-subproblem work and account for growing integer values.

For repeated operations, write setup plus the sum of call costs under the actual initial state and update rules. Include rebuilds or disposal when the boundary charges them. Do not distribute setup over hypothetical future uses or infer constant per-call cost merely because some work is cached.

## Qualify and check the bound

State what the bound covers: all permitted inputs, a worst case at stated dimensions, a particular shape, or a conditional operation sequence. Retain unknown contributions, for example total callback work, beside the known structural term. An upper bound remains an upper bound until matching lower-bound reasoning justifies tightness. For a worst-case tight claim, give a permitted family that attains the order; a small example or the largest input inspected is insufficient. Do not describe one implementation's bound as a lower bound for every algorithm solving the problem.

If an expectation is relevant, name the input distribution or randomized mechanism and what is held fixed. With no such model, leave average-case cost unspecified. Amortized cost instead bounds total work over a defined sequence, including expensive individual operations and the initial state. Support it with an aggregate, charging or potential argument suited to the code; a warm timing average is not that argument. Expected and amortized qualifications can coexist, as the separate collision and resizing arguments in [MIT's hashing notes](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/ce9e94705b914598ce78a00a70a1f734_MIT6_006S20_lec4.pdf) illustrate. Those theoretical assumptions do not automatically apply to a language's dictionary.

Check the derivation against the source's actual branches and a useful limiting case. For example, let one independent dimension stay small while another grows, or consider a permitted shallow versus deep structure. Confirm that output construction and early termination agree with the bound. Use this reasoning to correct the argument, without turning every explanation into a generated test suite or formal proof project.

## Account for storage by ownership and lifetime

Declare whether the space result counts auxiliary storage, input, output, retained state or their total, and whether units are slots, objects, words or bytes. Identify simultaneously live structures through the operation, rather than summing all allocations made over time.

Trace creation, sharing and release through the caller. A shallow copy adds reference slots while sharing payload objects; a slice or view may keep a larger backing object alive. Count each distinct payload once in a total, while retaining the costs of multiple containers and references. Include active recursion frames and their local data, unfinished intermediate results, buffers and caches. Sequential phases can reuse space, but an old result may remain live while its replacement is built. Add concurrent storage only where the caller actually permits overlapping work.

Separate peak temporary storage from what remains after return and across calls. A cache-entry limit does not bound payload bytes without a size assumption. Python's [lru_cache documentation](https://docs.python.org/3.14/library/functools.html#functools.lru_cache), for example, specifies retention of arguments and results until eviction or clearing. Clearing one owner does not release objects still reachable from another.

Keep removal of references, becoming unreachable, reclamation and returning memory to the operating system distinct. If cleanup cost depends on eager reference release or a collector, label that model. Unknown callback workspace and retained payload sizes remain explicit. Logical liveness is not measured process memory; a shallow size is not transitive storage, as the [getsizeof documentation](https://docs.python.org/3.14/library/sys.html#sys.getsizeof) makes explicit.

## Deliver a defensible explanation

Lead with the answer to the caller's question. Define the necessary parameters and assumptions, then show the decisive sum, recurrence or ownership argument with precise source pointers. Include only the bounds and scenarios that matter. Explain a surprising difference between local helper cost and whole-operation cost where the source supports it.

Distinguish source-established behavior, derived conclusions and unresolved premises. If a missing callback or library implementation prevents a full bound, finish the structural argument and name the specific unknown. A short self-contained note is usually enough; do not require a separate manifest, benchmark, proof packet or rewrite to answer a source-only question. Stop when the requested cost explanation and its limits are clear.
