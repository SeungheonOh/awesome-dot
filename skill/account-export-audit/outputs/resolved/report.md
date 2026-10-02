# Account export audit

Status: supported-for-stated-snapshot-copy

Keep a readable offline copy of the selected collection's current and archived notes, comments, deletion markers and original attachment bytes at the specified snapshot.

Selected snapshot: generation-42 at 2026-09-20T12:00:00Z.
Independent listing terminal and reconciled: true.

## Reconciliation

Objects: 5 expected = 5 matched + 0 missing + 0 conflicting.
Explicit exclusions: 1. Unexpected selected objects: 0.
Attachments: 2/2 matched; 95/95 bytes verified against separate control digests.
Missing required parts: none. Held archives: 1.

## Object inventory

- collection-007: matched; expected active revision 3; body absent
- note-0001: matched; expected active revision 4; body empty
- note-0002: matched; expected archived revision 7; body present
- comment-0001: matched; expected active revision 1; body present
- note-0003: matched; expected deleted revision 9; body absent

## Attachment inventory

- attachment-001 owned by note-0001: matched; expected 39 bytes; observed 39; attachments/attachment-001/notes.txt
- attachment-002 owned by note-0002: matched; expected 56 bytes; observed 56; attachments/attachment-002/notes.txt

## Explicit scope exclusions

- note-9000: different collection explicitly excluded

## Part decisions

- cobalt-part-1.zip: selected; Matches the requested snapshot identity; reconciliation still required.
- cobalt-part-2.zip: selected; Matches the requested snapshot identity; reconciliation still required.
- amber-part-2.zip: held; Different generation, snapshot_at, request_id; never used to fill this snapshot.

## Next action

The consolidated copy preserves all five selected raw objects and both attachment payloads. Keep the held later archive separate. Destination import behavior needs a separate rehearsal.

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
