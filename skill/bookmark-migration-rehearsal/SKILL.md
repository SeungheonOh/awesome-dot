---
name: bookmark-migration-rehearsal
description: "Move a selected bookmark collection between browser profiles with an import-ready file, occurrence-level reconciliation, a reversible pilot and verified target readback. Use for bookmark migration, not password or whole-profile transfer."
---

# Move Bookmarks Without Losing Their Places

Produce a usable bookmark transfer and account for every source folder and link occurrence. When the user requests a live import and the supported route is available, carry it through a backed-up pilot and target readback. A prepared file alone completes only a preparation request.

## Establish the boundary

Identify the source and target browser, version, operating system, device and exact profile; selected roots or folders; whether the target already has bookmarks; and an approved private location for the source export, target backup and migration record. Resolve whether the user wants preparation or execution. A clear request to import into a named profile authorizes the ordinary import; do not ask again just to create local drafts or perform that requested import.

For an explicitly file-only preparation request, work from the supplied export, selected scope and requested transfer format. An unchosen target profile or unavailable live backup does not block those local deliverables. Record destination behavior and metadata retention as untested; require target identity and current method checks before a later live import.

Before a live import, read existing sync/account state. An import can propagate to other devices or accounts. Clarify an unknown target or a newly exposed audience; do not enable sync, sign in, grant access or change security settings to make migration work. Never infer that two similarly named profiles are the same account. Credentials, passwords, cookies, sessions, payment data, history and whole-profile copies are outside this workflow. Select bookmarks alone in a multi-category importer.

Treat a known credential-bearing or one-time sign-in/reset link as authentication material even when it appears in a bookmark export. Hold it from the transfer and omit or redact secret values in every derived artifact, including sidecars and readable reports. Retain only the source locator, disposition and reason needed to find that occurrence in the untouched private original; do not duplicate secret-bearing titles, URLs or attributes. This is an explicit exception to the exact-value preservation rules below. Ordinary query strings are not automatically credentials, and should not be stripped to make a link appear harmless. Resolve a suspected access-bearing link before sending it to another profile or synced service.

Prefer the browser's official export/import interface. Consult current official instructions for the actual product; see the dated [browser method notes](browser-methods.md). Do not edit a live browser database. Keep private export content local: no online converters, link checkers or URL submission. Parse exports as data without executing scripts, loading icons or opening stored destinations. A syntactically acceptable URL is not a checked, safe or reachable website.

## 1. Capture a recoverable baseline

1. Export the selected source using the supported method. If export covers the whole profile, derive the selected subtree locally and leave the full export intact. Record the selection independently from the export so that missing exported folders can be detected.
2. Keep the original bytes unchanged. Record file digest, byte size, capture time, browser/profile identity, encoding and available source IDs. Reconcile source manager totals or an authorized tree listing with the selection. A file-only request establishes coverage of that file, not coverage of the live profile.
3. Before a live import, export/back up the target through its supported interface and read the result. Record its ordered tree and current profile identity. Identify the actual recovery operation and whether it appends, replaces or deletes. An HTML export does not by itself provide a one-click undo; restoring a native backup may replace newer bookmarks.
4. Freeze one run identifier and output filenames with no overwrite. Recheck source/target state before importing. If either changes, reconcile the new state first; never overwrite concurrent edits to restore an old baseline.

If the target cannot be backed up or an import cannot be distinguished from existing entries, stop before writing to it. Return the prepared file and the precise missing capability.

## 2. Inventory occurrences, not unique URLs

Parse folder nesting and sibling order, including empty folders and repeated folder names. Decode HTML entities exactly once and respect the declared encoding; resolve a decoding failure or an ambiguous folder boundary before transforming that subtree. Keep the source bytes available for audit.

Give every folder and bookmark occurrence a record containing the following, with the authentication-material exception above applied to all derived values:

```text
source export digest; native source ID if present;
otherwise export-local occurrence ID and its stated derivation;
parent occurrence ID; sibling index; ordinal path; display path;
item kind; exact title; exact decoded URL; all original attributes/description;
disposition and reason; planned output locator; observed target locator/ID;
field-by-field preservation status and import/readback evidence
```

An occurrence ID derived from a file digest and ordinal is a local lineage anchor, not a browser ID. Do not infer one from a title or URL. Preserve native IDs in the sidecar even if the destination assigns new ones. For repeated same-name folders, display paths alone are ambiguous; use parent IDs plus sibling ordinals.

Keep repeated URLs in different folders and identical links repeated in the same folder. Those placements may be intentional. Do not deduplicate, sort, merge folders, repair spelling, strip query strings/fragments, change HTTP to HTTPS, normalize Unicode, or expand redirects unless separately requested. A blank title is still a source value; report any target-generated replacement.

## 3. Prepare the transfer and exceptions

Choose the least-transforming supported route. Direct browser-to-browser import can be useful, but use it only if the categories, profile, scope and resulting changes can be bounded and reconciled. Otherwise use a supported bookmark HTML export and a local working copy.

- **Ordinary supported links:** Preserve titles, exact URL strings, nesting and sibling order in the transfer. Escape HTML syntax, not URL meaning. Keep empty folders even if every child is held.
- **Malformed or unfamiliar URLs:** Hold the affected occurrence in the private reconciliation record with the original value and location, except for authentication material whose secret values must remain only in the original. Distinguish malformed HTTP(S) from a valid but unsupported scheme. Do not guess repairs. Browser-internal pages, local files, mail links and bookmarklets need a destination-specific decision; retain non-secret values in the original export and sidecar rather than silently discarding or activating them.
- **Metadata:** Inventory creation/modification times, descriptions, tags, keywords, toolbar markers and icons if supplied. Make a per-field mapping of native support, transfer representation, observed retention and limitations. Preserve supported fields through the chosen route. Keep unsupported fields and raw attributes in the sidecar; do not claim that an attribute in HTML survived a browser import. Do not fetch icon URLs. Avoid embedding active content or unverified remote resources in generated previews.
- **Browser roots:** Map toolbar/menu/unfiled roots explicitly. Prefer a uniquely named migration wrapper when supported so the added tree can be identified and reversed. Preserve source root names inside it, treating toolbar markers as recorded metadata if their automatic placement would escape the wrapper. This intentional relocation must be visible in the report.

Save an import-ready file plus a complete sidecar before importing. The accounting must satisfy: every selected bookmark occurrence is either included once or held once; every selected folder remains represented or has an explicit unsupported outcome. A safe-subset file must say how many held entries it excludes. Loss of a user-required field is a decision point, even if the links still import.

## 4. Pilot, then execute the authorized import

Use an available isolated target profile when it is within the authorized scope; otherwise import a small identifiable batch into the actual target. Include a deep folder, an empty folder, Unicode, a repeated URL and representative metadata. Record the exact batch's source occurrence IDs. Do not change sync/privacy settings to create isolation without the needed approval.

1. Confirm the target profile and baseline still match. Import through the official interface. Record the selected file digest and actual action result.
2. Read the target manager and export its bookmark tree again. Inspect metadata fields the export does not expose through supported UI or an already-authorized interface. Match by target IDs if available; otherwise use the new subtree, ordered path, exact URL/title and duplicate occurrence counts. A success toast is insufficient.
3. Verify the pilot's folder boundaries, empty folders, order, Unicode, duplicates and metadata individually. Record any browser wrapper or normalization. Accept a difference only when it is already within the user's allowed losses; otherwise stop for that decision.
4. For a separate pilot profile, import the complete prepared file into the backed-up destination after the pilot passes. For a pilot in the actual target, import only the not-yet-imported occurrence IDs using a supported method that preserves their planned parents. If that is not possible, remove the exact unchanged pilot batch only when that cleanup is authorized, verify removal, then import the full file. Do not reimport the whole file on top of the pilot or silently split one folder into two.
5. After a timeout or uncertain result, inspect current state before retrying. An append importer can create duplicates on every retry. Retry only a verified unapplied operation; unresolved identity or concurrent changes stop the affected batch.

If the interface cannot support a bounded pilot or enough readback to distinguish additions, explain the limit and ask for the smallest alternative decision. Do not label a local parser test as a browser test.

## 5. Reconcile and leave a usable result

Compare source occurrences → planned transfer → observed target. Separately compare the target's pre-existing tree before and after, excluding only confirmed new additions. Report missing, extra, renamed, moved, reordered, normalized, held and metadata-lost entries; counts alone cannot establish fidelity. Include folder counts as well as link counts, and retain duplicate multiplicity in comparisons.

Return the target location when actually verified, the prepared HTML, the private lineage record and a concise report:

```text
Scope and baseline: source/target profiles, selection, capture and evidence limits
Accounting: selected folders/links; included; held; observed; fully reconciled
Preservation: titles, URLs, hierarchy, order, duplicates, metadata and existing target
Exceptions: affected source IDs, reason, actual state and smallest next decision
Recovery: exact added target IDs/subtree, backup location and reversal preconditions
Status: prepared only / pilot verified / imported with exceptions / fully reconciled
```

For an authorized rollback, first confirm the added subtree/IDs still match the recorded post-import state and contain no new user edits. Remove only those verified additions through the supported interface, then compare the remaining target to its baseline. Stop on changed identities or new entries. A whole-profile restore, deletion of existing bookmarks or an unrequested sync change needs its own authorization. Retain the source export, backup and reconciliation record until the user chooses their disposition.

## Worked offline case

The fictional [source export](source-bookmarks.html), [import-ready subset](import-ready.html), [lineage record](lineage.json) and [reconciliation report](reconciliation.md) demonstrate repeated placements, same-name sibling folders, Unicode, blank titles, empty folders and held URL types. The fixture has no credentials or real private destinations. [Offline verification](verification.md) explains the executed checks and the remaining live-browser boundary. Run `python3 check_example.py` from this folder to repeat those checks without opening any URL.
