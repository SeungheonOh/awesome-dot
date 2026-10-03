---
name: verify-generated-midi
description: Verify the actual downloaded MIDI export against a supplied score contract using an independent reader, checking timing, track structure and note-event balance. Use for sequencer or sonification exports, not audio quality assessment or automatic DAW compatibility claims.
---

# Verify a generated MIDI export

## When to use

Use when an application says it exported a score and the user needs evidence that the delivered MIDI contains the intended timed events. Separate successful byte generation, completed download, structural validity, musical content and playback in a target application.

## Required inputs

- The authorized export workflow or local MIDI file
- The score contract: expected duration, tempo policy, track/channel arrangement, note counts or event ledger
- The exact corresponding score-data snapshot, if the export has one
- An installed independent MIDI reader and the authorized verification scope

A MIDI file describes events; it is not an audio recording. Do not promise timbre, loudness, subjective quality or device-specific instrument playback from a file parse alone.

## Workflow

### 1. Capture the delivered artifact

For a browser export, establish the selected score and its source timestamp before clicking. Register the supported download listener before the action, then wait for the completed local download path. A UI toast or creation of a Blob is not proof that a file reached the download destination.

If a previous attempt timed out, distinguish that missing evidence from a known failure of the exporter. Retry only within authorization and a bounded plan. Do not claim a new live-data export reproduces an older score: pair it with the newly selected snapshot and timestamp.

Copy a completed download to an approved verification directory without overwriting earlier evidence. Record byte size and digest. Keep the corresponding score snapshot separate; a same-named JSON file from another run can produce misleading comparisons.

### 2. Open it with an independent reader

Use a parser separate from the writer being checked. Record its version and the file's format type, track count and timing division. Do not treat the filename extension or successful writer tests as independent validation.

For a narrow type-1, ticks-per-quarter-note contract, confirm those declarations match. Do not apply the same duration calculation blindly to independent type-2 patterns or SMPTE-based timing. If the reader or verification code does not support the file's timing mode, report that gap rather than forcing it into the expected profile.

### 3. Reconcile event time

In each file track, validate nonnegative delta times and accumulate them to absolute tick positions. Convert time through the actual tempo map using a reader that handles the declared timing mode; a single BPM conversion is insufficient if tempo changes occur.

Compare total duration and relevant event positions against the score contract with an explicit tolerance justified by tick resolution or declared rounding. Preserve intentional silent tails: the final note-off time and the file's declared ending can differ. Do not trim the file merely to make a measured duration match a display label.

### 4. Check note lifecycle and expected content

Count positive-velocity note-on events. Recognize note-on with zero velocity as a note release when interpreting ordinary MIDI note messages. Reconcile releases by channel and pitch, checking for unmatched releases and remaining active notes under the writer's declared event model.

For a generator that owns complete independent note pairs per track, a per-track active-count check is useful. Do not generalize it to every imported MIDI: cross-track channel sharing, overlapping same-pitch notes, sustain controls and other controller semantics can require a merged timeline and a richer state model. Note-event balance alone does not establish audible silence or musical correctness.

Compare the count and, when available, the actual pitch/start/duration/channel ledger with the score data. An equal total count can conceal changed pitches or timing, so state precisely which content comparison was performed.

### 5. Report the narrow verified result

Keep these statuses separate:

- Writer returned bytes
- Browser download completed
- Independent parser opened the exact downloaded file
- Structural/timing/event checks matched the declared contract
- Target DAW/device import or subjective listening was tested, or remains untested

Preserve the original and evidence. Do not submit private scores to online converters or upload them to a target service without the required authorization. A successful local parse does not establish acceptance by a particular DAW version.

## Worked example

A live-data score displays a 60-second duration at 96 BPM. Its matching snapshot records 24 melody notes and three percussion notes. The browser's completed downloads produce one MIDI file and its score JSON from the same selected run.

An independent reader finds type 1, three tracks, 480 ticks per quarter note, exactly 60 seconds and 27 positive-velocity note-ons. Per-track note releases balance without negative active counts under this generator's note-pair contract. The expected total is 24 + 3 = 27.

The conclusion is that this downloaded candidate passed the stated structure, duration and note-count checks. It does not establish that every pitch matches a source ledger, that the music sounds good, or that a DAW imported it. An earlier download-listener timeout remains an earlier inconclusive attempt; the later completed download supplies new evidence.

## Reference and evidence

The worked flow was exercised on actual browser-downloaded MIDI and score-data files, read independently with Mido. See [Mido's standard MIDI file documentation](https://mido.github.io/mido/files/midi.html) and [message documentation](https://mido.github.io/mido/messages/index.html) for the reader's file and delta-time interfaces. Recheck library behavior for the installed version and the timing mode in use.
