---
id: data-sonification-score
title: "Data Sonification Score"
summary: "Turn a small sanitized time series into a documented, repeatable audio score with a visual companion."
category: creative-coding
level: advanced
timebox_minutes: 150
capabilities: ["code", "files", "websites"]
tags: ["sonification", "data-mapping", "audio"]
status: recipe-not-run
---

# Data Sonification Score

Turn a small sanitized time series into a documented, repeatable audio score with a visual companion.

## Scenario

A data-minded musician wants to hear patterns in a small fictional sensor series. Sonification can make repetition and gaps noticeable, but arbitrary mappings can also create misleading impressions. The project should expose its choices, retain the original values, and give listeners a visual and textual way to inspect the same information.

## Inputs to prepare

- [SANITIZED CSV] with time and numeric value columns
- [MISSING-VALUE POLICY] and outlier treatment
- [PITCH RANGE] and finite playback duration
- [COMPARISON SERIES] if one is needed

## Copy this prompt into dot

```text
dot, create a data-sonification study from [SANITIZED CSV], [MISSING-VALUE POLICY], [PITCH RANGE], and [COMPARISON SERIES]. Use available Python or browser coding tools for parsing and a supported local audio engine for synthesis. Do not upload the dataset to an external audio service. If audio generation is unavailable, deliver the mapping specification and event data without claiming a playable score.

First summarize column names, units, ordering, missing values, and numeric ranges. Propose one explicit mapping from time to note onset and value to pitch, then let me approve it before generating a full score. Keep normalization consistent across compared series; disclose clipping, aggregation, and transformed scales. Represent missing values according to the chosen policy rather than silently turning them into zero.

Deliver editable source, a mapping manifest, note-event CSV or JSON, and a synchronized visual or text timeline. Target WAV export only if the available toolchain can generate and reopen it successfully. Provide explicit play, stop, mute, and bounded-volume controls for any preview. Test constant values, all-missing input, unsorted timestamps, duplicates, extreme outliers, and an empty file. Confirm that identical inputs produce identical events. Explain that musical impressions do not establish causation or statistical significance. Use fictional or sanitized data and ask before publication or external sharing; identify unexecuted audio checks.
```

## Iterate with a purpose

### 1. Compare mapping choices

```text
Create two documented pitch mappings from the same unchanged data and ask listeners to compare them without implying that one reveals a truer pattern.
```

### 2. Add a reference channel

```text
Add a quiet reference pulse or tone with a visible legend, then verify that it is distinguishable from measured values and missing-data markers.
```

### 3. Prepare an interpretation note

```text
Write a concise companion note separating observed data properties, chosen musical encodings, and subjective listening impressions, with links to the supplied data provenance if available.
```

## Expected deliverables

- Validated input summary and mapping manifest
- Editable parsing and synthesis source
- Deterministic note-event CSV or JSON
- Visual or text companion timeline
- WAV output only if generated and reopened successfully
- Edge-case and interpretation-limit report

## Acceptance checks

- Input values and units remain traceable through the event mapping
- Compared series use the same disclosed normalization unless an explicit alternative is labeled
- Constant-value data produces the documented constant-pitch behavior
- All-missing and empty inputs produce explanations rather than misleading audio
- Duplicate and unsorted timestamps follow an explicit documented policy
- Identical validated inputs and settings reproduce identical note events
- Audio preview starts only after interaction and stops completely when requested

## Access, privacy and stop conditions

- Audio generation and WAV export depend on the available toolchain
- Sound patterns are not evidence of causation, significance, or medical conclusions
- Use sanitized data and avoid transmitting private datasets to external services
- Publication, external sharing, and additional audio dependencies require approval

## Two possible extensions

- Create a listening worksheet that includes the visual data alongside the sound
- Explore a second variable only after documenting how listeners can distinguish its encoding
