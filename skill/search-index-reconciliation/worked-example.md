# A packing note is current, but search still finds its old wording

This original fictional application has three workshop notes. The source table changes after the first index build; the application deliberately performs no index maintenance. The task is to explain why searching for the updated note fails and to prepare a separate candidate for that fixed snapshot.

All work ran locally with Python 3.12.14, its installed `sqlite3` module and SQLite 3.53.1. No real collection, external account, extension installation, application UI or OS search setting was involved.

## Source identity and search contract

The complete input is [fixture.json](examples/fixture.json). There are no filters or access rules in this fixture; all three current documents have nonempty indexed text. Revisions belong to the source, not to an independent record of when the index was built.

| Stable ID | Initial source | Current source | What happened |
| --- | --- | --- | --- |
| 101 | Revision 1: “Pack amber crates beside the north rack.” | Revision 2: “Pack cobalt crates beside the east rack.” | Same document edited |
| 102 | Revision 1: Café meeting note, with résumé and handover terms | Same row and text | Unchanged control |
| 103 | Revision 1: saffron labels | Absent | Deleted |
| 104 | Absent | Revision 1: mint toolkit | Added |

The schema uses `doc_id INTEGER PRIMARY KEY` and `revision INTEGER NOT NULL`. The external-content FTS5 table indexes `title` and `body` with `content='documents'`, `content_rowid='doc_id'` and `tokenize='unicode61 remove_diacritics 0'`. No synchronization triggers are created. The runner builds the initial index, then applies the source edits, addition and deletion without maintaining it.

The captured source still has three rows. This count hides the replacement of ID 103 by ID 104. An ordinary FTS read also returns three rows, including the new ID 104 and ID 101's current cobalt text. The index's token postings instead cover 101, 102 and 103. The distinct posting IDs come from a temporary `fts5vocab` instance table on a memory copy, not from `SELECT count(*)` on the external-content table.

## Actual query ledger

Each expression below was passed as a bound value to this query:

```sql
SELECT rowid FROM documents_fts
WHERE documents_fts MATCH ? ORDER BY rowid;
```

Source rows were resolved separately by ID so that the deleted document's posting was not hidden by a join. “None” means no matching IDs for that exact expression.

| Expression | Preserved stale original | Rebuilt candidate | Finding |
| --- | --- | --- | --- |
| `cobalt` | None | 101 | Current wording becomes searchable |
| `amber` | 101 | None | Retired wording stops finding 101 |
| `mint` | None | 104 | New document gains its posting |
| `saffron` | 103 | None | Deleted document's posting is removed |
| `handover` | 102 | 102 | Unchanged content stays searchable |
| `café` | 102 | 102 | Accented token works |
| `cafe` | None | None | Accent behavior is unchanged |
| `résumé` | 102 | 102 | Accented body token works |
| `resume` | None | None | Unaccented spelling remains different |
| `cobal*` | None | 101 | Explicit prefix finds the current token |
| `balt` | None | None | Interior substring does not become a match |
| `title:orchard` | 101 | 101 | Correct field restriction works |
| `body:orchard` | None | None | Wrong field remains empty |

A separate actual query for `amber` selecting the FTS `body` returned `(101, 'Pack cobalt crates beside the east rack.')`. That current-looking display accompanied an old-term hit. For deleted ID 103, the rowid-only query returned the posting while a separate source lookup found no row. Reading its missing body directly through FTS raised an error on the tested engine, so the evidence records posting IDs and source existence separately.

The stale original passed FTS's internal-only check. Its content-comparing check, `INSERT INTO documents_fts(documents_fts, rank) VALUES ('integrity-check', 1)`, failed with `SQLITE_CORRUPT_VTAB` and the message “database disk image is malformed.” Here the known cause is the intentional source/index mismatch; that error text alone is not a diagnosis of physical file damage. Both checks passed for the candidate. See the [engine reference](references/sqlite-behavior.md) for the comparison scope.

## Produce the candidate without changing the original

Use Python 3.11 or later linked to SQLite with FTS5 available; the captured runtime is listed above. From this skill's directory, use a new child directory whose parent already exists:

```bash
python scripts/rehearse_index.py ./alder-reconciliation-run
```

The stdlib-only runner reads only its bundled fixture. It never accepts an existing database to repair. The fixture is bounded to 12 documents per source snapshot, 1,000 characters per text field, 24 queries and a 32 KiB JSON input.

The output contains:

- `original-stale.sqlite`: the preserved source snapshot and deliberately stale index
- `candidate-rebuilt.sqlite`: a separate database with the same source rows and schema, with only its index rebuilt
- `query-ledger.json`: exact queries, matching IDs, independently resolved source rows, indexed token instances, coverage sets, checks, versions and file identities

The runner closes the original before copying it and requires no journal/WAL sidecar. That procedure is specific to this tiny fixture with no other writers. Diagnostic `INSERT` commands run only in memory copies made from read-only disk connections. After the stale original is preserved, only the candidate receives the repair rebuild. Existing output directories, files and symlinks are refused, preserving prior evidence.

For the captured run, both databases were 24,576 bytes. The candidate matched the original byte-for-byte before rebuilding. Their final SHA-256 values were:

- Original: `c329cb1c858434bd74aa18f2e272b8a4864a712561663ccce5b6729e687bc676`
- Candidate: `e9a9ad3dd4010b01963f1f8ef11ee0796e79ce1567ee35ab538b75c6ce5dbd83`

All source rows and revisions, including their full text, compared equal between original and candidate. Schema and tokenizer compared equal. The original hash stayed unchanged, and reopening/inspecting the candidate did not alter its hash. Candidate posting IDs were exactly 101, 102 and 104. The [captured results](examples/captured-results.json) record the fixture hash and evidence. That file is a curated projection of the fuller `query-ledger.json`, with the two separately executed FTS content probes included; it is not the raw runner output schema. A different SQLite version may serialize database bytes differently; compare each run's preservation and semantic results rather than requiring these historical hashes.

Binary databases are regenerated by the runner; the example distributes their source fixture and captured evidence. Retain a generated candidate as a reusable local result. It is not automatically installed anywhere.

## Checks beyond the baseline

A separate check program inspected the generated databases without importing the runner or trusting its claimed pass flags. It ran the 13 query pairs directly, compared source rows and revisions, ran content checks on independent memory backups and verified byte preservation before and after readback.

Changed-input execution then replaced ID 101's current term with `ultramarine` at revision 3, added `amber` to the current ID 104, and added unchanged ID 105 with `copper` to both snapshots. The fresh candidate found `ultramarine` at 101, `amber` at 104 and `copper` at 105, while `cobalt` returned no IDs. This checked that results followed changed input and that “retired from one document” did not mean “forbidden everywhere.” Existing output directory, file and symlink cases all refused execution without changing their contents or targets.

Finally, on a third copy only, a later edit advanced ID 101 to `indigo` after rebuilding. `cobalt` still matched and `indigo` did not; the content-comparing check failed again. The preserved original and candidate remained unchanged. This demonstrates that the result belongs to an exact source snapshot. The missing maintenance path remains deliberately unimplemented.

## Additional independent readback

A fresh inspected run matched the captured fields, all 13 query pairs and both database identities. Additional case, phrase, conjunction and column-restricted searches followed the stated semantics; malformed query syntax remained an error. A revision-only edit to non-indexed metadata on a disposable memory copy left term consistency intact. This distinguishes source-version provenance from a claim that searchable words are stale. Original and candidate disk bytes stayed unchanged, and an occupied output was refused without replacing it.

## What the result establishes

The saved candidate's index matches this complete three-document source snapshot, preserves the selected search semantics, and passes the exercised queries and consistency checks. It does not establish access behavior, completeness of an upstream collection, all possible search relevance, application UI behavior, production load tolerance or crash durability. There is no live promotion in this example. An actual application needs its supported maintenance path and authorized handoff verified before treating a repaired snapshot as an ongoing solution.
