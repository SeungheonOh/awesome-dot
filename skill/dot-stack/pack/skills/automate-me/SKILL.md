---
name: automate-me
description: "Draft or revise a personal working-conventions skill from explicit preferences and authorized examples; keep one-off choices and permission rules separate."
---


# Automate me

Turn recurring working conventions into a focused skill the user can review. This creates instructions for a chosen task context; it does not change the assistant's identity, enable a permanent mode, or alter host confirmation rules.

## Find the intended target

Look only in the user-named location and the active project's known skill directories. Read an existing matching skill before proposing changes. Do not recursively search private host storage or infer transcript paths. If several targets fit, ask which one. Preserve the existing path and unaffected content for an update. A new skill uses a chosen project location such as `.agents/skills/<handle>-workflow/` or `.claude/skills/<handle>-workflow/`, according to the actual host and user preference. Avoid silently installing both copies.

If the user requested a draft, return it before saving. A request to create or update the specified project skill permits that scoped edit; it does not permit global rules, permissions, commits, or external publication.

## Gather useful evidence

Start from explicit user preferences and the current conversation. Use supplied examples or an authorized history/search source only when available and relevant. Bound history by project, topic, and time range; for an update prefer evidence since the previous version. Small histories need no workers. If a larger corpus warrants delegation, give each read-only worker an exact slice and return evidence pointers rather than raw conversations.

Look for decisions that change behavior: response length and format, review requirements, code conventions, collaboration choices, and the meaning of “done.” Mark each as explicit standing preference, recurring pattern, one-off choice, or contradiction. Repetition strengthens an inference but does not authorize a permission change. Current explicit instructions outrank older examples.

No history access is a normal branch. Draft from current evidence and ask one or two focused questions about the areas that matter. Use a supported question UI if available, otherwise ordinary chat. Do not require an interview if the user's request already supplies the conventions.

## Write a compact contract

Use only `name` and a narrow `description` in portable frontmatter. The description should identify the requested workflow or user-chosen style, not claim to activate on every turn. Include only sections with a real non-default convention. Each instruction should say when it applies and what decision changes.

Good: “For review requests, put reproducible correctness findings before style suggestions, and include the affected revision.”
Weak: “Be rigorous and communicate well.”

Reference genuinely required project resources rather than copying entire manuals. Ensure the target can resolve the reference after installation; include the resource when packaging an individual skill. Omit private conversation excerpts, sensitive facts, and third-party names unless needed for the requested workflow. Keep evidence used to draft separate from the reusable skill.

Permission preferences belong in the host's authorized settings process when one exists. Do not encode “always send” or similar authority in a skill as a shortcut. If the user wants such a change, explain the specific separate step while continuing the draft.

## Review and validate

Compare the draft with the existing skill and list material changes. Do not turn conflicting evidence into a universal rule. Ask about the conflict only if it matters; otherwise narrow the instruction. Apply [unslop](../unslop/SKILL.md) while preserving exact scope and exceptions.

Validate frontmatter, links, and any shipped scripts using available local checks. Walk through representative prompts: an intended trigger, a nearby non-trigger, an exception, and a case with no history access. Style quality still needs the user's judgment; structural validation is not proof that the skill matches them.

Return the draft or saved path, what evidence shaped it, unresolved preferences, and what was actually tested. Do not automatically commit, open a pull request, or enable a recurring update.
