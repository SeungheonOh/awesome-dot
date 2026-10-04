# The dot-stack guide

dot-stack turns an engineering goal into a small, checkable workflow. You describe the result, the constraints, and the evidence you need. `dot-mode` chooses a playbook; the other skills help understand, design, build, review, and verify the work.

The same instructions work with ChatGPT/Codex and Claude. Their tools differ. A skill supplies a method, not a shell, an independent reviewer, a connection to your repository, or permission to publish. This guide shows both the executable route and what to do when a capability is missing.

## Start here

1. [Set up dot-stack](01-setup.md): choose your host, discover the skills, and try a small task
2. [Route work with dot-mode](02-dot-mode.md): give a useful brief and find all 23 playbooks
3. [Understand before editing](03-understand.md): trace behavior, history, and unfinished work
4. [Design the change](04-design.md): compare alternatives and choose useful review coverage
5. [Build and clean](05-build-and-clean.md): reproduce, implement, and keep the diff focused
6. [Verify and ship](06-verify-and-ship.md): prove behavior and separate readiness from authorization
7. [Work while you are away](07-overnight.md): bound a long run and leave resumable evidence
8. [Steer with principles](08-principles.md): use all 23 principles to change concrete decisions
9. [Make it yours](09-make-it-yours.md): capture a workflow and test its instructions
10. [Recipes and pitfalls](10-recipes-and-pitfalls.md): copy a prompt and avoid common traps

Read the first two pages once. After that, start with the page for the work in front of you.

## A good first brief

```text
Use dot-mode to add JSON output to this command.
Keep existing text output byte-for-byte unchanged.
Run both forms against the sample project and show the results.
Work locally; stop before publishing anything.
```

Throughout the guide, `Use <skill-name> ...` is ordinary prompt text. Select or load that skill using your host's supported interface. It is not a universal slash command. Installation and invocation are covered in the guides for [ChatGPT/Codex](../platforms/chatgpt-codex.md), [Claude Code](../platforms/claude-code.md), [Claude custom skills](../platforms/claude.md), and [instruction-only chat](../platforms/plain-chat.md).

## The complete skill map

There are 47 core skills: 24 workflows below and [23 principles](08-principles.md). The playbooks are steps used by `dot-mode`, not another set of installed skills.

- Start and plan: [dot-mode](../../skills/dot-mode/SKILL.md), [setup-dot-stack](../../skills/setup-dot-stack/SKILL.md), [figure-it-out](../../skills/figure-it-out/SKILL.md)
- Understand: [how](../../skills/how/SKILL.md), [why](../../skills/why/SKILL.md), [teach](../../skills/teach/SKILL.md), [recall](../../skills/recall/SKILL.md)
- Design and examine: [architect](../../skills/architect/SKILL.md), [arena](../../skills/arena/SKILL.md), [swarm](../../skills/swarm/SKILL.md), [interrogate](../../skills/interrogate/SKILL.md), [blast-radius](../../skills/blast-radius/SKILL.md)
- Build and check: [tdd](../../skills/tdd/SKILL.md), [typescript-best-practices](../../skills/typescript-best-practices/SKILL.md), [no-comments](../../skills/no-comments/SKILL.md), [create-verification-skill](../../skills/create-verification-skill/SKILL.md), [maintain-verification-skill](../../skills/maintain-verification-skill/SKILL.md)
- Explain and improve the workflow: [technical-writing](../../skills/technical-writing/SKILL.md), [unslop](../../skills/unslop/SKILL.md), [bro](../../skills/bro/SKILL.md), [show-me-your-work](../../skills/show-me-your-work/SKILL.md), [automate-me](../../skills/automate-me/SKILL.md), [reflect](../../skills/reflect/SKILL.md)
- Build a bounded local interface: [make-bot-ui](../../skills/make-bot-ui/SKILL.md)

Three additional automation workflows live in the dormant [Benny recipes](../../automations/benny/README.md): [setup-benny](../../automations/benny/skills/setup-benny/SKILL.md), [triage-issue-reports](../../automations/benny/skills/triage-issue-reports/SKILL.md), and [reproduce-and-fix-issues](../../automations/benny/skills/reproduce-and-fix-issues/SKILL.md). Reading or installing them does not enable a trigger or authorize an external response. [Chapter 7](07-overnight.md#queues-and-event-driven-work) explains that boundary.

## What a trustworthy result says

- **Verified:** a named check passed on the stated artifact in the stated environment
- **Failed:** the observed result contradicted the acceptance condition
- **Unverified:** a required proof was not obtained, including stale or missing evidence
- **Blocked:** the next required action needs information, access, authority, or a decision

A useful report can contain all four. “Unit tests verified; browser behavior unverified; publication blocked pending approval” is more useful than an unsupported “done.”

Next: [Set up dot-stack](01-setup.md).
