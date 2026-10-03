# Prototype

Use for a disposable experiment that makes a concrete design or empirical decision cheaper. Read the [execution contract](../references/execution-contract.md). The artifact is an instrument, not production-ready code.

## Inputs

The decision to settle, candidate approaches, observable success criteria, time/resource bound, and whether the question is factual or a user preference. No decision means no reason to prototype.

## Steps

1. Define the smallest discriminating observation. For a layout, name viewport, interaction, content, and states; for behavior, name inputs and outputs; for performance, name workload and metric. Do not ask the user to guess an observable fact.
2. Inspect relevant prior art when the design space is open. Ask for a preference only when it cannot be inferred from the brief or measured. Do not block a narrow empirical experiment on an unnecessary moodboard.
3. Build in an isolated authorized scratch directory with the lightest already-available tools. Prefer local assets and synthetic data. New dependencies, remote services, tunnels, credentials, public hosting, and paid calls retain their own permission requirements.
4. Label comparable alternatives and hold nonessential variables constant. A switcher helps visual comparison; a common runner helps behavioral or timing comparison. Keep throwaway shortcuts visible so no one mistakes them for production decisions.
5. Observe the actual surface. Drive UI interactions and capture useful states. For non-UI experiments, retain output, timings, or traces. Cheap assertions are welcome where they expose the decision; a production test suite is unnecessary.
6. Compare results against the criteria. Explain tradeoffs, uncertainty, and the recommendation. A failed alternative is useful evidence; do not hide it or polish away a meaningful flaw.

## Failure and completion

If the prototype cannot discriminate, refine the criterion or report it inconclusive. Do not convert exploratory code into a feature without checking production requirements and receiving any needed authority. Return the decision, variants, observations, limitations, scratch location, and explicit throwaway status. Route an authorized implementation to [Feature](feature.md).
