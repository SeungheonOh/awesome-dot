# Orchestrate

Use for a genuinely multi-unit program that needs durable ownership, dependency management, and integration across sessions. A task one owner can finish within the session usually fits [Autonomous run](autonomous-run.md). Read the [execution contract](../references/execution-contract.md).

## Inputs and outcome

Define the countable authorized result, unit inventory, dependency graph, delivery boundary, project/repository identity, standing constraints, available workers/environments, resource budget, and operator-held decisions. “Complete the program” may mean verified local artifacts, a reviewable stack, or authorized merges; do not silently choose the most consequential version.

The coordinator owns briefs, state reconciliation, integration decisions, and reporting. Workers own bounded artifacts. A verifier independently examines a candidate when risk or a stated gate requires it. Add a sub-coordinator only if a real track is too large to manage in one drain; no fixed depth, worker count, or cloud placement is assumed. Choose environments by actual access and task needs.

## Durable state and ownership

Use a project-owned run directory, by default `.dot-stack/state/default`, outside the installed pack. The optional bookkeeping command is `node "$DOT_STACK_ROOT/tools/dot-stack.mjs" orch --store <run-directory> <command>` after verifying the root and current command help. The CLI records facts; it does not spawn, wait, schedule, grant approval, or merge.

Bind the store to repository, objective/scope, candidate generation, and coordinator owner before using it. Reusing a path does not make its old run current. Keep standing constraints, unit rows, branch/PR/head identities, dependency/frontier graph, verification receipts, decisions, open gates, and a derived status view. One writer owns each record or mutation domain. Keep transient state out of commits unless an auditable record was requested.

`orch init` initializes bookkeeping. Unit commands add/update work, ledger commands record/check proof, inbox commands queue completion pointers, and status derives a view. Frontier input is explicit: `orch frontier set --graph <graph-file>`, optionally restricted by `--prs <numbers>`. Build that graph from verified current forge/ref facts; do not infer it from branch naming or a proprietary stack registry. Inspect the actual JSON schema/help before writing input.

## Brief contract

Every worker receives:

- Goal and why this unit contributes to the user's outcome
- Immutable input/base identity, dependency findings, and relevant source pointers
- Writable paths/worktree/branch, forbidden paths/actions, and exclusive owner generation
- Acceptance predicates, exact available checks or procedures, and required evidence
- Resource/attempt limits and stop conditions, including hold propagation
- Report shape: status, candidate identity, artifact, checks actually run, findings, gaps, and next dependency
- Current user constraints and action authority, without secrets or irrelevant private context

Collapse this to a paragraph for a small unit. A vague missing dependency is a scoping defect to fix before spawning. Resume or replacement briefs consolidate current requirements instead of assuming an old interrupted worker retained them. Relay necessary upstream findings; sibling access is never assumed.

## Steps

1. **Frame.** Partition by independently verifiable outcomes and exclusive writes. State done, budget, tracks, dependency order, integration owner, and the delivery gate. If hierarchy and bookkeeping cost more than the work, collapse to one owner with inline verification.
2. **Initialize.** Inspect existing run/owner state and reconcile any active writers. Create the store only in an authorized location. Record standing constraints, graph, gates, and decision trail. If no helper exists, maintain equivalent small plain records; label unsupported state automation honestly.
3. **Pilot.** Run a representative unit through brief, build, proof, and the authorized delivery boundary. Test whether the brief, evidence recipe, and unit size work. A cheap repeated task needs only a cheap representative pilot. Do not require a real merge if the program stops at local verification or a reviewable stack.
4. **Scale.** Admit a rolling window of ready units within observed host capacity and user budget. Refill as results arrive; avoid waiting for the slowest member of an arbitrary batch. Parallelize disjoint artifacts and serialize unavoidable shared integration. Audit a sampled brief and stop expansion if its missing requirements would multiply errors.
5. **Drain.** Queue completion pointers with the unit/owner/generation and report location. At a safe boundary, claim a batch with `orch inbox drain`, reconcile each event idempotently, persist its unit and ledger effects, then acknowledge that batch with `orch inbox ack <batch>`. A crash before acknowledgement can replay it; record event identity to avoid duplicate side effects. Do not acknowledge before durable effects exist. Unknown/late owners become reconciliation work, never automatic integration.
6. **Integrate.** Review or assign review of finished artifacts outside the bookkeeping critical section. Integrate verified units continuously where authorized, rather than leaving everything until the end. One designated owner controls each stack's topology. A conflict becomes a scoped repair for the responsible owner. Worker completion is neither accepted integration nor merge permission.
7. **Verify.** Bind each ledger receipt to unit, base/head or content identity, check, environment, reviewer, and result. A cheap low-risk unit may use worker proof plus coordinator spot checks. Expensive, high-consequence, or explicitly independent gates require a separate verifier. Typecheck-only cannot prove behavioral correctness; blocked/missing receipts cannot pass. Refresh affected proof after integration or graph changes.
8. **Deliver.** For an authorized stack, advance only the contiguous verified frontier and follow [Shipping](shipping.md), including its atomic reviewed-head and current-base integration gates. A stored ledger pass cannot authorize landing a later head. For a reviewable stack use [Autopilot-stack](autopilot-stack.md). A local-artifact program stops at its own verified output. Check current graph generation before every topology action, record the observed result, then recompute from remote state.
9. **Close.** Drain final events, reconcile every spawned owner to done, held, cancelled, failed, or explicitly superseded, and establish the predicate on the final artifact. Account for uncertain processes rather than declaring them gone. Preserve the store and receipts. Report incomplete units and gates honestly.

## Liveness, retries, and pause

Use supported read-only status, process state, checks, and artifact receipts to distinguish working, waiting, and stuck. Lack of a commit alone does not prove a reasoning or long-test worker is dead. Set expected milestones appropriate to the job. On missed milestones, inspect and ask for status before replacing; revoke/isolate the old writer first.

Retry a recoverable tool/network failure only after inspecting its cause and possible side effects. For memory/resource failure, shrink scope. For an unknown failure, one diagnostic retry may help; repeated identical failures need a revised plan or a gate. A new model is not an automatic cure for a broken tool. A late result is accepted only after comparison with current ownership, head, and ledger; salvage unique findings through a fresh bounded unit.

The coordinator can use native events or a verified scheduler for useful checkpoints. A subprocess timer cannot revive an ended conversation. Choose cadence from expected progress and risk rather than a fixed ritual. If durable wake is unavailable, maintain session-bound observation or hand off resumable state. Do not create a fake persistent program.

On stop, freeze admission and propagate a no-new-writes hold immediately. Reconcile in-flight work and save [Pause safely](pause-safely.md) state. On restart, use [Session pickup](session-pickup.md): check live remote workers, reread constraints, verify store identity, recompute graph, recover unacknowledged events, and resume only missing work. Never clear a lock merely because a process ID looks unfamiliar on another host.

## Scope and report

Fix within-scope blockers, park unrelated discoveries, and ask only when a real decision or permission is needed. Approval gates remain visible while independent authorized units continue. Report counts from actual records, delivered units, current frontier/candidate identities, evidence coverage, abandoned/superseded work, live holds, and artifact/trail locations. Do not claim a requested merge or a durable wake based solely on stored intentions.
