# Offline Verification

Executed on 2026-10-02 with Python 3 and its standard library. No browser, live profile, network destination, converter or external validation service was used. The source and prepared HTML were parsed as text, not rendered as web pages.

Run `python3 check_example.py` from this folder. The checker reads the adjacent fictional artifacts without changing them. It is a bounded fixture checker, not a general-purpose HTML validator or proof of browser compatibility. Its parser rejects ambiguous structure and unexpected HTML elements instead of trying to repair them.

## What the check establishes

- The stored source and prepared digests match their actual bytes
- All 22 source items have an exact lineage row; native IDs remain separate from derived export-local IDs
- The 7 folders and 15 bookmark occurrences reconcile to 7 preserved source folders, 1 wrapper, 8 included links and 7 held links
- Ordered parent/child structure, empty folders, repeated folder names, duplicate multiplicity, blank title, Unicode, descriptions and exact URL strings match the planned transform
- Original attributes survive in the lineage record; carried metadata appears in the prepared file, while icon and toolbar metadata remain sidecar-only
- No held URL appears in the import file, and every target record accurately says that browser execution has not run

The checker independently traverses the source and transfer, computes the expected projection from occurrence records and compares complete ordered structures. It does not use a set of URLs, which would hide duplicate loss. Known fixture values also establish that the difficult cases are present.

## Deliberate failures detected

Each change below was applied to an in-memory copy. Output digests were recalculated for output mutations, so failure came from the structural/content checks rather than a stale checksum alone. No broken file replaced a deliverable.

| Mutation | Observed result |
| --- | --- |
| Remove one identical checklist occurrence | Rejected |
| Change one repeated folder's title | Rejected |
| Change an API URL query value | Rejected |
| Remove carried tags | Rejected |
| Append a byte to the original source | Rejected by source baseline check |
| Remove one lineage record | Rejected |
| Claim a target item was verified | Rejected |

## Executed result

```text
PASS: 7 source folders + 15 link occurrences = 7 retained folders + 8 included + 7 held links
PASS: hierarchy/order, repeated folder names, empty folders, Unicode, blank title, exact URLs
PASS: duplicate multiplicity, all original attributes/descriptions, source IDs and derived lineage
PASS: one wrapper; sidecar-only icon/toolbar metadata; no held URL in import file
PASS: source and prepared byte digests; no live-import claim
PASS negative control: duplicate occurrence removed
PASS negative control: folder identity/order changed
PASS negative control: URL changed
PASS negative control: metadata dropped
PASS negative control: original source changed
PASS negative control: lineage record removed
PASS negative control: unsupported live success claimed
Browser import, target recovery and destination reachability: NOT RUN
```

## Evidence limits

This establishes internal consistency of the fictional prepared transfer and its lineage record. The same small parser reads both HTML files, so agreement is not an independent browser-parser compatibility result. Import UI behavior, actual metadata retention, URL normalization, sync propagation, target-state preservation and rollback remain untested. The original fixture itself is the expected selection; it provides no evidence about a real browser's export completeness.

No bookmark was opened, and no URL was checked for reachability, safety or redirect behavior. A syntax result must not be described as a working-link result. A live import is complete only after the target-specific backup, pilot and reconciliation described in the skill are actually performed.

## Separate preparation rehearsal

A fresh guide-only case used three folders and six bookmark occurrences, with an explicit request to include `mailto` alongside HTTP(S). It produced actual transfer HTML and a sidecar: all three source folders plus the requested wrapper, four included links and two held browser/executable links. The result retained same-name sibling folders, same-folder duplicate links, an empty folder, a blank title and the requested mail link. It correctly decoded `R&amp;D &amp;amp; notes` once to the literal title `R&D &amp; notes` before re-escaping it for HTML. Source bytes remained unchanged.

The preparation finished without demanding an unchosen target browser. The guide now makes that branch explicit: target identity, backup and actual browser retention are prerequisites for live import, while file-only preparation can finish with those limits stated. This was another local data transformation, not a browser import or recovery test.
