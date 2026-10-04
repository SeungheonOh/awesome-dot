# Autopilot-stack

Use to build and verify an ordered queue as one reviewable base-branch chain for the operator to land. Read the [execution contract](../references/execution-contract.md). No owner or coordinator merges, arms auto-merge, closes, or deploys as part of this playbook.

## Inputs

Ordered outcomes or dependency graph, repository and mainline, allowed publication/topology actions, expected operator review, file boundaries, budget, and final delivery predicate. A request to state a plan is not a go. Start execution only when authorized. If remote publication is not authorized, prepare the equivalent local commits/patches and state the delivery gate.

## Steps

1. Establish one integration owner for the whole chain and one writer per build artifact. Inspect existing branches, PRs, current heads/bases, and active work before assigning ownership. Record intended parent relationships and operator-held decisions explicitly.
2. Run bounded owners using the implementation, evidence, decision-trail, review-triage, and liveness disciplines in [Autopilot-full](autopilot-full.md). Their brief excludes merging. Parallelize genuinely independent building; a dependent owner receives the exact parent candidate and required context.
3. Each owner reports code-ready at a fixed head/base with self-proof and artifacts. The coordinator obtains risk-appropriate independent review of that candidate, gates and real behavior. A missing reviewer or blocked lane stays unverified. Fix rounds include proven findings and fresh candidate-bound evidence, without automatic fixed lane counts.
4. A passing round permits integration planning, not blind reuse of the pre-integration verdict. The sole topology owner appends the change to the intended exact parent tip using authorized branch operations. Only the root targets mainline; each child targets its immediate parent. Verify remote head/base after an authorized push or retarget, and stop on concurrent ownership drift.
5. Revalidate the integrated candidate. Appending or rebasing can change semantics even with an unchanged patch-id. Check the base, dependencies, conflict resolutions, environment, and final diff; rerun affected gates and behavior at the actual stack head/base. Apply [Shipping](shipping.md)'s evidence rules without taking its merge actions.
6. Absorb mainline drift only through the integration owner. Work bottom-up, with responsible owners resolving conflicts in their files. Invalidate impacted receipts and re-review changed behavior before marking the chain deliverable. Never serialize unrelated owners behind unnecessary stack operations, and never let them independently rewrite topology.
7. Keep requested review gates visible. For an interaction change that needs operator approval, provide actual screenshots or a short capture from the current candidate. Non-UI changes provide their appropriate behavioral receipts. A static image alone does not prove interaction, and a branch-safe verdict is not product acceptance.
8. Deliver one verified linear chain in the intended order. Read back each PR's repository, parent/base, head, readiness, and relevant review/check state. Verify links and attach or reference only authorized evidence. Report any root/mainline movement that affects current readiness.

## Hold, recovery, and boundaries

Stop scheduling on the user's hold and propagate a no-new-writes order. Reconcile in-flight owners and save resume state. If a topology request times out, query the remote state before retrying. If a parent disappears or closes, hold dependent mutation and reconcile; do not retarget all descendants speculatively. A late worker's result is compared with the current chain and owner generation before use.

Live status and waits must use actual host capabilities. If the session cannot persist, save the chain identities, outstanding checks, owners, and next action; do not claim a future autonomous wake.

## Evidence and completion

Return verified root and tip links when published, bottom-to-top order with parent/head and per-link evidence status, operator review gates, and any excluded or blocked items. Completion is a current reviewable chain, not a merge. A later instruction to land starts [Shipping](shipping.md) with fresh state and authority.
