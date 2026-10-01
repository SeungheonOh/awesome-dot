---
id: recipe-step-photo-unifier
title: "Recipe Step Photo Unifier"
summary: "Unify authorized cooking-step photos while preserving the visual cues needed to follow the recipe."
category: image-editing
level: beginner
timebox_minutes: 75
capabilities: ["files", "images"]
tags: ["food-photography", "instructional-images", "consistency"]
status: recipe-not-run
---

# Recipe Step Photo Unifier

Unify authorized cooking-step photos while preserving the visual cues needed to follow the recipe.

## Scenario

You photographed a family recipe across two evenings, so the backgrounds and white balance vary. The images will accompany a private recipe booklet. You want a cohesive sequence without making raw ingredients look cooked or erasing the textures that explain each step.

## Inputs to prepare

- Authorized photos labeled with their cooking step
- The exact recipe text and user-confirmed stage descriptions
- Preferred background and overall lighting style
- Target booklet dimensions and any food details that must remain visible

## Copy this prompt into dot

```text
dot, help unify [AUTHORIZED COOKING-STEP PHOTOS] for [RECIPE TITLE] in a [BOOKLET SIZE] layout. Use the supplied [RECIPE TEXT AND STAGE LABELS] as the source of truth for ordering. First make a photo-to-step inventory and flag missing or ambiguous stages instead of inventing a cooking event. Keep the original images unchanged.

Where available, use image editing to bring white balance, background tone, crop, and overall exposure into a consistent visual range. Preserve the observable texture, ingredient quantity cues, browning, and utensil positions that explain the procedure as closely as possible. Do not make raw food appear cooked, add ingredients, fabricate doneness evidence, or remove relevant spills that show the actual process. Ask if an edit would change an instructional fact.

Deliver the ordered candidate sequence, a source comparison sheet, and a list of photos that should be retaken. Put step numbers and captions in a separate text layer or document so spelling can be checked. Review continuity between adjacent steps and test small-size legibility in the intended layout. Note any generated texture or geometry drift. These photos cannot verify food safety; retain the user-confirmed written instructions and flag contradictory imagery. Do not upload or publish the booklet without approval.
```

## Iterate with a purpose

### 1. Test step continuity

```text
Compare every adjacent pair of approved photos and identify unexplained changes in ingredients, vessels, or cooking stage.
```

### 2. Prepare reshoot plan

```text
Write a minimal reshoot list for missing stages, including the visible cue each replacement photo must demonstrate.
```

### 3. Build caption set

```text
Draft concise step captions from the supplied recipe text, keeping timing and safety information consistent with that text and flagging uncertainties.
```

## Expected deliverables

- Ordered and consistently treated photo candidates
- Source-to-candidate comparison sheet
- Missing-stage and reshoot list
- Separately editable step captions

## Acceptance checks

- Every candidate maps to a supplied recipe step
- Missing stages are labeled rather than fabricated
- Raw and cooked appearances are not intentionally swapped
- Ingredient and vessel continuity is checked between adjacent images
- A low-resolution close-up is flagged if the texture becomes unreliable
- Step captions remain separately editable and match the source text

## Access, privacy and stop conditions

- Image editing and layout exports depend on available tools
- Visual edits cannot establish doneness or food safety
- Only authorized recipe photographs and text may be used
- Publication or distribution of the booklet needs separate approval

## Two possible extensions

- Create a consistent shooting guide for another recipe
- Assemble the approved sequence into a separately reviewed recipe layout
