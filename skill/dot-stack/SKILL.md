---
name: dot-stack
description: "Use dot-stack to investigate, design, implement, and verify engineering tasks with scoped workflows, candidate-bound evidence, and honest capability limits."
---

# dot-stack

Use [dot-mode](pack/skills/dot-mode/SKILL.md) to choose the smallest relevant workflow for the user's engineering task. Read that workflow and its execution contract once, reusing unchanged material already in context. Load further resources only for missing, relevant procedural information; check tool/version assumptions against the actual project or host. Do not load the whole library or skip mandatory host/project instructions.

The bundled library is under `pack/`. Its nested skill files are resources of this entrypoint, not separately installed skills. Follow their relative links from the containing file, preserving this directory tree. The [guide](pack/docs/guide/README.md) provides a task-oriented index.

For optional helpers, the actual library root is this skill directory's `pack/`, not the outer skill directory. Verify [the manifest](pack/plugin.json) names `dot-stack` and [the helper](pack/tools/dot-stack.mjs) exists before using that absolute directory as `DOT_STACK_ROOT`. Read [helper requirements and commands](pack/tools/README.md) when needed. Keep the target project and mutable state outside the installed skill.

The instructions grant no tools, credentials, permissions, independent review, or scheduling. Use only capabilities actually available and actions the user has authorized under the host's rules. If a required capability is absent, provide the useful partial result and label the unrun step. Uploading this folder does not activate its bundled native plugin metadata or optional automation recipes.

[MIT license and full notice](LICENSE)
