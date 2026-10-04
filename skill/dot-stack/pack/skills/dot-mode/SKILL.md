---
name: dot-mode
description: "Route engineering work to a scoped playbook for investigation, implementation, verification, PR operations, or safe continuation. Use when asked for dot-mode or a disciplined end-to-end engineering workflow."
---

# dot-mode

Choose the smallest workflow that can establish the requested result. Read the chosen playbook and [execution contract](references/execution-contract.md) before acting, reusing unchanged material already in context. The contract gates further reads on missing procedural information and relevant tool/version compatibility. Use available tools honestly on ChatGPT, Codex, Claude, or an instruction-only host. This skill changes neither permissions nor the host's capabilities.

## Start with intent

1. Establish outcome, target, scope, authority, and stopping condition. Resolve an ambiguity only if it changes a consequential choice; otherwise state a reasonable narrow interpretation.
2. Distinguish explanation, plan, status, review, implementation, monitoring, and delivery. A status question stays a snapshot. A review does not become a fix. A plan does not start execution. Opening a PR is an optional authorized workflow, never the automatic ending of every task.
3. Inspect the current artifacts and relevant project instructions. Read and apply optional project `.dot-stack/config.json` under the execution contract before role selection, delegation, or artifact creation; preserve and surface invalid settings rather than ignoring them. For code, name the data shape and invariant before adding logic. For an uncertain factual choice, use a cheap authorized observation or isolated experiment; ask the user about genuine preferences, risk acceptance, or unavailable information.
4. Select a route below. For substantial work, keep a short task plan including prerequisites, independent work, shared mutable state, and verification. Adapt steps to the task; record a reason for omitted material gates instead of mechanically copying a long checklist.
5. Execute, review the integrated artifact, and report candidate-bound evidence. Use the contract's verified, failed, unverified, and blocked labels accurately.

Casual conversation, a simple factual answer, and an explicit opt-out need no engineering ceremony.

## Routes

- [Investigation](playbooks/investigation.md): explain how or why, evaluate an approach, or review supplied code without changing it
- [Bug fix](playbooks/bug-fix.md): reproduce a defect, establish its mechanism, and verify a correction
- [Perf issue](playbooks/perf-issue.md): diagnose and improve a specific measured slowdown
- [Hillclimb](playbooks/hillclimb.md): run bounded iterative experiments against one metric and correctness guardrails
- [Runtime forensics](playbooks/runtime-forensics.md): diagnose a live runtime symptom with permitted instrumentation
- [Trace forensics](playbooks/trace-forensics.md): analyze a supplied fixed capture without changing the running system
- [Feature](playbooks/feature.md): implement new or changed behavior with explicit acceptance criteria
- [Refactoring](playbooks/refactoring.md): change structure while preserving a pinned behavior contract
- [Prototype](playbooks/prototype.md): build a disposable instrument to answer a design or empirical question
- [Visual parity](playbooks/visual-parity.md): preserve an approved visual baseline under controlled rendering conditions
- [Authoring a skill](playbooks/authoring-a-skill.md): create or revise actionable portable skill instructions
- [Eval](playbooks/eval.md): measure a workflow or prompt change with controlled, blinded evidence
- [Babysit](playbooks/babysit.md): snapshot PR status, triage requested comments, or monitor/fix toward merge-ready within explicit scope
- [Shipping](playbooks/shipping.md): independently verify and land an explicitly authorized PR or contiguous stack
- [Autonomous run](playbooks/autonomous-run.md): sustain one authorized task until its checkable outcome or a real gate
- [Orchestrate](playbooks/orchestrate.md): coordinate a durable multi-unit program with ownership, dependencies, and evidence
- [Autopilot-full](playbooks/autopilot-full.md): let bounded owners build independent PRs through authorized merges with independent gates
- [Autopilot-stack](playbooks/autopilot-stack.md): build and verify a linear reviewable stack for the operator to land
- [Session pickup](playbooks/session-pickup.md): reconcile a supplied handoff and current artifacts, then resume only remaining work
- [Pause safely](playbooks/pause-safely.md): stop scheduling, reconcile active work, and preserve a usable resume point
- [Multi-phase plan](playbooks/multi-phase-plan.md): produce an executable plan with dependencies and proportional verification, then stop
- [Worktree cleanup](playbooks/worktree-cleanup.md): audit local worktrees and optional simulator state, then remove only an authorized verified set
- [Opening a PR](playbooks/opening-a-pr.md): prepare and publish a specifically requested reviewable change

A large change with no suitable route can use [figure-it-out](../figure-it-out/SKILL.md) to design one bounded workflow. Program size alone does not justify a hierarchy of coordinators.

## Supporting skills, when they earn their cost

Use [how](../how/SKILL.md) for an unfamiliar subsystem and [why](../why/SKILL.md) for historical motivation. Use [architect](../architect/SKILL.md) when a meaningful contract or structural choice needs exploration, [arena](../arena/SKILL.md) for competing implementations, [swarm](../swarm/SKILL.md) for complementary coverage, and [interrogate](../interrogate/SKILL.md) for a contested material decision. Crossing a function boundary alone does not require a panel.

Use [tdd](../tdd/SKILL.md) when a cheap behavioral test can pin the change. Use [no-comments](../no-comments/SKILL.md) to assess redundant commentary while protecting necessary contracts and legal notices. Use [technical-writing](../technical-writing/SKILL.md) for project prose and [unslop](../unslop/SKILL.md) for clarity. Use [show-me-your-work](../show-me-your-work/SKILL.md) for decisions that must survive a long run, not for routine narration. Read [review triage](references/review-triage.md) before acting on human or automated findings.

[setup-dot-stack](../setup-dot-stack/SKILL.md) optionally records project-local concurrency, evidence, and observed role preferences. Apply an existing valid configuration using the execution contract; otherwise inherit the host model by default. Never require a companion plugin, a particular model, a global rule, or an unavailable agent interface.

## Principles

Read a principle only when it changes a concrete decision. Read a known leaf directly; use the [principle index](../../docs/guide/08-principles.md) only when choosing among leaves. Do not load the index, every principle, or repeated host advice by default; reciting principle names is not evidence.

## Completion

Lead with the result and its effect on the consumer and maintainer. Include important choices, exact verification coverage, failures or gaps, and the remaining decision if any. Small work needs a short reply. Long work needs a durable artifact plus a concise summary. No PR, merge, deployment, independent review, successful test, or future wake may be claimed without corresponding evidence.
