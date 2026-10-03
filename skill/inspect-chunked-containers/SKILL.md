---
name: inspect-chunked-containers
description: Inspect a supplied chunk-based binary file with bounded offsets, checksum evidence and clearly separated structural versus decoding results. Use for format diagnostics and parser tooling, not an authenticity claim or a complete security verdict.
---

# Inspect chunked containers

## When to use

Use when a binary file is organized as length-delimited records and someone needs to understand its structure, corruption symptoms or supported decoding subset. Produce an exact ledger first; a successful visual preview alone can hide malformed structure or ignored trailing data.

## Required inputs

- Authorized file bytes and the intended format/version
- Framing rules, byte order, checksum coverage and required record ordering
- Supported decoding subset and maximum input/output work
- Whether output may include original payloads, metadata or only structural evidence

Do not trust the filename or MIME label to establish the format. Choose a documented signature and grammar before interpreting the bytes.

## Workflow

### 1. Establish bounds before reading records

Limit input bytes and record count. Verify the signature, then maintain an integer offset into a byte view that respects both its backing-buffer offset and its actual length. Before reading a record header, check that the minimum framing fits. After reading a declared payload length, compare it to remaining bytes minus framing before taking a slice or advancing.

Record offset, type and payload length. Do not silently truncate a record to available data, skip a bad signature or search forward for a plausible replacement header. An incomplete header and an unsupported record are different findings.

### 2. Check precisely defined checksum coverage

Compute the format's stated checksum over the exact covered bytes and compare unsigned values. Preserve stored and calculated values in the ledger. For PNG, the chunk CRC covers the four-byte type and payload, excluding the length field; the empty IEND payload still has a CRC over its type.

Verify the checksum implementation with a known vector or another implementation. A checksum match is evidence about byte consistency, not authorship, trusted origin or safety. A checksum mismatch should block dependent decoding under a strict inspector while leaving safely parsed structural evidence available.

### 3. Track ordering as explicit state

Model required first/last records, required presence, prohibited duplicates and sequences that must remain consecutive. Do not rely solely on finding a required type somewhere in the file. Distinguish an end marker from end of the physical input and report trailing bytes.

Unknown critical records can prevent interpretation; unknown optional records can remain opaque when the format permits that. Validate type-name reserved bits where defined. Maintain a written list of checks implemented, and label the result as selected checks unless the full conformance rules are actually covered.

### 4. Separate inspection from optional decoding

Classify unsupported features before allocating large output buffers. For an image, validate dimension arithmetic, bit depth, color mode, interlacing and additional transparency/animation features relevant to the chosen decoder. A structurally inspectable file may have an unsupported preview without being malformed.

Preserve a useful chunk ledger when decompression or reconstruction fails. Keep the decoding error beside that evidence instead of erasing it or relabeling all structural checks as failures. Do not display a silently incomplete animation or ignore a transparency rule while claiming a faithful rendering.

### 5. Bound expansion and reconstruct deterministically

When output size is derivable, use that exact expectation as an expansion bound and require equality at completion. Read compressed output incrementally, cancel when it exceeds the bound, and impose a compute deadline in a stoppable worker. Bound dimensions and total samples independently of compressed input size. These controls are application safeguards, not proof of an OS-enforced memory limit.

For PNG row filters, use bytes per pixel rather than image width for the left-neighbor distance. Reconstruct row order, preserve the previous row, apply the specified tie-breaking predictor and wrap additions modulo 256. Keep sample reconstruction separate from gamma/color-profile rendering.

### 6. Test and export the right evidence

Test truncation at framing boundaries, impossible lengths, bad checksums, duplicate headers, nonconsecutive data records, trailing bytes, unsupported features and compressed output both shorter and longer than expected. Use an independently produced small file with known raw output, plus forward/reverse transform comparisons that cover every supported mode.

For interactive tools, test canceling a pending file read, replacing a file during computation and receiving a late worker reply. Invalidate stale results before accepting the new input. Exports should honor the agreed scope: filenames, metadata values and payload bytes may be private even when the structural ledger is safe to share. Structural sizes and checksums can still identify a file, so do not call the export anonymous.

## Worked example

A PNG has a valid signature, a 13-byte IHDR, two consecutive IDAT chunks and an empty IEND. Its header declares 2×2, 8-bit RGBA without interlacing. Each row requires one filter byte plus eight sample bytes, so the complete inflated stream must contain exactly 18 bytes.

Concatenate the two IDAT payloads as one zlib stream, rather than inflating each independently. If the stream produces 19 bytes, stop with an expansion/size error; if it produces 17, report a short decode. If it produces 18, reconstruct each row using its filter byte and a four-byte left-neighbor distance. Preserve the ledger in all three cases. CRC agreement does not override an invalid inflated length.

A 16-bit or interlaced file can instead receive a structural report with preview explicitly unavailable. Do not coerce it into the 8-bit non-interlaced path.

## Reference and evidence

The PNG application used a Pillow-generated synthetic fixture with an independently recorded raw-pixel hash, a known CRC vector, 140 filter/color roundtrips and worker-level failure tests. Consult the [W3C PNG specification](https://www.w3.org/TR/png-3/) for exact format rules. Codec roundtrips sharing the same underlying library are not independent codec validation.
