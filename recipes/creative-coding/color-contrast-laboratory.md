---
id: color-contrast-laboratory
title: "Color-Contrast Laboratory"
summary: "Build an interactive color lab that explains text contrast and separates measured results from broader accessibility."
category: creative-coding
level: intermediate
timebox_minutes: 150
capabilities: ["code", "files"]
tags: ["color", "accessibility", "design-tools"]
status: recipe-not-run
---

# Color-Contrast Laboratory

Build an interactive color lab that explains text contrast and separates measured results from broader accessibility.

## Scenario

Your team has several brand colors but does not know which pairs work for interface text. You want a small learning tool that compares foreground and background colors, explains its calculation, and makes limitations visible. The first version should be useful without accounts, analytics, or a design-platform connection.

## Inputs to prepare

- An authorized palette with names and color values
- The contrast standard and version the project should implement
- Example text sizes and interface states to preview
- Target browsers, export needs, and private-versus-public visibility

## Copy this prompt into dot

```text
dot, build a color-contrast laboratory for [AUTHORIZED PALETTE] using [SELECTED CONTRAST STANDARD AND VERSION]. First confirm the standard’s calculation, thresholds, and scope from its official documentation, and cite that documentation in the project. Explain the smallest useful version before coding. If current documentation is unavailable, mark the standard implementation unverified rather than inventing rules.

Let users choose foreground and background colors, enter valid color values, swap the pair, and preview [TEXT SIZES AND INTERFACE STATES]. Show the calculated result with a plain-language explanation and text labels, never a pass indication that relies on color alone. Treat gradients, transparency, and images as out of scope unless a specific background-compositing rule is implemented and explained. Do not present a contrast result as proof that an entire interface is accessible.

Deliver source files, an authorized sample palette, a short calculation note, and a test record. Validate reference cases from the selected standard, identical colors, invalid input, keyboard-only use, and narrow screens. Round displayed results without changing threshold decisions, and show which values were actually used. If supported, add a local downloadable comparison report that contains only the chosen palette. Avoid collecting user data or adding analytics. Keep previews private, and ask before publishing the tool, uploading brand assets, or connecting a design account.
```

## Iterate with a purpose

### 1. Compare palette pairs

```text
Add a sortable comparison of all foreground-background pairs with explicit labels and a filter for the selected text-use case.
```

### 2. Explain failed cases

```text
For a failed pair, show a small set of candidate adjustments and their recalculated results while preserving the original value for comparison.
```

### 3. Add an audit export

```text
Create a local report containing tested color pairs, standard version, calculation date, assumptions, and untested interface states without claiming whole-product compliance.
```

## Expected deliverables

- Interactive contrast-lab source
- Authorized sample palette and pair previews
- Standard-linked calculation and limitations note
- Reference-case and input-validation test record
- Local comparison export if supported

## Acceptance checks

- The calculation and thresholds match the explicitly selected standard
- Identical colors and invalid inputs produce appropriate visible outcomes
- Rounded display values do not change the underlying threshold decision
- Results are understandable without color perception
- Unsupported transparency or gradients are rejected or clearly scoped
- The tool never equates contrast alone with overall accessibility

## Access, privacy and stop conditions

- Reference verification, code execution, and exports depend on available tools
- The implemented standard and version must be stated explicitly
- Brand palettes and assets require authorization for their intended visibility
- Public hosting, analytics, and design-account connections are separate approvals

## Two possible extensions

- Add user-supplied focus and hover-state comparisons
- Test the lab with designers and engineers unfamiliar with contrast terminology
