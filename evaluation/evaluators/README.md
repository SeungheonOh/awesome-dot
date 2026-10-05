# Evaluator fixtures

**Answer keys and test controls: keep outside candidate access.** These files are public so the benchmark can be inspected and reproduced. Public availability does not permit an evaluated attempt to read them.

Each `F1`–`F8` directory contains a grader, oracle/rubric assets, trusted packet hashes, accepted reference artifacts, deliberately defective controls, and local tests. Controls remain explicit files so reviewers can inspect the exact differences and reproduce the original hash-bound checks. Duplicate task packets and historical validation logs are omitted.

Run all local fixture checks from the repository root:

```sh
python -B evaluation/check.py
```

Or run one case, for example:

```sh
python -B -m unittest discover -s evaluation/evaluators/F5 -v
python -B -m unittest discover -s evaluation/evaluators/F4 -p checks.py -v
```

The 119 case/grader tests use original authored fixtures only. Synthetic review JSON tests grading integration, not the accuracy of an independent reviewer. Controls labeled accepted are expected fixture outcomes, not results of a model study.

F1–F4 use `grade.py`; F5–F7 use `grader.py`; F8 uses `grade.py`. Command-line argument details are available via each script's `--help`. The harness does not execute these graders automatically: it exports blind artifacts and imports structured grade records.

F8's normal `grade()` and CLI perform static integrity checks and leave behavior pending. `grade_author_fixture()` is restricted to exact hashes in its author fixture allowlist; it must never be extended to authorize model submissions. Its subprocesses are fixture-testing tools, not an isolation boundary. Any future execution of untrusted Python requires a separately reviewed adapter.

Do not regenerate the frozen F3 fixture or alter trust hashes merely to make tests pass. The included authoring helpers document fixture construction; changing a task requires deliberate versioning, independent oracle review, and regenerated manifests under a new protocol.
