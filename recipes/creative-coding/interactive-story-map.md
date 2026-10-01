---
id: interactive-story-map
title: "Interactive Story Map"
summary: "Build a browser-based story map with a complete keyboard-readable narrative beside the visual route."
category: creative-coding
level: intermediate
timebox_minutes: 150
capabilities: ["code", "files"]
tags: ["storytelling", "maps", "accessible-navigation"]
status: recipe-not-run
---

# Interactive Story Map

Build a browser-based story map with a complete keyboard-readable narrative beside the visual route.

## Scenario

You have written a fictional story that unfolds across six places on an imaginary island. You want readers to explore the route visually without making the map essential for understanding the plot. This is a small first coding project using dot, so the build should stay easy to inspect and run.

## Inputs to prepare

- A fictional story divided into location-based chapters
- An authorized illustrated map or simple fictional coordinates
- Preferred reading order, visual style, and maximum chapter count
- Target browsers and a private preview or explicitly approved publication destination

## Copy this prompt into dot

```text
dot, help me build a small interactive story map from [FICTIONAL CHAPTERS] and [AUTHORIZED MAP OR FICTIONAL COORDINATES]. Start by proposing the smallest useful version and explain how I will open it using the tools available here. Use simple browser technologies and avoid paid services, secret keys, or live map integrations. If a runnable environment is unavailable, deliver source files with clear setup instructions rather than claiming it was tested.

Show selectable location markers beside a complete ordered chapter list. Selecting either view should reveal the same chapter and visibly indicate the current location. Include previous and next controls, a reset-to-start action, responsive layout, and meaningful keyboard focus. The story must remain readable without interacting with the map. Keep the map schematic and do not infer real locations or request device location.

Deliver the source, fictional sample data, a short editing guide, and a test record distinguishing executed checks from suggested ones. Test duplicate location names, a chapter without coordinates, a narrow screen, keyboard-only navigation, and missing map artwork. Render story text safely as text rather than executable markup. Use only authorized assets and keep any real personal addresses out of the sample. Create a private preview where supported; do not publish until I approve the content and exact visibility or destination.
```

## Iterate with a purpose

### 1. Add branching choices

```text
Add optional chapter choices using supplied story branches, including a clear way to return to the main path and a test for a branch that rejoins an earlier chapter.
```

### 2. Improve the text alternative

```text
Refine the ordered text view with location descriptions and a printable story-only version, preserving every chapter without relying on map position.
```

### 3. Package an author workflow

```text
Create a plain-language data-editing checklist and validation messages for missing titles, invalid coordinates, and duplicate chapter identifiers.
```

## Expected deliverables

- Runnable browser project or source with setup instructions
- Fictional chapter dataset and authorized map integration
- Keyboard-readable chapter list and navigation
- Author editing guide
- Executed-versus-proposed test record

## Acceptance checks

- Map markers and chapter-list selections stay synchronized
- All chapters remain readable without the map
- A chapter without coordinates appears in the text view with a clear status
- Duplicate display names do not confuse unique chapter identifiers
- Keyboard navigation has visible focus and no trap
- No live location permission or secret key is required

## Access, privacy and stop conditions

- Running and previewing code depend on available environment and account tools
- The map is fictional or schematic rather than a navigation service
- Only authorized assets and sanitized story data are included
- Publication needs approval of content, destination, and audience

## Two possible extensions

- Add a downloadable story-only reading edition
- Explore a second narrative route using new user-authored chapters
