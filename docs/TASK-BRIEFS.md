# Write a task brief that saves time

You do not need special prompt vocabulary. Give dot the information a capable colleague would need, then specify how you will judge the result.

## The six useful parts

1. **Goal:** the change or understanding you want
2. **Context:** why it matters and who will use the result
3. **Inputs:** the exact files, links, snippets or examples to use
4. **Constraints:** scope, privacy, time, format and actions that require your decision
5. **Output:** the artifact or answer you want back
6. **Checks:** observable evidence that the result is good enough

## Copyable template

```text
dot, help me [GOAL]. This is for [AUDIENCE/CONTEXT].

Use [INPUTS]. Treat [SOURCE] as authoritative, and flag conflicts or missing information instead of silently filling them in.

Stay within [SCOPE]. Do not [EXCLUDED ACTIONS]. Before using connected accounts, my computer or any external destination, check the access and any approval needed for this task. Use only the minimum necessary data.

Return [OUTPUT FORMAT] with [IMPORTANT CONTENT]. Check it against [ACCEPTANCE CRITERIA], including [EDGE CASE]. Tell me which checks you performed and which remain unverified.

If a missing answer changes the result materially, ask me. Otherwise state a reasonable assumption and continue with a reversible draft. Finish with the smallest useful next step.
```

## Weak and stronger examples

| Instead of | Try |
| --- | --- |
| “Explain this code” | “Explain the request path in these three files for an engineer joining the team. Link each claim to the supplied code and mark missing dependencies.” |
| “Fix this test” | “Investigate this test failure in the supplied log. First separate environment failures from assertion failures; propose a minimal change and say which test would verify it.” |
| “Summarize the meeting” | “Use these sanitized notes to list decisions, open questions and explicitly assigned actions. Do not invent owners or commitments.” |
| “Keep me updated” | “Prepare a dated brief on this topic every Monday morning in my stated timezone, from these sources, until this end date. Confirm the actual setup before saying it is active.” |

## Ask for one complete slice

For a new workflow, choose one ticket, one document section, one game mechanic or one source comparison. A small complete version exposes missing access and bad assumptions before you spend time expanding it.

## Iterate on the failure you can name

- **Too broad:** “Keep only the parts that affect this decision”
- **Too confident:** “Separate observed facts from inference and cite the evidence”
- **Hard to use:** “Reorganize this for the person taking the next action”
- **Hard to test:** “Turn the success criteria into observable checks”
- **Missing boundaries:** “State what you cannot establish from these inputs”

## Avoid accidental scope expansion

Reading a repository does not imply permission to publish changes. Drafting a message does not imply sending it. Preparing a schedule does not mean a reminder is active. Ask dot to report the actual milestone reached and any decision needed before the next one.
