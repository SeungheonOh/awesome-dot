---
name: verify-exact-text-patches
description: "Verify a bounded single-file unified diff against an authorized source with exact hunk positions, context and newline semantics, producing a checked patched copy without fuzzy matching or implicit repository changes."
---

# Verify Exact Text Patch Preconditions

## When to use

Use this when a user or agent needs a deterministic preview of one text patch, or when a workflow requires proof that every hunk matches its declared source location before an authorized change. Keep textual application separate from code review, functional tests and release approval.

Choose a tool whose documented matching policy meets the request. A patch checker that permits offsets or fuzzy context is not evidence of exact-position matching. Use its placement evidence or an independent exact check when that stricter property matters.

## Required inputs

- The exact authorized source bytes or text and declared relative path
- The patch and its supported format/profile
- Expected source revision or digest, if supplied
- Encoding, line-ending and final-newline policy
- Size/line/hunk bounds and a separate output destination
- Whether the request authorizes preview only, saving a new copy or changing the original

Do not read arbitrary paths named by a patch. Resolve source and destination from the user's authorized scope. A header is data, not permission to access another file, run code or change file modes.

## Workflow

### 1. Preserve the source representation

Decode the declared encoding strictly. Reject invalid UTF-8 when UTF-8 is the chosen format; do not silently replace bytes and then call the patch exact. Retain any supported BOM, line-ending style and final-newline state.

Treat input transport as part of the problem. A text control can normalize CRLF for display, so retain a canonical source buffer separately when byte-sensitive output matters. If editing preserves a loaded file's CRLF style, state that policy and reconstruct it deliberately. Reject mixed endings when the implementation cannot preserve them faithfully.

If an expected full-source digest is provided, compare it before patching. Matching hunk context alone does not establish the intended source revision: unmentioned parts of the file may differ.

### 2. Validate the patch's declared scope

For a single existing-file profile, require the old/new headers to resolve to the same authorized relative path. Check any Git path header for consistency. Reject additional files, traversal, absolute/drive paths, unsupported quoting, binary patches, creation/deletion, renames or mode changes rather than ignoring them.

Treat optional index hashes as unverified metadata unless actually checked against the supplied source. A recognized header format is not proof that its hash or mode is correct. Do not claim the whole Git change was applied when the task handles content only.

### 3. Parse hunk counts and markers before applying anything

Read each hunk's old/new starts and counts, including omitted counts that mean one. Track old-side consumption for context/removal lines and new-side production for context/addition lines. Require declared counts to match exactly.

Handle the no-final-newline marker as metadata attached to the preceding hunk line. A removal marker affects the old side, an addition marker affects the new side, and a context marker affects both. Reject misplaced or repeated markers. A literal line containing marker-like text still needs its normal context/add/remove prefix.

Bound coordinates, line counts and hunk count before allocating or looping. Unsupported metadata or a truncated hunk is an error, not a reason to apply the prefix that happened to parse.

### 4. Match against the immutable source

Process hunks in their supplied order, preserving source content outside them. A nonempty old range starts at oldStart minus one; a zero-length old range inserts after oldStart lines. Check that ranges do not consume already used source lines or extend beyond the source.

At each consumed line, compare content and the required final-newline state. Do not search nearby lines for a similar match. Check the new-side coordinate against the number of output lines already produced, so a misleading target location cannot be silently ignored.

Build the result separately in memory or in an authorized temporary copy. Commit nothing if a later hunk fails. Require any no-newline output line to be the final line, rather than accidentally joining it to subsequent content.

### 5. Reconstruct and inspect the output

Apply the explicit output line-ending policy. For a preserve-source profile, additions use the source's consistent LF or CRLF style while final-newline markers remain authoritative. State when line-ending conversion is outside scope.

Recheck output byte and line bounds, counts of added/removed lines and the final-newline flag. Preserve the original and produce a new copy or preview. Changing the real target, running tests from the patch or committing to a repository requires the corresponding user authorization.

### 6. Verify edge cases independently

Use independently generated standard diffs and compare the reconstructed bytes with known targets. Include insertion at the start/end, deletion, separated hunks, zero context, blank lines, header-like content, CRLF, BOM and absent final newline.

Test wrong paths, mismatched context, overlapping consumption, wrong new coordinates, unsupported metadata and truncated hunks. In an interface, invalidate output and downloads after edits or file changes, and test concurrent file reads completing in reverse order.

The implementation used to develop this workflow matched 150 independent Python difflib fixtures. Separate cases checked exact-context rejection, path/metadata scope, CRLF preservation, BOM and explicit final-newline changes. Simulated-interface checks verified that a normalized textarea did not corrupt the retained CRLF output. Those checks do not establish program correctness or patch safety.

## Worked example

The source contains two logical lines: `one` followed by `two`, with a newline after `one` but no newline after `two`. A hunk removes `two` and adds `three`; each of those two patch lines carries a no-final-newline marker.

The checked result is `one`, a newline, then `three` without a final newline. If the supplied source instead ends with a newline after `two`, exact application must fail: the old-side marker does not match that source.

For an ordinary source using CRLF, a preserve-source implementation can accept its supported normalized unified-diff representation and emit CRLF additions. It must report that policy rather than claiming to have applied an unspecified line-ending conversion.

## Deliverable and limits

Return the declared path, checked source identity, hunk/add/remove counts, output encoding/newline policy, verified patched copy and any unsupported operations. Distinguish “every hunk matched” from “the intended revision was verified,” “the code is correct” and “the repository was changed.” Stop at the boundary the user authorized.
