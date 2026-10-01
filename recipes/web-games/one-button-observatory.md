---
id: one-button-observatory
title: "One-Button Observatory Rhythm Game"
summary: "Build an approachable timing game with calibration, adjustable speed, and a non-timed practice mode."
category: web-games
level: intermediate
timebox_minutes: 90
capabilities: ["code", "files", "websites"]
tags: ["rhythm", "single-input", "accessibility"]
status: recipe-not-run
---

# One-Button Observatory Rhythm Game

Build an approachable timing game with calibration, adjustable speed, and a non-timed practice mode.

## Scenario

A maker event needs a game that can be played with one large button or a keyboard key. Players align telescope shutters with repeating signals. Different devices introduce different delays, so the prototype needs a clear calibration step and a way to enjoy the pattern without tight timing.

## Inputs to prepare

- [INPUT KEY] and optional touch target size
- [PATTERN LENGTH] and number of rounds
- [TEMPO RANGE] and hit-window options
- [AUDIO PREFERENCE] and reduced-motion preference

## Copy this prompt into dot

```text
dot, help me build One-Button Observatory using [INPUT KEY], [PATTERN LENGTH], [TEMPO RANGE], and [AUDIO PREFERENCE]. Use available coding and browser tools, and tell me which timing checks can actually be measured in that environment. Start with a silent visual prototype before adding optional synthesized sound.

Players press one control when a moving marker aligns with a telescope shutter. Use a finite sequence, a visible hit window, and a documented score rule. Reaching the selected accuracy target wins; finishing below it ends the round with a neutral summary and retry button. Include calibration, pause, speed adjustment, large touch controls, and an untimed step mode that teaches the identical pattern without competitive scoring. Audio must be optional and begin only after user interaction. Avoid flashes and provide a stationary-cue alternative to sweeping motion.

Deliver editable source, original pattern data, controls, and a test log. Test held keys, double presses, background-tab suspension, muted playback, and restart midway through a round. Explain how timing uses elapsed timestamps rather than frame counts. Separate visual, input, and audio latency caveats rather than promising universal synchronization. Keep results on-device by default; ask before publishing, collecting player data, or using copyrighted recordings. Show which win, failure, and reset checks remain unverified.
```

## Iterate with a purpose

### 1. Add adaptable practice

```text
Add a practice session that lets the player select a wider timing window or slower tempo after each round without labeling either choice as failure.
```

### 2. Create original patterns

```text
Create three original rhythm-pattern packs and a local editor that validates duration, tempo, and overlapping cues.
```

### 3. Inspect input timing

```text
Add an opt-in local diagnostic view showing target and press timestamps, with export and delete controls and no network transmission.
```

## Expected deliverables

- Single-input game with silent and optional audio modes
- Original finite patterns and scoring specification
- Calibration and accessibility instructions
- Input, pause, outcome, and restart test log

## Acceptance checks

- Reaching the configured accuracy target produces a win at the end of the finite sequence
- A lower result shows a readable summary and a usable retry control
- Holding the input key does not score multiple hits for one cue
- Untimed step mode preserves cue order and disables competitive accuracy scoring
- Background suspension does not count hidden cues as misses
- Restart cancels pending cues and resets score, sequence position, and calibration choice as documented
- All audio can be muted without hiding required information

## Access, privacy and stop conditions

- Browser and device latency prevent guarantees of music-grade timing accuracy
- Synthesized audio still requires user interaction and supported playback
- No copyrighted recordings or external player-data collection without approval
- A one-button control scheme may still need individual accessibility testing

## Two possible extensions

- Support an available standard gamepad with remappable input
- Produce a facilitator checklist for accessible event hardware
