# Set up dot-stack

Start with one repository and one small task. You do not need to configure a model panel, install a scheduler, or connect every service before the workflows become useful.

## Choose the installation that fits your host

Follow the matching host guide rather than trying commands from another interface:

| Where you work | Start with | What to check |
| --- | --- | --- |
| ChatGPT or Codex | [ChatGPT/Codex guide](../platforms/chatgpt-codex.md) | Does the current surface discover the skill, and can it read your project? |
| Claude Code | [Claude Code guide](../platforms/claude-code.md) | Is the local plugin loaded in this session? |
| Claude with custom skills | [Claude guide](../platforms/claude.md) | Use the single-entry ZIP and verify host acceptance |
| A chat with supplied files | [Plain-chat guide](../platforms/plain-chat.md) | Are the instructions and relevant source files actually available? |

The package has one canonical `skills/` tree. The [single-entry export](../platforms/single-entry.md) wraps the full library under `pack/` for supported one-skill surfaces; its actual helper root is `dot-stack/pack/`. A full plugin and a skills-only copy are different installation choices; installing both can create duplicate discovery. Preserve the resource files beside each `SKILL.md`. Copying only the headline instructions loses references and playbooks that the workflow needs. Do not overwrite a same-named existing skill without reviewing the difference.

In ChatGPT, use the available skill selector; in Codex, use the documented skill interface. Claude Code plugin skills use a plugin namespace. Plain chat can use supplied instructions without native installation. The host guides give the exact syntax and its limits.

## Run setup without inventing capabilities

After discovery, ask:

```text
Use setup-dot-stack for this repository.
Explain what you can read, edit, execute, and review independently here.
Keep the current model. Propose any project settings before saving them.
```

[setup-dot-stack](../../skills/setup-dot-stack/SKILL.md) checks the relevant environment and proposes a practical starting point. A useful answer might say:

```text
Project files and local tests are available.
Native delegation is not available in this session.
I can implement and self-review sequentially; independent review remains missing.
No project configuration is needed for the inherited-model default.
```

That is a valid setup. It should not pretend that a second paragraph from the same assistant is an independent review.

By default, delegated work inherits the host's model. If you request a different model, setup must confirm that the host actually exposes that choice. Multiple workers on one model can still provide independent execution contexts; multiple model families are a separate property. An unavailable model is a disclosed limitation, not a reason to guess an equivalent name.

Optional project preferences belong in `.dot-stack/config.json`. They influence the workflow; they do not grant permissions or make a model available. Setup must preserve unrelated settings and save only changes you requested. It does not silently change global rules, sign in, register credentials, or enable automation.

## Know where optional helpers live

Some workflows use the Node entrypoint `tools/dot-stack.mjs` in the complete package. The entrypoint is not copied into every skill. A full installation can use its observed package root. A skills-only installation needs a separately verified package root, for example one supplied as `DOT_STACK_ROOT`, before using optional helpers.

The assistant must verify that the root identifies this package and contains the dispatcher. It must not search private host storage, download a helper automatically, or assume a relative path survived installation. Missing helpers can leave a manual next step or an equivalent authorized native operation. They cannot turn an unrun command into a passed check.

## Accept a verification workflow when it helps

Setup should look for an existing harness or project verification skill. If there is no usable path, it can offer [create-verification-skill](../../skills/create-verification-skill/SKILL.md). This creates instructions for launching and exercising your actual app; it does not make browser access appear.

Choose a project-local location appropriate to your host, as described in its guide. Before trusting the generated workflow, require one observed end-to-end run. If execution is unavailable, the output is a draft with unverified steps. [Chapter 6](06-verify-and-ship.md#create-a-project-verification-skill) explains the evidence to expect.

## Run your first task

```text
Use dot-mode to add a --json option to the existing status command.
Default output must stay byte-identical on the sample input.
JSON must parse and contain the same record count.
Do not push or open a pull request.
```

Expect a small plan with the Feature steps, the checks that establish success, and any capability gaps. A skipped step needs a reason. Follow-up instructions can refer to that plan while the session retains it, but a new chat needs the brief or a handoff; the skill is not a durable background process.

If the host can only read supplied files, ask for an unapplied patch and exact test instructions. You can still review the proposal without mistaking it for an executed change.

Next: [Route work with dot-mode](02-dot-mode.md).
