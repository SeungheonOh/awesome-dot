---
name: polyrhythm-audio-instrument
description: Build a browser polyrhythm instrument with two synchronized pulse counts, audio-clock scheduling, visible phase, reliable stop/reset behavior, and testable rhythm mathematics.
---

# Polyrhythm audio instrument

Build an instrument someone can actually play, rather than a page describing rhythm. The worked product, Pulse Loom, places two evenly divided pulse trains in the same cycle, with independently recognizable synthesized voices and synchronized ring/timeline views.

## Inputs and boundaries

Establish the intended rhythm vocabulary, supported counts, tempo meaning, browser delivery target, and permitted hosting. Synthetic clicks avoid recordings, microphones, uploads, licensing ambiguity, and external audio dependencies. Use explicit user-initiated playback and a modest initial gain. Respect the user's hosting, audience, solo-work, and contribution constraints.

Read the current skills repository before contributing; refresh its default branch before edits and before publication. Keep product code, tests, credentials, deployment files, and logs outside a skills-only contribution.

## Chronological build

1. **Define the time model.** A cycle is four quarter notes at the selected BPM, so `duration = 240 / BPM`. Voice A has a pulses and B has b pulses within that same duration. Label counts as pulses per cycle; calling both counts BPM would misrepresent the rhythm.
2. **Create a pure event generator.** Produce event offsets `i * duration / count`, including zero and excluding the next cycle's endpoint. Sort by time with a deterministic voice tie-break. Keep simultaneous events for both voices; do not deduplicate them as if one were redundant.
3. **Choose the smallest useful controls.** Provide two count selectors, tempo, volume, voice mutes, play/stop, and a few presets. The worked bounds are 2–12 pulses per voice and a displayed 30–180 quarter-note BPM range. Keep the play surface visible immediately.
4. **Use the audio clock for sound.** Create or resume AudioContext inside the Play interaction. Poll a short lookahead scheduler, then schedule oscillator starts against `AudioContext.currentTime`. Keep absolute event time as `origin + cycleIndex * duration + offset`; deriving every note from the last JavaScript callback accumulates timer jitter.
5. **Keep synthesis small and bounded.** Give each voice a distinct timbre/pitch and accent its first pulse. Apply a short attack and decay envelope, start/stop the oscillator at scheduled times, and disconnect ended nodes. Track active sources so stopping playback also cancels notes already scheduled ahead.
6. **Make changes unambiguous.** A simple, dependable policy is to stop when counts, tempo, presets, or mutes change, then require Play to restart. If seamless changes are requested, design boundary scheduling deliberately; do not bolt a second scheduler onto a running first one. Volume can change through a short gain ramp.
7. **Handle interruptions and races.** Stop timers, animation frames, and active sources on Stop or hidden-tab/page-exit events. Invalidate pending asynchronous start requests with a generation counter. Repeated start/stop input must not create multiple loops or allow a delayed resume promise to resurrect stopped playback. Show a recoverable message if audio cannot start.
8. **Draw from the same clock.** Use the audio clock for phase, ring markers, and visual pulse activity; requestAnimationFrame only draws. Do not use animation timing to trigger sound. Explain that hardware/output latency can offset heard audio from the visualization even when scheduling is correct.
9. **Validate model and lifecycle separately.** Exhaustive small-domain numerical checks prove event counts and alignments; DOM tests with a mock AudioContext check lifecycle and UI wiring. Neither proves audible quality, real device latency, or mobile browser behavior. Perform a real listening/interaction check when the environment permits it and report the distinction.
10. **Package for the selected host.** Validate static-asset packaging with the chosen deployment tool. A dry-run is not a deployment. Preserve private audiences during host migration; ask before publishing an existing private app to a public URL. Contribute only the reusable skill, pull current main, inspect the diff, push without overwriting concurrent work, and verify the remote revision.

## Mathematical checks

For integer counts a and b, the number of shared pulse instants per cycle, counting the start but not the duplicated next-cycle endpoint, is `gcd(a,b)`. The event list contains exactly `a+b` events because both voices still sound at those instants.

Useful checks:

- All event offsets lie in `[0, duration)` and are nondecreasing
- Each voice contributes its requested count
- Shared instants match the greatest common divisor within a numerical tolerance
- At 120 BPM, a four-quarter-note cycle lasts two seconds
- Absolute event times remain correct after many cycle indices
- Invalid counts and tempo are rejected before scheduling
- Stop cancels the active sources and scheduling loop
- A tempo/preset change produces a clean stopped state with the new labels
- Returning to a hidden tab does not automatically restart sound

## Evidence from the worked build

All 121 count pairs from 2 through 12 passed event-count, ordering, bounds, coincidence, and absolute-time checks. Invalid settings and JavaScript syntax checks passed. A jsdom test with mocked Web Audio verified explicit start, simultaneous first pulses, source-stop cleanup, tempo-stop, and preset synchronization. Wrangler's static deployment dry-run passed. At contribution time, live Cloudflare publication was pending account authorization/audience setup; actual audio listening and real-browser/mobile behavior remained unverified. Do not inherit these results without rerunning them on another implementation.

## Implementation references

- [MDN: Audio sequencing and lookahead scheduling](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques)
- [MDN: AudioContext currentTime](https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/currentTime)
- [MDN: Web Audio best practices](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Best_practices)

If the sound stutters, first inspect event timing, scheduler duplication, and background-tab behavior. Do not compensate by firing late notes in a burst or increasing gain. If playback permission is unavailable, keep the visual instrument useful and ask the user to start audio explicitly.
