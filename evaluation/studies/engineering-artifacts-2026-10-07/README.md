# Engineering artifact pilot evidence

This evidence package contains the original synthetic engineering fixtures and graders, pinned guide snapshots, six unchanged first-final artifacts, and the results for all eight planned v2 positions. The source packet passed independent artifact-readiness review; publication integration and release are separate steps.

All four exporter artifacts passed every frozen component. Both captured triage repeat-2 artifacts also passed, with disposition unrun retained. The two triage repeat-1 artifacts were not captured after an infrastructure interruption and remain unknown, one per condition. The captured outcomes do not show a component difference between conditions on these fixtures and cannot establish general guide effectiveness.

## Read the results

| Case | Condition | Planned | Captured | All structured outcomes pass | Infrastructure unknown |
|---|---|---:|---:|---:|---:|
| Exporter | Baseline | 2 | 2 | 2 | 0 |
| Exporter | Guide | 2 | 2 | 2 | 0 |
| Triage | Baseline | 2 | 1 | 1 | 1 |
| Triage | Guide | 2 | 1 | 1 | 1 |

See results/all-results.json for every attempt, raw grader output, observed timing, first-final hash, and missing-result status. results/summary.json reports each component with the original two-position condition denominator. An absent artifact makes the raw grader return discovery=false; for the two infrastructure losses, substantive model outcomes remain unknown rather than being labeled model failure.

Exporter components are valid discovery, accepting both correct implementations, and detecting each of five frozen mutants. All four captured artifacts passed all seven. Their case counts were baseline 21 and 15, guide 16 and 14; a larger case count is not a quality score.

Both captured triage artifacts covered the reported reverse-completion sequence, normal forward completion, and pending-request reset. Each had 16 observation claims agree with the expected and predicted state checks and passed all five structured report checks. Both dispositions remain unrun. The evaluator replayed the data; this does not show that the candidate ran the fixture. Summary and next-check prose semantics were not graded.

## Contents and provenance

- fixture/: all 47 original author-frozen files plus their unchanged freeze manifest, including common tasks, project code, graders, controls, guide snapshots, and author validation tests
- artifacts/: exactly six first-final message strings, copied byte-for-byte as UTF-8 without JSON repair or reformatting
- results/: all eight safe result records and unchanged grader stdout/stderr, plus descriptive aggregates
- prompts/: clearly labeled public projections of task messages and a transformation manifest
- METHODS.json: design, timing, configuration, collection, scoring, and limits
- DEVIATIONS.json: abandoned operational v1, its concurrency deviation, pretrial v2 timing change, and the v2 infrastructure interruption
- verify.py and manifest.json: local consistency and byte-integrity checks

The unchanged triage guide links to WORKED_EXAMPLE.md, which is outside this frozen packet. Read the [pinned public worked example](https://github.com/SeungheonOh/dot-skills/blob/020eebcabf444f18150e912ab44d5d3bde61a16e/skill/bug-reproduction-triage/WORKED_EXAMPLE.md), Git blob 20930b6d0f8f233cb2a3eff4a88896b3e8490ac3. This navigation reference does not add the example to the designated guide or dispatched prompts. The repository link checker exempts only that exact missing source/target pair; it scans Markdown files, not the labeled public-projection text files.

The source fixture manifest is a preserved pretrial snapshot. Its historical candidate_trials_run=0 fields describe author validation, not this later cohort. The later cohort contains eight dispatched positions, six captured artifacts, and two infrastructure losses. Author harness checks and preparation checks are not model trials.

The public prompt projections remove the shared operational wrapper before the first supplied-file marker. Every supplied task/project byte and designated-guide appendix remains unchanged. The projections were not themselves dispatched and must not be represented as exact full prompts. Original full-source hashes are retained in the projection manifest. Operational restrictions are described in METHODS.json; private coordination text and private runtime locations are not included.

## Verification

From this packet directory, run:

    python -I -B verify.py
    python -I -B fixture/verify_freeze.py
    python -I -B fixture/selftest.py

The first command checks package inventory, hashes, byte-identical captured artifacts, unchanged grader stdout, prompt projection structure, and all eight result positions. It does not regenerate model answers or rerun primary grading. The other commands verify the original fixture and its author controls. Their outputs are validation evidence, not new candidate attempts.

For an independent JSON-only replay, place one published artifact at the original case's fixed project path and invoke the unchanged fixture/<case>/trusted/grade.py with that project root, as described in fixture/README.md. Never execute or import candidate-authored code. The original primary grading ran once after every slot closed and used the bounded environment and resource limits in METHODS.json.

## Limitations

This was an exploratory procedural-boundary pilot, not the strict-isolation trial originally described by the author protocol. Native agents shared ambient tools and filesystem access. Task-level tool abstention was requested but was not technically enforced or comprehensively audited. Backend model/version, numerical token limits, full tool traces, and exact backend start times were unavailable. xhigh was requested with the inherited native default model.

The observation budget was 900 seconds after each successful spawn acknowledgement was observed. Inline-transfer and collection latency are recorded; they cannot support speed or equal-compute claims. First-final strings were manually transferred from native messages, not extracted as original transport bytes. Source prompt hashes do not independently prove inline tool-call byte equality.

One coordinator capability interruption caused two unrecoverable first-final captures. Those original attempts were retained without replacement, and the remaining four original unstarted positions continued in order after a same-host handoff. The abandoned v1 cohort was never graded or pooled with v2; its one artifact and seven unstarted positions remain separately documented.

Only descriptive structured outcomes are supported. These two synthetic tasks do not establish production correctness, population effects, overall prose quality, process honesty, candidate execution, or general guide effectiveness. Artifact-readiness review does not establish those unassessed outcomes.
