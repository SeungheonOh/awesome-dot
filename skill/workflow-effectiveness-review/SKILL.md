---
name: workflow-effectiveness-review
description: "Compare existing baseline and assisted task-run records on matched scope, acceptance quality, human effort, elapsed time and unfinished work; return a bounded comparison with auditable denominators and missing measurements."
---

# Review Whether a Workflow Helped

Use this when someone has records of doing comparable work with their usual workflow and with assistance, and wants to know what those records actually show. Deliver a scoped comparison of accepted work, effort and delays, with enough evidence to reproduce it. This works for everyday tasks such as preparing a restock checklist and technical tasks such as checking a release package.

This is a review of recorded work, not a general productivity claim, employee ranking, survey-theme analysis or fact-check of a promotional statistic. A useful result can be “less hands-on work in one pair, longer delivery time, and too much missing data to compare the whole batch.” Do not force a winner.

## Establish the comparison

Read the real records the user supplied or already authorized you to access. Preserve their requested workflow, source boundary and destination. No special tracker, integration or experiment is required. Record these inputs in plain language:

- **Question and unit of work:** the practical decision, task family, deliverable, start boundary and what counts as accepted completion
- **Variants:** what the baseline actually used, what assistance changed, tool/version or settings if known, and whether a person switched variants mid-task
- **Scope:** dates and timezone, all eligible attempts in the supplied window, task complexity or size, operators/reviewers, and any inclusion rules already used
- **Quality:** the user's acceptance criteria, tolerances and required checks; the source material and output versions needed to inspect them
- **Measurements:** timing logs, timestamps, review notes, corrections, retries, setup or training records, failures and unfinished attempts, with units and provenance
- **Design and access:** any original task assignments or pairing, execution order, repeated inputs, permitted source locations and authorized output/delivery

Use “unknown” for absent inputs. Ask only for missing information that changes the question or prevents a meaningful comparison. If quality criteria were not supplied, propose concrete criteria from the requested deliverable; label them analyst-proposed until confirmed. Continue source accounting and timing checks meanwhile. Do not retrospectively choose easier criteria for the assisted outputs or silently change the baseline to “doing nothing.”

If no baseline records exist, give a one-variant description and the smallest missing evidence needed for a comparison. Do not invent a baseline, substitute a remembered typical duration or use the worked example as measurement data. If the request is for a new study, explain what would need to be recorded and seek the necessary authority before running tasks, recruiting people or installing collection tools. This skill does not start an experiment automatically.

## 1. Account for attempts before comparing outcomes

Create a source inventory and attempt ledger. Keep raw values and original versions separate from derived fields. Cite an actual file/row, event ID, output version, review note or authorized record URL for each consequential value. Missing locators remain gaps; never fabricate a provider link.

```text
source: id, locator, version, coverage/window, timestamp_basis, access_gaps
attempt:
  id, task_instance_id, variant, operator_key, reviewer_key,
  scope_signature, input_and_output_versions, start, acceptance_or_cutoff,
  outcome, initial_quality, final_quality, correction_or_retry_links,
  measured_effort, elapsed, documented_waits, setup_links,
  measurement_kind_and_coverage, source_ids
disposition: source_or_attempt_id, included_or_excluded, reason, affected_metrics
pair: id, baseline_attempt_id, assisted_attempt_id, match_basis, differences,
      assignment_basis, order, eligible_metrics
```

The outcome is accepted, completed but rejected, unfinished, cancelled or unknown. Distinguish work never started from an attempted task. A retry remains linked to the original task and its effort; it is not a new successful task that erases a failed attempt. If a task switches from assistance to manual recovery, label the hybrid path and retain both phases. Do not present it as a clean assisted-only success. Count tasks, attempts/retries and outputs separately when they differ.

Include eligible failures, abandoned attempts, long waits and unavailable records in the accounting. Deduplicate repeated exports by stable identity and version; multiple snapshots of one attempt do not enlarge the sample. Keep scope mismatches visible with a reason for excluding them from a metric. Do not drop a slow run merely because it is unusual, or select records by success after seeing the result. If only successful examples were supplied, say so and do not infer a completion rate for all work.

## 2. Check that the work is comparable

Build a scope signature from the delivered work, not the task title alone: input count and difficulty, ambiguity, required output fields, permitted tools, review standard and completion boundary. “Draft available” and “reviewed result accepted” are different endpoints. An assisted workflow that produces more work may be useful, but its time is not a like-for-like comparison with a smaller baseline deliverable.

- Use recorded pairs or justify matches from task characteristics before examining their time advantage. Pairing is a record of comparability, not proof that assistance caused a difference
- Keep the same quality gates and endpoint for both sides of a pair. A change in criteria or input version can require a new stratum or an unmatched description
- If tasks share scope but have different source contents, explain the matching limits. If someone repeats the exact same task, record what they could have learned from the first run
- Show order, practice, operator/reviewer differences, tool availability, interruptions and task assignment where known. Do not call an ordering randomized unless records establish it
- If grouping was created after inspecting outcomes, disclose that choice; do not present it as an original design

When no defensible pair exists, report variant-specific descriptions for comparable task groups with their composition and sample sizes. Do not turn sorted fastest-to-slowest runs into pairs or subtract unmatched averages as a causal estimate. Do not pool unlike task families into one productivity score. Normalizing by item count is only defensible when the units and complexity are comparable; six easy items are not automatically equivalent to six ambiguous ones.

## 3. Apply acceptance gates and preserve rework

Inspect the available output against each supplied criterion and its source. Use pass, fail or unverified, with the exact evidence and output version. Keep initial submission and final accepted output separate. A reviewer saying “looks good” supports that review event; it does not prove an unavailable artifact met every criterion.

Record every evidenced correction: affected criterion, original value or omission, revised value, source supporting it, severity under the supplied rubric, who did the repair and recorded repair/review effort. Retain rejected drafts and retry links. Do not invent defect severity weights, trade a missed must-have for speed, or treat an unreviewed draft as accepted. A zero-correction count needs evidence of no recorded corrections within the declared coverage; absent review records are unknown.

Report first-submission passes and final accepted tasks with explicit denominators covering all eligible attempted tasks. Keep rejected, unfinished and unverified counts alongside them. When a quality result is unavailable, label the numerator as confirmed passes and state how many outcomes remain unverified; do not treat unknown outcomes as known failures or imply an exact pass rate. Do not calculate “time to accepted result” for a task with no accepted result. Its time and effort through the cutoff still belong in the attempt ledger and batch resource accounting.

## 4. Reconcile what each clock measures

Keep these quantities separate and use the same definitions on both sides:

| Quantity | Meaning and treatment |
| --- | --- |
| Human effort | Active human time preparing inputs, prompting/operating, checking, correcting, handling artifacts and recovering failures. Sum nonoverlapping intervals per person. With multiple people, report person-minutes, including review effort, rather than calling the sum wall-clock time |
| Elapsed time to acceptance | Agreed task start through accepted completion. Preserve gross calendar duration, including waits and interruptions. If a net duration is also requested, name the excluded intervals and apply the same rule to both variants |
| Documented wait | Evidenced tool, queue, external-dependency or other inactive intervals, with overlap noted. An unattended tool can consume elapsed time without consuming human effort |
| Setup and learning effort | Variant-specific setup, reusable preparation, training or migration recorded outside the per-task interval. Show observed setup separately and include it in any stated total adoption-cost scope |
| Effort/time through cutoff | Resources already spent on unfinished work. Label as spent so far, not a completion duration or an eventual estimate |

Do not subtract a tool runtime from elapsed time and call the remainder human effort. Logs showing messages sent and replies received do not show continuous active work. Calendar timestamps can establish elapsed time without establishing active time. Distinguish measured intervals, recalled estimates, derived bounds and missing values; do not mix their precision.

Reconcile phases to totals only where the source establishes an exhaustive, nonoverlapping partition. For one person, active and idle intervals can partition elapsed time. Concurrent operators, overlapped tool work or incomplete phase logs usually cannot. Flag clock disagreements, negative durations, timezone ambiguity, duplicated intervals and rounding differences before aggregating. Preserve the inconsistent record and exclude only the affected calculation until resolved.

Missing time is never zero. Keep an exact total unavailable if a component is unknown. A lower or upper bound is useful only when its assumptions are explicit and supported. For example, known active time plus an unclassified interval can bound effort when a complete single-person timeline rules out additional or overlapping work. Do not invent a midpoint for missing review time. If records only bound one side, report that one-sided bound.

Do not quietly amortize setup across hypothetical future tasks. Show actual batch totals and, if useful, a separately labelled allocation across the observed task count. Any future break-even calculation is a conditional scenario, not an observed saving; state the assumed repeat frequency, per-task difference, maintenance and review burden. If those inputs are missing or completion is unequal, leave break-even unresolved.

## 5. Calculate the supported comparisons

Choose the informative descriptive quantities for this question rather than filling a scorecard. Lead with acceptance and coverage, then effort and delivery time. A speed comparison restricted to accepted tasks is allowed, but label it a selected subset and show all-attempt outcomes alongside it.

For each metric, state the task/attempt unit, eligible set, known values, missing values, exclusions and number of complete pairs. Preserve all pairs in the ledger even when a particular metric is unavailable. Different metrics may have different sample sizes; never let a displayed row imply a shared denominator when it has none.

```text
paired_difference = assisted_value - baseline_value
  negative: less of this quantity in the assisted attempt
  positive: more of this quantity in the assisted attempt
relative_difference = 100 * paired_difference / baseline_value
  only if baseline_value > 0 and both measurements have the same meaning
first_pass_fraction = initial passes / all eligible attempted tasks
accepted_fraction = accepted tasks by cutoff / all eligible attempted tasks
batch_human_effort = observed setup + effort for every eligible attempt/retry
  retain missing components or propagate defensible bounds
```

Show counts with fractions, especially for small sets. If the denominator is zero, the fraction is unavailable. Report an absolute difference without a percentage when the baseline is zero. Do not average per-task percentages and present the result as the percentage change in a batch total. If presenting both, label each calculation and its weighting separately.

With a few comparable runs, the individual pairs, median or mean paired difference, and observed range are usually enough. Say which summary was used. An observed range is not a confidence interval. One pair supports a description of that pair; it does not establish typical performance. Repeated work by the same person, shared setup and reused inputs do not become independent people or independent experiments.

Check whether missing measurements, failures, different task mix, correction effort or setup could change the headline. Show supported bounds or leave the answer unresolved. Do not invent a statistical-significance claim, causal effect, population benefit, monetary value of time or company-wide extrapolation. An authorization to review logs is not permission to infer individual competence or rank workers. If the user needs formal inference, a causal study or personnel evaluation, report this review's limits and clarify that separate scope.

## 6. Return a useful result

Produce the comparison, not merely a plan to measure it. Keep the main result short enough to act on and place the traceable details below it:

1. **Bounded answer:** what changed in this recorded set; whether both workflows produced accepted equivalent work; the most important uncertainty
2. **Scope and accounting:** question, variants, endpoint, window/cutoff, task matching, ordering, total eligible tasks, retries, exclusions and inaccessible records
3. **Quality and resource comparison:** first-pass/final outcomes, correction burden, effort, elapsed/wait time and setup, each with its own denominator and measurement coverage
4. **Pair/attempt appendix:** source locators, output versions, quality decisions, phase totals, missing values, formulas and computed results before display rounding
5. **Interpretation and next decision:** what the evidence supports, what it cannot establish, and the smallest missing record or user choice that could change the conclusion
6. **Checks performed:** observed result or explicit reason a check could not run

Recommend a workflow change only against the user's criteria. If the priority is unknown and lower effort conflicts with later delivery or more review, state the tradeoff and ask for that priority only if a choice is required. Do not rebrand a failed acceptance gate as a quality/speed tradeoff the user already approved.

Use the requested authorized destination. Save or deliver the completed result when the user already authorized that bounded action, then inspect the saved content and verify the returned reference. Do not ask again solely because actual records or routine delivery are involved. Reuse prior authorization while the source, audience, data and purpose remain in scope. New account access, experiments, outreach, uploads to another service, sensitive disclosure, broader sharing or ongoing monitoring need the applicable authorization. Preserve source records; corrections to the analysis do not authorize rewriting the logs.

## Verification and stopping

- Reconcile every supplied source and every eligible attempted task, including failures and unfinished work; verify duplicate/retry treatment
- Open the evidence for every decisive acceptance decision and correction, using the correct output version and a shared gate
- Recompute at least the headline differences, denominators and setup-inclusive totals/bounds from raw records; check signs, units, overlap and zero baselines
- Confirm that missing time, absent review and unfinished results remain visible; compare the accepted-only subset with the all-attempt accounting
- Verify the matching basis and order were not relabelled as experimental control; identify the exact scope of every claimed improvement
- Read back the actual result and its local/source links; record any unavailable artifact, blocked delivery or unrun check

Stop when the bounded record set is accounted for and each requested comparison has a supported value, bound or named gap. A valid result may be inconclusive. Ask for the smallest missing record when it would change the answer; continue independent checks. Do not fill the gap by running new tasks, silently widening the window, contacting participants or repeatedly requesting already-granted permission.

## Worked example

[The fictional cupboard-checklist records and completed review](example.md) include three matched task pairs, a review correction, missing review timing, different active and waiting time, reusable setup and an unfinished retry. All durations and outcomes in that example are authored fixture data, not measurements of dot, a real person or a deployed product. [The verification record](verification.md) states which checks were actually run and their limits.
