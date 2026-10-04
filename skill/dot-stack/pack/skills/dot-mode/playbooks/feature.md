# Feature

Use for new or changed behavior. Read the [execution contract](../references/execution-contract.md). Own the integrated result, whether implementation is delegated or direct.

## Inputs

User outcome, acceptance scenarios, affected consumers, existing contract, authorized files, and delivery boundary. Distinguish required behavior from appealing scope additions. Resolve genuine product choices before hard-to-reverse implementation; observe factual uncertainty cheaply where possible.

## Steps

1. Read the affected subsystem, entry points, callers, and project conventions. Name the data shape, allowed states, transitions, boundary validation, and ownership. Prefer an explicit coherent model over scattered flags or defensive wrappers.
2. Compare designs when there is a consequential choice. Use [architect](../../architect/SKILL.md) or an isolated [Prototype](prototype.md) for uncertainty that merits exploration. A local obvious change may proceed without a panel. Record the selected tradeoff and rejected option briefly.
3. For multi-step work, record a throughput checkpoint: blocking prerequisites; independent workstreams; shared mutable state and its owner; smallest safe decomposition. Split shared targets before adding locks. One tightly coupled feature can have one owner with internal disjoint tasks.
4. Implement verifiable slices. Give any worker exact scope, baseline identity, acceptance checks, and evidence requirements. Inspect returned diffs and integrate deliberately. Use [arena](../../arena/SKILL.md) only if comparing alternative implementations is worth the cost. Do not force delegation when unavailable or slower.
5. Verify the consumer contract. Exercise positive, invalid-input, error/recovery, and relevant lifecycle cases through the real boundary. UI work needs actual interaction and appropriate visual/accessibility checks; a library or service does not need screenshots. Run affected integration and regression gates on the final candidate.
6. Inspect the final diff at changed responsibility boundaries. Check affected consumers and relevant input, error, and return conventions against the existing contract; preserve them unless the requested behavior changes them. Put a correction in the owning abstraction and remove duplication only when the diff shows a concrete in-scope problem. Check temporary scaffolding, user data, secrets, and comments carrying non-obvious constraints. Do not manufacture cleanup to complete a review ritual. Resolve a contested high-impact design with explicit evidence rather than reviewer consensus alone.
7. Deliver coherent changes and proof. Follow repository commit policy; never rewrite shared history for a tidy narrative. Use [Opening a PR](opening-a-pr.md) only for authorized publication.

## Failure and recovery

If acceptance is underdetermined, separate the implementation that is safe from the decision that belongs to the user. A missing driver or failing unrelated baseline creates a named coverage gap. Do not turn it into a green result or broaden the task into unrelated repairs. If integration changes a tested candidate, rerun impacted checks.

## Evidence and completion

State what the consumer can now do, the selected design and maintenance consequence, verification at the current candidate, material tradeoffs, and any open decision. Include the throughput checkpoint only when it helped plan substantial work. Completion follows the requested delivery boundary, not automatic shipping.
