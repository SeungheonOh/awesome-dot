---
name: verify-merkle-inclusion
description: "Check a supplied Merkle inclusion proof against an independently established root, tree size and exact leaf encoding; report the reconstructed path and the limits of the membership claim."
---

# Verify Merkle inclusion

Use for a concrete membership proof or a bounded implementation comparison. This is separate from checking a downloaded file's ordinary checksum, authenticating a signed tree head, proving append-only consistency, or auditing a blockchain.

## Establish the contract before hashing

Obtain the exact leaf bytes, index, tree size, sibling path, hash algorithm, tree-shape convention and expected root. Identify where the expected root and size came from. A root copied out of the same untrusted proof can establish internal consistency but cannot authenticate a publisher. If no independent anchor is available, report that limited result rather than silently promoting the embedded root to trusted status.

Determine whether the input is raw bytes, a prehashed leaf, or a structured record with a specified serialization. Do not add a leaf prefix twice, hash a hex string as text instead of decoding it, trim whitespace or normalize Unicode without the protocol requiring it. Preserve duplicates and ordering. If accepting text records, state the encoding and treatment of malformed Unicode; rejecting unpaired surrogates prevents silent replacement from merging different inputs.

## Follow the selected tree scheme

For the binary history-tree convention in [RFC 9162 §2.1](https://www.rfc-editor.org/rfc/rfc9162.html#section-2.1), use the declared hash with separate leaf and parent prefixes. Uneven trees split at the largest power of two below their size; they do not duplicate the final leaf. The single-record path is empty, while an empty tree has no record inclusion proof.

Use the specification's index/size-based verification procedure, including its right-edge handling. Reject out-of-range indices, malformed digests, excess path nodes and incomplete paths. Reconstruct the root from the supplied leaf and siblings and compare it with the expected anchor. Do not accept a convenient alternate padding rule to make a failing proof pass. A proof for another scheme needs that scheme's own rules.

## Make the result inspectable

Return the exact claim checked: leaf or a separately agreed identifier for its bytes, encoding, index, tree size, scheme, expected root and its provenance, computed root, pass/fail and each sibling's left/right role. Keep malformed input, a validly parsed nonmatch and unavailable verification capability distinguishable.

A successful membership check does not show that the record is true, that it occurs only once, that the publisher is authorized, or that a log has never rewritten history. Those require different evidence. A shared proof exposes the selected record and hash commitments; hashes of predictable records can be guessed. Keep private inputs local unless their disclosure is authorized.

## Verify an implementation

Use fixed hash vectors and an independently structured reference computation. For a recursive tree builder, a full-record streaming stack reduction gives a useful independent root oracle. Exercise all indices around uneven and power-of-two boundaries, not only the leftmost leaf. Mutate leaves, sibling order, sibling bytes, indices, expected sizes and anchors. Check empty and singleton cases, repeated records, byte-distinct Unicode and explicit resource limits.

When verification is asynchronous, bind its output to the exact submitted proof and anchor snapshot. Editing either must invalidate the old verdict. Cancellation may discard output without stopping a hash operation already running; describe that accurately.

### Synthetic example and actual validation

Using UTF-8 records `alpha`, `beta`, `gamma`, SHA-256 and the history-tree scheme above gives root `385da30f3917282c8939dff851957e519ab1846b1351a14c0adb3b11632742aa`. The index-2 proof for `gamma` has one sibling, `983cb57c04cddd52634edab38a7bef85708a974f114bbd9aa9ec5d4ce6656b4b`, on the left. Appending another `gamma` changes the tree and root; padding the original list this way is not the selected convention.

In an October 2026 local implementation check, recursive Web Cryptography roots matched independently structured Node hash/stack roots for sizes 1–128, and all 8,256 inclusion paths passed. Deliberate record, path, anchor, size and encoding mutations were also checked. This is evidence for that bounded synthetic implementation exercise, not an external log's authenticity, certificate validation or a general security certification.

For a visual calculation record, show left/right operand order and preserve full digests in the export even if the on-screen view abbreviates them. Label a partial computation as partial; its final displayed hash is not necessarily the tree root. Bind the diagram and its verdict to the same proof/anchor snapshot as the numerical check, and disable stale exports after edits. A readable diagram helps inspect the calculation but is not an independent cryptographic verifier.
