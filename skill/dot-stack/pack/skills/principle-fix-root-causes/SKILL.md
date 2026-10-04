---
name: principle-fix-root-causes
description: "Diagnose a reproduced defect through causal evidence, repair its mechanism, and check related instances without confusing containment with a lasting fix."
---

# Fix root causes

Use this when debugging an observed failure. Aim for a mechanism that explains the reproduction and predicts what the repair will change. Repeating “why” is useful only when each answer has evidence.

## Build the causal chain

1. Capture the failing input, environment, observed result, and expected behavior. Distinguish a reliable reproduction from a one-time report. Preserve evidence before changing state.
2. Trace the earliest violated invariant. Form competing explanations and inspect the values, events, or ownership transitions that distinguish them. Add targeted, non-sensitive instrumentation when existing evidence is insufficient.
3. Repair the cause at the layer that owns the invariant. A guard is appropriate for expected missing data or an actual trust boundary; it is inadequate when it merely hides corruption and claims success.
4. Keep a regression check that fails for the original defect and passes after the repair. Check the surrounding successful path as well as the failure path.
5. Search for the same mechanism in nearby code and callers. Fix related instances within the authorized scope; report a wider migration or unrelated subsystem separately.

For failures after restart, inspect persisted configuration, schema versions, caches, locks, and partial writes. Recovery after clearing a file suggests a state interaction, not proof that deleting that file is the correct fix. Use a copy or isolated fixture when possible; do not destroy production evidence or user data to test a hypothesis.

## Containment is sometimes necessary

A bounded workaround can protect users while a deeper repair is unavailable. Name the degraded behavior, monitoring, owner, and removal condition. Preserve a rationale comment for a genuine external limitation. Do not reject an effective incident mitigation merely because it is not the final architecture, or present it as a demonstrated root-cause fix.

## Example and counterexample

Applies: restart loads a half-written cache record and crashes. Reproduce with that record, make persistence atomic or reconciled, validate restored state, and verify restart after an interrupted write.

Does not apply: an optional result is legitimately absent. Return the documented empty state and test it; inventing an upstream defect would violate the contract.

Stop when the causal prediction and regression checks hold for the relevant surface. If evidence is inconclusive, return the hypotheses and next diagnostic rather than a confident narrative.
