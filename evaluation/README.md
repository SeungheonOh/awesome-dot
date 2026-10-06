# Evaluation

**Two distinct records:** 180 authored fixture tests check the evaluation machinery, and a [separate native-cloud study](results/native-cloud-2026-10-06/README.md) records 16 actual attempts on eight fictional cases. The originally planned sealed CodexCLI pilot has not run. The native study does not establish human time savings or productivity.

- [Methodology](docs/methodology.md): question, comparison, measures, and limits
- [Protocol](docs/protocol.md): fixed task setup, timing, grading, and prerequisites
- [Cases](cases/README.md): eight fictional tasks and their inputs
- [Pinned packages](packages/README.md): exact treatment files and provenance
- [Harness](harness/README.md): no-install commands and implementation
- [Evaluator fixtures](evaluators/README.md): answer keys, controls, and tests
- [Results and status](results/README.md): what has and has not been measured

## Check it locally

From the repository root, with POSIX Python 3.12:

```sh
python -B evaluation/check.py
```

This runs source-integrity checks, documentation-link checks, 61 harness tests, and 119 case/grader tests. It uses only the standard library and local authored fixtures. It makes no model calls, installs nothing, and does not execute bundled skill helpers. [More targeted commands](harness/README.md#commands) are available.

## Original sealed-pilot scope

The planned pilot has eight cases and one matched control/skill pair per case: 16 attempts. Both arms receive the same competent instruction, inputs, tools, and time cap. The skill arm additionally receives its exact designated package, pinned to [commit 67bb5a82](https://github.com/SeungheonOh/dot-skills/tree/67bb5a82d3d97c1ee1bbbfaa3e695a604c3a0d56). The 19 pinned files include guides, examples, and helpers; this is a package-supplied comparison.

These are public, inspectable benchmark fixtures, including public answers. They are not a permanently held-out dataset. A valid attempt must still have a fresh context and verified access boundaries. New generalization claims require independently authored cases and a new protocol version.

**Do not mount this repository as an evaluated agent's workspace.** The agent must receive only its case allowlist and, for the skill arm, the designated package files. Directory separation is not a sandbox. Live dispatch is disabled, and the remaining [runtime and review gates](docs/protocol.md#before-model-trials) must be resolved before that sealed pilot. The separate native-cloud study reports its weaker instruction-only boundaries explicitly.
