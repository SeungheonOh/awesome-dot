# Verification of the Cedar Packet

Executed locally on 2 October 2026 with Python 3.12.14 and the installed standard library. The [reproducer](scripts/reproduce.py) was inspected before execution. The [saved packet](outputs/packet/packet.md) is an actual output, not a predicted result.

## Original-byte identities

All five input files match their corresponding saved originals byte for byte. The duplicate source remains two occurrences.

| Source | Bytes | SHA-256 |
| --- | ---: | --- |
| s001 | 1221 | `dae5bdf4b036aa03532bbafd798bd161a0b2a149e4a69f6f1c757f9f953e34a8` |
| s002 | 1210 | `67b69635d00196493688ee2eeb11de7c90bb3957f91ee1139a271162195048f0` |
| s003 | 1210 | `67b69635d00196493688ee2eeb11de7c90bb3957f91ee1139a271162195048f0` |
| s004 | 1548 | `cf0e3f6fa76d8a0df7e09feedff86a057b37dc4db4834865d6380731abf75651` |
| s005 | 1219 | `8102731c1ddf4139f3fd0b5a15498f637daa46458c92a94b2a963472edbe2368` |

These digests establish byte identities for the supplied fictional data, not author authenticity or unseen source coverage. Scoped Git attributes disable text normalization for original EML and selected payload files.

## Selected payload identities

The seven saved outputs independently match both the MIME-decoded source payloads and these explicit text values:

| Payload | Occurrences | Bytes each | SHA-256 |
| --- | --- | ---: | --- |
| Route revision B | s002:2, s003:2 | 47 | `2cb756523dd88d96dbb5da875583c2c26f8dc103bb9e1089af40a7542502e8e9` |
| Packing list | s002:3, s003:3, s004:2 | 42 | `6ec198c673061441d8b6dae92c51d91f8f24c445efff9d5ea374fe9c4de85a20` |
| Café floor plan | s002:4, s003:4 | 43 | `2bd4073f0e94db273a438418fb2449a1ef17715c7b41de30b0ad5dd2afc945e5` |

The route payload has CRLF line endings, the packing list has LF endings, and the UTF-8 café plan has no final newline. All three properties were checked as bytes, separately from readable-text comparison. Total selected decoded bytes are 306 across seven occurrence files.

## Saved-result checks

- Source EML hashes and lengths, copied-original equality, and unchanged supplied bytes after execution
- Independent byte-parser decoding of every selected part and strict base64 decoding of its exact wire payload slice
- Independent inspection of all recorded raw-header and body ranges; selected ranges exclude the boundary's encapsulation CRLF
- Exact RFC2231 filename continuation bytes and interpreted `café-floor-plan.txt` retained together
- Equal s002/s003 message bytes and Message-ID retained as separate source occurrences and outputs
- Equal packing bytes under s002, s003 and s004 retained as three separate occurrences
- Same-name different-content count sheets remain separate unresolved candidates; neither appears in delivered files
- Body alternatives, inline legend, nested attached-message content, malformed base64 and unsupported transfer encoding produce no selected outputs
- Fresh reproduction matches the included example packet's file membership and bytes
- A second attempt into the same output directory fails and leaves every existing output unchanged

## Changed-input checks

Changed-input runs use isolated copies of the fixture. The original fixture and example packet remain unchanged.

1. Change s002's reviewed body evidence while retaining the old reviewed-source digest. Six dependent selections are held. The independently supported s004 packing-list occurrence remains deliverable. Stale unresolved explanations are marked for reinspection
2. Change only the duplicate s003 source. Its three selected occurrences are held; the other four selected files remain deliverable. Equality of the original Message-ID never overrides the changed source bytes
3. Change s004's body to approve count-sheet A. Its old unresolved explanation is no longer asserted as current. The packet preserves it only as a labeled previously reviewed reason, marks changed evidence, and requires the reviewed selection to be refreshed before deciding the item

These checks establish invalidation of stale decisions; the fixture adapter does not infer a new approval from edited prose. An authorized real workflow must inspect new evidence, update the actual selection, and then deliver newly supported outputs.

## Additional independent readback

A separate inspected run reproduced every saved packet file exactly. Independent parser and wire-slice checks confirmed all seven selected occurrences and 306 decoded bytes, including the distinct line endings and final-newline states. Fresh valid and invalid quoted-printable and 7bit inputs checked exact decoding or a held result. Changing only the excluded attached-message source left the seven independent selected files usable while marking the roster explanation as based on changed evidence. Existing-destination refusal preserved the previous packet. These are local MIME and file checks within the stated adapter scope.

## Limits and reproduction

The helper supports this five-source layout with CRLF MIME wire lines, a 64 KiB bound per source, at most 40 visited parts per source and a depth bound of 6. It supports plain-text attachment payloads with base64, quoted-printable or 7bit transfer encoding; the delivered example exercises base64. Its raw-range locator is paired with the parsed fixture tree and is not a general MIME implementation. Unsupported structure can stop a run before any output is written.

Signed/encrypted entity handling is a preservation/hold rule, not an exercised cryptographic workflow. No actual signature validation or decryption was performed. No attachment was executed; HTML was not rendered; no link/image was fetched; no mailbox, account, external service, converter installation or live email client was used. MBOX/PST import, mailbox flags/folders, sender authenticity and target-application compatibility were not tested.

From this skill folder, inspect the helper and run with an absent local destination:

```sh
python3 -B scripts/reproduce.py --out my-attachment-packet
```

Read `my-attachment-packet/packet.md` and `index.json`, then compare the actual files with the source part locators. The existing-directory refusal is deliberate; use a different new directory for another run.
