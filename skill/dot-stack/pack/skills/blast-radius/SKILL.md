---
name: blast-radius
description: "Trace direct and hidden consumers of a change, identify load-bearing safety assumptions, and test realistic breakage beyond the diff."
---


# Blast radius

Find what a change can break outside its edited lines. The useful result is a small set of evidenced risks and safety claims, not a long list of imaginable failures. This is a review; do not apply fixes or publish findings unless requested.

## Anchor the change

Establish the actual base and candidate revision or working-tree snapshot. Inspect the diff and affected contracts. Do not assume the base branch is named `main`. If the diff is incomplete, state that limit. Use [how](../how/SKILL.md) to trace an unfamiliar flow and [why](../why/SKILL.md) when historical constraints bear on safety.

## Follow consumers beyond symbol search

Find direct callers, then inspect consumers a search can miss: serialized data, public API clients, persisted rows, configuration, feature flags, generated bindings, command output, other-language readers, lifecycle hooks, teardown, and async ordering. Read the actual dependency version and local patches before relying on library semantics.

Do not expand every review into a system audit. Prioritize reachable paths affected by the change. For a wide change, independent read-only reviewers may cover separate boundaries; without delegation, perform the same targeted checks sequentially.

## Test the fact safety depends on

State the one or two load-bearing claims. For example: “Deleting this cache entry cannot remove an active subscription.” Try to disprove them with a real caller and the actual library, rather than proving a simplified imitation.

For each claim, record the strongest evidence obtained:

1. Hypothesis only
2. Source evidence at a pinned path and line
3. A traced reachable or unreachable failure path with stated assumptions
4. An executed test importing the real implementation and asserting observable behavior
5. A reproduction through the running application's relevant user path

These are different evidence kinds, not a requirement to reach the highest for every risk. A compile-time contract may need real compiler tests; a cancellation bug needs runtime ordering; a UI regression needs the actual interaction. An unavailable runtime leaves the executable proof unverified.

Use isolated fixtures and allowed local checks. Assert the meaningful outcome, not a matching source string, a mock's call count alone, or an empty successful command. Include negative controls when the test could pass without exercising the change. Record revision, command, environment, result, and artifact location. Avoid live destructive probes.

## Calibrate the report

For a risk, show the changed contract, reachable consumer, triggering conditions, consequence, and evidence. Separate likelihood from impact. Do not invent numeric probabilities. A severe outcome requiring several unobserved failures stays a hypothesis unless the path is demonstrated. A single reproducible defect outweighs several speculative reviewer votes.

Return:

- What changed, including indirect behavior
- The safety claims and their evidence levels
- Confirmed risks, with exact locations and the cheapest regression check
- Risks checked and cleared, with the assumptions under which they are cleared
- Unverified boundaries and the concrete check needed before release

“Nothing found” means nothing found in the stated scope; it is not a guarantee. Strip secrets and unrelated private context before any separately authorized sharing.
