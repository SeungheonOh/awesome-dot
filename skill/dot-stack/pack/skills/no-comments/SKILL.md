---
name: no-comments
description: "Review comments and suppressions in a scoped change, remove proved redundant or stale narration, and preserve required contracts and non-obvious constraints."
---


# Review comments

Improve the code's explanation burden without deleting information the code cannot express. The name is shorthand, not a demand for zero comments. Scope comes from the user's files or diff; otherwise determine the actual base and working-tree changes before editing.

## Review first

When available and proportionate, use the pack's [comment-reviewer role](../../agents/comment-reviewer.md) in a read-only independent context. Its file is a role brief, not proof that the host registers an agent with that name. If unavailable, review directly and label it self-review.

Classify each relevant comment or suppression:

- Preserve: license notices, public API contracts, external protocol constraints, safety rationale, generated-file requirements, meaningful historical constraints, and justified compiler/linter directives
- Remove or rewrite: demonstrably stale statements, narration of obvious code, redundant summaries, and misleading claims
- Encode then reconsider: an invariant that could be enforced more reliably by a type, boundary check, regression test, or existing lint rule
- Unresolved: intent or constraint lacks enough evidence; retain it while reporting the uncertainty

Read surrounding code and trace the claimed constraint. Use source history when “do not remove” or a surprising workaround refers to a real external limitation. Missing proof that a comment is necessary is not proof that deletion is safe.

## Apply only authorized changes

A cleanup request authorizes the scoped cleanup, not a redesign of unrelated code. Fix obvious dead narration directly after checking it. For a meaningful logic change, distinguish the proposed root-cause repair from comment editing and obtain authority if the request does not cover it. [Architect](../architect/SKILL.md) can help a genuinely nontrivial change; do not require a design competition to remove one sentence.

Do not delete a constraint while its replacement check awaits approval. If the root cause is outside scope, preserve the useful warning and report the bounded follow-up. Do not delete compiler expectation directives used to assert negative type behavior, or suppression comments whose necessity is demonstrated. Test a suppression's removal with the relevant compiler/linter rather than guessing.

## Validate and report

Inspect the final diff for lost license text, altered API documentation, unintended code edits, and scope escapes. Run relevant lint, compiler, and behavioral checks when available. If removing a comment changes a tool directive or generated output, verify that specific effect.

Return what was removed or rewritten, what was preserved and why, any structural fixes actually authorized and tested, and unresolved constraints. Count deletions only if useful; the quality of the remaining explanation matters more than the count. No automatic commit or external review post.
