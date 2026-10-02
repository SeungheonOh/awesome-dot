---
name: compare-json-and-verify-patch
description: "Compare two supplied JSON documents structurally and generate a locally verified JSON Patch without applying it to a live system."
---

# Compare JSON and verify a patch

## When to use

The user needs a reviewable structural difference or patch artifact, without changing the service represented by the data.

## Required inputs

- Ordered before/after documents and authorized field scope
- Array identity/ordering rules and numeric precision requirements
- Output limits and fields that should not be repeated in the report

## Workflow

1. Parse strictly with bounded bytes, nesting and value count. Reject duplicate object keys when discarding them would hide a difference. Preserve missing versus null and disclose numeric precision limits.
2. Compare objects by keys and arrays under the agreed policy. For positional arrays, do not infer entity identity or call replacements a minimal move sequence.
3. Encode JSON Pointer correctly: escape tilde before slash; empty path means root, while slash means an empty-string member. Remove surplus array tail entries in descending index order.
4. Generate only required add/remove/replace fields. Keep private values out of a summary when not needed, while disclosing that a complete patch may contain them.
5. Apply the patch to a local copy with an independent applicator and compare the result with the desired parsed value. Preserve originals and do not apply it remotely without separate authorization.

## Output

A scoped diff, patch artifact, exact comparison semantics and round-trip verification result.

## Verification and limits

Check root replacement, null versus absent, escaped/empty keys, array shrinkage, type changes, unsafe numbers and prototype-like keys.

## References

[JSON Patch](https://www.rfc-editor.org/rfc/rfc6902.html) · [JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html)
