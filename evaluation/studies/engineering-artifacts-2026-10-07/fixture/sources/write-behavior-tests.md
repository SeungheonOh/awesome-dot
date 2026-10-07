---
name: write-behavior-tests
description: Create or improve automated tests for a specific behavior contract using the project's existing test approach. Use when the user needs meaningful coverage of observable results and failure paths, rather than diagnosis of a failing run or a coverage-number increase alone.
---

# Write Behavior Tests

Deliver tests that distinguish the required behavior from plausible mistakes. Test the contract at the right boundary, run the actual tests, and explain what they protect. A larger test count or a green run is not enough if the assertions would also accept the wrong result.

## Establish what should be true

Read the requirement, relevant interface or specification, current implementation, and existing tests. Identify the input or starting state, the operation, the observable result, and the important conditions under which that result changes.

Do not treat current behavior as automatically correct. A requirement may intentionally change an old default, and an existing bug should not become the expected answer merely because the implementation returns it. If sources conflict on a consequential case, show the concrete difference and resolve that contract before encoding an assertion. Continue writing tests for settled behavior.

Determine the requested scope: new tests, stronger assertions, a regression test, or tests accompanying an authorized implementation. Test creation alone does not require changing product behavior. If a well-grounded test exposes a defect, preserve the useful failing case and report it; implement a fix when the request also covers that work.

## Choose the boundary that proves the behavior

Use the project's existing framework, fixtures, and conventions where suitable. Find the entry point or consumer whose behavior matters. A unit test may be enough for a pure calculation; a changed serializer, command, or persisted default may need a check through its real consumer.

Separate concerns without replacing the whole system with mocks. Mock a boundary when it makes an external dependency controllable, but keep enough real code to exercise the contract under test. A mock returning the expected answer does not prove the product can produce it. State what an isolated test leaves to integration or application-level checks.

Select cases that cover different decisions or likely mistakes:

- An ordinary valid input with a concrete expected result
- A meaningful boundary or alternative branch
- A relevant failure or incomplete result, including the resulting state
- A compatibility case when existing callers or saved data must continue to work

These are prompts for judgment, not a mandatory checklist for every function. Use parameterized cases when they clarify a shared rule; use distinct tests when setup or expected behavior differs substantially.

## Build reliable inputs and assertions

Use original or approved test data with only the detail needed to express the case. Preserve the distinctions the contract depends on, such as order, duplicate occurrences, types, omitted versus explicit values, or empty versus unknown results.

Compute expected values independently of the implementation being tested. Calling the same helper to build both the expected and actual result can reproduce the same defect twice. For generated or property-based inputs, state the invariant and any valid-input assumptions; random generation is useful only when failures can be reproduced and the oracle is meaningful.

Assert the output that matters, including consequential side effects or their absence. Checking only that a function returns, a file exists, or a status is successful may miss the wrong content. Conversely, avoid asserting incidental formatting, private call order, or internal helper names unless they are part of the actual contract.

Make time, randomness, environment, and external dependencies controllable where they affect the test. Use an explicit clock or synchronization condition rather than a sleep that merely makes failure less likely. Keep temporary resources isolated, restore changed state, and clean up only resources the test owns. Do not make tests depend on personal accounts, private files, or live services unless that integration is explicitly within the requested environment and authority.

For errors, assert the relevant type, status, or documented message and verify the remaining state. Do not catch every exception and call the test successful. A timeout, skipped test, or failed setup is not a passing assertion.

## Check that the tests can detect a mistake

Run the focused tests using the actual project command and prerequisites. Inspect the result rather than assuming discovery included the new file. Confirm the intended cases executed and that assertions reached the real behavior.

Where useful, demonstrate that a new regression test fails before the corresponding fix, or check a small deliberately wrong variant in an isolated copy. Choose a benign, relevant mistake, such as dropping a duplicate, reversing a comparison, or changing a default. Do not mutate the user's working implementation merely to manufacture a failure, and do not require a mutation exercise for every trivial test.

If a test fails, distinguish an implementation defect, incorrect expectation, unsuitable fixture, and environment problem. Fix the part the evidence supports. Do not weaken the assertion or skip the case solely to make the suite green.

Run nearby or required project checks when the new tests affect shared fixtures, setup, or discovery. After later edits, rerun the affected cases. Avoid repeated full-suite runs when no relevant files or unresolved concern changed.

## Deliver the useful coverage

Leave the tests in the requested project location and preserve unrelated changes. Explain which behavior the tests now protect, what actually ran, and any defect or unavailable integration check still open. A failing regression test can be the correct deliverable when the task was to expose a known problem; label its expected failure clearly rather than claiming the suite passes.

Keep coverage claims tied to the tested boundary. Do not infer production reliability, complete compatibility, or the absence of all bugs from a local suite. Follow the established scope for commits, remote runs, and publication; test authoring does not itself authorize changing shared services or disabling existing checks.
