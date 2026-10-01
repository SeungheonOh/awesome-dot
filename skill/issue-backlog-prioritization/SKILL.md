---
name: issue-backlog-prioritization
description: "Rank a defined issue backlog against the user's criteria and gates, expose score uncertainty and dependency blockers, and apply only specifically authorized tracker changes."
---

# Prioritize an Issue Backlog Without Hiding Its Unknowns

Produce an auditable importance comparison and a separate view of what can start. A prerequisite can be low-scoring yet necessary; a high-scoring issue can remain blocked. Neither fact is a reason to rewrite the other's importance score.

## Use and inputs

Use for an existing set of issues the user wants compared, sequenced or updated. Work from the actual authorized tracker, export and supporting documents. Do not replace incomplete real records with invented examples. This is not an individual-performance assessment, a security test or authorization to reproduce vulnerabilities.

Establish:

- Exact project, issue IDs or query, inclusion/exclusion rules, snapshot date and source links
- Decision being made: importance, next executable work, or both
- User-supplied criteria, definitions, scale direction, weights, formula, hard gates and tie policy
- Evidence for each criterion, readiness conditions, dependency IDs and their completion evidence
- Requested output destination; separately, the exact tracker, issues, fields and value mapping authorized for writes

Use an existing explicitly endorsed rubric when one is available. If the rubric is missing or ambiguous, extract facts and present tradeoffs while asking for the decision-changing criterion. A proposed rubric must remain a proposal until the user accepts it. Do not invent weights, priorities, owners, due dates or delivery promises.

## Workflow

### 1. Freeze the comparison scope and provenance

Read all in-scope issues and the necessary prerequisite records. Preserve original IDs, status, version token and text. Deduplicate repeated exports by stable issue ID, not by similar titles; surface conflicting versions. Record each material input as value, source, observation date and any uncertainty. An issue's age or number of comments is not evidence of impact unless the rubric explicitly uses it.

Separate reported symptoms, verified effects and proposals. Do not infer a person's competence, effort or reliability from assignment history or a backlog. If an issue contains sensitive vulnerability information, use the authorized defensive impact summary without generating payloads, reproducing exploitation or exposing details to a broader audience.

### 2. Apply gates before claiming eligibility

Record each user-defined hard gate as pass, fail or unknown with its evidence. Keep excluded or failed items visible with their reason; do not silently drop them or turn a failed gate into a small scoring penalty. An unknown gate stays unresolved and cannot be described as passed.

Keep importance eligibility separate from readiness. For example, an in-scope, high-impact item may meet the ranking gates but lack a required design decision. State whether a gate changes comparison eligibility, execution readiness or both according to the user's rubric.

### 3. Calculate importance faithfully

For every fully specified item, show the component values and the exact supplied formula. Verify scale bounds, weight units and whether larger values mean better or worse. Do not normalize or invert scales silently. Use one consistent formula across comparable items and avoid adding a derived dependency bonus unless the user authorized it.

For missing inputs:

- Retain null/unknown rather than zero, a midpoint or a guessed “typical” value
- Calculate a score interval only when the missing input has defensible bounds from the supplied scale and the formula supports those bounds
- For a monotonic weighted sum with nonnegative weights, substitute the allowed lower and upper values separately. For other formulas, evaluate their actual behavior; denominator zero, negative weights or correlated bounds may require separate cases or an unresolved score
- Label wide intervals as uncertainty, not low confidence or low importance. Do not drop an unknown criterion and redistribute its weight

Keep exact values for comparisons and round only for presentation. Using only separate score intervals, A is definitely above B when A's minimum exceeds B's maximum. Overlapping or touching ranges do not prove either a strict ordering or an exact tie; keep them explicitly unresolved or incomparable unless additional supplied evidence resolves the relation. Do not rank by interval midpoint. Apply only an approved tie-breaker. Use equal tiers for equal exact scores without an approved tie-breaker; an ID order used for display is not a priority order.

### 4. Check dependencies and derive readiness

Build a directed graph where A → B means A requires B. Resolve referenced IDs against the allowed tracker scope. An inaccessible, missing or uncertain prerequisite makes readiness unknown, not satisfied. Use explicit dependency evidence; a comment mentioning another item is not automatically a hard dependency.

Check self-dependencies and directed cycles with a standard graph traversal or strongly connected components. Report the participating IDs and a cycle path. Do not break a cycle, close an issue or change links automatically. A topological order for a cyclic component does not exist; independent acyclic work may still be ready.

For each issue, preserve its importance result and report ready, blocked, unknown or complete, with the reason. “Ready” requires evidenced satisfaction of the relevant gates and prerequisites. If the user requests an execution order, respect dependency direction and distinguish prerequisites from their higher-scoring dependents. Show the work a prerequisite would unblock without asserting it inherits the dependent's score. Do not infer duration, capacity, an owner or a completion commitment.

### 5. Deliver the decision and, when authorized, the narrow update

Return the ranked known-score tiers plus unresolved score ranges, gate results, readiness and dependency exceptions. State the smallest missing fact that could change the decision. If uncertainty prevents a unique first choice, say so rather than turning the display order into a recommendation.

For an already-authorized tracker update:

1. Prepare exact issue-ID/field/before/after changes in the approved destination. Use only the authorized mapping from results to field values. An analysis request alone does not authorize writes
2. Check each destination field's type. If it cannot represent an unresolved range, do not silently store a midpoint, zero or definitive priority. Leave it unchanged and ask only about the unsupported representation
3. Refresh target records and use supported version/conditional-write controls. Reconcile concurrent changes before writing; preserve unrelated fields, descriptions, labels, owners and dates
4. Apply only authorized changes. Do not add a comment, notification, assignment or status change merely because it would be convenient
5. Read back each changed field. Report verified changes, unchanged unresolved fields, failures and any conflicting readback. An uncertain response is not success; inspect the current state before retrying to avoid duplicate writes

If approval or access is absent, deliver the private analysis and exact proposed changes without performing the blocked action. Do not switch trackers, expand audiences or create a new external destination as a workaround.

## Output and checks

The finished output must make the following inspectable:

- Scope/snapshot and the approved rubric, including gate and tie rules
- Per-issue evidence, component values and exact score or bounded range
- Importance tiers or a partial order, with unresolved comparisons explicitly marked
- Separate readiness, prerequisites, missing references and cycle findings
- Decision-changing questions and, if relevant, verified tracker changes

Recompute scores independently, confirm interval endpoints, and check all rows against source data. Verify equal scores stay tied and blocked work retains its importance. Check that no final priority claims depend on an invented input. For writes, compare readback against the exact authorized field set and avoid claiming unrelated fields were preserved unless the available response supports it.

The [fictional fixture](example.md) and `python3 check_example.py` exercise score arithmetic, an unknown, a tie, a blocked dependency, a missing prerequisite and a cycle. They are a test of the reasoning rules, not a live tracker integration.

## Example request

“Use these issue records and my attached rubric to compare importance and tell me what can start. Keep missing urgency scores unresolved. Preserve equal-score ties and show dependency blockers separately. Prepare the results privately; do not edit the tracker.”
