---
name: prepare-a-wav-loop
description: "Trim an authorized PCM/float WAV at exact frame boundaries, optionally crossfade the loop seam, and export a validated new audio file."
---

# Prepare a WAV loop without replacing its source

## When to use

The user needs a bounded loop asset from a supplied recording, with a clear record of timing, overlap and format changes.

## Required inputs

- Authorized WAV, supported encoding/channel/sample-rate limits
- Selected frame or time interval and desired seam overlap
- Output encoding and whether peak scaling is allowed

## Workflow

1. Validate RIFF/WAVE chunk bounds and actual PCM/float format. Convert requested times to frame indices with a declared rounding rule and preserve the original bytes. Reject unsupported encodings rather than guessing.
2. Check a nonempty interval and overlap shorter than the available segment under the chosen construction. State the output length formula; overlap crossfades shorten a loop and are not merely a fade applied in place.
3. Apply the documented seam construction identically across channels. Keep operations frame-aligned, reject nonfinite samples and do not silently resample or normalize.
4. If requested, calculate peak scaling explicitly and record the gain. A seam crossfade does not guarantee perceptual smoothness; comfortable-level listening is a separate authorized check.
5. Serialize a new WAV with valid sizes, channel layout and sample encoding. Reopen using an independent parser and verify sample rate, frames, channels and duration. Do not claim an output was heard if only numeric checks ran.

## Output

The new loop file, source interval, overlap, gain/encoding changes and numeric/listening verification status.

## Verification and limits

Test mono/stereo, minimum intervals, exact overlap endpoints, out-of-range float samples and quantization. No source overwrite or external upload is implied.
