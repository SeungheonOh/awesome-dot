# Operational addendum

## Administrative bootstrap change after dispatch began

Attempts T01–T04 received the frozen original bootstrap text with trailing line-feed bytes removed for dispatch. Beginning with T05, the coordinator appended the same administrative reporting and permission-handling paragraph to both conditions. The added paragraph supplied no task facts, correctness hints, scoring changes, or additional tool authority. The controller reports that the underlying higher-priority rules already applied to all attempts.

This is a post-start prompt deviation. Exact frozen task prompts and bootstrap files remain unchanged. For all attempts, the operational audit distinguishes the frozen file bytes from the controller-reported dispatch text; from T05 onward, it also records the appendix and effective-bootstrap hashes separately; they must not be substituted for the original freeze hashes. Effective message hashes are reconstructed from the controller-reported construction rule. For attempts not yet dispatched, these are planned hashes; checkpoint accounting identifies completed attempts. They are not independently captured API payloads. The changed wording may still influence behavior, so prompt identity across the entire study is not claimed. Both members of each case/repeat pair use the same bootstrap variant.

No model attempts are replaced or rerun because of this change. All 24 scheduled rows remain in the denominator. Task/input/package bytes, scoring requirements, schedule, and caps are unchanged. Private administrative wording and coordination messages are excluded from this public explanation and from artifact checkpoints.

## Incremental artifact retention

First-submission artifacts are retained in cumulative Library checkpoints after each four terminal attempts, with all 24 scheduled rows preserved. Each checkpoint includes only the task-specific artifact allowlist and a clean accounting projection. It excludes private dispatch text, final coordination messages, agent identifiers, and unrelated files. Pending rows stay visible, and absent evidence is not labeled a failure.

Checkpoint creation does not grade outputs, establish process isolation, or publish results. Original shared-filesystem, timing, model-identity, and review limitations continue to apply.

## Delayed controller launch record for T24

The first controller logging process for T24 could not start because its transport disconnected. The controller checked that no launch event had been written, then retried only the logging operation against the same intact ledger. The resulting launch record is delayed; there was no replacement candidate or repeated model attempt. The dispatch-intent record was already present, and the final receipt remains bound to the same attempt. The event is retained in the operational audit; its timing is an observation limit, not model compute time.
