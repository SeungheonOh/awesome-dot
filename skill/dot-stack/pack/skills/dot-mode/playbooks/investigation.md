# Investigation

Use for an explanation, read-only review, historical question, or recommendation. Read the [execution contract](../references/execution-contract.md). The result is a cited answer, not a patch.

## Inputs

A concrete question, relevant artifacts or authorized read access, and the decision the answer should support. Identify the revision and coverage boundary. If the question is ambiguous, distinguish current behavior, original intent, and proposed behavior.

## Steps

1. Map entry points, data shapes, relevant invariants, and callers. Use [how](../../how/SKILL.md) for unfamiliar structure and [why](../../why/SKILL.md) when history matters. Read only the material needed to support the answer.
2. Trace representative inputs through the actual path. For a code review, inspect the diff and its surrounding contracts. Separate a demonstrated defect from a plausible risk and a preference. A comment or PR description is context, not proof.
3. Check each important assertion using source locations, existing tests, supplied logs, or safe read-only queries. When authorized, run a focused local test or disposable isolated probe; inspect its setup for service calls and writes first. Keep scratch outputs separate and preserve product files and remote state. A review does not authorize a repair, dependency installation, another environment, or external mutation. Honor an explicit no-execution or strict read-only constraint; mark any prevented runtime claim unverified.
4. Evaluate competing explanations. Record evidence that would falsify the leading interpretation. For a recommendation, compare relevant costs, operational risks, reversibility, and user impact; do not manufacture a tradeoff table when one option is clearly sufficient.
5. Synthesize at the level the user asked for. A subsystem explanation can use overview, concepts, execution flow, locations, and gotchas. A review should prioritize findings with concrete locations and consequences, then name coverage gaps.

## Failure and scope

Missing files or inaccessible history limit the answer. State which claim remains unverified and request only the missing material that changes it. A historical explanation inferred from code is not established author intent. If a defect is discovered, describe it and the smallest next step; do not silently switch to Bug fix, publish a comment, or open a PR.

## Evidence and completion

Return the answer or recommendation, source pointers, confidence and counterevidence, and material unknowns. Stop once the question is answered at the available evidence level. No throughput ceremony or independent reviewer is required for a small cited explanation.
