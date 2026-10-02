# Tool behavior that changes the workflow

Checked on 2026-10-02. The example used OCRmyPDF 16.7.0+dfsg1 and Tesseract 5.5.0. Current online documentation may describe newer versions; check local `--version` and `--help` before applying a flag. The example's legacy flags are intentional.

## OCRmyPDF

`--skip-text` skips an entire page with existing text; it does not prove that all image text on that page is searchable. `--redo-ocr` attempts to replace detectable invisible OCR while preserving visible text and can OCR image content on mixed pages. Some older OCR representations are not distinguishable from visible text. `--force-ocr` rasterizes content and can flatten interactive objects, so it is not the default preservation route. Version 17 added corresponding `--mode` names. See the official [advanced OCR behavior](https://ocrmypdf.readthedocs.io/en/stable/advanced.html#when-ocr-is-skipped).

The sidecar contains newly recognized OCR text, excluding preserved native text and pages not OCRed. Whole-document extraction needs a separate readback. Page selection does not by itself disable whole-file optimization or PDF/A conversion. OCRmyPDF cannot add OCR while preserving a digital signature; its signature-invalidating override requires a deliberate authorized workflow, not an automatic retry. See the official [sidecar guidance](https://ocrmypdf.readthedocs.io/en/stable/cookbook.html#produce-pdf-and-text-file-containing-ocr-text), [selected-page processing](https://ocrmypdf.readthedocs.io/en/stable/cookbook.html#process-only-certain-pages) and [signed PDF warning](https://ocrmypdf.readthedocs.io/en/stable/cookbook.html#digitally-signed-pdfs).

## Tesseract

Use `tesseract --list-langs` to inspect installed models. Specify languages with `-l`; combinations and their order can change recognition. hOCR and TSV expose text, positions and confidence information for review. They are intermediate recognition results, not a proof of accurate transcription. The official [command-line documentation](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html) describes language selection, searchable-PDF, hOCR and TSV outputs. [OCRmyPDF's language installation notes](https://ocrmypdf.readthedocs.io/en/latest/languages.html) explain the separate language-pack dependency.

## pypdf and PyMuPDF

pypdf extracts stored PDF text; it does not read characters from image pixels or validate existing OCR. Extraction is valuable alongside visual inspection, especially for comparing native pages. Layout and reading order require review. See [pypdf text extraction](https://pypdf.readthedocs.io/en/stable/user/extract-text.html).

PyMuPDF's OCR `TextPage` can support extraction/search in memory; that operation alone does not establish that a delivered PDF has a saved OCR layer. Reopen the written artifact for the final tests. See [PyMuPDF OCR recipes](https://pymupdf.readthedocs.io/en/latest/recipes-ocr.html).

`Page.search_for()` returns rectangles or quads. A wrapped or hyphenated phrase can produce several results, and adjacent repetitions can be combined. Its normal case-insensitive handling has Unicode limits. Check the actual selected text and target viewer behavior for the task. Most page-method coordinates refer to unrotated space; use the documented transforms for rotated pages. See [search behavior](https://pymupdf.readthedocs.io/en/latest/page.html#Page.search_for) and [page coordinates](https://pymupdf.readthedocs.io/en/latest/page.html#modifying-pages).
