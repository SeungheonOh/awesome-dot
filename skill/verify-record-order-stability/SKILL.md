---
name: verify-record-order-stability
description: Verify sorting or ordered-data transformations with duplicate keys by tracking record identity, testing tie policies and distinguishing an observed result from an algorithmic guarantee.
---

# Verify record order stability

## When to use

Use when a data pipeline, table sorter, ranking implementation or algorithm trace must preserve a meaningful order among equal keys. Comparing only the final key values can hide lost records, duplicate records or reordered ties.

## Required inputs

- Records with independent identities and the exact comparison key
- The required ascending/descending and tie-breaking policy
- Whether original order must survive equal comparisons
- Bounds and whether the output includes intermediate operation traces

Do not add a new business tie-breaker merely to make tests deterministic. A stable sort and a sort with an explicit secondary key are different contracts, even if one example produces the same order.

## Workflow

### Preserve identity before transforming

Give each test record an immutable identity independent of its key. Keep an untouched input snapshot. Duplicate keys must remain distinguishable; testing with only distinct values cannot expose tie-order failures.

After transformation, separately check sortedness, identity permutation and original data association. A sorted key list alone does not prove all input records survived exactly once.

### Establish the tie contract

For stability, compare the output identity sequence within each equal-key group to its sequence in the input. Original indices are useful fixture identities, not durable IDs for real records across unrelated loads.

Inspect comparison and movement rules. Adjacent-swap insertion that moves only strictly inverted neighbors preserves equal keys; changing the comparison to include equality loses that property. A distant minimum swap can reorder equal records even when the minimum search picks the first matching value.

### Use an independent expected result

For bounded fixtures, compare with an independently implemented reference or explicit expected permutations. An oracle can order by primary key and original index to express expected stability. Keep that test oracle separate from the production comparison routine.

Include all-equal inputs, alternating duplicates, already sorted and reverse inputs, signed values, a single record and the maximum supported size. Exhaustive small alphabets are especially useful because they naturally generate many duplicate-key arrangements. Retain a minimal counterexample when a tie policy fails.

### Audit traces when the product exposes them

For each comparison-only state, require unchanged records and the expected counter increment. For each swap, reconstruct the next identity array from the previous snapshot and the two recorded indices. Check that historical snapshots cannot be changed by later mutation. Final correctness does not prove the displayed explanation is faithful.

Counters must be labeled as the chosen implementation's operations. They are not runtime benchmarks. Playback timing is a presentation choice, not execution time. Test step, back, seek, restart, end-of-playback and late callbacks after input replacement through the real caller or a clearly labeled simulated consumer.

## Worked example

Input records are 2A, 2B, 1C. A minimum-swap selection pass exchanges 2A with 1C, producing 1C, 2B, 2A. The values are correctly sorted, every identity survived, but equal-key order was reversed. The stability check must fail even though a value-only test passes.

Strict adjacent-swap insertion produces 1C, 2A, 2B and preserves the tie order. Selection may preserve ties on another input; that observation does not make the algorithm stable in general.

## Output and limits

Report the comparison policy, identity checks, tie-order result, exercised input space and any unverified consumer behavior. A finite test corpus supports implementation confidence but is not a proof for unbounded inputs. Keep analytical guarantees distinct from fixture observations.
