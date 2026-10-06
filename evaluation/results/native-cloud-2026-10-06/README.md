# Native-cloud artifact study · 2026-10-06

**No measured uplift on the primary criteria.** All 16 actual native-agent first submissions passed all five artifact criterion groups: **40/40 groups per arm, eight tied pairs, 0 percentage-point difference**. Both arms reached the ceiling on this small suite. That does not establish that skills never help, and overall process acceptance remains unknown.

## Results

C received no designated package; S additionally received the case's pinned package. Every scheduled case and first submission is included.

| Case | Task | C groups passed | S groups passed | S − C |
| --- | --- | ---: | ---: | ---: |
| F1 | Expense reconciliation | 5/5 | 5/5 | 0 |
| F2 | Meeting actions and handoff | 5/5 | 5/5 | 0 |
| F3 | Meeting windows | 5/5 | 5/5 | 0 |
| F4 | Source-grounded decision | 5/5 | 5/5 | 0 |
| F5 | Document revisions | 5/5 | 5/5 | 0 |
| F6 | SQLite report reconciliation | 5/5 | 5/5 | 0 |
| F7 | JSON Patch verification | 5/5 | 5/5 | 0 |
| F8 | Text-merge caller maintenance | 5/5 | 5/5 | 0 |
| **Total** | **8 pairs; 16 attempts** | **40/40** | **40/40** | **0** |

Thus 8/8 artifacts in each arm passed their case's primary checks. These are artifact-level results, not verified full-process acceptance. Structured grading and two AI-assisted semantic reviews where required supplied the ratings; no human evaluation was conducted. F8 additionally received source-reviewed local behavioral execution.

**Secondary finding:** An identical, post-hoc F8 edge-case check found that S raised `UnicodeEncodeError` when saving text containing a lone surrogate (`U+D800`); C preserved it through save/reload. This check was added after source review, is separate from the predeclared primary criteria, and does not change their scores. [F8 evidence and scope →](f8/README.md)

## Limits that matter

- Both arms used the same requested model/effort configuration within an ambient native runtime. Ambient instructions or skills could be present in both; C was not a skill-free baseline
- Separation was instruction-only on a shared filesystem. OS isolation and complete process integrity were not independently verified; overall acceptance stays unknown
- Exact serving model, token use, cost, and human productivity are unknown. Approximate 77–273-second observation intervals include concurrent scheduling and tool/observation overhead and do not establish speed savings
- Eight public authored cases, one pair each, and ceiling scores support no statistical-significance or population claim

This is a separate exploratory study. The original sealed CodexCLI pilot has not run. The [method appendix](method.md) details scoring, provenance, and all accounting/protocol deviations.

## Inspect and reproduce

- [All 16 attempt records](attempts.json), [eight paired results](paired-summary.json), and [exact saved artifact files](artifacts/)
- [Artifact hashes](artifact-manifest.json), [source/prompt provenance](provenance.json), and [randomized schedule](schedule.json)

From the repository root:

```sh
python -B evaluation/results/native-cloud-2026-10-06/score.py
```

This verifies evidence bindings and reproduces the saved-rating summary without executing submitted code. Generated Python artifacts are included for inspection, not automatic execution. The separate `python -B evaluation/check.py` command runs 180 authored fixture tests, not model trials.
