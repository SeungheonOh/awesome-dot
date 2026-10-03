# Claude Code

The whole-package route keeps skills, role files, and optional helper resources together. No login, permission change, model override, connector, hook, or background service is installed by the manifest.

## Try the plugin locally

From a shell where Claude Code is already installed:

```sh
claude plugin validate /absolute/path/to/dot-stack
claude --plugin-dir /absolute/path/to/dot-stack
```

The native manifest is `.claude-plugin/plugin.json`. Skills live in root `skills/`; agent roles live in root `agents/`. In the resulting session, use `/dot-stack:dot-mode` or `/dot-stack:setup-dot-stack`. The native validator is authoritative for the installed client; our local JSON checks do not replace it. A marketplace is not required for local development loading. [Official manifest reference](https://code.claude.com/docs/en/plugins-reference), [plugin overview](https://code.claude.com/docs/en/plugins)

## Skills-only alternative

Copy the complete skill folders to project `.claude/skills/` or personal `~/.claude/skills/`, after inspecting and resolving existing names. Do not silently overwrite a user's skill. Use `/dot-mode` for this standalone route; plugin commands are namespaced. Keep companion skills together, and preserve each folder's resources.

Personal local files do not automatically become available in every hosted session. Follow the current host's documented repository/account distribution path for hosted work. Standard portable frontmatter is deliberately minimal; no shared skill grants `allowed-tools` pre-approval or embeds model/fork settings. [Official skill guide](https://code.claude.com/docs/en/skills)

## Agent roles

The plugin offers `dot-agent` for scoped engineering and `comment-reviewer` for evidence-backed read-only recommendations. Native registration comes from the plugin, not a filesystem-only copy of `skills/`. The comment reviewer limits itself to the native read/search tools and does not edit comments or application code. Its reports distinguish justified comments, misleading narration, structural improvements, and unresolved evidence.

Delegate through the actual host interface. Do not assume a fixed tool signature, background parameter, concurrency allowance, recursion depth, or model list. If workers are unavailable, continue useful sequential work and label it self-review. If the task requires independence, that requirement remains unmet. [Official subagent guide](https://code.claude.com/docs/en/sub-agents)

## Optional helpers and state

Node 22+ can run the full package's central dispatcher:

```sh
node /absolute/path/to/dot-stack/tools/dot-stack.mjs --help
```

For copied skills, use an explicitly supplied package root such as `DOT_STACK_ROOT`; verify the manifest identity and helper file. No guessed cache path or automatic dependency installation. Keep optional project preferences in `.dot-stack/config.json` and run state in `.dot-stack/state/`; never write operational state inside the installed plugin.

The helpers inspect, validate, record, or observe. They do not confer authority to publish, merge, deploy, send messages, activate a schedule, or modify account security. Follow the host's existing permission and sandbox rules, including a denial, rather than changing approval settings to finish. [Official permissions](https://code.claude.com/docs/en/permissions)

## Smoke-test checklist

1. Run the native validator and record its actual output/client version
2. Load the local plugin and confirm namespaced skill discovery
3. Ask for a bounded read-only explanation on a disposable repository
4. Verify the intended role can be selected and its resources resolve
5. Run one permitted fixture edit/check and inspect the resulting artifact
6. Disable or omit a required capability in a fixture scenario; confirm truthful fallback

These checks must run on your actual client. This package's release evidence records local checks separately from native provider runs; an absent CLI is reported as not run.
