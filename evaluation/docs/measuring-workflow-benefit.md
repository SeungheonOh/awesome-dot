# Measure completed-workflow benefit

Use this supplement when artifact checks cannot answer whether a skill helps someone finish useful work. It describes a later, separately authorized study, not a launcher or evidence of improvement. Start with [Evaluate one skill change](adding-a-case.md); copy the [blank record](../templates/workflow-study-record.md). Existing artifact results cannot retrospectively supply missing human effort or billing measurements.

## 1. Define completion before measuring speed

Write the task's acceptance criteria and observable endpoint before collection. Distinguish the first submission from a reviewed, corrected, accepted result. Count normal user prompting, checking, clarification, editing and resubmission in the workflow. Predeclare permitted help, correction limits and stopping rules equally across conditions.

Retain the first artifact unchanged and every subsequent version. Record who made each correction and why. Evaluate first-output quality and final quality separately against the same frozen requirements. Name the human reviewer, using a study identifier, and record review evidence; label AI-assisted review accurately. Keep research-only adjudication separate from the review a user ordinarily needs. Record actual blinding and its limits.

If the endpoint includes delivery or an external action, require observed confirmation of that action and separate authorization. A satisfactory draft does not establish delivery. Report quality and completed tasks before timing: quicker unacceptable work is not a workflow benefit. This follows the distinction between effectiveness, assistance and resources in [NIST's usability-report guidance, sections 5.4.4.1–2](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=151449).

## 2. Keep the comparison identifiable

Reuse the authoring guide's package/input freeze and requested-versus-observed runtime record. Hold task instructions, input bytes, permissions, available tools, help policy and budgets constant within an exact-task comparison. Record ambient instructions, inaccessible runtime details and deviations. A package supplied is the intervention; correct use is not assumed.

Before outcomes, save all planned attempt IDs, assignment units, sequence, pairing, caps and analysis rules. Randomize condition assignment within task blocks where feasible; record operator experience and session conditions that could matter. [NIST's randomized-block guidance](https://www.itl.nist.gov/div898/handbook/pri/section3/pri332.htm) explains separating a treatment comparison from known nuisance factors. Conclusions still depend on the actual assignment, implementation and sample; randomization does not guarantee balanced operators or unbiased measurement.

Choose and label the design:

- **Same inputs, different operators:** each operator sees a particular task once; both conditions receive that task. These are task-paired observations, not within-person effects. Operator differences remain relevant.
- **Same operator, different task variants:** predeclare comparable variants and counterbalance condition order and variant-to-condition assignment across operators. These are not identical-input pairs; variant difficulty remains a limitation.

Fresh agent contexts do not erase human familiarity. Do not treat repeating an already solved task as a fresh comparison. Learning from a skill can persist into later baseline work; a pause or counterbalanced order does not establish its removal. The [primary reporting guidance on carryover](https://www.bmj.com/content/366/bmj.l4378) discusses persistent treatment effects; applying that concern to learned workflows is a design judgment here. If learning could transfer across tasks, keep each operator in one condition for the study or restrict conclusions to observed sessions.

## 3. Observe distinct clocks

Define each event, clock source, timezone, precision and capture method before running. Save source timestamps and evidence, not reconstructed estimates.

- **Completion elapsed:** observed workflow start through accepted completion, including intervening waits and correction cycles. Record any excluded setup/training separately and identically. Observer-receipt timestamps measure observation windows if actual event times are unavailable.
- **Active human work:** observed intervals per person for preparation/prompting, review, correction and other task work. Merge overlapping intervals for one person's total; show review and correction subtotals. Multiple people's person-time can exceed elapsed time. Retrospective estimates are not observed active time.
- **Waiting and queueing:** identify intervals only when observed. They can overlap human work or each other. Do not add overlapping categories to elapsed time or infer idle time by subtracting person-time.
- **Machine timing:** preserve provider-reported execution/queue measures or process CPU counters separately, with their definitions. Wall time and tool-arrival gaps do not measure model compute. Unexposed fields remain unknown.

Keep study administration and research-only scoring outside workflow effort, with that exclusion visible. If an acceptance requirement is discovered unmet, retain the earlier decision and correction; do not preserve an invalid completion timestamp as success.

## 4. Keep failures and missing measurements

Record every planned position, including never-started attempts, cancellations, timeouts and collection failures. Separate known unacceptable work from unassessed quality, and incomplete work from missing completion evidence. For an unfinished attempt, retain observed time until stopping or last observation; do not call it time-to-completion, zero or the cap.

Link repairs to their originals. A correction phase does not replace first-submission results. Record partial timing coverage, missing intervals and reasons; do not fill gaps with guesses. Keep incomplete pairs visible.

Retain only necessary evidence with authorized access; private retention does not authorize publication, so obtain permission for the intended audience and redact protected information before releasing raw records.

## 5. Compare costs only when metered

Retain attributable provider charges, currency, billing period, included services, rate/discount basis and evidence. Compare costs only on a comparable basis with stated capture coverage. Partial charges are not whole-workflow cost. Tokens alone are usage, not observed billing; missing usage is not zero. Do not price human time without an explicitly defined, separately labeled valuation.

## 6. Show raw pairs before summaries

For each planned pair, show both attempt IDs, assignment/order, first and final quality, completion status, corrections, observed elapsed/person-time, metered cost and missingness. Give scheduled, started, assessed, accepted and complete-measurement counts by condition. State each summary's denominator and pairing unit.

Only compute paired time/cost differences where the specified comparable measurements exist. Successful-pair timing is a selected subset; publish its coverage alongside all failures. Keep participants, tasks, repeats, checks and reviewer votes distinct. Do not pool historical studies with this new workflow record.

Describe ties and regressions. Before/after differences, counterbalancing alone and small convenience samples do not establish causal benefit, equivalence or population productivity. Any broader inference needs an appropriate prespecified design and analysis; this guide supplies neither a sample-size justification nor a power estimate. The [runtime and review gates](protocol.md#before-model-trials) still apply where relevant, with additional human-study authorization and measurement arrangements required.
