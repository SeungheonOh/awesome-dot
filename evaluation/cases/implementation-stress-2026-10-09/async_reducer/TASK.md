> Public contract projection. Behavior and mathematical requirements are unchanged. Delivery/evaluation process instructions, where present, are omitted. See provenance.json for source hashes and changes. This package is UNRUN.

# Implement an ownership-safe asynchronous comparison reducer

This is an original fictional, offline engineering task. Implement `replay(events)` in `solution.py`, using Python 3.11+ standard library only. Return one detached JSON-compatible public snapshot after each event. This is an implementation task: a table of predicted outcomes, hard-coded answers to examples, or prose alone is insufficient. The evaluator calls your function with other valid event lists. Internal design is unrestricted.

The function has no I/O, clocks, threads, asynchronous execution, imports with side effects, or persistent process state. Events simulate completion orders deterministically. Every call starts afresh. Do not mutate input events. Snapshots must not share mutable descendants with inputs or one another. Return `[]` for an empty event list.

## Public state

Each snapshot has exactly `left`, `right`, `comparison`, and `export`.

Each field (`left` or `right`) has exactly:
- `revision`: nonnegative integer, initially 0
- `value`: string or null, initially null; empty string is a valid loaded value
- `active`: request ID or null, initially null
- `loading`: boolean, initially false
- `error`: error string or null, initially null

`comparison` has exactly:
- `generation`: nonnegative integer, initially 0
- `active`: request ID or null, initially null
- `loading`: boolean, initially false
- `result`: null, or `{left: captured string, right: captured string, items: [{id: string, value: string}, ...]}`
- `error`: error string or null, initially null
- `selected`: item ID or null, initially null

`export` is initially null. When an item is selected from a current successful comparison it is exactly `{left: result.left, right: result.right, item: {id, value}}` for that selected item. It must describe the displayed successful result, including the selected item's payload. It never uses subsequently edited fields or an older successful result.

## Field events

`field` is always `left` or `right`.

- `{type: "edit", field, value}`: increment only that field's revision, replace its value, clear its active/loading/error, and invalidate the comparison. This happens even when the string equals the previous value. It supersedes that field's request but does not touch the other field.
- `{type: "load", field, request}`: increment only that field's revision, clear its value/error, make this request active and loading, and invalidate the comparison. It supersedes that field's previous request only.
- `{type: "field_success", field, request, value}`: if this request is active and has not already settled, accept its value, clear error, and settle it. Keep active/loading until its `field_finally`. Otherwise do nothing.
- `{type: "field_error", field, request, error}`: if active and not already settled, clear value, store error, and settle it. Keep active/loading until its `field_finally`. Otherwise do nothing. First terminal event wins, including duplicates or conflicting terminal deliveries.
- `{type: "field_finally", field, request}`: only if the request is still active, clear active and loading. Retain current value/error. Finally closes the request even if no terminal event arrived; all its later terminals are ignored. An obsolete finally must not alter any field or comparison.
- `{type: "cancel_field", field}`: increment that field's revision; clear value, active, loading and error; invalidate the comparison. This also applies when no request is active. It does not cancel the other field.
- `{type: "example", left, right}`: increment both field revisions, set their supplied strings, clear both active/loading/error, and invalidate the comparison exactly once.

An invalidation increments comparison.generation exactly once and clears comparison active/loading/result/error/selected and export. Field success/error/finally do not themselves invalidate; their preceding accepted load already did. Invalidation does not reset field revisions or comparison generation.

## Comparison and selection events

- `{type: "compare", request}`: accept only if both fields have non-null values and neither is loading. If ineligible, this is a complete no-op (including counters). If accepted, increment comparison.generation, clear old result/error/selection/export, make the request active/loading, and capture both field values and revisions. A newer accepted compare supersedes the old compare. Field reads are independent, but comparison is one result owned by this one request and both captured revisions.
- `{type: "compare_success", request, items}`: accept only for the current active, unsettled request whose captured field revisions still match. Store the captured strings and supplied items, clear error, and settle the request. Keep active/loading until its finally. Selection and export remain null until a select event.
- `{type: "compare_error", request, error}`: under the same acceptance rule, keep result/selected/export null, store error, and settle the request. First terminal event wins. Ignore every obsolete terminal.
- `{type: "compare_finally", request}`: only for the active request, clear active/loading while retaining current result/error/selection/export. It also closes a request that has not settled. Ignore obsolete cleanup.
- `{type: "cancel_compare"}`: invalidate the comparison exactly once, even if no request is active. Leave fields unchanged.
- `{type: "select", item}`: null clears selection/export. A non-null ID selects that exact item only if comparison.result currently contains it; export is derived as above. An absent ID is a complete no-op, including when a different item was already selected. Empty result lists are successful results with no selectable item. A new comparison must clear selection even when its new items reuse an old item ID.

## Input and output bounds

Inputs are ordinary JSON trees with unique object keys and the exact described event fields and types. Strings are Unicode, including empty values, combining characters and astral characters. IDs and errors are nonempty strings; payload values may be empty. Each accepted or rejected `load`/`compare` start has a distinct request ID within its request namespace (left, right, comparison); the same ID may occur in different namespaces. Completions may name an ID never started. Item IDs within one successful payload are distinct. There are at most 250 events per trace and 20 items per result, with strings at most 200 characters. Invalid input shape handling is out of scope. No hidden syntax validation requirements exist.

All observable behavior above is required. Public smoke inputs are illustrative and do not enumerate the tested interleavings. Checks include independent fields; edits without replacement; cancellation/examples; old success/error/finally; duplicate/conflicting current terminals; early finally; compare admission; selected export consistency; composed races; purity and repeatability. All legitimate implementations with the same behavior are accepted, regardless of coding style or guide terminology.

