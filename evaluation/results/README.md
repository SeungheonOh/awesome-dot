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

- The [transfer artifact cohort](../studies/transfer-2026-10-07/README.md), 2026-10-07, retains 12 first submissions and 24 captured outputs across two synthetic cases, with three repeats per case and condition. All 156 declared artifact-check instances passed; T1 C and S each passed 42/42 and T2 C and S each passed 36/36. Both equal-case means are 1.0, with six tied case/repeat pairs. The one-word prompt deviation and unknown actual model/build, realized tool/instruction exposure and isolation limits remain explicit. This separate ceiling tie establishes no benefit, equivalence or broad transfer, and does not change the primary-study table or its denominators; [inspect all statuses](../studies/transfer-2026-10-07/RESULTS.md) and [run its separate verifier](../README.md#verify-the-separate-transfer-package).
- The [engineering artifact pilot](../studies/engineering-artifacts-2026-10-07/README.md), 2026-10-07, retains all eight planned positions across two synthetic cases: six captured artifacts passed the frozen structured checks, and two triage positions are infrastructure unknowns, one per condition. Both captured triage dispositions remain unrun. This source-only, artifact-level evidence establishes no candidate tool execution or tool-performance benefit. It remains separate from the two primary-study rows and their denominators; [run its separate checks](../README.md#verify-the-separate-engineering-package).
- The exploratory [semantic grader calibration](../calibration/semantic-2026-10-07/README.md), 2026-10-07, checks grader behavior on 14 related synthetic outputs. It contains no skill intervention or uplift estimate and is not pooled with the two studies. Its raw reviews and methodological limits are preserved; [run its separate verifier](../README.md#verify-the-separate-calibration-package) for saved-result reproduction.
- The 180 authored fixture tests (61 harness + 119 case/grader tests) check the evaluation machinery. They are not model trials.
- The original sealed CodexCLI pilot has 0 attempts and has not run. Its [runtime and review prerequisites](../docs/protocol.md#before-model-trials) remain open, and live dispatch is disabled. Not-run or unknown process status is not a 0% acceptance rate.

Exact serving model, token use, cost, and comparable compute time remain unknown. These studies support no time-saving, productivity, statistical-significance, or population claim.

See [reproduction commands](../README.md#reproduce-the-saved-accounting) for both saved-evidence checks and the separate fixture suite.
