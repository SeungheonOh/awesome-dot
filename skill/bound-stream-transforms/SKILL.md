---
name: bound-stream-transforms
description: Process a bounded local byte stream through compression, decompression or a similar transform without publishing partial output after overflow, cancellation or integrity failure. Use when input size does not reliably bound output size; not for extracting arbitrary archive paths or executing restored files.
---

# Bound a streamed file transform

## When to use

Use when a file operation can expand data or fail after already producing chunks. Deliver complete verified output or an explicit failure with partial output discarded. A compressed file's small input size is not a safe output budget.

## Required inputs

- Authorized source bytes and operation/format
- Input, output and elapsed-time limits suitable for the task
- Exact success condition, including integrity or roundtrip checks
- Cancellation ownership and intended local output destination
- Whether the result includes sensitive contents or identifying metadata

Keep format support narrow and explicit. Gzip restoration is not ZIP or tar extraction, and producing bytes is not permission to execute or open them in a sensitive application.

## Workflow

### 1. Define asymmetric limits when the format needs them

Bound input bytes before processing and bound output bytes while reading. Do not trust a declared expanded size or compression ratio as the only limit. A legitimate incompressible input can grow slightly when compressed, so a maximum-size file you compress should still fit the supported restoration input limit.

State whether limits apply to each pass or the entire operation. An elapsed-time guard on an asynchronous stream is not an operating-system CPU or memory sandbox. Native codec buffers, input storage and final output copies also consume memory; a retained-output cap does not bound every internal allocation.

### 2. Read incrementally and count actual bytes

Use a byte-oriented stream API and reject unexpected chunk types. Add each chunk's byte length before retaining it; reject the operation immediately when the cumulative result exceeds the allowed output size. Count bytes rather than decoded string characters.

Keep the output private to the operation until the stream has completed successfully. A decoder may produce apparently useful bytes and only later discover a bad checksum, truncated trailer or forbidden trailing input. Never offer those partial bytes as a successful restore.

Do not allocate the complete declared output size from an untrusted header. When an in-memory result is appropriate, retain bounded chunks and assemble them after success. For larger authorized workflows, use a controlled temporary output and finalize only after verification, with cleanup limited to resources the operation owns.

### 3. Wire cancellation through the whole operation

Associate each operation with an identity or generation. On user cancellation, input replacement or a new operation, cancel the owned reader/transform where supported and invalidate the old result. A late callback must not re-enable a download for obsolete input.

Clear timers and listeners and release the stream reader in a finally path. Treat callback failures as operation failures, not as successful completion. Await or explicitly handle cancellation errors so cleanup does not introduce an unhandled rejection.

Keep the original source unchanged. Cancelling a transform discards its partial output; it does not imply deletion of the user's input file or reversal of any data already transmitted in a different workflow.

### 4. Establish format completion and integrity

Use the codec's documented completion semantics. For the web Compression Streams API, gzip support is a single member; extra members or trailing bytes are errors. Other APIs may support concatenated members, so test the implementation actually used rather than assuming identical behavior across wrappers.

For compression, when the workflow requires a byte-preserving result, decode the produced stream under the same output bounds and compare every decoded byte with the original. This verifies the exercised roundtrip, not cryptographic authenticity or universal compatibility.

For restoration without an original baseline, report the codec's integrity/completion checks and the absence of an independent original-file comparison. A valid gzip checksum does not prove the file is harmless or intended. A SHA-256 digest identifies the resulting bytes; it is not a signature or publisher verification.

Do not hide lossy conversions inside a compression step. Text decoding, newline changes, filename encoding and archive extraction are separate operations with separate contracts.

### 5. Finalize output only for the current input

After all required checks and any digest computation, confirm that the operation is still current and not cancelled. Only then enable saving or atomically finalize the output.

Derive a safe suggested output name without treating a supplied path as authority to overwrite files elsewhere. Keep the format and naming convention explicit. Do not claim that a gzip header's original filename or filesystem metadata was restored when the API exposes only bytes.

Report exact input/output byte counts and the direction of change. Compression can make data larger; an empty input needs a separate ratio label rather than division by zero. A separate inspection report can omit filenames and contents while retaining byte counts, operation, digest and verification method. Such omission reduces disclosure but does not automatically make all reports non-sensitive.

### 6. Exercise failure paths, not only a successful roundtrip

Use original text, empty bytes and non-text binary fixtures. Check:

- A successful roundtrip and compatible decoding through the intended consumer
- Truncated input and a corrupted checksum or trailer
- Additional members/trailing bytes under the selected format policy
- A highly expanding input that exceeds a small test output cap
- Cancellation during progress and a reader that never completes
- Input replacement during file loading or transform completion
- A maximum supported incompressible input, when practical and within the authorized resource budget

Keep the original failure visible. Do not increase the limit, weaken the checksum policy or retry indefinitely merely to obtain output. Explain a legitimate unsupported format separately from a corrupt file.

## Worked example

A local browser-style gzip utility used native CompressionStream/DecompressionStream with a 20 MiB compression-input cap, a 32 MiB restoration-input cap and a 32 MiB output cap. Each streamed pass had its own 10-second elapsed-time guard. The larger restoration cap matters because gzip framing and incompressible data can make the encoded result bigger than the original.

On Node 24.19, a deterministic 20 MiB binary fixture produced 20,977,943 compressed bytes from 20,971,520 input bytes: about 100.0306% of the input size. The result was decoded again and every byte matched. The supported restoration path also accepted this result, avoiding the mistake of rejecting the compressor's own maximum-size output.

Smaller tests covered empty/text/binary inputs, native zlib interoperability, truncated trailers, CRC corruption, concatenated members and trailing bytes. A gzip encoding of 10,000 repeated characters was restored with a 100-byte test cap and failed without returning partial output. Cancelling from a progress callback rejected the operation; a hanging reader hit the deadline and its cancellation hook ran. Simulated UI tests checked that replacing a file or stopping an operation kept stale output unavailable.

These checks covered the local runtime and programmatic UI. They did not establish real-browser download delivery, hard CPU containment or malware safety of restored files. The codec interoperability check used two APIs backed by the same native library, so it was not described as an independent compression-algorithm validation.

## References

- [WHATWG Compression Standard](https://compression.spec.whatwg.org/): byte chunk types, gzip member completion and trailing-input behavior
- [MDN Compression Streams API](https://developer.mozilla.org/en-US/docs/Web/API/Compression_Streams_API): supported browser stream interfaces
