---
name: document-filing-pass
description: "Organize an authorized document collection with evidence-based names and folders, verified same-service moves, stable file IDs and a reversible change manifest."
---

# File Documents Without Losing Their Identity

Turn a bounded inbox of documents into a usable collection. Apply clear, already-authorized ordinary renames and moves within the same service; leave ambiguous items reviewable. Preserve the files, their stable identifiers and their effective access.

## Define the collection and permitted changes

Identify the service/account, source folder IDs or explicitly selected file IDs, whether subfolders are included, destination folder IDs and the requested naming convention. Resolve folder identity from the service, not a matching display name alone. Record exclusions and where the private change manifest should be kept.

Confirm the action boundary from the user's request: preview only, or execute clear moves/renames. If the user asks to organize a specific collection, ordinary moves and renames within that scope do not need repeated approval. Ask about an unclear collection or destination before mutating it. Do not treat a broad account search as permission to reorganize the account.

Check destination ownership and effective access before planning a move. A same-service move can change inherited access or cross a shared-drive boundary. Hold those changes for the user's decision; do not change sharing, ownership or retention controls as part of this workflow. Create a missing private folder only when its location and creation are within the requested organization scope and its inherited access is verified.

## Workflow

### 1. Inventory by metadata, then read only what is needed

List the bounded collection with pagination. Capture stable file ID, current name, parent IDs, file type, revision/ETag, modified time, size where meaningful, available content checksum and ownership/access evidence. Record shortcuts as shortcuts and resolve their targets only when the request includes them; moving a shortcut does not file its target.

Start with metadata and useful existing names. Open only the page, header, tab or excerpt needed to establish type, issuer, document date and relevant reference. For a scanned file, use authorized local or same-service text extraction when available; do not upload it to a new OCR service without permission. A failed extraction is a held classification, not a reason to read every other file.

Avoid unnecessary personal details in names or logs. Do not infer passwords, account identifiers, health conditions or other private facts from context. If a needed field would expose sensitive information in a filename, use a neutral label and preserve the evidence reference privately. An encrypted or inaccessible document remains unopened; do not bypass access controls or ask for a password in chat.

### 2. Classify and construct names from evidence

For each file build a proposed row: stable ID, current state, proposed name/parent, document kind, extracted naming fields, concise evidence locator, confidence reason and disposition. Use a small set of destinations already requested or clearly established in that collection.

Apply these distinctions:

- Use the document's evidenced issue/event date required by the convention, not upload or modification time. Keep invoice date, payment date and service date separate.
- Resolve numeric dates such as `03/04/26` only from reliable context. Preserve unknown or partial precision rather than inventing a day.
- Use a reference number only when it belongs to the document, not an unrelated account or tracking number. Preserve meaningful leading zeroes.
- Keep the native file type and extension; renaming a file does not convert its format. Do not add an extension to a native document that normally has none.
- Normalize only filenames: forbidden characters, length and known service-specific comparison rules. Do not alter document contents to make the name fit.

If the convention cannot express an undated manual or other clear document type, propose a narrow exception, such as `Issuer_Model_User-Manual.pdf`, instead of fabricating a date. Apply an exception directly only when the convention or user's instructions already allow it.

### 3. Separate collisions, duplicates and uncertain identities

Check proposed names against existing destination items and other planned changes using the service's actual case/normalization rules. A service that permits same-name files can still leave the collection ambiguous.

A filename collision does not prove duplicate content. For clearly distinct documents, use the user's collision rule or preview a stable suffix before applying it. Prefer a harmless document reference or a short stable file-ID suffix when appropriate. Recheck that the suffix itself is unique; do not overwrite, replace or append a random counter without recording it.

A matching trustworthy byte checksum can establish identical bytes for ordinary binary files. It does not authorize deletion or merging of records. Identical names, size, dates or similar text do not establish identical bytes; native cloud documents and shortcuts may need a different supported comparison. Keep suspected duplicates and alternate versions distinct in the manifest. If the user says to leave duplicates untouched, hold every member of the duplicate group; do not silently pick and move a canonical representative. Apply a representative-specific treatment only when the user’s rule or explicit selection authorizes it. Do not export private documents solely to compute hashes unless that export is authorized and necessary.

Preview uncertain classifications, conflicting dates, ambiguous versions, unresolved collisions and access-changing moves with the smallest decision needed. Continue independent clear files while those rows remain held. Do not make a confident-looking filename the substitute for missing evidence.

### 4. Freeze a reversible plan

Before the first change, save a private manifest containing:

- Service/account scope, run timestamp, authorized source IDs and destination IDs
- File ID and complete before state: name, parent IDs, revision and relevant access evidence
- Proposed after state and the evidence used for classification
- Disposition: execute, held for review, excluded or already correct
- Ordered planned operations, their preconditions, status and eventual readback evidence
- Collision/duplicate relationships and a recovery instruction for each applied change

Use stable IDs for actions and links returned by the service. Do not invent file URLs or use a path/name as the sole identity. Store only metadata necessary to explain and reverse the operation; a manifest is not a second copy of the document's private contents. If the manifest cannot be saved reliably, return the preview and stop before mutations.

The [fictional manifest](manifest.json) demonstrates this record shape. Read the [worked example](example.md) for its naming decisions and recovery checks. It is a fixture, not a connector request payload.

### 5. Apply clear authorized changes with preconditions

For each executable row:

1. Read the file and target folder again by ID. Confirm the recorded name, parents, revision, target identity and access still match the plan. If content or metadata changed, hold that row and refresh its evidence; do not overwrite another person's work.
2. Check for a new destination collision. Do not rely on the earlier listing after another process may have written there.
3. Use the service's ordinary metadata update/move action. Prefer an atomic update with a revision precondition if supported. Otherwise sequence the minimal rename and move, recording the verified intermediate state after each. Never implement a move as download, reupload and delete: that loses identity and may change access/history.
4. Read back by the same stable ID. Check name, exact parent set, unchanged file type, ownership and effective access. Confirm the content checksum is unchanged when the service provides a reliable one; native-document revisions can change on metadata edits without proving content changed.
5. Mark the operation verified only after readback. Record a failure or uncertainty honestly. On a timeout or ambiguous response, inspect current state before retrying; an operation may already have succeeded. Do not create a duplicate operation by guessing.

If rename succeeded but move failed, record the actual intermediate state as partially applied and decide recovery from that state. Preserve multi-parent semantics and handle shared-drive moves only when their special behavior is understood and authorized. Otherwise hold them. If an unexpected access change is detected, stop that batch, report the exact discrepancy and seek the needed recovery decision; do not improvise permission changes.

### 6. Reconcile and deliver the completed pass

Re-list the authorized scope and look up moved files by ID. Every initial file must reconcile to exactly one manifest row: verified change, held, excluded or already correct. Check that no source file vanished and no new file was created to simulate a move. Ensure the manifest's observed state matches the service, not merely the intended plan.

Return a concise result with the verified destination links, what actually changed, held decisions and a private manifest link or file. Do not copy document contents into the summary. If some files were inaccessible or a list page failed, state that coverage limit rather than claiming the collection is complete.

For an authorized later reversal, process verified operations in reverse order, using file IDs. First verify that the current state matches the recorded post-change state, the old destination still exists, access would remain appropriate and the restored name has no new collision. If any precondition fails, stop that row for review. Read back each reversal and append its result; keep the original journal. A reversible manifest does not itself authorize a future rollback or unrelated changes.

## Stop conditions

- Missing collection or destination identity: prepare only the bounded inventory you can establish
- Ambiguous evidence or a concurrent edit: hold the affected row and continue independent rows
- Access expansion, ownership transfer, deletion, file-content edits or external uploads: outside this filing pass unless separately authorized under the applicable rules
- Uncertain mutation result: inspect before retrying and report it unresolved if verification is unavailable

## Example request

```text
dot, organize the PDFs in this specific inbox folder into the existing Receipts, Invoices and Manuals folders in the same account. Rename clear files using their document date, issuer, type and printed reference, while keeping undated manuals named by issuer and model. Preserve file IDs and access. Use my approved suffix rule for genuinely distinct same-name documents. Leave ambiguous dates and possible duplicates untouched, show me those decisions and save a reversible manifest in the private project folder. Do not delete anything or change sharing.
```

## Evidence status

The example is wholly fictional and its local checker verifies manifest consistency. A real filing pass requires service readbacks to establish moves, unchanged identities and effective access. Local fixture checks cannot establish those external results.
