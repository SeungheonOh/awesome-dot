# Make the workflow yours

A reusable skill should capture a decision process that helps on the next task. It should not turn one unusual session into a permanent rule, hide account-specific assumptions, or silently give future runs more permission.

## Capture preferences with automate-me

```text
Use automate-me with these three supplied task summaries.
Find repeated preferences about explanation, review, and verification.
Show which examples support each proposed rule before drafting a personal mode.
```

[automate-me](../../skills/automate-me/SKILL.md) can use authorized history or material you provide. It must not assume access to private transcript files. Ask it to distinguish an explicit lasting preference, a repeated pattern, and a one-off choice. You decide which patterns belong in the new workflow.

Choose a project-local skill destination that your host supports. Keep its purpose narrow and its resource references complete. A personal mode can describe preferred communication and engineering habits; it cannot preapprove publishing, change account settings, or create new credentials merely by containing those instructions.

For an update, supply the prior skill and the relevant newer examples. Preserve unaffected preferences and show the proposed changes. Do not claim to have mined “everything since last time” unless that history was actually available.

## Reflect on a difficult task

```text
Use reflect on this handoff and decision log.
Identify what would have changed the failed attempts.
Separate useful rules from one-off advice. Propose edits before applying them.
```

[reflect](../../skills/reflect/SKILL.md) gathers lessons, tests whether they generalize, and presents accepted candidates, rejected proposals, and a backlog. Native reviewers can supply independent perspectives when available. A sequential self-review is still useful, but should be described accurately.

Prefer a rule with a trigger and observable effect: “Before comparing parser speed, freeze the input and warm-up procedure.” Avoid vague commandments such as “be more careful.” If a lint or test can enforce the lesson, consider that structure before adding prose every future assistant must remember.

## Author one focused skill

```text
Use dot-mode to draft a skill for reviewing database migrations in this repository.
It should inspect schema changes, rollback assumptions, and representative data.
Make it read-only by default and list the checks that need a disposable database.
```

The [Authoring a skill playbook](../../skills/dot-mode/playbooks/authoring-a-skill.md) helps define the trigger, required inputs, procedure, outputs, constraints, and missing-capability behavior. It can use a supported host authoring tool if one exists, or produce portable files directly. No universal built-in creation command is assumed.

A useful draft answers:

- When should this skill load, and when should it not?
- What evidence must the user or host supply?
- What does the workflow do with each input?
- Which actions are read-only, local mutations, or external mutations?
- What proves success, and what leaves the result unverified?
- Where are its examples and other required resources?

Validate frontmatter, naming, links, and resource closure. Then try a realistic task and a missing-capability case. A syntactically valid `SKILL.md` can still give unsafe or useless instructions.

Verification skills have a specialized route: [create-verification-skill](../../skills/create-verification-skill/SKILL.md) and [maintain-verification-skill](../../skills/maintain-verification-skill/SKILL.md). [Chapter 6](06-verify-and-ship.md#create-a-project-verification-skill) explains the required proof run.

## Write for the reader

[technical-writing](../../skills/technical-writing/SKILL.md) distinguishes tutorials, how-to guides, reference, and explanations. Pick one primary job for each page. A beginner tutorial should lead to one successful result; a reference should make exact details easy to find.

```text
Use technical-writing to review this setup guide for a first-time contributor.
Check every prerequisite and distinguish commands they run from expected output.
Use unslop afterward to remove repetition without removing warnings or evidence.
```

[unslop](../../skills/unslop/SKILL.md) improves prose clarity. It must preserve uncertainty, scope, caveats, and legal notices. [bro](../../skills/bro/SKILL.md) can restate a dense explanation in plain language without changing its claims.

## Evaluate a change before trusting it

The [Eval playbook](../../skills/dot-mode/playbooks/eval.md) compares instruction variants with the same task, inputs, allowed tools, and scoring criteria. Define the rubric before reading outputs, keep candidate environments isolated, and record the actual files and tools each run used where the host exposes that evidence.

```text
Compare the current migration-review skill with this proposed version.
Use the same two synthetic migrations and a fixed defect checklist.
Report missed defects, false positives, permission handling, and execution limits.
```

Neutral candidate labels and independent scoring can reduce bias. They do not make an evaluation independent if one assistant generated and scored every result. If separate execution contexts are unavailable, call it a structured dry run, not a blinded agent experiment. Never fabricate tool traces or execution evidence.

Read the outputs as well as the scores. A higher score on one fixture is not proof of broad improvement. Include cases where dependencies are absent, a user asks for read-only work, and the apparent next step requires external authorization.

Keep instruction changes separate from feature work when practical. That makes it possible to review, compare, and revert the workflow change on its own.

Next: [Recipes and pitfalls](10-recipes-and-pitfalls.md).
