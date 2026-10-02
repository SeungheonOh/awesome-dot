# Verification record

The original fictional fixture and the included workbook were checked locally on 2026-10-02. No installation, network retrieval, account access, live-service write or upload was involved.

Installed versions used:

- Python 3.12.14 for strict parsing, source-tree reconstruction and independent ZIP/XML checks
- Node.js v24.19.0 and `@oai/artifact-tool` 2.8.59 for authoring
- LibreOfficeDev 26.8.0.0.alpha0, build `2c87e51eeaa2b413ff4ae097b2705eea1995d8e5`, for a real saved-file round trip and native PDF rendering
- Poppler `pdftoppm` for rasterizing the native PDF into the included previews

The [portable runner](scripts/reproduce.py) completed end to end. Both the authored XLSX and the saved native-consumer copy reconstructed all 51 actual JSON nodes, every scalar type/value, object field presence and order, ordered child arrays, and all parent links. Six missing optional fields were represented separately. The checker also verified exact review-cell mappings, long string IDs, zero and blank states, literal formula-looking text, sheet/header order, table/filter extents, frozen header/identifier panes, source metadata and the absence of formulas, macros, connections, external relationships and spreadsheet error cells.

All five native sheet previews were visually inspected. Full IDs and the literal `=1+1` remain legible. Counts are separated from state labels, every table header fits, and the complete source-path sheet includes the missing-field observations. No claim is made about Excel or cloud-application behavior. The supplied timestamp uses explicit JSON-text encoding; unsupported direct timestamp conversions are held, not inferred.

The [control results](outputs/example/controls.json) record 13 rejected input cases, nine detected saved-file corruptions, and two occurrence-preservation controls. Rejections include duplicate keys expressed with literal and Unicode-escaped spellings, malformed JSON, unsupported numeric/text conversions, unknown fields and wrong relationship shapes. Corruptions include erased zero, changed ID, wrong parent, state change, executable formula, removed child, changed source pointer, and added content outside the declared review or metadata areas. The original source digest remained unchanged.

Use [artifact-manifest.json](artifact-manifest.json) for exact included binary/source sizes and SHA-256 digests. The source has 1,089 bytes. The workbook has 13,980 bytes. [reconciliation.json](outputs/example/reconciliation.json) identifies the authored workbook; [native-readback.json](outputs/example/native-readback.json) identifies the separately saved consumer copy tested. The consumer copy is verification evidence, not an additional deliverable. Serialization metadata can make repeated runs produce different binary digests without a content change; each run reports its own identities and repeats semantic checks.

These checks establish conversion fidelity to the selected fixture. They do not establish provider authenticity, account-wide coverage, arbitrary-schema support, or suitability for a live import. The workbook is a static review copy and its value/state evidence does not automatically update after manual edits.

## Independent readback

A separate readback checked the exact authored workbook, the saved consumer copy and another disposable LibreOffice save. Each reconstructed the same 51 source nodes and six absent-field observations. The 13 input holds and seven saved-file corruption cases passed again. A fresh four-parent input retained 38 source nodes, three absent fields, repeated IDs and independent sibling occurrences in the derived mapping; it was not authored as another workbook. Four additional input variants held Boolean quantity, a numeric ID, an unknown nested field and unsupported surrogate text, and a saved zero-to-text mutation failed the cell-type check. Direct XML readback confirmed the long identifiers and literal `=1+1` are strings while quantity zero is numeric. This review did not repeat workbook authoring or test Excel, cloud applications or interactive controls. The native previews were separately inspected.

A later altered-copy probe found that an extra populated cell outside a declared area escaped the original checker. The checker now rejects such content on all five sheets. The two new controls cover the review and metadata areas; all 13 input holds and nine corruption controls passed after the correction. A formatting-only extra cell with no value still passes. The source, workbook, previews and prior native-consumer evidence were unchanged.
