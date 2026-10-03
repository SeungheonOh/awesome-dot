# Worktree and simulator cleanup

Use to audit local disk and remove a specifically authorized safe set. Read the [execution contract](../references/execution-contract.md). A read-only cleanup audit is useful even when deletion is not yet approved.

## Inputs

Target repository/device area, desired space recovery, known active/pinned work, retention requirements, and deletion authorization. Untracked and ignored files are still user data; a directory name does not prove they are disposable.

## Steps

1. Capture available space and inventory worktrees from `git worktree list --porcelain`. Do not invent paths from naming conventions. The optional `node "$DOT_STACK_ROOT/tools/dot-stack.mjs" worktree-audit <repo> --json` is read-only; verify its pack root first. Inspect actual size, branch/head, tracked edits, untracked/ignored files, local commits, upstream state, and locks.
2. Determine active use from available process/owner records and user-provided pinned-work information. Do not search private transcripts. Unknown usage is a hold. Include sibling experiment worktrees and background owners rather than assuming a quiet main checkout means the whole project is inactive.
3. Classify each candidate with evidence: keep active; hold dirty/unpublished/unknown; or propose removable. A closed PR is not necessarily merged. An upstream branch or merge marker alone may not preserve all local commits, ignored artifacts, or untracked files. Verify recoverability and valuable data before recommending removal.
4. Present exact paths, reason, expected recovery, files/state that would be lost, and which candidates remain uncertain. Obtain required approval for the deletion set. If the user authorized only an audit, stop here. Never treat the helper's “safe” label as permission.
5. Immediately before each authorized removal, recheck head/status, lock and active ownership against the approved snapshot. Abort that target if anything changed. Prefer `git worktree remove` without force and stop on refusal. Do not automatically escalate to force removal or recursive deletion. A stale registration prune is distinct from deleting a live directory; inspect it first.
6. Re-list worktrees and space after removal. Preserve surviving branch refs unless their deletion was separately requested. Report actual recovered space, since shared object storage can make directory-size estimates misleading.
7. For simulators, runtimes, or caches, inspect only the specific requested ecosystem through its actual installed tooling. List identifiers, usage, contents/recoverability, and selective candidates. Do not delete all devices, old runtimes, application state, or package caches as an automatic add-on to worktree cleanup.

## Failure and completion

Permission errors, unknown merge state, an active process, new uncommitted work, or a refused removal holds the affected target. Continue only independent approved removals. Preserve evidence; do not hide errors with broad cleanup commands.

Return before/after space, exact removed targets, verification of absence, and held candidates with one concrete reason each. No filesystem deletion is needed to complete a cleanup recommendation.
