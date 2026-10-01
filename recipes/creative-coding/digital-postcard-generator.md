---
id: digital-postcard-generator
title: "Digital Postcard Generator"
summary: "Build a local-first postcard composer with editable text, authorized imagery, and verifiable export behavior."
category: creative-coding
level: intermediate
timebox_minutes: 150
capabilities: ["code", "files", "images"]
tags: ["postcards", "canvas", "creative-tools"]
status: recipe-not-run
---

# Digital Postcard Generator

Build a local-first postcard composer with editable text, authorized imagery, and verifiable export behavior.

## Scenario

You want to make a few digital postcards from your own photographs without uploading them to an unfamiliar service. The project should offer a small set of layouts and downloadable images. You also want a text companion so the message is not available only as lettering inside a picture.

## Inputs to prepare

- Authorized images or a choice of built-in geometric backgrounds
- A fictional or user-approved postcard message and signature
- Target pixel dimensions, layout choices, and visual style
- Supported browsers and whether the result should stay private

## Copy this prompt into dot

```text
dot, build a small digital-postcard generator using [AUTHORIZED IMAGES OR GEOMETRIC BACKGROUNDS], [APPROVED MESSAGE], and [TARGET PIXEL DIMENSIONS]. Begin with a simple plan explaining how I can run it with the tools available here. Prefer local browser processing and do not add accounts, analytics, remote image uploads, recipient-address collection, or automatic sending. If an online service becomes necessary, stop and explain what data it would receive before using it.

Provide a few editable layouts, a crop-position control, separate message and signature fields, a reset action, and a downloadable image export. Use ordinary layout or canvas text for reliable editing rather than relying on generated typography. Include a plain-text companion containing the message and a user-editable image description. If image generation is available, keep optional generated backgrounds separate and label them clearly.

Deliver source files, sample content, setup guidance, and a test log. Test a long message, Unicode characters, a missing image, an unsupported file, repeated exports, and a narrow screen. Verify the actual downloaded dimensions and whether text is clipped. Inspect whether any network request transmits image or message content; report what was tested rather than guaranteeing privacy without evidence. Keep originals untouched and disclose unverified export metadata. Do not send postcards or publish the generator until I approve the files, destination, and audience.
```

## Iterate with a purpose

### 1. Improve long-message handling

```text
Add a clear overflow warning and an optional second layout for [LONG MESSAGE], without silently truncating or rewriting the user’s words.
```

### 2. Add batch variations

```text
Generate a local preview sheet of approved layout and background combinations, keeping the message unchanged and avoiding automatic downloads until selected.
```

### 3. Verify export privacy

```text
Review the export and network behavior with the available inspection tools, documenting what image metadata and content transmission were actually checked and what remains unknown.
```

## Expected deliverables

- Local-first postcard composer source
- Editable layouts and authorized sample assets
- Image export and plain-text companion
- Setup and customization guide
- Dimensions, overflow, and privacy test record

## Acceptance checks

- Long text is visible or produces an explicit overflow warning
- Downloaded images have the requested pixel dimensions
- Unicode text and repeated exports are tested
- Missing and unsupported files fail with a readable message
- Any content-transmitting network request is disclosed before use
- No sending, address collection, or publication occurs automatically

## Access, privacy and stop conditions

- Browser rendering, file export, and inspection support depend on available tools
- Only user-authorized images and messages are used
- Privacy and metadata removal are not claimed without actual verification
- Sending postcards or public hosting needs approval of destination and audience

## Two possible extensions

- Add a print-layout option with verified printer requirements
- Create an accessible gallery of user-approved postcard examples
