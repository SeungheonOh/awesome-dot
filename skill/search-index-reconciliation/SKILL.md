---
name: search-index-reconciliation
description: Explain missing or stale results for selected documents in an authorized collection search index, distinguish source revisions from indexed terms and query semantics, and verify an isolated repair candidate. Use for index freshness, not document OCR or business-report totals.
---

# Reconcile a collection's search index

Deliver an evidence-backed explanation for the selected search failures, a query-result ledger tied to exact source revisions, and a verified candidate or supported next action. A document visible in a collection, an unchanged row count, or a successful indexing job does not establish that its current terms are searchable.

## Establish the source, search contract and boundary

Start with the user's selected documents and actual failing searches. Record stable document IDs, current revisions or content hashes, collection/tenant, indexed fields, deletion state, source capture time, query text, filters and the identity/access context under which search ran. A displayed last-modified time is weaker evidence than a known source revision and completed index checkpoint. Keep source text and indexed text distinct, including any extraction or transformation step between them.

Use already-authorized sources and tools. Inspect the named collection and selected examples; do not enumerate unrelated collections or change permissions to make a result appear. A selected document's full text, query history and index terms can contain private information. Keep the evidence within the requested destination and audience.

Resolve the distinctions that change the diagnosis:

- Can the same user open this exact document and revision directly? An absent search result may follow an access rule, account, filter or collection boundary.
- Is the document's format and relevant field supported for indexing? A visible file can lack extractable content. If its text layer needs OCR review, address that document-level problem separately.
- What does this engine mean by a term, phrase, prefix, case, accent, stemming and substring? Record the actual tokenizer/analyzer and language settings. Search syntax and filters are part of the contract, not noise to normalize away.
- Was this revision actually ingested, indexed and made available to the queried replica? Distinguish source edit time, ingestion state, index checkpoint and replica/read time. Treat an incomplete export or inaccessible queue as unknown.

Select a small source-grounded set: a current distinctive term, a retired term after an edit, an added document, a deleted document, and an unchanged control when available. Include one plausible semantic mismatch. Do not use broad searches that reveal unrelated content merely to fill the set.

## Compare source evidence with real index behavior

Record the exact search request and returned IDs, revisions if genuinely stored in index metadata, and errors. Fetch the matching source by stable ID separately when needed. Keep orphan index IDs visible; an inner join to the current source can conceal deleted-document postings. Current text returned beside a match does not necessarily mean those current words produced the match.

Compare four independent questions:

| Question | Useful evidence | What it does not establish |
| --- | --- | --- |
| Does the selected source exist at the expected revision? | Source lookup with ID and revision/content fingerprint | That the terms were indexed |
| Which IDs/terms are present in the index? | Supported index metadata or bounded posting inspection | User access or upstream corpus completeness |
| Does the actual query find the expected IDs? | Search request and result ledger, with filters and analyzer held fixed | Every other query's relevance |
| Are source and index mutually consistent? | Engine-supported consistency check with its exact comparison scope | Application correctness or durable future synchronization |

Compare ID sets as well as counts. In an index that excludes empty or unsupported content, a source ID without postings may be correct; reconcile it to its eligibility and extraction status. A collection-wide claim requires collection-wide coverage evidence within authorized scope. A few search probes establish only their own results.

A source revision can advance when only non-indexed metadata changes. Retain that change in the provenance; compare indexed fields and actual query/consistency evidence before diagnosing stale terms.

Classify each observation as source missing/outdated, ingestion/extraction pending or unsupported, index stale, access/filter mismatch, query-semantic mismatch, or unresolved. More than one cause can coexist. A job marked complete or an internal index check alone does not erase contrary query evidence.

## Prepare the smallest supported candidate

Check the product's supported repair path and installed engine/version before executing it. Prefer a bounded document refresh when supported and sufficient; use a complete rebuild only when its effects, authority and resource budget fit the task. Do not edit opaque index internals or assume an optimization/merge operation refreshes content. For SQLite FTS5 details, read [the narrowly scoped reference](references/sqlite-behavior.md).

Capture a consistent source snapshot and preserve the original before changing the candidate. For a database, use its supported backup/export or documented quiescence process; copying an active main file alone may omit committed state or mix snapshots. Record what guarantees the snapshot is stable and which revision set it represents. Do not stop a service or alter OS search, access, network or security settings as an incidental repair step.

Review the full operation's read/write effects and dependencies, including hooks or external services, not just its name. Bound source size, temporary storage, expected write amplification, run time and locks. A small result limit does not bound indexing work. If cost or safe isolation cannot be established, prepare the concrete operation and blocker instead of running it on a live index.

Within existing authority, build a separate candidate against the fixed source using the same fields, IDs and tokenizer. Keep an existing output intact and choose a fresh destination. Do not silently turn on accent folding, substring search or new fields to make a freshness test pass. Such changes require their own search-behavior decision. Preserve enough evidence to abandon the candidate and retain the original.

## Verify the saved candidate and hand it back

Reopen the saved candidate and repeat the exact query ledger with its original access context, fields and filters wherever that application context is available. Verify positive and negative results: current terms appear, retired terms disappear for the affected IDs, deleted IDs no longer match, new eligible IDs are covered, and unchanged controls remain stable. A retired term may legitimately appear in another current document, so compare IDs rather than demanding a global zero.

Check all source rows, IDs, revisions and required metadata against the preserved snapshot. Verify the analyzer/schema stayed fixed. Run the engine's appropriate consistency checks, noting whether they compare external content or merely index structure. Record original preservation and candidate readback separately from search correctness. If the source advanced during the work, keep the result labeled for its captured revision set and reconcile the delta through the supported maintenance path; do not claim it is current.

Deliver the candidate or portable regeneration, exact input identity, before/after query results, covered and unresolved IDs, checks actually run, and the remaining operational step. Local engine tests do not prove behavior in an untested app UI, access rules, upstream completeness, crash durability or production readiness. An isolated candidate is not an installed repair. Complete any explicitly authorized save or application handoff and verify it; obtain any missing authority before promotion or new external effects.

Identify how future additions, edits and deletions are meant to update this index. Repairing the present snapshot does not repair a missing maintenance path. Report an observed gap and its owner or supported remedy without expanding a snapshot reconciliation into unrequested application changes.

## Original worked example

[The Alder workshop example](worked-example.md) creates three fictional source rows and an external-content SQLite FTS5 index, deliberately lets the source advance without index maintenance, and rebuilds only a separate candidate. It demonstrates stale postings behind current-looking ordinary reads, document replacement hidden by equal counts, and accent/substring controls that correctly stay unchanged. The stdlib-only [fixture runner](scripts/rehearse_index.py) accepts a new output directory, never an existing database.
