---
name: principle-test-behavior-not-implementation
description: "Write tests that exercise a real contract and fail for a plausible defect, using independent expectations and meaningful positive, negative, and boundary cases."
---

# Test behavior, not implementation

Use this while adding, reviewing, or changing tests. A valuable test has a contract, an exercised subject, and an observation that would distinguish correct behavior from a plausible defect.

## Choose an independent oracle

Call the subject through the interface relevant to the test's level and assert an externally meaningful result: returned data, persisted state, emitted payload, visible interaction, or a required absence of effects. Use literal expected values for concrete examples, or an independent specification, relation, or property when exact literals are inappropriate. Do not compute the expectation with the same implementation being tested.

Prefer assertions that explain the contract. `is defined`, a success exit, or a call count alone rarely proves a transformation. Inspect the result, payload, state transition, or error semantics. Mocks can isolate an external boundary; mocking away the behavior under test proves little. An interaction is itself valid observable behavior when the contract requires a specific protocol, cancellation, or absence of a dangerous effect.

Check whether a plausible broken implementation would still pass: returning nothing, returning a constant, ignoring input, skipping an effect, or emitting the wrong payload. The “return nothing” thought experiment is one mutation, not a universal validity test. Use an actual temporary mutation when practical and safe, then restore the candidate and rerun.

## Legitimate negative and structural tests

Absence can be the essential result: unauthorized input must send no email; an empty query can return an empty list; cancellation must perform no write. Establish that the subject ran and the setup reached the relevant path. Use a corresponding allowed/nonempty case when it helps rule out a disconnected harness, but separate tests can supply that evidence.

Keep compile-time rejection tests, cross-table invariants, schema checks, and stable public-format tests when they protect a real contract. A snapshot or constant pin is weak if it merely mirrors an editable implementation detail; it is useful when the exact output is an agreed compatibility requirement and changes are deliberately reviewed.

## Example and counterexample

Applies: pass `Hello, World!` to a slug function and expect `hello-world`; separately exercise repeated whitespace and already-valid input.

Does not apply: assert that a fixture contains the values the test itself inserted without invoking the subject, or assert `f(x) == f(x)` as a correctness check. Replace the oracle rather than deleting useful coverage merely because its current assertion is weak.

## Evidence

Name the defect each test would catch, the contract it observes, and whether the checker was actually run. Preserve tests that survive legitimate refactoring while rejecting wrong behavior; no specific matcher is categorically good or bad without its contract.
