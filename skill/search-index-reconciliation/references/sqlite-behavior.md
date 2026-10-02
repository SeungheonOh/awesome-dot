# SQLite behavior used here

Checked against the primary documentation on 2026-10-02. These are engine contracts; the worked example records observed results separately.

- External-content FTS5 uses a separate content table. Its index must be maintained by the application. Ordinary reads can resolve through that content table, while `MATCH` obtains IDs from index postings. Current-looking returned text therefore does not demonstrate freshness. [External content and its pitfalls](https://www.sqlite.org/fts5.html#external_content_and_contentless_tables)
- For an external-content table, `integrity-check` with `rank=1` additionally compares index and content. The default check does not perform that comparison. These commands use `INSERT` syntax; the fixture runs diagnostic checks in disposable memory copies. [Integrity check](https://www.sqlite.org/fts5.html#the_integrity_check_command)
- `rebuild` replaces the full index from its content. It does not maintain later changes. The repair rebuild runs only on the isolated candidate. [Rebuild](https://www.sqlite.org/fts5.html#the_rebuild_command)
- `unicode61 remove_diacritics 0` retains accents, with Unicode 6.1 case folding and token boundaries. A token prefix requires explicit query syntax; an interior substring is different. [Unicode61](https://www.sqlite.org/fts5.html#unicode61_tokenizer), [prefix queries](https://www.sqlite.org/fts5.html#fts5_prefix_queries)

The runner uses Python's SQLite [read-only URI connection](https://docs.python.org/3/library/sqlite3.html#how-to-work-with-sqlite-uris) and [backup API](https://docs.python.org/3/library/sqlite3.html#sqlite3.Connection.backup) for inspection copies. Its disk-to-disk copy is limited to the closed fixture it just created, with no sidecars or other writers. Use a supported snapshot mechanism for an actual application database.
