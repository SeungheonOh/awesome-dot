# Results

The completed studies are separate records with different criteria. Both reached the ceiling on their primary artifact checks; neither measured a primary-check benefit from the designated package. Do not pool their denominators.

| Study | Cases / submissions | With skill | Baseline | Primary result |
| --- | ---: | ---: | ---: | --- |
| [Repeated stress study](../studies/repeated-stress-2026-10-06/README.md), 2026-10-06 | 4 / 24 | 159/159 requirements | 159/159 requirements | 12 tied case/repeat pairs |
| [Initial native-cloud study](native-cloud-2026-10-06/README.md), 2026-10-06 | 8 / 16 | 40/40 criterion groups | 40/40 criterion groups | 8 tied case pairs |

With skill (S) means the designated pinned package was supplied. Baseline (C) received no designated package but could have ambient skills. All scheduled first submissions are retained. Shared-filesystem isolation and complete process integrity were not verified; primary artifact passes are not full-process acceptance.

## Inspect the evidence

- Repeated study: [tasks and assertions](../studies/repeated-stress-2026-10-06/cases/README.md), [all 24 submissions](../studies/repeated-stress-2026-10-06/results/README.md), [requirement-level outcomes](../studies/repeated-stress-2026-10-06/results/attempts.json), [grading evidence](../studies/repeated-stress-2026-10-06/evidence/README.md), and [methods](../studies/repeated-stress-2026-10-06/methods/README.md)
- Initial study: [all 16 attempts](native-cloud-2026-10-06/attempts.json), [paired results](native-cloud-2026-10-06/paired-summary.json), [raw artifacts](native-cloud-2026-10-06/artifacts/), and [methods](native-cloud-2026-10-06/method.md)

The initial study's [post-hoc F8 check](native-cloud-2026-10-06/f8/README.md) found a lone-surrogate save failure in the package-supplied artifact. This was outside the predeclared primary criteria and does not change those scores.

## Other evaluation records

- The 180 authored fixture tests (61 harness + 119 case/grader tests) check the evaluation machinery. They are not model trials.
- The original sealed CodexCLI pilot has 0 attempts and has not run. Its [runtime and review prerequisites](../docs/protocol.md#before-model-trials) remain open, and live dispatch is disabled. Not-run or unknown process status is not a 0% acceptance rate.

Exact serving model, token use, cost, and comparable compute time remain unknown. These studies support no time-saving, productivity, statistical-significance, or population claim.

See [reproduction commands](../README.md#reproduce-the-saved-accounting) for both saved-evidence checks and the separate fixture suite.
