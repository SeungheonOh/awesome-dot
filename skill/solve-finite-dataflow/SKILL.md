---
name: solve-finite-dataflow
description: Compute and validate least fixed points for finite monotone set analyses, with explicit seeds, dependencies and convergence evidence. Use for grammar FIRST/FOLLOW calculations or similar reachability and dataflow tasks, not numeric equation solving or analyses with unbounded fact domains.
---

# Solve finite dataflow

## When to use

Use when facts depend recursively on other facts, and a one-pass traversal misses information. Deliver the resulting facts with enough explanation to distinguish a converged analysis from a partial bounded approximation.

## Required inputs

- Finite entities and fact universe
- Transfer rules stating which facts may be added and under what conditions
- Initial seeds and any distinguished entry or start entity
- Requested downstream interpretation, including how to handle conflicts or empty sets

Verify that the domain is finite and updates are monotone before relying on this procedure. Rules that remove facts, invent unbounded values or depend on absence may require a different analysis.

## Workflow

### 1. Normalize identities and validate the model

Separate entity names from data labels and reserved sentinels. Use maps or sets that treat prototype-looking names as ordinary data. Reject malformed rules and accidental duplicate alternatives when duplicates would produce misleading conflict counts. Preserve the full entity roster, including entities that receive no facts.

For a grammar supplied as named productions, document the classification rule: defined names are nonterminals; other symbols are terminals. Under that rule, a misspelled nonterminal becomes a terminal rather than an unresolved reference. Show the terminal roster so that the user can catch this mistake. Represent the empty production structurally, not as an ordinary token with a special-looking spelling.

### 2. Define the smallest starting state

Initialize facts to empty sets or false predicates, then add only justified seeds. For reachability, seed the requested entry. For FOLLOW sets, seed the start symbol with the end-of-input sentinel. Seeding every entity computes a different problem.

Keep distinct concepts separate. A nonterminal being nullable is a Boolean fact; epsilon need not be stored as a terminal in FIRST. An empty fact set is a legitimate result and must not disappear from the output.

### 3. Propagate until no fact changes

Apply transfer rules, unioning newly justified facts into existing sets. Repeat complete passes until a pass adds nothing, or use a worklist that revisits every dependent rule when its inputs change. A change flag must reflect an actual new fact, not simply encountering a nonempty set.

Termination follows from a finite fact universe and growth-only updates. Explain the applicable finite bound rather than choosing a magic iteration count and calling its last state final. If a practical deadline or resource cap stops computation, label the result incomplete and block downstream claims that require convergence.

For mutually dependent nullable/FIRST facts, iterate them together or compute nullable completely first. Compute FOLLOW only after the sequence-FIRST operation has stable prerequisites. In a sequence, continue past a nonterminal only if it is nullable; a terminal stops the scan.

### 4. Preserve competing explanations

When facts feed a decision table, retain every applicable alternative in each cell. Never overwrite an earlier rule just because another one is visited later. Distinguish no alternative, one alternative and multiple alternatives.

For LL(1), a production contributes its leading terminals to its row; if its entire RHS is nullable, its row also uses the LHS FOLLOW set. A multi-production cell is a grammar/table conflict, not proof that the language is inherently ambiguous. Do not automatically rewrite associativity, precedence or the grammar to hide the conflict.

Keep reachability and productivity diagnostics separate from these set equations. State whether downstream execution blocks on all conflicts or only a separately analyzed reachable subset.

### 5. Validate the fixed point independently

Check that every seed remains present, every transfer implication holds at the result, and another complete pass adds nothing. Reorder entities and rules and compare sets rather than presentation order. Include cycles without seeds, chains whose facts need several passes, empty productions and nullable suffixes.

For small acyclic grammar fixtures, enumerate complete derivation trees independently. Derive FIRST from the first terminal of each yield, nullable from empty yields, and FOLLOW from the terminal immediately after each nonterminal's span in a complete start derivation. Use reachable, productive fixtures for this oracle so that its language-yield interpretation matches the intended comparison. Bounded enumeration of a recursive grammar is not a completeness oracle.

### 6. Deliver the result and its scope

Report exact sets, empty sets, seeds, relevant conflicts and resource limits. Keep the source model with the output when authorized. If an interactive input changes, invalidate dependent analyses and traces together. Do not export a stale successful trace beside a newly edited model.

## Worked example

Take S → A b, A → B, and B → a | empty. Initially only FOLLOW(S) contains the end sentinel. B becomes nullable and has FIRST {a}; those facts propagate to A. S is not nullable because its final b cannot disappear, and FIRST(S) is {a, b}. FOLLOW(A) receives b from S's suffix, and FOLLOW(B) receives b from FOLLOW(A).

Now consider S → A a and A → a | empty. The A/a table cell receives both alternatives: one because a starts the nonempty production, the other because a follows A. Preserve both production IDs and explain why one lookahead token cannot select between them under this table. Do not keep whichever alternative happened to be inserted last.

## Reference and evidence

The grammar application was tested against 180 finite acyclic derivation-tree fixtures in addition to conflict, empty-input and cycle cases. See [Cornell's top-down parsing notes](https://www.cs.cornell.edu/courses/cs4120/2026sp/notes/topdown/) for the grammar-specific fixed-point equations. These tests provide implementation evidence, not a proof for arbitrary transfer systems.
