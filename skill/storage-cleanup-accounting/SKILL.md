---
name: storage-cleanup-accounting
description: "Assess a scoped storage problem, execute authorized recoverable cleanup, and reconcile file identities, allocated space and measured volume availability without overstating savings."
---

# Clean Up Storage With an Honest Space Report

Use when someone needs usable space on a particular device or volume, or wants to understand whether a proposed cleanup will help. Produce a small keep/move/remove manifest, perform the clear actions already authorized, and report what actually happened to space on the affected volume.

Start with a goal such as “make another 5 GB available on the laptop's internal volume for this export,” rather than “delete the largest things.” State whether GB means decimal bytes or GiB, and whether the goal is additional free space or a final available-space threshold. A tidy folder, fewer visible files and reclaimed storage are different outcomes.

For renaming or categorizing documents, use [document filing](../document-filing-pass/SKILL.md). For evidence that selected historical files can be recovered, use [backup restore spot checking](../backup-restore-spot-check/SKILL.md). Neither operation by itself establishes space reclaimed here.

## 1. Resolve the device, volume and authority

Identify the actual machine and account, the selected folders or file IDs, recursion boundary, exclusions, and the volume containing each candidate. Resolve mounted storage, shortcuts, external drives and cloud accounts from current evidence. The folder called “Archive” may be on the same volume as Downloads; an external-looking path may be a mount or a synced folder. A second volume can also share an underlying storage pool. Do not infer an independent destination from its name or drive letter alone.

Record the current filesystem or service, available-space measure, timestamp, units, quota or container boundary if relevant, and the requested target. Prefer the operating system's measurement for the exact affected volume. Cloud account quota, a remote server's capacity, local disk availability and application storage categories must remain separate. If the symptom is failure to create even a tiny file despite free bytes, also check available file entries/inodes and the applicable quota before prescribing large-file deletion.

Read-only inspection within the request needs no extra approval. Carry out ordinary safe moves that the user already requested within a resolved destination and unchanged access. An instruction to investigate is not permission to delete, upload, change backup retention or uninstall applications. A vague “clean up” request does not settle which records can be lost. Resolve only the missing scope or destructive decision while progressing the safe inspection and any independently authorized rows.

If recoverable deletion of a specific set is already authorized, use the supported recovery mechanism after checking that recovery actually applies to this location and account. Do not turn that into permission to empty Trash, permanently remove files, purge cloud recycle bins, erase snapshots or change protection settings. Irreversible removal needs the required approval for that particular action, even after an earlier general cleanup request.

## 2. Find the smallest useful candidates

Inspect the selected folders using metadata first. Record inaccessible paths, missed pages and skipped mounts as coverage gaps. Avoid scanning every home directory, following links outside scope, reading private content unnecessarily, or opening online-only files just to estimate them; opening can download their contents. Do not install a disk cleaner to begin this pass.

Start with candidates the user can evaluate: an old export they identified, a separately retained downloaded copy, or a locally cached cloud file they explicitly no longer need offline. Verify the role of each candidate before acting. Old timestamps, a “copy” filename, a matching size or a cache label are not evidence that data is disposable. A saved export may contain edits missing from the original. Application libraries, mail stores, virtual disks and project dependency trees need their supported application workflow; do not remove pieces merely because a scanner ranks them highly.

Keep uncertainty visible:

| Observation | What it establishes | What still needs checking |
| --- | --- | --- |
| Same byte digest | The compared ordinary file bytes match at that observation | Which record must remain, metadata/history, and whether storage is independent |
| Same device and inode on an applicable local filesystem | Multiple names refer to the observed same file | Links outside the selected tree, current identity, and whether any retained reference remains |
| Large logical size | The file's addressable length | Local allocation, holes, compression, shared extents and residency |
| Cloud-only status | The provider reports no ordinary full local copy | Local metadata/cache footprint, account identity and current sync state |
| Backup success indicator | A backup job reported success | Recovery of the specific version and whether deletion is appropriate |

Hash only the small, relevant ordinary-file candidates when useful and authorized. Do not read entire cloud libraries to find duplicates. Recheck identity and revision around long reads; changed inputs do not support a stable comparison.

## 3. Keep three accounting questions separate

**How much content is visible?** Logical/apparent bytes describe file length. They are useful for understanding exports or transfers, but summing them by path can count hard-linked content repeatedly and include holes or nonresident data.

**How much allocation does this filesystem report?** On the Linux example, `st_blocks × 512` is the reported allocation; `st_size` is logical length. Count each `(device, inode)` once for a selected regular-file total. This removes hard-link double counting only. It does not discover sharing between different inodes, physical device overhead, snapshots or exclusive ownership of data blocks. [Python's filesystem field definitions](https://docs.python.org/3/library/os.html#os.stat_result) explain these platform-dependent fields.

**How much usable capacity did the action make available?** Measure the same volume and metric before and after the action. A reported allocation total is not a guaranteed reclaimable amount. Retained hard links, open files, clones, snapshots, compression, deduplication, sync behavior and filesystem accounting can change when or whether availability increases. If exclusive allocation is unknown, label reclaimable bytes unknown rather than turning file size into a promise.

On a machine with GNU tools, `du -B1` reports allocation estimates, `du --apparent-size -B1` reports apparent size, and `df -B1` reports filesystem capacity in byte units. Pin the selected path and record commands/options and errors privately. GNU `du` normally counts hard-linked files once per invocation; adding separate folder totals can count their shared file again. Its estimates can also differ from physical use on copy-on-write or compressed storage. See the [GNU du manual](https://www.gnu.org/s/coreutils/manual/html_node/du-invocation.html) and [GNU df manual](https://www.gnu.org/s/coreutils/manual/html_node/df-invocation.html). These options are not a promise that macOS or another implementation accepts the same syntax.

Do not add nested folder totals, sum parent and child rows, or attribute a hard-linked file independently to every folder that names it. Keep directory metadata separate when comparing an explicit regular-file inventory with a whole-tree tool total. Record permission failures rather than presenting an incomplete sum as full coverage.

## 4. Prepare the minimal action manifest

Choose the smallest set of clear candidates likely to help the stated goal with acceptable recovery and disruption. A legitimate result can be “none of these authorized actions releases space.” Do not expand to unrelated apps or system folders merely to reach a target.

Save a private plan before changes. Each row needs:

- Stable service identity or appropriate local identity plus original relative path, revision/mtime, observed size and necessary content evidence
- Keep, hold, move, release-local-copy, or remove disposition, with a brief reason
- Exact operation and destination/recovery location, authority already provided, and any approval still needed
- Expected effect on the target volume, with units and evidence; use zero or unknown when appropriate
- Preconditions, status, observed destination/state and recovery instruction

Include only metadata needed to explain and undo the action. Do not put private filenames or full directory inventories into a public report. A checksum is comparison evidence, not a substitute for a usable retained version or deletion authority.

Apply these operation-specific distinctions:

- **Same-filesystem move or local Trash move:** The file payload remains on that filesystem. Claim no freed payload space. Staging may help review, but is not a solution to a capacity target. Verify the actual Trash location and semantics instead of assuming every service uses a local folder.
- **Copy or move to another storage location:** Check that it is genuinely separate capacity, appropriate for the data, within the authorized destination and recoverable as required. Verify a readable destination copy and required metadata before any separately authorized source removal. Copying alone leaves both copies. Moving the source into Trash on its original volume still retains its payload there. A failed or interrupted copy must not trigger deletion.
- **Release a cloud file's local copy:** Confirm that the current version is uploaded, the cloud copy is available through authorized access, the user approved losing offline availability, and the provider offers that precise operation. In OneDrive for Windows, “Free up space” changes a locally available file to online-only; deleting an online-only file deletes it from OneDrive as well. Recheck the current client and account before acting. This changes local residency, not the cloud storage quota. [Microsoft's Files On-Demand guidance](https://support.microsoft.com/en-us/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows)
- **Remove a duplicate or application-managed item:** Establish which item must remain and the actual recovery route. Use the application's supported control for managed content. A matching digest does not authorize deletion or predict physical savings.

Keep snapshot and protected-system cleanup out of an ordinary file pass. For example, Apple counts Time Machine local-snapshot space as available storage and manages those snapshots automatically; that display is not an extra saving to add to a file list. Do not disable backups or purge snapshots to make the report's numbers match. [Apple's local-snapshot guidance](https://support.apple.com/en-us/102154)

## 5. Execute clear authorized rows and read them back

Before each operation, recheck source identity, current version, residency if relevant, destination identity/access and collisions. Stop a changed row rather than applying a stale plan. Prefer a supported no-overwrite or atomic conditional operation. A path check followed by a rename is not a general concurrency guarantee when other processes can change the directory.

Perform one small batch at a time. Reopen or read back the moved/copy destination, confirm expected bytes or supported native version, and verify the original location's actual state. Preserve the properties the task requires; a plain file copy may not preserve ACLs, alternate streams, package relationships or native history. Record verified, failed, partially applied and unknown results separately. On a timeout, inspect both locations before retrying. Do not overwrite an unexpected destination or blindly repeat an uncertain operation.

When an operation makes a file online-only, do not immediately open it as a “verification” step and download it again. Verify the synced cloud version before release and check the local provider residency state after it. Use the correct local-space metric for that file's volume.

If a decision remains open, continue the independent authorized rows. For an authorized reversal, check that the recorded post-action identity and version still match, the old location is suitable and no collision has appeared. Reverse only those verified operations and append readbacks. Do not roll back someone else's later edit.

## 6. Measure the result and close the loop

Take the baseline after preparatory copies and report-file creation where practical; those writes use space too. Measure again after completed operations using the same device/volume, tool, unit, quota context and residency state. Retain timestamps and raw evidence. A displayed category chart may lag; a later comparable read can distinguish a delayed update from an incorrect expectation.

Report four separate quantities where available:

1. The requested target and starting available space
2. What changed: specific file states and verified destinations/recovery locations
3. The observed change in volume availability, including a decrease or zero
4. The portion defensibly attributable to the action, or why attribution remains uncertain

Background writes, sync, snapshots and metadata can move the volume counter during a pass. Do not announce the entire delta as savings merely because it followed a cleanup. If the target is a final availability threshold, state whether it was met at the recorded observation, separately from causal attribution. If it is additional capacity created by these actions, do not use unrelated free-space growth to claim success.

When space did not increase, inspect the relevant already-visible evidence: same-volume staging, retained links, local/cloud confusion, unfinished sync or copy, another quota, delayed accounting, or an open-file indication from an existing supported tool. Do not kill applications, restart the machine, purge retention or run blanket cache deletion merely to force a number upward. Report the smallest remaining decision or scoped diagnostic.

Deliver the manifest and a short result such as “Two requested files moved and verified. Available space increased by X bytes during the interval; Y is attributable, the rest is unexplained,” or “The review move preserved all payloads and freed zero payload bytes; the 8 KiB goal remains unmet.” Link only verified destinations and identify held rows and coverage limits.

## Worked evidence

The [fictional example](example.md) runs in a new directory on Linux. It measures a sparse file, a hard link and a separate file with the same bytes, then performs and reverses one authorized move. The [source and verification notes](sources-and-verification.md), [pre-action plan](plan.json), [actual observations](evidence.json) and [completed manifest](manifest.json) separate local evidence from platform behavior that was not exercised. The included script is a small rehearsal, not a cleanup tool for user folders.
