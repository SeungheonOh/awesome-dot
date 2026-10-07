---
name: inspect-rlp-encoding
description: "Decode or validate a supplied RLP byte tree with exact prefix and container boundaries, canonicality checks and explicit separation from higher-level Ethereum semantics."
---

# Inspect RLP encoding

Use for a concrete RLP item, a codec check or a byte-range explanation. This is separate from ABI argument decoding, bytecode disassembly and transaction execution.

## Establish framing and meaning

Obtain the exact bytes and whether the caller expects one item or a separately specified envelope/stream. Do not strip a leading byte because the remainder looks plausible. A typed transaction or other wrapper needs its own framing evidence before extracting the RLP body.

Choose explicit byte, node and nesting limits. Clarify whether the result is structural RLP validation or validation against an additional protocol schema. A byte leaf is not automatically an integer, text string, address or account. Empty bytes and an empty list are distinct values. Leading-zero rules for protocol integers must not be imposed on arbitrary byte strings without that schema.

## Decode bounded containers

Follow the [Ethereum RLP definition](https://ethereum.org/developers/docs/data-structures-and-encoding/rlp/) for direct single bytes, short byte/list payloads and long length-prefixed payloads. Treat lengths as exact unsigned values and check them against available bytes and resource limits before converting indices or allocating memory.

Check every child against its containing list's end, not merely the end of the complete input. Record each item's encoded start, payload start and end with a clear inclusive/exclusive convention. Advance by the complete encoded child length; require children to fill their parent exactly. If one item was requested, retain a trailing-byte error instead of silently ignoring the rest.

For strict canonical validation, reject redundant single-byte prefixes, leading-zero length fields and long forms used for short payloads. Re-encode the decoded byte tree and compare the complete original bytes as a further consistency check. State whether a rejection is a format violation or only an implementation resource limit.

## Preserve inspectable evidence

Return a typed byte/list tree, exact byte ranges and the chosen limits. Keep node IDs and paths scoped to that input; edits must invalidate old selections and exports. A paged view should not discard nodes from the full report. A subtree export must include its own original prefix and payload, and should be checked as a standalone item.

Keep optional text previews separate from the byte value. Decode previews strictly, preserve a BOM when present, and escape invisible controls for display. Invalid text encoding does not make an otherwise valid byte leaf invalid. Do not normalize the underlying bytes to improve the preview.

A structurally valid item can still be invalid for its purported transaction or trie schema. Do not infer signatures, ownership, authorization, a chain state or execution success. Exports can expose private bytes; share them only within the user's authorized destination and scope.

## Verify a codec or repair

Use an independent implementation for canonical positive vectors. Include all one-byte values, empty bytes/lists, short/long boundary lengths, nested lists and supported capacity limits. Separately exercise truncated lengths, huge declared lengths, leading-zero lengths, redundant prefixes, parent-boundary crossings, trailing data, depth limits and node limits. Do not let a permissive reference decoder define the strict rejection policy by accident.

In a local October 2026 exercise, 580 synthetic root vectors matched Ethers 6.17.0. All 1,919 extracted subtrees were also independently decoded and re-encoded with that version, while malformed and resource-bound cases were checked separately. This supports the tested bounded byte codec; it is not a transaction-validity or deployment claim.
