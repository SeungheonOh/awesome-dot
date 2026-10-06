# Local evaluation harness

A Python-standard-library scaffold for source identity, paired scheduling, attempt accounting, blind export, and reporting. **This harness has not run a model trial. Its live dispatch is disabled.** A [separate native-cloud study](../results/native-cloud-2026-10-06/README.md) records actual attempts outside this sealed-pilot harness. Its test processes and usage counters are authored test doubles.

The pilot uses `designated_skill_package_supplied`: S gets an exact per-task package allowlist, including the guide and designated examples/helpers; C gets none. The small `examples/fixture_only` demonstration instead uses a synthetic standalone guide to test plumbing. It is not the pilot treatment or benchmark data.

## Commands

From the repository root, using POSIX Python 3.12:

```sh
python -B evaluation/check.py
PYTHONPATH=evaluation/harness python -B -m unittest discover -s evaluation/harness/tests -v
PYTHONPATH=evaluation/harness python -B -m dot_eval inspect-config evaluation/pilot-source-config.json
PYTHONPATH=evaluation/harness python -B -m dot_eval --help
```

No dependency installation is needed. The aggregate check runs the 61 harness tests and 119 evaluator tests, verifies pinned source manifests, and checks local documentation links. The tests use temporary directories and safe authored local fixtures. They do not call a model or run package helpers.

`inspect-config` checks the explicit source selection and reports missing runtime fields. It does not launch a process or produce an execution freeze. `freeze` creates an environment-specific content binding; it is not runtime authorization. `live-run` always returns a blocking error, with no override switch.

For an entirely synthetic ledger/report demonstration:

```sh
DEMO=$(mktemp -d)
export PYTHONPATH=evaluation/harness
python -B -m dot_eval freeze evaluation/harness/examples/fixture_only/config.json "$DEMO/protocol.json"
python -B -m dot_eval plan "$DEMO/protocol.json" "$DEMO/schedule.json" --seed 4071
python -B -m dot_eval init "$DEMO/protocol.json" "$DEMO/schedule.json" "$DEMO/study"
python -B -m dot_eval fixture-run "$DEMO/study" a0001
python -B -m dot_eval fixture-run "$DEMO/study" a0002 --mode failed
python -B -m dot_eval report "$DEMO/study" --output "$DEMO/report.json"
```

Never merge this demonstration ledger with model-trial records. Synthetic studies do not produce an overall skill-effect estimate.

## Implementation

- `protocol.py`: explicit source hashing, validation, balanced C/S scheduling, and allowlisted packet copies
- `execution.py`: authored fixture subprocesses, timing, timeout cleanup, and a fail-closed live gate
- `core.py`: bounded file reads, content identity, and append-only ledger validation
- `telemetry.py`: allowlisted JSONL metrics, logical-item deduplication, per-turn usage, and missingness
- `grading.py`: blind artifact export and immutable ratings/adjudication import
- `reporting.py`: all-scheduled accounting, paired summaries, and uncertainty restrictions by study type

A prepared packet is not a sandbox. The scaffold does not execute graders or generated task code. Its sanitized metric events omit raw reasoning, commands, tool output, and credentials, but are insufficient to certify process integrity. Independent evidence is still needed before that review can pass.

For non-fixture studies, overall acceptance requires separate artifact-bound process-integrity and free-text/verification-claim reviews. Machine group passes alone are insufficient. Missing or untrusted evaluator infrastructure remains unknown rather than becoming a failed submission.

The exploratory pilot reports observed equal-case paired differences with no inferential interval. The code also contains more general analysis functions, tested on synthetic rows; their existence does not authorize use on this small pilot.

See the [protocol](../docs/protocol.md), [methodology](../docs/methodology.md), and [isolation requirements](ISOLATION.md) before adapting the harness.
