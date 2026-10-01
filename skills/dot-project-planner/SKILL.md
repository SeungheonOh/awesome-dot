---
name: dot-project-planner
description: An original, reusable project-planning prompt for building and checking a bounded project with dot.
---

# dot project planner

**Packaging status:** reference text, not a tested dot installation package. No automatic loading or compatibility is claimed. The dependable way to use this artifact is to paste the prompt below into a dot conversation. If another tool supports this file convention, check that tool's own installation instructions separately.

## Copyable planning prompt

```text
dot, help me turn [IDEA] into a small, checkable project for [AUDIENCE]. My desired outcome is [OUTCOME]. I can provide [INPUTS], and my constraints are [TIME, FORMAT, BUDGET, ACCESSIBILITY AND PRIVACY NEEDS].

Start by checking which required capabilities and inputs are available in this conversation. Distinguish your available environment, my connected apps and my own computer. Ask only for missing information that changes the project materially. If a dependency is unavailable, propose a useful reduced version and explain what it cannot establish.

Create a short project brief with: the user problem, the smallest complete version, explicit non-goals, inputs, expected artifact formats, three concrete acceptance checks and the main risk. Keep the first version private and use synthetic or sanitized examples where possible.

Build the smallest useful draft in the appropriate format. Inspect the actual output where you can. Test one normal case, one edge case and one repeated or interrupted action. Report what passed, failed and was not run. Do not call a generated file a working demo without testing the behavior it claims.

Then propose three distinct iterations: improve usability, address the biggest uncertainty, and add one optional capability. Explain the tradeoff before broadening the scope. Before sharing, publishing, sending, buying or changing account access, identify the destination and consequence and get any required decision from me. If scheduling is part of the project, verify the timezone, cadence, destination, stop condition and actual setup.

Finish with the artifact, a concise check report, known limits and the smallest next action. Never invent an output link, a completed action or a successful test.
```

## Review questions

- Can the user inspect a concrete result after the first pass?
- Is the hardest assumption tested rather than hidden?
- Are planned actions clearly separated from completed actions?
- Is there a safe stopping point before external consequences?

See the [main collection](../../README.md) for fully specified projects and the [run log](../../templates/RUN-LOG.md) for recording evidence.
