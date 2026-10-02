---
name: spreadsheet-cleanup-reconciliation
description: "Clean an authorized workbook or CSV into a documented schema, preserve formulas and identifiers, investigate duplicates, and reconcile every source row and numeric change before delivering or applying the result."
---

# Clean a Spreadsheet and Prove What Changed

Turn a supplied workbook, CSV or named sheet into a usable dataset with a reversible change record. Finish the cleanup that the user authorized; isolate genuinely uncertain cells or records instead of holding the entire result for perfect data.

## Required inputs

- Source file or authorized sheet, relevant tabs/ranges and intended use
- Desired output schema or an example accepted by the downstream consumer
- Rules for dates, currencies, units, missing values, status aliases and duplicate treatment, when available
- Delivery instruction: cleaned copy, local export, or changes to a named existing sheet/range
- Any control totals, expected population or reference dataset used for reconciliation

Inspect the supplied inputs first. If there is no target schema, derive a conservative proposal from the existing columns and preserve all original fields. Ask only about decisions that would change meaning or scope. A cleanup request permits preparing a cleaned copy; it does not by itself authorize replacing a live source, deleting records, publishing data or adding viewers.

## Workflow

### 1. Capture the source before transforming it

Record source identity, filename or sheet ID, revision or retrieval time, selected ranges, file hash when available and extraction method. Keep an untouched source or verified version-history reference and work in a separate copy or staging area. Assign each record a stable lineage ID based on source and record ordinal; retain an existing business identifier separately. CSV record ordinal is not necessarily a physical line number because quoted fields can span lines.

Inspect the actual structure rather than treating the visible grid as the whole dataset:

- Inventory sheets, hidden rows/columns, filters, tables, merged headers, protected ranges, formulas, named ranges and external links
- Distinguish detail rows, subtotals, footer notes and blank separators before counting records or summing values
- For CSV, establish encoding, delimiter, quoting and the header row; preserve leading zeros and long identifiers as text
- For workbooks, inspect both formula expressions and available displayed/cached results without saving a values-only load over the source
- Identify unsupported features such as macros, drawings or data connections before choosing a library that may discard them

Do not run macros or refresh external connections to inspect a file. If available tools cannot preserve workbook features, make a separate data-only export with the loss clearly stated, or ask for an appropriate editing route. An inaccessible tab is a coverage gap, not an empty tab.

### 2. Define the schema and the meaning-preserving rules

Create a compact transformation specification before writing data:

```text
column | source column(s) | target type | nullable | accepted inputs
       | transformation rule | rule evidence | invalid-value treatment
```

Keep identifiers as text even if every current value contains digits. Separate date-only values from timestamps and retain timezone information where present. Do not infer a day/month convention from a single ambiguous date. Preserve original date text beside unresolved parsed values.

Treat blank, zero, not applicable, unknown and parse failure as distinct states unless the supplied business rules explicitly equate them. For amounts, keep a nullable numeric value and a reason when parsing is unresolved. Use decimal arithmetic with the evidenced scale; do not introduce rounding or combine currencies or units silently. Do not infer currency solely from a symbol with several meanings.

Apply only justified normalizations. An explicit status dictionary can map aliases; superficial similarity cannot. Trim whitespace only in fields where it is insignificant, not inside free-text notes or identifiers that may contain meaningful spaces. Preserve unknown categories and report them rather than forcing the nearest match. Standardize headers without discarding duplicate column names: resolve collisions visibly or retain source-position identifiers.

### 3. Build a profiled, reversible candidate

Profile the selected population before and after transformation: record counts, null/zero/parse-failure counts, distinct business keys, category values and typed-value ranges. Calculate source control totals separately by currency/unit and exclude subtotal rows from detail totals.

For each changed cell or rule-applied group, retain the source location, original value, proposed value, rule ID and reason. Keep raw fields alongside normalized values when the source cannot otherwise be traced reliably. Preserve row order unless sorting is requested; never sort one column independently of its records.

For a workbook edit, change only authorized input cells. Preserve formula expressions, references, number formats and intentional blanks. Inserting, deleting or moving rows can change formulas, table ranges and named ranges; test those effects explicitly before applying. A cached formula result is not proof that the edited workbook has recalculated. If a supported calculation engine is unavailable, state that formulas were preserved but results were not recalculated.

Treat formula-like text from CSV as data. Do not evaluate strings beginning with spreadsheet formula triggers while parsing. When a spreadsheet-facing output could interpret such text as formulas, use a format that explicitly stores the affected cells as text, or produce a separately documented safe display export; retain the original text in the immutable source. Avoid silently altering machine-import values with escape prefixes.

### 4. Resolve duplicates only with a supported record rule

Compare several views: byte-equivalent records, equality after approved normalization, repeated business keys and similar-looking records. These are different observations, not interchangeable evidence that a row is disposable.

For each candidate group, show source IDs, matching fields, differing fields and a proposed disposition. Collapse a group only when the user or an authoritative dataset rule establishes that it represents one record. Specify which record survives and carry all source IDs into its lineage. When repeated keys have conflicting amounts, dates or statuses, keep the records and flag the conflict unless an evidenced version/supersession rule resolves it. Recency or completeness alone is not such a rule.

Do not merge two rows merely because names match, or delete an exact repeat that may represent a legitimate repeated event. For unresolved groups, a review column or exception register is a useful finished result. Apply independent, safe normalizations to those records while preserving the disputed values.

### 5. Reconcile the candidate before writing it

Explain every change in population and every numeric difference:

```text
source detail records = kept source representatives + absorbed duplicate records
                      + excluded records + quarantined records

output rows = kept source representatives + deliberately added output rows

output known-value total = comparable source known-value total
                        - removed known values + added known values
                        + documented corrections
```

Count a source record in exactly one disposition. When a transformation splits or combines rows, use a many-to-many lineage map instead of forcing the simple row equation. Assign any synthesized row its own ID and derivation; do not invent balancing rows to force agreement.

Reconcile separately for every currency, unit and relevant accounting period. Report null and parse-failure populations alongside known-value totals; a matching sum can hide missing values or duplicated zeros. Show how unresolved duplicate groups contribute to a provisional total. Compare to independent controls when supplied, and investigate residual differences rather than adjusting data to fit them. If there are no controls, say that internal reconciliation passed, not that business completeness was proved.

### 6. Apply the authorized result and read it back

For a cleaned-copy request, write the requested artifact with source lineage, exceptions and a concise change summary. Preserve workbook functionality when the output is a workbook; do not substitute CSV when formulas or multiple tabs are required. For an authorized in-place edit, re-read the destination revision and target cells immediately before writing. Stop conflicting portions if another editor changed them; continue unaffected ranges where safe.

Use narrow range writes or a staged, validated replacement within the user's instruction. Do not clear an entire sheet to replace a subset. Do not change access permissions or upload to a new service merely to deliver the file. If a write times out, inspect the target state before retrying.

Reopen the saved artifact or re-fetch the written ranges. Verify schema, row dispositions, identifier text, null/zero distinctions, formulas and reconciled totals from that readback, not from the in-memory candidate alone. Inspect workbook rendering or representative cells for truncated headers, unintended date conversions and formula errors. Verify formula expressions across the affected region and flag calculation results that could not be independently refreshed. Confirm source preservation and provide the actual artifact or verified destination.

## Deliverables

Return the cleaned artifact or applied-sheet result, its scope and a short summary of what changed. Include:

- Transformation specification with the evidence for non-obvious rules
- Source-to-output lineage and a change/disposition ledger
- Unresolved exceptions with source cells/records, impact and the smallest decision needed
- Before/after reconciliation by currency or unit, including missing-value coverage
- Actual readback checks, formula-recalculation status and any preservation limitations

Do not bury a material unresolved key conflict in an “all checks passed” statement. A usable cleaned copy can be complete while explicitly retaining unresolved business questions.

## Verification

1. Trace every output row to its source or documented derivation and account for every source detail record
2. Check leading-zero and long identifiers, quoted delimiters and date ambiguity against the raw source
3. Check that blanks and parse failures did not become zeros and unknown statuses did not acquire invented meanings
4. Review at least one duplicate group against its actual authorization and survivor rule
5. Recalculate control totals independently of the transformation path and explain all differences
6. Reopen the output, compare formulas and identifiers, and confirm that only the authorized destination changed

Use [the fictional worked example](example.md) for an executable-sized fixture with authorized duplicate collapse, a retained key conflict, nullable amounts and currency-separated reconciliation.

For native formulas and saved XLSX readback, use [the equipment-workbook example](workbook-example/workbook-example.md). It preserves text IDs and workbook structure, retains missing-count and key-conflict evidence, and checks saved results after a local LibreOffice round trip and a disposable zero-input probe.

## Stop and ask

- Ask when a locale, key rule, missing-value convention or target range would materially change the result; finish unaffected cleanup first
- Ask before destructive source replacement, deletion or new sharing that the user has not authorized
- Preserve a conflicting or unparseable value and report its consequence; never choose the interpretation that makes totals agree
- Do not claim that normalization validates the underlying transaction, identity or business event

## Example request

```text
dot, clean this supplied order-ledger export into a new workbook. Keep customer IDs as text, use the attached status dictionary, and leave ambiguous dates unresolved. Collapse only exact repeated export records under the supplied export rule, preserve conflicting repeated order IDs, and give me source-row lineage and per-currency reconciliations. Save the cleaned copy in the authorized folder and read it back; leave the original file intact.
```

## Evidence status

The CSV fixture establishes internal consistency. The native workbook companion records the exact local LibreOffice build, recalculation and saved-file checks actually performed on fictional data. Neither example establishes a live-system write or broad application compatibility. Report only the operations and verification actually performed during each use.
