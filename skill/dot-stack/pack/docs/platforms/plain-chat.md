# Use dot-stack as instructions

This route works with a plain ChatGPT or Claude conversation when you can supply the relevant workflow and task materials. It does not install skills or add tools.

## Give the assistant a bounded brief

Paste the relevant `SKILL.md` text, or attach a readable file together with any referenced material it needs. A URL works only if the host can actually retrieve it. For a broad engineering task, begin with `skills/dot-mode/SKILL.md`; for a specific review or explanation, choose the focused skill instead of loading the whole catalog.

Example:

> Use the supplied bug-fix workflow to review these two source files. The expected result is one saved item per click. Identify a likely cause, propose the smallest patch, and give a regression test. You do not have my repository or a shell, so label the patch unapplied and tests unrun. Do not publish or contact anyone.

State the goal, available evidence, constraints, allowed actions, and what counts as done. Bring missing files rather than asking the assistant to infer their contents.

## What a useful answer can contain

- A code-path explanation with evidence from supplied files
- A design comparison, tradeoffs, and a concrete decision criterion
- A proposed patch and the exact behavior it should change
- Test cases, expected results, and commands for an execution host
- A review with specific findings and clearly stated coverage limits
- A resume brief separating completed work from planned work

It cannot truthfully claim to have edited your files, run commands, inspected an unavailable browser, spawned independent workers, checked a live PR, or scheduled a future run without actual tools and evidence. Role-playing several reviewers is still one assistant's analysis.

## When tools become necessary

If your desired result requires execution, provide the relevant files to a tool-enabled host or use a supported coding environment. The assistant should continue permitted analysis and ask only for the missing access or decision that changes the next step. A permission denial must be respected; supplying another path or transport is not a workaround.

For safe handoff, carry the exact source revision/file identities, intended behavior, proposed patch, unresolved questions, and required checks into the execution session. Have that session re-read the current artifacts before applying anything. Old conversation confidence is not current candidate evidence.
