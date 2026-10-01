---
id: travel-photo-distraction-cleanup
title: "Travel Photo Distraction Cleanup"
summary: "Prepare restrained travel-photo edits with clear documentation of removed distractions."
category: image-editing
level: beginner
timebox_minutes: 45
capabilities: ["files", "images"]
tags: ["travel-photos", "retouching", "edit-log"]
status: recipe-not-run
---

# Travel Photo Distraction Cleanup

Prepare restrained travel-photo edits with clear documentation of removed distractions.

## Scenario

You have a vacation photograph of a public overlook with a stray bag and temporary sign distracting from the view. You want a cleaner image for your own wall, while keeping an honest record that the scene was edited and avoiding unnecessary treatment of identifiable people.

## Inputs to prepare

- An authorized travel photo with unnecessary identifying metadata removed
- A marked list of small objects the user wants removed
- Landmarks, people, and scene features that should remain unchanged
- Desired personal print size and crop preference

## Copy this prompt into dot

```text
dot, prepare a restrained cleanup of [AUTHORIZED TRAVEL PHOTO] for a personal print at [PRINT SIZE]. Remove only [MARKED DISTRACTIONS] and preserve [LANDMARKS AND FEATURES TO KEEP] as closely as available tools allow. First confirm which requested objects overlap people, architecture, reflections, or complex textures. If an area would require substantial scene invention, show the uncertainty and ask whether to retain it instead.

If image editing is available, make one conservative candidate and a separate optional crop that avoids the distraction without reconstruction. Do not add a landmark, move a person, change weather, or alter signage beyond the agreed list. Keep the untouched source separately, and do not infer anyone’s identity from the image. Treat this as a personal aesthetic edit, not documentary or evidentiary photography.

Deliver both review options, a simple edit-location map, and an export recommendation based on actual pixel dimensions. Inspect repeated pavement, foliage seams, reflections, and shadow continuity where objects were removed. Report any geometry or text changes because generative edits may not preserve exact pixels. If neither cleanup nor crop looks credible at the intended size, recommend leaving the source unchanged or using a smaller print. Do not publish, tag people, or share image location data without my approval.
```

## Iterate with a purpose

### 1. Compare crop versus repair

```text
Compare the non-reconstructed crop with the edited version at the intended print ratio and explain which has fewer distracting artifacts.
```

### 2. Inspect print detail

```text
Prepare close-up review crops around every repaired region and check them at an equivalent print viewing scale.
```

### 3. Write an honest caption

```text
Draft a short personal-album caption that can disclose object removal without inventing facts about the trip or location.
```

## Expected deliverables

- Conservative cleanup candidate if supported
- Non-reconstructed crop alternative
- Edit-location map
- Print-resolution and artifact review note

## Acceptance checks

- Only objects on the approved list are intentionally removed
- An untouched original remains available
- Overlaps with people or complex architecture are flagged
- Reflections and shadows are checked after removal
- An unrepairable region triggers a keep-original or crop option
- Location metadata is not shared with third parties

## Access, privacy and stop conditions

- Use only photographs the user is authorized to edit
- Generative cleanup may introduce scene details or alter exact geometry
- The result is not a documentary record of an unedited scene
- Sharing, tagging, and publication are outside this private-edit scope

## Two possible extensions

- Create a matching crop set for a personal wall arrangement
- Record preferred retouching limits for the rest of the trip’s photos
