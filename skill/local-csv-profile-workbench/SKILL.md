---
name: local-csv-profile-workbench
description: Build a privacy-preserving browser CSV profiler with strict record validation, explicit missing-value rules, numeric summaries, distributions, and safe previews without uploading source data.
---

# Local CSV profile workbench

Build an inspection surface that helps a user understand a table before plotting or analyzing it. The worked product, Table Lens, accepts a local file or pasted CSV, reports types and missing values, previews records, and draws one selected column's distribution entirely in the browser.

## Inputs and decisions

Establish the expected file size, row/column limits, header policy, supported separators, missing-value definition, and desired persistence. If none are given, a bounded browser-only tool can start with 1 MiB, 20,000 data rows, 50 columns, a required first header row, and comma/semicolon/tab input. Use a clearly synthetic sample until the user supplies data.

Never infer permission to upload a user's table from permission to host the application. Keep parsing and analysis client-side when local processing is the promised behavior. Do not add analytics, remote parsers, accounts, or storage behind a “local-only” interface. Downloaded profiles may contain category values from the original data; make that visible.

## Chronological procedure

1. Read current repository guidance and the user's contribution limits. Keep app source, datasets, tests, and deployment metadata outside a skills-only repository contribution. Refresh the default branch before editing and publishing.
2. Define the import contract before building charts. Reject broken quotes, records of unequal width, and inputs exceeding the declared limits. Preserve the last valid dataset on failure. Identify errors by logical record number when embedded newlines make physical line numbers ambiguous.
3. Write a state-machine parser. Track quoted fields, escaped double quotes, separators, record boundaries, and text after a closing quote. Support a UTF-8 BOM and CRLF records. Preserve embedded newlines and commas inside quotes. Do not split a whole file on commas or newlines.
4. Detect separators only outside quotes in the first record, and let the user override the guess. Detection is a convenience, not evidence that every later record is valid. Require consistent width after parsing. Avoid a phantom final record for a single trailing newline.
5. Normalize headers transparently. Give empty headers generated names and disambiguate duplicates without dropping columns. Report the number changed. Keep raw cell text available for preview and categorical grouping; do not silently trim every value into a different category.
6. Classify conservatively. Treat only empty or whitespace-only cells as missing unless the user chooses another policy. Preserve zero. Use a strict finite-number grammar, not permissive parseFloat. Currency, percentages, dates, and NA-like labels stay text. Call a column numeric only when every nonmissing value passes the same rule.
7. Compute summaries and distributions. Show row count, column count, missing cells, numeric-column count, distinct values, and selected-column statistics. Exclude missing cells from distributions and denominators deliberately. Use a one-bin display for constant numeric values; otherwise equal-width bins with the maximum explicitly included in the final bin. Guard both overflowing ranges and widths that underflow to zero. For text, show a bounded top-value list with counts and explain exact-match grouping.
8. Build a working data surface. Put import controls beside the dataset overview, column selector, distribution, and scrollable preview. Use textContent or escaped HTML for filenames, headers, cells, labels, and tooltips. A CSV cell is data, never executable markup. Distinguish a synthetic sample from imported data.
9. Handle asynchronous imports. Use a generation counter so a slow file read cannot replace a newer selection or pasted dataset. Surface read failures without erasing the current table. Reset restores the sample and clears import errors. Keep export local, revoke object URLs, and describe the exported content honestly.
10. Test malformed and boundary data before packaging. Run pure-parser and simulated-DOM tests, then real-browser/file-picker/mobile checks when available. A deployment dry-run verifies packaging, not publication or real browser behavior. Publish only to the authorized audience. Extract the reusable decisions and checks into the skill, pull main, review the skill-only diff, and verify the pushed revision.

## Important numerical choices

- Numeric zero is not missing; empty text is not automatically zero
- Reject Infinity and overflowing numeric strings such as `1e309`
- Calculate a mean without unnecessarily overflowing a raw sum, for example by summing each finite value divided by the count, while still checking the final result
- For even-sized medians, `a/2 + b/2` avoids overflow from `a+b`
- Do not draw bins if `max-min` is nonfinite or the chosen bin width becomes zero from floating-point underflow
- Histogram counts must sum to the number of nonmissing numeric values
- A numeric-looking identifier can still be semantically categorical; expose the inferred type rather than claiming to understand its meaning

## Acceptance checks

Use small synthetic fixtures with: BOM and CRLF; quoted commas; escaped quotes; embedded newlines; trailing empty cells; a terminal newline; duplicate/blank headers; zero and empty values; tabs and semicolons; missing columns; unclosed quotes; text after closing quotes; constant numbers; large magnitudes; and subnormal ranges.

Require:

- Valid quoted content survives parsing unchanged
- Broken records fail with a useful message
- Empty import does not replace a valid table
- Duplicate headers remain separate columns
- A zero-valued cell contributes to numeric statistics
- Numeric bin counts reconcile to the input
- HTML-like cell text remains visible text, without creating elements
- An invalid import followed by a valid import clears the error and updates every summary
- Export describes whether it contains original categorical values

The original build passed the parser/numeric fixtures above, histogram conservation, an explicit subnormal-range guard, and JavaScript syntax checks. A jsdom test passed sample loading, numeric-column selection, invalid-import preservation, paste recovery, HTML escaping, missing-value display, and reset. Wrangler static packaging passed its dry-run. Live hosting, real file-picker behavior, mobile visuals, and browser download completion were not yet verified at contribution time.

## Stop or repair

If the requested file exceeds safe in-browser limits, offer an explicitly authorized local batch workflow or a higher-capacity design; do not quietly upload it elsewhere. If types or missing-value rules are ambiguous, preserve the raw values and ask for the interpretation that affects the analysis. If parsing or validation fails, keep the prior result clearly labeled and never present it as the new file's profile.
