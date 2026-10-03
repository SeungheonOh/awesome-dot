---
name: design-quantitative-experiment
description: Prepare a prospective quantitative experiment protocol, including a defensible comparison, allocation or run order, measurement materials, feasible sizing assumptions, and a planned analysis. Use before collecting outcomes; reviewing existing data, qualitative research, and software runtime benchmarks have different deliverables.
---

# Design a Quantitative Experiment

Deliver a protocol someone can use, with the allocation and measurement materials the proposed experiment needs. Resolve the design choices that affect the answer, then check that the planned records can support that answer. A complete preparation task does not require running the experiment or producing observations.

Keep the work proportional to the question. A small comparison may need a short protocol and one recording sheet; a complex design may need separate schedules, scoring instructions and calculations. Preserve the user's actual population, materials, constraints and requested format. This guide covers ordinary benign planning, not specialist authority to conduct clinical, hazardous or other high-stakes interventions.

## Define the answer the experiment should provide

Read the request, candidate materials, available prior evidence and practical constraints before asking for more. Establish the decision, who or what it concerns, the relevant setting and follow-up window, and what can actually be varied. Identify costs, available independent units, timing, equipment and conditions that limit the design. Ask only for missing choices that change the protocol; continue preparing independent parts and label provisional assumptions.

State the target quantity, or **estimand**, in ordinary language: the outcome under which alternatives, averaged over which units or population, at what time, and with what weighting. A difference in mean scores, a difference in proportions reaching a threshold, and a difference in time to an event answer different questions. Define the sign and units of an improvement. If departures from assignment are plausible, specify whether the target concerns assignment to a method or actually receiving it; the latter may require assumptions the design cannot support.

Specify a primary outcome and its calculation before outcomes are seen. If several outcomes are genuinely primary, say how their joint decision will work. Separate secondary and exploratory questions. Retain components of a composite, ratio or rate, including the eligible denominator; do not invent weights to make an appealing summary.

Connect the primary outcome to a practically meaningful effect or an acceptable precision. Use the user's threshold or a justified domain basis, with its source. A guessed effect cannot become an agreed requirement. When no threshold is available, mark it as an unresolved decision or compare explicit planning scenarios. Distinguish detecting any difference from establishing an important benefit, equivalence or an acceptable loss; those require different decision criteria. [NIST's objective guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri31.htm) helps connect the experimental aim to the design.

## Identify units and a comparison that can work

Describe the intervention, control or comparator precisely enough to reproduce: content or settings, duration, permitted assistance, and what stays common. Record relevant versions. If alternatives change several things together, the contrast concerns that bundle; it cannot identify the effect of each component without additional design support. Check that the proposed combinations are feasible. [NIST's variable-selection guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri32.htm) addresses factors, levels and responses.

Make the unit structure explicit:

- **Assignment or experimental unit:** the smallest unit independently assigned to a condition under this design
- **Observation unit:** what produces one recorded measurement; there may be several within an assigned unit
- **Dependence:** shared people, containers, batches, locations, time periods or equipment that connect observations
- **Independent replication:** new assigned units or independently repeated experimental runs, distinguished from rereading the same unit or taking subsamples

Count each separately. Many readings from one treated container do not create many independently treated containers. One group per condition leaves treatment confounded with group; additional people inside those groups do not supply the missing group-level replication. If that is all the user has, name the causal or precision limit and offer the smallest feasible redesign or a bounded exploratory study. Do not quietly claim a confirmatory experiment.

Choose the simplest design that answers the actual question under these constraints. Explain consequential choices instead of listing every possible design:

- Use concurrent comparable controls where feasible; an unrandomized before/after comparison needs explicit treatment of time trends and cannot inherit a randomized causal interpretation
- Randomize eligible units to conditions, or randomize run order, at the level where treatment can actually vary. Specify the allocation ratio, procedure and restrictions. Alternating labels or a convenient schedule is not randomization
- Block on important known nuisance factors when this improves comparison, preserving variation in treatment within blocks and reflecting blocks in the analysis. Do not put every control in one batch and every treatment in another. [NIST's randomized-block guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm) explains this design-analysis connection
- With repeated exposure or a crossover, assess learning, fatigue, order and carryover. Specify the period and sequence allocation, comparable tasks, and any defensible reset or washout. Balanced order does not erase an irreversible learning or treatment effect; use separate units or narrow the question when necessary
- With shared treatment or spillover, consider cluster assignment and the number of independent clusters. Record cluster membership and any contamination. Individual-level randomization cannot solve treatment spillover merely by changing labels
- With multiple factors, select combinations that identify the requested effects and interactions. State effects that remain confounded or unidentifiable; a smaller design does not automatically answer every original question

Distinguish random allocation from sampling a population. Allocation may support a causal comparison within the experiment without making a convenience sample representative. Identify any limits on transfer to other people, batches, conditions or times.

## Make measurement consistent and recordable

Define exactly how the outcome is observed or scored: instrument or rubric, units, permissible values, timing relative to assignment or exposure, and the endpoint. Include the needed starting materials, task instructions or scoring key. Preserve an equivalent measurement opportunity across conditions. When relevant, specify calibration, a scoring check, and blinding of the observer or scorer that is actually feasible; do not claim that an obviously different intervention is concealed.

Keep treatment assignment, treatment actually received and measurement status distinguishable. Define eligibility and exclusions before assignment where possible, plus rules for invalid measurements, deviations and replacement runs. An inconvenient outcome is not an exclusion reason. A replacement remains linked to the original attempt; it must not erase it or enlarge the sample unnoticed.

Plan missingness explicitly. Distinguish a measurement intentionally not scheduled from one missed, withdrawn, invalid or unavailable. Record reasons and timing where known. Do not code missing as zero or automatically analyze only completers. State the proposed missing-data treatment and the assumptions or sensitivity analysis it needs. When observing time to an event, retain the observation schedule, last confirmed event-free time, detected-event time and follow-up cutoff as needed; “no event by cutoff” is not an observed event at the cutoff. The analysis must respect the available timing resolution and censoring.

Create a recording sheet or file with stable identifiers linking assigned units, blocks or clusters, exposures and repeated observations. Include raw outcome components, measurement times, relevant pre-treatment covariates, status/reason codes and deviations when the analysis uses them. Define each field's meaning and units, and how repeated rows are keyed. Keep operational instructions and answer keys away from participants when they would reveal the target response. Collect only information relevant to running or interpreting this experiment.

## Size the study within the real budget

Choose a sizing approach for this design and decision: power for a specified effect and decision rule, precision for an estimate, or a clearly bounded feasibility pilot. State the relevant assumptions, their provenance and uncertainty: variability or baseline rate, allocation, correlation for paired/repeated observations, cluster structure, expected attrition, significance or interval level, and power where used. Report independent-unit counts, allocation by condition or block, and total observations separately.

Use a calculation or tool appropriate to the outcome and analysis, and retain enough inputs and method detail to reproduce it. Verify what its sample-size output counts and round or balance it as the design requires. A simple independent-means formula cannot be reused unchanged for clustered, paired, binary or censored outcomes. [NIST's sample-size discussion](https://www.itl.nist.gov/div898/handbook/prc/section2/prc222.htm) illustrates dependence on assumptions for a mean; its formulas and examples are not universal sizing rules.

When critical inputs are unknown, show plausible labeled scenarios grounded in available information, a precision limit at the available sample, or the specific pilot information needed. Do not manufacture a standard deviation, correlation, effect or universal minimum count. A tiny pilot's variation estimate is itself uncertain. Specify whether pilot records could enter the main analysis and under what preplanned conditions; changing measurement or selection after seeing pilot results may require a separate confirmatory sample.

Reconcile the proposed size with availability, measurement capacity, duration and cost. If the desired precision or effect detection is infeasible, state that directly. Present the useful conclusion a smaller study could support and any change that requires the user's choice. More repeated readings cannot automatically substitute for more independent units.

## Set analysis and stopping before outcomes

Write a concrete analysis plan for the chosen primary quantity, rather than “use an appropriate test.” Specify the analysis set, unit, aggregation or model, contrast, covariates or block terms, weighting, and uncertainty calculation. Respect pairing, clustering and serial or repeated measurements. Decide whether repeated readings form a justified unit-level summary or enter a dependence-aware model; counting every row as independent is not a default.

State the assumptions that matter and what will happen if they are untenable, including a simpler estimate, sensitivity check or inconclusive result. Choose any one-sided hypothesis, equivalence margin or transformation for substantive reasons before seeing the direction of the data. Set the treatment of multiple primary contrasts or outcomes; label additional analyses exploratory instead of selecting the most favorable result. Lack of a statistically detectable difference does not establish equivalence.

Define the planned endpoint for enrollment or runs, follow-up and analysis. Include practical interruption or invalidation rules relevant to the experiment. If results will be examined during collection, specify which looks can affect decisions and an analysis/stopping method that accounts for them, including the maximum scope. Do not keep adding units or stop at the first favorable result under a fixed-sample analysis. Distinguish an operational stop from evidence of an effect.

Keep a dated version of the protocol and materials before collection. A formal registry is needed only when the context requires or the user requests it. Record later amendments, their reasons and whether outcomes were already visible; do not rewrite exploratory decisions as prior commitments.

## Check and deliver the usable protocol

Where allocation is part of the design, produce the actual planned assignment or run-order sheet from known units, or a ready procedure with clearly identified slots when units are not yet known. Record the randomization method, constraints and reproducibility information, such as a generator and seed, when used. Preserve assignment concealment where it matters. A draft allocation is not evidence that anyone received treatment.

Check the packet against itself before handing it over:

- Reconcile eligible units, treatment counts, blocks, sequences, measurement opportunities, follow-up and resource totals. Check any generated allocation against its restrictions without rerandomizing until it looks favorable
- Trace each primary analysis input to a field or documented derivation. Verify that IDs preserve dependence, contrasts are supported by the allocation, required denominator components exist, and the planned design has enough independent information for the stated analysis
- Walk through the measurement and analysis path using blank records or explicitly fictional diagnostic records if useful, including a missing or interrupted observation. Keep diagnostic values out of the future results. Report only the checks actually performed
- Read back the deliverables, calculations and links. Resolve contradictions such as a paired analysis with unlinked units, an endpoint the schedule never observes, or a claimed treatment contrast inseparable from batch

Lead the handoff with what the design can answer and its most consequential limit. Provide the finished protocol, allocation/run order where needed, measurement materials, sizing rationale and analysis/stopping plan in the requested form. Identify the few unresolved decisions or unavailable inputs that prevent readiness; do not describe a provisional choice as approved. Distinguish protocol inspection and planning calculations from an experiment that has run.

Stop when the requested preparation is complete and its feasibility and limitations are clear. Preparing a protocol does not authorize recruiting or contacting people, collecting their data, deploying an intervention, changing a live product or publishing results. If execution is separately requested, establish its actual scope and prerequisites before acting. Do not invent observations, participant consent or empirical findings to make the planning deliverable look complete.
