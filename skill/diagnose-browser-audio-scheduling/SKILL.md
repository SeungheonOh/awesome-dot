---
name: diagnose-browser-audio-scheduling
description: "Inspect browser audio timing and lifecycle behavior, identify duplicated or late scheduling, and verify start/stop recovery without changing the composition."
---

# Diagnose browser audio scheduling

## When to use

An authorized browser-audio implementation stutters, drifts, restarts after Stop, or fails during rapid interaction.

## Required inputs

- The relevant scheduling/playback code and a bounded reproduction
- Tempo/event semantics and expected start, stop and edit behavior
- Allowed test runtime and whether audible playback is authorized

## Workflow

1. Trace event generation separately from sound scheduling and visual animation. Establish the expected absolute event times; do not infer them from frame rate.
2. Inspect whether sound uses AudioContext.currentTime and a bounded lookahead horizon. Identify timer-relative accumulation, duplicate loops and bursts of overdue notes after a stall.
3. Check ownership of active sources, timers and pending resume promises. Stop must cancel scheduled voices and invalidate older asynchronous starts. A late failure from an older start must not cancel a newer session.
4. Reproduce rapid Play/Stop, parameter changes, hidden-tab transitions and failed resume. Make authorized fixes at the owning lifecycle boundary rather than increasing gain or hiding errors.
5. Run timing/lifecycle tests separately from a comfortable-level listening check. Explain device latency and browser behavior that a mock cannot establish.

## Output

A short diagnosis with the reproducible sequence, responsible code path, authorized fix if requested, passed checks and remaining audible/device limits.

## Verification and limits

Check that only one scheduler owns playback, Stop silences already-scheduled sources, and stale promises cannot restart or stop a newer session.

## References

[MDN Web Audio sequencing](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques)
