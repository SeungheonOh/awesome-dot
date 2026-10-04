---
name: maintain-source-linked-citations
description: Repair or update citations generated from maintained document source and reference data, preserving occurrence-specific meaning and regenerating a consistent bibliography and reading copy. Use for source-key, metadata, duplicate/version or style-dependent update problems in a supported citation pipeline. Keep claim verification, reference discovery and ordinary prose editing with their substantive workflows; live reference-manager fields require their actual native consumer.
---

# Maintain Source-Linked Citations

Deliver the corrected maintained source and reference data, plus the regenerated documents the user requested. Preserve the relationship between each citation occurrence and its intended work. A visually corrected bibliography is insufficient when the next regeneration would restore the error or break a source link.

Keep the work proportional to the change. One broken key may need one source correction and a focused rebuild check. A larger reconciliation can warrant a compact change map. Do not automatically create a database, citation audit appendix, new reference manager or publication workflow.

## Find the authoritative citation system

Inspect the actual manuscript, reference data, style and generation settings. Determine whether citations are source keys processed during a build, application-managed fields, plain text, or a mixture. Identify the maintained inputs and the derived reading copies before editing. A DOCX extension or reference-looking string does not establish live linkage.

For source-linked work, establish which processor and input formats the project actually uses. Check bibliography resolution, key sensitivity, style selection, locale and any filters or templates that affect the result. Preserve an existing working pipeline when it meets the request; do not migrate formats merely because another tool is familiar. A bibliographic file extension can select a reader with different field interpretation, so verify the parsed meaning when that matters.

This guide's main workflow is maintained source plus a supported citation processor. If the user needs application-managed Word or reference-manager fields repaired and kept live, use the actual supported manager and document consumer. Do not replace them with similar-looking generated text as silent completion. If that consumer is unavailable, explain the exact limitation and preserve the source; static field inspection cannot establish that Refresh works.

Keep substantive questions separate. Reference lookup can help find metadata, catalogue matching can help resolve a work's identity, and claim checking can examine whether a passage supports a statement. Correctly linked, well-formatted citations do not by themselves establish source credibility or evidential support. Do that additional work only when it is part of the request.

## Separate works, library records and occurrences

Identify the work or version each key denotes. A library can contain duplicate records for one edition, distinct editions with similar titles, or a preprint and a later article. Similar author-year labels, titles or identifiers are evidence to inspect, not permission to merge. Retain a version distinction when the cited content or source authority requires it.

Inspect citation occurrences across the whole requested document, including notes, captions, tables and supplementary sections. An occurrence may contain several cited items, and the same work may recur with different page ranges, sections, prefixes, suffixes or author-display choices. Preserve those occurrence properties independently of the shared library metadata.

Use the format's citation representation or parser where possible. A broad string replacement can alter a code example, an ordinary date, a literal display number or prose mentioning an author. Count parsed citation items or groups when checking coverage; rendered text may combine items, suppress repeated authors or collapse number ranges. One displayed bracket is not necessarily one cited work.

Keep a compact working map when the repair needs it: old key, intended work/version, supported correction and affected occurrences. Preserve unresolved mappings and conflicting evidence instead of guessing the nearest title. Ask only when a material identity or authorized change cannot be established from the supplied sources.

## Repair the source of the error

Apply authoritative metadata corrections to the reference record and broken-key corrections to actual citation occurrences. Keep institutional authors distinct from personal name parts, retain meaningful title capitalization and publication types, and preserve unchanged metadata. Do not invent missing fields to make an entry look complete.

For a confirmed duplicate, choose the supported canonical record, update its real citation references and verify that no intended occurrence becomes orphaned. Remove or retire redundant records only within the authorized scope. Do not delete an entire library item merely because it is absent from one document's bibliography.

Keep work identity and occurrence locators separate during consolidation. Two citations of the same report at pages 3 and 18 remain different occurrences after their duplicate keys converge. A locator from one version should not be moved to another version just because the titles are similar. If the source needed to resolve a conflict is unavailable, preserve the unresolved question visibly.

Maintain source-format semantics. Braces, name structure, escape conventions, date parts and rich-text markup may affect how the processor reads metadata. Inspect the parsed record when a conversion is necessary. Do not silently round-trip the whole library through a lossy format to correct one title.

Make manuscript changes only as authorized. Preserve unrelated prose, section contents, tables, figures, notes and links. When moving a section, retain its citation and note relationships. When removing the final citation to a work, distinguish removal from the rendered bibliography from removal of the reusable library record.

## Regenerate selection and display together

Identify the intended bibliography population: cited works, explicitly included uncited works, permitted exceptions, or a requested complete library. Respect the source's actual selection mechanism and requested style. A retained but unused library record need not appear in the document; an intentional uncited entry need not have an invented in-text citation.

Regenerate through the actual processor after the source corrections. Capture consequential warnings and unresolved keys. Do not suppress an unresolved citation merely to produce a clean-looking file. Diagnose the failed layer: source syntax, reference resolution, metadata interpretation, style, document generation or export.

Let the selected style and processor update citation numbers, ordering, repeated-author forms, year suffixes and bibliography formatting. Changes in document order or metadata can legitimately alter these outputs. Repairing only a rendered number or suffix leaves the dependency broken. If the user requires a specific display convention, establish that convention in the appropriate style or supported occurrence option, rather than patching generated text after every build.

Do not assume bibliography order is always first citation or always alphabetical; inspect the supplied style and resulting output. Preserve citation-item order or supported grouping semantics as specified by the source and processor. A different visible form can be correct after regeneration, while an identical visible form can hide a link to the wrong work.

Keep the maintained source distinct from reading copies. A generated DOCX can have editable paragraphs and tables while its citation text remains static. Describe that behavior accurately. Do not claim native-manager continuity from a successful source-based rebuild or from preserved XML alone.

## Check links and the actual saved documents

Reopen the corrected source and reference data. Check that expected keys resolve, unintended duplicate or orphan entries are absent where required, and protected occurrence properties survive. Reconcile cited, intentionally uncited and unused records according to their different roles. For a small repair, inspect every affected occurrence and the resulting bibliography; for larger work, state the actual coverage.

Read the regenerated citations and references against the intended works, not only against old display strings. Check numbering or disambiguation after the consequential edit, especially for repeated works, same-author/date collisions, multi-item groups and citations outside the main prose. A parsed representation can establish link and locator structure; the rendered document establishes what the reader sees. Use both when the task requires a delivered document.

Open the exact saved reading copies and inspect their complete rendered pages at a useful size. Confirm that notes, captions, tables, reference wrapping and page flow remain readable and that the requested formats agree. Use document-editing or export guidance for layout and native-file preservation. A successful process exit or extracted text alone does not establish an intact reading copy.

When continued regeneration is part of the deliverable, exercise the documented command from the saved packet in a separate location or equivalent clean consumer context. Include the relative resources it actually needs and state ordinary dependencies. Avoid relying on private helper paths or files omitted from the handoff. Compare meaningful source, citation and document behavior while distinguishing harmless generation metadata from substantive changes.

A requested insertion, removal, section move or metadata update can provide a useful propagation check. If another temporary change is needed to test update behavior, use a disposable copy and keep it out of the delivered manuscript. Do not add an unrequested citation or alter a final source merely to demonstrate the pipeline.

## Deliver the maintainable result

Return the requested sources, reference data and reading copies with a short explanation of the changes and the command or supported action for the next update. Include necessary style and layout resources with their applicable attribution. Keep detailed reconciliation records separate unless the user asks for them or they are needed to resolve a material uncertainty.

State what remains linked, what was actually regenerated and inspected, and which native-application behavior was not exercised. Preserve original inputs and useful prior versions. A successful local source-based update establishes that particular pipeline; it does not certify every citation style, another reference manager, all document formats or the truth of the cited claims.

## References

The [Pandoc citation documentation](https://pandoc.org/MANUAL.html#citations) describes source citation syntax, bibliography data, styles and deliberate inclusion of uncited items. The [CSL specification](https://docs.citationstyles.org/en/stable/specification.html#disambiguation) explains coordinated citation and bibliography disambiguation. These are examples of processor-dependent behavior, not requirements to use one tool. [Zotero's Word-plugin documentation](https://www.zotero.org/support/word_processor_plugin_usage) describes native Refresh and the loss of automatic updates after unlinking; source-generated reading copies do not demonstrate that native workflow.
