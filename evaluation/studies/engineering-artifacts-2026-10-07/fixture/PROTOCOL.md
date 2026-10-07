# Pretrial protocol: engineering outcome fixtures

## Freeze and review boundary

This packet is an author-side preregistration candidate, not an experiment result.
The frozen contract, runner, graders, output constraints, controls, and guide
snapshots are listed by SHA-256 in freeze-manifest.json. verify_freeze.py checks
all frozen paths plus exact inventory. Independent review must approve the packet
before trial dispatch. Corrections before trials require a newly dated/hash-bound
freeze and recorded review; retain superseded freezes and validation evidence.
No score threshold or hidden expectation may be changed after seeing candidates.

The visible guide sources are pinned to repository commit
020eebcabf444f18150e912ab44d5d3bde61a16e. Their Git blob identities are checked
against the fetched source. Guide treatment means only the designated guide for
the case. Do not include other guides, examples, rubrics, previous evaluations,
hidden mutants, controls, or another candidate's work.

## Arms and dispatch

For each case, use the identical common/PROMPT.md and complete common/project
snapshot in both conditions. Use the same model/version, tool permissions,
artifact format, context budget, token/time limit, and supported execution
environment. The baseline gets no designated guide. The guide arm additionally
gets exactly the pinned guide bytes. Do not disguise extra rubric hints as
"setup" in only one arm. Record the exact dispatched prompt and file hashes.

Trials must use clean isolated candidate workspaces containing only the selected
common material and, for treatment, the one designated guide. The shared author
stage is not a suitable candidate environment: it contains graders and controls.
Keep network access off; no personal accounts, repositories, or other tools are
needed. No candidate is entitled to modify product files. If shell tools are
available, allow the supplied fixture command under the same resource limits in
both arms. Do not execute newly authored candidate program files at grading time.
An artifact-only/no-tools trial is acceptable if both arms receive that same
restriction; identify it as such. It measures source-derived replay claims and
test design, not demonstrated candidate-run behavior.

Trial coordinator must predeclare the model identity, repetitions, paired arm
ordering/randomization, run limits, and dispatch schedule in a separate immutable
manifest before starting. This packet deliberately runs no model trials and does
not claim an established sampling plan. One result from each arm is descriptive,
not a causal population estimate. Do not silently discard failures, truncations,
invalid JSON, missing artifacts, refusals, or scheduler/infrastructure problems.
Report original attempts and any approved retry as distinct, linked attempts.

## Collection and safe grading

Collect the exact allowed relative file, not a candidate-nominated arbitrary
path. Preserve its raw bytes and hash. If the interface returns a single artifact
body instead of a filesystem, the same deterministic extractor must be specified
before dispatch for both arms; do not hand-repair code fences, JSON, or claims.
Missing output is a discovery failure. A wrong-location file is not discovered.
Record prohibited modifications independently rather than running them.

Use a private coordinator-owned staging directory under trusted parents. Copy
only the captured JSON into the fixed output path. Never copy candidate Python
files into the evaluator directory. Invoke the evaluator's frozen grader with
python -I -B, a controlled working directory, a five-second process timeout, and
an environment stripped of inherited PYTHON* settings. Apply the same external
CPU/memory/resource limits to both arms. Freeze and verify grader hashes before
and after scoring. Save stdout, stderr, exit code, status, and output JSON.

The bounded loader caps the file at 65,536 bytes before parsing, refuses final
and intermediate candidate-path symlinks, requires regular files, rejects FIFOs
without blocking, rejects duplicate keys/nonfinite numbers, and checks nesting
before JSON decoding. Case schemas bound actions, records, tests, strings, and
all output data. Invalid shapes are scored as invalid artifacts, not crashes.
The grader does not evaluate expressions, templates, imports, code, URLs, or
commands in artifact strings. Trusted code remains responsible for the task;
"declarative" does not mean candidate content is trusted.

Infrastructure disagreement between the triage product and its independent
oracle is a harness error, never evidence against the candidate. Preserve and
investigate it; do not convert it to a passing or failing candidate result.

## Frozen outcomes and interpretation

Exporter's seven components are separate: valid discovery, correct-program
specificity, and detection of each of the five frozen mutants. Report the two
correct programs' failures and raw mutant failures as diagnostics. A purported
mutation kill earns no qualified credit if any assertion fails either correct
program; otherwise an always-failing test would be rewarded. The summary all-
required flag is conjunctive, never a substitute for component reporting.

Triage separately reports valid discovery, three sequence-coverage checks,
independent expected-state agreement, predicted-state agreement, and five
structured report checks. The product is correct on the supplied reported
sequence. An evidence-bounded no-defect prediction or honest unrun disposition is accepted; invented data loss or
unjustified global certainty loses the corresponding report outcome. Summary
and next-check prose meaning is unassessed. Do not count matching field values
as proof that prose is faithful. No semantic grader is smuggled into this case.

Present case results and original denominators even when inconvenient. These
synthetic tasks cannot establish general engineering reliability, production
correctness, or a guide's effect outside the tested model/task/tool configuration.
No existing/historical evidence should be relabeled, overwritten, or pooled as
if it were produced by this packet.

## Author-side validation already performed

34 tests pass after one prefreeze control-fixture correction. The initial
wrong-saved-state negative control inadvertently changed its expected snapshot
as well, due to an in-memory alias in authoring. The grader correctly rejected
both claims; a selftest expecting only one rejected claim exposed the fixture
mistake. The corrected saved JSON changes predicted state only. Both the first
failed log and later passing log are retained. No candidate output was involved.

Positive and negative controls, selective single-mutant witnesses, schema and
size rejections, untrusted-import non-execution, public-runner discovery, and
independent-oracle checks are covered. The second correct exporter uses a
separately expressed implementation; the controller oracle scans completed
patch history rather than using the product's per-field generation counters.
The oracle agrees across all 24 orders of four saves and 500 reproducible mixed
action scripts, including resets. This is finite validation, not a proof.

## Independent-review correction from v1 to v2

The v1 freeze remains intact and is rejected for trial use. Independent review
found exporter/trusted/grade.py bytes incorrectly copied into triage/common/
project/bounded_json.py (SHA-256 86c7f76e84a69810998142119c83cc2cb7ed3c1e3e16cbf1f3bc866fa79daf8a).
The error came from an authoring script reusing a mutable text variable across
file-copy iterations. The hidden evaluator was unaffected, explaining why the
original 29 tests passed. Candidate-visible isolation and public usability were
not established by that result.

Version 2 copies the actual bounded loader (SHA-256
04d2a2b7dded6f13e5c20e49257a5019bd070431f99ca3be213772ec8dca78ea), runs the triage
public command from an isolated copy with no hidden modules available, verifies
all intended public/trusted file pairs, checks exact common-file inventories,
and prohibits hidden graders/oracles/mutants/control artifacts in common inputs.
A regression audit reuses these new checks against a disposable v1 copy to
establish that the original leaked packet fails them. The first freeze, its
logs, and its original claims are retained unchanged, with no candidate trials.
The revised freeze requires fresh independent approval before dispatch.

Review also found a fairness conflict: v1 allowed no-tools trials and honest
unrun briefs, while its bounded_non_reproduction score demanded not_reproduced.
Version 2 replaces that component with bounded_conclusion, accepting both
not_reproduced and unrun when scope is supplied_fixture_only and all other state
and report checks pass. Grading output retains submitted_disposition verbatim.
An honest-unrun positive control verifies this; it does not assert candidate
execution, and candidate execution provenance stays unassessed.
