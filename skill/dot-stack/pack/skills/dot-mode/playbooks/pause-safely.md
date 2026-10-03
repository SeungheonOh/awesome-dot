# Pause safely

Use for an explicit pause/stop, a required handoff, or an unavoidable execution boundary. Read the [execution contract](../references/execution-contract.md). “Going away, keep going” is continued work when supported, not a pause request.

## Inputs

Current goal, all owners/processes, worktree and dirty state, pending external actions, and durable storage the next session can actually access. Do not assume temporary storage survives environment replacement.

## Steps

1. Stop scheduling new work immediately and send a no-new-writes hold to every active owner. Finish only the current safe atomic step or roll back its owned partial change when safe. Do not start a new implementation wave to reach a prettier stopping point.
2. Reconcile each in-flight operation. Confirm whether it completed, stopped, or remains active; record uncertain side effects. Use supported cancellation when appropriate and report if it is unconfirmed. Do not terminate unrelated processes or infer that a child stopped because the parent did.
3. Preserve work without unauthorized side effects. Save edits in the current authorized workspace and, when requested/allowed, a patch or local WIP commit. A pause alone does not authorize commit, push, PR creation, overwriting user files, reset, stash, or destructive cleanup. Record a broken working state honestly rather than hiding it.
4. Save a compact resume record in the agreed durable project/run location. Include goal/scope, latest constraints, repository/worktree/head/base and dirty identity, completed and pending steps, valid proof, failed/unrun checks, decisions, active owner/process IDs, uncertain external actions, exact next safe step, and required gates. Link an existing trail instead of duplicating it.
5. Verify the resume file can be read and the saved artifact exists. Identify any data still ephemeral or inaccessible to a future session. Leave transient evidence intact unless its deletion was authorized.

## Failure and completion

If storage is not durable, provide the needed handoff content to the user and state that limitation. If a worker cannot be stopped, do not claim a clean zero-writes state; identify its scope and protect against a conflicting resume.

Return the pause point, saved paths/commits when applicable, working-tree condition, active or uncertain operations, and first resume action. This is a checkpoint, not a claim that the original task finished. Resume through [Session pickup](session-pickup.md).
