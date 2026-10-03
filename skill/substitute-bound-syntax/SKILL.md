---
name: substitute-bound-syntax
description: Perform capture-avoiding substitution on syntax trees with lexical binders, preserving free variables and shadowing. Use when implementing or reviewing interpreters, symbolic reducers or scope-sensitive transformations; not for plain text replacement or a full language compiler.
---

# Substitute bound syntax

## When to use

Use when replacing a variable with an expression can cross lexical scopes. The task is to preserve what every variable refers to while transforming syntax. A string replacement can silently change meaning even when the output still parses.

## Required inputs

- The grammar and AST node types, including every construct that introduces a binder
- The variable being substituted, replacement expression and subtree receiving it
- Rules for shadowing, variable identity and name generation
- For a reducer: the exact reduction strategy, stopping conditions and resource bounds

The workflow below uses variables, abstractions and applications as a small reference grammar. Extend it deliberately for pattern bindings, recursive bindings, modules or macros; each has its own scope boundaries.

## Workflow

### 1. Establish structure and binding

Parse into an AST before substitution. Specify application association and abstraction extent rather than relying on pretty-printing intuition. Reject unsupported syntax, trailing input and malformed binders. Put limits on input bytes, nesting and identifier lengths before recursive processing.

Compute free variables structurally: a variable contributes its name; an application takes the union of its children; an abstraction removes its binder from its body's free set. Preserve names exactly. If the language uses symbols or unique IDs rather than names, honor those identities instead.

### 2. Replace only the intended free occurrences

For substitution of expression N for variable x:

- At a variable, replace it only when it is x
- At application, substitute in both children
- At an abstraction binding x, stop; occurrences inside belong to that binder
- At another abstraction, first determine whether x is free in its body. If not, leave the subtree unchanged
- If x is free there and the binder also occurs free in N, rename that binder before descending

The early free-variable check avoids unnecessary renaming and makes the trace easier to explain. Do not rename every occurrence of the old name indiscriminately: nested binders using the same spelling shadow the outer binding.

### 3. Generate a genuinely fresh binder

Choose a name absent from all names in the receiving subtree and replacement, including existing bound names, and reserve newly generated names during this transformation. Renaming the selected binder must rename precisely its bound occurrences, stopping at an inner binder with the same old name.

Then continue substitution into the renamed body. Preserve the replacement's free variables. Keep an explicit record of binder renames when explaining a reduction; do not present alpha-renaming as a computational result or a changed user variable.

### 4. Separate substitution from strategy

Substitution answers how one redex changes. Strategy answers which redex to contract. Keep the two operations independently testable.

For full normal order, choose the leftmost outermost beta redex. For full applicative order, choose the leftmost innermost one. Both may reduce beneath abstractions. Do not label full applicative normalization as call-by-value without matching the language's value restriction and evaluation contexts.

Record the redex location, before/after expression and any renames. A step limit does not prove divergence. If detecting repeated states, compare alpha-equivalent structure, preserving free names and representing bound occurrences by their distance to the nearest matching binder. A repeated state proves looping only for the stated deterministic strategy; it does not exclude another strategy reaching a normal form.

### 5. Bound the work and preserve valid state

Substitution can duplicate a large argument. Cap intermediate node count and depth as well as input size and step count. For an interactive tool, use cancellable isolated computation and a deadline; a counter alone may not prevent a costly individual step. Report the last valid state and the specific limit hit rather than publishing a partial transformation as a normal form.

When input or strategy changes, invalidate old results. Ignore replies from canceled or superseded computations. Trace exports contain source expressions, which may be private; do not describe them as anonymized diagnostics.

### 6. Verify binding, not spelling

Test shadowing, a free replacement variable colliding with a binder, an existing generated-looking name, substitution where the target is absent, and reduction underneath an abstraction. Compare results modulo alpha-equivalence rather than requiring one fresh-name spelling.

For independent implementation evidence, represent bound variables as de Bruijn indices and implement shifting/substitution there. Compare named-tree single-step results against the index-based reducer for each strategy. Also test parse/print roundtrips modulo alpha-equivalence and that beta reduction introduces no new free variables. These checks support implementation confidence; they are not a machine-checked proof for every term.

## Worked example

Reduce `(λx. λy. x) y`. Replacing x directly with y would produce `λy. y`, capturing the originally free y and changing the meaning. Rename the inner binder to a fresh name first: `λv_1. x`. Substituting then produces `λv_1. y`, where y remains free. If v_1 already occurs in the body or argument, choose another fresh name.

For shadowing, `(λx. λx. x) free` reduces to `λx. x`: the inner binder blocks substitution into its body. For strategy sensitivity, `(λx. answer) ((λz. z z) (λz. z z))` reaches `answer` under normal order, while full applicative order repeats the argument state. This demonstrates why a looping trace must be labeled with its strategy.

## Evidence and reference

This procedure was exercised with hand-checked capture/shadowing examples and 1,400 single-step comparisons against an independently implemented de Bruijn reducer. Resource and UI checks are separate from semantic checks. See [Cornell's capture-avoiding substitution explanation](https://courses.cs.cornell.edu/cs3110/2021sp/textbook/interp/subst_lambda.html) for the underlying binding problem.
