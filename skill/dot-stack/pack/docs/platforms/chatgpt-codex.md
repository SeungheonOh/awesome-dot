# ChatGPT and Codex

Choose the route matching your actual host. The same workflow can be useful without every execution capability. dot-stack supplies instructions and optional local helpers; it does not install connectors, choose your account model, or grant permissions.

## Local filesystem skills

For Codex CLI or supported local skill discovery, place the **contents of the pack's `skills/` directory** under project `.agents/skills/` or user `~/.agents/skills/`, preserving each complete skill folder. Inventory existing names first; compare collisions rather than overwrite them. Keep the pack together when workflows reference companion skills. The package's root `agents/` files are not automatically registered as Codex agents.

Use `/skills` or `$dot-mode` in Codex CLI/IDE. In ChatGPT's skill picker, use `@` and select the actual displayed skill. Natural-language matching also depends on each skill description. Restart the client if changed skills do not appear. These are the documented discovery/invocation surfaces, not a universal slash-command interface. [Official skill guide](https://learn.chatgpt.com/docs/build-skills)

A skills-only copy does not bring the optional helper `tools/` directory with it. Retain the full package elsewhere if you need those helpers; see **Optional tools** below.

## Single-entry resource export

If your actual ChatGPT surface accepts a single Agent Skills folder, use `dot-stack-0.4.0-single-entry.zip` and the [single-entry guide](single-entry.md). It supplies one root skill named `dot-stack` with all library resources under `pack/`. Do not assume every ChatGPT account or interface accepts ZIP uploads; use the feature your host actually exposes. A normal chat attachment is supplied context, not proof of skill installation. For plugin-capable hosts, use the native archive below.

## Portable plugin package

The root `plugin.json` and root `skills/` form the portable package. The provided `.claude-plugin/` metadata serves the other host; do not move resources into manifest directories.

For an optional local marketplace, place the package at a known path inside your marketplace root, for example `plugins/dot-stack`, and add a local catalog entry at `.agents/plugins/marketplace.json`. Preserve existing catalog entries. The entry must name `dot-stack`, point at `./plugins/dot-stack`, and include the host's required install/authentication policy and category. Use the current official catalog example rather than inventing an install URL. Registering a catalog with `codex plugin marketplace add <local-marketplace-root>` does not by itself verify plugin installation. The documented local test flow uses the ChatGPT desktop plugin directory; restart and inspect the actual installed plugin and skill list. [Official packaging and local installation](https://developers.openai.com/plugins/build/plugins)

This release is a local package. It does not claim public-directory publication or an installed workspace entry. Workspace publishing/sharing requires the relevant authority and a verified destination. Local files, workspace skills, plugin availability, and connector authorization have separate controls; installing this package does not connect accounts. [Official skill controls](https://learn.chatgpt.com/docs/enterprise/skills)

## Optional tools

The full pack includes dependency-free Node helpers, requiring Node 22 or newer. Use the root the host actually supplies, or explicitly set `DOT_STACK_ROOT` to your extracted library directory: `dot-stack/` in the native archive, `dot-stack/pack/` in the single-entry archive. Confirm that `plugin.json` names `dot-stack` and `tools/dot-stack.mjs` exists. Then inspect its help:

```sh
node "$DOT_STACK_ROOT/tools/dot-stack.mjs" --help
```

Do not guess a cache path, recursively scan private host folders, install a runtime automatically, or assume `../../tools` survives a skill-folder copy. Run project work against the explicit target project; helper location is not the target working directory. If Node or the helper is absent, use an existing equivalent permitted tool or report the unrun step. State belongs in the target project's `.dot-stack/state/`, not the installed package.

## Delegation and permissions

Use native workers only when available in this session. Pass the bounded role instructions and required skill references; do not invoke a fictional tool named after this package. Codex custom agents use a different TOML configuration format, so the package's Markdown roles can be included in briefs without claiming native registration. Hosted ChatGPT workers and local Codex sessions expose different controls and inherit applicable parent restrictions. [Official subagent guide](https://learn.chatgpt.com/docs/agent-configuration/subagents)

Use inherited models by default. Mark self-review and same-model review accurately. No native delegate means useful sequential work can continue, but an independent-review requirement remains unverified. No scheduler means no promised future wake. A blocked external write must not be retried through another transport.

## Verify your installation

Ask for a read-only explanation of a supplied tiny repository using `dot-mode`; confirm the expected skill actually loads and companion references resolve. Then use a disposable fixture to test a local edit and check. Finally test a request requiring an unavailable capability: the assistant should report the gap instead of claiming execution. Record the client version and package revision. Structural validity does not establish live behavior on your account.
