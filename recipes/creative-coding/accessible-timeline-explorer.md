---
id: accessible-timeline-explorer
title: "Accessible Timeline Explorer"
summary: "Build a timeline that preserves date uncertainty and offers equivalent visual and list navigation."
category: creative-coding
level: intermediate
timebox_minutes: 180
capabilities: ["code", "files"]
tags: ["timeline", "accessibility", "data-visualization"]
status: recipe-not-run
---

# Accessible Timeline Explorer

Build a timeline that preserves date uncertainty and offers equivalent visual and list navigation.

## Scenario

A team wants to explain a sanitized project history to new colleagues. Some events have exact dates, some span a month, and a few have no confirmed date. You need an interactive timeline that shows those differences honestly and remains usable by someone who prefers a text list.

## Inputs to prepare

- Sanitized events with titles, descriptions, sources, and unique identifiers
- Date precision for each event, including ranges and unknown dates
- Optional categories, filter priorities, and the intended timezone
- Target devices and the permitted preview or publication audience

## Copy this prompt into dot

```text
dot, build an accessible timeline explorer for [SANITIZED EVENT DATA] aimed at [AUDIENCE]. Begin by reviewing the event structure and explaining the smallest useful version in plain language. Keep exact dates, month-only dates, ranges, and unknown dates distinct. Use [TIMEZONE] for supplied times and ask about ambiguous date strings rather than silently guessing. Do not invent missing milestones or source references.

Provide a visual timeline and an equivalent chronological list with the same filters, selected event, and detail content. Include category filters, a text search, a clear reset action, and a visible count of matching events. Keep unknown-date events in a labeled section instead of placing them at a fabricated point. Use accessible labels, visible keyboard focus, and a layout that works on [TARGET DEVICES]. Avoid color-only categories and motion-dependent navigation.

Deliver source files, a fictional sample dataset, a data-format guide, launch instructions, and a test log. Execute checks only where the available environment supports them and clearly mark all others not run. Test duplicate dates, overlapping ranges, no matching events, missing dates, malformed input, and keyboard-only use. Display imported descriptions as text, not executable markup. Keep the sample free of confidential project information, credentials, and personal records. Do not publish or connect internal systems until I approve the exact data, audience, and destination.
```

## Iterate with a purpose

### 1. Add uncertainty controls

```text
Add a filter for exact, approximate, range, and unknown dates, and verify that filtering does not imply precision the source lacks.
```

### 2. Create a printable history

```text
Generate a print-friendly list with event sources and date-precision labels, keeping the same filter state visible in its heading.
```

### 3. Validate imported data

```text
Add clear, non-destructive validation for duplicate identifiers, reversed ranges, unsupported date formats, and missing titles before replacing the current dataset.
```

## Expected deliverables

- Timeline and equivalent list-view project
- Fictional sample event dataset
- Date-precision and data-format guide
- Keyboard and edge-case test record
- Private preview if supported

## Acceptance checks

- Visual and list views expose the same event content
- Unknown dates are never assigned fabricated positions
- Overlapping ranges and duplicate dates remain selectable
- An empty filter result includes a clear reset path
- Ambiguous and malformed dates produce readable errors
- Categories have text labels as well as color

## Access, privacy and stop conditions

- Code execution and private previews depend on available tools
- The source data, not the visualization, determines historical accuracy
- Confidential or personal event data requires a defined access boundary
- Publication and internal-system connections need separate approval

## Two possible extensions

- Add source-reference footnotes to a printable report
- Compare two sanitized timelines without merging uncertain dates
