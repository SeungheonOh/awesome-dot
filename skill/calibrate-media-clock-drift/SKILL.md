---
name: calibrate-media-clock-drift
description: "Derive and validate an offset or two-anchor time mapping for existing timed media cues, preserving wording and rejecting unsupported edits."
---

# Calibrate linear media clock drift

## When to use

An existing timed track drifts relative to the same continuous recording and the user supplies trustworthy matching anchor moments. Use a caption-authoring workflow instead when words or boundaries still need transcription.

## Required inputs

- Existing timed cues and the exact source/target media versions
- One offset or two corresponding source/target anchor times with evidence
- Supported interval, output precision and whether the media has cuts or speed changes

## Workflow

1. Confirm that the anchors refer to the same continuous material. Cuts or piecewise speed changes cannot be repaired by one linear map; ask for an edit map or keep those spans unresolved.
2. For two anchors use scale=(targetB−targetA)/(sourceB−sourceA) and offset=targetA−sourceA×scale. Require increasing distinct anchors and check that both equations reproduce their supplied target times.
3. Apply the mapping to cue starts and ends using full precision, then round once at serialization. Scaling changes durations. Preserve cue order and text, and retain original/mapped times separately.
4. Reject negative, reversed, collapsed or out-of-range mapped cues rather than clamping them while keeping all their words. Flag overlaps and unverified extrapolation outside the anchor interval.
5. Serialize a new supported-format copy and reparse it. Report numeric alignment separately from actual listening/render review; two exact anchors do not prove every spoken word is synchronized.

## Output

The mapping coefficients, anchor evidence, retimed copy and cue exceptions, with originals unchanged and media-review limits explicit.

## Verification and limits

Check both anchors, offset-only scale 1, millisecond rounding, unchanged text and interval validity. Do not invent word timing or split text across cuts without evidence.
