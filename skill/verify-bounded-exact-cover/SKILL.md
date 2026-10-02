---
name: verify-bounded-exact-cover
description: "Formulate and verify a bounded exact-cover task with explicit required items, legal candidate rows, fixed choices and honest solved/impossible/incomplete search outcomes."
---

# Verify a Bounded Exact Cover

## When to use

Use this when a user or agent needs to choose combinations that cover every required item exactly once, such as packing a small board or allocating a finite inventory to compatible slots. First establish that exact cover matches the real rules. Optional coverage, repeated capacity, costs and timing may require a different model.

## Required inputs

- A finite universe of required items with stable identifiers
- Legal candidate rows, each naming the required items it covers
- Resource-use rules, such as using every physical piece exactly once
- Fixed choices that must be preserved and any forbidden combinations
- Search budget, expected output and a way to independently validate a candidate solution

A candidate generator is part of the model. Missing legal candidates can produce a false impossibility result even if the search exhausts its generated rows.

## Workflow

1. **Write the coverage contract.** List every required item and its exactly-once meaning. Include resource identity columns when distinct physical resources must each be used once. Do not merge identical-looking pieces if their identities or other constraints matter.
2. **Enumerate legal candidates.** Generate each row from the permitted transformations or assignments. For geometric packing, normalize rotations/reflections, deduplicate equivalent shapes, translate them across the board and reject placements outside the boundary. Reflection is allowed only when the task permits it. Preserve a row-to-original-action mapping.
3. **Validate fixed choices.** Verify they belong to the candidate set, do not overlap required items and do not reuse a resource. Treat a fixed choice as a constraint, not a suggestion that the solver may silently remove. Report invalid input separately from a valid but uncompletable partial plan.
4. **Search the remaining universe.** Choose an uncovered required item, preferably one with the fewest compatible rows. Try each compatible candidate, cover its items, exclude conflicting rows and recurse. Preserve enough history to reverse each trial exactly. If an uncovered item has no compatible row, that branch cannot complete.
5. **Bound computation explicitly.** Count search work consistently and stop at the agreed limit. Return one of three outcomes: a verified solution; exhaustive failure within the specified candidate model; or incomplete search. A timeout or node limit never proves impossibility. Cancel obsolete computations when the user changes the plan, and keep old results from replacing the newer view.
6. **Validate a returned solution independently.** Expand the selected rows and count every required item. Each must appear exactly once; no outside item may appear. Check resource identities and every fixed choice. For geometry, enumerate occupied coordinates independently of the search bitmask to catch indexing or boundary errors.
7. **Turn a solution into an actionable hint if requested.** Offer one unchosen row from a valid completion, with its exact position/transformation or assignment. Keep the user's fixed choices intact. Call it one possible completion unless uniqueness was separately established. If a partial plan is proven impossible, identify that scope and suggest reconsidering a fixed choice rather than declaring the original task unsolvable.
8. **Test the model boundary.** Include a known solution, an independently justified impossible instance, a deliberately tiny budget, malformed fixed choices, duplicated resources and symmetric candidates. Verify that each search status is distinguishable in the UI or report. Where feasible, compare small instances with an independent brute-force enumeration.

## Worked example

Required items are slots A, B, C, D and physical resources P, Q. Candidate rows are:

- P-left covers A, B, P
- P-right covers C, D, P
- Q-left covers A, B, Q
- Q-right covers C, D, Q

Choosing P-left leaves C, D and Q. Q-right completes the exact cover. Independent counts are one for each of A, B, C, D, P and Q.

If P-left and Q-left are both fixed, they overlap A and B. Reject the fixed plan as invalid before search. Do not silently move Q. If only P-left is fixed and Q-right is absent from the permitted candidates, the remaining valid partial plan has no completion in this candidate model. Check whether the missing row is truly forbidden before claiming the real task is impossible.

A search stopped before examining the relevant branch is incomplete, even if no solution has yet been found. A found solution establishes feasibility, not uniqueness or optimality.

## Output and stopping condition

Return the coverage contract, candidate-generation assumptions, fixed choices, search status and work count. For a solution, include the chosen rows and independent coverage check. For exhaustive failure, state the precise finite model exhausted. For incomplete search, preserve the partial evidence without giving an impossibility claim.

Stop when the scoped feasibility or hint result is established. Changing task constraints, applying an allocation in a real system, or expanding the search budget substantially requires the appropriate authority and resources; a model solution is not permission to execute it.
