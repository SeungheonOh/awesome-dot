---
name: compare-sampled-signal-filters
description: "Compare candidate digital filters using shared samples, declared initialization, time traces and correctly normalized amplitude spectra."
---

# Compare filters on the same sampled signal

## When to use

A user needs to choose or inspect a filter without confusing attenuation, smoothing, phase delay and improved signal quality.

## Required inputs

- Authorized samples and sampling rate, or an explicitly labeled synthetic signal specification
- Candidate filter definitions, parameters and initial-state rules
- The question to evaluate and any acceptable delay or distortion constraints

## Workflow

1. Validate finite samples, uniform timing and sampling rate. If using synthetic noise, keep one seed across candidates so the comparison changes only the filter.
2. Apply every candidate to the same samples, preserving startup transients unless the user specifies an equal exclusion interval. Distinguish an RC-derived design setting from a verified digital −3 dB frequency.
3. Compare input/output on common axes. Calculate RMS with explicit zero-input handling and measure delay where the chosen method supports it. Lower RMS alone does not establish better quality.
4. For an amplitude spectrum, state mean removal, window, frequency resolution and normalization. For a Hann-windowed one-sided estimate, double interior positive-frequency bins, not DC/Nyquist. Do not label amplitude as power spectral density.
5. Check frequencies against Nyquist and disclose possible aliasing in nonsinusoidal input. Keep full precision for calculations and round only presentation.

## Output

A source-qualified comparison with filter parameters, initialization, sampling assumptions, time/frequency results and a recommendation limited to the stated objective.

## Verification and limits

Check bypass equality, one-sample averaging, constant-input behavior, a known bin-centered sinusoid and finite output at parameter extremes. Verify the same input realization was used throughout.
