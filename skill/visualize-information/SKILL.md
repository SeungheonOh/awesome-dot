---
name: visualize-information
description: Create or improve a chart, process diagram, timeline, or system diagram that communicates supplied or established information. Use when the visual itself is the deliverable, with a readable export and supporting data or relationships; discovering an answer from data, producing a whole presentation, and writing a technical guide are separate primary tasks.
---

# Visualize Information

Deliver a finished visual that helps its reader answer a specific question. Include the requested output format, a readable preview, and the data or relationships needed to understand and revise it. A recommendation for a chart type or unrendered source alone is not a finished visual.

Use this workflow to communicate information whose meaning is already established. Bounded calculations and grouping needed to draw the visual belong here. Discovering why a metric changed, testing an explanation, or deciding what the data supports is the primary work of `analyze-data-question`. A whole presentation belongs to `source-backed-presentation`; technical documentation with a supporting diagram belongs to `write-technical-guide`. For other documents, keep the appropriate writing or editing workflow primary. A visual can support those larger tasks without replacing their deliverable.

## Start from the reader's question

Establish what the reader should be able to compare, locate, follow, or explain after seeing the visual. Use the request to infer audience, setting, and level of detail. Ask only when an unresolved choice would materially change the meaning or usability, such as an unknown rate denominator or whether a system diagram describes the current system or a proposed one.

Honor a requested form, medium, template, or notation. If it cannot faithfully express the information, explain the specific problem and choose a compatible correction or ask about the material tradeoff. Choose the visual from the question when the form is open:

- Comparisons need a shared reference; trends need ordered time; distributions need the spread, not merely a summary value; composition needs an explicit whole
- Processes need steps, decisions, handoffs, and paths; timelines need events or intervals and their temporal relationship; system diagrams need components, boundaries, and meaningful connections

Use multiple coordinated panels or a focused overview plus detail when one crowded view obscures the answer. Do not add interactivity, decoration, or extra categories unless they help the intended reader. Interactivity is an option when available and useful, not a completion requirement.

Check the tools and rendering capabilities actually available before choosing the production method. Select a suitable authoring method for the requested output and expected revisions. Do not promise a native editable format, embedded interaction, or an export that the environment cannot produce.

## Establish what will be encoded

Read the relevant supplied material and preserve its source, scope, date or version when known. Keep a compact representation of the information the visual uses: plotted values and definitions for a chart, or entities, events, connections, and conditions for a diagram. This representation should be sufficient to check the visible claims without reverse-engineering the image.

Resolve inconsistent names, units, and dates using evidence. Do not silently collapse distinct entities or interpret a missing relationship as proof that none exists. Preserve disagreements and uncertainty when the sources do not settle them. Label inferred or proposed elements where the reader encounters them; a polished appearance must not turn a suggestion into an observed fact.

Apply only transformations needed for the requested communication. Record material filtering, grouping, calculations, exclusions, and ordering. If those choices require discovering a substantive answer, pause that part of the visual and establish the answer rather than choosing a convenient-looking result.

## For charts: preserve quantitative meaning

Identify the unit of observation, metric, population, time window, and units. For rates, retain numerator and denominator or their definitions and supporting counts. Keep denominators aligned across comparisons, or make the difference explicit. Do not average group percentages as if groups were equally sized unless that weighting is intended. Label incomplete periods, changes in definition, and unequal exposure where they affect interpretation.

Distinguish missing, zero, not applicable, suppressed, and estimated values. Use a gap or an explained encoding for unknown values; do not plot them as zero or silently connect through them. Do not create confidence intervals, projections, or interpolated observations without a basis. Show supplied uncertainty in a form whose meaning is clear, including what an interval represents.

Choose encodings whose geometry matches the quantity. When bar length encodes an absolute magnitude, start at zero. For ranges, durations, or changes, make endpoints clear so a floating bar is not mistaken for an absolute value. Position-based plots may use a narrower range when it serves the question and the scale is clear. Explain logarithmic scales and axis breaks; do not hide a discontinuity. When area encodes magnitude, scale area rather than radius. Avoid perspective or decorative volume that changes apparent values.

Keep scales comparable across panels intended for direct comparison, or visibly label the difference. Use a second axis only when its meaning and relationship are defensible; independently chosen scales can manufacture apparent agreement. Preserve chronological or intrinsic category order. Sorting by magnitude can help a ranking question but should not erase an ordered scale or imply a sequence that does not exist.

For composition, verify the whole and whether categories overlap or omit an unknown share. Do not force incomplete or overlapping values into a 100% total. Keep rounding consistent with source precision and avoid labels that falsely suggest reconciliation. Place qualifications where a reader will see them, not only in a separate explanatory file.

## For diagrams: preserve relationship meaning

Define what nodes, containers, lines, arrows, and spatial grouping mean before arranging them. An arrow may indicate execution order, a message, a dependency, ownership, or a proposed transition; these meanings are not interchangeable. Preserve direction and endpoints from the evidence. Distinguish relationship types with labels or an explicit legend when they coexist.

For a process, keep entry and exit conditions, decision branches, return paths, and consequential exceptions visible at the chosen level of detail. Label branches with the condition that selects them. A numbered list or left-to-right layout should not imply that concurrent or optional work is always sequential. Do not invent a successful terminal state when a path remains unresolved.

For a timeline, distinguish point events from durations and preserve chronological order, timezone, date precision, and uncertainty as relevant. Position events proportionally when distance represents elapsed time. If using evenly spaced milestones to communicate order, make clear that spacing does not represent duration. Do not give a rough date the apparent precision of a known timestamp.

For a system diagram, use boundaries only for a supported distinction such as ownership, deployment, trust, or logical grouping. Label which distinction applies. Separate observed architecture from proposed design, using distinct views or clearly keyed markings. Do not infer data movement, causal influence, or a security guarantee merely from proximity or a shared container.

Reduce crossings and route connectors so their endpoints are unambiguous. Use junctions only for actual joins; a crossing must not accidentally create a connection. Keep repeated entities identifiable, and label aliases or repeated instances when they aid readability. If a simplified view omits a meaningful path or component, state the scope rather than letting absence suggest it does not exist.

## Render, inspect, and deliver

Set layout and text size for the actual reading context, such as an embedded document, printed page, screen, or large display. There is no universal canvas size or library. Use legible labels, sufficient contrast, and redundant cues when color distinguishes essential categories or states. Provide a short text explanation of the visual's main relationships or message so the image is not the only way to access them.

Export using the available tools and inspect the actual delivered output at its intended display size. Source code, a successful export command, or a thumbnail is not evidence that the result is readable. Check for clipped or overlapping text, substituted fonts, missing marks or arrowheads, ambiguous connectors, illegible notes, and export changes to scales or layout. When a preview and final format differ, inspect the final format too when possible; the preview does not prove that a separate export survived intact.

Check semantic accuracy as well as appearance. Compare plotted values, totals, labels, and scale endpoints against the retained data. Trace diagram paths and connection directions against the retained relationships, including exceptions and uncertainty. Revise and re-export when inspection reveals a problem.

Deliver the visual in the requested format, with a preview the recipient can open. Include editable source when requested or when revision is a reasonable part of the handoff; use a genuine authoring representation, not merely an image pasted into an editable container. Supply the plotted data or relationship list and the material definitions and transformations, without unnecessarily duplicating unrelated source records. Keep source and export consistent after revisions.

If the environment cannot render or inspect the requested format, use an available compatible route where possible. Otherwise deliver the supported portion and identify the exact missing export or unverified rendering. Do not claim to have visually checked an artifact that was never opened or rendered. Briefly state what the visual communicates, the checks performed, and any limitation that changes how it should be read.
