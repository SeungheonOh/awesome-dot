# Four workflows. Twenty-four first submissions.

A repeated offline stress study of task-specific Markdown guides, run on 2026-10-06.

[See every attempt](results/README.md) · [Inspect the tasks](cases/README.md) · [Read the methods](methods/README.md) · [Verify the saved evidence](reproduce_saved_evidence.py)

## What happened

Both conditions met every predeclared artifact requirement on all three repeats of all four synthetic cases. We did not observe a difference on the primary checks. The repeated workload still reached the scoring ceiling; that is a limitation of this comparison, not evidence of general equivalence.

<picture>
  <source media="(max-width: 600px)" srcset="../../../.github/assets/repeated-stress-runs-mobile.svg">
  <img src="../../../.github/assets/repeated-stress-runs.svg" width="1280" alt="All 24 native-agent attempts across four synthetic workflows, three repeats per condition. C received no designated package; S received its designated package. Every R1 and R2 attempt passed 14 scheduled requirements, every R3 attempt passed 12, and every R4 attempt passed 13. All 12 pairs tie, with zero failed or not-assessed requirements. Four authored cases, not 12 independent task samples. Shared runtime; C was not skill-free; process integrity unknown.">
</picture>

C received the task packet without the designated package. S received the same packet plus the pinned package. C was not a skill-free baseline. All boundaries were procedural in a shared cloud filesystem.

| Workflow | Requirements per attempt | C repeats 1 / 2 / 3 | S repeats 1 / 2 / 3 | All criteria met, C / S |
|---|---:|---|---|---|
| Expense reconciliation | 14 | 14/14 · 14/14 · 14/14 | 14/14 · 14/14 · 14/14 | 3/3 · 3/3 |
| Dated action handoff | 14 | 14/14 · 14/14 · 14/14 | 14/14 · 14/14 · 14/14 | 3/3 · 3/3 |
| SQL report reconciliation | 12 | 12/12 · 12/12 · 12/12 | 12/12 · 12/12 · 12/12 | 3/3 · 3/3 |
| Merge and persistence maintenance | 13 | 13/13 · 13/13 · 13/13 | 13/13 · 13/13 · 13/13 | 3/3 · 3/3 |

The raw totals are 159 of 159 scheduled requirement instances per condition, with zero failed or not assessed. There are 53 distinct requirements and 318 scheduled instances overall. All 12 paired pass-count differences are zero; each case's three-repeat difference is also zero. The predeclared equal-case mean verified fraction is 1.0 in each condition. These are descriptive artifact counts on four authored cases, not interchangeable measures of general quality or 12 independently sampled tasks.

## What the evidence covers

<picture>
  <source media="(max-width: 600px)" srcset="../../../.github/assets/repeated-stress-coverage-mobile.svg">
  <img src="../../../.github/assets/repeated-stress-coverage.svg" width="1280" alt="Distinct requirements by synthetic workflow: R1 expense reconciliation and R2 dated action handoff each have 11 mechanical and 3 AI-semantic requirements; R3 SQL report reconciliation has 12 mechanical requirements; R4 merge consumer maintenance has 13 behavioral requirements. Each requirement was assessed on three repetitions in each condition. Semantic judgments are AI ratings, not human evaluation.">
</picture>

The 36 semantic instances received two distinct AI-assisted masked reviews each: 24 reviews and 72 initial votes, with no disagreement. R4's 78 behavioral instances came from reviewed and approved bounded executions of the unchanged frozen probe. Candidate notes do not independently verify their own test claims. [Inspect saved reports and reviews](evidence/README.md).

Artifact coverage does not verify process acceptance. Exact serving model/build, tokens, provider cost, comparable compute time, isolation and complete access histories remain unknown. No population effect, significance, time saving, cost saving or full-dot efficacy claim follows from this study.

## Example artifacts

<picture>
  <source media="(max-width: 600px)" srcset="../../../.github/assets/repeated-stress-evidence-mobile.svg">
  <img src="../../../.github/assets/repeated-stress-evidence.svg" width="1280" alt="Selected saved JSON fields from synthetic workflows. R1 source T07-R1-r3-C shows USD 2,142.65 payable, USD 252.90 held and a separate unvalued EUR 24.00 hold; C007 is a duplicate of C001 with zero reimbursement, and C026 has null USD values. R2 source T05-R2-r3-C shows 18 active actions, 4 of them overdue, 12 done and 4 cancelled; A21 is unresolved and A30 has a null due date. Both displayed sources are C, no designated package. Shown fields and summary values match all three C and three S artifacts within each case. Reformatted excerpts, not screenshots.">
</picture>

No failing criterion was observed. The predeclared fallback uses representative verified outputs, selected by case and dispatch order: [T07 expense reconciliation](artifacts/T07-R1-r3-C/reconciliation.json) and [T05 action register](artifacts/T05-R2-r3-C/action_register.json). Both are C submissions because the fixed selection rule reaches them first. They are saved-file excerpts, not screenshots or guide-benefit examples. The saved [expense totals](artifacts/T07-R1-r3-C/reconciliation.json#L590-L604) and [action totals](artifacts/T05-R2-r3-C/action_register.json#L419-L429) ground the summaries. Inspect the paired S outputs for [R1](artifacts/T08-R1-r3-S/reconciliation.json) and [R2](artifacts/T06-R2-r3-S/action_register.json); the displayed business fields match all six attempts within each case, without claiming whole-file identity. [All 45 original files remain available](artifacts/).

## Inspect or reproduce

- [24-row readable ledger](results/README.md), [per-requirement JSON](results/attempts.json), [all raw pairs](results/pairs.json), [summary](results/summary.json)
- [Frozen tasks, inputs, rubrics and scoring sources](cases/README.md), [pinned guides](guides/README.md), [source provenance](provenance/source-bindings.json)
- [Methods and operational caveats](methods/README.md): post-start bootstrap change, approximate controller timing, T24 logging disconnect and R4 flattened-input lookup
- [Deterministic graphic renderer](../../visualization/render_repeated_stress.py) and [exact visual provenance](results/visual-provenance.json); from the repository root run `python -B evaluation/visualization/render_repeated_stress.py --check`
- [Safe saved-evidence reproducer](reproduce_saved_evidence.py): run `python -I -B reproduce_saved_evidence.py` from this directory; reads and hashes only, with no candidate or model execution

## Historical context

The [earlier eight-case native-cloud study](../../results/native-cloud-2026-10-06/README.md) is preserved unchanged, including its two 40/40 primary scores and separately labeled post-hoc finding. Its files and denominators are not pooled with this study. The [original evaluation protocol](../../README.md) remains a distinct, unrun sealed design.
