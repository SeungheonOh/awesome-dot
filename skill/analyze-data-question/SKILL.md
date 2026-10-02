---
name: analyze-data-question
description: Answer a concrete question from authorized tabular data through calculations, focused exploration, and interpretation. Use for comparisons, trends, distributions, and possible explanations; a request only to profile, clean, or join data does not need this workflow.
---

# Analyze a Data Question

Deliver an evidence-backed answer to the user's question, with the calculations and limits needed to understand it. Let the question guide the exploration. A column inventory, cleaned dataset, analysis plan, or dashboard is not a substitute for the requested answer.

## Define what the answer measures

Inspect the supplied data and available definitions before asking for more context. Establish the outcome of interest, relevant population, comparison, and time window. Reuse the user's definitions; disclose reasonable assumptions and ask only when a missing choice would materially change the answer.

Distinguish a source row from the unit being analyzed. A row might be an event, line item, person, or repeated snapshot of the same person. Choose the unit that answers the question before aggregating. Repeated observations must not silently give some people or entities more weight.

For rates and averages, identify the eligible denominator and weighting. “Per order,” “per customer,” and “per active customer” answer different questions. Keep numerator and denominator aligned in population and time; retain counts behind percentages. Do not average group rates or averages without considering their underlying weights. Define how an empty or unknown denominator affects the result.

For time comparisons, use the appropriate event date, timezone, and comparable observation windows. Distinguish events during a period from outcomes for a cohort that started in that period. Allow for different follow-up time, incomplete recent periods, and changed metric definitions when relevant.

## Check the data that can change the answer

Use the available tools to inspect and calculate from the actual authorized sources. Preserve raw inputs and work on a separate analysis representation. Identify the source and extraction or snapshot date when known. Check extraction limits and scope before treating the supplied rows as the full population.

Focus quality checks on the fields and records the question depends on:

- Whether keys, repeated records, or joins inflate the chosen observation count
- Whether types, units, currency, dates, or category meanings are consistent
- How much of the eligible population has usable outcomes, comparison fields, and denominators
- Whether missingness, exclusions, or source coverage differ across the groups or periods being compared

Keep missing, zero, not applicable, and invalid values distinct. Do not silently convert unknown outcomes to failures or successes, or drop them from a rate. State the treatment and show its effect when material. A result for records with observed values is not automatically a result for everyone eligible.

Resolve ordinary preparation within the requested analysis. Preserve ambiguous records and bound their effect when possible; ask for a definition only when needed. Avoid turning every analysis into a full cleanup or reconciliation project.

## Calculate, then explore what explains the result

Start with the calculation most directly responsive to the question. Show its magnitude in useful units, with enough supporting counts to interpret it. Distinguish a percentage-point difference from a relative percent change, and avoid precision the data cannot support.

Choose follow-up views for their ability to explain or challenge that answer:

- Inspect distributions when an average may hide skew, a long tail, or distinct subgroups. A median, range, percentile, or share above a meaningful threshold may help more than another average
- Investigate unusual values before changing them. A valid extreme observation can be the main result. Correct or exclude a value only with a supported reason; otherwise retain it and show its influence if substantial
- Compare meaningful groups or periods, including their sizes and coverage. Check whether changing customer mix, exposure, seasonality, or eligibility could account for an overall difference
- When composition matters, examine comparable subgroups or a justified common weighting alongside the overall result. State the population each view represents; do not choose weights or filters because they produce a preferred conclusion

Explore enough to answer the question and assess its important alternatives. Do not search every possible slice for a striking pattern. If a pattern emerged only after trying many comparisons, describe it as exploratory and treat follow-up confirmation separately.

## Check how much the conclusion depends on choices

Use simple sensitivity checks proportional to the uncertainty: another defensible time window, inclusion of valid extremes, plausible treatment of missing outcomes, or a like-for-like population. Recompute the affected result and report whether its direction or practical size changes. Do not create arbitrary scenarios when the definition is settled and the uncertainty immaterial.

Use statistical intervals or tests only when they answer a real question and their assumptions fit the data. Account for repeated observations or clustered sampling when relevant. A descriptive difference alone does not establish statistical significance, generalizability, or causation; large samples do not repair biased coverage.

Separate what was observed from possible explanations. An association or before-and-after change can suggest a mechanism but does not establish that an intervention caused it. Say what further evidence would distinguish important alternatives without withholding a useful descriptive answer.

## Deliver a result someone can use

Lead with the answer and its practical meaning, then the few calculations that support it. State material qualifications near the affected claim. If the evidence cannot answer the full question, give the bounded answer it does support and identify the specific missing data or decision.

Use a chart only when it makes a comparison, distribution, or pattern easier to see. Choose an appropriate scale, label units and populations, and make partial periods or missing coverage visible. A table or a few sentences may be sufficient. Do not require a plot, formula, or hypothesis test to call the analysis complete.

Keep transformations reproducible with tools actually available: retain the source reference and the filters, derived fields, exclusions, weighting, and aggregation used. Save a rerunnable calculation when the work warrants it; a small calculation can have a compact explanation instead. Check headline values against the executed results and inspect any delivered chart or file for misleading labels or stale values. Report what was actually calculated, not an unexecuted method as a finding.

Deliver in the requested format with the relevant source links or artifact. Ordinary requested analysis does not need a new approval round; changing source records, sharing data, or building an app is separate work unless requested.
