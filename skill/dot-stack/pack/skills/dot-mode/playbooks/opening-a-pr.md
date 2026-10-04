# Opening a PR

Use when the user requested publication of a reviewable code/document change or a bounded execution brief explicitly authorizes it. Read the [execution contract](../references/execution-contract.md). This playbook is not an automatic epilogue to other work.

## Inputs

Repository and forge, intended base, owned branch/worktree, exact change scope, publication authority, readiness preference, and required project checks. A push or PR exposes code and metadata externally; respect the host's data-sharing and approval requirements.

## Steps

1. Inspect current worktree, branch, remote, and unrelated edits. Use an authorized isolated worktree if needed. Preserve user work. Never reset, hard-clean, or move someone else's changes out of the way to obtain a tidy diff. Check whether a PR for the same branch already exists before creating another.
2. Review the complete base-to-head diff, including generated files, tests, docs, licenses, and protected comments. Remove owned debug leftovers, speculative additions, and secrets. Use [no-comments](../../no-comments/SKILL.md) and [technical-writing](../../technical-writing/SKILL.md) where useful; no companion plugin is required.
3. Run repository-prescribed checks and risk-appropriate behavioral proof at the candidate intended for publication. Record baseline failures and unrun gates. Shape coherent commits according to project policy. Stage explicit owned paths. Do not rewrite published/shared history simply to make a narrative cleaner.
4. Resolve the authorized forge interface through an actual read. Prepare the title and body. Follow the repository's conventions; otherwise use a concise imperative title, optionally `type(scope): subject`. Explain why, material scope, consequential tradeoffs, blast radius, and verification. Keep detailed logs and full revision receipts in a suitable artifact rather than burying the reviewer in a lab notebook.
5. Verify destination/base and whether the change is independent or stack-dependent. An independent PR targets the agreed mainline. A stack child targets its intended parent branch and states that dependency. Rebase/retarget only when separately authorized and owned; refresh proof after integration changes.
6. Publish using the requested readiness. A draft can be appropriate for incomplete work or early feedback; a ready PR requires the stated review criteria. Never silently turn a draft into ready or open a ready PR before proof merely to satisfy a timer.
7. Read the created/updated PR back. Confirm URL, repository, title, base/head, draft/ready state, content, and any remote warnings. A command's successful exit alone is not evidence that the intended PR state exists.

## Failure and idempotency

If creation or push times out, query the branch and existing PR before retrying. Respect concurrent remote changes and do not force through a lease conflict. If publication is blocked, leave the patch and description ready locally and identify the exact missing authority/access. Never bypass a hook or approval gate to finish.

## Evidence and completion

Return the verified PR link, relevant scope/choice, checks and limits, and current readiness. Opening it does not authorize review replies, ongoing babysitting, merge, deployment, or branch deletion. If those were explicitly part of the original workflow, continue through the corresponding playbook under the same bounded brief.
