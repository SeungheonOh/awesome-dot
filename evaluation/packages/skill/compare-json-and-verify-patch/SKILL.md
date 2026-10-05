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

## Rehearse an existing patch

Use this branch when the input is an ordered patch supplied by a person, service or agent rather than a generated comparison.

1. Freeze the source document, patch, source version or content hash, and number/size limits. Confirm whether the destination supports all six RFC 6902 operations. A local rehearsal cannot establish a remote service's exact numeric representation or extension behavior.
2. Parse the document and patch before mutation. Require a patch array and valid operation-specific members. Reject unsupported operations and malformed pointers; do not silently repair paths or reorder operations. Unknown additional operation members are ignored under RFC 6902.
3. Apply operations sequentially to an isolated deep copy. Resolve every path against the evolving copy, using own object members only. Object keys such as __proto__ are data. Decode ~1 and then ~0; distinguish an empty pointer from a pointer to an empty-string key.
4. Enforce each operation's preconditions. Remove, replace and test require the target to exist; copy and move require the source. Add may replace an object member, but an array index inserts before that element. Array indices are canonical nonnegative integers; a dash is permitted only as the final append target for add.
5. For move, remove the source before resolving the destination's array position. Reject moving a value into its own descendant. Copy must not alias a mutable source. Test compares parsed JSON values with object-key order ignored and array order preserved.
6. Stop at the first failed operation. Report its index and reason without exposing disallowed values. Discard the partial copy and keep the source unchanged. Do not offer a failed partial result as a successful preview.
7. Bound the resulting size and depth after operations as well as before them: repeated copies can amplify a small input. For interactive work, cancel or invalidate results when any input changes, and reject late results from earlier runs.
8. Export the successful result and a minimal operation journal tied to the frozen source. Represent removal of the entire document distinctly from a JSON null value. If the source changes later, rehearse again; a previous preview does not establish that the patch is safe against a newer version.

### Additional worked example: move and atomic failure

Start with {"items":["A","B","C"],"version":7}. Apply a test that /version equals 7, then move from /items/0 to /items/2. Removal first produces ["B","C"], then insertion at index 2 gives ["B","C","A"].

If a subsequent test expects /items/0 to equal "A", it fails because that value is now "B". An atomic local rehearsal reports failure at that third operation and discards the preview; the original document remains {"items":["A","B","C"],"version":7}. It must not export the intermediate moved array as the final answer.

Changing the failed test to expect "B" yields a successful preview. This example illustrates ordered semantics and rollback of a local copy, not permission to send the patch to a repository or API.

## Output

A scoped diff, patch artifact, exact comparison semantics and round-trip verification result.

## Verification and limits

Check root replacement/removal, null versus absent, escaped/empty keys, array shrinkage, type changes, unsafe numbers and prototype-like keys. For supplied patches, cover all six operations, same-array moves, descendant rejection, missing parents, leading-zero indices, append bounds, copy independence, failed-test rollback and size amplification. Use an independent applicator or oracle for generated-patch round trips; testing an implementation against itself is weaker evidence.

## References

[JSON Patch](https://www.rfc-editor.org/rfc/rfc6902.html) · [JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901.html)

## Stop and ask

Ask which document is authoritative if old/new ordering is unclear. Hold exact-value conclusions when parsing would lose required precision. Report duplicate members rather than accepting whichever value a permissive parser retained.

## Worked example

Before is {"a/b":[1, 2, 3],"keep":null}; after is {"a/b":[4],"new":null}. A valid ordered patch replaces /a~1b/0 with 4, removes /a~1b/2, removes /a~1b/1, removes /keep, and adds /new with value null.

The slash in the member name becomes ~1. Array tail removals run in descending order so removing index 1 does not invalidate a later request to remove index 2. The new null member is an addition, not the absence of a value.

Apply these operations to a local copy of before and compare with after. The report identifies positional-array semantics and makes no minimal-edit-script claim. Nothing is applied to a live service.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
