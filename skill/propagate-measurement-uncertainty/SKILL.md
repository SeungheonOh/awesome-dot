---
name: propagate-measurement-uncertainty
description: "Calculate a derived measurement result and its uncertainty from stated inputs, with shared effects, an interpretable budget and qualified interval or coverage claims."
---

# Calculate and Explain Measurement Uncertainty

Return the derived quantity, its units, the uncertainty measure requested and enough of the measurement model to explain the result. When recomputation is requested, deliver editable inputs and an actual saved calculation that a reader can run or update. A short calculation can stay in the response; do not require a workbook, simulation or evidence package for every question.

Use when uncertainty attached to measured inputs, corrections or reference quantities must pass through a defined calculation. Use **check-dimensional-calculations** for unit and nominal-value work alone, **analyze-data-question** for an ordinary question about supplied observations, **build-predictive-model** for a fitted prediction artifact, and **simulate-system-scenarios** for the behavior of an evolving system. These neighboring methods can support a real dependency without becoming a mandatory chain.

## Define the quantity and the input statements

Identify the quantity being estimated, its equation, output units and intended use. Read the actual readings, uncertainty statements, correction notes and relevant versions. Separate supplied evidence from model assumptions and missing information. Establish whether the requested result is the equation evaluated at input estimates, a distributional mean or another specified summary; nonlinear transformations can make those different quantities.

For each input, retain its estimate, unit, source and uncertainty meaning. A correction estimate changes the nominal calculation; uncertainty in that correction describes a separate effect. A calibration statement applies only under its stated conditions. Keep exact conversion factors separate from uncertain reference quantities.

Resolve what an expression such as “±0.2” means before treating it as a standard uncertainty: it may be a bound, standard deviation, expanded uncertainty or stated interval. Do not invent a multiplier or probability model. If material information is missing, give the supported nominal result or explicitly conditional partial calculation and identify the missing input. A partial budget is not automatically a bound on the complete uncertainty.

## Put components on a consistent basis

Convert uncertainty statements with their stated interpretation:

- For independent repeat readings of a stable quantity, the uncertainty of the estimated mean may be `s / sqrt(n)`, with the appropriate sample variance. The spread of individual observations answers a different question. Paired rows, drift, dependence or a fitted calibration can require another statistical treatment
- Convert an expanded statement `U` with a known factor `k` to its standard form `u = U / k`. Retain the original statement and factor
- Convert a bound to a standard uncertainty only under an explicit, justified distributional model. For example, a uniform distribution over a symmetric half-width `a` has standard deviation `a / sqrt(3)`; a bound by itself does not prove uniformity
- Check whether rounding, resolution or another named effect is already included. Do not add the same uncertainty twice or divide a common correction component by the number of repeated readings

[NIST's Type A guidance](https://physics.nist.gov/cuu/Uncertainty/typea.html) describes statistical evaluation, including the uncertainty of a mean under independent observations. Its [Type B guidance](https://physics.nist.gov/cuu/Uncertainty/typeb.html) explains conversion using supplied multipliers or stated distribution assumptions. Keep those conditions visible in the calculation.

## Preserve shared effects and dependencies

Represent one shared uncertain source once, wherever it appears in the equation. Reusing the same correction or reference is different from having independent quantities with equal uncertainty magnitudes. A shared effect can increase, reduce or cancel uncertainty depending on the equation's sensitivities.

Use the supported joint-input model: independent source components, a covariance matrix, paired observations under an appropriate statistical model, or another supplied dependence structure. Row alignment alone does not establish paired observations. Check covariance units, symmetry and validity when a covariance matrix is used. Do not quietly set an unknown material correlation to zero.

For a scalar output `y = f(x)`, first-order propagation can be written as `u_y² = J Σ Jᵀ`, with sensitivities in `J` and input covariances in `Σ`. In an independent-component representation this reduces to the sum of squared standard effects. If a shared parameter enters several terms, differentiate the whole equation with respect to that one parameter. Preserve covariance cross terms when working with correlated derived inputs. [NIST's combination guidance](https://physics.nist.gov/cuu/Uncertainty/combination.html) describes this approximation and its covariance terms.

Make the budget interpretable: input/component, estimate, unit, standard uncertainty, sensitivity or propagation role, dependence and output contribution. Correlated contributions cannot always be allocated uniquely to independent positive rows. State the convention used, or show the relevant covariance terms directly. A plausible total does not establish correct component identity.

## Choose and check a proportionate propagation method

Use an exact expression where available or first-order propagation where the equation is sufficiently smooth over the relevant uncertainty scale. Inspect denominators, discontinuities, thresholds and physical domains. Choose a useful check: analytic sensitivities, a finite-difference comparison, a local curvature bound, a known limiting case or a direct alternative calculation. A local numerical check establishes its stated neighborhood, not behavior in unexamined tails.

When nonlinear or asymmetric behavior requires propagating distributions, establish the input distributions and their dependencies first. Do not manufacture distributions merely to run a sampler. Preserve shared draws across every use of the same uncertain quantity. [JCGM 101](https://www.bipm.org/en/doi/10.59161/jcgm101-2008) provides the measurement-model context for distribution propagation using Monte Carlo methods.

For a numerical distribution calculation, retain the algorithm, input model, numerical settings and reproducibility information needed for the task. Bound its work and assess numerical stability at a meaningful precision. A fixed seed reproduces one computation; it does not validate the assumed model or establish sufficient tail precision.

Account for outcomes outside the equation's domain. Report their frequency or probability when supported and explain the consequence for the requested result. Do not silently clip inputs, replace undefined values, redraw until valid or discard failed trials. A summary conditional on valid outcomes needs that condition and its denominator; it cannot stand in for an unconditional interval without justification. If the requested uncertainty is not established, return that useful finding alongside the supported calculation.

## Report the result and the meaning of its interval

Give the estimated quantity and units, combined standard uncertainty when established, and the requested expanded uncertainty or model-based interval. State factors, probability levels and interval conventions explicitly. Round the reported result consistently with its uncertainty while retaining sufficient working precision for recomputation.

`U = k × u` is an expansion rule. A chosen `k = 2` does not by itself establish 95% empirical coverage or a confidence interval. The connection depends on the output distribution and the reliability of the uncertainty estimate; [NIST's coverage guidance](https://physics.nist.gov/cuu/Uncertainty/coverage.html) states the conditions for the familiar approximate interpretation. Likewise, quantiles of an assumed propagated distribution describe that model. They do not validate it against unobserved physical measurements.

Explain the dominant contributions and any requested sensitivity comparison without changing the accepted model silently. Label a deliberately incorrect or alternative model as a diagnostic. Distinguish changing an uncertainty magnitude from changing a correction estimate. Unmodeled effects remain unquantified; do not claim they were experimentally excluded. A successful calculation does not certify an instrument or the object measured.

## Make the requested result usable

When files or a reusable calculation are requested, save the inputs, equation/assumptions, budget and results in formats suited to the user. Use available tools and proportionate controls. Interpret source values before a conversion can conceal a relevant invalid input; distinguish invalid model values from unsupported numerical representation. Check finite derived results and any domain restrictions before returning an ordinary result. Preserve earlier outputs when an edited input fails.

Reopen the exact saved output and reconcile its values, units, component identities and reported limits. Exercise the delivered command or workbook through the actual supported consumer, from the context in which it is meant to work. If maintainability is requested, change one meaningful input in a separate copy and verify the corresponding recomputation while retaining the original. Keep implementation diagnostics separate from the explanation a reader needs for normal use.

Deliver the requested answer or actual files with the equation, supported uncertainty statement, important assumptions and remaining limits. Distinguish mathematical checks, saved-file readback, consumer execution and real measurement evidence. Stop when the requested calculation and usable handoff are complete, or when a concrete missing input or unsupported method prevents the dependent claim.
