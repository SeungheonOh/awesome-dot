---
id: echo-beacon
title: "Echo Beacon Memory Game"
summary: "Make a multimodal sequence-memory game with adjustable pacing and equivalent non-audio play."
category: web-games
level: beginner
timebox_minutes: 60
capabilities: ["code", "files", "websites"]
tags: ["memory", "audio", "inclusive-play"]
status: recipe-not-run
---

# Echo Beacon Memory Game

Make a multimodal sequence-memory game with adjustable pacing and equivalent non-audio play.

## Scenario

A family game night includes people who prefer visual play and someone who cannot rely on sound cues. A memory game should let everyone use the same rule set through different cues. The host wants adjustable sequence length, clear mistakes, and no punishment for taking time to find a control.

## Inputs to prepare

- [BEACON COUNT] between three and eight
- [START LENGTH] and [GOAL LENGTH]
- [CUE DURATION] and pause between cues
- [INPUT MODES] and a non-flashing palette

## Copy this prompt into dot

```text
dot, build Echo Beacon as a compact browser memory game if a suitable coding environment is available. Use [BEACON COUNT], [START LENGTH], [GOAL LENGTH], [CUE DURATION], and [INPUT MODES]. Explain the sequence-generation rule and the difference between demonstration and answer phases before implementation.

The game demonstrates a sequence of labeled beacons, then the player repeats it. Each correct round extends the sequence by one item until the goal length is reached. A wrong item ends the attempt with the expected and selected labels; offer replay of that round and a full reset. Provide visual-only, audio-plus-visual, and text-sequence practice modes. Audio must start only after an explicit interaction, have a mute control, and never carry information absent from the visual interface. Avoid rapid flashing and allow unlimited answer time.

Deliver editable source, a short control guide, a deterministic test seed, and a verification checklist. Test repeated identical beacons, double-click prevention, key repeats, muted playback, background-tab interruption, and goal lengths equal to the starting length. Define whether an interrupted demonstration restarts or pauses and show that choice clearly. Keep score on-device only if I opt in. Ask before publishing or adding accounts, external audio, or tracking. Distinguish tested behavior from intended behavior.
```

## Iterate with a purpose

### 1. Add a practice ladder

```text
Add a practice ladder that changes one difficulty variable at a time and lets players replay a chosen length without score pressure.
```

### 2. Create custom cue sets

```text
Allow local selection of symbol sets and optional synthesized tones, with a preview that checks labels remain unique.
```

### 3. Compare recall strategies

```text
Add a noncompetitive local session summary showing sequence lengths attempted and selected cue mode, with a delete-session control.
```

## Expected deliverables

- Editable memory-game source
- Accessible cue and control guide
- Seeded example sequences including repeated items
- Verification checklist and any untested conditions

## Acceptance checks

- Correctly repeating a sequence at goal length produces a win
- A wrong input reports an error without relying on sound or color
- Repeated adjacent beacons are visibly separated during demonstration
- Holding a key does not accidentally submit repeated answers
- Muted play retains all information required to complete a round
- Reset during demonstration cancels outstanding cues and clears progress
- Background interruption follows the documented pause or restart behavior

## Access, privacy and stop conditions

- Browser audio requires user interaction and device support
- Performance is a game score, not a cognitive or medical assessment
- Do not collect personal performance data or publish without approval

## Two possible extensions

- Add a shared-device alternating-turn mode
- Produce a printable symbol-sequence version
