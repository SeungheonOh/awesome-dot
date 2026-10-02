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

## Output

A pair-by-pair ratio, threshold decision and assumptions, plus permitted verified alternatives. Other page states and accessibility requirements remain separate.

## Verification and limits

Check black/white 21:1, identical 1:1, swap symmetry and near-threshold values. Verify every suggested final hex pair independently.

## References

[W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)
