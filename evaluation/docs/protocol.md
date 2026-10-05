# Pilot protocol

The [source configuration](../pilot-source-config.json) records task and package selection. It is deliberately incomplete as an execution configuration. Inspecting it verifies local source assets; it neither freezes a runtime nor authorizes a trial.

## Fixed task setup

- Eight cases, F1-A through F8-A; one control/skill pair each
- C/S arms use the identical common instruction saved in the source configuration
- S receives only its declared package files and the fixed package-read instruction in the harness
- Per-attempt caps: 900 seconds for F1–F7 and 1,500 seconds for F8, identical within each pair
- No further task facts are supplied after launch; the fixed clarification reply is recorded in the configuration
- Task inputs remain protected; requested deliverables go under `output/`
- First submission receives no grader feedback before finalization
- No live accounts, external communications, package installation, or unauthorized network access

Only designated package files are treatment. Cross-links to neighboring skills do not expand that allowlist. Canonical package sources remain outside candidate access; S gets a fresh disposable copy preserving the declared `skill/<name>/...` layout. Helper execution requires separate runtime review and must remain inside the verified boundary and attempt cap. The local preparation checks never execute those helpers.

## Source and execution identity

[Package hashes](../packages/manifest.json) pin 19 files to repository commit `67bb5a82d3d97c1ee1bbbfaa3e695a604c3a0d56`; the live repository may evolve independently. [Case hashes](../cases/manifest.json) bind all 52 task/input files. Evaluator-side trust manifests also bind the protected packet bytes.

An eventual execution freeze includes prompt/input/package/grader dependencies, harness code, runner binary and version, model request, reasoning setting, inventories, caps, and analysis plan. Source paths in this preparation remain relative. A frozen execution protocol intentionally binds absolute paths in a specific validated environment; moving it does not make it portable.

Hashes detect changed content, not malicious storage or deleted ledger tails. Preserve independent copies of the frozen protocol, schedule, and ledger head. Every scheduled attempt receives a ledger record before work begins. A retry cannot replace an earlier record.

## Grading and blinding

Graders evaluate exact structured data and predeclared criteria. Free-text and verification claims require independent source-grounded review. Overall acceptance also requires independent process-integrity review. Review records bind the exact artifact and sanitized evidence hashes; unknown review domains stay null. AI-assisted review must be labeled as such and is not human evaluation.

Blind exports omit arm, guide, timing, and the controller's identity mapping. The artifact itself may reveal treatment. Directory separation and an independence attestation do not enforce blindness or reviewer independence; access controls and procedure must be demonstrated.

F8's normal grading API does not execute submitted Python. It returns pending behavioral results until a separately reviewed isolation adapter exists. Its local tests execute only original exact-hash-allowlisted author fixtures. The SQL evaluator uses a read-only fixture connection, a restricted authorizer, and resource limits; these are not a general Python sandbox. All evaluators still require review for the selected untrusted-submission environment.

## Before model trials

All of the following remain prerequisites:

1. Verify supported runner startup using authorized existing authentication
2. Demonstrate actual candidate read/write and network boundaries, excluding answer keys, sibling attempts, ambient skill catalogs, live accounts, and unauthorized tools
3. Pin CLI/model/reasoning settings and verify surfaced event/usage semantics without relying on model self-identification
4. Verify the selected runtime's required timezone data for the F3 package: Europe/London, America/New_York, and Asia/Singapore
5. Establish a reviewed untrusted-output grading path, especially F8 behavioral evaluation, and adequate process-review evidence
6. Freeze the complete runtime configuration, clarification delivery, source/grader identities, seed, and realized schedule before outcomes
7. Obtain authorization for the exact trial scope and environment

The current harness has no live launcher or override switch. `live-run` always fails closed. Filling missing fields or successfully freezing sources does not close these gates. Do not weaken isolation, alter credentials, or bypass access restrictions to make a run proceed.
