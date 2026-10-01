---
id: artwork-print-preflight-preview
title: "Artwork Print Preflight Preview"
summary: "Prepare print-size previews and a preflight checklist for authorized raster artwork."
category: image-editing
level: intermediate
timebox_minutes: 90
capabilities: ["files", "images"]
tags: ["print-preflight", "artwork", "resolution"]
status: recipe-not-run
---

# Artwork Print Preflight Preview

Prepare print-size previews and a preflight checklist for authorized raster artwork.

## Scenario

You have a digital illustration that you own and want to print as a small poster. Its aspect ratio differs from the frame, and the edges are soft. Before paying a printer, you want to compare fit options and understand which issues need human review.

## Inputs to prepare

- The authorized source artwork at its best available resolution
- Target paper size, frame opening, and printer-provided requirements
- A choice between white margins, cropping, or an exploratory edge extension
- Any colors, signatures, or fine details that must not be intentionally altered

## Copy this prompt into dot

```text
dot, help preflight [AUTHORIZED RASTER ARTWORK] for a print on [PAPER SIZE] with [FRAME OPENING]. Use [PRINTER REQUIREMENTS] if supplied; otherwise label bleed, color-profile, and format requirements unverified. Begin by reporting the actual pixel dimensions, aspect ratio, and effective resolution for each proposed fit. Do not treat a larger exported file as proof of recovered detail.

Prepare a no-reconstruction option with margins, a crop preview, and, only if I select it, an exploratory edge-extension candidate using available image tools. Keep [PROTECTED DETAILS] away from unintended trimming. If upscaling is supported, show an original-versus-upscaled detail comparison and identify invented or softened texture. Keep all generative candidates separate from the untouched artwork; do not promise exact colors, geometry, signatures, typography, or pixels.

Deliver a size-and-fit review sheet, a candidate export with its settings recorded if supported, and a preflight checklist for the printer. Verify final dimensions, visible margins, crop boundaries, and readability of any source lettering. Flag low-resolution details or a missing printer specification as unresolved. Recommend a small physical proof before committing to a full print run. Do not upload artwork to a printer, convert an unknown color profile destructively, purchase printing, or grant reproduction rights without approval.
```

## Iterate with a purpose

### 1. Choose fit treatment

```text
Apply the approved [MARGINS OR CROP] treatment to a separate candidate and verify the final dimensions against the supplied printer requirements.
```

### 2. Inspect fine detail

```text
Produce comparison crops of signatures, thin lines, and textured areas so the user can decide whether upscaling is acceptable.
```

### 3. Prepare proof review

```text
Create a physical-proof checklist for color shifts, trimming, banding, edge detail, and paper finish without placing an order.
```

## Expected deliverables

- Pixel-dimension and effective-resolution report
- Margin and crop comparison previews
- Candidate export with recorded settings if supported
- Printer preflight and physical-proof checklist

## Acceptance checks

- Effective resolution is computed from real pixel dimensions and print size
- A crop never silently removes a signature or protected detail
- Unknown printer requirements remain explicitly unverified
- Upscaling artifacts are compared with the source
- An undersized source triggers a quality limitation instead of a quality guarantee
- No print order or rights grant is made

## Access, privacy and stop conditions

- Image and print-export support varies by available toolchain
- Upscaling and generative extension can invent details
- Digital previews cannot guarantee printed color or finishing results
- Printer uploads, purchases, and reproduction permissions require separate approval

## Two possible extensions

- Compare a photographed physical proof against the intended design
- Adapt the approved fit for a second frame size
