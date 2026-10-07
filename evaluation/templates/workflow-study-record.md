# Workflow study record

Blank planning and observation record for [Measure completed-workflow benefit](../docs/measuring-workflow-benefit.md). No study has been run by copying this file. Complete the plan before outcomes; duplicate the attempt and pair sections as needed. Leave planning fields blank until specified. During collection, write `unknown` with a reason for unavailable evidence, `not applicable` with a reason where appropriate, and zero only when observed. Preserve source records; do not overwrite first outputs or earlier decisions.

## Study plan

- Study ID and version:
- Question, intended users/tasks and limits of applicability:
- Study owner; authorization for runtime, human participation and permitted actions:
- Frozen plan location/hash and freeze timestamp:
- C condition and pinned package identity, if any:
- S condition and pinned package identity:
- Common task/input identities and hashes:
- Tools, permissions, ambient instructions and isolation evidence/limits:
- Requested model/reasoning/budgets; observed runtime fields and unknowns:
- Observable completion endpoint; required action/delivery evidence:
- Frozen first/final quality criteria and evidence requirements:
- Workflow review roles; research-only adjudication and blinding procedure/limits:
- Allowed clarification, help, corrections, reruns and stop rules:
- Assignment unit and method; blocking factors; randomization seed/mechanism:
- Realized schedule location/hash; planned attempt IDs, order and pairing:
- Exact-input/different-operator or within-operator/variant design; rationale:
- Prior exposure, training and carryover controls; remaining limitations:
- Variant identities, equivalence rationale and condition/order counterbalancing:
- Workflow start, first-output, acceptance and stop event definitions:
- Clock sources, timezone/offset, precision, synchronization and collection method:
- Included setup/training; separately recorded exclusions and interruptions:
- Human interval categories, overlap handling and capture method:
- Queue/wait and machine timing definitions and available instruments:
- Charge source, attribution, included services, currency and comparable billing basis:
- Prespecified summaries, units, denominators and missing-data treatment:
- Authorized evidence retention/access and privacy arrangements:
- Intended publication audience and evidence proposed for release:
- Publication permission/approval and permitted scope:
- Required redactions, reviewer and release checks:

### Planned positions

Add every scheduled position before collection, including positions that may never start.

| Attempt ID | Pair/block ID | Task/input or variant ID | Condition | Operator ID | Period/order | Planned cap |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Attempt record

- Attempt ID; pair/block ID; condition; task/input/variant identity:
- Operator/reviewer identifiers, relevant experience and prior exposure:
- Actual sequence/period, environment and requested-versus-observed configuration:
- Status and reason: planned / not started / running / completed / stopped incomplete / evidence unavailable:
- Task start timestamp and evidence:
- First submission timestamp, immutable artifact location/hash and evidence:
- Final artifact location/hash:
- Accepted completion timestamp and evidence, only if established:
- Stop or last observation timestamp/reason, if unfinished:
- First-output quality: accepted / unacceptable / unassessed; criterion evidence:
- Final quality: accepted / unacceptable / unassessed; criterion evidence:
- Workflow review versus research-only adjudication; reviewer type and blinding limits:
- External action/delivery evidence, if required:
- Deviations, integrity limits and collection failures:

### Events and human work

Repeat rows for all observed intervals/events, including review and correction rounds. Preserve rejected acceptance decisions. Mark receipt-time observations distinctly from actual event timestamps. Put study-only activities in separate rows labeled excluded.

| Event/interval ID | Person/role or system | Activity | Start timestamp/source | End timestamp/source | Clock/precision | Evidence | Overlap IDs or missingness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| | | | | | | | |

| Correction/review ID | Trigger/criterion | Human or agent actor | Input/output artifact hashes | Decision/change | Activity interval IDs | Evidence |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

### Observed totals and coverage

Derive only from documented events. Active human totals are person-time, not elapsed time; review/correction subtotals may overlap and must not be blindly summed. Unfinished attempts have observed elapsed-to-stop, not completion elapsed.

- Completion elapsed and units; event IDs; complete/partial/unavailable coverage:
- Elapsed until stop/last observation and units, if incomplete:
- Active human work by person and combined person-time; interval IDs/coverage:
- Human review subtotal and coverage:
- Human correction subtotal and coverage:
- Other active human work subtotal and coverage:
- Observed wait/queue intervals, overlap treatment and coverage:
- Separately reported provider timing/CPU counters, units, definitions and coverage:
- Excluded setup/training, study administration and research-only scoring:
- Known missing intervals/counters and reasons:

### Observed charges and usage

- Attributable metered charges, amount and currency:
- Provider/billing period, services, rate/discount basis and source evidence:
- Complete/partial/unavailable charge coverage and excluded costs:
- Provider usage counters with their original names, units and per-call evidence:
- Comparability limits; any separately labeled human-time valuation:

## Pair record

Pair on the unit declared before collection, not because two outcomes look comparable. Retain missing counterparts. Do not call different-operator pairs within-person effects or variant pairs identical-input comparisons.

- Pair/block ID; pairing rationale and unit:
- C attempt ID; S attempt ID:
- Exact input match or variant differences; operator/sequence differences:
- First-quality comparison with both raw assessments:
- Final-quality and completion comparison with both raw assessments:
- Corrections/help comparison with both raw records:
- Completion elapsed C / S, units and capture coverage:
- Active human person-time C / S, units and capture coverage:
- Observed charges C / S, currency, scope and capture coverage:
- Which differences are comparable and why; declared direction for subtraction:
- Missing counterpart/data, failed acceptance, deviations and interpretation limits:

## Accounting and report

Counts are separate populations/stages, not necessarily additive categories. State how each is defined. Use metric-specific capture denominators, including failed attempts with observed expenditure.

| Count or coverage definition | C | S | Unit/denominator and reason for gaps |
| --- | --- | --- | --- |
| Scheduled positions | | | |
| Started attempts | | | |
| First-quality assessed | | | |
| First-quality accepted | | | |
| Final-quality assessed | | | |
| Final-quality accepted | | | |
| Completed with required quality/evidence | | | |
| Known incomplete | | | |
| Unassessed completion | | | |
| Complete observed elapsed coverage | | | |
| Complete active-human-work coverage | | | |
| Complete comparable-charge coverage | | | |

- Distinct participants, tasks, variants, repeats and paired units:
- All raw attempt/pair records and evidence locations:
- Prespecified summaries and exact denominators, including accepted-pair subset coverage:
- Ties, regressions, failures, missingness and protocol deviations:
- Observations supported by these sessions:
- Claims not established; learning, selection, measurement and generalization limits:
