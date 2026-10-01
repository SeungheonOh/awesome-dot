---
id: product-instruction-leaflet
title: "Product Instruction Leaflet"
summary: "Design a clear instruction leaflet for a low-risk product using only approved assembly information."
category: design-publishing
level: intermediate
timebox_minutes: 120
capabilities: ["files", "images"]
tags: ["instructions", "technical-handoff", "product-design"]
status: recipe-not-run
---

# Product Instruction Leaflet

Design a clear instruction leaflet for a low-risk product using only approved assembly information.

## Scenario

Your small team makes a simple flat-pack desktop organizer. The assembly text is accurate but difficult to scan, and customers confuse two similar panels. You want a compact leaflet that clarifies the steps without inventing safety claims, compatibility promises, or missing manufacturing details.

## Inputs to prepare

- Approved instructions for a low-risk non-electrical product
- Authorized product photos or diagrams and a verified parts list
- Leaflet dimensions, print constraints, and intended languages
- Existing warnings, support information, and revision identifier

## Copy this prompt into dot

```text
dot, design an instruction leaflet for [LOW-RISK PRODUCT] using [APPROVED INSTRUCTIONS], [VERIFIED PARTS LIST], and [AUTHORIZED DIAGRAMS OR PHOTOS]. Use [LEAFLET DIMENSIONS] and [PRINT CONSTRAINTS]. Start by mapping each instruction to the parts it uses and list any ambiguous orientation, quantity, or step dependency. Ask for clarification instead of inventing a missing assembly step or drawing a hidden mechanism from guesswork.

Create a clear sequence with numbered steps, consistent part labels, an inventory panel, and a completion check. Preserve supplied warnings and support information without weakening their meaning. Use editable text and simple visual annotations; if an image tool is used for illustration, label uncertain geometry and do not treat it as an engineering drawing. Keep the project limited to the approved low-risk product, not electrical, medical, child-safety, or load-bearing instructions.

Deliver an editable leaflet or full layout specification, a review export if supported, and a step-to-source checklist. Test confusingly similar parts, mirrored orientation, a missing part, and small black-and-white printing. Verify that labels are consistent from inventory to final step and that [REVISION IDENTIFIER] appears on the leaflet. Note untested physical assembly. Do not publish, send to customers, make compliance claims, or replace official instructions until the responsible product owner approves the final content and audience.
```

## Iterate with a purpose

### 1. Test a novice walkthrough

```text
Walk through the leaflet from a first-time reader’s perspective and record every point requiring an assumption; do not claim a physical assembly test occurred.
```

### 2. Improve part distinction

```text
Design clearer labels and callouts for [SIMILAR PARTS], using only verified dimensions and orientations from the supplied source.
```

### 3. Prepare translation layout

```text
Create a text extraction and space-expansion plan for [LANGUAGE] while preserving step identifiers and marking translations for qualified review.
```

## Expected deliverables

- Numbered instruction leaflet draft
- Parts inventory and label system
- Step-to-source checklist
- Novice-reader and print-size test notes
- Revision and product-owner approval panel

## Acceptance checks

- Each step uses verified parts and source instructions
- Similar parts are visually distinguishable
- Mirrored orientation is explicitly checked
- A missing part leads to approved support guidance rather than improvisation
- Warnings retain their approved meaning
- Physical testing and compliance status are not invented

## Access, privacy and stop conditions

- The scope is limited to a low-risk non-electrical product
- Generated illustrations are not verified engineering drawings
- Layout and export support vary by available tools
- Product-owner approval is needed before customer distribution or instruction replacement

## Two possible extensions

- Create a separate quick-start card after content approval
- Prepare a customer-feedback form focused on confusing steps
