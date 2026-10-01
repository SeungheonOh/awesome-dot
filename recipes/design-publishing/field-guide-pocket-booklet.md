---
id: field-guide-pocket-booklet
title: "Field Guide Pocket Booklet"
summary: "Create a pocket reference that helps new team members find approved procedures quickly."
category: design-publishing
level: intermediate
timebox_minutes: 120
capabilities: ["files"]
tags: ["onboarding", "reference-design", "information-design"]
status: recipe-not-run
---

# Field Guide Pocket Booklet

Create a pocket reference that helps new team members find approved procedures quickly.

## Scenario

New members of a campus support team keep searching a long handbook for routine room-setup steps and contact roles. You want a pocket guide for low-risk, everyday tasks. It should make the approved source easy to find and clearly defer any safety or policy question to the full handbook.

## Inputs to prepare

- Approved reference text covering low-risk routine tasks
- Top five questions new readers need answered
- Pocket dimensions, expected printing method, and accessibility needs
- Source owner, revision date, escalation roles, and confidentiality exclusions

## Copy this prompt into dot

```text
dot, turn [APPROVED SOURCE TEXT] into a pocket field guide for [NEW READER ROLE]. Focus on [FIVE ROUTINE QUESTIONS] and exclude [CONFIDENTIAL OR OUT-OF-SCOPE MATERIAL]. First map each proposed quick-reference entry back to a supplied source section. If a procedure is ambiguous, outdated, or safety-sensitive, flag it for the source owner rather than filling the gap with a plausible instruction.

Design for [POCKET DIMENSIONS] and [PRINTING METHOD]. Use plain-language headings, short steps, clear page references, and a compact contents page. Explain unfamiliar terms where the source supports the explanation. Keep emergency, security, and policy instructions as references to approved material; do not rewrite them into a potentially incomplete shortcut. Include [REVISION DATE], the source owner’s role, and the approved escalation route.

If document tools support the format, deliver editable source and a print-ready candidate; otherwise deliver the full content and page-layout specification. Also provide a source map and a timed find-it test with five realistic questions. Check tiny text, page edges, long role names, and a task missing from the guide. Confirm that the reader can tell when to stop and consult the full source. Do not distribute the guide or expose internal procedures outside [AUTHORIZED AUDIENCE] without approval.
```

## Iterate with a purpose

### 1. Run find-it tests

```text
Use five supplied newcomer questions to assess navigation and report which answers require too much page turning or jargon knowledge.
```

### 2. Add an update record

```text
Add a revision record and owner-review checklist that identifies which source sections must be rechecked before reprinting.
```

### 3. Create a large-print edition

```text
Adapt the same approved content into a larger-print edition with matching entry identifiers and source references.
```

## Expected deliverables

- Pocket-guide content and page plan
- Editable source and print candidate if supported
- Source-to-entry traceability map
- Five-question navigation test
- Revision and escalation panel

## Acceptance checks

- Each procedural entry cites a supplied source section
- The guide carries an owner role and revision date
- Small text and inner margins are reviewed at output size
- A missing task clearly directs readers to the full source
- Safety-sensitive gaps are flagged instead of completed
- Internal information stays within the approved audience scope

## Access, privacy and stop conditions

- The guide is a navigation aid, not a replacement for authoritative procedures
- Available layout tools determine export and accessibility options
- Only approved, sanitized reference material belongs in the draft
- Distribution requires approval of the version and recipient scope

## Two possible extensions

- Build a matching searchable digital reference from approved content
- Prepare a source-owner review form for the next revision
