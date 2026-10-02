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

### Keep evidence and preference separate

Assign each criterion a source or an explicit user judgment. When a cost is converted into a higher-is-better score, retain both the original amount and the agreed conversion rule in the working record. A missing score can be handled as an unresolved row or an explicitly requested range; do not impute a point estimate silently.

For sensitivity, state what stays fixed. Varying one weight while preserving all scores answers a preference question. Varying uncertain scores answers an evidence question. Keep those analyses separate, and record ties at crossing points rather than choosing a winner by list order.

## Output

The input matrix and provenance, baseline ranking, ties, sensitivity range and decision-relevant caveats. Leave the final subjective choice with the user.

## Verification and limits

Confirm that scaling every weight by the same positive constant leaves the ranking unchanged. Check endpoints and at least one independently calculated weighted average.

## Example request

“Compare these three options using my scores and weights. Show the baseline and how the leader changes as cost fit varies. Keep missing scores unresolved, and return the assumptions with the ranking.”

## Worked example

The supplied criteria are cost fit, quality and convenience with weights 35, 40, 25. Supplied scores are A=[9, 6, 7], B=[6, 9, 6], C=[7, 7, 9]. All are subjective 0–10 higher-is-better ratings.

The baseline averages are A=7.30, B=7.20 and C=7.50. C leads by 0.20. At 100% cost-fit weight, A leads with 9. At 0% cost fit, distributing the remaining weight in the supplied 40:25 ratio gives B≈7.846, C≈7.769 and A≈6.385.

The handoff says C leads under the current preferences but the leader changes at the explored extremes. It preserves the score sources and does not call C objectively best. If B’s quality score were missing, the baseline ranking would be incomplete until the user supplied it or authorized a range analysis.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
