---
id: garment-colorway-contact-sheet
title: "Garment Colorway Contact Sheet"
summary: "Compare garment colorways while preserving a review trail for seam, texture, and logo drift."
category: image-editing
level: intermediate
timebox_minutes: 75
capabilities: ["files", "images"]
tags: ["apparel", "colorways", "contact-sheet"]
status: recipe-not-run
---

# Garment Colorway Contact Sheet

Compare garment colorways while preserving a review trail for seam, texture, and logo drift.

## Scenario

You designed a simple jacket and have permission to edit the sample photographs. Before asking a manufacturer about dyes, you want to narrow six possible colors to two. The comparison must distinguish visual exploration from a production specification or a promise about fabric behavior.

## Inputs to prepare

- Authorized front and back sample photographs
- Six color references and the allowed garment panels
- Seams, logos, fasteners, and material texture that need close review
- The intended lighting reference and review audience

## Copy this prompt into dot

```text
dot, prepare a colorway exploration for [GARMENT] from [AUTHORIZED FRONT AND BACK PHOTOS]. Use [SIX COLOR REFERENCES] on [PERMITTED PANELS] only. First inventory the visible seams, fasteners, logos, and fabric texture so we have a checklist for unintended changes. Keep the original photographs separate and do not infer hidden construction from the front view.

If image editing is supported, create a consistent contact sheet with one front and one back candidate for each colorway. Put names and identifiers in the surrounding layout rather than trusting generated lettering inside the photos. Use matching framing and a restrained lighting treatment so the colors can be compared fairly. Identify any drift in stitching, folds, logos, or panel boundaries instead of asserting exact preservation.

Deliver individual candidates, the contact sheet, and an exception log listing uncertain areas. Compare the darkest and lightest colors for lost texture and check that both views use the same intended color identity. Ask me to shortlist two options, then prepare a manufacturer discussion brief that clearly requests physical swatches. These images are concept studies, not dye formulas, color-calibrated proofs, or production-ready patterns. Do not contact a manufacturer, upload branded photographs, or place orders without approval.
```

## Iterate with a purpose

### 1. Shortlist two colors

```text
Create a side-by-side comparison of [TWO SELECTED COLORWAYS], including enlarged texture areas and a list of visible tradeoffs.
```

### 2. Test trim contrast

```text
Explore two trim colors on the approved panels while holding the main garment color fixed. Record every permitted change.
```

### 3. Prepare swatch questions

```text
Draft questions for a supplier about actual fabric swatches, dye consistency, wash performance, and sample lead times without sending them.
```

## Expected deliverables

- Six front-and-back colorway candidate pairs if supported
- Labeled comparison contact sheet
- Seam, texture, and logo exception log
- Physical-swatch discussion brief

## Acceptance checks

- Each intended colorway has a matching front and back identifier
- Only allowed panels are intentionally recolored
- Light and dark candidates retain reviewable texture or disclose loss
- Logos and fasteners are checked against the source
- A partially hidden seam is marked uncertain rather than invented
- No production formula or color-accuracy guarantee is claimed

## Access, privacy and stop conditions

- Available image tools may change garment shape, text, stitching, and pixels
- Use only authorized garment photographs and brand assets
- Digital previews cannot replace material and dye testing
- Supplier contact and external uploads require separate approval

## Two possible extensions

- Add photographs of real swatches to the comparison
- Create a separate design-decision record after physical sampling
