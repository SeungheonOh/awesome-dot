---
name: tdd
description: "Create a focused failing-before and passing-after regression check for a bug when a practical test path exists, preserving real behavior and boundary coverage."
---


# Test-driven bug repair

Make the broken behavior executable before changing production code when the user requests it or a cheap clear regression path exists. Prefer the narrowest meaningful test already supported by the repository. Do not build a large brittle harness solely to satisfy a ritual.

## Reproduce the contract

Identify expected behavior, observed failure, relevant source revision, and the smallest public or domain-level operation that exposes it. Read nearby tests and the actual implementation. A regression should fail because the contract is violated, not because an import, dependency, fixture, or service is missing.

Write a test with literal expected outcomes: returned value, emitted event, persisted state, rendered behavior, rejected malformed input, or type-check result. Avoid reproducing the algorithm in the expectation. Do not overmock the boundary under investigation. Use the real compiler for type claims, real parsing for boundary claims, and the actual domain operation for behavior claims.

## Demonstrate red, then green

1. Add the focused regression check against the baseline
2. Run it and retain the failure proving the intended bug
3. Make the smallest authorized repair at the owner of the broken contract
4. Run the same regression and verify it passes without weakening its assertion
5. Run relevant neighboring and integration checks against the final candidate

If tests and implementation have different owners, finish the baseline run before the production writer starts, or run against a fixed isolated baseline. Record which source and assertion bytes ran; a concurrent edit can turn a claimed red run into evidence about neither candidate. After a review-driven repair, rerun the new counterexample and affected existing cases on the integrated candidate.

If the candidate was already edited, safely reconstruct the baseline in an isolated location when practical. Do not reset user work to manufacture a red run. If baseline execution is impossible, disclose that missing evidence rather than claiming the test was red.

For flaky behavior, control the clock, scheduler, seed, or fixture using existing supported test seams. Repetition alone does not make an intermittently passing test reliable. Test cancellation, repeated actions, boundaries, and failure recovery when they are part of the specific bug.

## When a formal test is impractical

Use a targeted script importing the real implementation, an existing browser path, a command transcript, or a focused integration probe. Explain why the durable test would require disproportionate setup and what the substitute does and does not prove. No runtime means a draft test and unrun instructions, not a pass. A user explicitly requesting a failing test still needs that requirement reported as unmet if it cannot be demonstrated.

Do not change tests merely to match incorrect behavior, weaken assertions to turn the suite green, or modify unrelated fixtures. An intentional specification change needs its own explicit rationale. A skipped check stays skipped.

## Evidence to return

Name the baseline and candidate, exact regression command, failing-before symptom, passing-after result, neighboring checks, and evidence paths. State all failures and unverified stages. A green focused test is not a claim that the entire project or production deployment passed.
