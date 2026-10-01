---
id: portrait-lighting-study
title: "Portrait Lighting Study"
summary: "Explore portrait lighting directions with consent-aware edits and visible identity-drift checks."
category: image-editing
level: intermediate
timebox_minutes: 60
capabilities: ["files", "images"]
tags: ["portraits", "lighting", "consent"]
status: recipe-not-run
---

# Portrait Lighting Study

Explore portrait lighting directions with consent-aware edits and visible identity-drift checks.

## Scenario

A colleague has authorized you to use their portrait for a small internal speaker biography. The existing photo is evenly lit but flat. You want a few lighting studies to discuss with them, without silently reshaping their face or presenting an edited background as a real location.

## Inputs to prepare

- An authorized adult portrait and the subject’s agreed edit scope
- Three desired lighting directions or neutral visual references
- Features, clothing, and accessories to retain
- The private reviewer list and intended final image dimensions

## Copy this prompt into dot

```text
dot, create a portrait-lighting study from [AUTHORIZED ADULT PORTRAIT] within [SUBJECT-APPROVED EDIT SCOPE]. The intended use is [BIOGRAPHY CONTEXT], and the private reviewers are [REVIEWER LIST]. Compare soft window light, gentle side light, and a subtle studio-style treatment, adjusting these choices if the source makes them implausible. Keep the original file separate.

Use available image tools to explore lighting and a neutral background only. Do not deliberately alter facial structure, body shape, age, skin tone, disability-related features, clothing, or identity-bearing details. Ask before removing personal accessories. Label any synthetic background as a visual treatment rather than an actual place. If a requested look cannot be achieved without substantial identity drift, explain that and recommend a new photograph.

Deliver three labeled candidates, a source comparison at face level, and a short subject-review checklist. Inspect eyes, teeth, hair edges, glasses reflections, and the transition from face to neck. Report incidental changes because generative tools do not guarantee exact likeness or pixel preservation. Include the actual dimensions and a crop preview for [TARGET FORMAT]. Keep the candidates private, and do not publish, send them to reviewers, or replace a profile photo until I approve the audience and selected image.
```

## Iterate with a purpose

### 1. Review likeness

```text
Compare the selected study with the source at matching face size and list any differences the subject should explicitly review.
```

### 2. Prepare biography crops

```text
Prepare square and landscape crop previews of the approved candidate, keeping space for separately typeset biography text.
```

### 3. Create reshoot brief

```text
Turn the preferred lighting direction into a simple reshoot brief with camera position, light direction, and background guidance.
```

## Expected deliverables

- Three lighting candidates if supported
- Face-level source comparison
- Biography crop previews
- Subject consent and quality review checklist

## Acceptance checks

- The requested edit scope is stated before candidates are produced
- Eyes, glasses, hair edges, and teeth are inspected
- Identity or skin-tone drift is disclosed rather than hidden
- A source with obstructed facial features triggers a limitation note
- Synthetic backgrounds are labeled as treatments
- No image is sent or published without audience approval

## Access, privacy and stop conditions

- Use an adult portrait with the subject’s authorization for the intended edits
- Image tools cannot guarantee exact likeness or geometry preservation
- The recipe does not infer identity, emotion, health, or protected traits
- Profile replacement and external sharing are separate actions

## Two possible extensions

- Use subject feedback to select a reshoot direction
- Build a consent-aware portrait intake checklist for future speakers
