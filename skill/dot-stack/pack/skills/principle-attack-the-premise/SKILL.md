---
name: principle-attack-the-premise
description: "Re-examine a shared assumption when repeated fixes fail the same acceptance check; design a discriminating observation before trying another variation."
---

# Attack the premise

Use this when two or more materially different attempted fixes fail the same check while relying on the same assumption. It is a diagnostic reset, not permission to redesign the whole system.

## Find the assumption that matters

1. Record the symptom, the exact failing gate, what changed in each attempt, and the sentence both attempts assumed true. Separate an observation such as “worker A owns 80% of leases” from an explanation such as “leases are returned too slowly.”
2. Check that the failures are comparable: same workload, version, measurement window, and observation method. A broken test harness or changed input is not evidence against the premise.
3. Choose an observation that could distinguish the premise from a plausible alternative. State the predicted result for each before measuring. Preserve the input and a rerunnable query or small diagnostic when practical.
4. For actor imbalance, count work assigned, completed, and retained per actor across comparable runs. Include exposure or capacity, not just totals. Persistent concentration suggests examining role assignment, ownership, or routing before adding another rebalance loop.
5. Change the mechanism supported by the evidence. If unfair assignment causes the skew, consider changing that assignment rather than compensating forever. Check whether ordering, affinity, or ownership makes the asymmetry intentional.

## Limits and stopping conditions

An even census rejects a particular skew explanation; it does not prove that every shared premise is correct. For a parser or authorization failure, a counterexample input or decision trace may be the right experiment instead of an actor census. Stop revising the premise when a discriminating observation supports a mechanism and a realistic reproduction can test the fix. If evidence remains inconclusive, report the competing hypotheses and cheapest useful next observation; do not call a guess the root cause.

## Example and evidence

Applies: two queue-return fixes leave the same worker overloaded. A workload-normalized census shows a dispatcher always assigns that worker expensive jobs. Test a corrected assignment against the original workload and verify both balance and ordering.

Does not apply: a misspelled field causes a reproducible parse failure with a known contract. Correct the field and test it; speculative premise hunting adds no information.

Return the shared assumption, discriminating evidence, supported conclusion, and check result. Keep scope expansion separate from diagnosis.
