---
name: opaque-color-contrast-workbench
description: Build a local sRGB text/background contrast tool with exact WCAG threshold decisions, a palette matrix, and clearly bounded foreground-color suggestions.
---

# Opaque Color Contrast Workbench

Create a design utility for checking a specific opaque foreground/background pair. A passing pair is not a claim that a page or product conforms to WCAG. Keep the generated app and its tests outside this skills contribution.

## Inputs and boundaries

Accept #RGB and #RRGGBB only, normalize case, and reject alpha, CSS expressions, and named colors. Choose a small synthetic palette for examples; use private brand palettes only within the user's approved destination. A dependency-free static app can do all calculations locally without transmitting color inputs.

## Chronological build approach

1. Implement normalization and numeric calculations as a pure module. Expand three-digit hex, parse the three integer channels, and keep the original normalized colors for export. Do not use CSS parsing as an implicit acceptance policy.
2. Implement sRGB relative luminance from the current [W3C contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Divide each channel by 255; use the linear branch through 0.04045 and the 2.4 power branch above it. Combine linearized channels with 0.2126, 0.7152, and 0.0722 weights. The contrast ratio is (lighter luminance + 0.05) divided by (darker luminance + 0.05).
3. Keep numeric display formatting separate from threshold decisions. Test the raw ratio against 4.5 for AA normal text, 3 for AA large text, or 7 for AAA normal text. A displayed rounded 4.50 can still fail. Explain large-text assumptions beside the controls and source them; do not infer them from a large heading preview.
4. Add a preview with body copy, headings, numerals, and fine print. Keep the workbench's own controls readable even when the user's pair has poor contrast. Update text and background together only after both inputs validate.
5. Treat unapplied edits as dirty state. Disable export, swap, and suggestion application when they would act on old values. Preserve the last valid preview with an explicit stale-state indicator. Invalid entry must not partially update just one color.
6. For a practical suggestion, search a declared family of candidates rather than claiming a global optimum. One transparent approach samples 255 steps from the foreground toward black and 255 toward white. Quantize each candidate to its actual hex color, recompute contrast, and retain the first passing candidate on each ray. Choose the smaller RGB-distance candidate, while explaining that RGB distance is not perceptual distance. Never label it the nearest accessible color.
7. Handle an impossible foreground-only target. If neither endpoint can pass against the fixed background, explain that the background or target must change. Do not silently lower the threshold or alter the background.
8. Add a small pair matrix with semantic table headers and keyboard-operable cells. Give every cell the pair, numeric ratio, and textual pass/fail status; color alone is insufficient. Clearly define whether rows or columns represent foregrounds. Selecting a cell should synchronize both text fields and color pickers.
9. Export only validated colors and annotate the selected threshold and computed ratio. Downloading CSS does not mean it has been integrated into a user's site. Do not upload or publish the tool until its intended hosting destination and audience are authorized.

## Verification that changes decisions

- Black/white must equal 21:1; identical colors must equal 1:1. Black and white luminance are zero and one. Red, green, and blue primary luminance equal their weights.
- Ratio is symmetric when swapping a pair. Every valid ratio lies between one and 21.
- Check a value just below a threshold separately from the threshold itself; formatted strings must never decide the result.
- Recompute every suggested hex color independently. A result may pass before quantization and fail afterward if this is implemented incorrectly.
- For a sampled-ray search, verify the immediately preceding step on the selected ray fails. Test already-passing pairs and impossible targets as separate outcomes.
- Exercise invalid short hex, alpha hex, empty text, and unsupported names. Verify no partial application and no enabled stale export.
- Exercise preset recovery, swapping twice, threshold changes while dirty, matrix selection, successful suggestion application, reset, and download initiation.
- Inspect the real preview at narrow and wide widths if browser access permits. Simulated DOM tests establish control behavior only; they do not establish rendered contrast, color accuracy, or screen-reader usability.

## Reference-build observations

Inkbench's pure-model checks covered endpoint values, primary luminance, symmetry, unrounded thresholds, invalid input, and 3,072 foreground/background/target repair cases. A separate simulated-DOM suite covered the 36-cell matrix, pair application, swap, stale-export prevention, invalid-input recovery, presets, possible/impossible repairs, download initiation, and reset. Real-browser visual QA remained unverified at contribution time. Repeat the checks against any new implementation rather than treating this record as certification.

## Output and limits

Deliver the runnable app separately, with source and relevant verification results. Explain that transparency, gradients, images, font rendering, component states, and other accessibility criteria require separate checks. For this repository contribution, include only SKILL.md; keep product files, tests, hosting configuration, and build notes outside the repository.
