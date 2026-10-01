# Contribute a useful workflow

Add a skill that helps someone finish a concrete task. Favor a clear, useful procedure over another idea, prompt variation or broad promise.

Put everything for it in `skill/<descriptive-name>/`. The entry point is `SKILL.md`; keep examples, sample inputs and supporting files beside it. Keep the structure small and the instructions focused on the outcome.

A good skill explains:

- When the workflow is useful and what outcome it produces
- The exact inputs and access needed, including what to do when something is missing
- Ordered steps, calculations or transformations that another dot agent can follow
- Decision branches, failure handling and points where the user must choose
- The output structure and observable checks, including an edge case
- Which actions require permission, and when to stop

Use plain language and synthetic or sanitized examples. Never include secrets, personal account exports or confidential work material. Source factual claims where needed, keep unknowns visible and do not claim a file, test, schedule or external action succeeded without evidence.

If you add a working example, record the commands, relevant environment, observed checks and limits in the same skill folder. A partial demonstration is useful when its scope is clear. Keep code small and explain it in the guide; do not introduce a framework just to maintain Markdown.

Before proposing a change, read the final skill as if you were the person or dot agent receiving the task. Open its local links, inspect its examples, and run any included checks. Explain what distinct problem it solves and what remains unverified.

By contributing, you confirm you have the right to share the material under the repository's MIT License.
