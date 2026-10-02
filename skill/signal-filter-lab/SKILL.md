---
name: signal-filter-lab
description: Build an interactive browser laboratory for synthetic waveforms, digital filtering, and paired time/frequency plots, with reproducible numerical checks and clear model limits.
---

# Signal filter lab

Build a working learning instrument: users change a signal, apply a filter, and compare the same samples in time and frequency. Keep the product in its own workspace; this contribution contains the reusable method only.

## Inputs and boundaries

Establish the audience, learning question, desired controls, hosting destination, and contribution scope. A useful default is a beginner exploring which parts of a noisy signal survive a filter. Synthetic data avoids microphone permissions, private recordings, API dependencies, and source ambiguity. Do not add recording, uploads, or external analysis unless requested. Respect explicit solo-work and service restrictions.

## Chronological build procedure

1. Read the current repository guidance and the user's instructions. Refresh main before authoring and before publication. If the user asks for skills only, keep app source, tests, screenshots, deployment metadata, and build diaries outside that repository even if its general guide permits them.
2. Choose one observable question per experiment. Start with cleaning a noisy slow tone, separating low and high tones, and smoothing a square wave. Each preset must set all relevant controls so earlier experiments cannot contaminate it.
3. Isolate pure signal functions before building the interface. Generate a fixed observation window, deterministic pseudorandom noise, filter output, spectrum, RMS, and peak frequency. Use one configuration object for controls and computation. Changing the noise seed should be explicit; slider edits should not silently draw a new random realization.
4. Choose and expose the sampling model. The worked implementation uses 512 samples at 256 Hz, a two-second window, 0.5 Hz frequency bins, and a 128 Hz Nyquist limit. Keep editable sine frequencies below Nyquist. Explain that sampled square and triangle waves contain higher harmonics that may alias.
5. Implement a small honest filter set: bypass, a first-order low-pass, a first-order high-pass, and a causal moving average. Label an RC-derived cutoff as a design setting rather than a calibrated digital −3 dB frequency. Include startup transients; do not silently trim them from one view but keep them in another.
6. Build the actual instrument surface. Put source and filter controls beside a dominant time plot, with a spectrum and numerical readouts immediately below. Use consistent input/output colors, text legends, visible units, and accessible control labels. Scale both traces on a plot together; independently autoscaling them would conceal attenuation. Resize the canvas backing store for the display pixel ratio without changing the samples.
7. Wire complete recovery paths. Presets, reset, noise regeneration, filter-specific controls, and an input-trace toggle should update the same model. Hide irrelevant controls rather than leaving an inactive cutoff visually authoritative. Keep field-guide explanations secondary to experimentation.
8. Test numerical invariants, then inspect interactions when a supported browser is available. Fix failures before deployment. Distinguish floating-point roundoff from a model bug; choose a justified tolerance, or make mathematically exact special cases exact. In this build a one-sample average became a direct copy and high-pass startup state was initialized to zero.
9. Publish with the chosen service, preserving its authorized audience. Verify terminal deployment success. Extract the reusable chronology, formulas, pitfalls, and acceptance criteria into a skill, rather than copying the product into the contribution. Review the final diff and verify the remote commit after pushing. Reconcile concurrent main changes without force-pushing.

## Numerical contract

For sample period `dt = 1 / fs` and design setting `fc`, let `rc = 1 / (2πfc)`.

- Low-pass: `a = dt / (rc + dt)`; `y[n] = y[n−1] + a(x[n] − y[n−1])`; initialize `y[0] = x[0]`
- High-pass: `b = rc / (rc + dt)`; `y[n] = b(y[n−1] + x[n] − x[n−1])`; initialize `y[0] = 0`
- Causal average: mean of the latest `min(n+1, window)` samples; a window of one returns an unchanged copy
- RMS: `sqrt(mean(x²))`; level change: `20 log10(output RMS / input RMS)`, with an explicit zero-input/output branch
- Spectrum: remove the mean, multiply by the Hann window `0.5 − 0.5 cos(2πn/(N−1))`, calculate the DFT, and scale interior positive-frequency magnitudes by `2 / sum(window)`. If DC or Nyquist bins are displayed, use their appropriate undoubled scaling instead

Do not call the spectrum a power density: it is an amplitude estimate. Peak frequency is a bin estimate, not an exact measurement. A lower RMS does not prove better signal quality. A smoothed trace can also be attenuated and delayed.

## Acceptance checks

- Identical settings and seed yield identical input samples; changing only the seed changes noisy samples
- Bypass preserves every sample; a one-sample average preserves every sample
- Constant input remains constant through the low-pass and becomes zero through the high-pass under the stated initialization
- A unit-amplitude 8 Hz sine at the stated sample rate/window peaks at 8 Hz, with estimated amplitude within 0.001 of one
- At the same low-pass setting, a 4 Hz sine retains more RMS than a 60 Hz sine
- Every combination of the supported waveform/filter types returns finite values at control extremes
- Reset restores source, filter, seed, and trace-visibility defaults; presets overwrite all intended settings
- Keyboard, mobile, 200% text sizing, plot labels, and resize behavior are checked in a real browser when available

The original Signal Foundry build passed the numerical checks above, including 12 waveform/filter edge combinations and JavaScript syntax validation. Its deployment reached success, and a hosting-provided desktop screenshot was inspected. Full browser interaction, mobile visual, and optional WebMCP execution checks were unavailable in that environment; those remain explicit verification limits, not inherited passes for future implementations.

## Failure and stopping conditions

If spectra look wrong, verify frequency-bin mapping, window normalization, and common axis scaling before styling. If filters produce invalid values, validate sample rate, cutoff, and window bounds before rendering. If a browser or publishing step is unavailable, retain the tested local product and state the exact unverified stage. Never portray synthetic examples as real measurements or this educational instrument as calibrated engineering equipment.

A completed product and skill are one iteration. If the user requested ongoing creation, continue to the next distinct useful product within the same authorized scope; a successful first release is not a stopping instruction.
