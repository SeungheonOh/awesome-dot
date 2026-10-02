# Account export audit

Status: held

Keep a readable offline copy of the selected collection's current and archived notes, comments, deletion markers and original attachment bytes at the specified snapshot.

Selected snapshot: generation-42 at 2026-09-20T12:00:00Z.
Independent listing terminal and reconciled: true.

## Reconciliation

Objects: 5 expected = 2 matched + 3 missing + 0 conflicting.
Explicit exclusions: 1. Unexpected selected objects: 0.
Attachments: 1/2 matched; 39/95 bytes verified against separate control digests.
Missing required parts: [2]. Held archives: 1.

## Object inventory

- collection-007: matched; expected active revision 3; body absent
- note-0001: matched; expected active revision 4; body empty
- note-0002: missing; expected archived revision 7; body unavailable
- comment-0001: missing; expected active revision 1; body unavailable
- note-0003: missing; expected deleted revision 9; body unavailable

## Attachment inventory

- attachment-001 owned by note-0001: matched; expected 39 bytes; observed 39; attachments/attachment-001/notes.txt
- attachment-002 owned by note-0002: missing; expected 56 bytes; observed unavailable; attachments/attachment-002/notes.txt

## Explicit scope exclusions

- note-9000: different collection explicitly excluded

## Part decisions

- cobalt-part-1.zip: selected; Matches the requested snapshot identity; reconciliation still required.
- amber-part-2.zip: held; Different generation, snapshot_at, request_id; never used to fill this snapshot.

## Next action

No consolidated copy was created.

- Requested export parts are missing, repeated or unexpected.
- Required source objects or properties are missing or conflicting.
- Selected record attachment references do not equal the independently expected references.
- Attachment payloads, ownership or independent byte evidence are unresolved.

Supply the missing part from export-cobalt at generation-42. The later amber part cannot fill that gap.

## What this establishes

Coverage of the independently listed, filtered snapshot selection and the checked properties only. Archive totals are internal consistency checks. No live account or provider-wide completeness was checked.

- This is supplied fictional evidence, not an authenticated provider response.
- Record bodies have no independent content digest; presence and preserved values can be checked, but their fidelity to live source text cannot.
- The control lists only the stated selection and one explicit exclusion; it is not an inventory of the whole account.
- other collections
- earlier revision history
- deleted bodies
- account settings
- access permissions
- rich-text rendering
- destination import behavior
- post-snapshot changes
