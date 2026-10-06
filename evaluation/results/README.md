# Results and status

**Actual native-cloud study: 16 attempts, eight paired cases, no measured primary-criterion uplift.** Both arms passed 40/40 artifact criterion groups, producing eight ties. A post-hoc F8 robustness check found a save failure in the package-supplied artifact. [Full results, exact artifacts, and limitations →](native-cloud-2026-10-06/README.md)

Three records must stay separate:

| Record | Observed status | What it establishes |
| --- | --- | --- |
| Local authored fixture checks | 180 passed: 61 harness + 119 case/grader tests | Evaluation machinery behaves as tested on authored fixtures; no model calls |
| Native-cloud exploratory study, 2026-10-06 | 16 actual first submissions; 8/8 primary artifact checks passed in each arm | Descriptive artifact outcomes on these eight cases; full process acceptance unknown |
| Original sealed CodexCLI pilot | 0 attempts; not run | Its runtime/isolation gates remain open and live dispatch is disabled |

The native study used separate directories on a shared filesystem with instruction-only boundaries and an ambient runtime. It is not a run of the sealed protocol, a skill-free comparison, a human-productivity benchmark, or evidence of time savings. Exact serving model, tokens, cost, and full process integrity remain unknown. No significance or population claim is made.

## Reproduce the local checks

```sh
python -B evaluation/check.py
python -B evaluation/results/native-cloud-2026-10-06/score.py
```

The first command verifies sources and documentation links and runs 180 authored test methods. Case/grader counts are F1: 10, F2: 9, F3: 22, F4: 24, F5: 9, F6: 13, F7: 18, F8: 14; these counts exclude nested assertions/subtests. It verifies 52 task/input files and 19 pinned package files totaling 171,703 bytes. The second command verifies published evidence and reproduces the native study's saved-rating counts without executing submitted code.

The original pilot's [runtime and review prerequisites](../docs/protocol.md#before-model-trials) remain unchanged. Do not turn its not-run status, or the native study's unknown process outcomes, into a 0% acceptance rate.
