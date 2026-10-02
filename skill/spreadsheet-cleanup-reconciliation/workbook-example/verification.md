# Native workbook verification

Checked on 2026-10-02 UTC. [Saved-file evidence](checked/verification.json) records the actual local consumer operations and results. The [guide](workbook-example.md) explains the fictional source, exact authorized transformations and reproduction command.

## Result and scope

The candidate retains six export records and all 15 formula expressions. Its headline is **Numeric row-availability subtotal**, with **9 units** and an adjacent statement that both disputed 0044 rows are included. Actual usable inventory remains unresolved because two counts are missing and no rule settles the repeated key. The 9-unit result is not a unique-item inventory total.

The source's saved row subtotal is 6. Converting its text ` 4 ` to numeric 4 makes the first row's `4 − 1 = 3` calculable, producing the candidate's 9 without changing the underlying equipment quantity. Both 0044 rows remain and contribute 6 of those 9 units.

The fixture explicitly permits the exact marker N/A to become an empty numeric count. The candidate preserves `source_marker (N/A)` in `Inventory!H11`; its change ledger retains the raw N/A-to-blank decision and the review annotation. The other missing count retains its separate source-blank reason. `0012` keeps numeric zero, and all six kit IDs retain leading zeros as text.

LibreOffice recalculated and saved the source, candidate and a disposable probe. Saved values were read with `openpyxl` and directly from the XLSX formula/cache XML. In the probe, setting only the missing `Inventory!D10` count to numeric zero makes `F10 = −1`, changes the row subtotal to 8 and leaves the other missing count and key conflict visible. The delivered candidate is unchanged.

## Preserved structures and visual readback

The saved source/candidate comparison retained sheet order and visibility, the `AvailableUnits` name, `A7:H13` filter, `C8` freeze panes, whole-unit validation, conditional-format rules, print areas, gridline settings, formula text, row lineage and number formats. Existing cell styles matched. Four newly populated review cells were checked against the existing body style after LibreOffice resolved their inherited font/alignment.

The [Overview](checked/overview.png) and [Inventory](checked/inventory.png) previews were inspected at 1400-pixel page width. The subtotal label, unresolved-inventory statement, IDs, blank cells and provenance annotations are readable without truncation. These are LibreOffice PDF exports rendered by Poppler.

The captured source hash remained unchanged. Reusing the output directory was rejected before any operation. The runner forces recalculation in a disposable profile, then checks actual saved caches and changed-input behavior; export success alone is not treated as recalculation evidence.

## Engine, identity and limits

Exact consumer: `LibreOfficeDev 26.8.0.0.alpha0 2c87e51eeaa2b413ff4ae097b2705eea1995d8e5` on Linux. Python 3.12.14, openpyxl 3.1.5 and XlsxWriter 3.2.9 were already installed. No packages were installed.

[Metadata readback](checked/metadata.json) contains only the generic creator/last modifier `awesome-dot fictional example`, fictional title/subject, timestamps, language and LibreOffice's application identity. Custom properties are empty. There are no macros, external relationships, links, connections or embedded objects.

Microsoft Excel and live Google Sheets were not tested. No charts, native tables, pivots, protected sheets or external connections are present, so their preservation is not claimed. Validation and conditional-format structures were checked; interactive behavior across spreadsheet applications was not. There is no independent business inventory control.

## Selected binaries

Exact sizes and hashes are in [artifact-manifest.json](artifact-manifest.json). Every selected file is below 2 MiB.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| [Captured source](checked/inventory-source.xlsx) | 10,918 | `a071ed3b3b13e6e4f4c6af4d961feedd060ea130fac7475bf97ee4839a371176` |
| [Checked candidate](checked/inventory-cleaned.xlsx) | 10,956 | `7af51e41a55b387290ed637936e2b420a7feab69d6872e4a63b3edb27b11e6b0` |
| [Overview preview](checked/overview.png) | 126,567 | `661c19e8efbc47d618e3edeba721d90880165ced8eae9b51d2dd2d1e7884064f` |
| [Inventory preview](checked/inventory.png) | 113,686 | `c94a2e337418f1dce07d8ce8b8936fb9cbbc07b99e2eca2683fa67f7a6647845` |

## Independent readback

An independent review checked the supplied source, candidate and probe caches, formula expressions, scoped cell changes, native workbook structures, metadata and approved binary hashes. It then opened the supplied pre-recalculation candidate and zero-probe input through fresh isolated LibreOffice profiles: the numeric row subtotal recalculated to 9, then 8 with the changed row at −1. The remaining missing count and repeated-key conflict stayed visible. This pass did not rebuild the original source fixture.
