# Lead judgment

Decide which findings matter. Do not merely count reviewers or automatically favor the coordinator's original implementation.

## Verify before categorizing

Read the cited location at the reviewed revision. Trace the proposed failure through real callers and defenses. Reproduce it when a cheap safe check exists. Distinguish an impossible typed state from an external input that bypasses those types. A null test is irrelevant only after the boundary and all relevant callers have been established.

Compare against the actual user goal, migration plan, compatibility requirements, and known temporary scaffolding. A reviewer may lack context; supply the missing artifact rather than dismissing the concern by authority. Current conventions can themselves be defective, so “the codebase does this elsewhere” is context, not a refutation.

## Assess importance and certainty separately

A single supported security or data-loss finding deserves attention. Several reviewers repeating one unsupported assumption do not establish it. Repeated independent reproduction is stronger than repeated wording. Keep high-impact uncertain paths as explicit risks with a discriminating check; avoid presenting them as proved defects.

“An interface would look nicer” is preference unless it resolves a concrete caller burden. “This edit creates two owners of deletion policy and they already disagree” is a structural finding. A suggested extraction needs to reduce understanding or change cost, not satisfy a line-count rule.

## Record the decision

Use Act on, Consider, Noted, or Dismissed with one clear reason and an evidence pointer. Merge duplicates without losing independent evidence. Do not cap the number of real defects to make the report look tidy. Group related failures under a root cause where that helps actionability.

Mention missing reviewers, stale revisions, unrun tests, and unresolved contradictions. Do not approve a required check that never returned. The final verdict applies only to the inspected artifact and stated coverage, not to future edits or deployment outcomes.
