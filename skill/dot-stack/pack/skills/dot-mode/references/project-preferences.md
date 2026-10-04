# Project preferences

Read when the authorized project has `.dot-stack/config.json`, before role selection, delegation, or evidence artifact creation. This reference supplements the [execution contract](execution-contract.md); it grants no capabilities or permissions.

At the start of a relevant engineering task, resolve the actual authorized project root and check for `.dot-stack/config.json` there. Do this before selecting role models, spawning workers, or creating evidence artifacts. If absent, inherit the current model, choose proportional concurrency within host limits, and use the normal project/run location. Never search global or private host directories for a substitute.

If present, read the file in full without modifying it and validate the [project schema](../../../config/config.schema.json). With the verified pack root, the optional validator is `node "$DOT_STACK_ROOT/scripts/validate-config.mjs" <project>/.dot-stack/config.json`. When it is unavailable, inspect the same structure manually and state that executable validation was not run. Resolve filesystem containment before creating artifacts, including symlinks in `.dot-stack` or the configured path.

Apply valid values as workflow instructions:

- `max_concurrency` is the ceiling for this run's simultaneous delegated workers across nested owners, not a target to fill. Use the lower of it, the host's actual limit, and a narrower current user budget. Track admission centrally or allocate non-overlapping sub-budgets; do not give every child the entire cap. Sequential work remains valid.
- `role_models` maps the role used in the task brief to `inherit` or an exact host-exposed choice. Select that supported model through the real host controls when possible. `inherit` and omitted roles use the parent model. An explicit current user choice takes precedence. Model preference never creates independence or overrides the host's supported reasoning settings.
- `artifact_directory` is the project-relative destination for newly created evidence and decision artifacts. Verify its real resolved destination stays within the authorized project. Operational helper state remains `.dot-stack/state/default` or the explicitly selected store; do not relocate runtime state implicitly. Keep outputs free of secrets and obey sharing boundaries.

Relay effective role choice, concurrency allocation, artifact location, and any applicable current override in delegation briefs. On resume, reread current preferences before spawning or writing new artifacts. Changes do not retroactively relocate existing evidence or magically reconfigure running owners; reconcile those deliberately.

Malformed JSON, unknown fields, invalid paths, unsupported values, unavailable explicit models, and missing model-selection controls are named configuration gaps. Preserve the file unchanged. Continue unaffected authorized work, but hold the dependent choice and ask for a specific correction or permission to use a disclosed inherited/default alternative. Do not silently discard a setting or claim it was applied. A missing optional catalog with no explicit model preferences still permits inherited operation. Schema checks establish structure, never entitlement or authority.

