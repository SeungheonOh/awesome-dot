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

### Bound interpolation and extrapolation

Retain the anchor source, corresponding target moment and the confidence or review method for each. One anchor supports an offset only when the same playback rate is established. Two anchors support a linear mapping under the stated continuous-rate assumption, not arbitrary cuts.

After mapping, report every cue outside the anchor interval as extrapolated. Reconcile cue count and exact wording before and after. If rounding collapses a short interval, hold that cue instead of inventing a minimum duration. Keep overlap flags separate from unsupported timing because overlapping speech can be intentional.

## Output

The mapping coefficients, anchor evidence, retimed copy and cue exceptions, with originals unchanged and media-review limits explicit.

## Verification and limits

Check both anchors, offset-only scale 1, millisecond rounding, unchanged text and interval validity. Do not invent word timing or split text across cuts without evidence.

## Focused follow-up

With a third verified anchor, calculate its residual under the two-anchor mapping. A large residual is evidence against the constant-drift assumption; do not automatically fit a more complex warp without the needed scope and media evidence.

## Worked example

The supplied continuous-track anchors are source 1.000 s→target 2.000 s and source 11.000 s→target 12.200 s. The scale is(12.2−2)/(11−1)=1.02, and the offset is 2−1×1.02=0.98 s.

A cue at source 3.000–5.000 s maps to 4.040–6.080 s. Its duration grows from 2.000 to 2.040 s; the words remain unchanged. Both anchors reproduce exactly before serialization, and the mapped cue lies between them.

A cue at 20 seconds would be extrapolated beyond the supplied anchors and labeled accordingly. If the target media contains a cut at 6 seconds, this single mapping is insufficient: preserve the cue and request an edit map rather than guessing which words survive the cut.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
