---
name: local-subtitle-timing-bench
description: Build a local SRT caption timing editor with offset and two-anchor calibration, reversible cue edits, overlap diagnostics and new-copy export. Use for subtitle timing tools, not speech transcription or automatic media synchronization.
---

# Local subtitle timing bench

Make timing edits inspectable and reversible. Without media playback or a user-supplied synchronization observation, a timing tool cannot claim that captions match spoken audio.

## Build in this order

1. Define the supported subtitle subset before parsing. A narrow SRT implementation can require numeric indices, millisecond start/end times, and nonempty multiline captions. Reject positioning metadata and unsupported blank caption lines explicitly instead of dropping them. Decode UTF-8 fatally, normalize line endings, bound bytes and cue count, and preserve the current working document when an import fails. Explain any whitespace normalization and renumbering on export.
2. Use integer milliseconds internally. Validate minute/second ranges, finite values, positive duration, and an explicit maximum timestamp. Keep stable internal cue IDs separate from source sequence labels. Export in retained source order with fresh sequential indices; never silently sort cues.
3. Implement timing transformations as pure functions returning a new validated document. Offset moves both ends equally. Two-anchor calibration uses scale=(targetB−targetA)/(sourceB−sourceA) and offset=targetA−sourceA×scale. Require increasing anchors on both timelines, constrain unreasonable scale, and round each final endpoint once to milliseconds. Explain that scaling also changes durations and applies to the current working track.
4. Reject the entire transformation if any cue becomes negative, collapses to zero duration or exceeds the supported timestamp range. Do not silently clamp early cues to zero or partially apply a mapping. Retain the imported baseline and bounded immutable undo snapshots independently.
5. Separate review hints from correctness errors. Overlap, reading density and short duration can be intentional. Detect temporal overlap using a time-sorted copy, then map flags back to original IDs. Comparing only adjacent source rows misses nested overlaps; comparing a source-order maximum end falsely flags disjoint earlier cues. Flag both sides of a real overlap. Preserve source ordering in presentation/export and report out-of-order cues separately.
6. Keep text inert in the editor. Display caption markup literally with textContent, retain it in SRT output, and document whether density estimation strips tags. Avoid using subtitle text as HTML. Treat character-per-second thresholds as configurable heuristics, not accessibility certification.
7. Protect unfinished edits and delayed imports. Disable exports while a cue draft is open, require Save or Cancel before switching cues, and validate before creating an undo snapshot. Use an import generation counter so an older file read cannot overwrite a newer sample/import. A decoding failure must not clear the valid track.
8. Render bounded pages of cues rather than thousands of editable nodes. Show exact start/end values, review flags, filter state and page counts. Provide keyboard-visible focus, labeled form controls, and a status region. Imported content stays in memory unless the user explicitly requests persistence.
9. Export a new SRT copy and optionally an edit record containing original cues, current cues and transformation history. Such a record contains caption text and can be sensitive; label it accordingly. A download click is a request, not proof that a device saved the file.

## Verification

Round-trip parsed fixtures through serialization, while accounting for deliberate index and newline normalization. Test BOM/CRLF, multi-hour timestamps, malformed ranges, zero duration, missing captions, unsupported metadata, markup-like text and invalid UTF-8. Compare many transformed endpoints to an independent arithmetic expression and verify both anchor equations. Include disjoint out-of-order cues, nested overlaps and exact touching endpoints.

Interaction checks should exercise offset, rejected negative shifts, Undo, reset-to-import, draft export suppression, literal text rendering, filters, pagination, import supersession and failed-import preservation. Test downloads' actual serialized bytes through a captured Blob. Real-browser checks are still needed for responsive layout, keyboard interaction and actual downloaded-file behavior; simulated DOM tests do not prove those.

## Worked implementation

Cue Loom supported UTF-8 SRT up to 2 MiB and 5,000 cues, timestamps below 100 hours, scale 0.5–2, 25 undo snapshots and 40-row pages. Its pure-model tests passed 1,000 timestamp/mapping cases, anchor checks, invalid-input cases and overlap cases. Simulated-DOM tests passed edit/export/reset/filter flows, literal markup handling, delayed-import supersession and failed UTF-8 preservation. Actual browser layout, saved download bytes and synchronization with real media remained unverified.

Deliver the app and tests separately. A skills-only repository contribution should contain this reusable workflow, not the product, fixture files or build log. Publication needs the user's chosen destination and authorization.
