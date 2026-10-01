---
id: heirloom-photo-conservation-study
title: "Heirloom Photo Conservation Study"
summary: "Prepare restrained repair studies of a damaged photograph while documenting uncertain reconstruction."
category: image-editing
level: intermediate
timebox_minutes: 90
capabilities: ["files", "images"]
tags: ["photo-restoration", "archives", "comparison"]
status: recipe-not-run
---

# Heirloom Photo Conservation Study

Prepare restrained repair studies of a damaged photograph while documenting uncertain reconstruction.

## Scenario

You have an authorized scan of an old photograph with scratches, fading, and a torn corner. Relatives disagree about whether to keep its original texture. You want a comparison that separates modest cleanup from speculative reconstruction before choosing an image for a private album.

## Inputs to prepare

- An authorized high-resolution scan, with identifying metadata removed where appropriate
- A list of defects to repair and features that must remain recognizable
- A choice of monochrome or original color, plus the intended print size
- Any authentic reference scan and the permitted private review audience

## Copy this prompt into dot

```text
dot, help me prepare a careful conservation study of [AUTHORIZED SCAN] for [PRIVATE ALBUM OR PRINT SIZE]. Inspect the image first and list visible damage separately from details you cannot confidently recover. Use [AUTHENTIC REFERENCE], if supplied, only for the purpose I authorize. Ask before making assumptions about missing facial features, clothing, signs, or background objects.

If image editing is available in this account, make two clearly labeled studies: a restrained cleanup that retains grain and age, and a stronger repair version with reconstructed regions called out. Prioritize [REPAIR PRIORITIES] and compare each version against [FEATURES TO RETAIN]. Preserve the original as a separate file. Do not describe either study as historical evidence or imply that uncertain details have been recovered accurately.

Provide a before-and-after review sheet, an edit log, and a print-size recommendation based on the actual output dimensions. Check faces, edges, repeated textures, and the torn area at close zoom; report remaining defects and limitations. Generative edits can change geometry and exact pixels, so flag drift instead of promising perfect preservation. Keep all files private to [REVIEW AUDIENCE]; do not publish, share, or overwrite originals without my approval.
```

## Iterate with a purpose

### 1. Compare texture

```text
Compare only the grain, contrast, and repair seams of the two studies at matching zoom. Recommend the gentler version where evidence is missing.
```

### 2. Prepare print candidate

```text
Prepare a separate print candidate for [SIZE] using the chosen study. Verify actual dimensions and show any crop before exporting.
```

### 3. Record provenance

```text
Create a short archival caption that identifies the source scan, approved edits, uncertain reconstruction, and the untouched original’s filename without claiming authenticity for new details.
```

## Expected deliverables

- Two labeled repair studies if image editing is available
- Before-and-after review sheet
- Edit log distinguishing cleanup from reconstruction
- Print-size and resolution note

## Acceptance checks

- The original scan remains unchanged and separately named
- Each reconstructed region appears in the edit log
- Faces and clothing are compared at matching zoom
- A missing corner without a reference remains marked uncertain
- Final dimensions support the stated print-size recommendation
- No version is described as an authentic recovered original

## Access, privacy and stop conditions

- Restoration depends on available image and file tools; missing tools may limit the result to an edit plan
- Generative repair may change facial details, geometry, text, and pixels
- Use only images and reference material the user is authorized to edit
- External sharing requires a named audience and approval

## Two possible extensions

- Add family-supplied captions as a separate document
- Create a scan-handling checklist for the rest of the album
