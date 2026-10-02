---
name: compare-restricted-pattern-languages
description: "Check whether two patterns accept the same full strings within an explicitly supported regular-language syntax, returning a shortest distinguishing string or a scoped complete/incomplete result."
---

# Compare Restricted Pattern Languages

## When to use

Use this when a user or agent wants evidence that a proposed validation or matching-rule rewrite preserves accepted strings. Examples alone can disprove equivalence but cannot generally prove it. This workflow uses finite automata only when the actual syntax and matching semantics are supported; it must not silently reinterpret a richer production regex dialect.

## Required inputs

- The two exact patterns and intended matching engine/dialect
- Full-string versus substring matching semantics
- Alphabet, Unicode/case behavior, flags and treatment of empty input
- Supported operators and a finite exploration budget
- Authorized test fixtures and the intended evidence output

Backreferences, lookarounds, locale behavior and engine-specific constructs require explicit support or a different verification route. Do not remove unsupported constructs, anchors or flags and claim the simplified result covers the original patterns.

## Workflow

1. **Freeze semantics.** State exactly what counts as a match, including whether the entire string must be consumed. Distinguish an empty pattern accepting the empty string from a pattern accepting no strings. Pin the alphabet and character-unit definition used for witness length.
2. **Parse the supported syntax.** Validate length and nesting limits before construction. Apply the documented precedence: repetition to its operand, concatenation, then alternation. Reject unsupported or malformed syntax instead of falling back to a permissive interpretation. The pattern is data, not code to evaluate.
3. **Construct and check automata.** Compile each pattern into a finite automaton, for example a Thompson epsilon-NFA. Compute epsilon closures with a visited set so epsilon cycles terminate. Test literal, empty, optional, repeated, concatenated and alternative fragments against their intended semantics.
4. **Explore the product by breadth-first search.** Start from both initial epsilon closures. For each relevant character, compute both next state sets and their closures. Canonicalize sets so the visited key does not depend on traversal order. Store predecessor and character for every discovered pair.
5. **Check acceptance mismatch, including at the initial pair.** If exactly one side accepts, reconstruct a distinguishing string from predecessor links. An initial mismatch yields the empty string; it is a real witness, not a missing result. With unit character costs, breadth-first discovery establishes shortest length. Document the tie-break order when several shortest witnesses exist.
6. **Separate the three outcomes.** A witness means different languages. Exhausting every reachable pair without a mismatch means equivalent only under the stated semantics. Reaching a budget or canceling means incomplete. Count discovered and processed pairs distinctly if both appear in the report; neither a small sample nor an interrupted queue proves equivalence.
7. **Verify a witness independently.** Feed the full string into an independent interpreter or engine that truly shares the supported semantics. Confirm exactly one match and, for small fixtures, enumerate shorter strings to check minimality. Do not accidentally use a substring matcher or engine-specific end anchor that changes the conclusion.
8. **Package the evidence.** Return the exact patterns, supported semantics, alphabet, status, budget/work counts and full witness with each side's acceptance. Render the empty string explicitly. If previews are truncated, preserve the complete witness in the evidence artifact. Keep private patterns local unless sharing is authorized.

## Worked examples

### Empty-input regression

Compare a* with a+ under full-string matching over the alphabet {a}. The initial closure for a* accepts and the one for a+ does not. The shortest distinguishing string is the empty string, length0. Both accept a, aa and longer all-a strings, so a test set containing only nonempty examples would miss the regression.

### Equivalent rewrites

Compare (a|b)* with (a*b*)* under the same restricted syntax over {a,b}. Both accept every finite string of a and b, including empty. Complete product exploration should find no acceptance mismatch. If the configured budget stops the search early, report incomplete even though this mathematical example has a known equivalence.

### Prefix distinction

Compare ab with a. The string a is accepted only by the second pattern. This witness depends on full-string matching; do not use a search-for-substring API to verify it.

## Validation cases

Cover empty input, empty alternatives if supported, nested epsilon cycles, characters outside the alphabet, precedence, unsupported syntax, an intentionally tiny budget and cancellation followed by a new request. For a small alphabet, cross-check membership across all strings up to a fixed length using a separate implementation. That finite enumeration is a regression check, not the equivalence proof.

## Limits and stopping point

A result for the model's syntax does not establish compatibility with arbitrary JavaScript, PCRE or another engine. It also does not measure runtime backtracking behavior or security against expensive matching. Stop once the scoped comparison and witness checks are complete; changing a live validation rule or widening input acceptance requires separate authorization.
