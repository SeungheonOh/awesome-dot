---
name: build-spreadsheet-model
description: Build or extend an editable spreadsheet that recalculates useful outputs from clearly defined inputs and assumptions. Use for a reusable planning, comparison, forecasting, or operational model, rather than a one-time analysis or data cleanup alone.
---

# Build a Spreadsheet Model

Deliver a spreadsheet the user can change and keep using. Make the relationships between inputs, calculations, and outputs understandable, and verify the saved model with representative inputs. A static table of computed answers is not a working model when the request calls for editable assumptions and recalculation.

## Define the model's job

Establish what the user wants to compare, plan, or decide; which inputs they will change; and which outputs they need. Reuse supplied definitions, existing workbooks, templates, and conventions. Ask when an unresolved definition changes the model, such as whether a rate applies to the opening balance, average balance, or individual transactions.

Identify the requested spreadsheet application or file format. Inspect the tools actually available before promising a native file, live shared sheet, or automated connection. Preserve the chosen destination and existing workbook structure when those are part of the request.

Separate a known fact, a user-selected assumption, and a calculated result. Keep a missing input visibly unresolved or use a clearly labeled provisional value where the request permits it. Do not make a forecast look complete by silently inventing demand, prices, growth, capacity, or dates.

## Design the relationships before formatting

Sketch the smallest model that answers the question. Define the units, time basis, record or period represented by a row, and the relationships that produce the requested outputs. Decide what must be editable and what should be derived.

Keep inputs, calculations, and outputs distinguishable through labels and layout. Separate worksheets can help a larger model; a small model may work better in one well-labeled table. Do not impose an elaborate workbook architecture on a simple comparison.

Preserve meaningful distinctions:

- Zero is a known value; blank may mean missing, not applicable, or not yet entered
- A total, a rate, and an average need different aggregation rules
- A stock measured at a point in time differs from a flow over a period
- An amount, a quantity, and a percentage should not share an unlabeled unit
- A forecast or scenario is conditional, not an observed result or commitment

Define how incomplete or invalid inputs affect outputs. Prefer a visible unresolved status to a plausible-looking total that silently treats unknowns as zero. Use rounding where the actual business rule requires it; display rounding alone should not accidentally change downstream calculations.

For an existing workbook, inspect formulas, named ranges, tables, validations, protected areas, external references, and relevant macros before editing. Preserve unrelated formulas and features. Do not replace a formula with its cached value or rebuild the workbook in a format that silently loses functionality.

## Build an editable artifact

Use the available spreadsheet capability to create the requested file or update the authorized workbook. Put genuine inputs in labeled cells and calculate dependent values with formulas or the workbook's established mechanism. Avoid hard-coded answers where the user expects inputs to change.

Keep formulas understandable and consistent across comparable rows or periods. Use references that survive the intended operations, such as adding rows or copying a scenario, when those operations belong to the request. Introduce helper calculations when they make the logic easier to audit; avoid a complex formula merely to keep everything in one cell.

Retain identifiers as identifiers, including leading zeros and long digit strings. Keep imported text literal rather than allowing formula-looking content to become executable spreadsheet expressions. Use actual numeric or date values only when the source meaning supports that type.

Make edit locations and required inputs clear through labels or instructions, not color alone. Add validation when it prevents a likely mistake without blocking legitimate use. Format numbers and dates in units the reader can understand, and make incomplete assumptions or excluded scope visible near the affected result.

Use charts when they reveal the decision-relevant pattern; a model does not need a dashboard to be useful. Ensure a chart's source range, scenario, units, and handling of missing values match the model it represents.

## Verify calculations and intended edits

Check the model independently of its own formulas. Calculate a small representative case by another transparent method, reconcile an applicable total, or compare a known result. Choose a check that could reveal a wrong relationship, not merely repeat the same formula in another cell.

Change an important input in a separate verification copy or safely restorable state. Confirm that the right outputs change, unaffected outputs remain sensible, and dependent tables or charts update. Include a meaningful boundary such as zero activity, an empty period, an invalid rate, a missing assumption, or a new row if the workbook is meant to accept one. Do not add every case mechanically.

Inspect formulas for broken references, unintended circular dependencies, shifted ranges, and inconsistent copied logic. An error-free sheet can still calculate the wrong metric; compare the results with the definitions and acceptance behavior.

Recalculate and reopen the saved artifact in an available compatible consumer when possible. Distinguish formulas written to a file from results actually calculated by a spreadsheet engine. A cached result can be stale; a library that stores formulas may not evaluate them. If the requested application is unavailable, report the tested consumer and remaining compatibility limit without claiming its behavior was checked.

Inspect the saved layout at a usable scale. Check visible labels, clipped values, sheet navigation, formula/input distinctions, chart labels, and any requested print or export view. Restore the intended delivery inputs after experiments and verify that the delivered file contains those values.

## Hand over a maintainable model

Deliver the actual workbook or verified sheet link, with a short explanation of what the user changes, what recalculates, and the material assumptions or limits. Put essential usage notes in the workbook when the file needs to make sense on its own. Avoid a long separate manual for an uncomplicated model.

State the meaningful checks performed and any unverified consumer behavior. If missing inputs prevent a trustworthy output, deliver the usable structure with those gaps visible rather than presenting a completed forecast. Ordinary requested workbook creation can proceed within its authorized destination; adding external data connections, sharing with new recipients, or using the model to make transactions is separate work.
