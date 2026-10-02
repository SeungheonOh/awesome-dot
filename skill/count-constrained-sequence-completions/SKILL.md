---
name: count-constrained-sequence-completions
description: "Count and construct completions of a small partially fixed sequence, using sufficient-state dynamic programming and independent checks while preserving the user's existing choices."
---

# Count Constrained Sequence Completions

## When to use

Use this when an agent or user has a short sequence with some fixed positions and needs to know whether it can be completed, how many completions remain, or which next choice preserves feasibility. Examples include a bounded symbol puzzle, an adjacency-constrained template or a small planning model with explicit transition rules.

This produces feasible completions under the supplied rules. It does not establish artistic quality, operational usefulness or an optimal choice unless the model also supplies and verifies an objective.

## Required inputs

- Sequence length and the finite allowed values at each position
- Fixed user choices, distinguished explicitly from empty positions
- Start/end restrictions, per-position rules and transition/history constraints
- Whether the task needs existence, an exact count, one witness or an optimized result
- Numeric and computation bounds, and permission to fill or change any user choices

Use a distinct empty marker such as null. Do not use zero when zero is a valid choice. Reject out-of-domain fixed values rather than silently clearing them to make the problem solvable.

## Workflow

### 1. Express the constraints before choosing a solver

Separate rules that depend only on one position, adjacent positions, the entire prefix or the final completed sequence. Preserve all fixed choices as constraints.

For a simple adjacent-transition model, a candidate at position i can be checked from i, the preceding value and the fixed external context. A rule such as “each symbol may appear only twice” also depends on prior counts. Treating that rule as adjacent would produce wrong counts even if the returned sample witness happened to work.

### 2. Define a sufficient memoization state

Choose the smallest state that retains everything future decisions depend on. Position plus previous value is sufficient only when all prefix-dependent rules can be decided from that information. Global counts, used-item sets, resource totals or other history must be included when relevant.

Keep the domain, fixed choices and external context immutable during one solve. A memo table from an earlier problem must not be reused after the user changes a clue unless the cache key includes the complete relevant problem identity.

If a correct compact state cannot be established, use a bounded direct enumeration or report the unsupported rule. Do not omit a constraint merely to keep the dynamic program small.

### 3. Count suffixes and retain one witness

At each state, iterate permitted candidates, restricted to the user's fixed value when present. Reject candidates violating the applicable local or transition rules. Sum the counts returned by valid successor states. A completed valid sequence contributes one; a dead end contributes zero.

Retain a witness only from a successor with a positive count. Record the full suffix, not a partial greedy guess. Memoize the resulting count and witness for the sufficient state.

Check an upper bound on the count before choosing its numeric representation. For example, twelve positions with at most ten choices each have at most 10^12 assignments, within JavaScript's exact integer range. Larger models may require BigInt or an explicitly capped count. “At least N” must not be displayed as an exact total.

### 4. Recheck the witness independently

Run the completed sequence through a separate verifier over the original rules and fixed positions. Confirm its length, domains, endpoints and every required relationship. A positive count with an invalid witness is an implementation error, not a usable hint.

For small cases, compare counts with direct enumeration that does not call the solver's transition helper. Include impossible clues, an already complete solution, multiple solutions and an empty position between fixed neighbors. Test more than the one preferred example.

### 5. Turn a witness into a bounded hint

If completion exists, a hint may fill one requested empty position from a verified witness while leaving all fixed choices unchanged. Explain that this is one feasible option, not necessarily the best-looking or highest-value one.

If no completion exists, distinguish an immediately violated rule from a conflict that only appears when considering later positions. Do not overwrite the user's fixed choices to force a solution. Offer the conflicting evidence or ask which choice may be relaxed when changing it is outside the request.

### 6. Preserve interaction and persistence semantics

Invalidate counts, hints and exports after every problem change. Late asynchronous results must belong to the same problem version before they update the interface. Stop any preview playback or simulation that still refers to an older sequence.

When saving completed sequences, persist the actual choices rather than only a completion badge if the user expects to replay or export them later. Validate restored solutions against the current rule version, clone arrays before editing and retain a clear distinction between a cleared draft and a saved solution.

## Worked example

Use the alphabet {A, B, C} for a sequence of length three. Adjacent symbols may not match, and the final symbol is fixed to A.

The four completions are ABA, ACA, BCA and CBA. Position plus previous symbol is a sufficient state because the only history rule concerns adjacency and the fixed final A is part of the unchanged problem.

If the user fixes the first symbol to B, only BCA remains. A hint for the empty middle position can therefore give C without changing B or A. If the user instead fixes the first two symbols to BB, there are no completions; replacing the second B silently would violate the task.

Direct enumeration of all 27 assignments reproduces the count of four. The same implementation pattern was also checked against independent enumeration for bounded four-position melody fixtures, and every supplied longer puzzle returned a separately validated full witness. Those checks support the tested finite models, not arbitrary history-dependent constraints.

## Failure states and deliverable

- **Invalid input:** name the unsupported value, position or bound
- **No completion:** report zero only after complete search of the declared model
- **Budget exceeded:** return unknown/incomplete, optionally with a verified witness already found; do not imply the count is exact
- **Numeric count limit:** use a suitable exact type or a clearly labeled lower bound
- **Stale result:** discard it without altering the current draft

Return the frozen rules and fixed choices, count or bounded-search status, verified witness and any applied hint. Include the state representation and the reason it is sufficient when another agent will maintain the solver. Keep model feasibility separate from external execution or approval.
