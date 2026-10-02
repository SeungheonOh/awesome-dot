# Mapping and reconciliation

Selection: the entire supplied `fixture/source.json`, format `pocket-shelf/1`, with no excluded records or fields. Its export timestamp is the supplied literal `2026-09-28T17:30:00+02:00`. Source byte identity is recorded in [reconciliation.json](reconciliation.json).

| Sheet | Row meaning | Source mapping | Data rows |
| --- | --- | --- | ---: |
| Collections | One parent occurrence | `/collections/{p}` | 5 |
| Items | One item occurrence | `/collections/{p}/items/{i}` | 4 |
| Labels | One scalar label occurrence | `/collections/{p}/labels/{i}` | 3 |
| Source paths | One actual JSON node, then declared missing-field observations | Exact source pointer, parent pointer, original key/index and traversal ordinal | 51 actual + 6 missing |
| Read me | Metadata and interpretation notes | Filename, digest, source version and scope | 16 information rows |

Parent and child indices start at zero. IDs remain business data; pointers identify occurrences. `Items.Parent pointer` and `Labels.Parent pointer` match `Collections.Source pointer`. Both identical `home` labels survive with different pointers and indices. The tables can be filtered independently. No field normalization, row deduplication, timestamp conversion or Cartesian product is applied.

## State accounting

| Field or relationship | Present non-empty | Empty | Null | Missing |
| --- | ---: | ---: | ---: | ---: |
| Collection note | 1 string | 1 empty string | 1 | 2 |
| Items relationship | 2 arrays containing 4 items | 1 empty array | 1 | 1 |
| Labels relationship | 2 arrays containing 3 labels | 1 empty array | 1 | 1 |
| Item quantity | 2 integers, including zero | 0 | 1 | 1 |
| Item note | 1 string | 1 empty string | 1 | 1 |

`Items` counts reconcile as `2 + 0 + 0 + 0 + 2 = 4`; `Labels` counts reconcile as `2 + 0 + 0 + 1 + 0 = 3`. These equations count child occurrences; the zero contributions from null/missing relationships do not convert their blank count cells to numeric zero.

The three blank-looking note states mean different things. `EMPTY_STRING` restores `""`; `NULL` restores `null`; `MISSING` omits the field. A quantity value of 0 is a native numeric cell paired with `INTEGER`. A supplied empty relationship has `EMPTY_ARRAY`, no child rows and count 0; explicit null and missing relationships have distinct states and blank count cells.

`Source paths.Scalar JSON` is an inert scalar JSON token. Strings carry JSON quotes, null carries `null`, integers carry their exact decimal token, and containers have no scalar token. States plus parent links rebuild objects and arrays in source order. The root is the empty pointer. Extra `MISSING` rows have no node ordinal or scalar token and are excluded from reconstruction. `View cells` connects each review record/field to its original source pointer, including absent-field observations.

## Saved evidence

The saved authored XLSX and a separately saved LibreOffice copy passed exact row, pointer, type, value, relationship, field-presence and source-tree reconstruction checks. Long IDs remained strings, `03/04/05` remained text, and `=1+1` remained text with no formula node. The workbook has filterable tables and frozen headers. No formulas, macros, data connections or external relationships were found.

All five sheets were rendered through LibreOffice and visually reviewed. The [previews](previews/collections.png) show the saved native copy. Native readback establishes behavior for the recorded local LibreOffice build only. Excel and cloud applications were not tested. Editing review cells is outside the static conversion contract and does not update state or lineage automatically.

The [controls](controls.json) hold 13 malformed/unsupported input cases, detect nine deliberately damaged workbook copies, and preserve repeated-ID/label occurrences. The source digest remained unchanged. These are internal conversion checks against the supplied fixture; they do not prove account completeness, provider authenticity, or live-service import suitability.
