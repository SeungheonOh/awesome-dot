# Method, provenance, and limitations

This is a separate, small native-cloud artifact study performed on 2026-10-06. It does not satisfy or claim to execute the original [sealed CodexCLI pilot protocol](../../docs/protocol.md). That pilot remains unrun, and its live-dispatch gate remains disabled.

## What was compared

Eight existing authored fictional cases each received one fresh-context control attempt (C) and one fresh-context package-supplied attempt (S). All 16 first submissions are retained. Both arms received the same task/input bytes, competent common task instruction, requested model inheritance and reasoning effort, allowed local tool scope, self-check policy, and within-case time cap. S additionally received its designated package from repository commit `67bb5a82d3d97c1ee1bbbfaa3e695a604c3a0d56`. C received no designated package. The surrounding runtime could still supply ambient instructions or skills to both arms; this is an incremental package comparison, not a skill-free baseline.

The study requested the same inherited model without an override and `xhigh` reasoning for every attempt. Exact serving model/build, actual backend equivalence, and identical ambient tool/instruction inventories were not independently verified. Those unknowns prevent exact model-level replication claims.

The case order and four C-first/four S-first assignments were seeded and recorded before observed outcomes. [schedule.json](schedule.json) gives every assignment and prompt hash. Attempts launched in that order, with overlap permitted. Caps were 900 seconds for F1–F7 and 1,500 seconds for F8. No grader feedback, repaired submission, best-of selection, or replacement trial was used. No further task facts were supplied after launch.

## Preserved material

- [The 52 task/input files](../../cases/manifest.json) and [19 designated package files](../../packages/manifest.json) remain byte-pinned in the repository
- [provenance.json](provenance.json) binds the original control freeze, source configuration, task/input and package manifests, exact per-attempt prompt hashes, and evaluator sources
- [attempts.json](attempts.json) links each attempt to its exact input/package hashes, frozen artifact files, saved grades, reviews, observation times, and explicit unknowns
- [artifact-manifest.json](artifact-manifest.json) binds all 46 saved artifact files; published artifact bytes are unchanged from the frozen first-submission copies

Task/input and package content is public. The exact orchestration prompts are identified by hash but are not published. This method description is not a byte-identical prompt replacement. The original freeze and audit records are hash-identified; this public report publishes a restricted provenance/accounting projection rather than private execution logs. Hash equality detects content changes at observation time; it is neither proof of a trusted clock nor tamper-proof storage.

## Scoring

Each case has five predeclared artifact criterion groups. Structured checks use the existing case graders. F1, F2, and F4 also use two separately prepared, source-grounded AI-assisted semantic ratings bound to the exact saved artifacts. Their states agree, and both sets of evidence are published under [reviews](reviews/). These are AI ratings, not human evaluation. Review packets used masked artifact labels without the arm mapping, but strict reviewer blindness and independence were not enforced by operating-system access controls; artifact content could reveal treatment.

The saved grade records retain the existing graders' field names. In those records, `accepted` means only that grader's artifact checks passed; it is not verified overall study acceptance. Overall acceptance and process integrity remain null in the public attempt and paired records. Free-text observations and generated self-test claims do not prove what occurred during execution.

F8's behavioral reviewer read the exact submitted Python before independent source-reviewed local execution on owned copies. Its primary score uses the original criteria/probe plus actual full/focused tests and advertised-defect sensitivity. A separate post-hoc lone-surrogate diagnostic does not rewrite the primary score. See the [F8 execution evidence and limitations](f8/README.md).

[score.py](score.py) verifies saved artifact/input/grade/review bindings and reproduces the per-case counts and paired summary. It does not execute submitted code, rerun model attempts, or recreate semantic judgments. Deterministic graders and original rubrics remain in [evaluators](../../evaluators/README.md).

## Timing and missing telemetry

Per-attempt intervals are the differences between controller-observed dispatch confirmation and observed final notification. They include concurrent scheduling, queue, tool, and observation overhead; dispatch confirmation may occur after execution has begun. Several completion observations were grouped. Intervals are approximate observations, not model compute time or exact wall-clock runtime. No speed comparison or time-saving percentage is inferred.

Provider-reported tokens, cost, and exact serving model/build were unavailable and remain null for every attempt. Human work/review time and productivity were not measured.

## Accounting and protocol deviations

The [accounting projection](accounting.json) records all eight cases and 16 attempts, all 16 frozen receipts, paired input equality, unchanged original bound sources, and protected-input/package checks. The audit is post-hoc content verification, not a trusted execution-transcript audit.

1. **Shared filesystem and instruction-only separation.** Each attempt had a separate directory, but there was no independently demonstrated OS-level read/write/network isolation. Prohibited reads, transient edits, interference, descendant-process quiescence, or changes between final notification and collection cannot be ruled out by frozen hashes alone. Process integrity remains unknown.
2. **Dispatch recording differed from the stated sequence.** Dispatch records were appended after launch using immediate post-dispatch observation times, rather than written before launch. The frozen schedule and hash-bound copies support provenance but do not independently prove every event's exact timing or temporal precedence.
3. **Collection changed after the control freeze.** A collector fix created destination parent directories for nested manifest paths. The original copy behavior failed on nested test files. The fix was recorded before F8 collection and separately checked on synthetic fixtures, including rejection of symlinks, hardlinks, symlinked ancestors, and changed source files. Candidate bytes and rubrics were unchanged. The collector remains non-atomic and is not an isolation boundary.
4. **A common F8 instruction overrode the temporary-file location.** The original task requested temporary save files outside the source/output trees; the common dispatch instruction instead directed temporary work under `output/.work` and removal before final submission. Both arms followed the common instruction, and frozen outputs contain no such temporary directory. This is a protocol inconsistency, not an arm-specific candidate failure.
5. **Generated bytecode appeared beside source files.** Two generated bytecode cache files were added during preparation/collection. All 453 originally bound source files remained unchanged; generated caches are excluded from the public source/artifact inventory.

## Interpretation limits

There is one pair per case, with public tasks and answer keys and no independently held-out replication. Absence of direct answer access, prior familiarity, or training exposure cannot be established. The five groups vary by case; pooled counts describe this authored suite and are not interchangeable measures of general task quality. Ties at a ceiling show no measured uplift on these criteria, not proof that skills never help.

There are no inferential confidence intervals, significance claims, population-wide efficacy estimates, human-productivity claims, or estimates of full dot product performance. Local artifacts do not measure real email delivery, bookings, live calendar changes, account access, or native document fidelity. More discriminating independently authored tasks, controlled access boundaries, verified runtime identities, repeated trials, and human review would be needed for stronger claims.
