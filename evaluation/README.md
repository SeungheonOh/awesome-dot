# Evaluation

Saved task outputs, requirement-level evidence, and local checks for this repository. The two original artifact studies found no difference on their predeclared primary artifact checks. They do not establish general equivalence or productivity gains.

Jump to [results](results/README.md) · [contributor guide](docs/adding-a-case.md) · [verification](#verify-locally)

For a new contribution, start with [Evaluate one skill change](docs/adding-a-case.md), a short guide with executable authored controls.

## Repeated artifact study

- Date: 2026-10-06
- Runtime: native cloud agents; exact serving model/build not exposed
- Cases: 4 authored synthetic workflows
- Runs: 24 first submissions, with 3 repeats per case and condition

With skill (S) received the task packet plus its pinned designated package. Baseline (C) received the same task packet without that package. Ambient instructions or skills could be present in both; baseline does not mean skill-free.

| Metric | With skill | Baseline | Delta (S − C) |
| --- | ---: | ---: | ---: |
| Requirements passed / scheduled | 159/159 | 159/159 | 0 |
| Submissions meeting all requirements | 12/12 | 12/12 | 0 |
| Equal-case mean verified fraction | 100% | 100% | 0 pp |

All 12 case/repeat pairs tied. The 53 distinct requirements produced 318 scheduled instances across both conditions, with no failed or unassessed instances. These are artifact checks on four cases, not 12 independently sampled tasks. Always-pass requirements did not distinguish the conditions in this study.

[Full report](studies/repeated-stress-2026-10-06/README.md) · [Tasks and assertions](studies/repeated-stress-2026-10-06/cases/README.md) · [Every submission](studies/repeated-stress-2026-10-06/results/README.md) · [Saved grading evidence](studies/repeated-stress-2026-10-06/evidence/README.md)

## What these results support

They describe the saved artifacts against the declared requirements. Both studies used shared filesystems with procedural boundaries; isolation and complete process integrity were not verified. Semantic ratings are AI-assisted, not human evaluation. Exact model identity, token use, provider cost, and comparable compute time remain unknown. Recorded observation intervals cannot establish speedups.

The [earlier eight-case study](results/native-cloud-2026-10-06/README.md) contains 16 submissions and 40/40 primary criterion groups per condition. Its separate post-hoc save failure remains documented. Its scores are not pooled with the repeated study. See the [complete results index](results/README.md).

## Separate grader calibration

The exploratory [semantic grader calibration](calibration/semantic-2026-10-07/README.md), dated 2026-10-07, checks grader behavior on 14 related synthetic outputs. It contains no skill intervention and estimates no skill uplift; its votes are not pooled with either study. Shared-filesystem masking, label-aware gold review, sparse negative examples and unknown serving models limit its interpretation. The package preserves all raw reviews and methodological limitations.

## Separate engineering artifact pilot

The [engineering artifact pilot](studies/engineering-artifacts-2026-10-07/README.md), dated 2026-10-07, preserves eight planned positions across two synthetic cases: six captured first-final artifacts passed their frozen structured checks, and two triage positions remain infrastructure unknowns, one per condition. Both captured triage dispositions remain unrun; evaluator replay is not candidate-execution evidence. Tool abstention and isolation were not enforced or verified. These descriptive results are not pooled with the two studies above and support no tool-performance or general guide-effect claim.

## Separate transfer artifact cohort

The [transfer cohort](studies/transfer-2026-10-07/README.md), dated 2026-10-07, retains 12 first submissions across two synthetic tasks with three repeats per case and condition. All 24 output files were captured, and all 156 declared artifact-check instances passed: T1 C and S each 42/42, and T2 C and S each 36/36. Both equal-case means are 1.0; all six paired differences are zero. This ceiling tie is a narrow descriptive result, with no demonstrated benefit, equivalence or broad-transfer conclusion. It is not pooled with any other study.

The unchanged evidence preserves the actual one-word prompt deviation in T2 repeat 1 C and its unknown impact. Actual serving model/build and realized tool/instruction exposure remain unknown, and sealed isolation was not established. Public prompts are labeled projections, not historical dispatch transcripts. The package's [methods](studies/transfer-2026-10-07/METHODS.md), [provenance](studies/transfer-2026-10-07/PROVENANCE.md) and [complete results](studies/transfer-2026-10-07/RESULTS.md) retain these limits.

## Reviewed authored routing regression

The [task-routing contract regression](contracts/task-routing/README.md) contains 12 fictional requests, ten frozen candidate guides plus the router, and 39 authored controls. Two source-first author reviewers approved all control labels after the v2 clarity recheck. Its read-only checker validates packaging and response shape while leaving semantic adequacy null. These are authored contracts, with zero model trials; they are not measured guide efficacy and are not pooled with study results.

## Verify locally

Run the core checks for the original fixtures and two original artifact studies from the repository root, using POSIX Python 3.12:

```sh
python -I -B evaluation/verify.py
```

This standard-library entrypoint does not include the separately verified calibration, engineering or transfer packages below. It runs the following core checks in a fixed order:

1. The earlier study's attempt/schedule identities, task assignments, prompt-hash agreement, 350 saved grading-source hashes, and three source-config/manifest hashes
2. Source/link checks and the original 180 authored fixture tests: 61 harness and 119 case/grader tests
3. All immediate evaluation regression modules: navigation, report-consistency, and verifier regressions
4. The earlier study's saved-evidence scorer
5. The repeated study's saved-evidence verifier
6. `report.py --check` for table, condition-label, and caveat consistency

Each top-level subprocess command and its output are shown. Failed checks are named, later checks still run, and any failure produces exit status 1. Each top-level subprocess has a 15-minute timeout; the original fixture subprocesses retain their 2-minute timeout. An interruption returns 130 and leaves the remaining checks incomplete. Missing or empty required modules, failed imports, and runtime skips fail the harness and evaluation regression stages; nested saved-artifact tests are not discovered. Top-level child interpreters run in isolated mode. Inherited Python settings are removed before every step, so optimization cannot disable the historical verifier's assertions.

The fixture stage calls the unchanged `check.py` workflow, substituting a strict harness test runner in memory. Every known harness module must contribute tests, and skipped tests fail verification. The harness tests run once, followed by the original grader tests. The standalone `check.py` command retains its original behavior.

The added identity and source checks harden verification of the existing records. Attempt numbers must be integer 1 under the declared first-submission policy. Time caps must be positive integers equal to the hash-bound task configuration: 900 seconds for F1–F7 and 1,500 seconds for F8. These checks do not change saved scores or add agent runs. Exact orchestration prompts remain unpublished: comparing their saved hashes does not reconstruct or independently verify their contents.

## Reproduce the saved accounting

The original commands remain available:

```sh
python -I -B evaluation/studies/repeated-stress-2026-10-06/reproduce_saved_evidence.py
python -B evaluation/results/native-cloud-2026-10-06/score.py
python -B evaluation/check.py
```

- The first command verifies the repeated study's published hashes, saved requirement outcomes, review agreements, and pair/summary arithmetic.
- The second verifies the earlier study's evidence bindings and recomputes its saved-rating counts.
- The third runs only the original source/link and fixture checks. It does not invoke either study verifier or the report/navigation regressions.

The native result tables are derived from the saved JSON with a separate read-only [report tool](report.py). It checks five complete tables in four reports: the overview, repeated-study case and evidence-type tables, complete results index, and 24-row submission ledger. Whole-table comparison rejects missing, duplicate, reordered, or extra rows, including a pooled-total row. It also checks condition labels, dispatch order, saved artifact links, selected numeric statements, and required caveats. Run it and its regression tests:

```sh
python -I -B evaluation/report.py --check
python -B -m unittest discover -s evaluation -p test_check.py -v
python -B -m unittest discover -s evaluation -p test_report.py -v
python -I -B evaluation/verify.py --tests-only
```

Running `python -I -B evaluation/report.py` without `--check` prints the current tables; it does not rewrite reports or evidence.

The report tool binds repeated-study counts to its saved summary, scheduled attempts, and requirement definitions. The earlier study's separate index row is checked against its saved criterion groups and paired summary; its attempt identities, conditions, cases and ordinals must match its saved schedule. Evidence-type denominators count scheduled requirement instances by their declared mode, including failures and not-assessed outcomes; they do not count review votes or add overlapping raw and semantically integrated grading reports. The index keeps the studies' different units and denominators separate.

The checked reports use a small plain-Markdown subset. Table detection includes rows and tables without outer pipes, including one-cell body rows. Tables must be separated by blank lines; all nonblank body lines are retained for comparison. Fenced code examples cannot satisfy a report table or prose guard. HTML, HTML comments, and other angle-bracket constructs outside valid code fences are unsupported and fail the check; deleting them could otherwise make hidden text appear to be a visible table, caveat, or code fence. This is intentionally not a general Markdown renderer.

This is bounded consistency checking, not a general prose fact checker or a fresh evaluation. Selected count statements and exact caveat text are guarded; arbitrary new prose, business-value examples, semantic judgments, and provenance claims still need review. Full source/artifact hashes and review evidence remain the responsibility of the saved-evidence verifiers above. No historical study file is regenerated.

These commands make no model calls and install nothing. The saved-evidence commands and added binding checks only read saved files; they do not execute submitted code, import graders, or perform a fresh semantic review. Fixture checks use authored local test inputs and subprocesses to test evaluation machinery; their passes are not agent outcomes.

### Verify the separate calibration package

The calibration is not included in the core command above. From the repository root, run:

```sh
python -I -B evaluation/calibration/semantic-2026-10-07/verify.py
```

This separately reproduces package hashes, saved-vote accounting and 14 frozen-grader cross-checks. It executes only the packaged evaluator code against saved data, using temporary review copies; it makes no model calls, does not execute candidate outputs and does not rewrite the package. Keep assertions enabled: do not add `-O` or `-OO`.

### Verify the separate engineering package

The engineering pilot is not included in the core command above. From the repository root, run:

```sh
python -I -B evaluation/studies/engineering-artifacts-2026-10-07/verify.py
python -I -B evaluation/studies/engineering-artifacts-2026-10-07/fixture/verify_freeze.py
python -I -B evaluation/studies/engineering-artifacts-2026-10-07/fixture/selftest.py
```

These commands check the package inventory, hashes and saved-result consistency, the unchanged 47-file author freeze, and 34 author-control tests. They do not regenerate candidate outputs or rerun primary grading; control-test passes are not model attempts. The frozen triage guide's one omitted local example is documented in the [package provenance](studies/engineering-artifacts-2026-10-07/README.md#contents-and-provenance) and exempted only by its exact Markdown source/target pair. Keep assertions enabled: do not add `-O` or `-OO`.

### Verify the separate transfer package

The transfer cohort is not included in the core command above. From the repository root, run its saved-evidence verifier with the reviewed manifest digest:

```sh
python -I -B evaluation/studies/transfer-2026-10-07/verify.py --manifest-sha256 443a359867c2c646d72842c7dc62ef14aadc076b5e087572895ce6ccb59b1401 --self-test
python -I -B evaluation/studies/transfer-2026-10-07/test_verify.py
```

The first command verifies the 129 manifest-covered files, all 24 captured outputs and all 156 saved statuses, and runs 13 authored in-memory controls. The second runs 12 authored filesystem controls in temporary fictional fixtures inside the package directory. Neither command launches agents, executes candidate SQL/code or reruns primary grading; authored controls are not candidate outcomes. The digest pins saved package bytes, not historical execution truth. See the [package's verification and trust limits](studies/transfer-2026-10-07/PROVENANCE.md#saved-evidence-verification-and-freeze).

### Check the authored routing contract

```sh
python -I -B evaluation/contracts/task-routing/verify.py
python -I -B evaluation/test_task_routing_contract_links.py -v
```

These standalone checks verify the public allowlist, exact inputs and authored response shapes, plus the narrow documented copied-guide link exceptions. They do not run models, execute scenarios, or grade semantic quality. The routing package checker is not part of the core verifier or CI workflow.

## Continuous integration coverage

The [Offline evidence checks (partial)](../.github/workflows/evaluation-offline.yml) workflow is deliberately narrower than the complete local verification above. On pushes to main and pull requests targeting main, it checks:

- Pinned source manifests and local evaluation-document links
- Saved accounting for the earlier and repeated artifact studies
- Published report tables, selected count statements and required caveats
- The separate engineering package's saved-result integrity and 47-file author freeze
- The authored action-handoff example's positive and negative controls

It does not run `evaluation/verify.py`, the original harness or F1–F8 grader suites, calibration's frozen-grader cross-checks, or engineering author-control tests. The full core command and the standalone calibration and engineering commands above retain their separate scope. A green CI result means only this listed subset passed for that workflow's checked commit; it is not complete verification, a fresh model evaluation, or evidence of skill improvement.

The job uses Ubuntu and Python 3.12 with standard-library checks, no package installs, no model calls, no supplied secrets and read-only repository permissions. Checkout and Python setup may access GitHub; this workflow does not enforce network isolation. Checks stop on the first failure, so later commands can remain unrun. The workflow has a bounded runtime and does not regenerate saved evidence or publish files.

## Original sealed-pilot scope

The [original sealed protocol](docs/protocol.md) is a separate, unrun design. Its [harness](harness/README.md) has no live launcher; live dispatch remains disabled. The [runtime and review gates](docs/protocol.md#before-model-trials) still need to be met before any sealed model trial.

Do not mount this repository as an evaluated agent's workspace: it contains public answers and scoring sources. Fresh contexts and verified access boundaries are required; directory separation is not a sandbox.

[Methodology](docs/methodology.md) · [Original cases](cases/README.md) · [Pinned packages](packages/README.md) · [Evaluator fixtures](evaluators/README.md)
