# Observed verification

Verified on 2026-10-02. This record concerns the exact included fictional artifacts. It is a conversion/delivery check, not a real software-release approval.

## Frozen native artifacts

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| [Editable source](approved-source.docx) | 40,024 | `87a88a30c418ec41bae6f27c7c43101c6651f9be6d0a5e2ce63e8cb508cfb053` |
| [PDF delivery](release-delivery.pdf) | 88,485 | `9f31052560c71fe1950ad5e185b5a0a538c7c6ab6456fe8a7116ad0d5a9734a0` |

The source was authored as a native DOCX with paragraph styles, a native table, numbered steps, hyperlinks and footer fields. Its early authoring preview exposed an inherited title border and equal-width table grid; those were repaired before freezing the included source. No wording changed in that layout pass. The frozen source hash matched before and after the final export, and the delivered PDF is byte-identical to the isolated export output.

## Execution and machine evidence

Existing tools used: Linux; Python 3.12.14; python-docx 1.2.0 for original authoring; pypdf 6.10.0 for inspection; LibreOfficeDev 26.8.0.0.alpha0 build `2c87e51eeaa2b413ff4ae097b2705eea1995d8e5`; Poppler `pdftoppm` 26.05.0 for rendering. This LibreOffice build is a development build, not a claim of validation on a stable release.

The source package was inspected before rendering/conversion. The final export used a fresh `UserInstallation` profile, a fresh output directory and `--headless --norestore --convert-to pdf:writer_pdf_Export`. It exited 0 and produced a new parseable PDF. It also emitted 32 `Fontconfig error: No writable cache directories` warnings. The warning was retained in the execution record; no permissions or system font configuration were changed. See [the portable command sequence](example.md#reproduce-the-export-with-existing-tools).

Observed results:

- The checker passed for the included source and PDF
- All 45 nonempty source body/table paragraphs matched in order after whitespace-only normalization; accents, signs, punctuation and identifier characters were not normalized away
- The complete five-row, four-column table block appeared in order on page 1, preserving each platform, pass/fail count and build identifier association
- Two pages, each 612 × 792 points, portrait with rotation 0; the explicit source break put Recipient delivery checks on page 2
- Both expected headers, revision labels and `Page 1 of 2` / `Page 2 of 2` footer values were present
- The two `/URI` annotations had the exact approved targets on the correct pages; both rectangles lay within page bounds and covered their visible labels on inspection
- `Zoë`, `café`, `Δ latency = −12 ms`, `99.5%`, `HD-1847` and `v2.4.1+rc.03` survived extraction and visual review
- Source fields were exactly PAGE and NUMPAGES; inspected revision/comment/hidden/object/protection indicators were absent. The known empty bibliography custom XML was separately inspected
- PDF inspection found no encryption, forms, JavaScript or embedded-file indicators in the locations checked. This limited inspection is not a security audit

The PDF font report listed eight embedded, subsetted TrueType entries, each with a Unicode map: three LiberationSans entries, one LiberationSans-Bold, one Carlito, one Carlito-Italic and two Carlito-Bold entries. The source includes both explicit font names and theme font references. The font report alone does not establish which substitutions occurred, so this record makes no such claim. Exact font-family identity was not a fixture acceptance requirement; all visible text was inspected. A brand-font requirement would need further source-to-output font tracing.

## Every page was visually inspected

These previews were rendered from the exact included PDF at 144 dpi, 1224 × 1584 pixels each:

| Exact preview | SHA-256 | Visual observations |
| --- | --- | --- |
| [Page 1](preview-page-1.png) | `7f7e9c6d8c2c612859ef27eb295a6dd1312d6bec6d06c6cbb78f6c85b2f3dc4c` | Title and release condition readable; five table rows aligned with light borders and deliberate column widths; numbers correctly paired; Unicode strings and link label visible; header and footer clear |
| [Page 2](preview-page-2.png) | `bb56c70bdce864ad82f22b3c7335285167c857a5abb129570cb89353a7fe4d8b` | Four numbered steps intact; pending-review qualification visible; second link label clear; closing boundary statement present; correct header and page 2 footer |

Both pages were opened at readable resolution. No clipping, overlap, missing visible glyphs, broken row boundaries or unexpected blank pages were observed. Header/footer regions and link label locations were checked separately. The source was also rendered and both source pages inspected before the final export. Both source preview and final export used LibreOffice, so their agreement is not an independent Word rendering comparison.

## Negative controls actually run

Separate disposable copies were deliberately damaged; the included artifacts were preserved. Each of these checks exited 1 and reported `machine_checks_passed: false`:

| Damaged copy | Observed failure |
| --- | --- |
| PDF pages reversed | Ordered paragraph/table checks, page anchors, page labels and link pages failed |
| PDF page 2 removed | Missing body content, page count, page anchor and second link failed |
| First PDF link pointed to a different revision | Link target check failed |
| DOCX contained an unresolved inserted revision | Preflight stopped with a source-feature review issue |

These controls establish that those specific defects are detected. They are not a claim that all possible conversion defects are caught.

## Independent readback

A separate review ran the inspected checker on the exact supplied DOCX/PDF and repeated the four damaged-copy checks. Fresh renders of the supplied PDF matched both preview images byte-for-byte. Both pages, table associations, Unicode strings, release qualifications, link-label rectangles and page footers were independently inspected; source and delivered bytes remained unchanged. Native metadata, local links and the referenced official documentation were also checked. This review did not repeat DOCX conversion or add Word, browser-link, accessibility or other-viewer coverage.

## Limits

The PDF reports tagging and contains a structure tree. Neither was treated as accessibility approval. Reading order, assistive technology behavior, PDF/UA, PDF/A, screen-reader support and digital-signature validity were not validated. The document itself retains the pending screen-reader review.

Microsoft Word, other operating systems, printers, mobile PDF viewers and actual link navigation were not tested. Neither fictional URL was visited. No upload, account action, installation or permission change was performed. The result is an inspected two-page example in this toolchain; rerun and visually inspect any regenerated export before using it.
