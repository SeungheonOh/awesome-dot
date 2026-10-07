---
name: inspect-abi-payloads
description: "Inspect supplied ABI argument bytes under an explicit type schema, preserving exact values and offset origins while separating canonical encoding from function identity and execution acceptance."
---

# Inspect an ABI payload

Use for a bounded read-only explanation of calldata or return bytes. This is not bytecode disassembly, transaction simulation, a wallet action or a safety verdict.

## Establish the decoding contract

Obtain the exact bytes, ordered types and whether a four-byte selector is present. Record the source of the schema. ABI bytes are not self-describing: a plausible decode, even a canonical one, does not prove the supplied types are correct. Do not infer a function identity from a short selector without separate evidence, and do not associate arbitrary bytes with a deployed contract.

Choose and disclose the supported type subset and resource limits. Reject unsupported tuples, arrays or encodings before applying simplified layout assumptions. Each argument occupies one head word only in an appropriately restricted subset; static tuples and fixed arrays can occupy several words. Packed encodings and indexed dynamic event values need different treatment.

Use the current [Solidity ABI specification](https://docs.soliditylang.org/en/latest/abi-spec.html) for the selected layout. Normalize only declared transport syntax, such as an optional hex prefix. Require complete byte pairs. Reject oversized input instead of silently clipping a pasted schema or byte string.

## Decode with explicit origins and bounds

Keep selector bytes separate from the argument payload. Track every head and tail range with its origin and endpoint convention. At nested levels, use the enclosing tuple or array's specified offset base rather than blindly reusing the outer calldata start.

Read large lengths and offsets as exact integers, compare with supported and available bounds, then convert to a machine-sized index. Check arithmetic before allocation. Validate integer width/sign extension, Boolean representation, fixed-byte alignment, padding and the selected string-decoding policy. Treat string lengths as byte lengths, not character counts. Preserve exact Unicode and a leading BOM when the byte contract calls for it; do not normalize a record to make it look familiar.

Return integers in an exact representation. Do not apply token decimals, currency units, ownership meaning or address identity based on a field's apparent shape. Escape invisible formatting controls in human-readable output without changing the decoded value.

## Separate readability, canonicality and behavior

A bounded decoder can recover values from some gapped, aliased, reordered or trailing-byte layouts. Report those separately from malformed or unsupported input. When supported, re-encode the decoded tuple using a canonical encoder and compare the complete byte sequence. Keep the original bytes intact; canonical output is a separate artifact, not an automatic repair.

Apply an output budget too. Several pointers may reference the same large tail, so canonical expansion can exceed the original input size. Preserve useful bounded inspection results while marking canonical export unavailable rather than allocating without a limit or silently dropping arguments. State whether a result came from a byte comparison or a known size mismatch.

A decoder's rejection does not prove that every on-chain decoder would reject the call. A canonical match does not establish the right function, correct contract behavior, authorization or safety. Do not execute or submit anything as a side effect of inspection.

## Verification and deliverable

Compare positive vectors with an independent, version-recorded ABI implementation. Include width boundaries, exact large integers, signed negatives, empty values, multibyte strings, arrays and capacity limits. Separately test corrupted padding, head-pointing/unaligned/out-of-range offsets, huge lengths, aliases, gaps, trailing bytes and unsupported types. Preserve string case when normalizing oracle results; only normalize representations whose type permits it.

Return source/schema assumptions, selector mode, exact typed values, byte ranges, canonicality evidence and unsupported limits. Exports can disclose private call arguments, so keep them local unless sharing is authorized. Editing the source or schema must invalidate a previous result and its exports.

An October 2026 local exercise compared 380 synthetic encoding/decoding vectors with Ethers 6.17.0 and independently rechecked the saved fixtures through that version. It covered all supported integer widths and maximum supported sizes, plus deliberate malformed and non-canonical cases. These checks establish the exercised bounded byte model, not execution or real-contract identity.

If adding a paged byte view, retain the original bytes and exact range origins. Show which declared heads or tails cover each displayed word, including shared coverage, without labeling that coverage account ownership or a vulnerability. A final partial word must show only supplied bytes, not invented padding. Test that concatenating all pages reconstructs the source byte-for-byte and that page navigation never changes the full export.
