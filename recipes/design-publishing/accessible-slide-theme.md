---
id: accessible-slide-theme
title: "Accessible Slide Theme"
summary: "Create a reusable slide theme that makes technical presentations easier to read and navigate."
category: design-publishing
level: intermediate
timebox_minutes: 150
capabilities: ["files"]
tags: ["slides", "accessibility", "engineering-communication"]
status: recipe-not-run
---

# Accessible Slide Theme

Create a reusable slide theme that makes technical presentations easier to read and navigate.

## Scenario

An engineering team shares reviews with a mixed audience of specialists and new colleagues. Their slides use small code screenshots and color-only status labels. You want a reusable theme with practical examples that makes the next presentation easier to follow without claiming perfect accessibility from appearance alone.

## Inputs to prepare

- A sanitized sample outline and two representative technical slides
- The intended audience, presentation setting, and slide format
- Approved brand colors, fonts, and logo permissions
- Required layout types, accessibility priorities, and any confidential content to exclude

## Copy this prompt into dot

```text
dot, build an accessible slide-theme starter for [TEAM AND AUDIENCE] using [SANITIZED SAMPLE OUTLINE] and [AUTHORIZED BRAND ASSETS]. The presentation setting is [ROOM OR REMOTE], and the required file format is [FORMAT]. First identify barriers in the supplied examples, especially small code, dense diagrams, unexplained acronyms, and meaning conveyed only by color. Explain the proposed improvements in everyday language.

Create reusable layouts for a title, agenda, technical explanation, comparison, code excerpt, decision, and next steps. Use editable text, a consistent hierarchy, meaningful reading order where supported, and non-color status labels. Include sample slides based only on supplied facts; mark placeholders instead of inventing results. Keep confidential project identifiers and production data out of examples. Provide guidance for replacing screenshots with readable text or simplified diagrams.

Deliver an editable theme or layout specification depending on available tools, a short authoring guide, and an accessibility test record. Check contrast, long headings, a dense code example, monochrome viewing, and the smallest expected screen. Inspect exported reading order and image descriptions if the chosen format supports them; clearly state untested properties. Do not call the deck fully accessible on visual checks alone. Keep drafts private, and do not upload, present, or share outside [APPROVED AUDIENCE] without approval.
```

## Iterate with a purpose

### 1. Repair a real slide

```text
Apply the theme to [SANITIZED TECHNICAL SLIDE], retaining its factual meaning and recording the readability improvements and remaining compromises.
```

### 2. Test presenter use

```text
Add sample speaker notes and a keyboard-based presentation check, then report limitations of the actual format and available viewer.
```

### 3. Create a theme handoff

```text
Prepare a concise handoff showing which layouts to choose, how to add image descriptions, and how to test each new export.
```

## Expected deliverables

- Seven reusable slide layouts or a complete specification
- Sanitized example slides
- Plain-language authoring guide
- Accessibility and export test record

## Acceptance checks

- All required layout types are present
- Status information remains understandable without color
- A dense code example is readable or split into meaningful parts
- Long headings do not overlap other elements
- Contrast checks name the tested color pairs
- Exported reading-order and description support are tested or marked unverified

## Access, privacy and stop conditions

- Editable theme and accessibility features depend on the available presentation tools
- Visual quality alone does not establish accessibility compliance
- Use only authorized brand assets and sanitized examples
- External sharing or publication requires the approved files and audience

## Two possible extensions

- Create a companion one-page technical-summary template
- Test the theme with feedback from actual audience members
