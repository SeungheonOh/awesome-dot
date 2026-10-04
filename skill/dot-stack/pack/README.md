# dot-stack

![dot-stack: reason, build, prove](assets/logo.svg)

Engineering skills for ChatGPT and Claude: understand the system, choose a proportionate approach, make the change, and prove the result against the actual artifact.

This is an experimental 0.4.0 workflow library. Local structural checks do not establish better task outcomes or live-host behavior.

The pack contains **47 core skills**, **23 task playbooks**, **three optional issue-automation skills**, two reusable agent roles, and dependency-free local engineering helpers. It is a community workflow library, not an official product of either provider.

## Start with your task

Give your assistant this instruction and make the pack available:

> Use dot-stack's dot-mode for this task. Identify the smallest relevant workflow, preserve my existing work, and report what you verified and what remains unverified.

A bug fix should produce a reproduction and a regression test. An investigation should produce evidence and uncertainty, without silently changing code. A review should report actionable findings, without becoming permission to push or merge. A performance improvement should name a workload and measure the same metric before and after.

[Read the guide](docs/guide/README.md), or open the [main workflow](skills/dot-mode/SKILL.md). The [setup skill](skills/setup-dot-stack/SKILL.md) can record project preferences when requested; setup is optional.

## Use it in your environment

- [ChatGPT and Codex](docs/platforms/chatgpt-codex.md): packaging, local discovery, and the difference between installation and account access
- [Claude Code](docs/platforms/claude-code.md): native plugin and project-skill options
- [Claude custom skills](docs/platforms/claude.md): single-entry ZIP with all library resources
- [Plain chat](docs/platforms/plain-chat.md): use the instructions with supplied material, without pretending execution tools are available

The same core instructions work with the capabilities the session actually exposes. No skill grants credentials, adds a shell, creates an independent reviewer, changes permissions, or guarantees a future wake. A single-assistant second pass is self-review. A queued action is not a completed action.

## What the workflows cover

- Understand and investigate: how, why, recall, blast-radius, runtime and trace forensics
- Design and build: architect, arena, swarm, TDD, features, refactors, prototypes, TypeScript patterns
- Verify and review: interrogate, verification-skill creation and maintenance, visual parity, measured optimization
- Coordinate delivery: multi-phase plans, PR observation, candidate-bound review, authorized shipping, resumable work and safe pauses
- Improve the process: 23 focused engineering principles, reflection, technical writing, teaching and decision records
- Optional automation: evidence-based report triage and issue reproduction, dormant until explicitly configured and enabled

Select only the material relevant to the task. Rigor is evidence and sound decisions, not a compulsory committee or a long checklist for every small edit.

## Local tools

The optional helpers require Node.js 22 or later and do not install dependencies at invocation. The complete development test command also requires Python 3 for archive checks. Run from the pack root:

```sh
node tools/dot-stack.mjs doctor
node tools/dot-stack.mjs --help
node scripts/validate.mjs
npm test
```

[Tool contracts and examples](tools/README.md) explain orchestration state, PR observation, plan checks, read-only worktree auditing and decision records. State belongs in the target project or an explicitly chosen run directory, never in the installed pack. A tool's output is evidence within its stated scope, not automatic authority to publish, delete or merge.

## Verification and limits

See [verification guidance](VERIFICATION.md) for reproducible commands, coverage, and limits. Structural validation is not a productivity benchmark. Native behavior in one assistant is not proof of behavior in another. Claims of improvement must refer to the observed test or comparison, not universal superiority.

The project includes reproducible validators and executable helper tests. Live provider installation, account-specific features, external-service permissions and real production workflows require their own checks. No marketplace publication or production deployment is implied by this archive.

## Choose and build an archive

The release inventory in `distribution-files.json` explicitly names the files approved for distribution. The packager never sweeps up arbitrary files from a used checkout. Review and update that inventory when intentionally adding distributable files; local credentials, run state and debug logs do not belong in it.

Two exports serve different hosts:

- `dot-stack-0.4.0-native.zip`: the multi-skill plugin package, retaining root manifests, skills, roles, and helpers
- `dot-stack-0.4.0-single-entry.zip`: one `dot-stack/SKILL.md` entrypoint with the complete reviewed library beneath `dot-stack/pack/`, for supported single-skill surfaces

Use the [single-entry guide](docs/platforms/single-entry.md) for format details, helper paths, and checks. Neither archive grants account access or proves live upload acceptance.

With Node.js and Python 3.10+ on a POSIX filesystem, run all checks before packaging and choose fresh output paths outside this directory:

```sh
npm test
node scripts/validate.mjs
python3 scripts/package.py --format native --output /fresh/output/dot-stack-0.4.0-native.zip
python3 scripts/package.py --format single-entry --output /fresh/output/dot-stack-0.4.0-single-entry.zip
```

The packager validates the selected library and actual archived entrypoint/resources, rejects unsafe paths and symlink aliases, and exclusively creates the archive and its SHA-256 receipt. The single-entry export preserves every selected library file byte-for-byte under `pack/`; its root license duplicates the exact full notice. It refuses to overwrite either output. This verifies the reviewed inventory, not the absence of every possible secret in intentionally listed source files; inspect those contents before distribution.

## License

[MIT](LICENSE). Preserve the included copyright and permission notice when redistributing.
