---
name: compare-integer-apportionment
description: Compare whole-unit proportional allocation rules for fixed group weights, explaining exact ties, quota bounds and changes when the total allocation changes. Use for apportionment-method comparisons rather than optimizing a supplied cost objective or applying legal election rules.
---

# Compare Integer Apportionment

Return each requested rule's allocation under the same weights and total, with the rounding and tie decisions that explain differences. Do not label one method objectively fairest without the user's chosen criterion. For a cost or benefit optimum subject to resource constraints, use `solve-constrained-optimization` instead.

## Fix the model before comparing

Identify groups with distinct stable labels, nonnegative weights and the whole-unit total. Confirm how zero weights, minimum guarantees, eligibility thresholds and exact ties should work when those choices matter. A method starting every group at zero is different from one guaranteeing each group an initial unit. If the task concerns an actual election or legal allocation, obtain its current governing rules; a mathematical example is not a jurisdiction-specific calculator.

Keep weights unchanged when testing the effect of total size. Changing weights, membership or tie priority at the same time answers a different question. Preserve identifiers and input precision; converting a large integer to a floating-point number can erase a consequential difference.

## Compute only the requested rules

For Hamilton/largest remainder, compute each exact quota as total units times group weight divided by total weight. Allocate floors, then give the remaining units to the largest fractional remainders. With a common denominator, compare integer remainder numerators directly.

For zero-minimum Jefferson/D'Hondt, repeatedly award the next unit to the largest weight divided by its current allocation plus one. For zero-minimum Webster/Sainte-Laguë, use the odd divisors one, three, five and so on. These variants are distinct from modified divisors or guaranteed-minimum systems. [Census Bureau method descriptions](https://www.census.gov/about/history/historical-censuses-and-surveys/census-programs-surveys/decennial-census/methods.html) provide background; retain any additional rules supplied for the actual task.

Compare rational priorities by exact cross-products when integral inputs permit it. Keep equal priorities equal. Apply a stated deterministic or authorized random tie rule, and disclose the tied candidates and winner where it changes an award. Alphabetical order or row order is a policy choice, not mathematical evidence that the winner deserves preference. Do not silently break near-ties using display rounding.

## Explain changes with checkable evidence

Verify nonnegative integer allocations and the exact total. Show each group's before/after allocation and difference when comparing totals. A quota violation means an allocation falls outside the floor and ceiling of its exact proportional quota; it is separate from a loss when the total grows. Neither property alone settles all fairness questions.

A synthetic fixed-weight example is 1500, 1500, 900, 500, 500, 200. Hamilton with 25 units gives 7, 7, 4, 3, 3, 1; with 26 it gives 8, 8, 5, 2, 2, 1. The two 500-weight groups lose a unit while the total grows. Label this a loss-on-increase counterexample, not an implementation failure or a claim about real groups. Do not report that test as applicable when the compared total stayed equal or decreased.

For independent verification, compare a sequential divisor implementation with selection from a complete bounded list of rational priorities. Test exact ties, input reordering under the tie rule, scaling all weights by a common factor, a known counterexample, and weights that differ beyond floating-point precision. A worked implementation passed 500 seeded comparisons, the example above, exact 10^18 near-ties and total/boundary checks. Its source and simulated-DOM checks do not establish legal correctness or real-browser layout.

If producing a chart, use a shared scale for both totals and label the method, tie rule and minimum guarantee. Retain exact figures and enough calculation evidence in a reusable export; a rounded chart alone cannot explain a disputed award. Reopen exported results and verify that the method, weights, totals and identifiers match. Calculating an allocation does not authorize applying it to an external system.

When explaining an award sequence, preserve the initial phase: Hamilton’s floors are already allocated before remainder awards begin, while zero-minimum divisor methods begin with no units assigned. Reconstruct each frame from immutable inputs and the award prefix. Show exact priorities and eligibility before the next award; a group that already received a Hamilton remainder cannot receive a second one. Check that each step adds exactly one unit, the chosen priority is maximal under the tie rule, backward replay restores the prior frame, and the final frame agrees with the saved allocation. A worked replay checked 12,487 frames plus stale-control and terminal-state interactions.

For an independently checked saved allocation, reconstruct source groups and require the declared minimum and tie policies before evaluating results. A divisor checker can rank the complete bounded priority list rather than calling the original sequential allocator; Hamilton can independently sort exact remainders. Reject changed sources, missing or duplicate methods, mismatched totals and award vectors inconsistent with the tie policy. State whether saved quota, tie and replay annotations are checked too; a correct final vector does not validate all attached commentary. A worked verifier checked 150 generated reports, altered-source/policy/vector cases and the declared maximum dimensions.

For a bounded total-size sensitivity scan, hold weights, membership and tie priority fixed and compare each adjacent total explicitly. Report the checked interval and any actual losing groups with before/after counts. No loss in a finite interval is not a general monotonicity proof. Keep progress separate from a completed result, allow cancellation for repeated calculations, and invalidate partial or late output after edits or replacement runs. A worked scan checked 380 generated transitions against direct allocation differences, a known loss case, progress bounds and cancellation/error races.
