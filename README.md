# awesome-dot

## Less busywork. Clearer next steps.

**Practical skills that help dot turn everyday admin and technical work into useful results.**

A pile of information is not a finished task. These guides explain how to turn it into something you can use: a reconciled spending overview, a preparation reminder, a focused investigation or a review-ready change handoff.

Each skill gives another dot agent the inputs, steps, decisions, outputs and checks needed to carry out one concrete workflow. Pick the job you want done, give dot the skill and your relevant inputs, and review the result.

### Make everyday work easier

- **Understand where the money went:** turn planned and actual totals into a [clear budget variance explanation](skill/budget-variance-waterfall/SKILL.md)
- **Get ahead of a deadline:** create [one useful preparation reminder](skill/deadline-leadtime-alert/SKILL.md), with the timing and delivery checked
- **Untangle recurring charges:** build a [subscription cost inventory](skill/subscription-cost-inventory/SKILL.md) from a sanitized list
- **Learn with a purpose:** turn a weak spot into [focused practice with feedback](skill/deliberate-practice-workbook/SKILL.md)

### Make technical work easier

- **Make a vague bug actionable:** prepare a [reproduction brief with expected results](skill/bug-reproduction-triage/SKILL.md)
- **Reduce review back-and-forth:** build a [source-linked change handoff](skill/code-review-handoff/SKILL.md)
- **Plan a dependency change:** identify [affected usage, checks and decision gates](skill/dependency-upgrade-plan/SKILL.md)
- **Make a release decision from evidence:** prepare a [readiness packet with explicit gaps](skill/release-readiness-gate/SKILL.md)

### Give dot a job, not just a topic

```text
dot, use this skill to help me finish [TASK]: [SKILL LINK OR TEXT].

Use [INPUTS]. Produce [DELIVERABLE] for [AUDIENCE] and stay within [SCOPE]. Follow the skill's decision points and checks. Ask when a missing answer changes the result, and tell me which checks you actually performed.

Keep the work private. Before any external action that needs my decision, explain what will change and where.
```

These are readable instructions, not a claim that dot automatically installs arbitrary files. Capabilities depend on the tools and access available in the conversation. A useful draft, an executed check and a completed external action are different milestones.

### One skill, one folder

Everything for a workflow belongs together:

```text
skill/
  workflow-name/
    SKILL.md
    examples/       # only when useful
    supporting files
```

Start with the skill's inputs. Follow its procedure. Inspect the actual deliverable. Stop at a missing permission, consequential decision or unsupported capability instead of inventing a successful result.

[Contribute a useful workflow](CONTRIBUTING.md)

This is a community project, not an official OpenAI project or endorsement. Original text and code use the [MIT License](LICENSE).
