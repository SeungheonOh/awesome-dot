---
name: local-json-change-inspector
description: Build a browser-local JSON comparison tool that distinguishes missing values from null, generates ordered JSON Patch operations, rejects ambiguous inputs, and verifies patch roundtrips.
---

# Local JSON change inspector

Build a tool that compares parsed structure rather than formatting and produces a reviewable patch without applying it anywhere. The worked product, Change Atlas, accepts two JSON documents, lists additions/removals/replacements, filters by path, and downloads a JSON Patch.

## Inputs and limits

Define the comparison semantics, size/depth/value limits, numeric precision policy, array identity policy, and delivery audience. The example compares objects without regard to key order and arrays by position. It does not infer entity IDs or generate move operations. Missing and null remain distinct.

Keep documents client-side when the UI promises local processing. Do not add telemetry, remote validation, storage, or automatic patch execution. A downloaded patch can contain sensitive changed values, so explain its contents. Keep product source, fixtures, tests, and deployment files outside a skills-only repository contribution; read current guidance and refresh main before editing and pushing.

## Chronological workflow

1. **Define ambiguity handling before diffing.** Native JSON.parse discards duplicate object members and can lose numeric precision. Either disclose those semantics or reject inputs that would hide important distinctions. This build rejects duplicate keys, nonfinite results, and unsafe large integers; it explicitly describes floating-point decimal limitations.
2. **Bound parsing work.** Check byte length before processing, then enforce a nesting and value-count limit during a strict parser walk. Accept only JSON whitespace and grammar. Preserve escaped strings and distinguish arrays, objects, null, booleans, strings, and numbers. Create object properties safely so keys such as `__proto__` remain ordinary data.
3. **Implement a pure structural comparison.** Equal primitives produce no operation. Type changes replace the whole value at that path. Compare common object keys recursively; separately record missing and added keys. Sort keys for deterministic output without pretending order is meaningful.
4. **Handle arrays deliberately.** For positional comparison, recurse over the shared prefix, remove surplus old tail entries in descending index order, then append new tail entries. Array removals shift later indices; ascending tail removals can produce an invalid patch. Reordering may appear as replacements and need not be a minimal edit script.
5. **Encode paths correctly.** JSON Pointer escapes `~` as `~0` and `/` as `~1`, in that order. The empty path addresses the document root; it is different from `/`, which addresses an empty-string member. Keep the actual pointer in exports and use a human label only in the visual display.
6. **Separate review records from exported operations.** A visual record can include before/after values and explicit presence flags. Export only the required JSON Patch operation fields: remove has op/path; add and replace also have value. Do not mistake an absent value for null or emit undefined as JSON data.
7. **Build the working surface.** Use two editors, one compare action, operation counts, path/type filters, and readable before/after values. Escape all user content before HTML rendering. Limit rendered rows and shorten long visual values with an explicit notice, while retaining the full patch for download.
8. **Guard stale results.** Editing or swapping input marks the old comparison stale and disables export. A failed parse preserves that old result only with its stale label. A successful comparison clears errors and reenables export. Empty patches are valid results. Reset/sample loading must update both editors and filters consistently.
9. **Verify transformations, not merely counts.** Apply generated patches in an independent test helper and compare the resulting document with the desired parsed document. Include root replacement, escaped keys, positional array growth/shrinkage, null versus missing, type changes, and prototype-like keys. Add generated nested pairs for broader coverage.
10. **Package and publish within scope.** A static app can run without backend services. Validate the selected host's packaging and preserve private audiences. Do not claim publication from a dry-run. Extract the chronological procedure, numerical/structural choices, and tested limits into the skill, then refresh main, review the skill-only diff, push without overwriting concurrent work, and verify the remote revision.

## Acceptance criteria

- Reordering object members alone produces no changes
- `[1,2,3]` to `[4]` yields a patch that can be applied without index errors
- Root null-to-object changes use the empty pointer
- Keys containing slash, tilde, or an empty string remain addressable
- Added null differs from an absent property
- Duplicate keys, unsafe large integers, trailing content, and broken grammar produce useful errors
- Prototype-like keys do not alter application prototypes
- Independent patch application exactly reconstructs the desired parsed value
- Input edits and parse failures prevent exporting an outdated patch
- HTML-like keys and values create no HTML elements
- Large result sets have bounded visual rendering and a complete export

The original build passed 250 generated patch roundtrips plus targeted root/type, array-index, escaped-path, key-order, duplicate-key, numeric, and prototype-safety cases. Simulated-DOM tests passed filtering, stale-export guards, error recovery, equal-document display, escaping, side swapping, and a 200-row rendering cap. Syntax and Wrangler static packaging dry-run passed. Live hosting, real-browser/mobile layout, and download completion were not yet verified at contribution time.

## Sources and model boundaries

- [RFC 6902: JSON Patch](https://www.rfc-editor.org/rfc/rfc6902.html)
- [RFC 6901: JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html)

This tool compares parsed JavaScript values, not exact source text or arbitrary-precision decimals. It produces add/remove/replace operations, not a globally minimal patch. If exact decimal or entity-aware array semantics are required, establish those rules and test them separately before presenting the result as equivalent.

Stop before applying patches to real systems unless that action and target are independently authorized. A comparison request grants inspection and artifact creation, not modification of the compared service.
