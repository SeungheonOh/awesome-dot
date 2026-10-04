---
name: architect
description: "Design caller-facing types, boundaries, and implementation steps before a consequential code change; compare materially different shapes and document the choice."
---


# Architect

Start with how callers use the feature, then derive types and ownership. The deliverable is a reviewable design, not permission to implement, commit, or publish it. If the user requested design only, stop at the design. If implementation is already authorized, continue within that scope unless they requested a checkpoint.

## Ground the design

Identify the outcome, existing callers, constraints, and exact source revision. Trace the relevant entry points, state ownership, and failure paths. Use the approach in [how](../how/SKILL.md) when the system is unfamiliar; use [why](../why/SKILL.md) when changing an established constraint depends on its history. Neither companion is required for a small self-contained design.

Separate observed constraints from assumptions. Note compatibility promises, latency or scale requirements backed by measurements, and the boundaries you may change. For greenfield work, state the missing integration context rather than inventing it.

## Sketch alternatives

For a consequential choice with more than one viable shape, sketch at least two structurally distinct options. For a mechanical change with a determined interface, explain why a second design would add no information. A storage abstraction versus direct domain operations is a genuine alternative; renaming the same methods is not.

Before expanding a sketch, identify the observation that would select or reject it. Run a cheap compatibility or failure-path probe first when available; if it resolves the choice, record that result instead of producing symmetric designs for their own sake. Retain broader exploration for unresolved consequential choices.

Use independent candidate workers only if available and worthwhile. Give each the same grounding and a separate output location using [the runner brief](references/runner-prompt.md). Otherwise sketch alternatives sequentially and label them as one assistant's exploration. Inherit the host model unless the user chose supported alternatives; multiple candidates do not imply multiple models.

Each sketch contains:

1. Two realistic caller examples, including a failure or interrupted operation
2. Domain types and function signatures derived from those examples
3. A module map naming who owns validation, persistence, policy, and lifecycle
4. Stub bodies or clearly labeled pseudocode, never accidentally executable scaffolding in production
5. The key invariant, a way to test it, and accepted tradeoffs

Read [design red flags](references/design-red-flags.md). Prefer an interface that hides meaningful complexity, not a short interface that pushes coordination onto callers. Trace dominant reads and writes through the chosen data structures. Check repeated calls, partial failure, and concurrent writers where relevant.

## Choose and record

Compare the candidates on the actual constraints. [Arena](../arena/SKILL.md) can organize substantial competing designs; it is optional. Select one base rather than averaging incompatible ownership models. Record accepted ideas, rejected ideas, and reasons in the [rationale](references/rationale-template.md). A disagreement is a reason to inspect an assumption, not a vote to count.

If a missing answer would change a costly or irreversible choice, ask that question and continue independent exploration. An uncertain external contract stays an explicit risk; do not design around a fabricated guarantee.

## Implement only when requested

Start with a vertical slice that exercises the key contract. Replace stubs with behavior and run the contract checks. Surface meaningful deviations: a new parameter may reveal a missed requirement, while repeated casts may reveal the wrong domain model. One edge case does not invalidate a design.

Redesign when several independent changes require the same workaround, callers must understand internal sequencing, supposedly private state needs cross-module locks, or the types repeatedly need escape hatches. Preserve evidence and user work. Re-ground, compare a smaller shape, and seek a decision if the redesign changes scope. Do not erase uncommitted work or silently widen the assignment.

## Hand back

Return the caller examples, chosen sketch, rationale, first bounded implementation step, and unresolved questions. State whether code was only sketched or actually changed, which checks ran on which artifact, and what remains unverified.

Example decision: “Use one repository-owned save operation. Separate validate/write calls let a caller write an unvalidated draft. Keep transport parsing at the HTTP boundary. Next: test one save and one duplicate request through the repository.” This is a design example, not evidence that the project has those APIs.
