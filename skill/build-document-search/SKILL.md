---
name: build-document-search
description: Build a reusable full-text index and query consumer for an authorized document collection, with declared search semantics, traceable passages and checked updates. Use for creating retrieval behavior, rather than a one-off lookup or diagnosing freshness in an existing index.
---

# Build Document Search

Deliver the searchable collection and a working way to query it, with results that lead back to the source material actually indexed. A populated database, plausible snippets or a search-box mockup alone does not establish useful retrieval.

Use `search-index-reconciliation` when the task is diagnosing missing or stale results under an existing accepted search contract. For new search behavior, decide that contract before treating a result as correct. Keep the requested delivery form: a local command, library function, existing application feature or another specified consumer. Do not add a hosted interface or generated-answer layer merely because an index is being built.

## Define what a search should return

Inspect the selected corpus, intended queries and consumer requirements. Identify the authorized collection and versions, supported formats, useful metadata filters, result limit and output fields. Establish whether a result is a document, page, section or another record, and whether several matches from the same document should be grouped.

Distinguish the unit indexed from the unit returned. Section indexing can improve local relevance and excerpts while missing a document-level all-words query whose terms occur in different sections. Whole-document indexing can find that document but may need several passages to show why it matched. Choose deliberately from the user's question; do not let chunk boundaries silently redefine it.

Settle consequential semantics such as all versus any words, quoted phrases, case/accent handling, morphology, prefix or substring behavior, and which fields can match. Explain a reasonable initial choice when design judgment is delegated. Ask only when an unresolved choice changes the required behavior or permitted source scope. A keyword interface must not silently claim broad natural-language understanding.

An index and its excerpts contain copies or derivatives of source content. Keep them within the authorized destination and audience. Use actual access rules when a multi-user application requires them; an ordinary category filter is not automatically an authorization boundary.

## Prepare sources with durable provenance

Preserve source identities and capture the actual revision or content identity used for indexing. A title, filename or list position alone may not distinguish a renamed document, a second occurrence or a later revision. Keep the original source separate from extracted or normalized search text.

Read supported content using suitable format-aware tools. Retain the locators needed by the result: a page, heading, line range, section ID or other meaningful anchor. Record unsupported files, unreadable pages, partial extraction and intentionally excluded fields. A document present in the folder can still have no searchable text; an empty result does not prove the requested information was absent from inaccessible material.

Choose boundaries that preserve useful context. Avoid splitting a heading from its qualifications, a table value from its labels, or an answer from the question it addresses. Use overlap only where it helps; repeated overlapping chunks should not create duplicate-looking results or inflate an occurrence count. Keep a mapping from every indexed unit to its source revision and location.

Retain raw text for evidence even when indexing a transformed representation. Case folding, stemming, OCR correction or token normalization can be useful retrieval choices, but a displayed quotation must still be faithful to the source. Identify derived metadata or aliases rather than presenting invented keywords as original document content.

## Build the actual query path

Use the requested engine and project conventions, or choose an available engine that supports the necessary behavior with proportionate complexity. Inspect its actual version and capabilities. Exercise a small real index/query operation before relying on a compile flag or assumed feature. Avoid unnecessary services, installations or transfers of the corpus.

Make the public query language explicit. Ordinary input should have predictable treatment of whitespace, punctuation, quotes and unsupported operators. Keep literal text separate from engine syntax, and return a useful error when a requested expression is unsupported or malformed. An empty query, no matches and a failed query are different outcomes. Verify the selected engine's behavior instead of assuming that token phrases, substrings and prefixes are interchangeable; the [SQLite FTS5 query and tokenizer documentation](https://www.sqlite.org/fts5.html) illustrates these distinctions for that engine.

Choose fields and ranking for the actual use. A title or heading boost can help, but there is no universal weight set. State whether title/metadata matches can produce a result whose displayed body lacks a query word. Use a stable tie rule when repeatability matters. Scores are not probabilities or proof of relevance; their direction and comparability depend on the engine. For example, SQLite's [BM25 function](https://www.sqlite.org/fts5.html#the_bm25_function) assigns better matches numerically lower values.

Apply required filters before selecting the final top results. If the user wants distinct documents, group or select the appropriate matching passages before enforcing the document limit. Limiting raw chunks first can let one document crowd out other useful documents; filtering only the already truncated result can hide eligible matches. Preserve the agreed ordering through the actual consumer, not just an isolated database query.

Return excerpts and locators from the indexed source version. Mark omissions or truncation, preserve consequential context, and show multiple passages when needed to explain a document-level match. Do not attach newly fetched text to an old posting and imply that the new words caused the match. If source and index have diverged, identify the result's captured revision, refuse an invalid source claim, or use the supported refresh path as the contract requires.

Make the saved index usable through the promised entry point. Reopen it in the actual query consumer, keep source paths or links valid in the delivered layout, and document needed runtime/schema/analyzer compatibility. A successful build or deserialization is insufficient if the query command relies on the builder's working directory or an unavailable source file.

## Check relevance as well as structure

Use a small set of realistic queries chosen from the intended use, with source-grounded expected properties. Include useful positive results and a meaningful no-match, ambiguity or filter case. Judge passages against the original sources; do not define relevance solely by what the current implementation returns.

Check several different questions separately:

- Were the intended source records and supported fields actually indexed, with their identities and extraction coverage preserved?
- Does the query obey the declared word, phrase and filter semantics?
- Are returned documents distinct and ordered as promised, with accurate source excerpts and locators?
- Do the selected results help with the user's intended lookup, and what relevant material is missed or ranked poorly?

Engine integrity checks, source/index consistency and retrieval relevance establish different things. Equal document counts cannot prove that the right documents or terms are present. A correct title match can still yield an unhelpful excerpt. Diagnose a miss as extraction, identity/update, query semantics, filtering, ranking or corpus-coverage trouble before changing unrelated settings.

If weights, token rules or other choices are tuned using examples, keep that development use visible. Use additional queries not used to choose the settings when a broader quality claim matters. Report query-level results and their actual scope; a few handpicked probes do not establish general semantic recall or production accuracy. Use a formal metric only when its relevance labels, denominator and result unit fit the request.

Keep checks proportional. Exercise the actual saved consumer and a consequential boundary or changed-source case rather than producing a large framework by default. Preserve material unsuccessful queries and explain the limitation instead of adding query-specific result mappings or quietly rewriting the corpus.

## Make updates and delivery honest

Define how additions, edits and deletions reach the index. A complete rebuild can be a good solution for a small collection; incremental maintenance needs a reliable identity and change contract. Absence from a partial listing is not evidence of deletion. Keep intentional historical versions distinguishable from the current searchable collection.

Preserve the usable prior state when preparing an update. Verify the saved new state with changed and retired terms, added and removed IDs, and an unchanged control suited to the actual delta. Compare IDs as well as counts. A retired term may still legitimately match another current document. Do not label a prepared replacement as an installed live update unless that promotion was requested and verified.

Deliver the requested index, source or application change, query invocation and concise search contract. Include meaningful observed queries, source/extraction coverage, the supported update path and material relevance limits. Check that the final instructions work from the delivered files and that displayed results correspond to the final index.

Retrieval supplies source material; it does not establish that a source's assertions are true or that a generated answer is grounded. Keep those claims separate. A local search demonstration also does not establish large-corpus performance, concurrent-update behavior or integration with an untested live application.
