# Multi-phase or multi-PR plan

Use to produce an executable plan for dependent phases or a stack. Read the [execution contract](../references/execution-contract.md). The plan is the deliverable. Do not start implementation merely because the plan is complete.

## Inputs

User outcome, current repository/artifact, constraints, known consumers, dependency boundaries, desired delivery mode, authority, budget, and evidence already available. A small obvious edit can use a short plan rather than a program template; explain the smaller scope and still honor the requested planning deliverable.

## Steps

1. Inspect the affected structure and current proof. Resolve factual uncertainty with read-only evidence or an already-authorized isolated [Prototype](prototype.md); a planning request does not automatically authorize production changes or new external services. Leave unresolved preference/risk decisions explicit.
2. Divide the target into independently verifiable phases. Name each dependency and writer boundary. A phase should end in a demonstrable consumer outcome or an essential checked prerequisite, not “implement some code”. Identify the first useful integration and final acceptance.
3. Choose execution mode. [Autonomous run](autonomous-run.md) fits one bounded task; [Orchestrate](orchestrate.md) fits a durable program; [Autopilot-full](autopilot-full.md) needs independent items and explicit landing authority; [Autopilot-stack](autopilot-stack.md) delivers an operator-landed chain. Do not assume publication or merge authority from a mode's name.
4. Fill the template below for each phase. Every applicable check names the current candidate, command/scenario, evidence location, and pass predicate. Use real paths and observed commands; mark unknown prerequisites as unresolved rather than inventing them. In a ready-to-execute plan, resolve placeholders and dependency IDs.
5. Scale verification to the change. Unit/static checks, behavioral/live checks, and performance checks serve different claims. A docs-only phase can justify live/perf as not applicable. UI behavior needs real interaction and relevant visual evidence. Performance work needs a metric and meaningful baseline/budget. No universal screenshot count, worker count, or ten-lane requirement applies.
6. Plan evidence invalidation. Every phase records head/base or artifact digest and environment. Final integration needs current-candidate proof, not a collection of green earlier commits. A rebase or dependency change reopens impacted checks; matching patch identity alone is insufficient.
7. Validate syntax, dependencies, links, ownership conflicts, authority gates, and check feasibility. If the optional helper is available, run `node "$DOT_STACK_ROOT/tools/dot-stack.mjs" check-plan <plan-file> --json` after verifying the root. Passing it validates structure, not command truth, host availability, or approval. Manually inspect those limits.
8. Deliver the plan, evidence/unknowns, validation outcome, and exact decisions needed. Stop. Execution requires the user's go and any host-required action approvals.

## Plan template

The following is a structure to fill, not an executable example. Keep **Inputs** and **Phases**, plus one complete block per phase. Replace bracketed text with grounded specifics before treating it as ready.

```markdown
# [Program] plan

[Consumer outcome and bounded scope.]

## Inputs

- Goal: [observable final predicate]
- Repository and starting candidate: [verified identity]
- Constraints and authority: [allowed writes/external actions; operator-held gates]
- Execution mode and owner: [selected playbook, integration owner]
- Budget and stopping conditions: [agreed bounds; blocked/cancelled behavior]
- Persistence: [actual wake capability or session-bound resume plan]

## Phases

## [Verb phrase]

**ID.** phase-one
**Depends on.** None.
**Surface.** cli
**Accept.** [Observable result for the consumer.]

**Files.**
- [ ] [Owned path and intended change; exclude unrelated writes.]

**Build.**
- [ ] [Coherent change with a named contract or symbol.]

**Verify, unit.**
- [ ] Run [actual command] at the phase candidate. Evidence: `[result path]`. Pass when [behavior and expected result].

**Verify, live.**
- [ ] Run [representative consumer scenario] on the current candidate. Evidence: `[output/trace path]`. Pass when [observable predicate].

**Verify, perf.** Not applicable. [Specific reason this phase makes no performance claim and poses no relevant budget risk.]

**Review gate.** [Independent review or operator decision required, who owns it, evidence, and hold point. Or None with a concrete rationale.]

**Delivery.**
- [ ] [Authorized local artifact, PR, stack append, or merge outcome; authority remains separate from evidence.]
- [ ] Bind the final receipt to current head/base or artifact digest and environment. Recheck impacted proof after integration.

## [Next verb phrase]

[Repeat a complete phase block with unique ID, valid dependencies, and actual surface.]

## Close the program

- [ ] Verify the final acceptance predicate on the integrated current candidate.
- [ ] Reconcile active owners, pending actions, and failed/unverified evidence.
- [ ] Deliver the requested result and remaining gates. Retain the resume/decision trail.

## Prototype evidence

[Question, observed result, candidate identity, artifact, limits; or reason none was needed.]

## Alternatives and risks

[Material alternatives, rejected reasons, failure modes, owner, and contingency.]

## Reading and commands

[Verified project instructions, actual supporting skill paths, prerequisites, and boot/check commands.]
```

Allowed surface labels are `docs`, `cli`, `service`, `ui`, and `mixed`. Dependencies use exact phase IDs or `None`. An applicable verification block must state `Evidence:` and `Pass when`. `Not applicable` requires a substantive reason; it cannot excuse the behavior the phase claims. A UI phase cannot mark live verification not applicable. Explicit unresolved prerequisites mean the plan is not yet execution-ready even if other parts are well formed.

## Evidence and completion

Return plan location, ordered phase IDs/dependencies, review/delivery gates, what prototypes established, what remains unverified, and the exact validation command/result. Do not turn placeholders or simulated checks into passing receipts. No prototype, planner, or helper supplies permission to begin the program.
