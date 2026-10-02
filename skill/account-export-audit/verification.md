# Executed offline verification

Executed on 2026-10-02 with Python 3.12.14 on Linux. The example uses only Python's standard library: archive inspection, JSON/CSV parsing, hashing, local file writes and temporary fictional fixtures. It performs no account requests, installation, upload, import or source deletion.

## Saved outcomes

| Case | Selected object accounting | Attachment accounting | Copy result |
| --- | --- | --- | --- |
| Partial | 5 expected = 2 matched + 3 missing + 0 conflicting | 1/2 payloads; 39/95 matched bytes | Held; no consolidated directory |
| Resolved | 5 expected = 5 matched + 0 missing + 0 conflicting | 2/2 payloads; 95/95 matched bytes | Five exact raw objects and two original payloads saved |
| Incomplete independent control | 5 supplied inventory IDs match; denominator not confirmed | 2/2 payloads; 95/95 matched bytes | Held despite matching archive totals |

Every case identifies note-9000 as an explicit different-collection exclusion. The later Amber archive stays held in every case. The resolved copy retains note-0002 revision 7 and its original title/body, not the later revision 8. The two payloads named notes.txt remain distinct through their attachment-ID paths.

## Executed checks

`python3 -B scripts/verify.py` passes 19 checks:

1. Reproduce every saved output byte in a new temporary directory and verify all supplied fixtures stay unchanged
2. Rebuild each original ZIP deterministically and compare exact archive bytes
3. Independently parse the CSV controls, selected ZIP records and saved copy; reconcile exact IDs, count uniqueness, kinds, states, revisions, parents, reference lists and 95 attachment bytes against separately supplied hashes
4. Preserve the empty body, omitted optional field, explicit null, Unicode tag and tombstone's absent fields distinctly
5. Keep a missing generation-42 object missing when it appears only in generation-43
6. Permit the resolved generation-42 copy while preserving the later archive's held disposition
7. Withhold consolidation when the independent listing has an unresolved continuation cursor, even though all visible objects and bytes match
8. Treat an omitted required body differently from a valid empty body
9. Detect a same-length attachment byte change through its independent digest
10. Detect an equal-total export in which one expected identity was replaced by an unexpected identity
11. Hold repeated part/record identities without choosing a first or last winner
12. Refuse an existing output directory without changing its contents
13. Refuse a benign archive with more than the configured member limit
14. Hold a required attachment when both its independent control row and payload are absent, keeping two expected references and an unknown byte total rather than silently reducing the denominator
15. Hold repeated attachment controls without counting their bytes twice
16. Produce only the audit for an audit-only request, even when a complete snapshot copy would otherwise be supported
17. Reject string, numeric, null, array, object or missing consolidation-authority values before creating any output; accept only JSON booleans and keep the copy-result field boolean
18. Reject unsupported body-presence values and labels that would weaken a selected note/comment's required body, including when the actual exported body is missing
19. Reject noncanonical or empty inventory scope markers before output instead of silently dropping rows from both the selected and excluded sets

The archive-boundary countercase contains only 33 tiny ordinary text members. No exploitation payload or network target is part of the checks. The helper also checks its supported member layout, regular-file types, case-folded name collisions, per-member/total expanded bytes, expansion ratio, encryption, supported compression, explicit part cursors, JSON duplicate keys and schema. These protections are intentionally bounded to the fictional layout; the listed checks do not establish support for all ZIP formats or hostile input classes.

Skill frontmatter validation passes. Local Markdown links were checked against existing files. The archive contents were decoded and inspected as JSON and UTF-8 text; no executable members, active content, credentials or real account data are included.

An independent forward test read the skill and raw fixtures before consulting saved outcomes. It confirmed both evidence transitions, all required relationships and body-presence distinctions, attachment ownership/digests and exact saved-record preservation. It also exercised the omitted attachment-control-and-payload countercase. After the cross-control check was corrected, independent reruns confirmed that this case stays held with two required references, an unknown total byte denominator and no consolidated copy. The normal partial/resolved results still pass, and original fixture hashes remain unchanged.

A second independent review inspected the adapter and reran all 19 checks in an isolated copy. It confirmed exact output and archive reproduction, then verified that non-boolean consolidation authority, unsupported scope markers and body controls cannot silently authorize a copy or weaken required coverage. The original fixtures and saved output bytes stayed unchanged. This review remained within the fictional format; no account or destination service was contacted.

## Exact input archives

All three ZIPs use stored members and total 4,076 bytes. Each member is a regular data file. Their identities are:

| Archive | Bytes | SHA-256 |
| --- | ---: | --- |
| amber-part-2.zip | 1,069 | f3b2db50368057f8118a974a9b8d61dc73d752d78081d328845a3fd963bf0b44 |
| cobalt-part-1.zip | 1,341 | 8b239906387b7a08ee345cf2e3619f6662867df2954c12d3d33664ad29ea315f |
| cobalt-part-2.zip | 1,666 | 375cbf30b470752159b2de4c5662ec8d104cdf52e93714ddec2f2e41c32e9523 |

Amber contains manifest.json (514 bytes) and records.json (331 bytes). Cobalt part 1 contains manifest.json (515), records.json (415) and attachments/attachment-001/notes.txt (39). Cobalt part 2 contains manifest.json (515), records.json (723) and attachments/attachment-002/notes.txt (56).

Attachment-001 SHA-256 is cd7a452074c6aad9f029042d8ab52c66d9a325bfc76199f9b787036f7e958f80. Attachment-002 SHA-256 is 08cf429a3a5a0631ef504348437dfd8b820bdea1080d7f50193c0771060fd7f6. Both independently declared control values agree with their selected archive payloads and saved copies.

## Scope of the evidence

The independent control is separately authored fictional source evidence, not an authenticated live response. Its shape exercises what a real independent selection, paginated listing and export-job receipt must establish. It cannot prove that a provider generated these files or that a whole account was exported.

The checks establish the selected raw records' preservation from the chosen archives, relationship coherence, explicit lifecycle/field semantics, and the attachments' byte relationship to separately supplied control digests. They do not establish record-body fidelity to a live source because no independent body digests were supplied. They also do not check provider export omissions, inaccessible source objects, native rendering, historical revision recovery, current account state, destination import behavior or retention/legal sufficiency. A different real schema requires an inspected adapter and evidence for its semantics.

No result supports account closure or deletion of the original account/export. The resolved copy is a useful bounded retention artifact under the stated requirement, not a tested migration or a complete account backup.
