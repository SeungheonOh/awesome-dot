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

### Capture the smallest lifecycle trace

Record actions and promise resolutions with session/generation identifiers, audio-clock times and source ownership. Do not rely solely on console logs that say “playing.” Check which sources were actually scheduled and cancelled. Keep the reproduction synthetic when possible; microphone capture and private recordings are not necessary for a start/stop race.

If a code change is authorized, first freeze the failing sequence as a test. Ensure cleanup belongs to the session being cleaned up. A global error handler that stops whichever session is current can reproduce the same race in another form.

## Output

A short diagnosis with the reproducible sequence, responsible code path, authorized fix if requested, passed checks and remaining audible/device limits.

## Verification and limits

Check that only one scheduler owns playback, Stop silences already-scheduled sources, and stale promises cannot restart or stop a newer session.

## References

[MDN Web Audio sequencing](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API/Advanced_techniques)

## Handoff checklist

Name the action sequence, expected ownership, observed divergence and exact test result. If audible playback is unavailable, deliver the diagnosis and lifecycle evidence without claiming to have listened.

## Worked example

The supplied trace is: Play starts session A; AudioContext.resume remains pending; Stop invalidatesA; Play starts session B and schedules its first notes; thenA’s resume promise rejects. The observed bug is thatA’s catch handler calls a global Stop and silencesB.

The diagnosis is stale-session cleanup, not an incorrect tempo. The proposed authorized fix checksA’s generation before changing current playback and cleans up onlyA-owned sources. The regression reproduces this exact resolution order and requiresB to remain active. A separate test resolvesA successfully after Stop and requires no restarted sources.

Mocked promise/source tests establish lifecycle behavior for this sequence. The report still leaves real-device latency and audible quality unverified until those checks are performed.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
