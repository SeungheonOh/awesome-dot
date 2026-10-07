# Public provenance and trust boundaries

This is a new public projection of the reviewed v2 authored routing regression. Its [own allowlist manifest](MANIFEST.json) identifies public bytes independently of the immutable author-source manifest `6c1113a41496cb7bcc3378d8853b185aca997f63c64a89572f4a907cd7dd54e6`. The source freeze remains unchanged.

## Preservation and projections

[The publication map](provenance/publication-map.json) lists every exact copied file and original hash, each projection, and omitted source artifacts with their hashes. Requests, common instruction, interface, schema, eleven source entry points, semantic-review template and all 39 responses are exact copies. The public rubric changes only its top-level review-status string, and the control index changes only each control’s semantic_status string. Every other JSON field is unchanged and bound by a canonical status-excluded content hash. No expected label, allowed route, source anchor or control wording was changed for publication.

Public README/methods/review/control documentation and the verifier are newly written for this package. The [review projection](provenance/review-projections.json) substitutes anonymous A/B labels for internal identifiers and preserves original record hashes, scope, timestamps and conclusions. The [prospective recipe projection](provenance/prospective-inputs.json) records unexecuted candidate ordering and input hashes. It is not an exact historical dispatch claim: no dispatch or trial occurred.

Private retrieval captures, original coordination records, absolute workspace paths and the workspace-dependent build script are omitted. The original source checker and historical mechanical report are also omitted; they depended on private records and historical pending-review metadata. The new standard-library verifier is read-only and checks this public allowlist instead. Original-record hashes are provenance identifiers, not a way to verify undisclosed contents or establish semantic truth.

## Source and linked-reference scope

All eleven full guide files are pinned to [b8fd615](https://github.com/SeungheonOh/dot-skills/tree/b8fd6155afbc87c8c7f237d0e26200644c82847d). [The source manifest](source-manifest.json) records their exact lengths, SHA-256 hashes, Git blobs and immutable URLs; these guide bytes were also verified identical at c0e8d9b. This is a claim about those eleven files, not the entire repository.

Copied guide bytes retain 34 links to omitted examples, scripts, artifacts and context. [The exact omission map](provenance/omitted-links.json) records each copied source/target pair, the original repository path, its verified blob in the pinned source tree, and a direct immutable URL. The original files remain accessible through those URLs but are not included here. The repository document checker exempts only those exact pairs; ordinary tests reject neighboring source paths or targets. No broad directory, filename, extension or template exemption was added.

The router's preserved parent-directory link resolves to this copied eleven-entry-point directory. The candidate collection remains exactly ten entries, excluding the router itself. It does not represent natural discovery, all repository guides or full-catalog no-fit. Do not silently add linked context to a later comparison's input allowlist.

## What can be verified

The [verifier](verify.py) checks the public file allowlist and hashes, preserved-original bindings, source identities, rubric and control-index status-excluded content hashes, line evidence, authored control shapes, review projections' freeze identifiers, all 24 prospective input hashes, and the exact omitted-link mapping. It reads data and prints a report only. Semantic adequacy remains null.

The public manifest omits itself to avoid a self-hash cycle. Use an independently retained manifest digest for an external freeze check. Byte integrity cannot prove that review procedures were followed, replace semantic review, or establish a model result. No measured model results are claimed, and historical evaluation artifacts, scores and workflows remain unchanged.
