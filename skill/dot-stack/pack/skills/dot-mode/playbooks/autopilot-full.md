# Autopilot-full

Use for an explicitly authorized queue of independent changes whose owners carry work through landing. Read the [execution contract](../references/execution-contract.md). The coordinator owns acceptance and oversight; one owner owns each PR lifecycle. For a coordinator-landed standing program use [Orchestrate](orchestrate.md). For operator landing use [Autopilot-stack](autopilot-stack.md).

## Inputs and authority

Resolve the item list, intended repository/base, independent versus dependent items, writable boundaries, allowed external actions, merge method, operator-held items, budget, and finish predicate. A request to explain the protocol means state it and stop. Execution requires the user's go. “Autopilot” does not erase host approval requirements or authorize new scope.

Record what each owner may build, commit, publish, reply to, rebase, or merge. If only implementation is authorized, perform that portion and hold publication/landing. A coordinator's clean verdict is an evidence gate, not a substitute for user authority or forge policy.

## Steps

1. Establish current state and exclusive ownership. Resolve the forge through an authorized read, inventory existing branches/PRs, and check for active owners. Assign independent items disjoint worktrees/branches. Coupled changes follow dependencies; do not pretend overlapping edits are independent because they have different PR numbers.
2. Give each owner the bounded lifecycle. It reads the project contract, implements coherent slices, preserves a decision trail, runs self-proof, prepares authorized publication, triages requested review findings, and reports a code-ready candidate. A PR is opened when publication is authorized and its draft/ready state is appropriate, not on an arbitrary timer or obligatorily before proof.
3. Record owner and child IDs, scope, input/head/base, meaningful milestones, state, and artifact paths. Keep decision records durable in the project/run area, with no secrets. The coordinator audits all active work through supported status and receipts; it does not rely on a memorized wake cadence.
4. At code-ready, freeze a review round to the candidate identity. Assign risk-appropriate independent verification: applicable project gates, load-bearing behavior through the actual surface, and focused diff review. Use complementary lanes when they add coverage; no fixed worker quota or UI driver is required for non-UI changes. If independent review is unavailable, the round remains unverified rather than being relabeled self-review.
5. Include a baseline comparison where it matters. Run the same behavior on base and candidate; if the feature is new, record that the base lacks it and verify the added contract and requested end state. Performance ratios require comparable scenarios; otherwise use justified absolute budgets.
6. Reconcile every finding against evidence and send one coherent fix brief to the owner. A demonstrated defect remains a blocker even if a lane called it a note. Ask for a regression test or reproducible receipt, including other sites sharing the mechanism. New substantive changes create a fresh review round; reuse only demonstrably unaffected evidence under [Shipping](shipping.md).
7. Owners separately report merge-ready with current head/base, self-proof, check/review state, and independent verdict coverage. Reconcile drift before landing through the authorized topology owner. A rebase requires current remote concurrency checks and fresh integration-sensitive proof; never force-push shared history or silently bypass lease conflicts.
8. On the current round's clean evidence and valid landing authority, the owner follows [Shipping](shipping.md) for its own PR, including its atomic expected-head/current-base landing gate. A read-then-merge or delayed auto-merge that can silently land another candidate is not sufficient. Confirm the actual remote merge and target integration before taking the next item. Operator-held items stop at merge-ready. No owner may treat a reviewer response, local ledger, or another agent's approval as a new permission grant.
9. After each merge, inspect the affected integration state within the agreed program scope. Newly surfaced regression findings are triaged against the actual landed artifact. Complete any requested post-merge checks; do not create an unlimited watch or unrelated repair program.

## Liveness and hold

Set milestone expectations by task type and observed runtime. Long tests or waiting CI may legitimately produce no new commits. On suspected stall, inspect live state and latest evidence, then narrow, retry safely, or replace. Confirm stop/ownership transfer before a replacement writes. A failed lane is missing proof, not a pass; account for it in the next round.

Use real host events or supported session-bound waits. Persist a resumable record if durable observation is unavailable. On the user's stop, send a no-new-writes hold to every owner immediately and reconcile pending external actions. Do not infer cancellation succeeded.

## Evidence and completion

Report queue item, owner, state, current candidate, review round and verdict, what actually merged, operator-held gates, and trail location. Close only when every requested item reaches its authorized outcome and active children/pending actions are accounted for. Explicitly identify partial, failed, or blocked items rather than filling the queue with new work.
