---
id: generative-type-foundry
title: "Generative Type Foundry"
summary: "Build a seeded typography playground that preserves exact text while varying layout and rhythm."
category: creative-coding
level: intermediate
timebox_minutes: 100
capabilities: ["code", "files", "websites"]
tags: ["typography", "svg", "deterministic-design"]
status: recipe-not-run
---

# Generative Type Foundry

Build a seeded typography playground that preserves exact text while varying layout and rhythm.

## Scenario

A developer wants to understand the difference between text content and visual layout by making a small poster generator. A short phrase becomes a field of repeated words, spacing, and rotation. The project should keep the wording accurate, respect font licensing, and make every variation reproducible.

## Inputs to prepare

- [EXACT TEXT] and language
- [CANVAS SIZE] with screen or print intent
- [APPROVED FONT] and license information
- [SEED] and allowed spacing, scale, and rotation ranges

## Copy this prompt into dot

```text
dot, create Generative Type Foundry using [EXACT TEXT], [CANVAS SIZE], [APPROVED FONT], and [SEED]. If suitable coding tools are available, build a local browser playground with real text and editable SVG output. Check which font files and text-shaping features are actually available before promising identical rendering across environments; ask before downloading or installing anything.

Start with a plain reference layout that preserves the exact supplied wording. Add bounded seeded variations in word position, spacing, scale, and rotation while keeping a separate readable transcript. Provide controls for those ranges, a seed field, regenerate, reset, and an overlap-warning toggle. Avoid cutting apart combining characters or emoji sequences: operate on whole words unless supported grapheme segmentation is verified. Explain any limitations for right-to-left or complex-script text.

Deliver editable source, three original presets, SVG exports where supported, and a font-and-parameter manifest. Keep text as text by default; outline conversion is optional and requires a supported tool and appropriate font rights. Check empty input, very long words, missing glyphs, off-canvas text, and the same seed after reset. Include a high-contrast static preview and reduced-motion behavior. Do not replace the wording with an image-generated approximation. Ask before publication, uploading fonts, or using organization branding; distinguish measured layout checks from subjective design judgments.
```

## Iterate with a purpose

### 1. Add a controlled poster series

```text
Create a three-poster series that changes one parameter family at a time while preserving text, font, seed, and canvas size where applicable.
```

### 2. Create a print-preflight view

```text
Add margin guides, a scale reference, and a font-dependency report for the selected physical page size, without promising commercial print readiness.
```

### 3. Support reviewed multilingual text

```text
Using text I supply, add a language-specific preset after checking shaping, direction, and line-breaking support; keep unsupported cases clearly labeled.
```

## Expected deliverables

- Editable typography playground source
- Three seeded design presets
- Conditional editable SVG exports
- Font, license, text, and parameter manifest
- Layout and character-handling verification checklist

## Acceptance checks

- The readable transcript matches the supplied text exactly
- Repeated generation with the same seed and parameters reproduces the same layout
- Empty text and missing font files yield useful messages
- Long words and off-canvas bounds are flagged rather than silently clipped
- Combining characters and emoji are not split by unsupported character indexing
- Reset restores seed and layout controls as documented
- Export dependencies identify fonts needed to reproduce the appearance

## Access, privacy and stop conditions

- Font availability, licensing, and shaping support vary by environment
- SVG text can render differently on machines without the same font
- Outlining is conditional and may remove text editability and accessibility
- Branding, font uploads, and publication require approval

## Two possible extensions

- Add a local comparison board for shortlisted presets
- Create a text-only specification that another designer can reproduce
