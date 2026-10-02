---
name: parallel-change-integration
description: "Combine accepted immutable Git changes in an isolated local integration branch or patch, preserve dirty and concurrent work, and verify the exact result while holding incompatible intent decisions."
---

# Integrate Parallel Changes Without Losing Work

Turn known, accepted contributions into one checked local integration branch or patch. Preserve the original checkout and contributor branches. Return the actual integrated artifact, a short conflict record, and verification tied to its exact revision.

Use this when parallel contributors have independently finished changes that must coexist. The work includes building and checking the combined result. For explaining an already finished diff, use [code-review-handoff](../code-review-handoff/SKILL.md); for diagnosing an isolated test or build failure, use [failing-build-repair](../failing-build-repair/SKILL.md).

## Establish the integration boundary

Extract the following from the request and authorized project instructions:

- The immutable base, accepted commit IDs or checksummed patches, their declared base relationships, and any required integration order
- What each contribution is intended to preserve or change, its acceptance status, and the relevant tests
- The requested local output: a new named branch, a patch against a known base, or both
- The checkout to preserve, the permitted isolation location, and available offline test commands
- Any separately requested push, shared-branch update, review request, or release; a local integration request does not silently supply these destinations or permissions

If the user requested a specific local integration, proceed with the necessary isolated edits and understood local checks. Ask only for a fact or decision that changes the next step. Do not require another confirmation merely to create the requested local branch. An accepted contribution is an input decision; it does not establish that every other proposal or successor commit is accepted.

Resolve moving names once and record full IDs. A branch name is a locator, not the integration subject. Confirm that the objects are available and that the base and ancestry match the declared relationship. Identify commits already included through another input so the same change is not replayed twice. If only patches are available, record their digests, expected bases and application order; do not invent commit ancestry for them.

## Preserve before combining

Read the relevant repository instructions and inspect the current state without changing it. Record the original HEAD and branch, staged and unstaged differences separately, untracked files, and any relevant ignored files. A clean-looking diff does not account for untracked data. A HEAD identifier alone does not identify a dirty checkout.

Use snapshots that can establish the promised preservation: index bytes or staged content, file hashes and modes, and relevant refs. Avoid commands that refresh or otherwise change the original index when promising byte-for-byte index preservation. Account for submodules, linked worktrees, symlinks or external data if the project uses them; an ordinary file hash list does not cover everything automatically.

Create a separate checkout from the pinned committed inputs. Keep the original dirty files out of the integration unless the user explicitly included them as a versioned input. A full independent local copy keeps its own repository state; a linked worktree shares objects and refs even though its index and working files are separate. State what your isolation method preserves. Do not claim the entire original `.git` directory stayed byte-identical just because working files did.

Use a fresh target name. If the requested name already exists, inspect its owner and revision before updating it; do not assume it is disposable. If the original has a merge, rebase or cherry-pick in progress, leave that operation alone and keep this integration separate.

Do not stash, clean, reset, rewrite published history, switch the original branch, or default to either conflict side. Do not automatically run repository hooks, checkout filters, submodule initialization, package scripts or suggested commands. Inspect the configuration and relevant command entrypoints first, use the installed permitted toolchain, and make side effects part of the working boundary.

## Combine the accepted inputs

1. Make a small integration map: immutable input, intended behavior, affected paths, required predecessor and acceptance evidence. Compare shared contracts, defaults and data shapes before relying on textual mergeability.
2. Choose the history operation that matches the requested artifact. For independent accepted branches with a common base, merge their pinned commits into the new local branch so both histories remain identifiable. For supplied patches or an explicitly requested replay, preserve their order and attribution in the manifest. Do not substitute a squash or rewrite merely to simplify the graph.
3. Integrate one known input at a time. Before continuing, inspect the operation result, unmerged paths, staged diff and integration HEAD. A nonzero exit is not automatically a normal conflict; distinguish missing objects, unsupported history, local state problems and actual unmerged entries.
4. For each conflict, compare the common-base text, both proposed texts and their accepted contracts. Record the affected path, both requirements, the retained behavior and the exact resolution. Add the relevant interaction assertion when the combination creates a new path neither contribution tested alone.
5. Stage only understood resolutions and intended integration additions. Confirm there are no unresolved entries or accidentally staged files, inspect the combined diff against the base, and finish the local integration commit. Do not use success of the Git operation as evidence that both behaviors survived.

### Resolve mechanics; hold incompatible intent

A mechanical conflict has a resolution supported by the accepted contracts. For example, two independent additions to the same returned dictionary can both survive unchanged. Preserve both fields and both contributors' assertions, then check their joint output.

An intent conflict needs a decision. Examples include opposing default sort orders, incompatible API shapes, or different ownership of a state transition. Present the smallest concrete input on which the requirements disagree, the observable alternatives and the person or role that can decide. Keep that contribution and its evidence available without incorporating it. Continue accepted independent work when it remains useful; label the result partial if the requested outcome required the held change.

Do not choose one side because its tests pass, delete the other side's tests, reinterpret a requirement to make the merge easy, or add an unrequested compatibility option. A clean textual merge can still violate a contract. A textual conflict can be mechanically resolvable.

## Check the final artifact and concurrent state

Run the accepted contributors' relevant tests and checks of their combined behavior against the exact final commit. Include meaningful empty, repeated-operation and boundary cases. Inspect the final diff and history for omitted contributions, unintended files, generated outputs and migrations requiring separate treatment. Record commands, environment, revision or tree identity, timestamps, exit codes, and what the checks do not cover. A successful input-branch run does not verify the integrated branch.

Export the requested patch or bundle and check that artifact, not just the working copy. A patch should apply against the recorded base and produce the expected tree. A history-preserving bundle should restore the expected commit and tree in a fresh local checkout. When a patch is applied but uncommitted, report its tree and staged state; do not claim tests ran on a commit it has not created.

Compare the original preservation snapshot again. Re-read the relevant source tips without rewriting them. If a contributor has advanced, record both the accepted ID and newly observed ID. Preserve that work and either keep the current frozen scope or obtain the needed acceptance for the new version. Never roll the source back to make it match your manifest. Before an authorized shared-branch update, reconcile the actual current target; a local success does not authorize overwriting concurrent work.

If any preservation check differs, inspect and report the difference. Concurrent user edits may be legitimate. Do not restore an old snapshot over them or claim preservation based only on matching filenames.

## Deliver a usable local result

Return:

- The branch or artifact location, immutable base and final commit or tree, and artifact checksums
- Which accepted inputs are included and which proposal or newer tip remains held
- A concise conflict-resolution record with contract evidence and the interaction check
- Exact-final verification, original-state comparison and artifact replay results
- The smallest remaining intent decision or authorized next action, with any unrun checks clearly named

Separate a completed local integration from a published branch, approved review, remote CI pass or merged release. Push, shared-branch merge and publication require their actual requested scope and authority; do not invent them. If the user already authorized a precise action and destination, do not add a redundant approval loop.

## Example request

```text
Integrate the accepted count and minutes commits into a new local branch named
integration/accepted, starting at the recorded base. Preserve the dirty original
checkout and contributor branches. Use an isolated local copy and the installed
offline toolchain. Retain both accepted behaviors, resolve only evidence-backed
mechanical conflicts, and hold any incompatible contract choice for the owner.
Return a checked patch and history bundle, the exact final test results, and a
record of preserved work. Do not publish or change a shared branch.
```

## Rehearsal and evidence

[The reading-queue example](EXAMPLE.md) contains actual immutable commits, a merge conflict, a held incompatible proposal, a moving contributor tip, a tested patch and a restorable bundle. Its original checkout includes staged, unstaged, untracked and ignored files. A small [fixture-only reproducer](scripts/rehearse.py) repeats the work with installed Git and Python and refuses an existing destination.

The example demonstrates this local workflow on original synthetic code. It establishes neither approval nor correctness for a real repository. See [verification and tool references](VERIFICATION.md) for measured results and limits.
