---
name: build-folder-synchronizer
description: Create or repair repeatable synchronization between two independently editable local folder copies, using retained agreement to reconcile changes, deletions, conflicts, and partial completion. Deliver a configured supported workflow or a scoped implementation with checked saved results. One-way generation, historical backup restoration, and merging one document have different authority rules.
---

# Build a folder synchronizer

Deliver a usable way to reconcile the selected folders again after further edits. The central fact is what the copies last agreed on, under which pairing and policy. Two visible files alone cannot tell whether a one-sided file is a new addition or the survivor of a deletion.

Start with an existing supported synchronizer or the project's current implementation. Check its actual version, comparison rules, retained state, conflict handling, and recovery behavior against the task. Prefer configuration when it satisfies the requirement. Build a small local component only for a concrete unmet need or an explicit implementation request; no new framework, service, watcher, remote setup, or credential is inherent in this task.

For maintenance, inspect the affected caller, configuration, saved agreement, and relevant file effects before editing. Preserve the original data and state while reproducing the issue on owned copies. Fix the differing behavior through the real entry point, retaining a nearby working case.

## Define the pair, population, and permitted effects

Resolve these consequential choices from the request and existing workflow. Keep them in its normal configuration or concise usage documentation, rather than inventing a second specification:

- **Pair identity:** the two actual local roots, their roles if asymmetric, and how the workflow recognizes this continuing pair. Resolve aliases and mounted locations sufficiently to avoid selecting the same tree twice or treating an unavailable volume as an empty folder. Use separate, non-overlapping roots for the ordinary two-copy workflow.
- **Selected population:** recursion and inclusion/exclusion rules, relative-path spelling and case, supported object types, and whether empty directories participate. Include new names on either side and previously agreed names now missing. Keep tool state, temporary files, retained originals, and generated reports outside that population.
- **Equality:** which contents and metadata matter. Exact bytes are the ordinary-file default; timestamps and sizes alone do not establish unchanged bytes. Normalize text, names, or Unicode only when the accepted contract defines that equivalence. Equal content at different paths does not establish one object.
- **Effects and decisions:** allowed directions, overwrites, deletion propagation, conflict treatment, and any supported merge or winner rule. A tool's default or a preview is not deletion authority. Carry out effects already authorized for the selected roots; resolve only a missing consequential policy or scope decision.
- **Execution and consumer:** who may edit or synchronize during a call, the expected collection size, the actual command/API, and the reader that must use the resulting files. Set expectations for partial progress and how a caller recognizes unresolved work.

Make rename, type, and metadata behavior explicit. Treat disappearance plus creation as two changes unless the chosen mechanism has an accepted rename identity rule; do not infer a rename solely from matching digests. A file/directory replacement or directory removal can affect descendants, including excluded entries. Classify it as a related structural operation and check its full permitted effect, or hold it as unsupported. Decide whether links, hard links, permissions, timestamps, and other relevant metadata are preserved, synchronized, ignored, or unsupported; byte equality does not answer those questions.

A one-way generated mirror has an authoritative input and rebuildable output. A backup preserves historical versions. A document merge produces a candidate with its own acceptance rules. Do not apply those authority assumptions to independently editable folders.

## Retain agreement with its meaning intact

Keep enough state to distinguish each selected path's last accepted contents or absence from both current copies. Bind that state to the pair, selection and comparison policy, consequential conflict/deletion rules, and a supported state format. Use the engine's own archive when suitable; a small implementation may use an ordinary versioned file or existing database. A digest identifies compared content but cannot restore or merge the old bytes when those capabilities need them.

Treat this as agreement, not disposable cache. Validate its identity and usability before normal mutation. A missing entry can mean previously absent only within a known complete population under the same policy. Unreadable state, unsupported versions, a different pair, or changed selection rules must not silently become an empty baseline.

Make first pairing deliberate. For an equal pair, verify selected membership and the agreed equality before recording the initial agreement. If the starting copies differ, settle how initial side-only entries and collisions are handled; do not invent a common ancestor. Keep first pairing or re-pairing distinct from ordinary continuation. If a supported engine silently starts fresh after archive loss, guard that invocation or use another supported route that meets the accepted continuation policy.

Keep state alongside the continuing workflow, in a location the next invocation will actually use. Moving roots or changing filters can require supported state migration or deliberate re-pairing. Preserve the prior state and explain the consequence before either; editing its identity fields or deleting it to clear an error does not establish lineage.

## Compare three states before choosing changes

Read both current populations and their coverage, then compare with retained agreement. Represent known absence separately from unreadable, skipped, or unobserved content. A failed listing, vanished mount, or partial scan does not establish deletions. Hold affected comparisons; proceed on independent paths only when their coverage and effects are established. Do not label that smaller result a complete synchronization.

For a policy that propagates one-sided changes and preserves independent divergence, use this per-path decision rule. Here B is the last agreed state, L and R are current states, and equality includes only the properties the contract selected. Known absence is a state; an empty file is present.

| Observation | Eligible result under that policy |
| --- | --- |
| L = R = B | No content work |
| L = R, different from B | Accept matching current edits or matching absence as agreement, if that class of agreement is permitted |
| L differs from B; R = B | Propagate L to R, including a known deletion only when authorized |
| R differs from B; L = B | Propagate R to L on the same terms |
| L and R differ from B and each other | Hold the conflict with both current states and prior agreement intact |
| Required state or coverage is unknown | No inferred copy, deletion, or new agreement for the affected path |

The conflict row includes different edits, different creations at a previously absent name, and deletion versus edit. Shared current edits need not conflict merely because both changed. Conversely, a newer timestamp is not permission to choose a winner. If the accepted workflow instead preserves conflict copies or selects a winner, make those exact effects and their repetition behavior explicit. Do not silently adopt a tool's different policy.

Retain the source of each decision: path, prior and current comparable state, intended direction/effect, and any unresolved choice. A concise preview can carry this information. Conflicts may remain while independent eligible paths progress. A merger, if requested and appropriate to the format, produces a candidate that must satisfy the accepted merge rules before becoming shared agreement.

## Apply current decisions and advance state truthfully

Use a coherent capture or the selected mechanism's supported change checks. A preview can become stale: revalidate its pair, policy, agreement revision, selected membership, and relevant file states before mutation, or recompute from current files. If the user accepted specific previewed effects, newly different effects still need to fit that authority. Do not apply an old byte buffer over an intervening edit.

Choose concurrency behavior that the implementation can actually support. A bounded local workflow can require one synchronizer and paused edits during each call. State that operating assumption plainly; a pre-write re-read does not enforce it. If overlapping writers are required, use appropriate coordination and stale-state checks for both file effects and agreement. A lock on the state file alone does not control an unrelated editor.

For each eligible operation or related group:

1. Recheck the relevant current-state preconditions and effect scope, including structural dependencies.
2. Apply only the authorized change. Use supported staging and publication appropriate to replacement or creation; a prior existence check is not an exclusive creation guarantee. Preserve the properties the contract requires.
3. Read the saved copies and verify the intended contents or known absence. Record failures and uncertain effects separately from planned changes.
4. Advance agreement only for the portion actually established under the policy, then reopen or inspect the saved state. Leave unresolved or unverified paths at their prior agreement.

For a configured engine, use its supported operations and state inspection. Do not edit internal archives or add a parallel baseline merely to mimic these steps.

Per-path progress is often sufficient. A complete replacement of one file or a database transaction for agreement does not atomically commit two directory trees. If the consumer requires a coherent group, use a supported group publication route or establish that requirement cannot yet be met. Keep atomic visibility, ordinary process recovery, and power-loss durability distinct.

After a failed call, report the saved state actually reached. A nonzero exit or lost response need not mean no effects occurred; a zero exit can still describe unresolved conflicts. Expose enough outcome information for the real caller to decide whether to use a result, review a conflict, or retry.

## Resume from saved reality

After interruption, inspect both folders and the retained agreement before repeating work. Keep already completed eligible effects, unresolved edits, and incomplete operations distinguishable. Reconcile using current observations; do not replay a stale plan or roll back someone else's later edit.

If a copy succeeded before agreement was saved, both current copies may already be equal. Under a policy allowing matching current states to establish agreement, that path can advance without copying again. If the copies have since diverged, apply the ordinary comparison and conflict rules. A journal is useful only when the promised recovery needs facts that the available state cannot reconstruct; it is not a default requirement.

Lost or incompatible agreement requires a different decision: restore appropriate retained evidence through a supported route, or deliberately establish a new pairing after reviewing current differences. Do not turn baseline loss into automatic resurrection or deletion. Preserve uncertain temporary or recovery files until their ownership and role are known; retries do not authorize unrelated cleanup. Stop when the usable result and visible holds satisfy the task, or when a concrete state, policy, access, or capability gap prevents further progress.

## Exercise the continuing workflow

Use preserved originals and separate owned copies for rehearsals. Run the actual configured command or public API, inspect saved files and state, and derive expected outcomes from the accepted policy independently of the implementation's report.

Exercise ordinary edits from each side and a later cycle using the same retained agreement. Include the consequential cases the actual contract supports: matching edits, independent divergence, additions, deletion, and deletion versus edit. Challenge a comparison shortcut with equal-size or unchanged-time edits when relevant. Check the selected population and excluded content, rather than merely comparing file counts.

Test stale-preview behavior when a preview is part of the interface. For promised recovery, choose a meaningful isolated interruption after a real file effect but before its agreement checkpoint, inspect those saved files, and retry the same pair. An available controlled seam is enough; do not require a journal, whole-tree transaction, arbitrary crash matrix, or unsupported concurrency tests. Also check ordinary startup with missing or incompatible agreement when that refusal is part of the contract.

Repeat unchanged work and verify no unintended copies, conflict duplicates, resurrection, or content loss. Diagnostic timestamps need not be identical. Run the intended reader on the saved resulting folders and read back its useful output when a downstream consumer is supplied; a successful transfer or archive/listing comparison alone does not establish that result.

Deliver the configured workflow or runnable scoped implementation, concise invocation, retained-state location and lifecycle, actual saved result, visible conflicts, and evidence for the checks performed. State local filesystem/platform, object and metadata coverage, concurrency assumptions, and the exact interruption boundary exercised. Source execution, installation, and general synchronization reliability are separate claims.

## Primary mechanism references

Use documentation for the selected version and route. The [Unison manual source](https://raw.githubusercontent.com/bcpierce00/unison/master/doc/unison-manual.tex), especially Updates, Conflicts, Reconciliation, Invariants, and Archive Files, describes retained per-path state, equal concurrent changes, and recovery after propagation precedes archive advancement. Its archive-loss behavior needs checking against the task's initialization policy.

For an existing rclone workflow, read [bisync operations and recovery](https://rclone.org/bisync/). Its resync and ordinary continuation have different effects; its listing check is distinct from checking current underlying files. These references help select and configure a mechanism. They are not evidence that the delivered workflow was exercised.
