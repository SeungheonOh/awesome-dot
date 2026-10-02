---
name: check-opaque-color-contrast
description: "Evaluate supplied opaque foreground/background pairs against a declared text contrast threshold and return verified alternatives when requested."
---

# Check opaque color contrast

## When to use

A design review needs numeric contrast evidence for specific color pairs, not a claim that an entire product is accessible.

## Required inputs

- Foreground/background pairs and supported color notation
- Text size/weight or the explicitly chosen threshold
- Whether changing the foreground, background or both is permitted

## Workflow

1. Normalize accepted opaque sRGB colors. Do not silently treat alpha, images or gradients as flat backgrounds. Establish the applicable threshold from current accessibility guidance and the actual text assumptions.
2. Linearize sRGB channels using the 0.04045 breakpoint and 2.4 exponent; compute relative luminance with 0.2126/0.7152/0.0722 weights. Calculate (lighter+0.05)/(darker+0.05).
3. Compare the unrounded ratio with the threshold. A displayed 4.50 can still be below 4.5. Label both the result and text assumptions.
4. If repairs are requested, search a declared candidate family under the permitted changes. Recompute after quantizing to actual output hex values. A sampled RGB ray is not the globally nearest perceptual color.
5. Return an impossible foreground-only result when no allowed candidate passes; do not lower the threshold or change the background without permission.

### Record the rendered-use assumptions

Collect the actual foreground/background pair for each relevant state, not only the default brand colors. Opaque-pair arithmetic cannot establish contrast over a changing image, gradient or translucent layer. Obtain the composited color or flag that case as outside the calculation.

Keep a result row with normalized colors, full-precision ratio, selected threshold, size/weight assumption and decision. Suggestions must respect the allowed component to change. If the background is fixed, report that constraint beside the candidate rather than quietly choosing a different pair.

## Output

A pair-by-pair ratio, threshold decision and assumptions, plus permitted verified alternatives. Other page states and accessibility requirements remain separate.

## Verification and limits

Check black/white 21:1, identical 1:1, swap symmetry and near-threshold values. Verify every suggested final hex pair independently.

## References

[W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

## Stop and ask

Do not infer text size/weight from a screenshot without enough evidence for the required classification. Ask which component may change if every permitted foreground candidate fails against the fixed background.

## Worked example

The supplied pair is foreground #777777 on background #FFFFFF, for normal text under a 4.5:1 target. Its ratio is approximately 4.4781:1, so it fails despite rounding close to 4.5. A proposed foreground #767676 against the same white background has approximately 4.5422:1 and passes that pairwise threshold.

The output keeps the original result and labels the replacement as one passing candidate, not the nearest perceptual match. If the supplied text is actually large under the applicable standard, its threshold may differ; that is a separate evidenced assumption.

Neither result certifies keyboard accessibility, focus-state visibility or the whole page’s conformance. Alpha and image-backed cases remain unresolved until their rendered background is known.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
