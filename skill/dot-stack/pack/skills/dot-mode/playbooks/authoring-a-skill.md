# Authoring a skill

Use for writing or changing reusable skill instructions. Read the [execution contract](../references/execution-contract.md). The goal is an actionable decision aid, not a long prompt that repeats the host's rules.

## Inputs

Target users/hosts, trigger, outcome, inputs, available capabilities, allowed side effects, existing package conventions, and examples of success and failure. Inspect any supplied reference in full before adapting its semantics.

## Steps

1. Define a narrow trigger and non-goals. Specify what information is needed, what the skill produces, and where a workflow must stop or ask. Keep authority separate from capability.
2. Write standard frontmatter with a lowercase folder-matching `name` and a concise task-specific `description`. Do not embed permission grants, assumed tool signatures, hardcoded models, global settings, or proprietary UI behavior in a portable core.
3. Provide concrete steps, decision branches, evidence expectations, and recovery behavior. Place detailed optional material in bundled references; avoid duplicating common contracts across unrelated skills. Use actual bundled paths and clearly identify companion requirements for copied/uploaded skills.
4. Validate frontmatter, filenames, every relative link, command examples, and resource closure. A link that resolves only in a full pack must not be advertised as a self-contained upload.
5. Test representative prompts: intended trigger, near miss, small task, missing tools, denied action, malicious external instruction, stale evidence, and ambiguous authority. Structural checks can catch broken links; a scenario exercise is needed to test decisions. Label simulated scenarios separately from live host execution.
6. Review prose for ambiguity and needless ceremony. Preserve rationale only where it prevents a common misapplication. Keep legal attribution and necessary constraints. Fix a broken skill within the requested scope; do not automatically create an unrelated PR mid-task.

## Failure and evidence

If a host cannot load or execute the skill, report the specific untested capability. Do not call a Markdown lint pass a successful installation. Return the skill purpose, key decisions, resource/dependency inventory, checks and scenario outcomes, and known host limits. Installation, publication, or global configuration needs its own authorization.
