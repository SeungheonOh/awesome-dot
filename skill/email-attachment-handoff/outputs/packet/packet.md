# Cedar attachment packet

This is a partial, usable local packet from five supplied fictional message occurrences.

Selected decoded files: 7. Original EML occurrences preserved: 5.

## Start with these files

- [route: s002:2](files/s002-part-2.txt) — 47 bytes; filename metadata is recorded in index.json
- [packing: s002:3](files/s002-part-3.txt) — 42 bytes; filename metadata is recorded in index.json
- [floor: s002:4](files/s002-part-4.txt) — 43 bytes; filename metadata is recorded in index.json
- [route: s003:2](files/s003-part-2.txt) — 47 bytes; filename metadata is recorded in index.json
- [packing: s003:3](files/s003-part-3.txt) — 42 bytes; filename metadata is recorded in index.json
- [floor: s003:4](files/s003-part-4.txt) — 43 bytes; filename metadata is recorded in index.json
- [packing: s004:2](files/s004-part-2.txt) — 42 bytes; filename metadata is recorded in index.json

## Unresolved requests

- **final count sheet:** Body s004:1 says both are provisional and neither has been chosen. Needed: Which count sheet was approved, or a supplied later approval/corrected attachment.
- **final door roster:** Body s004:1 says it is still to come; no top-level roster is supplied. s005:2 is an out-of-scope attached message, not a final top-level roster. Needed: The final roster as an authorized supplied file/message; expanding nested-message scope alone would not establish finality.

## Other held parts

- s004:5: held_malformed; Only base64 data is allowed
- s004:6: held_unsupported; unsupported transfer encoding: x-cedar-placeholder

The [index](index.json) maps each selected occurrence to original EML bytes, exact part ranges, encoded headers, decoded hashes and decision evidence. Repeated messages and identical payloads remain distinct occurrences.

Verification covers local parsing, transfer decoding, output readback and original preservation. It does not establish sender authenticity, account completeness, signature validity, successful decryption or compatibility with a live email client.
