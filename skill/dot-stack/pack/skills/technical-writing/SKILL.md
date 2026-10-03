---
name: technical-writing
description: "Write or revise technical docs around the reader\u2019s task, with clear document purpose, executable procedures, precise terminology, and preserved evidence."
---


# Technical writing

Write so the intended reader can act or understand on the first read. Begin with audience, purpose, requested format, source of truth, and the action or decision the document supports. A style rule serves accuracy and readability; it must not change a contract, erase a warning, or invent certainty.

## Choose the dominant document purpose

Separate different reader jobs where useful, without fragmenting a short document unnecessarily.

- **Tutorial:** guide learning by building something. Name the concrete result first. Use a tested path, visible intermediate results, and expected output. Keep background short and link deeper explanation
- **How-to:** help a competent reader reach a goal. Name prerequisites, ordered steps, branches, and recovery. Avoid unrelated teaching or an exhaustive option catalog
- **Reference:** support lookup. Mirror the actual API, schema, command, or configuration. State types, defaults, limits, errors, and version scope. Distinguish unknown facts from established ones
- **Explanation:** help the reader understand a bounded topic. Connect mechanisms, constraints, history, tradeoffs, and alternatives. Separate documented reasons from interpretation

A task guide may need a small option table; a tutorial may need one sentence of explanation. Use purpose to organize, not as a ban on useful context. For pull-request descriptions and commit messages, focus on the reviewer’s decision: what changed, why, verification, and remaining risk.

## Make procedures usable

Use the actual symbols, files, UI labels, commands, and supported versions from the project. Put prerequisites and warnings before the step they constrain. Identify the working directory and expected outcome of commands. Distinguish literal commands from illustrative fragments; do not present placeholders as a runnable recipe.

Prefer one action per numbered step. Add expected output where success is not obvious, plus failure recovery when the reader could damage data or get stuck. Name side effects: a command that writes files or contacts a service must not be described as read-only. Do not introduce a new installation, authentication, or publication step casually.

When possible, execute documented commands in an authorized isolated environment and record the version tested. Verify examples with the real compiler or parser when their correctness depends on it. If execution is unavailable, mark the examples untested and inspect them carefully; never imply successful execution.

## Use direct and unambiguous language

Name who does what. Use present tense for current behavior and future tense only for future events. Put the condition before an instruction: “If the check fails, restore the test fixture before retrying.” Use the common case before exceptions.

Give each concept one name. Keep exact technical terms when they are more precise than a synonym. Define unfamiliar terms once. Prefer “use” to “utilize,” but do not replace a protocol's formal keyword or a legal requirement with a looser word.

Split sentences with competing thoughts, not every sentence over an arbitrary word count. Vary rhythm naturally. Keep articles and conjunctions that prevent misreading. Put “only,” “not,” and “unless” next to what they modify. Replace ambiguous pronouns and long noun clusters with explicit nouns and verbs. State whether “or” is exclusive when the choice matters.

Use sentence-case headings that help navigation. Number sequences and use parallel bullets for unordered items. Use descriptive links and the repository's established code formatting. Do not impose tabs, punctuation bans, or a different house style without a reason. Preserve accessibility and the user's required delivery format.

## Preserve evidence and meaning

Check claims about counts, trees, performance, compatibility, and status against the target revision. Include the command that regenerates a changing inventory when helpful. Do not invent source retrieval dates. A document saying “tests passed” needs evidence; a draft command is not that evidence.

Editing for clarity must retain uncertainty, exceptions, attribution, and privacy boundaries. “May fail under concurrent writes” must not become “fails” merely to sound decisive. Avoid vague attribution; cite the actual source or mark the claim unsupported. Do not copy private logs into a public-facing draft without authorization.

Use [unslop](../unslop/SKILL.md) for wording cleanup, not as a mandate to change technical meaning. Preserve user voice where requested. Do not update the style skill itself while editing another document.

## Review the final artifact

Read it as someone who did not attend the discussion. Can they find the prerequisite, perform the next step, recognize success, and recover from the important failure? Check links and snippet consistency. Keep reference detail in a linked artifact when it would bury the main result.

Example rewrite:

Before: “Configuration updates should only be performed when lowering the limit. If exceeded, it fails.”

After: “The checker reads the limit from `budget.json`. If the import count exceeds that limit, the check fails. Run the update command only to lower the limit.”

The example clarifies actor, condition, and referent. In a real document, replace “the update command” with its verified invocation and preserve any additional prerequisites.
