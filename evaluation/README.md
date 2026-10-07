# Evaluation

Saved task outputs, requirement-level evidence, and local checks for this repository. The two completed studies found no difference on their predeclared primary artifact checks. They do not establish general equivalence or productivity gains.

## Latest result

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

The [earlier eight-case study](results/native-cloud-2026-10-06/README.md) contains 16 submissions and 40/40 primary criterion groups per condition. Its separate post-hoc save failure remains documented. Its scores are not pooled with the latest study. See the [complete results index](results/README.md).

## Separate grader calibration

The exploratory [semantic grader calibration](calibration/semantic-2026-10-07/README.md), dated 2026-10-07, checks grader behavior on 14 related synthetic outputs. It contains no skill intervention and estimates no skill uplift; its votes are not pooled with either study. Shared-filesystem masking, label-aware gold review, sparse negative examples and unknown serving models limit its interpretation. The package preserves all raw reviews and methodological limitations.

## Verify locally

Run the complete local verification from the repository root, using POSIX Python 3.12:

```sh
python -I -B evaluation/verify.py
```

This standard-library entrypoint runs the following checks in a fixed order:

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

The calibration is not included in the unified command above. From the repository root, run:

```sh
python -I -B evaluation/calibration/semantic-2026-10-07/verify.py
```

This separately reproduces package hashes, saved-vote accounting and 14 frozen-grader cross-checks. It executes only the packaged evaluator code against saved data, using temporary review copies; it makes no model calls, does not execute candidate outputs and does not rewrite the package. Keep assertions enabled: do not add `-O` or `-OO`.

## Original sealed-pilot scope

The [original sealed protocol](docs/protocol.md) is a separate, unrun design. Its [harness](harness/README.md) has no live launcher; live dispatch remains disabled. The [runtime and review gates](docs/protocol.md#before-model-trials) still need to be met before any sealed model trial.

Do not mount this repository as an evaluated agent's workspace: it contains public answers and scoring sources. Fresh contexts and verified access boundaries are required; directory separation is not a sandbox.

[Methodology](docs/methodology.md) · [Original cases](cases/README.md) · [Pinned packages](packages/README.md) · [Evaluator fixtures](evaluators/README.md)
