---
name: calibrate-windowed-spectra
description: Validate the scaling, axes and interpretation of a windowed audio spectrum or spectrogram using known signals and independent transforms. Use when spectral values or visualizations need trustworthy units; not for speech recognition, pitch transcription or subjective audio-quality judgments.
---

# Calibrate windowed spectra

## When to use

Use when an audio-analysis tool needs spectra whose numbers mean what the labels say. Deliver a documented transform/scaling convention, calibrated test evidence and a visualization with correct time and frequency coordinates. A colorful spectrogram alone cannot establish amplitude accuracy.

For choosing among filter candidates, use [compare-sampled-signal-filters](../compare-sampled-signal-filters/SKILL.md); this workflow checks the spectral measurement itself.

## Required inputs

- Sample rate, channel layout, sample encoding and full-scale reference
- Transform length, hop, window convention and segment boundaries
- Desired quantity: amplitude, power or power spectral density
- One-sided or two-sided representation and frequency-axis range
- Display limits, processing budget and intended export

Resolve these before comparing libraries. Two reasonable implementations can disagree because they use different window definitions, detrending, normalization or units. Do not “fix” this by normalizing every image to its own brightest pixel.

## Workflow

### 1. Preserve the signal contract

Decode only supported file encodings and validate container sizes, channel count, sample rate and block alignment. Reject non-finite samples. Keep values beyond the nominal full-scale range visible in the diagnostics rather than silently clipping them before analysis.

Analyze channels separately unless the task explicitly calls for a mix. Averaging opposite-polarity stereo channels can cancel a real signal; it is not a neutral way to simplify the data. Retain the selected channel and original frame offset in the result.

Bound the selected duration and total transform work. A worker can keep the interface responsive, but does not remove memory and CPU limits. Cancel obsolete work and prevent its result from replacing a newer selection.

### 2. Define the transform and normalization explicitly

For an N-sample periodic Hann window, use `w[n] = 0.5 - 0.5*cos(2*pi*n/N)`. A symmetric Hann using N−1 is a different window; name the one actually used. Record whether the input mean is removed and whether incomplete frames are padded or omitted.

For a coherent-gain-corrected one-sided amplitude spectrum, divide each FFT magnitude by the sum of window coefficients. Double interior positive-frequency bins, but do not double DC or the Nyquist bin of an even-length transform. Convert amplitude ratios with `20*log10`; power ratios use `10*log10`. Do not label amplitude-bin values as a power spectral density.

Define dBFS relative to the file's nominal sample amplitude. Under this amplitude convention a full-scale, bin-centered sine produces about 0 dBFS at its bin. Its unwindowed time-domain RMS is about −3.0103 dBFS. Neither value is an acoustic sound-pressure measurement.

Keep zero and infinity handling explicit. A silent frame has zero amplitude, whose mathematical logarithm is negative infinity. A finite display floor can render it, while a summary may use a documented null/silence representation. Do not turn the display floor into an asserted physical noise level.

### 3. Calibrate before using complex recordings

Exercise original known signals:

- A bin-centered sine with known peak amplitude
- The same sine at half amplitude
- DC and, for an even transform, an alternating-sign Nyquist signal
- Silence and an off-bin sine
- Separate stereo channels, including an opposite-polarity pair if mixing is supported

Check the expected bin frequency `k*sampleRate/N`, amplitude correction and time-domain RMS independently. Use tolerances consistent with floating-point input and transforms, not exact equality to theoretical zero.

Compare the FFT implementation against a direct DFT on small fixtures, or against an independent established implementation with matching conventions. Do not compare two wrappers around the same FFT and call that independent validation. Include phase and multiple frequencies so a single sine cannot hide indexing or sign mistakes.

An off-bin sine will spread energy and show scalloping loss. This is a windowing effect, not automatically a gain-calibration defect. The strongest bin is not necessarily the fundamental frequency or perceptual pitch.

### 4. Keep spectrogram coordinates tied to frames

State whether time labels refer to frame starts, centers or ends. When displaying centers, include the original segment offset and half the transform length. Use the actual hop in sample units; if the hop changes to stay within a frame budget, report that change.

Use only complete windows when that is the chosen policy, and report omitted tail samples. Zero padding may refine the display grid but does not create additional independent frequency resolution. Do not equate FFT bin spacing with guaranteed separation of nearby tones.

Keep frequency units and Nyquist limits visible. Cropping the displayed frequency range must not alter the computed transform. If the display aggregates multiple bins or frames into a pixel, document whether it uses a maximum, mean or other statistic rather than presenting a pixel as an exact original bin.

### 5. Separate analysis from presentation controls

Choose a stable amplitude color range or an explicit user-controlled floor. Changing that floor should remap colors without recomputing, rescaling or modifying the samples. Values above the display ceiling can be saturated visually while remaining available numerically and flagged when consequential.

Provide a selected-frame spectrum and text readout so the color image is not the only way to inspect the result. Label full-band and cropped views consistently. Reset or mark stale readouts when the segment, channel or transform settings change.

Exports should include sample rate, transform/window/hop convention, channel, original time offset and the stated numerical quantity. A summary without raw audio can still reveal information about a recording; keep its destination within the user's scope. Do not automatically upload local audio for an offline analysis.

### 6. Verify the execution and artifact boundaries

Check both numerical results and the path that produces them. For a worker implementation, test message identity, transferable buffers, cancellation and a late completion after the user changes channels or opens a different file. A worker-thread adapter can validate the protocol without proving browser-worker behavior; state that boundary.

Render a known spectrogram and inspect its orientation, time progression, frequency range and clipping. Keep this distinct from real-browser layout or subjective listening. An app that never plays audio does not need to claim audio playback validation.

## Worked example

Use a 1,024-sample frame at 16,384 Hz containing a 1,024 Hz sine. It lands at bin 64. With a periodic Hann and the one-sided amplitude convention above, a unit-amplitude sine's bin is approximately 0 dBFS. Halving its amplitude gives approximately −6.0206 dBFS, while its time-domain RMS becomes approximately −9.0309 dBFS. A DC input and an alternating-sign Nyquist input each test that endpoint bins are not doubled.

A local JavaScript implementation tested these values, silence and bounded frame generation. Twelve small 32-sample signals were checked against direct real/imaginary DFT summation. A Node worker-thread adapter exercised the actual browser-worker module's request/result protocol and transferable buffers. A simulated UI check verified that display-floor changes did not launch another transform and that an obsolete channel's completion could not restore a cancelled result.

For a separate original four-second chirp at 16 kHz, a 1,024-point transform and 256-sample hop yielded 247 complete frames. Frame centers ran from 0.032 to 3.968 seconds. The rendered spectrogram showed the rising-frequency trace, while numeric peak bins progressed from 218.75 to 1,984.375 Hz. These are discrete bin peaks, not exact instantaneous-frequency estimates. Real-browser layout and actual Web Worker behavior remained unverified by the adapter and artifact checks.

## References

- [Julius O. Smith, spectrum analysis of a sinusoid](https://www.dsprelated.com/freebooks/mdft/Spectrum_Analysis_Sinusoid_Windowing.html): windowing, leakage and transform interpretation
- [SciPy periodogram](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.periodogram.html): explicitly distinguish spectrum and density scaling when comparing implementations
