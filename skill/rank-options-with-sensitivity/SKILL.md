---
name: rank-options-with-sensitivity
description: "Turn supplied options, comparable scores and priority weights into a transparent ranking and a bounded sensitivity analysis."
---

# Rank options and test sensitivity

## When to use

A choice depends on competing priorities and the user wants to understand which assumptions make an option lead.

## Required inputs

- Options and criteria with stable identities
- Score direction, scale and sources; missing values explicitly marked
- Nonnegative priority weights and the uncertainty or priority to vary

## Workflow

1. Check that all scores use a comparable higher-is-better scale. Do not combine raw costs, durations and ratings without an agreed conversion. Keep subjective judgments labeled.
2. Treat missing scores as unknown rather than zero. If weights sum to zero, return no ranking. Do not fabricate missing evidence to complete the matrix.
3. Calculate each weighted average using full precision and identify ties using a numerical tolerance, not rounded display values.
4. Vary the selected priority over a declared grid or solve its crossing points analytically. Reallocate remaining weight in the original proportions; disclose any convention needed when the other weights are all zero.
5. Describe how the leader changes and which assumptions matter. A one-weight sweep is not robustness to all possible score/weight changes. Do not use this workflow to make high-impact eligibility decisions about people.

## Output

The input matrix and provenance, baseline ranking, ties, sensitivity range and decision-relevant caveats. Leave the final subjective choice with the user.

## Verification and limits

Confirm that scaling every weight by the same positive constant leaves the ranking unchanged. Check endpoints and at least one independently calculated weighted average.
