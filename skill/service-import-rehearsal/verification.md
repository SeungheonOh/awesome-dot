# Verification evidence

The offline rehearsal and behavioral checks were executed successfully with Python 3 on 2 October 2026. No service was contacted and no account was changed. Fictional partial-result evidence is evaluated at its supplied timestamp, 12 January 2026 at 10:01 UTC, rather than the execution date.

## Executed checks

```sh
python3 scripts/rehearse.py --fixtures fixtures --output outputs
python3 scripts/verify.py
```

The rehearsal generated and reopened eight artifacts: two machine CSV files and six JSON files. The source is unchanged. The import-ready subset has five unique identities and exact saved-file round-trip equality. All 16 source records have one primary disposition, and all five submitted-candidate records have one fictional recovery outcome.

The behavioral check script passes 37 checks covering:

- All five operation dispositions, exact duplicate lineage, conflicting duplicate groups and crossed internal/external IDs
- Truncated exports, incomplete lookups and one visible match without authoritative uniqueness evidence
- Leading zeros, Unicode, quoted commas, logical CSV record numbering with embedded newlines, literal formula-like strings, blank preservation, explicit clear and create defaults
- Immutable operation digests and changed-payload identity, deterministic artifacts, source preservation and parser readback
- Partial success, unknown/incomplete readback, expired replay retention, contradictory success receipts, equal values under the wrong record ID, and desired state without proof of operation causality
- Same-key retry candidate restricted to the one eligible unchanged original operation
- Cross-account evidence, contradictory snapshots, duplicated receipts, duplicate headers and ragged records rejected without submission

The skill frontmatter and naming validator passed. The bounded public hygiene scan passed for the finished folder. These structural and pattern checks complement the executed behavior checks; they do not establish live product correctness or prove absence of every possible disclosure.

An independent guide-only case used a different seven-row fictional contract with exact keys `001` and `1`, an explicit `CLEAR` token and no documented replay facility. It produced an actual three-row candidate CSV, preserving the leading-zero distinction and Unicode: two updates and one create. It excluded one already-equal row and three ambiguous rows, including both sides of a conflicting pair. The supplied partial outcome was correctly split into confirmed applied, desired state with unknown creator, and unchanged current state with no terminal outcome. No retry file was emitted. The case did not use the bundled adapter or assume its idempotency guarantees.

Another independent case reversed the example's blank-cell meaning and used a reserved leave-unchanged token. The resulting plan applied the supplied blank-as-clear rule, rejected an intended literal token with no supported escape, and held a lost-response create without replay support. That review clarified three general instructions: retain unchanged fields when an importer requires them, keep identical same-key repeats ambiguous without a duplicate-export rule, and handle every reserved control token rather than only explicit clears. These guide refinements do not change the bundled fictional adapter's contract or output.

## Evidence limits

The helper is a narrow, offline adapter for the supplied fictional contract, not a universal importer. It does not upload files, emulate a real service's parser, test transaction isolation, enforce remote permissions, prove real idempotency, or observe downstream effects. The initial source-to-target mapping and lookup evidence are supplied fixture premises. Unknown identity existence remains blocked even if the rest of the CSV is valid.

The generated machine CSV intentionally preserves formula-like strings because this fictional target stores them literally. Open the JSON plan for review. A real spreadsheet or service may interpret these cells differently, and that behavior must be established before adaptation.

Readback can establish current state without establishing its cause. The fictional retry candidate is safe only under the explicit same-key/same-payload replay rule, retention window, strong lookup semantics and atomic uniqueness assumption. A successful replay still requires fresh readback; returning an earlier receipt need not restore an object that someone subsequently removed.
