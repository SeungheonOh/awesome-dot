---
id: panorama-crop-storyboard
title: "Panorama Crop Storyboard"
summary: "Turn one authorized panorama into a coordinated sequence of crops for different viewing contexts."
category: image-editing
level: beginner
timebox_minutes: 45
capabilities: ["files", "images"]
tags: ["cropping", "storytelling", "composition"]
status: recipe-not-run
---

# Panorama Crop Storyboard

Turn one authorized panorama into a coordinated sequence of crops for different viewing contexts.

## Scenario

You have an authorized wide landscape panorama but need a balanced banner, square image, and three-part sequence. The important subject is close to an edge. You want an intentional visual story that avoids accidental cropping and clearly distinguishes a rearrangement from the original scene.

## Inputs to prepare

- An authorized high-resolution panorama
- The primary subject and secondary details to preserve
- Target aspect ratios, display sizes, and sequence length
- A preferred reading direction and any caption or text-safe zones

## Copy this prompt into dot

```text
dot, plan a coordinated crop storyboard from [AUTHORIZED PANORAMA] for [TARGET FORMATS] and a [SEQUENCE LENGTH]-panel sequence. The main subject is [PRIMARY SUBJECT], and the supporting details are [SECONDARY DETAILS]. Use [READING DIRECTION] and reserve [TEXT-SAFE ZONES] where requested. First inspect the image and propose focal priorities before cropping.

Use available image and file tools to create a whole-image crop map, candidate crops, and a sequence contact sheet. Prefer crops that use existing pixels; do not expand the scene, move landmarks, or fill missing areas unless I explicitly approve a separate exploratory version. Keep the source untouched. If the tool used can alter pixels rather than merely crop, disclose that and verify the candidate visually instead of claiming exact preservation.

For each output, report its aspect ratio, pixel dimensions, and which important features are lost. Check subject placement, horizon continuity, safe space for separate text, and whether adjacent panels overlap intentionally or feel repetitive. Test a narrow banner and a small mobile preview as edge cases. Deliver a naming scheme and a short recommendation for which formats work best. Put captions in a separate editable document; do not trust generated typography. Do not upload, publish, or share any files without approval.
```

## Iterate with a purpose

### 1. Refine sequence rhythm

```text
Reorder the approved panels to improve the transition from establishing view to detail, then explain each panel’s visual purpose.
```

### 2. Test responsive crops

```text
Preview the selected banner at [WIDE AND NARROW WIDTHS] and define a focal-position rule that keeps the primary subject visible.
```

### 3. Pair separate captions

```text
Write one user-reviewable caption per panel from supplied location facts only, keeping all lettering outside the image files.
```

## Expected deliverables

- Whole-image crop map
- Candidate crop files if supported
- Sequence contact sheet
- Dimensions, losses, and focal-position notes

## Acceptance checks

- Every output has its target ratio and actual pixel dimensions recorded
- The primary subject remains visible or a tradeoff is clearly stated
- The narrow-banner case is tested
- Panel overlap is intentional and documented
- No scene expansion or landmark movement occurs without approval
- Captions are separately editable and avoid invented location facts

## Access, privacy and stop conditions

- Crop and export options depend on available tools
- Tools that regenerate images may change exact pixels and details
- The recipe requires an authorized source with sufficient resolution
- Publication and external sharing require separate approval

## Two possible extensions

- Build a print triptych mockup from the approved sequence
- Create reusable focal-position rules for a future gallery layout
