# Transfer cohort saved evidence report

The completed October 7 2026 cohort reached the ceiling on its declared artifact checks in both conditions. All 12 planned first submissions arrived on time; all 24 required output files were captured; all 156 checks passed. T1 C and S each passed 42/42 checks with 3/3 all-met submissions. T2 C and S each passed 36/36 with 3/3 all-met. Both equal-case means are 1.0, and all six paired S-minus-C differences are zero.

This published evidence package preserves the original captured output and grade bytes. It is a separate exploratory cohort and makes no change to historical reports, outcomes or denominators.

## What was compared

- T1: a fictional SQL metering reconciliation task with incomplete coverage, null amounts, signed credits, exceptions and independent source controls
- T2: a fictional engineering action handoff assembled from source threads, with cutoff, ownership, deadline and completion-evidence distinctions
- C: task and source files without the designated workflow package
- S: the same task and source bytes plus the designated guide package, with an instruction to read and apply it

Three fresh repetitions per case and condition were requested. This was ordinary local tool work with procedural allowlists, shared filesystem and ambient tools. Sealed filesystem/network/process isolation was neither enforced nor demonstrated. The source protocol's strict sealed-isolation gate remains unsatisfied. C was not proven skill-free.

## Important qualifications

The observed tie does not establish efficacy, equivalence, speed, cost, population effects, broad transfer or production correctness. Two deliberately authored and heavily specified tasks are a narrow descriptive sample. T1 tests one public parameter scenario and cannot exclude hardcoding. T2's structured checks do not certify free-text meaning or prose usefulness. Native self-reported testing is not trusted execution evidence.

Fresh native sessions with no inherited conversation, requested reasoning effort xhigh and no model override were requested. Actual model/build, realized tool/instruction inventory and hidden access are unknown. First outputs are observer-time bounded snapshots, not atomic generation-time proof.

There was one recorded prompt deviation: T2 repeat 1 C omitted “final” from “return a brief final message.” The first-terminal collection rule remained. Exact prompt parity was imperfect; impact is unknown. The root coordinator explicitly approved continuing the unchanged schedule without correcting, replacing or rerunning that candidate.

## Inspect the evidence

- [Results](RESULTS.md): all 12 submissions and all 156 named statuses
- [Methods](METHODS.md): schedule, capture, grading, metrics and interpretation limits
- [Provenance](PROVENANCE.md): frozen source identities, task-budget amendment, exact-copy allowlist and privacy boundary
- [`outputs/`](outputs/): all 24 original captured output files, unchanged
- [`evidence/results.json`](evidence/results.json) and [`evidence/results/`](evidence/results/): unchanged saved primary results and raw grades
- [`evidence/grading/`](evidence/grading/): unchanged scorer stdout, stderr and process records, plus labeled launch projections
- [`cases/`](cases/): exact original/effective tasks, fictional inputs and authored scoring specifications
- [`designated-guides/`](designated-guides/): the five exact designated public guide files
- [`prompts/`](prompts/): newly authored public task/condition projections, never historical dispatch transcripts

## Verify the saved package

Python 3.10 or newer, standard library only, is sufficient. From the package directory run:

    python -I -B verify.py --self-test

For an externally pinned check, supply the independently reviewed manifest digest:

    python -I -B verify.py --manifest-sha256 REVIEWED_DIGEST --self-test

Optional authored filesystem controls can also be run with:

    python -I -B test_verify.py

Those controls create and clean temporary fictional fixtures inside the package directory. They test only the saved-evidence verifier and do not run agents or primary graders.

The verifier hashes the exact file inventory and captured outputs, reconciles the saved raw statuses and scorer output, checks denominators and descriptive arithmetic, and checks the documented task-budget replacement and observation chronology. It never executes candidate SQL/code, graders or native dispatch. Its positive/negative self-tests are authored checker controls, not evaluated-agent evidence.

Without an independently obtained manifest digest, this is internal consistency checking rather than authentication. Even a pinned digest authenticates these saved bytes only; it does not independently prove historical execution, source access isolation, or semantic correctness. No live runner or primary grading replay is included.
