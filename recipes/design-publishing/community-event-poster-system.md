---
id: community-event-poster-system
title: "Community Event Poster System"
summary: "Build a consistent poster family with editable event facts and legible variants for print and screens."
category: design-publishing
level: beginner
timebox_minutes: 90
capabilities: ["files", "images"]
tags: ["posters", "events", "workplace-communication"]
status: recipe-not-run
---

# Community Event Poster System

Build a consistent poster family with editable event facts and legible variants for print and screens.

## Scenario

You are organizing an engineering community open house and need a lobby poster, a small noticeboard version, and a screen graphic. Several people will edit the event details. You want one clear visual system that prevents stale dates, inaccessible text, and accidental disclosure of internal project names.

## Inputs to prepare

- Approved event title, date, timezone, venue, and registration destination
- Authorized logo and images, or permission to use a text-only design
- Audience, public-versus-internal visibility, and details that must stay confidential
- Required print and screen sizes plus any brand guidance

## Copy this prompt into dot

```text
dot, create a coordinated poster system for [EVENT] using only [APPROVED EVENT FACTS] and [AUTHORIZED ASSETS]. The intended audience and visibility are [AUDIENCE AND PUBLIC OR INTERNAL SCOPE]. Exclude [CONFIDENTIAL DETAILS]. Begin by turning the facts into a compact content checklist and flag missing dates, timezone, venue details, or registration links before laying out final copy. Do not invent a speaker, sponsor, or registration claim.

Propose two visual directions in plain language, then develop the selected direction for [PRINT AND SCREEN SIZES]. Make the title, date, location, and next action easy to find in that order. Keep wording editable and place text with layout tools rather than baking critical information into a generated image. Use only fonts and imagery available for this use; explain substitutions.

If suitable design tools are available, deliver editable source files, print and screen exports, and a one-page guide for updating event facts. Otherwise provide a complete layout specification with sample copy. Inspect the smallest version, a long event title, monochrome printing, and any registration code or link at actual output size. Report untested print or accessibility requirements. Keep all drafts private; do not publish, email, upload, or order printing until I approve the final files, destination, and audience.
```

## Iterate with a purpose

### 1. Stress-test event copy

```text
Replace the sample title with [LONG TITLE] and add [ACCESS INFORMATION]. Adjust the smallest layout without shrinking essential facts below the agreed readable size.
```

### 2. Prepare update checklist

```text
Create a single change checklist for date, venue, timezone, speaker, and registration edits so each approved poster variant stays consistent.
```

### 3. Package the release

```text
Package only approved variants with clear filenames, export settings, and a distribution checklist that states the permitted audience. Do not distribute them.
```

## Expected deliverables

- Two initial visual directions
- Editable poster system if supported
- Print and screen export candidates
- Event-fact update and distribution checklist

## Acceptance checks

- All variants match the same approved event facts
- The date includes the supplied timezone where relevant
- The smallest output remains readable at intended size
- A long title and monochrome version are tested
- Any registration destination matches the user-supplied link
- Confidential details are absent from public-facing drafts

## Access, privacy and stop conditions

- Layout, font, and export support depend on available tools
- Only authorized brand assets and approved event facts are used
- Generated image text is not relied on for critical event details
- Publishing, uploads, distribution, and print purchases require approval

## Two possible extensions

- Adapt the approved system into a reminder slide
- Create a post-event thank-you graphic using newly approved facts
