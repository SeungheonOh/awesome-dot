# Claude custom skills

Claude Code's plugin package and a consumer/API custom-skill upload are different delivery units. Do not upload the whole dot-stack multi-skill plugin ZIP as if it were one skill.

## Choose the correct unit

Use `dot-stack-0.4.0-native.zip` for the [Claude Code plugin](claude-code.md). Use `dot-stack-0.4.0-single-entry.zip` for a surface that accepts a custom-skill folder ZIP. The latter contains one root `dot-stack/SKILL.md` and the intact library in `dot-stack/pack/`; manual dependency assembly is no longer needed. Nested skill files are read-on-demand resources, not a claim that sibling native skills are registered.

The [single-entry guide](single-entry.md) covers building, inspecting, and reading this export. Its entrypoint uses only `name` and `description`, with a matching folder name and a description under 200 characters. This follows the documented folder/metadata format, not a guarantee that the host accepts this library's breadth or resource layout. [Official custom-skill format](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)

Claude's different surfaces have different runtime, network, and package-install constraints. An API-managed skill requires its own configured execution integration; uploading or copying a file does not provide that integration. Consult the actual target surface and inspect the tools it exposes. [Official Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)

## Capability-based execution

- Supplied code and text can support explanation, design comparison, review, and a proposed patch
- Filesystem and execution tools are required to apply changes and run checks
- An actual browser/control tool is required for observed UI proof
- Native delegation is required for an independent worker result
- An actual supported scheduling mechanism and user approval are required for future runs
- Connector availability and action authorization are checked separately

When a capability is absent, return the useful partial result and identify precisely what was not executed. A generated test command is not a passing test; a draft is not a sent message; model self-review is not independent review.

## Validate a custom upload

Inspect the isolated single-entry archive and verify that packaged resource links resolve. Follow the actual target surface’s upload flow only when requested and permitted. Reject secrets, private run state, caches, unsupported metadata, or misleading install claims. Confirm the skill appears in the target account, then run a small representative fixture and a missing-tool scenario. Report upload acceptance separately from behavioral success.

Local export validation, extracted helper checks, and host upload/activation are separate results. This release has not been uploaded to or executed in a live Claude account.

If no custom-skill feature is available, use the [plain-chat route](plain-chat.md). Instructions remain useful without claiming installation.
