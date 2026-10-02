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

### Keep comparison and application scopes separate

Freeze the exact before/after identities and the parsing policy. If exact decimal identity matters, use an appropriate representation rather than accepting binary-float equivalence. Preserve values containing prototype-like keys as ordinary data, and bound both parsing and generated-patch size.

Present path, change kind, presence and permitted before/after detail in the review. Export operations in their application order. If a new edit changes either input, invalidate the old patch until comparison and round-trip verification are repeated. Verification against a local copy does not authorize deployment.

## Output

A scoped diff, patch artifact, exact comparison semantics and round-trip verification result.

## Verification and limits

Check root replacement, null versus absent, escaped/empty keys, array shrinkage, type changes, unsafe numbers and prototype-like keys.

## References

[JSON Patch](https://www.rfc-editor.org/rfc/rfc6902.html) · [JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html)

## Stop and ask

Ask which document is authoritative if old/new ordering is unclear. Hold exact-value conclusions when parsing would lose required precision. Report duplicate members rather than accepting whichever value a permissive parser retained.

## Worked example

Before is {"a/b":[1, 2, 3],"keep":null}; after is {"a/b":[4],"new":null}. A valid ordered patch replaces /a~1 b/0 with 4, removes /a~1 b/2, removes /a~1 b/1, removes /keep, and adds /new with value null.

The slash in the member name becomes ~1. Array tail removals run in descending order so removing index 1 does not invalidate a later request to remove index 2. The new null member is an addition, not the absence of a value.

Apply these operations to a local copy of before and compare with after. The report identifies positional-array semantics and makes no minimal-edit-script claim. Nothing is applied to a live service.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
