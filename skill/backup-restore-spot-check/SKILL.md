---
name: backup-restore-spot-check
description: "Restore a selected subset of an existing backup into an isolated approved destination, compare the recovered versions with backup evidence, and reopen representative files without replacing originals."
---

# Check That Selected Backup Files Can Be Recovered

Use when the user wants evidence that particular files in an existing backup can actually be retrieved and read. Produce isolated restored copies and a per-file recovery report. A backup listing, successful backup-job badge, or orderly folder collection is not a restore test.

This is a bounded spot check. It does not establish full coverage, disaster recovery readiness, application consistency, or authenticity of a manifest merely because hashes match. It does not create a new backup, replace original files, restore into production, or repair backup contents.

## Establish the recovery boundary

Resolve these inputs before copying:

- The exact backup account/device, capture or snapshot ID, capture time and timezone, and selected item IDs or relative names
- The user's expected selection, independently of what happens to appear in the backup listing; this is the denominator for coverage
- Evidence for the backed-up versions: snapshot catalog, manifest, provider version IDs, sizes and supported content digests, with its source and trust limitations
- The isolated destination the user approved, its identity, effective access, available space, and whether the restore produces ordinary files or native documents
- Available authorized access to the backup and, optionally, the corresponding current sources for comparison
- Representative files to reopen, and the already available, appropriate viewers or parsers

An explicit request to restore named copies into a named destination authorizes those ordinary copy operations within that scope. If the destination is missing or ambiguous, prepare the inventory and ask where copies may go. If there is no independent expected selection, let the user select from the catalog and label the resulting test as catalog-selected; do not claim missing backup coverage was checked.

Keep password vaults, credential stores and authentication material outside this workflow. Sensitive files need authorization for the specific destination and audience; copying to a synced or shared folder can transmit them. Do not create access grants, configure credentials, install software, upload files to a new service, or change retention/sharing settings to make a test work. An unreadable encrypted backup is blocked until an already-authorized supported access route exists; never ask for its password in chat.

## 1. Pin the versions and the evidence

Record the selected snapshot's immutable identity or version token. Keep these separate:

```text
Backup capture: snapshot ID + capture time + item version ID
Expected historical bytes: manifest/catalog source + size + digest algorithm/value
Available backup payload: observed version + size + freshly read digest, if supported
Current source: independent item identity + current revision + observation time
Restored copy: destination item identity + restored version + readback evidence
```

A current source that changed after the backup is not a valid historical checksum baseline. Its mismatch with the historical copy can be expected. Do not silently substitute today's file, another snapshot, or a same-named item for the requested backup version.

Inspect where the manifest came from. Record whether it is a provider catalog, a user-maintained list, or an unverified file kept beside the payload. Matching a digest establishes a byte relationship to that evidence; it does not prove who made the manifest, whether both were changed together, or that unlisted files were backed up. A checksum computed now from the backup is a useful copy baseline, but is not independent evidence of the original captured bytes. Timestamps alone do not establish lineage.

Match selected items by stable IDs and version IDs where available. Report missing catalog entries separately from catalog entries whose payload cannot be retrieved. Record incomplete listings, pagination errors and unavailable versions as gaps. Continue independent items without replacing missing rows with easier examples.

## 2. Plan an isolated, non-overwriting restore

Use an already available connector when it supports retrieving the selected version into the approved destination. Otherwise use the service's supported restore-to-alternate-location workflow or an authorized local copy of already accessible backup files. Inspect actual tool capabilities; do not invent a restore action or claim that listing metadata retrieved the bytes. Downloading or exporting must be within the approved destination and data-sharing scope.

Before writing:

1. Verify the destination is separate from both the live source and the backup, is not a production/application watch folder, and will not unexpectedly sync to a new audience.
2. Create a new run subfolder only within the approved scope. Check exact destination identities and collisions. Prefer exclusive creation/no-overwrite behavior; a naming convention alone is not protection.
3. Use only the selected regular files for a plain-file copy. Do not follow links into unselected locations. Preserve source and backup; never use move, delete, repair, or restore-in-place operations.
4. For provider-managed packages or native documents, use a supported export or alternate-location restore that preserves the properties being tested. If the available route only restores in place, requires new credentials, or cannot preserve the requested version, stop that row and explain the blocker.
5. Record the pre-copy item versions and what can be checked afterward without changing them. For ordinary files, record byte digests and membership of the bounded source/backup sets; a small test is not a scan of unrelated files.

Leave unexpected destination contents untouched. On a timeout or uncertain copy response, inspect destination state and version before retrying; do not create multiple copies or overwrite an uncertain result. Never delete restored copies automatically at the end of a real run.

## 3. Retrieve and verify separate properties

Read back the restored copies, rather than trusting a success response. Keep separate results for each property; one passing property cannot stand in for another.

- **Existence and count:** Which selected entries have a restored item? Report selected, catalogued, payload available, copied, and verified counts with explicit denominators. A count match does not prove identity.
- **Historical identity:** Did the operation retrieve the requested snapshot/item version? A native export may transform bytes; report the format and properties lost instead of comparing incompatible digests.
- **Byte integrity:** For ordinary files, compare restored size and a supported digest against both the observed backup payload and the historical manifest, where available. Identify which baseline disagrees. Re-read relevant inputs after copying to detect a changed backup or live source. If a version changed during the test, hold that comparison as unstable instead of declaring corruption.
- **Readability:** Reopen representative restored files using an appropriate existing viewer/parser. Record exactly which files and what was observed: text decoded, pages rendered, workbook loaded, or image displayed. A file can open despite missing bytes or damaged content elsewhere.
- **Application consistency:** Only report a domain-specific check when actually performed in an isolated supported mode, such as relevant formulas and totals in a restored workbook. Merely opening an application file does not establish that all its data or dependencies are usable. Unsupported formats remain untested; do not install a viewer or connect a restored database to production.
- **Current-source comparison:** If authorized and readable, compare the current source separately. A confirmed later revision that differs from a verified historical restore is `changed since backup`; if lineage is uncertain, say `current source differs; timing/lineage unconfirmed`. Neither result automatically invalidates the restored historical version.

Opening files must not execute scripts or macros, enable external links, refresh live data, or autosave over sources. If a viewer would do those things and there is no supported isolated read-only route, stop that open check. For plain UTF-8 text, reopening and decoding tests readability, not the truth of its contents.

## 4. Classify failures without hiding useful partial results

| Observation | Report | Next step |
| --- | --- | --- |
| Selected item absent from the supplied manifest/catalog | Missing historical evidence | Ask for the correct snapshot/catalog or identify an explicit alternative baseline; do not call the item restored from the requested version |
| Catalog entry present but backup payload absent | Backup item unavailable | Recheck the exact snapshot/item reference through existing access; report unresolved absence without changing the backup |
| Backup payload disagrees with historical manifest | Baseline conflict | Preserve both observations; check identity, manifest provenance and version stability before attributing corruption |
| Restored bytes disagree with observed backup payload | Copy verification failed | Keep the failed copy isolated; if authorized, retry once into a fresh destination after rechecking the baseline; report unresolved failure if it persists |
| Bytes match but open/read fails | Recovered bytes, unreadable in tested method | Record parser/viewer error and supported format; investigate without modifying the backup or silently repairing the copy |
| Format unsupported or viewer unavailable | Byte result reported; usability untested | Ask whether an existing compatible application or a user-performed open check is available |
| Current source differs from evidenced historical version | Historical result plus separate source-change finding | Confirm the user selected the intended capture; do not replace either version |
| Only restored existence could be verified | Retrieved; integrity and usability unverified | Name the missing evidence or capability; a download response alone is not a pass |

Source or backup changes observed during the check are a stop-and-review condition for affected rows. Do not attempt to undo concurrent edits. If destination access differs from the approved access, stop further copies and report the exact discrepancy; do not improvise permission changes.

## 5. Deliver the recovery result

Return the destination reference only to the authorized audience, plus a small private report. Include:

```text
Scope: selected items; chosen capture; selection basis; exclusions
Evidence: catalog/manifest provenance and what it can and cannot establish
Counts: selected / catalogued / payload found / copied / byte-matched / reopened
Per item: backup version, restored identity, size/hash results and baselines,
          open check, application check, current-source comparison, outcome
Preservation: source/backup readback checks and any unavailable checks
Exceptions: missing items, mismatches, unsupported checks, exact next decision
Conclusion: what this sample demonstrates and what remains untested
Retention: copies remain in the approved destination; no cleanup implied
```

Avoid including private document text or sensitive filenames in a broadly visible summary. Keep digests and identity references only where needed for the authorized report. Do not call a partially checked sample a complete or healthy backup.

Read the [fictional worked example](worked-example.md) for an executed plain-file copy/readback check and separate failure outcomes. Its temporary-data cleanup is limited to synthetic fixture files; it is not a real-run cleanup policy.

## Example request

```text
Check whether these selected files can be recovered from my September 28
backup. Use that capture's catalog as the historical reference. Restore copies
into the empty private Restore Check folder I selected, then reopen the text
files. You may read the matching current sources to identify later revisions.
Preserve the sources and the backup. Report missing items and anything you
cannot verify; leave the recovered copies in place.
```
