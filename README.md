# dot-skills

Reusable Markdown workflows for dot. Each skill includes the inputs, steps, examples, and checks for a concrete task.

## Use a skill

1. Open a [skill](skill/) and give dot its link or contents.
2. Add your files, goal, constraints, and allowed actions.
3. Review the deliverable, its checks, and anything still unverified.

Not sure which skill fits? Start with the [task router](skill/task-to-skill-router/SKILL.md). It selects a workflow from the available skills.

Try: “Use the task router to turn these bug notes into a reproducible report. Include expected behavior, reproduction steps, and missing evidence. Save it for my review.”

Tools, account access, and approvals determine what can run. Reading a skill does not install it or grant access.

## Examples

- [Explain a budget change](skill/budget-variance-waterfall/SKILL.md): reconcile plan versus actual, including refunds. See the [worked example](skill/budget-variance-waterfall/WORKED-EXAMPLE.md).
- [Make a bug report testable](skill/bug-reproduction-triage/SKILL.md): capture reproduction steps and an evidence log.
- [Plan errands](skill/errand-window-plan/SKILL.md): account for opening hours, travel, fixed appointments, and buffers.
- [Build an orbital game](skill/orbital-game-lab/SKILL.md): implement deterministic physics and verify missions.
- [Handle engineering work](skill/dot-stack/SKILL.md): choose a focused workflow and report what was verified.

[Browse all skills](skill/)

## Evaluation

We compared 24 submissions across four synthetic tasks, with and without a designated skill package. Both conditions met all declared artifact checks; the study did not demonstrate an improvement.

[Read the evaluation](evaluation/README.md) for the setup, per-case results, raw evidence, limitations, and reproduction commands.

## Contribute

[Add a skill](CONTRIBUTING.md) with a concrete example and checks.

[MIT License](LICENSE) · Community-maintained; not an official OpenAI project.
