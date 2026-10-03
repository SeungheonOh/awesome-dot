---
name: build-predictive-model
description: Train and evaluate a reusable supervised predictor from authorized tabular data, then deliver the fitted preprocessing/model artifact and a checked inference path. Use when future predictions and their validation are the output, rather than descriptive analysis, a formula-driven spreadsheet, synthetic-data generation, or AI prompt development.
---

# Build a Predictive Model

Deliver a predictor someone can actually use on new inputs, with evidence that explains its limits. The trained estimator, learned preprocessing, input/output contract and saved consumer must agree. A training score, notebook, or serialized object alone does not establish either useful predictions or working delivery.

Keep the work within the requested modeling task. Descriptive answers belong with `analyze-data-question`; editable assumption-driven workbooks with `build-spreadsheet-model`; invented datasets with `generate-synthetic-data`; reusable language-model instructions with `develop-ai-task-instructions`. Use software implementation or package verification only when the request needs that additional deliverable. Do not turn a local model into a hosted service or monitoring system without that scope.

## Define the prediction before fitting

Read the request, data definitions and any existing model or consumer. Identify what one prediction concerns, when it is made, the target and its units or class meanings, the prediction horizon, and the inputs available at that moment. Distinguish predicting a future outcome from explaining what caused a historical one.

Choose the evaluation question that matches intended use: later observations of familiar entities, unseen entities or batches, a different setting, or another specified transfer. A model can work for one and fail for another. Preserve the user's metric, cost tradeoff, resource limit and required quality threshold. If these are unsettled, propose a defensible criterion and explain its consequence; do not invent a success threshold after seeing scores.

Establish the actual delivery format and environment. A local fitted artifact and prediction command may be enough; a workbook, package, API or dashboard is not automatic. Inspect available libraries and versions before depending on them. Ask only for missing information that changes the target, permitted data, validity of evaluation or usable delivery, and continue independent work.

## Inspect the learning data and its availability

Preserve raw inputs. Inspect the fields that determine the target, eligible population, features and split. Distinguish rows from independent units, repeated measurements, duplicate exports, related entities and overlapping time windows. Define target maturity: a recent record whose outcome is not yet known is not a negative label or a zero duration.

Check consequential types, units, ranges, class meanings, missingness, source coverage and exclusions. Retain the reason for dropping or holding a record. Do not quietly remove difficult cases to improve the reported score. Resolve an ambiguous label definition before training it as truth; a supplied label can itself be wrong or inconsistently measured.

For each candidate feature, establish that its value is available at the prediction time. A post-completion measurement, later correction, label-derived field or future aggregate may explain the target while being unusable for prediction. An identifier may connect repeated units rather than provide a transferable signal. Decide from the intended use and source meaning, not from correlation alone.

Use only authorized data. Label invented data and designed relationships clearly. Synthetic observations can exercise the modeling and consumer workflow; their test scores do not establish performance on a real population. This workflow does not confer authority to deploy sensitive or high-impact decisions about people.

## Reserve evaluation data at the right unit

Define training, development and final evaluation roles before selecting a model. Preserve the actual row or group assignments, cutoffs and consequential seeds so the comparison can be understood and repeated. There is no universal split percentage or minimum sample size.

Match the split to the prediction question:

- For transfer to unseen groups, keep every related observation from a group on the same side of a comparison
- For future prediction, train on information available before the evaluated period; account for target windows or feature aggregation that overlap the boundary
- For independent observations, an appropriate random or stratified split may be useful, but stratification does not remove group or time dependence

Check that each split can support the chosen calculation. A class absent from an evaluation set, very few independent groups, or immature targets can make a metric undefined or a conclusion weak. Report that limit rather than repeatedly redrawing the split until it looks favorable. [Scikit-learn's cross-validation guide](https://scikit-learn.org/1.8/modules/cross_validation.html) describes why group and temporal structure change validation choices; use the method appropriate to the actual data, not a default splitter merely because it runs.

Use development data or suitable training-only cross-validation to choose features, model settings, calibration and decision thresholds. Keep final test outcomes out of those decisions. Once final results influence a revision, record that exposure; those same records are no longer untouched evidence for the revised candidate. Do not claim independence merely because files were renamed or a random seed changed.

## Fit the complete prediction path

Start with a meaningful simple baseline, such as a training-derived constant, majority-class rule or valid existing predictor. Compare it on the same eligible evaluation records and metric definitions. A complex model that does not improve the relevant outcome may not be the useful choice.

Select a small, justified set of candidates within the available data and compute budget. Prefer a simpler adequate model over an unbounded search. Explain a consequential choice, such as interpretability, support for missing values, inference cost or extrapolation behavior. Do not select an algorithm solely because it is fashionable or produces the best training score.

Fit every learned step on the training portion of each comparison: imputation, scaling, categorical levels, feature selection, target encoding, resampling and the estimator itself as applicable. Reuse those fitted steps to transform validation, test and future inputs. A preprocessing step performed once on the full table can leak information even if the estimator sees only training rows. A correctly constructed pipeline helps keep these stages together, as illustrated in [the common-pitfalls guidance](https://scikit-learn.org/1.8/common_pitfalls.html); verify how the chosen library actually fits it within validation.

Keep label meanings and output orientation explicit. For classification, a score, a class probability estimate and a selected class are different outputs. Record which class a score refers to and which threshold or decision rule converts it to an action. Do not describe uncalibrated scores as reliable individual confidence. For regression, preserve target units and any inverse transformation; do not silently clip predictions unless the contract defines that behavior and evaluation includes it.

Handle convergence warnings, failed fits and invalid configurations visibly. Correct a supported implementation error, but retain the comparison history when results affected a choice. Do not hide failed candidates or substitute a different metric after an unfavorable result.

## Evaluate the candidate that will be delivered

Freeze the chosen feature contract, preprocessing, estimator settings and decision rule before final evaluation. Run the held-out comparison within the declared scope. Preserve predictions paired with target and record identity where appropriate, plus the data/model versions needed to recompute the reported metrics.

Report the outcome in useful units, with counts and a baseline comparison. Include the errors that matter for the task: a duration model may need absolute-error scale and large misses; a classifier may need a confusion matrix, class support and the relevant false-positive/false-negative tradeoff. Accuracy alone can conceal a poor minority-class result. Keep averaging, weighting and the eligible denominator explicit. Undefined metrics are not zero or a pass. [The model-evaluation documentation](https://scikit-learn.org/1.8/modules/model_evaluation.html) explains the differing purposes of metrics and baseline estimators.

Inspect enough actual errors to identify material limits such as unseen categories, a shifted range, one poorly represented group or time drift. Treat findings from this inspection as post-evaluation knowledge. Do not repair those cases and reuse the original score as evidence for the repaired artifact.

Use intervals, resampling or repeated comparisons only when they answer the requested uncertainty and respect dependence. Cross-validation fold variation is not automatically a confidence interval, and repeated random splits do not create new independent observations. Keep descriptive test performance separate from causal claims, population guarantees and deployment readiness.

If the candidate misses the required quality level, say so and deliver the requested evaluation and useful artifact with that status. Do not manufacture a passing model. When refitting a selected procedure on more data for delivery, distinguish the newly fitted artifact from the one evaluated; the earlier score belongs to the stated evaluation procedure and data boundary, not to an untouched test of that refit.

## Save and exercise real inference

Save the full fitted prediction path in the requested compatible format, with its input schema, feature meanings, missing/unknown-value policy, output units or labels, and necessary version information. Preserve selected thresholds and any fitted calibration or target transformation with the model. A detached scaler or undocumented column order can make an otherwise valid estimator unusable.

Choose persistence with the actual consumer in view. Some formats have estimator or operator limits; some require matching runtime versions. Pickle-based formats can execute code when loaded, so do not treat an arbitrary supplied model as inert data. Use an authorized, trusted artifact route and verify format-specific compatibility, following relevant [persistence documentation](https://scikit-learn.org/1.8/model_persistence.html). A file hash identifies the bytes; it does not establish their source or safety.

Reopen the saved artifact through the intended prediction entry point in a fresh process or other meaningful consumer context. It must not rely on training-session variables, refit preprocessing on incoming rows or silently load a different model. Confirm that the exact saved model receives correctly typed features and emits the promised output, preserving input identity and order when those are part of the contract.

Compare representative pre-save and loaded predictions under an appropriate numerical tolerance. Exercise a consequential new-input case, such as an allowed missing value, an unseen category, reordered fields or a rejected invalid value. Check the documented invocation from the delivered files. A successful deserialization or `--help` call alone does not prove inference; a local inference check does not establish predictive quality on a new population.

## Deliver a usable, bounded result

Return the actual model artifact, consumer and requested training/evaluation materials, with a short usage note and the meaningful findings. State the prediction contract, data/split scope, baseline, observed test result, exact artifact identity, tested runtime and known limitations. Keep extra reports and charts proportional to the task.

Read back the final saved files and reconcile every reported score with the actual evaluated version. If final bytes changed, repeat affected consumer checks and identify whether statistical evaluation also needs renewal. Separate model fitting, evaluation, saved inference and any later integration; claim each only when performed. Hosting, live deployment, new external data connections and ongoing monitoring require their own requested scope.
