# Results and status

**No model trials have run. No skill-effect or productivity estimate is available.**

As of 2026-10-05, the public suite is prepared and its local source/fixture checks pass:

| Check | Result | What it establishes |
| --- | --- | --- |
| Harness tests | 61 passed | Scheduling, accounting, parser/reporting, and boundary-check behavior on authored fixtures |
| Case/grader tests | 119 passed | Reference/control behavior across eight authored cases |
| Task/input manifest | 52 files verified | Original packet bytes preserved |
| Designated package manifest | 19 files, 171,703 bytes verified | Exact treatment source snapshot preserved |
| Source configuration inspection | Passed; runtime fields pending | Local sources resolve; the study is not executable |
| Model attempts | 0 | No observed model outcomes |
| Live dispatch | Disabled | No launcher or override is provided |

Reproduce the local checks with `python -B evaluation/check.py` from the repository root. The case counts are F1: 10, F2: 9, F3: 22, F4: 24, F5: 9, F6: 13, F7: 18, F8: 14. These test-method counts do not include every subtest or nested fixture assertion.

The 16-attempt pilot is planned, not started. Supported startup, candidate isolation, adequate process-review evidence, runtime/event verification, and safe F8 behavioral grading remain open gates. See the [protocol](../docs/protocol.md#before-model-trials).

When an authorized study runs, publish the frozen source/runtime identities and schedule, every scheduled attempt's status, paired outcomes, unknown/missingness accounting, review provenance, observed elapsed time, and provider-reported usage coverage. Keep fixture tests, transport preflight, and model outcomes separate. Do not turn not-run or unknown results into a 0% acceptance rate.
