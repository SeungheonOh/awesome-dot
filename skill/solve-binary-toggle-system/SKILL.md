---
name: solve-binary-toggle-system
description: "Solve a supplied finite on/off toggle problem over GF(2), verify the returned presses, and distinguish any solution from a proven minimum."
---

# Solve a binary toggle system

## When to use

A task requires a valid toggle sequence or a reproducible solvable test instance, not a new game interface.

## Required inputs

- Current binary state, target state and exact press influence rule
- Board or graph dimensions and stable element ordering
- Whether minimum press count is required and a practical search bound

## Workflow

1. Construct one influence matrix whose columns represent presses. Set the right-hand side to current XOR target. Check boundary neighborhoods against the supplied rule.
2. Gaussian-eliminate the augmented system using XOR. An all-zero coefficient row with right-hand side one proves inconsistency under this model.
3. Extract a particular solution and free-variable basis. Enumerate the free-variable family only within the agreed bound when minimizing Hamming weight; otherwise report a valid solution with minimality unverified.
4. Apply the returned presses through the original influence rule and compare the complete final state with the target. Repeated presses cancel; this does not excuse an incorrect matrix.
5. If generating test instances, start at a known target and apply recorded seeded presses. Keep the seed, ordering and press rule with the instance.

## Output

A press sequence, resulting state, consistency verdict and explicit minimum/valid-only status, or a demonstrated inconsistent system.

## Verification and limits

Check double-press cancellation and press commutativity. For small cases, compare with an independent enumeration. JavaScript bitwise operators truncate at 32 bits; use a representation that fits the actual system.
