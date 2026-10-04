# Review rubric

Use applicable lenses. A narrow fix does not require an architecture essay. Bind every finding to the inspected candidate.

## Correctness and lifecycle

Trace the normal operation and relevant empty, boundary, error, cancellation, and repeated-action cases. Check state transitions, async ordering, resource release, stale closures, encoding, and arithmetic at the actual type and runtime boundary. For concurrency, identify which actors can overlap and what shared state they write. Explain the invariant protected by isolation or a transaction. “Could be null” needs a caller that can actually produce null.

## Root cause

Follow the failing behavior beyond the diff. Determine whether a guard, retry, fallback, or cast repairs the violated contract or hides it. A workaround may be necessary for an external constraint; require evidence and an explicit boundary. Prefer an enforceable type, test, or validation rule over a comment that asks future callers to remember an invariant.

## Structure and domain fit

Locate the canonical owner of policy and validation. Look for leaked transport/storage types, duplicated invariants, mixed levels of abstraction, and data structures that fight the actual access patterns. Prefer a coherent smaller model over another mode or branch when demonstrated. Do not demand abstraction for one simple use. Do not remove compatibility paths while external consumers or staged migration contracts still require them.

## Verification

Ask which behavior each check proves. Does a regression fail on the baseline for the intended reason? Does boundary validation reject malformed external input? Does a type claim survive the real compiler and negative type examples? Are asynchronous outputs and side effects inspected rather than inferred from a worker's summary? Does integration evidence apply to this final revision?

No shell means tests unrun, not passed. A missing browser leaves browser-specific behavior unverified even if unit tests pass. Snapshot text, source regex checks, lint, and syntax checks each prove narrower properties than end-to-end behavior.

## Complexity and maintainability

Show the concrete maintenance cost of new configuration, dual paths, generic frameworks, one-use wrappers, or scattered special cases. Demonstrate the simpler alternative's preserved behavior and migration cost. Avoid file-size thresholds and hypothetical future flexibility as independent verdict rules.

## Security and trust boundaries

Trace untrusted input to a relevant sink or authority decision: shell execution, queries, HTML, filesystem paths, object construction, redirects, auth, or access checks. Inspect timeout/retry/replay behavior, secrets in logs, and races where security depends on mutable state. Explain attacker control, prerequisites, existing defenses, and likely impact. Safe local tests or static evidence suffice when live exploitation would be unauthorized.

## User outcome

Confirm the change solves the stated problem under the expected workflow, including error recovery. A technically correct feature may still fail its required entry point, accessibility contract, or interruption behavior. Scope the finding to the promised experience rather than imagined requirements.
