# Saved packet verification

Reviewed on 2026-10-02. The packet contains the four requested original fictional pages in the exact order A1, B2, A2, A3. B1 is excluded. Originals were preserved and an existing output was refused.

## Exact delivered identities

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| [source-a.pdf](source-a.pdf) | 43,498 | `5c39023adab77a661f28ad754b8e09dc7f00837e03dbb82e50ef3abdc8c0f3d1` |
| [source-b.pdf](source-b.pdf) | 42,947 | `7cb86eb048badec8ebc55e2c36e3782b60b4badc12330a95105a50b82620aae5` |
| [packet.pdf](packet.pdf) | 84,614 | `d9b84156679d5641a9047ab9c37f6301ef5ffd15d384ae022f21f6cd955a5dfb` |
| [preview.png](preview.png) | 108,701 | `372f27c606779ec3f5d04b80e2ff40ccbbbbb2631c4b6786b752435754b52600` |

The full per-page evidence is in [page-map.json](page-map.json); the structured check record is [verification.json](verification.json). Relative filenames are intentional.

## Checks performed on the saved bytes

- Parsed the source and saved PDFs with pypdf in strict mode. Source A has three pages; source B has two; the saved packet has four
- Inspected source catalog/page/annotation features. No encryption, standard form/signature indicators, embedded-file/name-tree catalog entries, unsupported page features or unsupported annotations were present. Source navigation consists of one direct internal `/Fit` link and three plain flat outlines
- Compared every output page with its designated source page: extracted text, decoded content-stream SHA-256, all five effective page boxes, rotation and UserUnit agree. Original source hashes remain unchanged
- Verified portrait pages 1, 3 and 4 retain `[0, 0, 612, 792]` boxes; landscape page 2 retains `[0, 0, 792, 612]`. All five effective boxes agree within each page; all rotations are 0 and UserUnit is 1
- Reopened the actual link annotation. Its rectangle remains `[46, 450, 325, 474]`, its invisible border and label remain intact, and its direct destination now references saved output page 4 with `/Fit`
- Verified three saved outline entries in output order: Setup summary -> 1; Reading room layout -> 2; Equipment appendix -> 4
- Independently read the saved packet using PyMuPDF 1.26.6. `Page.first_link.uri` is `#page=4&view=Fit`; `Document.resolve_link` returns zero-based page 3, confirming output page 4. `Document.get_toc` independently reports bookmark destinations 1, 2 and 4. No URL was visited
- Rendered all five source pages and all four saved output pages with Poppler `pdftoppm` at 100 DPI. All four selected source/output RGB pairs have equal dimensions and identical pixels. The saved divider is entirely white
- Visually inspected every source/output full-page PNG and the final preview. Summary text, diagram labels, arrow and appendix text are readable, with no clipping or overlap. The diagram remains landscape. The blank remains blank. Preview labels appear outside the page images

The assembly, saved readback and render commands finished successfully. The final generation run emitted no warnings.

Native-content readback uses an explicit `stream is not None` test: a present pypdf `ContentStream` can be falsey even when it has drawing or text bytes. The saved output pages have these decoded stream sizes and hashes, all equal to their mapped source pages:

| Output page | Decoded bytes | SHA-256 |
| --- | ---: | --- |
| 1 | 937 | `01e06bb4551333fe6ca2ee149a0757c58fabe8b3bed70a6a75a6b54774acb223` |
| 2 | 1,477 | `d7a1132f0c25342eaac6d2adaab5238afbaa5873e1e8be3e9cff9cf8dd0291f8` |
| 3 | 42 | `f7ac222654d26a9cb26ce3bd9a2475e49599e30866f6d349e2468eddb6999c08` |
| 4 | 617 | `812b17f602db5c57397fc654584ec5c59c9ba0176ddd78633bd6a2469698e3a2` |

The intentionally blank page has a small graphics-state stream despite rendering entirely white. Its stream is preserved too.

## Focused negative checks

Each check below was exercised on a disposable copy or a rejected selection. Original sources and the good packet stayed unchanged.

| Deliberate problem | Observed result |
| --- | --- |
| Select A1 but omit its A3 link target | Held before writing any output: missing link target |
| Reuse the existing packet output path | Refused; existing packet hash remained unchanged |
| Add a harmless `/OCProperties` catalog marker to a copy | Preflight held on unsupported optional-content feature |
| Swap the first two output pages | Saved content/geometry comparison failed on output 1 |
| Delete the selected blank | Saved page-count check failed |
| Rotate the landscape page 90 degrees | Saved geometry comparison failed on output 2 |
| Change its CropBox | Saved geometry comparison failed on output 2 |
| Redirect the appendix link to output 2 | Saved link-target comparison failed |
| Add a vector line without changing text | Extracted text stayed identical; decoded stream hash changed; saved native-content comparison failed on output 2 |

## Independent readback

An independent review reran the corrected saved-file check and all nine negative cases, compared the actual decoded content bytes for every mapped source/output pair, and confirmed the recorded nonempty stream hashes. It also held a repeated-page selection before writing an output. Fresh 100-DPI source/output renders matched for all four selected pairs; the blank remained white, and the four output pages were visually inspected. PyMuPDF independently resolved the internal link and bookmark destinations. All four reviewed PDF/PNG byte identities remained unchanged. These checks retain the viewer-click and broader feature limits below.

## Actual tools and boundaries

Python 3.12.14; pypdf 6.10.0; ReportLab 4.4.9 with its bundled Vera fonts; Pillow 12.3.0; Poppler `pdftoppm` 26.05.0. PyMuPDF 1.26.6 supplied the additional independent navigation check. Nothing was installed, uploaded or fetched to make the example.

The [script](../scripts/example.py) reproduces the fixture, structural checks, render comparison and negative copies. A fresh script run does not claim that someone has visually reviewed its newly generated pages. The independent PyMuPDF check can be repeated from this skill directory when that optional package is installed:

```python
import fitz
document = fitz.open('examples/packet.pdf')
assert document.resolve_link(document[0].first_link.uri)[0] == 3
assert document.get_toc() == [
    [1, 'Setup summary', 1],
    [1, 'Reading room layout', 2],
    [1, 'Equipment appendix', 4],
]
```

These checks establish this packet's selected pages and supported navigation. No PDF viewer click test, signature validation, form-interactivity test, accessibility/PDF-UA/PDF-A assessment or universal PDF-feature preservation is claimed. One renderer's equality is limited to its recorded settings. The narrow fixture preflight is not an exhaustive PDF security scanner.
