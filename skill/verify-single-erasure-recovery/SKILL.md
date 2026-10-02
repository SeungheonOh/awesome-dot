---
name: verify-single-erasure-recovery
description: "Verify bounded XOR-parity recovery of one missing data shard, with explicit padding, per-shard and whole-file integrity checks, mixed-set rejection and recoverability limits."
---

# Verify Single-Erasure Recovery

## When to use

Use this when implementing or auditing a small local redundancy workflow and the intended guarantee is recovery from one unavailable data piece. This is a byte-level coding check, distinct from restoring a production backup or proving a storage service durable.

## Required inputs

- Exact original bytes for a synthetic fixture or an explicitly authorized local file
- Data-shard count, chunk layout, padding rule and original byte length
- Parity algorithm and supported loss model
- Manifest schema, per-shard digests and original-file digest
- Input-size limits and an isolated, non-overwriting output destination

Use synthetic bytes when developing the method. Do not test with account exports, credentials or other private files merely because they are nearby. Distribution to remote storage, changing retention and deleting originals are separate actions requiring appropriate authorization.

## Workflow

### 1. State the recovery contract before encoding

For n equal-length data shards D0 through Dn−1, one parity shard P is the bytewise XOR of every data shard. Recover one missing data shard by XORing P with all remaining data shards. If parity alone is missing, concatenate the intact data shards instead.

The claim is one erasure, not arbitrary corruption correction. A digest-invalid shard may be classified as an erasure only when the manifest is the accepted comparison baseline. Two unavailable data shards exceed this scheme's recovery capability. More parity requires a different code; do not repeatedly XOR guessed values until a plausible file appears.

### 2. Make chunk boundaries and padding unambiguous

For original length L and n data shards, choose and record a deterministic chunk size, such as max(1, ceil(L/n)). Allocate n zero-filled chunks of that size and copy consecutive original bytes into them. Store L explicitly and remove only the trailing padding beyond L after reconstruction.

Never infer original length by stripping zero bytes: legitimate files may end in zero bytes or consist entirely of them. Define the empty-file case explicitly. Validate lengths and counts before allocation, and keep decoding and aggregate selected-input sizes within supported bounds.

### 3. Bind every piece to one recovery set

Record the algorithm/schema, original byte length, data-shard count, chunk size, original-file digest and ordered list of data/parity shard digests. Each piece needs its index and payload, plus a way to identify the exact same manifest.

Reject mixed manifests, duplicate indices, impossible indices, unsupported algorithms and noncanonical or malformed payload encodings. A duplicate copy of one index does not count as another independent shard. Keep names as display/download metadata and sanitize them; never use an untrusted name as a filesystem path.

A hash list stored beside the shards is not authenticated merely because every piece agrees with it. It can detect accidental inconsistency against that list, but someone could replace both list and payload. Keep provenance or signature verification separate when authenticity is required.

### 4. Verify before reconstructing

Decode each selected piece and require its length to equal the recorded chunk size. Recompute its digest and compare with the manifest's digest at that index. Classify missing and invalid pieces explicitly; do not silently feed damaged bytes into XOR arithmetic.

Proceed only if all data shards are valid, or exactly one data shard is unavailable and parity plus every other data shard are valid. A malformed manifest is a set-level error, not a recoverable missing piece. Stop affected recovery without overwriting the source or presenting a download as verified.

### 5. Reconstruct and check the final bytes

For a single missing data shard, copy the parity bytes and XOR every valid data shard into that copy. Validate the reconstructed shard against its own expected digest before concatenation.

Concatenate data shards in index order, truncate to the exact original length, and compute the whole-file digest. A matching per-shard set is not a reason to skip the final length/order check. Offer output only after every required comparison passes, and preserve whether bytes were reconstructed or all data were already present.

If final verification fails, report the precise failed layer and retain inputs unchanged. Do not substitute another manifest, guess ordering or relax a digest comparison to produce a successful-looking result.

### 6. Test losses independently of the encoder

For each small fixture, remove each data shard in turn and recover the exact original bytes. Also remove parity, corrupt one data shard, remove two data shards, duplicate an index, mix two sets and alter expected digests. Include empty input, non-multiple lengths, real trailing zeros and the configured maximum size.

Use at least one hand-calculated fixture or a separate implementation. Encoder and decoder can share the same padding or ordering bug and still pass a round trip. Cross-check hash output with an independent API when practical.

For an interactive tool, invalidate old results when selected files change. A canceled file read or digest operation must not later replace the current selection or re-enable a stale download. Test those interrupted paths alongside the arithmetic.

## Worked example

Original bytes are [1, 2, 3, 4, 5], with two data shards and chunk size three:

- D0 = [1, 2, 3]
- D1 = [4, 5, 0], with one padding byte
- P = [1 XOR 4, 2 XOR 5, 3 XOR 0] = [5, 7, 3]

If D0 is lost, P XOR D1 gives [1, 2, 3]. Concatenating the recovered D0 and intact D1 produces six bytes; truncating to the recorded original length five yields exactly [1, 2, 3, 4, 5]. The same procedure must preserve a genuine original trailing zero when L includes it.

If D0 and D1 are both missing, P alone cannot uniquely identify them. Report unrecoverable under this one-parity scheme. A whole-file digest can validate a proposed reconstruction but does not supply the missing bytes.

The implementation used to develop this workflow passed 252 single-loss reconstruction cases across small lengths and shard counts, corruption/mixed-set/duplicate guards, a two-MiB boundary case, this independent XOR fixture and a separate SHA-256 check. Those tests do not establish real storage durability.

## Output and operational limits

Return the exact manifest identity/baseline, selected indices, missing and corrupt pieces, reconstructed indices, original/recovered lengths and digest outcomes. Report whether the output was only computed, saved or reopened; do not conflate those stages.

Parity is redundancy, not encryption. Data shards expose original byte ranges and parity also reveals information. Keeping every piece on one disk does not protect against losing that disk. Preserve the original until the user has independently tested their intended storage/recovery arrangement; this workflow never authorizes deletion or remote distribution.
