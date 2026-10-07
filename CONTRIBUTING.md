# Contribute a useful workflow

Add a reusable skill that helps someone finish a real task. Define its intended outcome and inputs clearly. Before adding a folder, check whether an existing guide can handle the request or needs a focused improvement; a new topic, file type or example alone does not require a new skill.

Put each skill in `skill/<descriptive-name>/` with `SKILL.md` as its entry point. Keep any examples and supporting files in that same skill folder. Keep the structure small. Examples and supporting files are optional; include them when they make the instructions easier to apply or verify, and link substantial detail from the point where it is useful.

Spend detail on choices that change the result:

- The task and deliverable the guide covers, and nearby requests it does not cover
- Inputs or capabilities that materially affect the work, including how to proceed when something is missing
- Transformations, decisions and failure handling that another agent needs to get right
- A usable output and meaningful ways to check it
- Action boundaries or user decisions that matter to this workflow

Apply these proportionately. A small clear task should not acquire a mandatory interview, elaborate record structure or unrelated approval round. Keep the method useful across ordinary inputs rather than building the guide around one fixture. Do not repeat generic instructions just to fill headings.

Use plain language and original synthetic or appropriately sanitized examples. Never include secrets, personal account exports or confidential work material. Source factual claims where needed, keep unknowns visible and do not claim a file, test, schedule or external action succeeded without evidence.

Try the instructions on a realistic task and inspect the resulting work. A fresh reader or a different input can expose a confusing decision more usefully than more mechanical checks of the same fixture. If you include a working example, record its actual commands, relevant environment, observed results and limits. Distinguish source inspection, calculations, file checks, application use and external delivery. Keep code small; do not introduce a framework just to maintain Markdown.

For a small, repeatable comparison, see [Evaluate one skill change](evaluation/docs/adding-a-case.md). It covers case design, authored controls, first-output evidence, and honest reporting.

Before proposing a change, read the final skill from the recipient's point of view, open its local links and inspect supporting material. Read a check's effects before running it, and run only the relevant checks supported by the environment and current authorization. Commands for later live work or long-running services are not automatic repository tests. Explain the distinct outcome or improvement and any meaningful verification limit.

By contributing, you confirm you have the right to share the material under the repository's MIT License.
