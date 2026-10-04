# Single-entry Agent Skills export

Choose this export when the host supports one custom-skill folder with bundled resources. It avoids copying individual workflows and assembling their dependencies by hand. The native multi-skill plugin remains the preferred route for plugin-capable hosts, with separate skill discovery and native manifest handling.

## Layout and use

```text
dot-stack-0.4.0-single-entry.zip
└── dot-stack/
    ├── SKILL.md       # short read-on-demand router; name: dot-stack
    ├── LICENSE        # exact full MIT notice
    └── pack/          # complete reviewed library, preserved byte-for-byte
        ├── skills/
        ├── automations/
        ├── tools/
        ├── docs/
        └── ...
```

The root routes an engineering task into the existing dot-mode resource. Only the chosen workflow and required references need to be read. Relative links inside the library retain their original file-relative meaning. The bundled native manifests and role files are resources; merely uploading this export does not activate a plugin, register workers, enable automation, or grant permissions.

For [Claude custom skills](claude.md), use the single-entry ZIP in the actual supported upload flow. For [ChatGPT or Codex](chatgpt-codex.md), choose the route your surface exposes; do not assume ZIP upload is universal. [Plain chat](plain-chat.md) remains available when no installation mechanism exists. Ask for dot-stack or select its actual displayed entrypoint, then give a bounded engineering task.

The documented [Claude folder and resource format](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) and [Agent Skills specification](https://agentskills.io/specification) inform this layout. Nested resources are allowed by the specification; their depth and the library's breadth still require real host acceptance and task checks. Local format validation is not that acceptance.

## Build and inspect locally

From the native source root, using Python 3.10+, Node.js, and POSIX no-follow filesystem support:

```sh
python3 scripts/package.py --format native --output /fresh/output/dot-stack-0.4.0-native.zip
python3 scripts/package.py --format single-entry --output /fresh/output/dot-stack-0.4.0-single-entry.zip
```

Both commands select only `distribution-files.json`, stage and validate the selected library, then verify the actual archived resources. The single-entry check also validates root metadata, template equality, local entrypoint links and both complete license copies. Literal local ESM imports and Markdown file links are checked; this is not a general parser for arbitrary code or a proof of externally supplied files, runtime-generated paths, or remote URLs.

Each fresh output receives an adjacent `.zip.manifest.json` receipt recording the ZIP SHA-256, size, format, and file hashes. The wrapper preserves every reviewed library file under `pack/`; the receipt names the entrypoint and resource root. Unlisted checkout files cannot enter the archive. Listed contents still require human review for secrets. Source aliases, output aliases, traversal, special files, private-state names, case-colliding inventory entries, and existing output/receipt files are rejected. An ordinary failure removes only files this invocation created. A forced kill or power loss can leave partial new files; it does not authorize overwriting them on retry. Identical reviewed bytes produce identical ZIP bytes in the same Python/zlib environment.

Extract a validated ZIP into a fresh disposable directory. From the extracted `dot-stack/` folder, the read-only local checks are:

```sh
node pack/scripts/validate.mjs "$PWD" --single-entry
node pack/tools/dot-stack.mjs doctor
node pack/tools/dot-stack.mjs --help
```

The helper location is `dot-stack/pack/`, with `plugin.json` identifying `dot-stack` and `tools/dot-stack.mjs` present. For work in a separate target project, set `DOT_STACK_ROOT` to the absolute `dot-stack/pack/` path and use `node "$DOT_STACK_ROOT/tools/dot-stack.mjs" ...`. Do not point it at the outer skill directory or guess a host-private installation path. Keep project/run state in the target project, outside the installed skill. Helpers require Node 22+; missing runtimes are an unrun capability, not an instruction to install them.

## Verify the actual host separately

When upload/installation is authorized, confirm the skill appears, run one read-only explanation on supplied material, verify the selected nested workflow is readable, then try a missing-capability case. Report upload acceptance, resource access, helper execution and task behavior separately. This release's local checks did not upload, activate, or execute the export in a live ChatGPT/Claude account. No reasoning-performance improvement is established by packaging tests.
