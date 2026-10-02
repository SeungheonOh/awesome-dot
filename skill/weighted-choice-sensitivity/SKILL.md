---
name: weighted-choice-sensitivity
description: Build a transparent weighted-choice web app with editable criteria, comparable scores, explicit ties, and a sensitivity sweep that shows when changing priorities changes the leader.
---

# Weighted choice sensitivity

Turn an ordinary multi-option choice into an editable comparison whose assumptions remain visible. The worked product is Tradeoff Studio: score options on shared criteria, adjust relative weights, and inspect how the ranking changes as one priority moves.

## Inputs and scope

Identify the options, criteria, intended score direction, source of each score, and publication destination. If the user grants creative discretion, use clearly labeled synthetic options rather than inventing facts about real products. Scores are subjective inputs, not measured probabilities. Do not use this tool to determine eligibility or consequential outcomes for people, or portray it as financial advice.

Keep source and tests in the product workspace. For a skills-only repository contribution, publish only this workflow. Read current repository guidance first, but preserve the user's narrower contribution and service limits. Refresh main before editing and again before pushing.

## Build in this order

1. **Define score semantics before visuals.** Use one bounded scale, such as 0–10 with higher always better. Rename a cost criterion to “Cost fit” and explain that lower expense earns a higher score. Do not mix raw dollars, minutes, and ratings directly in one sum.
2. **Separate a pure comparison model.** Represent each criterion with a name and nonnegative weight, and each option with a name and one score per criterion. Preserve positional or stable identifiers independently of editable names. Duplicate display names must not collapse distinct alternatives in calculations.
3. **Make invalid states explicit.** A blank score is missing, not zero. Require finite scores in range, nonempty bounded names, and matching row lengths. When all weights are zero, show a useful empty result rather than NaN or an arbitrary leader. Disable export of invalid models.
4. **Calculate normalized weighted scores.** For option j, `score[j] = sum(weight[i] * value[j][i]) / sum(weight)`. Keep full precision internally. Round only display values. Multiplying every weight by the same positive constant must leave the ranking unchanged. Find ties using a small numerical tolerance, not rounded text.
5. **Build the editable workspace.** Put priority controls and a score matrix next to the ranked output. Show normalized interpretation without demanding that raw weights sum to 100. Keep every option on the same 0–10 bar scale. Make add/remove controls bounded, give inputs useful accessible names, and keep wide matrices horizontally scrollable on phones.
6. **Add one transparent sensitivity experiment.** Choose a criterion k and sweep its share p from 0 to 100%. Allocate the remaining share across other criteria in their existing proportions. If their weights sum to zero, split that remaining share equally and disclose the convention. Plot each option's score over the sweep and mark the current share. Keep line colors tied to option identity.
7. **Describe sensitivity honestly.** A sampled sweep establishes only what was checked. Say “stays on top across this 1%-step sweep,” rather than claiming robustness to every possible combination of assumptions. Include ties among the leaders. Sensitivity to one weight does not validate the underlying scores.
8. **Complete recovery and handoff.** Reset restores the entire example, including the selected sensitivity criterion. Removing a criterion removes the matching score column and repairs the selected index. Download a structured comparison with its original inputs and computed ranking; use a Blob and revoke the object URL. State whether edits persist. Do not imply a download was saved merely because it was initiated.
9. **Verify, publish, then contribute the method.** Test the model invariants below, inspect the working surface and interaction flows where supported, and verify deployment success before giving a live link. Preserve the authorized audience. Pull current main, inspect a skill-only diff, publish without force-pushing, and verify the remote commit. A continuing creation request remains open after one release.

## Worked numerical example

Criteria weights: cost fit 35, quality 40, convenience 25. Options A, B, C respectively score `[9,6,7]`, `[6,9,6]`, `[7,7,9]`.

- A: 7.30
- B: 7.20
- C: 7.50

C leads by 0.20 under these inputs. At 100% cost-fit share, A leads with 9. At 0% cost-fit share, retain quality:convenience at 40:25; B leads with approximately 7.846. This change is a consequence of the chosen weighting, not new evidence about the options.

## Acceptance criteria

- The example yields C at 7.50, A at 7.30, B at 7.20
- Doubling all weights produces identical results
- Zero weights produce an explicit empty ranking
- Missing, nonfinite, or out-of-range scores are rejected
- Identical score vectors tie before display rounding
- Sensitivity endpoints agree with independent hand calculations
- Zero weights on all other criteria produce finite results using the disclosed equal-share convention
- Adding/removing rows or columns preserves rectangular data and focus validity
- Export retains original inputs, and user-entered names are escaped before HTML rendering
- Keyboard editing, narrow-screen layout, reset, invalid-input recovery, and download behavior are verified in a browser when available

The original build passed numerical checks for baseline ranking, weight scale invariance, zero weights, missing/range validation, ties, sensitivity endpoints, and the zero-other-weight fallback, plus JavaScript syntax checks. Deployment succeeded and a hosting-provided desktop screenshot was inspected. Browser interaction, mobile visual, and optional WebMCP execution validation were unavailable; do not count them as tested. Repeat checks for each implementation.

## Stop or repair

If scores are not comparable, repair the rubric before ranking. If a hard constraint makes an option unacceptable, model that as an explicit eligibility condition for ordinary choices rather than silently burying it in a small weight. Ask the user to resolve contradictory requirements. When publishing or verification fails, retain the local artifact and report the exact unfinished stage; never claim a robust recommendation from unverified assumptions.
