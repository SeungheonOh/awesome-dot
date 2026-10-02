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

### Preserve a comparable observation window

Record the original sample count, sampling rate, filter parameters and initial state for every candidate. If a filter changes sample count or introduces padding, identify exactly which output interval is being compared. Do not trim a transient from one candidate but retain it for another. For real recordings, keep the authorized source local and avoid copying unrelated channels into the report.

When reporting delay, state the estimator and whether the input is sufficiently informative for it. Cross-correlation on a periodic signal may have several equivalent peaks. Frequency-bin spacing is fs/N; it does not by itself establish the uncertainty of a peak estimate.

## Output

A source-qualified comparison with filter parameters, initialization, sampling assumptions, time/frequency results and a recommendation limited to the stated objective.

## Verification and limits

Check bypass equality, one-sample averaging, constant-input behavior, a known bin-centered sinusoid and finite output at parameter extremes. Verify the same input realization was used throughout.

## Interpretation traps

A smoother waveform can contain more phase delay. A lower peak can reflect attenuation rather than noise rejection. If the user needs signal-to-noise improvement, require a defensible signal/noise definition or reference; do not rename total RMS as SNR.

## Worked example

Use the synthetic samples [0, 2, 0, 2] and a causal two-sample moving average that uses available samples during startup. The filtered output is [0, 1, 1, 1]. A bypass candidate returns [0, 2, 0, 2] unchanged.

Input RMS is √2, approximately 1.4142; average-output RMS is √0.75, approximately 0.8660. The level change is about −4.26 dB. The comparison reports the reduced RMS and the stated startup convention. It does not call the average better: the user has not supplied a clean target or acceptable delay/distortion criterion.

If the first sample were discarded for the average only, the reported RMS would answer a different question. Keep both outputs on the same time axis and disclose the exact samples used in each metric.

## Evidence status

The worked example illustrates the stated inputs and reasoning. Unless an execution result is explicitly identified, it is not a claim that external services, real devices or user data were tested. Report actual checks and unrun stages on each use.
