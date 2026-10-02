# Cedar Reading-Room Attachment Packet

All people, addresses, message bodies and files here were created for this example. No mailbox, external link or remote resource was accessed. The fixture is a small collection of exported messages, not evidence of account completeness.

## Request and supplied evidence

> Prepare a local packet of the corrected route note, packing list and café floor plan. Retain every selected occurrence with the original messages. Also resolve the final count sheet and final door roster if these supplied top-level messages support them. Leave files inside attached messages outside the selection. Report anything unresolved.

The [reviewed selection](fixtures/selection.json) fixes the source hashes and part identities before delivery. Source IDs identify supplied file occurrences, not Message-IDs.

| Source | Supplied message | What it establishes |
| --- | --- | --- |
| s001 | [28 September draft](fixtures/messages/message-001.eml) | Route revision A, plus alternative body parts and a related inline legend |
| s002 | [29 September correction](fixtures/messages/message-002.eml) | “Revision B replaces my 28 September route note.” Includes route B, packing list and café floor plan |
| s003 | [Second supplied copy](fixtures/messages/message-003.eml) | Exactly the same EML bytes and Message-ID as s002, retained as a distinct source occurrence |
| s004 | [30 September follow-up](fixtures/messages/message-004.eml) | Confirms route B, repeats the packing list, leaves two count sheets provisional, and says the final door roster is still to come |
| s005 | [Forwarded context](fixtures/messages/message-005.eml) | Contains an attached earlier message. Its inner draft roster is outside the requested selection and does not establish a final roster |

These messages are source evidence for the fictional selection, not independent proof that the named sender is authentic. The local source-occurrence/part notation starts at `root`, numbers immediate children from `1`, and joins deeper paths with dots. Nested-message traversal is deliberately stopped at the `message/rfc822` container.

## The revision decision is based on text, not sorting

The same display filename `route-note.txt` labels A and B, but their decoded bytes differ. The correction in s002:1 names A's date and replaces it with B; s004:1 confirms B. Both s002:2 and s003:2 are selected because every supplied occurrence was requested. s001:2 remains excluded as the earlier revision.

The files `../handoff/count-sheet.txt` at s004:3 and s004:4 have different contents: 24 chairs versus 26. s004:1 expressly calls both provisional. No timestamp, filename or ordering rule picks a winner. Their filenames are retained only as metadata and never become output paths. The packet asks which option was approved or for a supplied later correction.

No final top-level door roster is supplied. An old roster inside s005's attached correspondence neither changes the explicit nested-message exclusion nor proves finality. The missing outcome stays visible instead of being filled with a plausible-looking draft.

## What was actually delivered

Open the [packet entry document](outputs/packet/packet.md). The actual local result contains seven selected occurrence files, five byte-identical EML copies, and the [index](outputs/packet/index.json).

| Requested deliverable | Decoded output occurrences | Result |
| --- | --- | --- |
| Corrected route note | [s002:2](outputs/packet/files/s002-part-2.txt), [s003:2](outputs/packet/files/s003-part-2.txt) | Revision B; 47 bytes each; CRLF endings |
| Packing list | [s002:3](outputs/packet/files/s002-part-3.txt), [s003:3](outputs/packet/files/s003-part-3.txt), [s004:2](outputs/packet/files/s004-part-2.txt) | Equal bytes in three distinct occurrences; 42 bytes each; LF endings |
| Café floor plan | [s002:4](outputs/packet/files/s002-part-4.txt), [s003:4](outputs/packet/files/s003-part-4.txt) | 43 UTF-8 bytes each; contains é; no final newline |
| Final count sheet | None | Two provisional candidates; selection unresolved |
| Final door roster | None | Requested final file absent from the selected scope |

Thus 3 of 5 logical deliverables are ready, represented by 7 occurrence files totaling 306 decoded bytes. There are 3 distinct selected payload byte values; that does not reduce the occurrence count. The packet is explicitly partial.

The 12 ordinary top-level text-attachment occurrences reconcile as 7 selected, 1 superseded, 2 unresolved candidates, 1 malformed base64 hold and 1 unsupported transfer-encoding hold. The attached-message container is separately excluded. Body/alternative and related-resource parts are inventoried but not delivered as requested files.

## Filename and wire-byte evidence

The café filename arrives as these folded header lines, preserved in the original messages and index:

```text
Content-Disposition: attachment;
 filename*0*=utf-8'en'caf%C3%A9-;
 filename*1*=floor-plan.txt
```

The interpreted display value is `café-floor-plan.txt`. The output name is the local identity `s002-part-4.txt` or `s003-part-4.txt`. Both encoded syntax and display interpretation survive; neither controls an output path.

Every part's `wire_range`, `header_range` and `payload_range` in the index are half-open byte offsets `[start, end)` in its saved original EML. `raw_headers_latin1` is a reversible representation of those header bytes, not a claim that the sender used a Latin-1 text charset. Transfer decoding is separate from interpreting the attachment's UTF-8 text.

The base64-damaged part s004:5 and unknown `x-cedar-placeholder` transfer encoding s004:6 are retained only in original evidence and the inventory. Their returned/recoverable text is not released as a verified attachment. HTML and its link are stored only as original message data; the HTML was not rendered and the link was not opened.

## Reproduce and understand the boundary

From this skill folder, use a new destination:

```sh
python3 -B scripts/reproduce.py --out my-attachment-packet
```

The installed Python standard library parses the five fixture messages, checks supported decoding, writes seven selected files and copies the originals, then reads the saved bytes back. The helper keeps separate sources even when hashes and Message-IDs match. It refuses an existing destination. It is deliberately limited to this fixture, its CRLF wire representation, fixed source identities and small part/size bounds.

The [verification record](verification.md) distinguishes the executed packet checks from untested sender authenticity, signature/decryption processing, live email-client behavior and general MIME-format support. An ordinary local packet is the requested deliverable; no ZIP, upload, email, account operation or import was performed.
