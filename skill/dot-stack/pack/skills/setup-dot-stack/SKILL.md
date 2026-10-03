---
name: setup-dot-stack
description: "Inspect available workflow capabilities and optionally save project-local dot-stack concurrency, model-role, and artifact preferences. Use to configure dot-stack for the current project without changing host permissions or global settings."
---

# Setup dot-stack

Default use needs no configuration. The assistant inherits its current model and uses available authorized tools. Optional `.dot-stack/config.json` expresses workflow preferences; it does not create capabilities, enforce a spending limit, or change the host's security and permission rules.

## Inputs and scope

Identify the target project, requested preferences, and the host's actually exposed choices. A request to explain configuration is read-only. A request to save project configuration authorizes that bounded file change, subject to host rules. Setup never installs software, changes global settings, registers tools, signs in, creates credentials, enables triggers, or writes host permission grants.

## Steps

1. Inspect the project path and repository instructions. Resolve the real project root and existing `.dot-stack` path. Do not follow a symlink into another project or global directory to write settings. Read any existing config in full before planning an update; preserve user data and unrelated files.
2. Discover only relevant capabilities: readable/writable project, execution, independent workers, actual model choices, browser/app driver, connected service read, and persistence if requested. Report missing capability honestly. If no model catalog is exposed, use `inherit`; do not ask the user to guess identifiers or invent a nearest model.
3. Translate the user's budget into bounded workflow choices, not provider-specific model-string surgery. Propose a suitable maximum concurrency and evidence scope. A model/effort change is used only if its exact choice is exposed and supported by that host; this config has no separate effort field. Do not promise a dollar cap from concurrency alone.
4. Show only requested changes and material unresolved choices. Model roles are optional keys meaningful to the workflow, such as implementation, review, investigation, writing, or a named specialized role. Role keys use lowercase letters, digits, and hyphens, beginning with a letter. Each value is `inherit` or an exact observed host choice. An inherited review model does not create an independent reviewer. Panel membership, if needed, is defined in the task brief and actual host controls, not invented by repeating an unavailable model.
5. Validate with the bundled [schema](../../config/config.schema.json). Supported fields are `schema_version` (1), optional positive-integer `max_concurrency`, optional `role_models` object with nonempty string values, and optional project-relative `artifact_directory`. Omitted preferences retain inherited workflow behavior. Confirm each non-inherit model is currently selectable; schema validity alone does not establish entitlement.
6. Validate artifact path containment both lexically and against the actual filesystem before writing there. Reject absolute paths, traversal, and symlink escapes. Existing unknown config fields cause validation failure; do not drop them silently or overwrite the file. Explain the unsupported field and preserve the original while the user decides how to reconcile it. A malformed file is similarly held for repair rather than reset to defaults.
7. Save only agreed/requested preferences, preserving unaffected valid fields. Use a safe atomic replacement after checking the source has not changed concurrently. If a new config would be identical, leave it unchanged. Do not overwrite another writer's update. Do not add config to version control or change ignore rules unless requested or covered by project convention and authority.
8. Read the saved file back and validate it. With a verified full-pack root, run `node "$DOT_STACK_ROOT/scripts/validate-config.mjs" .dot-stack/config.json`. Verify that root's manifest names `dot-stack` and the actual validator exists; copied skills alone may not contain it. If unavailable, inspect the documented structure and clearly report that the executable validator was not run. Never download a helper silently.

## Minimal shape

The example below uses inherited models only. It illustrates a possible requested configuration; do not save it automatically.

```json
{
  "schema_version": 1,
  "max_concurrency": 2,
  "role_models": {
    "implementation": "inherit",
    "review": "inherit"
  },
  "artifact_directory": ".dot-stack/artifacts"
}
```

## Failure and completion

No writable project yields a proposed config, explicitly unsaved. No model catalog still permits inherited operation. An unavailable explicit model needs a user choice or a disclosed allowed fallback; do not silently substitute. A denied write stops that mutation without rerouting to a different tool.

Return the saved or proposed path, changed preferences, validation result, missing capabilities, and their effect. These are instructions that workflows read; the helper runtime does not automatically enforce model selection or concurrency. Do not claim global application, installation, or activation in a future session.

If the project lacks a useful behavioral harness, mention [create-verification-skill](../create-verification-skill/SKILL.md) as an optional next step only when relevant. Do not create it or repeatedly propose it after a decline.
