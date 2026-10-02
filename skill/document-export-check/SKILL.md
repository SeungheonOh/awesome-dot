---
name: document-export-check
description: "Export an approved editable document to a separate PDF and verify that its claims, exact strings, links and page layout survived before calling the delivery ready."
---

# Verify an editable document export

Use when an approved Word document needs a usable PDF for a release handoff, customer instructions, onboarding packet or other everyday delivery. Produce the actual requested PDF, preserve the editable source, and show what was checked on the saved output. The problem is conversion loss after wording is agreed. Version reconciliation, new writing, OCR and signature validation belong to other workflows.

A successful export is a candidate. Text extraction and a page count cannot show whether a table is clipped, a minus sign is visibly missing or a link covers the wrong words. Inspect every output page as well as its machine-readable content.

## Establish the delivery contract

Identify these from the request and available files; ask only about a gap that changes the action:

- Exact source file and approved revision, with approval evidence or an explicit user choice of that file
- Requested operation: inspect an existing export, export a new copy, or repair and re-export within a named scope
- Output path, format and intended use; whether the user needs an editable companion, printing, search/copy, working links, forms or a specific accessibility/archival standard
- Protected content: amounts, dates, conditions, identifiers, URLs, symbols, table cell relationships and required headings
- Layout expectations: paper size, orientation, page order, intentional breaks, section numbering, headers/footers and required placement; do not invent an exact page-count requirement when none exists
- Permitted handling of comments, tracked changes, hidden material, calculated fields, attachments and signatures
- Applications, fonts and rendering tools already available, and any reference rendering from the approving application

An explicit request to export a named local file already authorizes that conversion and routine checks. Do it rather than return only instructions. It does not authorize accepting edits, rewriting a condition, uploading to a conversion website, installing dependencies, overwriting an unrelated destination or sharing with a new audience. Honor broader authorization already provided; do not add redundant confirmation steps.

If approval is ambiguous, prepare a labeled draft export only if that is useful and authorized. Do not call a filename such as `final-v4.docx` approval evidence.

## 1. Inspect and freeze the source

Record a content digest, file size, revision/date, intended destination and the source's identity before conversion. Work in a fresh directory and preserve the original bytes. Existing destination files should remain intact unless replacing that exact destination was requested; even then, prepare and verify a new candidate before the final replacement.

Use a format-aware reader and, when possible, an authoring-application view. Inspect body text, tables, headings, section/page settings, links, footnotes, headers and footers. Inventory tracked changes and comments, simple and complex fields, hidden text, content controls, linked/embedded objects, macros, signatures, protection and external relationships. Package inspection is a useful inventory, not a guarantee that arbitrary documents are safe to open or all features were understood.

Resolve the consequential branches before export:

| Observation | Required treatment |
| --- | --- |
| Tracked changes or unresolved comments alter the approved wording | Get the intended revision/disposition; do not silently accept everything. Hiding markup does not remove tracked changes, as [Microsoft documents](https://support.microsoft.com/en-us/word/accept-or-reject-tracked-changes-in-word) |
| A date, total, table of contents or cross-reference is a field | Record its instruction and displayed value; agree whether to update it, then verify the resulting value. Automatic refresh can change meaning |
| PAGE/NUMPAGES fields are expected | Verify every resulting page label and total; do not rely on cached DOCX page metadata |
| Required font is unavailable or substituted | Identify the substitution and inspect affected glyphs, wrapping and pagination. Obtain an approved replacement when appearance or meaning changes materially |
| Macros, active content, external data, embedded objects or unsupported elements appear | Pause the dependent conversion until an appropriate inspection/execution route is authorized; do not enable content or refresh remote data just to finish |
| Protected or signed source | Preserve it; do not bypass restrictions or claim a derivative retains the source signature. Clarify the permitted unsigned derivative when that matters |
| Required accessibility, archival, forms or signature behavior exceeds the available checks | Explain the exact missing verification and use the required specialized route; ordinary visual review is insufficient |

Create a short acceptance map before conversion: source locator, exact expected text/value/target, expected output location and check method. For a table, preserve the row/column association, not merely the presence of all its numbers somewhere in the PDF. Include at least one consequential qualification such as “pilot only” or “pending review.”

## 2. Make an isolated candidate

Choose an already installed exporter that supports the source format. Record its version, export filter/options and warnings. If using LibreOffice, its [command-line documentation](https://help.libreoffice.org/latest/en-US/text/shared/guide/start_parameters.html) describes `--convert-to`, `--outdir` and a separate `UserInstallation` profile. A fresh profile prevents accidental reuse of a user's settings/session; it is not a security sandbox.

Export the complete intended document to a new output directory. Do not silently choose a page range, print instead of export, rasterize everything, flatten forms or remove review material. Set special options only when needed and understood; the [PDF filter reference](https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html) lists supported properties, whose applicability must be checked against the installed version.

Capture the command, exit status and actual output path. Reopen the file and check that it is nonempty and parseable; a zero exit status or an old file with the expected name is not proof of a new successful export. Compare the source digest again. If it changed, stop using the stale candidate and establish the new revision.

If export fails, retain the logs and diagnose the named error. Retry with a new candidate path when justified. Missing software or permissions are blockers, not permission to install, upload or loosen security settings.

## 3. Check meaning, structure and links

Reopen the exact PDF that would be delivered and compare it to the acceptance map:

1. Account for every intended page, section and appendix. Check size, orientation, rotation and page labels, including intentional blanks. Reflow is not automatically wrong; assess it against the contract
2. Extract text and compare protected strings without normalizing away punctuation, accents, minus signs, decimal separators or identifier characters. Check totals against their rows and preserve the language that limits the claim
3. Compare all table row/column relationships and notes. Inspect whether text extraction changes order; use the rendered table to resolve ambiguity rather than treating an unordered bag of values as equivalent
4. Inspect actual link annotations and their destinations, pages and clickable areas. Visible underlining alone is insufficient. LibreOffice's [link export documentation](https://help.libreoffice.org/latest/en-US/text/shared/01/ref_pdf_export_links.html) describes export behavior, but verify this particular file. Check internal destinations against their headings; do not visit confidential or state-changing URLs solely to test a link
5. Review fonts, embedded/subset font observations, bookmarks, forms, annotations, metadata and attachments that the recipient needs. A font list is evidence about the PDF, not proof that every glyph looks right
6. Record accessibility/tag/signature indicators only as observations. A structure tree, searchable text or embedded fonts do not establish accessible reading order, PDF/UA compliance, archival conformance or cryptographic signature validity

For a small brief, compare every paragraph and table cell. For a large file, still inspect every rendered page, identify the extent of the semantic comparison, and disclose any sampling or unsupported elements. Do not label unreviewed content as verified.

## 4. Render every page and repair within scope

Render the saved candidate to page images using an available renderer. Open every image at readable resolution; zoom into dense tables, symbols, footnotes, headers and link labels. Check clipping, overlap, missing glyphs, table boundaries, line breaks, unexpected empty pages, heading placement and footer collisions. Match every acceptance-map item to the visible page.

When an approved original-application rendering exists, compare it alongside the output. If both the source preview and export use the same engine, say so: agreement between them cannot establish fidelity to Word's rendering on another machine.

Classify discrepancies and act:

- Export setting or tool issue: adjust the authorized setting, generate a fresh candidate and repeat affected checks plus a complete page review
- Layout-only repair within existing authorization: edit a separate editable candidate, retain the before/after record, then export and recheck. Do not fix only the PDF while leaving its supplied editable companion inconsistent
- Wording, accepted revision, totals, legal meaning, required font or unsupported-feature choice: preserve the evidence and ask the smallest necessary question before changing it
- Viewer-specific behavior: test in the intended viewer when available and authorized; otherwise state exactly which renderer/viewer was used and what remains untested

Never approve the export automatically because a checker returned “pass.” Its scope is narrower than the delivery decision.

## 5. Save and hand over the verified bytes

Deliver the requested PDF and, when requested, its unchanged approved source or explicitly identified edited candidate. Read back or re-download the final saved destination and compare the digest with the reviewed candidate when possible. A local check does not establish that an upload reached the right account, folder or audience.

Include a compact record: source revision/digest, output digest, converter version/options, page count, semantic/link results, pages visually inspected, repairs, unresolved items and unperformed checks. Logs and page images inherit the source's privacy needs; keep them private unless sharing them is authorized. Distinguish “reviewed for this delivery contract” from broader compatibility, accessibility or compliance claims.

Stop when the exact saved output satisfies the agreed checks, the source is preserved and remaining limitations are clearly accepted or labeled. If a material check fails or cannot be done, provide the candidate with its blocker instead of presenting it as delivery-ready.

## Worked example

The [fictional delivery exercise](example.md) includes an actual [editable source](approved-source.docx), [exported PDF](release-delivery.pdf), [narrow checker](check_example.py) and [verification record](verification.md). It preserves a release qualification, a native data table, Unicode strings, two link targets and a deliberate two-page structure. It does not certify accessibility or Word compatibility.
