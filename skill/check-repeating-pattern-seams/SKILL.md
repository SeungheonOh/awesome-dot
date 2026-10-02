---
name: check-repeating-pattern-seams
description: "Measure consecutive runs across the boundary of a repeating sequence or grid, distinguish finite runs from an unbroken repeated cycle, and verify the result with a separate exhaustive oracle."
---

# Check repeating-pattern seams

## When to use

Use this when a pattern repeats and a run-length limit, gap or continuity check must include the join between its last and first elements. Examples include weaving interlacement, tiled binary masks, cyclic work/rest plans and discrete looping event patterns.

The outcome is an explicit boundary-aware measurement and its meaning for the chosen domain. This does not automatically establish visual smoothness, audio continuity, safe workloads or material quality; those depend on additional properties.

## Required inputs

- The finite sequence or grid representing one repeat
- Which states or predicate count as the run being measured
- Whether the boundary is open, cyclic or joined to a different neighboring pattern
- Axis, traversal order and coordinate convention for a grid
- The intended interpretation of a cycle containing no interruption
- Limits on dimensions and any domain-specific acceptable run length

Do not assume that a preview image repeats merely because it is rectangular. An open-ended strip and a seamless tile need different boundary conditions.

## Workflow

### 1. Separate the structural state from its appearance

Derive the Boolean or categorical sequence from the authoritative model. Similar colors do not necessarily represent the same structural state. In a woven drawdown, for example, changing yarn colors must not change which yarn crosses above the other.

Check dimensions and allowed states before allocating or scanning. Reject an empty sequence unless the caller explicitly defines its meaning. For a two-dimensional grid, decide which rows or columns represent each physical direction; preserve that mapping in the report.

### 2. Define what happens at the join

For a cyclic sequence, index after the last element wraps to the first. A run at the end can join a run at the start. For a non-cyclic sequence, keep those runs separate.

If every element satisfies the predicate, distinguish two questions: within the finite displayed cycle the run has length n; under indefinite repetition it has no interruption. Use an explicit sentinel or labeled unbounded result for the latter, rather than reporting a reassuring finite maximum.

If no element satisfies the predicate, its longest run is zero. Keep this separate from empty input, unknown state and an unbroken cycle.

### 3. Measure a bounded number of elements

For a nonconstant cyclic sequence of length n, scanning two copies is sufficient to see every boundary-crossing run. Increment a counter when the predicate holds, reset it otherwise and track the maximum. Because at least one element breaks the run, the maximum is below n.

Another valid method combines the prefix and suffix runs with the longest interior run. Whichever method is used, handle the all-matching case separately and avoid accidentally adding the same uninterrupted cycle to itself.

For a grid, apply the chosen sequence operation to the relevant rows and columns. When reporting the worst case, preserve an unbounded result from any line; do not coerce a sentinel to zero or let an ordinary numeric maximum hide it.

### 4. Verify with a structurally different oracle

For small sequences, start at every index and count matching elements modulo n until the first mismatch or n steps. The largest count is the reference result. A count of n means the repeating sequence never breaks.

Exhaustively enumerate all binary patterns for several small lengths and test both state values. Include alternating states, an isolated matching cell, long matching prefixes/suffixes, all matching, none matching and rotations of the same sequence. Rotation must not change a cyclic maximum.

Do not use the production helper inside the oracle. For larger inputs, supplement with generated cases and metamorphic checks, but retain the small exhaustive suite as a regression.

### 5. Present the measurement without exceeding it

Name the boundary mode, state, axis and units of the count. Show the offending location or a small witness when useful. Apply a threshold only when it comes from the user's task or a relevant domain rule.

In a weaving sketch, a long structural float does not alone determine fabric quality: yarn, sett, tension and finishing still matter. In a repeating schedule, an unbroken active run is a structural fact, not by itself a medical or staffing recommendation.

## Worked example

One cycle is [true, true, false, true]. Looking only from left to right gives a longest true run of two. Repeating it joins the final true to the first two true values, producing a run of three. The false run is one.

For [true, true, true, true], the displayed cycle has four true elements, but indefinite repetition has no false interruption. Report the repeated true run as unbroken, rather than four or eight. The longest false run is zero.

## Executed example and limits

A discrete-pattern implementation was checked with all 2,044 binary sequences of lengths two through ten, for both true and false. The two-copy implementation matched an independent start-at-every-index oracle in all 4,088 comparisons. Additional plain-weave and generated-grid cases checked the row/column mapping used to report four front/back run measurements.

An exported vector drawdown was rendered and visually inspected separately. That image check did not establish physical fabric behavior or real-browser layout. Keep structural, visual and physical evidence separate when applying this workflow elsewhere.
