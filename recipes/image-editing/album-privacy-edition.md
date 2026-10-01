---
id: album-privacy-edition
title: "Album Privacy Edition"
summary: "Prepare a privacy-reviewed copy of an authorized photo set with explicit redaction limitations."
category: image-editing
level: intermediate
timebox_minutes: 90
capabilities: ["files", "images"]
tags: ["privacy", "redaction", "photo-review"]
status: recipe-not-run
---

# Album Privacy Edition

Prepare a privacy-reviewed copy of an authorized photo set with explicit redaction limitations.

## Scenario

You want to share a small set of authorized workshop photographs with a limited volunteer group. Some images show name badges, address labels, and laptop screens. You need a reviewable privacy edition and a clear record of exclusions before any file leaves your private workspace.

## Inputs to prepare

- Authorized adult workshop photos and a list of people who consented to sharing
- The exact intended recipient group and sharing purpose
- A list of identifiers to conceal, including text and reflected screens
- The approved redaction method and allowed image formats

## Copy this prompt into dot

```text
dot, prepare a private review copy of [AUTHORIZED PHOTO SET] for possible sharing with [EXACT RECIPIENT GROUP] for [PURPOSE]. Do not send or upload anything yet. First inventory visible identifiers, including badges, addresses, laptop screens, reflections, and location metadata. Use [CONSENT LIST] only to determine which supplied photos are within the permitted scope; do not identify people from their faces.

Propose exclusions and [APPROVED REDACTION METHOD] for each image. If exact image masking, flattening, and metadata inspection are available, create separate redacted exports with opaque coverage or crops that remove the sensitive regions. Do not rely on decorative blur, a removable overlay, or a generative edit as proof of redaction. If supported tools cannot verify these properties, deliver annotated instructions and keep the images unshared.

Produce a redaction register, candidate exports where verifiable, and a final human-review checklist. Reopen the exported files, inspect every marked region at close zoom, check for identifying reflections and thumbnails, and report which metadata fields were actually inspected. Keep originals separate and access-limited. Treat any unreadable or ambiguous region as unresolved, not safe. Ask for my approval of the final files, recipient scope, and delivery method before any sharing.
```

## Iterate with a purpose

### 1. Challenge the review copy

```text
Reinspect each candidate for overlooked reflected screens, tiny badges, partial identifiers, and embedded previews. Report unresolved files rather than certifying them safe.
```

### 2. Minimize the set

```text
Recommend the smallest subset of reviewed photos that serves the sharing purpose while excluding images needing extensive redaction.
```

### 3. Prepare sharing inventory

```text
Create a final filename and recipient-scope checklist for my approval, listing each verified export and any remaining limitations. Do not share it externally.
```

## Expected deliverables

- Per-image identifier and consent-scope inventory
- Redaction register with exclusions
- Flattened candidate exports only when verifiable
- Human-review and proposed-sharing checklist

## Acceptance checks

- No image is shared during preparation
- Each sensitive region maps to a documented crop or opaque redaction
- Exported files are reopened rather than only previewed in the editor
- Reflections and embedded thumbnails are considered explicitly
- If exact masking or metadata inspection is unavailable, the output stays an instruction plan
- Originals remain separate from candidate sharing files

## Access, privacy and stop conditions

- Use only authorized photos; this recipe does not infer identities or consent
- Generative editing alone is not reliable privacy redaction
- Verification is limited to supported file and metadata tools
- External sharing requires approval of files, recipients, and delivery method

## Two possible extensions

- Create a privacy-conscious photography checklist for the next event
- Prepare a consent and photo-selection worksheet using fictional sample data
