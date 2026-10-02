---
name: audit-weighted-quorum-intersections
description: "Check a bounded static weighted-voting configuration for read/write and write/write overlap, produce disjoint witnesses, and compute exact crash-availability failure cuts without claiming protocol correctness."
---

# Audit Weighted Quorum Intersections

## When to use

Use this when reviewing a small replica voting design or testing quorum calculations before they are used in a configuration planner. The result is a check of a supplied finite model. It does not deploy configuration or establish that a storage system implements a correct consistency protocol.

## Required inputs

- Stable replica IDs and positive integer voting weights
- Read and write weight thresholds, including whether equality qualifies
- Whether every subset meeting a threshold is permitted, or additional placement/role rules apply
- Optional unavailable replicas for a concrete crash scenario
- The expected failure model and bounded enumeration size

The workflow below assumes fixed membership, positive weights, threshold equality allowed and arbitrary qualifying subsets. Domain constraints, read-only replicas, dynamic reconfiguration, correlated failures and Byzantine faults need different or additional analysis. Do not silently discard those constraints.

## Workflow

### 1. Freeze and validate the model

Require unique IDs, exact positive integer weights and thresholds between one and total weight. Keep display labels separate from identity if labels can change. Record membership, weights and both thresholds together so a witness cannot be interpreted against a different configuration.

Choose a small explicit size bound before enumerating subsets. Twelve replicas require 4,096 subsets and are practical for a simple local checker. Larger input is not evidence of failure or safety; use a suitable exact method or return the unsupported size. Avoid floating-point comparisons for fractional weights; either obtain an exact rational representation or leave the result unresolved.

### 2. Separate intersection from availability

Intersection asks whether all permitted pairs share at least one replica. Availability asks whether the currently reachable replicas have sufficient weight to form a quorum. These are different questions: a configuration can have guaranteed intersection but become unavailable when one heavy replica fails.

Evaluate read/write and write/write intersection separately. A low read threshold may overlap every write quorum even when two write quorums can be disjoint, or vice versa. Do not silently add read/read overlap as a requirement unless the design calls for it.

Keep configured-membership proofs separate from a selected crash scenario. Marking a replica offline does not rewrite the voting rules or grant the remaining replicas new weights.

### 3. Find disjoint witnesses exactly

For thresholds A and B and full replica set U, enumerate each subset S. Compute its weight and the weight of U minus S. If weight(S) is at least A and weight(U minus S) is at least B, those two sets are a disjoint qualifying witness.

This complement check is complete for the stated positive-weight, unrestricted-threshold model: if disjoint qualifying sets S and T exist, T is contained in U minus S, whose weight is therefore at least that of T. It need not find a minimal witness; label returned sets accordingly.

If every subset is exhausted without a witness, all qualifying pairs intersect for this model. If enumeration is interrupted, report incomplete rather than guaranteed overlap. Return the replica IDs, both weights and both thresholds with any counterexample.

A threshold sum greater than total weight is a sufficient shortcut for intersection. Its converse is not valid for arbitrary discrete weighted nodes: failure of that inequality does not itself prove disjoint quorums exist. Use exact enumeration when the shortcut is inconclusive.

### 4. Calculate crash availability and a smallest outage

For a concrete set of unavailable replicas, sum the remaining weights and compare separately with read and write thresholds. Describe this as availability under the supplied crash scenario, not a measurement of a live service.

To find the fewest arbitrary replica failures that make a threshold unreachable, sort positive weights descending and remove them until remaining weight is strictly below the threshold. This greedy calculation is exact for minimizing the number of failed replicas: among all sets of k failures, the k heaviest remove the most weight. Retain a concrete failure witness and the remaining weight.

If k failures can first break availability, the configuration tolerates any k minus one replica failures in this model. This does not mean every k-failure combination breaks it. Rack, region or shared-power failures require grouping and a different objective; do not count each correlated replica as an independent failure event.

### 5. Present bounded evidence without hiding computation coverage

Optionally enumerate inclusion-minimal quorums: a qualifying set is minimal if removing any one member makes it fail the threshold. Distinguish inclusion-minimal from minimum cardinality or minimum weight.

If the UI displays only a prefix of minimal quorums, show both displayed and full counts. A presentation cap must not silently cap the computation used for an exhaustive conclusion. Invalidate exports when membership, weights, thresholds or the selected crash scenario changes.

### 6. Cross-check before relying on the result

For small fixtures, use an independent pairwise oracle that constructs all qualifying subsets and checks their actual set intersections. Compare the complement method against that oracle. Independently enumerate failure subsets and compare their minimum cardinality with the descending-weight calculation.

Cover unequal weights, exact threshold equality, one replica, an unavailable heavy replica, disjoint witnesses and a display-truncated family. Validate exported witnesses against the exact exported input rather than trusting derived Boolean flags.

## Worked examples

Three replicas A, B and C each have weight 2. Read and write thresholds are both 3. Total weight is 6, so the threshold sum is not greater than total weight. Nevertheless, every quorum needs at least two replicas. Any two such subsets of three replicas overlap. Exact enumeration returns three inclusion-minimal quorums: AB, AC and BC. It would be wrong to call this configuration unsafe solely because 3 + 3 equals 6.

By contrast, four replicas of weight 1 with both thresholds 2 admit disjoint quorums AB and CD. Each has weight 2 and their intersection is empty. This proves a missing intersection property, not an observed split-brain incident in a running system.

For weights 5, 1, 1, 1 and threshold 5, every quorum contains the heavy replica, so configured quorums intersect. Losing that one replica leaves weight 3 and makes the threshold unreachable. The smallest crash outage is one replica, even though there are four replicas in total.

The bounded implementation used to develop this workflow was compared with independent pairwise and failure-subset enumeration on 310 threshold/weight cases. That finite test coverage checks the implementation, not arbitrary distributed protocols.

## Deliverable and stopping point

Return the frozen model, each intersection result, disjoint witnesses when present, concrete crash availability, smallest outage witnesses, enumeration coverage and unsupported assumptions. Conclude only at that mathematical scope. A deployment recommendation additionally requires protocol behavior, failure-domain placement, membership-change handling, operational evidence and the user's authorization for any external change.
