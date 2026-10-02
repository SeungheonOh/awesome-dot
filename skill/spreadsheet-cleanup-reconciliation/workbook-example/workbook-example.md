# Worked XLSX example: equipment counts with unresolved evidence

A workshop coordinator wants to use a small equipment export to plan loans. A spreadsheet formula already subtracts reserved units from ready units. The export contains a padded kit ID, a count stored as text, a real zero, two different missing-count states and two disagreeing rows for the same kit. Cleaning the export must preserve its calculations without making the inventory look complete.

All equipment, identifiers, counts and instructions in this example are original fictional data. No live account or user information is involved. The Markdown and JSON describe the decisions; the XLSX files make the calculation and preservation claims inspectable.

## The authorized task

> Make a cleaned XLSX copy of equipment-export-A. Keep kit IDs as text, including their leading zeros. Remove only surrounding export padding from IDs and counts. Convert non-negative whole-unit count strings to numbers. Keep source blanks empty with reason blank. Convert the exact source marker N/A to an empty numeric count with reason source_marker; retain N/A in Review reason and the change ledger. Map the supplied status aliases. Keep row order and every record, including the two rows for kit 0044. Put unresolved evidence in Review reason. Preserve formulas and workbook features. Leave the source intact; do not import the candidate into a live inventory system.

The source specification in [fixture.json](fixture.json) supplies the status dictionary and field rules. [expected.json](expected.json) records the exact expected cell decisions and saved results independently of the transformation implementation. [reproduce.py](reproduce.py) builds and checks this particular example; it is not a general workbook importer.

## Inputs and intended decisions

The source contains two sheets. `Inventory` has six detail records in rows 8–13, an autofilter, frozen headers and identifying columns, whole-unit validation, conditional formatting and a named range. `Overview` uses formulas to summarize the detail. There are no hidden records, merged cells, native tables, charts, macros, pivots or external connections.

| Source row | Kit ID as supplied | Ready | Reserved | Decision |
| --- | --- | ---: | ---: | --- |
| export-A:1 | ` 0007 ` | text ` 4 ` | 1 | Trim ID to text `0007`; parse 4 as a number |
| export-A:2 | `0012` | numeric 0 | 0 | Keep both zeros; zero is evidence of none |
| export-A:3 | `0025` | blank | 1 | Keep missing; record `source blank` |
| export-A:4 | `0031` | text `N/A` | 0 | Convert count to blank; preserve `source_marker (N/A)` in review and raw N/A in the ledger |
| export-A:5 | `0044` | 3 | 1 | Keep row; flag conflicting key |
| export-A:6 | `0044` | 5 | 1 | Keep row; flag conflicting key |

Ready counts and reserved counts are whole equipment units. Status normalization is limited to the supplied dictionary: `ready` → `ready`, `count pending` → `needs_count`, and `hold` → `on_hold`, after trimming and case-folding. There is no supplied rule that authorizes collapsing kit 0044. The record identifier in column A provides stable lineage even where the business key repeats.

The candidate changes 11 cells: seven input normalizations and four review annotations. It inserts, removes, reorders and merges no records. The immutable source retains the exact original marker and whitespace; the candidate's review reasons keep the two kinds of missing count visible.

## Preserve calculations, then check what was actually saved

Each detail formula returns `unknown` unless both counts are numeric. For example, `Inventory!F10` contains:

```text
=IF(OR(NOT(ISNUMBER(D10)),NOT(ISNUMBER(E10))),"unknown",D10-E10)
```

`Overview!B4` sums the named range `AvailableUnits` (`Inventory!$F$8:$F$13`) and is labeled **Numeric row-availability subtotal**. `B5` counts `unknown` results. `B8` shows the availability contributed by both 0044 rows, and `B9` subtracts that contribution. This adds export rows, including the disputed pair; it cannot establish an actual usable or unique inventory total. That total remains unresolved.

| Saved result | Source workbook | Cleaned candidate | Why |
| --- | ---: | ---: | --- |
| Numeric row-availability subtotal | 6 | 9 | Converting text ` 4 ` allows the first row to calculate `4 − 1 = 3` |
| Rows without numeric counts | 3 | 2 | The numeric-text row becomes calculable; the two missing counts remain missing |
| Export records | 6 | 6 | Every record is retained |
| Numeric row subtotal from disputed kit 0044 | 6 | 6 | Both conflicting records still contribute |
| Numeric row subtotal outside 0044 | 0 | 3 | The first row's available units become calculable |
| Numeric ready-count cells | 3 | 4 | Numeric zero is counted; the blanks are not |

The source's semantic numeric-row subtotal is already 9 if its digit string is interpreted under the supplied export rule. The change from its displayed 6 to the candidate's displayed 9 corrects representation, not inventory quantity. No new stock or balancing row is invented; neither 9 nor the source's 6 is claimed as actual usable inventory.

An independent arithmetic check uses only the rows with known ready counts:

```text
Known ready units:       4 + 0 + 3 + 5 = 12
Comparable reserved:    1 + 0 + 1 + 1 =  3
Numeric row subtotal:  (4−1) + (0−0) + (3−1) + (5−1) = 9
Disputed contribution: (3−1) + (5−1) = 6
Outside that conflict:  9 − 6 = 3
Population:             6 source records = 6 retained + 0 absorbed + 0 excluded
```

The one reserved unit on kit 0025 is excluded from that comparable subtraction because its ready count is missing. Summing all reservations against only known ready counts would understate the known-row subtotal.

## Evidence still needed

| Evidence gap | Exact source location | Candidate behavior | Smallest needed decision |
| --- | --- | --- | --- |
| Missing ready count | `Inventory!D10`, export-A:3, kit 0025 | Blank count; `F10 = unknown`; reason says source blank | Obtain the ready-unit count |
| Missing ready count | `Inventory!D11`, export-A:4, kit 0031 | Blank count; `F11 = unknown`; reason retains `source_marker (N/A)` | Obtain the ready-unit count |
| Conflicting kit records | `Inventory!B12:E13`, export-A:5–6, kit 0044 | Keep both rows and 6 available units in the provisional subtotal | Establish whether both records are valid, or supply an authoritative survivor rule |

There is no independent inventory control. Internal row and arithmetic reconciliation can pass while those questions remain open. Review annotations record the evidence state of this cleanup; they are not an automatic case-management system. Update them when new evidence authorizes a correction.

## Reproduce locally

Use already installed Python 3.10 or newer, `openpyxl`, `XlsxWriter`, LibreOffice (`soffice`) and Poppler (`pdftoppm`). This workflow installs nothing and uses no network calls. Run from the directory containing this guide:

```bash
python3 reproduce.py --output ./run-local
```

The output directory must not exist. Existing outputs are refused, including an existing-directory symlink. Choose a new directory for another run. The runner preserves each intermediate file and records command arguments, exit codes and output in `report.json`, or `failure.json` if a step fails. If the operating system does not expose those executable names, supply the existing paths with `--soffice` and `--pdftoppm`.

The run proceeds in this order:

1. Create the fictional source with explicit string ID cells and formulas. The initial writer does not calculate formulas.
2. Open and save it through LibreOffice using a new isolated profile and output directory. Capture the resulting source hash, then read its actual saved caches.
3. Export a source PDF and PNG previews before editing.
4. Load a formula-preserving copy with `openpyxl`, make only the expected cell changes, and save it in another directory.
5. Open and save that candidate through LibreOffice with another isolated profile. Reopen the saved result both with formulas and with cached values; read its formula/cache entries directly from the XLSX package too.
6. Compare exact formula expressions, unchanged values, number formats, sheet order, names, filter, frozen panes, validation and conditional-format rules against the captured source. All existing cell styles must match; the four newly populated Review reason cells must match the existing body style. Calc resolves font and alignment inherited by those formerly empty cells when text is inserted. Check lineage, identifier text types, missing cells, numeric zero, expected results and the absence of formula-error cells.
7. In a disposable copy, set the missing `Inventory!D10` count to numeric zero. Recalculate and save through LibreOffice. `F10` must become −1, the subtotal must become 8, and one other missing count must remain visible. The candidate is untouched.
8. Export candidate PDF/PNG previews, confirm the source hash is unchanged, inspect document identity metadata and record source/candidate hashes and sizes. Visually inspect both candidate pages before delivery.

The tested engine can retain the writer's zero caches during a plain headless conversion. The runner therefore puts `OOXMLRecalcMode = 0` into each disposable profile. LibreOffice documents [recalculation on file load](https://help.libreoffice.org/latest/en-US/text/shared/optionen/01060900.html), and its [calculation-options enum](https://github.com/LibreOffice/core/blob/master/sc/inc/calcconfig.hxx) defines zero as always recalculate. This changes only the throwaway profile. The saved-value checks and changed-input probe establish whether that setting actually worked in a run.

## Inspect the checked example

Open the [captured source](checked/inventory-source.xlsx) and [checked candidate](checked/inventory-cleaned.xlsx). The [Overview preview](checked/overview.png) and [Inventory preview](checked/inventory.png) show the saved candidate. [Verification](verification.md) identifies the exact engine, scope, limits and hashes. These four binaries are listed in [the artifact manifest](artifact-manifest.json).

## What a reproduction creates

- `source/inventory-source.xlsx`: captured source with calculated source caches
- `candidate/inventory-cleaned.xlsx`: checked candidate with the same 15 formulas
- `report.json`: exact changes, formulas, raw saved caches, structure checks, engine version, command evidence and hashes
- `candidate-preview/page-1.png` and `page-2.png`: modest previews of Overview and Inventory, rendered by LibreOffice then Poppler

Keep the seed, edited pre-recalculation file, probe, profiles and failure logs as local reproduction evidence. They are not alternative cleaned workbooks. File bytes may differ between runs because document metadata and consumer serialization can change; compare the semantic checks and each run's own hashes.

The recorded run uses the exact LibreOffice development build stated in its report. It does not establish Microsoft Excel or live Google Sheets behavior, all-XLSX-feature preservation, source business accuracy or a live-system update. PDF rendering verifies a useful visual view; it does not simulate editing, filtering or validation interactions in every spreadsheet application.
