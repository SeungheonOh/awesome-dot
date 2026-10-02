# Pine Room selected-page packet

All text and vector drawings are original and fictional. The room content is only a mixed-page-layout fixture for digital document assembly. No live document, account, service or external image is involved. The example uses bundled ReportLab Vera fonts, embedded as subsets; it does not redistribute separate font files.

## Request and result

> Make a new packet in this exact order: Notes A physical page 1, Layout B physical page 2, Notes A physical page 2, Notes A physical page 3. Keep the second page landscape and keep the blank divider. Preserve page content and the appendix link. Keep all three source bookmarks, ordered by their output destinations. Keep the originals; do not replace an existing output.

The sources are [Notes A](examples/source-a.pdf), three pages, and [Layout B](examples/source-b.pdf), two pages. B1 is an explicitly excluded draft. A2 is a genuinely empty page with no label added to its ink. No page is cropped, rotated, rescaled or rasterized.

| Saved output | Original page | Content | Navigation |
| --- | --- | --- | --- |
| 1 | A1 | Setup summary, portrait | Appendix link now targets output 4; summary bookmark |
| 2 | B2 | Reading room diagram, landscape | Layout bookmark |
| 3 | A2 | Intentional blank, portrait | None |
| 4 | A3 | Equipment appendix, portrait | Appendix bookmark |

The [packet](examples/packet.pdf) contains these four pages. The [preview](examples/preview.png) adds labels outside the page images solely to show lineage; those labels are not new PDF content. The [machine-readable map](examples/page-map.json) carries the exact source hashes, physical indices, text, content-stream hashes and page geometry. The [verification record](examples/verification.md) states what was actually checked.

## Reproduce locally

Use an environment with Python, pypdf, ReportLab, Pillow and Poppler `pdftoppm` already installed. The script installs nothing, contacts no service, uses no credentials and refuses an existing creation directory. It was exercised with the versions recorded in [verification.json](examples/verification.json).

From this skill directory:

```bash
python scripts/example.py check examples
python scripts/example.py create new-example
python scripts/example.py negatives new-example new-negative-copies
```

`check` is read-only. It checks the saved identities, exact page order/content/geometry and destination targets against the included sources and map. It does not perform a viewer click test or rerender the included preview.

`create` writes new fictional sources, the packet, page map, a 100-DPI render of every source/output page, the preview and an automated record. Its four selected source/output RGB render comparisons must be equal; the saved blank must be entirely white. Open all generated page renders yourself. The newly generated record deliberately says manual review is pending. PDF serialization or renderer/font versions can change binary hashes; assess a new run's own identities and checks rather than assuming it reproduced the reviewed bytes.

`negatives` writes disposable copies in a new directory, leaving the good packet and sources unchanged. It must catch missing selected-link targets, an unsupported optional-content catalog, existing output, wrong order, dropped blank, changed rotation, changed CropBox, a broken internal link and a graphics-only content change. The graphics mutation must leave extracted text unchanged while changing the decoded content hash. A caught negative is evidence that this narrow check notices that fault, not proof that every corruption is detectable.

## Supported example boundary

The script accepts only simple native pages with direct `/Fit` internal links with invisible borders and plain, flat source outlines. It rejects forms/signature indicators, encryption, name trees, attachments, page labels, tags, layers, actions and catalog/page/annotation features outside its explicit support set. It rejects repeated selected pages because no occurrence policy is implemented. An omitted outline target also causes a hold.

The fixture contains none of those protected features. This gate is deliberately conservative and does not constitute an exhaustive audit of arbitrary nested PDF objects. Use the guide's inspection and an appropriate tool for real forms, signatures, complex navigation or accessibility requirements. Do not relax the gate merely to obtain an output file.

The script copies page resources and decoded content while rebuilding the supported links/bookmarks; the new packet gets its own descriptive metadata. All original printed numbering remains unchanged. No external URLs exist in the fixture, and no URLs are opened by any check.

## Primary implementation references inspected

The installed pypdf 6.10.0 implementation/docstrings were read for `PdfWriter.add_page` and `excluded_keys`, `add_annotation`'s returned inserted object, `add_outline_item`, `PdfReader.get_destination_page_number`, `Link` and `Fit.fit`. The ReportLab 4.4.9 docstrings/implementation were read for `Canvas.linkRect`, `bookmarkPage`, `TTFont` and `registerFont`. These are version-specific primary library sources, not a claim that every PDF construct is supported.

In particular, the example does not depend on implicit link importing: it copies a shallow page object without its annotations, creates a supported link through `add_annotation`, then explicitly sets its `/Dest` to the actual output page's indirect reference and `/Fit`. It reopens that saved reference and independently checks the resolved page. The originals and their reader page dictionaries retain their annotations.
