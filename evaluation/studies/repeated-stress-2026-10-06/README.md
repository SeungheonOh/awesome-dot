# Repeated stress evaluation

- Date: 2026-10-06
- Runtime: native cloud agents; exact serving model/build not exposed
- Cases: 4 authored synthetic workflows
- Runs: 24 first submissions, with 3 repeats per case and condition

With skill (S) received the task packet plus its pinned designated package. Baseline (C) received the same task packet without that package. Baseline was not skill-free: ambient instructions or skills could be present in both. Filesystem boundaries and review masking were procedural.

## What happened

Both conditions passed every predeclared artifact requirement. All 12 case/repeat pairs tied; no primary-check benefit was observed. The scoring ceiling limits this comparison and does not establish general equivalence.

| Case | With skill | Baseline | Delta (S − C) |
| --- | ---: | ---: | ---: |
| [R1 · Expense reconciliation](cases/R1/candidate/TASK.md) | 42/42 | 42/42 | 0 |
| [R2 · Dated action handoff](cases/R2/candidate/TASK.md) | 42/42 | 42/42 | 0 |
| [R3 · SQL report reconciliation](cases/R3/candidate/TASK.md) | 36/36 | 36/36 | 0 |
| [R4 · Merge consumer maintenance](cases/R4/candidate/TASK.md) | 39/39 | 39/39 | 0 |
| Total scheduled requirement instances | 159/159 | 159/159 | 0 |

Counts sum all three repeats per condition. Each R1/R2 submission passed 14/14 requirements, R3 passed 12/12, and R4 passed 13/13. There were 53 distinct requirements and 318 scheduled instances overall, with zero failed or not assessed. Each condition had 12/12 submissions meeting all criteria and a predeclared equal-case mean verified fraction of 100%.

These are four authored cases, not 12 independently sampled tasks. Requirements are not interchangeable units of general quality. Always-pass requirements did not distinguish the conditions in this study. [Every repeat](results/README.md) and [all paired differences](results/pairs.json) are retained.

## What the evidence covers

| Evidence type | Passed / scheduled, both conditions | Basis |
| --- | ---: | --- |
| Mechanical | 204/204 | Frozen R1/R2 data checks and R3 SQL checks |
| AI-assisted semantic | 36/36 | Two masked reviews per R1/R2 submission |
| Behavioral | 78/78 | Reviewed, approved R4 probe executions |

The 36 semantic instances received 24 reviews and 72 initial votes, with no disagreement. These are AI ratings, not human evaluation; masking and independence were procedural. R4 used the unchanged frozen probe in bounded executions. Candidate notes do not independently verify their own test claims. [Inspect the reports and review rationales](evidence/README.md).

Artifact coverage does not verify process acceptance. Shared-filesystem isolation, complete access histories, and process integrity remain unknown. Exact serving model/build, tokens, provider cost, and comparable compute time were not exposed. No population effect, significance, time saving, cost saving, productivity gain, or full-dot efficacy claim follows.

## Example artifacts

No failing criterion was observed. The predeclared fallback selected representative verified outputs by case and dispatch order. Both examples are baseline submissions because that selection rule reaches them first; they are not examples of skill uplift.

- R1: [baseline reconciliation](artifacts/T07-R1-r3-C/reconciliation.json) and [paired skill reconciliation](artifacts/T08-R1-r3-S/reconciliation.json). The baseline's [totals](artifacts/T07-R1-r3-C/reconciliation.json#L590-L604) show USD 2,142.65 payable, USD 252.90 held, and a separate unvalued EUR 24.00 hold. Inspect the [duplicate claim](artifacts/T07-R1-r3-C/reconciliation.json#L117-L134) and [unvalued hold](artifacts/T07-R1-r3-C/reconciliation.json#L493-L510).
- R2: [baseline action register](artifacts/T05-R2-r3-C/action_register.json) and [paired skill register](artifacts/T06-R2-r3-S/action_register.json). The baseline's [totals](artifacts/T05-R2-r3-C/action_register.json#L419-L429) show 18 active actions, including 4 overdue, plus 12 done and 4 cancelled. Inspect the [unresolved action](artifacts/T05-R2-r3-C/action_register.json#L246-L256) and [missing due date](artifacts/T05-R2-r3-C/action_register.json#L354-L364).

The cited business fields match all six outputs within each case; this does not claim whole-file identity. [All 45 original artifact files](artifacts/) remain available.

## Inspect or reproduce

- [Tasks, inputs, assertions, and scoring sources](cases/README.md)
- [Pinned guides](guides/README.md) and [source provenance](provenance/source-bindings.json)
- [24-row results ledger](results/README.md), [per-requirement outcomes](results/attempts.json), and [machine-readable summary](results/summary.json)
- [Methods and operational caveats](methods/README.md), including the bootstrap change, approximate controller timing, T24 logging disconnect, and R4 flattened-input lookup

From the repository root, using Python 3.12:

```sh
python -I -B evaluation/studies/repeated-stress-2026-10-06/reproduce_saved_evidence.py
```

The [saved-evidence verifier](reproduce_saved_evidence.py) reads JSON and hashes, checks evidence bindings, and recomputes the counts. It makes no model calls, executes no submitted code or SQL, writes nothing, and performs no fresh semantic review. This reproduces saved accounting, not the original agent runs.

## Historical context

The [earlier eight-case study](../../results/native-cloud-2026-10-06/README.md) retains its separate 40/40 primary scores per condition and post-hoc finding. Its denominators are not pooled here. The [original sealed protocol](../../docs/protocol.md) remains unrun.

Prior [visual provenance](results/visual-provenance.json), [graphic renderer](../../visualization/render_repeated_stress.py), and asset files are retained for the publication record. The [evaluation index](../../README.md) lists current reports and checks.
