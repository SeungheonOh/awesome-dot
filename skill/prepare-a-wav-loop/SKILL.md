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

### Specify the seam before modifying samples

Record the exact selected half-open frame interval and channel count. Convert seconds using the file’s own sample rate, not a requested export rate. If a new sample rate is requested, treat resampling as a separate operation with its own quality and length checks.

Document the overlap weights and ordering of the stitched segment. Apply identical frame positions to every channel. Check peaks before quantization; do not let out-of-range float values become clipped PCM silently. Preserve the source and save to a new destination with no-overwrite handling where available.

## Output

The new loop file, source interval, overlap, gain/encoding changes and numeric/listening verification status.

## Verification and limits

Test mono/stereo, minimum intervals, exact overlap endpoints, out-of-range float samples and quantization. No source overwrite or external upload is implied.

## Hold conditions

Hold export if samples are nonfinite, the overlap exceeds the selected interval, or the requested encoding cannot represent the samples without an unapproved change. Ask whether clipping, scaling or another encoding is acceptable rather than choosing silently.

## Worked example

A supplied synthetic stereo WAV has sample rate 48, 000 Hz. The chosen interval is frames 24, 000 through 120, 000 exclusive, giving 96, 000 frames or 2 seconds. The requested linear seam overlap is 12, 000 frames, and the chosen overlap construction shortens the loop by that amount.

The output therefore has 84, 000 frames, two channels and duration 1.75 seconds. If serialized as 16-bitPCM without extra chunks, the audio payload has 84, 000×2×2 =336, 000 bytes; the total RIFF file also includes headers. This arithmetic is not a claim about audible smoothness.

The handoff records the 0.5–2.5 second source interval, 0.25 second overlap, encoding and any allowed gain change. Independent parsing checks frames/rate/channels; listening remains explicitly unperformed if no playback check occurred.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
