---
name: evaluate-probability-predictions
description: Evaluate supplied binary probability predictions against known outcomes with explicit comparison cohorts, proper losses, ranking metrics and reliability bins. Use for an existing prediction export; not for training a model or approving consequential decisions.
---

# Evaluate probability predictions

## When to use

Use when someone has predicted probabilities and realized binary outcomes and wants to understand their quality. Produce a reproducible scorecard and reliability view with coverage and limitations. Do not turn a descriptive evaluation into a deployment recommendation without the separate evidence and authority that requires.

## Inputs

- Stable case ID, model/version ID, probability of the specified positive class, and outcome
- Target meaning, prediction horizon and whether outcomes are mature
- Evaluation split or time/group boundary, if supplied
- Comparison population, threshold convention and requested metrics

If split independence, leakage or label quality cannot be checked, say so. Unknown outcomes are not negatives. Synthetic fixtures can test the evaluator but cannot establish real model performance.

## Workflow

### 1. Validate the prediction unit

Preserve case identity and model identity. Reject duplicate case/model pairs or reconcile them under an explicit version rule. Check that models agree on the recorded outcome for a shared case; do not let inconsistent labels silently change the comparison.

Require finite probabilities between zero and one and explicit binary outcomes. Do not coerce a blank probability to zero, “unknown” to a negative label, or a percent value into a fraction without a known unit contract. Report invalid input rather than quietly removing difficult examples to improve scores.

Check whether repeated records represent independent cases, multiple horizons or repeated observations of one entity. The same textual ID is not enough when the prediction unit differs. Keep supplied weights, grouping and timing semantics explicit; do not introduce them merely to make a metric favorable.

### 2. Set the comparison cohort before scoring

For paired model comparisons, identify the intersection of eligible case IDs and show each model's available, used and excluded counts. The intersection may change the population, so retain the coverage effect beside the scores.

Separate-cohort scores can be useful descriptively, but differences may reflect population difficulty or prevalence rather than model quality. Do not rank models as though they saw identical cases. If the common cohort is empty, return no comparable score rather than fabricating zero.

### 3. Compute metrics with their actual meaning

For binary outcomes y and positive-class probabilities p:

- Binary Brier loss is the mean of `(p-y)^2`, on the zero-to-one scale
- Binary log loss is the mean of `-log(p)` for positives and `-log(1-p)` for negatives
- ROC AUC measures ranking, giving half credit to tied positive/negative scores; it requires both classes
- Threshold classification uses a declared boundary such as `p >= threshold`, with TP, FP, TN and FN retained

Use numerically stable expressions such as `log1p(-p)` where appropriate. Decide and disclose the boundary-probability policy. Un-clipped log loss is infinite when a model assigns zero probability to the observed outcome. If a library clips probabilities, record its epsilon and do not compare that result to an un-clipped implementation as if their definitions were identical.

Keep undefined ratios explicit: precision is undefined without predicted positives; recall is undefined without actual positives; AUC is undefined with only one class. Do not replace undefined values with zero for a cleaner table. Serialize infinities deliberately because ordinary JSON numbers cannot represent them.

A lower Brier or log loss does not alone prove better calibration; these scores also reflect discrimination and the outcome distribution. AUC says nothing about whether the probabilities are numerically well calibrated. A constant observed-prevalence Brier baseline is a descriptive reference, not a deployable baseline trained independently of the evaluation labels.

### 4. Inspect reliability with denominators

For a stated bin rule, compute each nonempty bin's mean prediction, observed positive fraction and count. Keep empty bins empty. State interval boundaries, including where p=1 belongs. Plot mean prediction on x and observed frequency on y with a diagonal reference; do not plot bin midpoints as if they were actual mean predictions.

Show counts alongside points. A one-case bin does not supply strong calibration evidence. Binned absolute calibration error depends on the bins and sample; label it descriptive and avoid presenting it as a universal model property. If uncertainty intervals are requested, choose an approach consistent with independent or grouped sampling and document its assumptions rather than adding generic error bars.

### 5. Separate threshold tuning from probability quality

Changing the decision threshold changes confusion counts and threshold metrics, but must not change Brier loss, log loss or AUC for the same predictions. Verify this invariant.

Do not choose a final threshold on the evaluation set and then describe that same result as untouched validation. If costs or constraints are supplied, retain them explicitly and distinguish exploratory threshold review from a prospective operating policy.

### 6. Verify independently and deliver

Use hand-computable cases for perfect, tied and reversed rankings; one-class data; exact zero/one probabilities; empty shared cohorts; missing and conflicting rows. For a small dataset, compare the efficient AUC computation against direct positive-negative pair enumeration. Check total confusion counts and bin counts against the used denominator.

Test that changing bins or thresholds leaves the underlying proper losses unchanged. Preserve precision in calculation and round only presentation. Label every export with the cohort, threshold, bin rule and metric conventions.

Export only the data needed for the recipient. Removing original case IDs reduces exposure but does not automatically anonymize small-group aggregates or model names. Do not publish or send sensitive evaluation data beyond the approved destination.

## Worked example

Two independent fixture cases have predictions 0.1 for outcome 0 and 0.9 for outcome 1. Binary Brier loss is `(0.01 + 0.01)/2 = 0.01`; un-clipped mean log loss is `-log(0.9)`, approximately 0.1053605; AUC is 1. At threshold 0.5, both cases are classified correctly. At threshold 0.95, both are classified negative, so accuracy becomes 0.5 while Brier, log loss and AUC remain unchanged.

A separate one-case fixture with probability 0 and outcome 1 has infinite un-clipped log loss and undefined AUC. Writing null or zero for that loss would conceal the certainty error. An exported string such as `"Infinity"` with the stated convention is an explicit representation.

In a local JavaScript evaluator exercised with Node 24.19, 200 seeded small prediction sets with tied scores were compared to an independent all-positive/all-negative-pairs AUC oracle. Confusion and bin totals reconciled, and threshold/bin changes left the proper losses and AUC unchanged. A simulated UI check verified cohort controls, invalid-input export guards and absence of case IDs from the aggregate export. A rendered reliability SVG was inspected separately. These checks validate the evaluator on those fixtures; they do not establish that any real model is calibrated, leakage-free or useful in production.

## References

- [scikit-learn probability calibration](https://scikit-learn.org/stable/modules/calibration.html): reliability diagrams and the distinction between proper losses and calibration alone
- [scikit-learn model evaluation](https://scikit-learn.org/stable/modules/model_evaluation.html): metric definitions and interpretation boundaries
