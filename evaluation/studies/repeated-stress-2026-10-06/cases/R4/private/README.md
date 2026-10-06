# R4 evaluator interface

Explicitly fictional, authored offline Python maintenance case. Candidate cap: 1500 seconds. Candidate packet is ../candidate only. Never expose this private directory during the task.

Submission: candidate/output/merge_workspace.py (or the same relative path in a trial copy). Thirteen atomic outcome checks are specified in manifest.json and public TASK.md. No style score. `probe.py` uses literal expected text and independent constructed edits, not the reference merge algorithm. It never imports reference.py.

## Phase 1: no-execution static report and exact owned copies

Choose a new evaluator-owned work directory whose parent already exists, then run:

    PYTHONDONTWRITEBYTECODE=1 python private/evaluate.py static --submission /absolute/trial/output/merge_workspace.py --work-root /absolute/evaluator/new-review

This bounded no-follow read parses source via AST without importing it, inventories imports/review flags, checks protected packet hashes, and copies exact source plus harness into work-root/reviewed. It writes static_report.json and plan.json, prints the exact plan hash, and leaves all behavioral outcomes unknown. An AST inventory is advisory; it is neither proof of safety nor an implementation-style test.

## Phase 2: reviewer approval followed by separate behavioral probe

The root reviewer must inspect the exact reviewed/source.py, reviewed/probe.py, evaluator runner, static report, and plan. Approve only a bounded consumer using standard-library code with effects inside the evaluator-owned directory. No network, credentials, production, candidate subprocesses, or external file operations are permitted. This is an execution safety boundary, not OS/process isolation. Resource limits are backstops, not a security sandbox.

After explicit root approval, record approval.json with approved=true, approved_by="root" (or "/root"), and plan_sha256 equal to the exact approved plan hash. Do not create that approval from a successful static report, infer it from an old approval, or let the candidate approve itself.

    PYTHONDONTWRITEBYTECODE=1 python private/evaluate.py run --plan /absolute/evaluator/new-review/plan.json --approval-file /absolute/evaluator/approval.json

The runner verifies the exact source, harness, runner, command, bounds and plan hashes before import. It runs the owned copy with -I/-B, 30-second wall/20-second CPU bounds, 512MiB address space, 8MiB per file, and 64 open files. The probe uses disposable fixtures only under work-root/tmp. Logs/results remain under work-root. Behavior is reported in behavioral_report.json. A denied, changed, timed-out, or uncompleted run remains ungraded/unknown, not a fabricated failure. The runner does not automatically retry or broaden access.

The failed-save probe patches os.replace, os.rename, and direct module aliases; if an alternate implementation uses no observable supported primitive, that check remains unknown for separate review. It is never failed merely for an alternate implementation strategy.

## Author-owned validation only

    PYTHONDONTWRITEBYTECODE=1 python private/probe.py --module private/reference.py --root private/tmp/reference-fixtures --result private/reference_result.json
    PYTHONDONTWRITEBYTECODE=1 python private/validate_controls.py

These paths are only for the authored reference/compact controls, never unreviewed submissions. Saved reference_result.json shows 13/13. control_results.json records nine caught negative controls plus a nonblocking FIFO reference regression. Positive_controls.json records valid os.rename and imported-alias save alternatives. No candidate model trials or publication were performed by the author.

The successful approval-gate run itself is intentionally not self-approved by the author. Its source and static phase are reviewable; production behavioral execution requires the root approval above. manifest.json freezes input/deliverable/scoring source hashes and validation evidence; temporary files and the manifest itself are excluded.
