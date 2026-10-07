---
name: verify-merkle-consistency
description: "Verify that two supplied Merkle tree snapshots have an append-only prefix relationship under a declared tree scheme, keeping both root anchors and the scope of the history claim explicit."
---

# Verify consistency between two Merkle snapshots

Use for an older/newer tree-head pair and its consistency proof. Membership of one leaf is a different question. A valid relationship between two roots does not authenticate either publisher, rule out split views shown to other clients, or certify an entire log's operating history.

## Required evidence

Obtain both expected roots and sizes, their provenance, the proof's hash list, and the hash/tree-shape conventions. Establish the ordering from the sizes rather than a timestamp alone. If the expected roots came only from the proof packet, label the check internal consistency; do not silently treat them as independent trusted anchors. Signature verification, key trust and an authorized retrieval of published heads remain separate tasks when needed.

Keep the old and new roles explicit throughout parsing, output and comparison. Bound sizes, proof length and input bytes to the implementation's supported range before converting large numeric fields or allocating memory. Reject unknown schemes and malformed digests instead of trying alternate padding or concatenation conventions until something passes.

## Apply the scheme's verifier

For the history-tree scheme, use [RFC 9162 §2.1.4](https://www.rfc-editor.org/rfc/rfc9162.html#section-2.1.4) with its separate old/new hash accumulators and uneven-tree handling. A single root reconstructed from a membership path is insufficient. Both reconstructed roots and the traversal's completion condition must match.

Handle boundary cases explicitly. The older size cannot exceed the newer size. Equal sizes require equal roots; define whether the accepted representation also requires an empty proof. A zero-size older tree imposes no constraints on earlier records, so do not present that vacuous case as meaningful evidence of preserved contents. Supporting or rejecting it should be explicit. A growing nonempty pair requires a complete proof; reject missing and excess nodes.

Do not replace a failed consistency proof by rebuilding an unrelated tree whose root happens to match one anchor. Reconstructing from a complete authorized record set is useful independent evidence only when it is tied to both intended snapshots and the same encoding rules.

## Report the bounded conclusion

Include scheme, both sizes and roots, provenance, pass/fail or unsupported status, and which checks failed. A path trace can show the old and new accumulators at each step. Label incomplete accumulations as intermediate hashes, not verified roots. Retain the distinction between a well-formed nonmatch and malformed input.

For an interactive checker, bind results and exports to the submitted pair of anchors and proof. Changing an input invalidates the verdict; a late calculation must not overwrite a newer one. Proof hashes can reveal predictable underlying values through guessing, even when the raw records are absent. Keep private evidence local unless sharing is authorized.

## Verification exercise

Generate synthetic sequences and compute their complete prefix roots using an independently structured hash calculation. Verify every supported old/new size pair, especially around powers of two and uneven right edges. Mutate each anchor and path component; remove and append nodes. A rewritten old-prefix record should fail against the preserved old anchor, while a changed newly appended tail with its corresponding new proof can legitimately pass.

A local October 2026 exercise checked all 8,256 positive size pairs through 128 records against independent full-prefix roots, with altered anchors, truncated/excess/changed paths, equal-size pairs, a rewritten prefix and a legitimate new tail. UI tests checked separate anchor entry and stale/cancelled results. These results cover the bounded synthetic implementation, not a deployed log, signed head, publisher identity or global split-view detection.
