# A second download fixes the gap; a newer snapshot does not

The request is to retain collection-007 as it existed at generation-42: current and archived note bodies, its comment, deletion markers and original attachment bytes. The copy need not include another collection, earlier revisions, deleted bodies, access permissions or rich-text rendering. The account and all content are fictional.

The independently supplied source inventory names five selected objects and one explicit exclusion. Its two listing pages form a terminal chain. A separate export-job control identifies parts 1 and 2 of export-cobalt. Attachment controls identify two owners and 95 expected bytes with source digests. These controls are fixture evidence supplied separately from the ZIPs; the audit does not create them by recounting an archive. They simulate an independently captured source listing, not authenticated provider evidence.

## Supplied data

| File | Evidence |
| --- | --- |
| [Need](fixtures/need.json) | Selected generation, filters and properties required for retention |
| [Source inventory](fixtures/source-inventory.csv) | Exact object IDs, kinds, lifecycle states, revisions, parents and expected references |
| [Source controls](fixtures/source-control.json) | Terminal independent listing, expected part IDs, original attachment sizes/digests and provenance limits |
| [Cobalt part 1](fixtures/archives/cobalt-part-1.zip) | Collection root, current note and attachment-001 |
| [Cobalt part 2](fixtures/archives/cobalt-part-2.zip) | Archived note, its comment, deletion marker and attachment-002 at the same generation |
| [Amber part 2](fixtures/archives/amber-part-2.zip) | A later generation's changed version of note-0002; not a replacement cobalt part |

The two attachments are both named notes.txt. Their attachment IDs and parent paths distinguish them. One current note has an intentionally empty body. The archived note has an explicit null color and a Unicode tag. The deletion marker has no body or attachment list; filling either with invented content would change its meaning.

## What the evidence changes

| Supplied evidence | Object result | Attachment result | Allowed output |
| --- | --- | --- | --- |
| Cobalt part 1 and later Amber part 2 | 2/5 matched, 3 missing | 1/2 matched, 39/95 bytes | Inventory and gap report; no consolidated copy |
| Both Cobalt parts plus Amber | 5/5 matched | 2/2 matched, 95/95 bytes | Coherent generation-42 copy; Amber remains held |
| All three archives but only the first independent listing page | All five supplied inventory IDs match | 95/95 bytes match | Source denominator is unconfirmed; no consolidated copy |

In the first case, note-0002 appears in the later archive but still counts as missing from generation-42. Its later revision 8 must not stand in for the expected revision 7. The comment, deletion marker and attachment-002 remain unavailable. The report's next step is precise: obtain part 2 from export-cobalt at generation-42.

The second case resolves that request. The saved [records](outputs/resolved/consolidated/records.json) contain all five original objects in the selected part order. The [lineage](outputs/resolved/consolidated/lineage.json) points every object to its archive digest and member index. Both [attachment-001](outputs/resolved/consolidated/attachments/attachment-001/notes.txt) and [attachment-002](outputs/resolved/consolidated/attachments/attachment-002/notes.txt) survive with their original bytes and distinct paths. Amber remains visible in the audit as held evidence; none of its fields enters the copy.

The third case prevents a tempting overclaim. The archive's own total is five, and five inventory rows match, but the supplied control chain stops at a continuation cursor. Agreement with visible rows cannot show that the source listing has ended. The report therefore distinguishes matching observed objects from supported coverage.

## Reproduce in a new local directory

No account access, installation, online converter or destination service is used. Run from the skill folder. Choose an unused output directory; the scripts refuse to overwrite a previous run.

```sh
python3 -B scripts/audit.py --fixtures fixtures \
  --archive fixtures/archives/cobalt-part-1.zip \
  --archive fixtures/archives/amber-part-2.zip \
  --output audit-run-partial

python3 -B scripts/audit.py --fixtures fixtures \
  --archive fixtures/archives/cobalt-part-1.zip \
  --archive fixtures/archives/cobalt-part-2.zip \
  --archive fixtures/archives/amber-part-2.zip \
  --output audit-run-resolved

python3 -B scripts/audit.py --fixtures fixtures \
  --archive fixtures/archives/cobalt-part-1.zip \
  --archive fixtures/archives/cobalt-part-2.zip \
  --archive fixtures/archives/amber-part-2.zip \
  --incomplete-control --output audit-run-incomplete-control

python3 -B scripts/verify.py
```

The optional [fixture builder](scripts/build_fixtures.py) reproduces the original ZIP bytes into a new directory with --output. It constructs only the fictional archive payloads; the independent source inventory and its expected attachment digests are separately authored fixture files. Verification rebuilds the archives in a temporary directory and compares their exact bytes with the distributed files.

The output establishes fidelity to the supplied selected snapshot evidence. It does not authenticate that evidence, compare record bodies to a live account, test native app rendering or show that any destination can import this format. No record body hash was independently supplied, so exact preservation from the selected archive is tested while live-source text fidelity remains unverified.
