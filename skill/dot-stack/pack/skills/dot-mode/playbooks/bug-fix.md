# Bug fix

Use for a reported defect the user wants corrected. Read the [execution contract](../references/execution-contract.md). Keep repairs supported by the observed mechanism; distinguish emergency containment from a root-cause fix.

## Inputs

Expected behavior, observed symptom, affected version/environment, reproduction conditions, writable scope, and the smallest meaningful regression gate. Preserve the starting revision and unrelated work.

## Steps

1. Reproduce through the boundary where the bug occurs. Use the existing API/CLI harness for those surfaces; use a supported app driver for UI behavior. Capture input, output, environment, and the failing predicate. If direct reproduction is unavailable, narrow conditions or instrument within scope. Ask for user-provided evidence only when the required surface cannot be reached, naming the specific limitation.
2. Build competing causal hypotheses. Read the relevant path and regression history where accessible. Choose an observation that separates hypotheses rather than stacking speculative fixes. Check state transitions, ownership, boundary validation, and timing. Remove temporary instrumentation when it is no longer needed.
3. Confirm the mechanism with a minimal reproducer, failing test, trace, or controlled change. If no cause is confirmed, deliver the diagnosis and gap instead of representing a defensive patch as a proven fix. For an active incident, a reversible containment already within scope may still be useful: verify its observable effect, disclose degraded behavior and the unresolved cause, and name the removal condition. Containment does not grant rollback or deployment authority.
4. Design the smallest correction to the responsible contract. Compare designs only when the boundary or blast radius warrants it. A delegate, when useful, gets exact paths, the failing receipt, the invariant to preserve, and acceptance checks. One writer owns the integrated fix.
5. Where cheap, use [tdd](../../tdd/SKILL.md): demonstrate the regression check fails for the intended reason on the original candidate, then passes with the fix. Keep failing evidence even if a red intermediate commit would violate repository policy; a failing-test commit is not compulsory.
6. Repeat the original reproduction on the corrected candidate. Run nearby positive, negative, and integration cases based on risk. Check every consumer of a changed shared primitive. Review the final diff for speculative changes, accidental scope, and leaked diagnostics.
7. Deliver the patch and proof. Use [Opening a PR](opening-a-pr.md) only when publication is authorized. A local fix does not automatically start PR monitoring or shipping.

## Failure and recovery

An inconclusive or wrong-surface result remains unverified. If a hypothesis is refuted, remove only its owned edits, preserving others' work. Repeated failed fixes trigger a premise review, not more guards. A pre-existing unrelated failure is reported with baseline evidence; do not quietly weaken the gate. Stop dependent actions on missing permission or an unsafe shared-writer conflict.

## Evidence and completion

Report what was broken, the established cause, the change, failing-to-passing evidence, current candidate identity, and residual risk. Quote only the useful output, with full logs as artifacts when available. The task is done when the requested defect is corrected and its acceptance checks are verified, or a precise remaining blocker is handed back.
