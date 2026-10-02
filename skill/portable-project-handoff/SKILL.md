---
name: portable-project-handoff
description: "Prepare a bounded project-file ZIP for a named recipient and target platform, preserve selected dependencies through reviewed copy-only renames, and verify the actual archive in an isolated extraction."
---

# Prepare a Project That Survives the Handoff

Produce the actual ZIP, its file-and-reference map, and evidence that the extracted project matches the reviewed package. A list of files or a successful archive command is insufficient. The useful outcome is a new, bounded transfer package whose selected files remain distinguishable and whose required relative references still point to the intended content.

Use for plain project files being handed to another person, device, or platform. This differs from checking whether an existing historical backup can be recovered and from reorganizing a live document collection. It does not imply software execution, deployment, a full backup, or application migration. Native application projects may require that application's supported packaging/export workflow; do not flatten a native package into ordinary files without establishing that the result meets the request.

## Establish the recipient, selection and acceptance test

Resolve these from the request and available files before asking for missing details:

- The source root or exact item identities, selected entry points/files, explicit exclusions, and whether subfolders belong to the selection
- The named recipient or bounded audience, intended use, target operating system/filesystem, extraction tool, and appropriate viewer/application where relevant
- The approved local preparation destination, package size limit and expected extraction folder; keep working copies outside the originals and any application watch folder
- What must survive: file bytes, logical references, editable sources, license/attribution files, application metadata or other stated properties
- Permitted transformations, such as specified destination renames and matching references, and whether the task is preparation only or also authorized delivery

Do not treat “make a ZIP for Rowan” as permission to send it. Actual upload or sharing needs authority for the identified package/data and named recipient/destination. Prepare locally when that is the approved scope. Check whether a destination is synced or already shared before copying private files there. Keep credentials and authentication material out of this ordinary handoff workflow.

If the recipient's platform is unknown, inventory the selected files and identify dependencies while asking for the detail that changes packaging. Do not invent compatibility requirements, promise universal portability, or silently adopt a restrictive filename policy. Record an explicit assumption if only a conservative preparation is possible.

## 1. Freeze the selected source and its dependencies

Record each selected path or stable identity, type, available revision, size and content digest. For ordinary files, preserve the exact relative path spelling. Save the selection independently of the archive command so omissions cannot disappear from the denominator. Record excluded items with reasons. Use neutral exclusion categories in a recipient-facing report when original names would reveal private information.

Trace references from the selected entry points through the required project files. Relevant references can include Markdown links, HTML/CSS assets, document attachments, configuration paths, application manifests, or native project dependencies. Use the format's actual syntax; a regular expression for simple Markdown links is not a parser for all Markdown, HTML or application data.

Distinguish internal relative references from external URLs, cloud shortcuts, filesystem links, embedded absolute paths, missing dependencies, and generated material. A cache is removable only when the intended use does not need it and its exclusion is authorized. A file outside the selection that is required by a selected file is a held dependency, not automatic permission to expand the handoff. Likewise, an excluded license or editable source cannot be quietly dropped when the requested outcome requires it.

For a plain-file bundle, do not follow symbolic links or shortcuts into unselected locations. Establish the desired treatment before copying them. Source references that resolve through the original project can conceal a broken transfer: final checks must resolve entirely within the extracted package, except explicitly declared external dependencies.

If a source changes during preparation, hold the affected files and refresh the plan. A digest observed during this run proves a byte relationship to that observation, not historical authenticity or completeness of an unseen source collection.

## 2. Inspect target naming and reference constraints

Check the selected paths and proposed package root against the actual destination's rules. Include directory components, generated support files and the full expected extraction path. A shallow destination can work where a deeply nested one fails. Distinguish a known rule violation from a conservative warning and an untested assumption.

For Windows targets, official guidance says to avoid assuming case sensitivity, lists reserved characters and device names, and disallows trailing spaces or periods in the shell. Inspect both files and folders; two case-distinct source files must never become one accidental output. See [Microsoft's naming guidance](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file). Long-path behavior depends on the application and configuration; do not change system settings to make a handoff pass. See [Microsoft's path-length guidance](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation).

For macOS, determine the actual volume behavior: Apple documents both ordinary APFS and case-sensitive APFS options. A successful write on one volume does not characterize every Mac. See [Apple's filesystem formats](https://support.apple.com/guide/disk-utility/file-system-formats-dsku19ed921c/mac).

Keep Unicode normalization, case comparison and duplicate-content checks separate. A generic case-fold/normalization screen is a warning aid, not a complete implementation of every filesystem's equivalence rules. Do not silently transliterate or normalize names, strip useful files, or convert internal spaces simply for convenience. Exact duplicate bytes still represent selected identities unless the user approved collapsing them.

## 3. Review a concrete copy and reference map

For every selected source, record the destination relative path, whether its contents stay byte-identical, and any precise reference edits. Include the reason and evidence for each change. For a collision, use distinct meaningful names or the user's already-approved disambiguation rule; never choose an arbitrary winner.

Preserve originals. Apply approved ordinary copy/rename/reference changes to the new package without redundant approval. Ask only when the missing decision changes selection, meaning, behavior, access or the permitted transformations. If a requested “no content changes” constraint conflicts with necessary reference edits, show the exact conflict rather than silently changing the files.

For text references, retain encoding, line endings and unrelated content unless a separate conversion is approved. Use format-aware edits or exact reviewed replacements with occurrence checks. Map logical targets, not merely matching text: after renaming two different guides, both links must continue to identify the same respective guides. Recheck anchors, URL encoding, quoted paths and case where the format uses them.

Renaming a source-code module, build input or native application's internal file can change behavior beyond visible links. Do not assume a whole-folder text replacement repairs it. If dependency semantics are unknown, hold that rename and use the application's supported copy/package route or seek the smallest needed decision. A local filename check cannot establish program compatibility.

## 4. Build the actual bounded archive

Create a new preparation folder and a new archive with exclusive/no-overwrite behavior. Write only the explicit selected files, approved transformations and declared support files. A recursive “zip everything here” command can accidentally include old archives, hidden configuration or unrelated drafts. Reconcile planned membership against actual ZIP members before testing extraction.

Use one clear top-level folder when appropriate for the recipient's extraction workflow. Keep the selected relative directory structure unless the reviewed map changes it. Choose a ZIP method supported by the intended extractor. If the package is over the agreed limit, return the size finding and options; do not remove required files or use an unrequested upload destination.

Reopen the archive and inspect member names, count, stored sizes and content digests. Inspect format metadata as well as visible files: names, comments and extra fields can reveal source details. An ordinary ZIP does not automatically preserve ACLs, extended attributes, cloud document identity, application metadata or all timestamps. Record what is preserved and test any property the request actually needs; do not claim preservation merely because the file opens.

Create a manifest that identifies selected, excluded and generated files separately. For changed files, retain both source and package digests plus the approved edits. Keep the archive's byte count and SHA-256 outside the archive to avoid a circular self-hash. A digest verifies the received bytes against the supplied baseline; it is not a signature or proof of who authored the package.

## 5. Extract independently and read back

Use an already available native extraction tool on the target platform when accessible within scope. Extract the exact archive into a fresh empty isolated folder. Inspect ordinary member paths/types first, avoid overwriting anything, and never execute bundled code, macros, installers or scripts just to test the package. Do not install software or change security settings to obtain a green result.

Check distinct properties and report each separately:

1. **Membership:** Exact extracted selected files and declared support files, with no missing, unexpected, merged or renamed outputs
2. **Bytes:** Each extracted file matches its planned package digest; byte-identical files also match their source digest, while edited files match the reviewed transformation
3. **References:** Required links/dependencies resolve within the isolated extraction to the same logical targets; original-source availability cannot supply missing content
4. **Readability:** Reopen representative files using an appropriate existing read-only viewer/parser, without external refresh or code execution; record what actually opened
5. **Preservation:** Re-read selected source versions/hashes and the reviewed map; report concurrent changes or unavailable checks
6. **Platform/application behavior:** Record the real operating system, extractor and application tested; reserve target-platform success for an actual target-platform test

If the target is unavailable, a native extraction on the available platform is useful evidence with a narrower conclusion. Label it precisely. A Python extraction tests Python's extractor; Linux unzip tests that Linux tool. Neither establishes Windows File Explorer, macOS Finder, a Markdown renderer or a project application's behavior.

If extraction fails or readback disagrees, keep the failed result separate and inspect the specific mismatch. Rebuild only after correcting the reviewed plan within existing authority, using a fresh destination and archive identity. Do not retry by overwriting a partially extracted folder. Leave real user's prepared or extracted files in place unless cleanup was explicitly authorized.

## 6. Deliver the package and its limits

Return the actual archive reference, exact byte count/SHA-256, recipient/platform scope, selected/excluded/generated counts, changes made, extraction evidence and unresolved limitations. The user should be able to identify the entry point and understand whether target-platform application use was actually checked.

If sending was authorized, verify the specific destination and audience, transmit only the reviewed package, and read back the uploaded identity/access or delivery receipt when available. An upload receipt alone is not proof the recipient extracted or used it. If the request ends at preparation, stop after the concrete local deliverables; do not contact the recipient.

## Worked handoff

The [fictional example](example.md) packages seven selected text files for a named Windows recipient. It includes an original [source bundle](fixtures/source-bundle.json), a [reviewed machine-readable map](fixtures/reviewed-map.json), the [actual ZIP](artifacts/maple-client-help.zip), its [manifest](artifacts/manifest.json), and [native extraction readback](artifacts/readback.json). The [verification record](verification.md) gives executed checks and precise limits.

The [small reproducer](scripts/reproduce.py) implements only this ASCII/plain-text scenario and simple inline relative Markdown links. It creates a new output folder; it does not modify the fixture inputs, accept arbitrary received archives, access accounts, execute package contents or send files. Run from this skill folder with an absent destination:

```sh
python3 scripts/reproduce.py --out my-handoff-check --native-unzip
```

If native `unzip` is unavailable, omit that flag to perform a Python extraction and retain that narrower evidence label. An existing destination is a stop, not a cleanup request. Read [scenario checks](scenario-checks.md) before adapting the example to different dependency formats or requested transformations.
