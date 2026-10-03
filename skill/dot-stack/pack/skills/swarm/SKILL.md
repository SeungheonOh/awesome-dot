---
name: swarm
description: "Partition a substantial task or compare parallel attempts with explicit ownership, input identity, completion rules, and evidence-based aggregation."
---


# Swarm

Use parallel work only when independent slices or candidate attempts justify its cost. A swarm is coordinated work, not a promise of unlimited workers, durable execution, or multiple models. For a small task, finish it directly.

## Frame the work

State the outcome, exact source revisions or input identities, allowed reads/writes, and acceptance checks. Choose one shape:

- Coverage: workers own distinct slices, and every required slice needs a result
- Race: workers attempt the same outcome independently
- Mixed: separate coverage groups each compare alternatives

For a race, choose the stopping rule before launch: first candidate that passes the full predicate, rank every complete candidate, or best-of with explicit comparison criteria. A fast self-reported pass does not win. For measurements, specify sample unit, sample count, ordering, environment, and method so results are comparable.

Use the actual host's concurrency and worker interfaces. A configured count is a ceiling, not permission to create more environments or spend unbounded resources. Inherit the model unless the user requested supported alternatives. If native delegation is unavailable, execute slices sequentially and disclose that independence was not obtained.

## Assign ownership

Give every worker a self-contained brief: goal, exact slice, input identity, relevant context, permitted paths/actions, output artifact, checks, and stop conditions. One writer owns each file or isolated worktree. Shared files need an integration owner; never rely on workers “being careful” while they edit the same path.

Keep authority bounded. Local filesystem access does not authorize external posts, credential use, publication, or deployment. A worker denial stops that dependent action, not an attempt through another transport.

## Track and integrate

Retrieve terminal outputs. Workers return Verified, Failed, Unverified, or Blocked with artifacts and commands. Read the artifacts, not only the report. Reject a measurement missing the specified revision or method; clarify and rerun within scope when useful. If the evidence still cannot be obtained, keep the slice as a gap.

When a worker fails, diagnose the real blocker and continue independent slices. A dropout is not a pass. For a first-pass race, verify the winning artifact, then cancel unneeded workers if supported and account for their state. If cancellation is unavailable, say so; do not claim they stopped. Do not leave unowned background mutations running.

Integrate through one owner. Candidate success does not prove the combined artifact works. Rerun checks sensitive to integration, shared interfaces, or final revision. Reconcile disagreements against source and behavior rather than votes.

## Report

Return one consolidated result: final artifact, per-slice status, concrete issues, missing coverage, revisions/methods used, and race rule if applicable. Say whether the work was independent, model-diverse, or sequential. Do not paste raw worker logs or claim the swarm completed while a required slice remains pending.
