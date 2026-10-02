---
name: searchable-pdf-review
description: "Make a reviewed searchable copy of an authorized scanned or mixed PDF while preserving the original and checking OCR against the page. Use for search and copy improvement, not redaction, signature validation or accessibility certification."
---

# Make a Reviewed Searchable PDF Copy

Deliver a separate PDF whose visible pages remain faithful to the source and whose text layer is useful for the user's actual searches and copying. An OCR job that exits successfully is a draft. Text-layer presence, confidence scores and a plausible-looking extract do not establish accuracy.

## Establish the working copy and intended use

Identify the exact input, requested pages, languages, intended searches, destination and whether the user needs ordinary search, copying, structured extraction or an accessible document. Use the supplied file and existing authorization to make a local copy without an unnecessary approval round. Keep original bytes untouched, record its digest and use a distinct output name.

Read the file only through an authorized route. If access fails, report the exact missing access and continue any useful preparation; do not imply a conversion occurred. An unavailable application does not invalidate a local file workflow when the file itself is accessible and the user authorized that workflow. Sending the document to an online OCR service is a separate disclosure: use local tools when available, and obtain any necessary approval before a new upload. Logs, page images and extracted text inherit the document's privacy needs.

Before changing a signed or protected file, establish the permitted purpose and consequences. Keep signed originals intact. Do not remove restrictions, invalidate signatures or flatten interactive content merely to get OCR running. If a permitted unsigned derivative is needed, agree on that derivative and label it clearly. A password or security prompt is not permission to bypass protection.

## 1. Inspect the document before choosing OCR

Record page count and order; effective page boxes, rotation and size; encryption and signature indicators; forms and widget values; annotations, links, bookmarks and tags that matter to the user. Inspect representative renders and text extraction together. Reconcile apparent blanks with the rendered page. Do not drop a blank page or reorder pages because extraction returned nothing.

Classify each relevant page, not just the document:

| Page evidence | Working decision |
| --- | --- |
| Image contains readable text; no useful text can be selected or extracted | Candidate for OCR |
| Native text already copies and searches correctly | Preserve it; OCR adds no benefit |
| Native text and a text-bearing image share one page | Identify the image regions; skipping the whole page would miss them |
| A scan already has a hidden text layer | Check its accuracy and alignment before deciding whether to replace it |
| Visible text copies as duplicates or nonsense | Investigate old OCR, duplicate layers and character mapping; do not pile another layer on top |
| Visually blank, drawing-only or photograph-only page | Preserve it; lack of searchable text can be correct |

An empty extraction alone cannot distinguish a scan, outlined text, a blank page and damaged encoding. A nonempty extraction cannot prove every visible region is covered. Inspect native and hidden layers when the distinction affects the method. Do not treat a broad force-OCR operation as a harmless repair.

Check installed OCR software and available language packs. Choose actual document languages, including relevant combinations and scripts; language selection is not automatic translation. If a needed language, handwriting, unusual layout or low-quality scan is unsupported, state the limitation and preserve the unresolved content. See [tool behavior and official references](references/tool-behavior.md) when selecting a mode.

## 2. Produce an OCR draft with the least necessary change

Use a new output path and retain the command, versions, selected pages/languages, warnings and skipped-page reasons. Try a representative page first for an unfamiliar layout. Account for each requested page as OCRed, already searchable, intentionally blank, skipped or unresolved; a timeout is not completion.

For a document like the included example, whose native text is on separate pages from scans, a compatible starting command is:

```bash
ocrmypdf --skip-text --output-type pdf --optimize 0 \
  -l eng --sidecar draft-ocr.txt source.pdf searchable-draft.pdf
```

This is a method choice, not a pixel-preservation guarantee. Check the installed version's help. Do not add rotation, deskew, cleanup, compression or PDF/A conversion without a reason: these can change properties beyond the text layer. When visual cleanup is requested, preserve the original and record the intended visible changes instead of claiming exact pixels were retained.

For mixed content on a single page or existing OCR, use a supported selective/redo route only after checking which text it preserves or removes. Some old OCR layers cannot be identified reliably. If replacement is uncertain, stop layering, report the limitation and choose a reviewed alternative within scope.

Keep the raw OCR result distinct from the reviewed result. An OCR sidecar is the text recognized during that OCR operation, not a complete document transcript. Extract the final whole PDF separately, by page, to include preserved native text and reveal omissions or duplication.

## 3. Review words against their source

Review the rendered source beside the extracted text, using a sufficiently detailed image to resolve characters. Prioritize what the user will rely on: identifiers, names, dates, amounts, decimals, units, punctuation, filenames and URLs, plus negations and limiting words. Check headings, reading order, column boundaries and table cell associations where relevant. A confidence score can help choose what to inspect, but does not authorize a correction.

Correct only what the source supports. Distinguish the letter O from zero and preserve real spelling, unusual names and deliberate spacing. Do not silently rewrite text to fit an expected meaning. When the source is ambiguous, record its page/region, possible readings and unresolved status in the review note. An uncertain critical token must not remain apparently authoritative in the searchable/copyable layer just because a separate note warns about it: omit it from that asserted layer or use an explicit uncertainty representation whose meaning is clear when copied. Keep the raw OCR as attributed draft evidence, and do not label that region fully reviewed. Ask for a clearer source only if the ambiguity blocks the requested use. Never silently substitute a guessed critical value.

Record each changed line or token with page, region, raw OCR, reviewed text and the supporting evidence. Keep unresolved regions and the extent of manual review visible in the handoff. A review of selected fields is not a review of every word.

Apply a supported text-layer correction, preserving the visible source. For a simple image-only page, a reviewed invisible overlay can be a reasonable local method when coordinates and encoding are verified. Build that overlay against the clean original image page, not on top of a flawed existing OCR layer. Keep Unicode mappings, reading order, word spacing and page transforms correct. A replacement line's geometry must follow the source; stretching a line into a box is not enough to establish good word selection. For complex pages, use an appropriate PDF/OCR editor or report the remaining limitation instead of pretending a simple overlay generalizes.

## 4. Verify the saved file through independent checks

Reopen the actual output file, then check these separate properties:

- **Document integrity:** Page count, order, effective boxes and rotations agree with the intended result. Verify native pages, blank pages and any retained forms, annotations, links or bookmarks. A rendered form value alone does not establish the underlying field value.
- **Visible fidelity:** Compare source and output renders at the same resolution and inspect changed or difficult areas at readable magnification. If exact source pixels are required, also compare decoded embedded image samples and their placement. Record renderer, DPI and scope; equality in one render does not prove every possible display is identical.
- **Text integrity:** Extract the whole saved document by page. Confirm reviewed critical strings, unchanged native text, complete negation and decimal values, and absence of stale or duplicate OCR lines. Inspect reading order; do not normalize meaningful punctuation to make a test pass.
- **Actual search and copy:** Search distinctive source-grounded strings and check results on the expected pages and near the visible words. Copy representative passages into plain text. Test in the intended PDF viewer when available. API extraction and search are useful evidence, but do not stand in for an unperformed viewer test.

If search rectangles are returned by an API, inspect their geometry and the text within them. Multiple rectangles can describe one wrapped phrase; rectangle count alone is not a universal occurrence count. For rotated or cropped pages, use the tool's coordinate conventions rather than assuming page coordinates start at the visible upper-left corner.

Fix an observed failure, regenerate the separate copy and rerun the affected checks. Do not keep retrying OCR parameters when the source itself is illegible. Preserve the best available source and state the unresolved region.

## 5. Deliver a useful, bounded result

Provide the reviewed copy and a short review note: input identity, pages covered, corrections made, unresolved content, preservation checks and search/copy results. Distinguish completed checks from inaccessible or untested ones. Call a file an OCR draft if review is incomplete. Do not claim accessibility, PDF/UA, PDF/A, signature validity or legal evidentiary equivalence from searchability alone.

If the requested goal includes saving to a named authorized destination, complete that save and verify the saved artifact. A newly shared location or audience still needs the appropriate authority. Provide a local reviewed copy when that is the authorized reachable destination, and explain any remaining requested delivery step.

## Original worked example

[The example and verification](examples/example.md) show a real OCR pass on an original fictional device sheet: three source-grounded corrections, one native-text page preserved and one intentional blank retained. The source and reviewed PDFs, source/correction record and a read-only checker are included. Use this example to understand the evidence, not as a substitute for reviewing a new document.
