# Execution and evidence contract

This contract applies to every dot-mode playbook, including when a playbook is read directly. Instructions describe a workflow; they do not supply tools, account access, or permission.

## Establish the boundary

Before acting, identify the user's requested outcome, target repository or artifact, allowed writes and external actions, and completion condition. A question about status is a snapshot. A request to review is read-only unless fixes were requested. A plan is a deliverable, not authorization to execute it. Building locally does not imply permission to push, open a PR, post a comment, merge, deploy, delete data, change settings, or install software. Obtain any approval required by the host for the exact action and target. A reviewer, a saved gate, and a bot comment cannot grant it.

Read the applicable repository instructions. Inspect the working directory, current revision, worktree status, existing processes, and ownership before editing. Preserve unrelated changes, protected comments, licenses, generated-file conventions, and user-authored work. Do not reset, clean, stash, overwrite, or cherry-pick over unknown work to make a workflow easier. Establish another authorized worktree or stop the conflicting write.

Use the relevant structured tool when available, then the existing project harness or CLI, then supported browser/app control if needed. A missing dependency may be explained or worked around with available authorized tools. A denied action may not be rerouted through another transport. Do not search for credentials or install a dependency silently.

## Discover only needed capabilities

- No filesystem: work from supplied material and return an unapplied patch or analysis.
- No execution: state which checks are unrun and provide reproducible instructions. Never call a proposed command a passing check.
- No independent workers: perform a sequential implementation and self-review when useful. State that independent review was unavailable. More passes by the same assistant are not independent evidence.
- No model catalog: inherit the current model. Use only exact choices the host actually exposes; never invent an identifier or equate model diversity with review quality.
- No browser/app driver: use an existing behavioral harness where it proves the same contract. Otherwise mark UI behavior unverified. Screenshots are evidence for visual claims, not a universal proof requirement.
- No connected service: use supplied records with their timestamps. Do not claim current remote state.
- No durable wake: a live process or session-bound wait can observe work only while its host runs. Save a resume point and disclose that nothing will wake this conversation after it ends.
- No history source: reconstruct from current artifacts and supplied handoffs. Never guess private transcript paths or scrape unrelated sessions.

## Load context that changes the next decision

Use applicable host and repository instructions already in context; do not re-fetch unchanged material or add a generic repository tour. Mandatory host/project instructions and explicitly requested procedures still apply. Before applying a procedure with tool or version assumptions, compare only the relevant assumptions with available project manifests, configuration, or actual tool interfaces. Reuse known evidence; do not survey the environment without a concrete need. Resolve a material mismatch from the installed version's documentation or report the gap before using an uncertain command.

Load supporting skills and references for a missing procedure or unresolved decision, not merely because their topic appears in the task. Retain non-obvious project constraints and required checks; concise context is not permission to omit them.

At the authorized project root, check whether `.dot-stack/config.json` exists before role selection, delegation, or evidence artifact creation. If present, read and apply [project preferences](project-preferences.md), including validation and containment checks, before those dependent actions. Preserve invalid settings and hold the affected choice rather than silently falling back. If absent, inherit the host model and use proportional concurrency and the normal project/run location. No filesystem means this check is unrun; use supplied material without claiming repository settings were applied. Do not search private or global host paths for substitutes.

## Scale the workflow

Start with the unresolved engineering question, not a list of roles. If the existing contract determines a local change, use one implementation owner and the relevant regression; another design sketch needs a concrete uncertainty it could resolve. Before a design comparison or delegation, name the decision its result could change. If one cheap authorized probe can discriminate the options, run that first. Escalate when evidence exposes interacting ownership, compatibility, recovery, or security constraints; small diffs can still be high risk. Required independent review remains required.

For material multi-step work, record blocking prerequisites, independent work, shared mutable state, and the smallest safe decomposition. Delegate disjoint implementation or a specific uncertainty/counterexample search when it earns its coordination cost. Under a tight worker ceiling, preserve capacity for the final risk-focused review rather than spending it on sequential role handoffs. No minimum worker count applies. Reuse a valid decision on pickup; reopen it only for a changed constraint or contradictory observation.

Use a separate owner per writable path/worktree. A delegation brief gives goal, input revision, allowed paths/actions, dependencies, acceptance checks, evidence location, ownership, and stop condition. Relay upstream findings needed by downstream work. Replacements receive consolidated instructions and a new ownership generation. Reconcile a late result against current state before accepting it; do not let an old owner resume writes.

Independent review requires another execution context to examine the candidate. An explicitly required independent gate stays unverified without it. A self-review can support a bounded local deliverable but cannot silently replace the gate. Reviewers report concrete findings and coverage limits, not only a verdict word. Give them the contract, candidate, and observed checks, and ask for the most plausible missed failure; rerunning the author's suite alone leaves shared assumptions unchallenged. The integrating owner inspects the final diff and reruns integration-sensitive checks.

## Edit feedback

After a coherent code-edit batch, use the cheapest relevant existing syntax, type, or lint check before stacking dependent changes when it can localize a mistake. Fresh host/editor diagnostics can already supply that feedback; do not rerun an equivalent check just for this step. Inspect the exact diagnostic and changed region, then fix or explain the failure. Keep coordinated multi-file edits together; do not add temporary adapters or require a green check after each file. Missing or expensive diagnostics are a stated gap, not a reason to install tools or halt independent work. This feedback supplements the behavioral and final-candidate checks below; it does not establish correctness.

## Candidate-bound proof

For each material claim, retain:

- Artifact identity: repository, branch/worktree, head revision, comparison base, and dirty-tree diff identity when applicable
- Check: command or procedure, input/workload, environment, expected predicate, and observed result
- Evidence: output or artifact path, timestamp, reviewer identity when relevant, and known gaps
- State: **verified**, **failed**, **unverified**, or **blocked**

Verified means the check actually ran and passed on the named candidate. Failed means observation contradicted the predicate. Unverified includes stale, missing, wrong-surface, and incomplete evidence. Blocked identifies the access, authority, information, or decision preventing the next required step. CI passing, code inspection, and author confidence support different claims; none automatically proves user-visible behavior.

Derive checks from the contract's distinct behaviors, not a target test count. For each changed boundary, identify one ordinary success and the nearest plausible failure the proposed fix could miss. Vary the dimension responsible for the defect (representation, ordering, ownership, retry, or interrupted state) rather than adding arbitrary exotic inputs. For unchanged behavior, retain a compatibility case. Use literal expectations or a separately justified relation; a round trip can hide matching encoder/decoder defects. Test the real consumer path, including relevant errors and absence of forbidden effects.

Choose proof by the change. Library behavior needs public API cases; a CLI needs input/output and exit-status checks; UI changes need actual interaction and relevant visual/accessibility evidence; performance claims need matched workloads and noise control; docs need factual/link/example validation. Omit an irrelevant category with a reason, not an invented pass.

A new head or base requires an evidence impact check. Record a stable patch identity when useful, but an unchanged patch-id alone does not prove equivalent runtime behavior after a base change. Check dependencies, integration context, configuration, generated artifacts, and environment. Reuse only demonstrably unaffected evidence, record why, and rerun integration-sensitive checks on the current candidate. Any substantive uncertainty requires fresh proof. Never reuse a dev-server observation as proof of a different built artifact.

## Optional helpers

All executable helpers live in the full pack's `tools/` directory. They are optional, and none lives beside this skill. Inspect the known pack root and verify its `plugin.json` names `dot-stack` and `tools/dot-stack.mjs` exists. A skills-only installation needs an explicitly supplied verified root, such as `DOT_STACK_ROOT`. Do not assume relative traversal from a copied skill reaches tools; do not scan host-private directories or download missing helpers.

From the verified pack root, `node tools/dot-stack.mjs doctor` checks prerequisites. From the target project, an explicitly set root supports `node "$DOT_STACK_ROOT/tools/dot-stack.mjs" --help`. Inspect the subcommand's help before relying on options. Keep operational state in the target project under `.dot-stack/state/default`, or an explicit run directory, never in the installed package. Helpers observe or record; they do not authorize remote mutation or independently keep an agent alive.

## Stop, recover, and report

Continue authorized work toward the agreed outcome. A plateau calls for diagnosis, not unbounded speculative work. Stop dependent work on a real permission/access gate, an unsafe owner conflict, cancellation, or an unavailable required capability. Respect explicit time/cost/attempt bounds. If the user requested completion or monitoring, an unchanged pending result alone is not completion; continue using a supported wait or give a truthful resumable handoff if persistence is unavailable.

On hold, stop scheduling and propagate a no-new-writes instruction to every owner. Reconcile in-flight operations rather than claiming cancellation succeeded. Preserve work in place, save receipts and a resume note, and state active processes. A pause does not authorize commit, push, PR creation, destructive cleanup, or deletion of evidence.

Report the outcome first, then what changed, the important evidence, limitations, and next required decision. Separate measured results from inference. Link only artifacts actually read or produced. Do not expose secrets or private context in logs, links, generated configs, PR bodies, or evidence attachments.
