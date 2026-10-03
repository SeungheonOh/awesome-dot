# Autonomous run

Use for one task the user wants driven to a checkable result. Read the [execution contract](../references/execution-contract.md). Sustained effort does not enlarge the permitted outcome.

## Inputs

A predicate that can be checked, authorized target and actions, acceptance evidence, ownership, limits the user imposed, and any decision/approval gates. “Keep going” changes persistence, not permission to publish, spend, change credentials, delete data, or broaden the project.

## Steps

1. State the done predicate before the first iteration. Examples are the original reproduction passing plus regression gates, a specified benchmark target within guardrails, or an authorized PR confirmed merged. Do not replace the user's outcome with an easier intermediate milestone.
2. Select the smallest implementation playbook and identify a supported observation mechanism. Prefer real events when exposed; otherwise use a reasonable session-bound wait sized to the external process. Do not claim a scheduler, durable goal, or future wake unless it actually exists and was verified.
3. Work in coherent verifiable increments. Each iteration examines current state, chooses an evidence-supported action, runs relevant checks, and records how the predicate moved. Keep useful changes and remove only owned refuted experiments. A growing pile of untested patches is not progress.
4. Diagnose recoverable failures within scope. A verifier defect that blocks the outcome may need a bounded repair; unrelated bugs, attractive refactors, new products, and automation setup are parked rather than absorbed automatically. Record an out-of-scope discovery and continue independent authorized work.
5. Checkpoint after material changes and before waits or handoff. Preserve intent, candidate identity, decisions, evidence, pending processes, owner IDs, next check, and any external action that may have completed despite a timeout. Use [show-me-your-work](../../show-me-your-work/SKILL.md) when a durable decision trail is useful.
6. Reassess the mechanism when attempts stall. Reproduce under tighter conditions, inspect missing data, split the task, or use a bounded alternate approach. Repeated identical retries without new evidence should stop in favor of diagnosis. Never lower the acceptance bar to call the task complete.

## Stop and resume

Continue until the requested predicate is verified or the user cancels/replaces it. Respect agreed time/cost bounds. A real permission/access/information gate pauses only dependent work; ask the precise question and retain the pending state. If useful progress is impossible after diagnosis, give the exact dead end and remaining options. If the host cannot persist through an external wait, preserve a [Pause safely](pause-safely.md) checkpoint and state the limitation instead of promising an unattended run.

An unchanged pending result is not completion of an explicit monitoring request. A vague autonomy request is also not an infinite mandate to invent more work after the predicate is met.

## Evidence and completion

Return the predicate, its final evidence-backed state, important iterations, accepted/discarded work, current artifact, and any specific gate. Distinguish implemented, verified, published, queued, and merged. Stop when the authorized outcome is established.
