<picture>
  <source media="(max-width: 600px)" srcset=".github/assets/landing-hero-mobile-v2.svg">
  <img src=".github/assets/landing-hero-v2.svg" width="1280" alt="awesome-dot: community skills for dot. Reusable workflows for presentations, forms, code, and creative projects. Pick a task, follow the workflow, and check the result.">
</picture>

<p align="center">
  <a href="#use-it-with-dot"><strong>Use a skill</strong></a> ·
  <a href="#open-the-actual-output">See real files</a> ·
  <a href="#what-ai-research-has-measured">Read the research</a> ·
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

**Reusable Markdown workflows for dot.** Each skill brings together the inputs, steps, examples, and checks for a concrete task. Give dot a skill and your materials, then review the work it produces.

## Open the actual output

These files are already in the repository. The scenarios and data are fictional; the downloadable artifacts are real.

<p align="center">
  <a href="skill/source-backed-presentation/intake-pilot-example.pptx"><img src="skill/source-backed-presentation/preview.png" width="390" alt="All five slides in the fictional intake-pilot presentation"></a>
  <a href="skill/source-backed-form-fill/room-enquiry-draft.pdf"><img src="skill/source-backed-form-fill/preview.png" width="270" alt="Fictional room-use enquiry draft with supplied answers filled and unresolved fields left blank"></a>
</p>

- **A decision deck:** Approved notes → five editable slides, an evidence chart, source links, and speaker notes. [Get the PPTX](skill/source-backed-presentation/intake-pilot-example.pptx) · [Use the skill](skill/source-backed-presentation/SKILL.md) · [Verification](skill/source-backed-presentation/verification.md)
- **A filled form:** Supplied facts → nine answers in native PDF fields, with unresolved questions left open. [Open the PDF](skill/source-backed-form-fill/room-enquiry-draft.pdf) · [Use the skill](skill/source-backed-form-fill/SKILL.md) · [Verification](skill/source-backed-form-fill/verification.md)

## Pick your next task

- **Explain a spending change.** Compare plan versus actual, handle refunds, and reconcile the totals. The [worked example](skill/budget-variance-waterfall/WORKED-EXAMPLE.md) shows why a flat total can hide category changes. [Use the skill →](skill/budget-variance-waterfall/SKILL.md)
- **Make a bug report testable.** Turn a vague symptom into reproduction steps, expected behavior, and an evidence log. [Use the skill →](skill/bug-reproduction-triage/SKILL.md) · [Prepare the review handoff →](skill/code-review-handoff/SKILL.md)
- **Plan errands around real constraints.** Account for opening windows, fixed appointments, travel, and buffers; show when the plan is too tight. [Use the skill →](skill/errand-window-plan/SKILL.md)
- **Build a playable orbital lab.** Follow a method for deterministic physics, solvable missions, and numerical checks. This is a build guide, not a hosted game. [Use the skill →](skill/orbital-game-lab/SKILL.md)

[Browse all skill folders →](skill/)

## What AI research has measured

**Independent studies of other AI tools, not benchmarks of dot or these skills.** Results depend on the task, tool, and user.

<picture>
  <source media="(max-width: 600px)" srcset=".github/assets/research-stats-mobile.svg">
  <img src=".github/assets/research-stats.svg" width="1280" alt="External research: 40% less writing-task time and 18% higher writing quality scores in a 2023 experiment; 15% more customer-support issues resolved per hour in a 2025 study. These are not dot or repository benchmarks.">
</picture>

- **Writing:** A randomized experiment with 453 college-educated professionals assigned half to ChatGPT access. Average task time fell **40%** and output-quality scores rose **18%** on the studied professional writing tasks. [Noy & Zhang, Science, 2023](https://doi.org/10.1126/science.adh2586)
- **Customer support:** A field study of an AI assistant across 5,172 agents found **15% more issues resolved per hour** on average. The most experienced and highest-skilled agents had small speed gains and small quality declines. Throughput is not a measured reduction in hours worked. [Brynjolfsson, Li & Raymond, QJE, 2025](https://doi.org/10.1093/qje/qjae044)

Benefits are not universal: an [early-2025 study of experienced developers](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) found longer task times with AI. [METR’s 2026 follow-up](https://metr.org/blog/2026-02-24-uplift-update/) highlights selection and measurement problems with current estimates.

This repository has no measured time-saving or productivity benchmark. To evaluate a workflow yourself, compare similar tasks and record total time, corrections, and final quality, including review effort.

## Use it with dot

1. **Choose a skill.** Open its guide and give dot the link or paste its contents.
2. **Bring your task.** Attach the relevant files and state your goal, constraints, and allowed actions.
3. **Ask for the output and checks.** Review the deliverable, supporting evidence, and anything still unverified.

Try: “Use the presentation workflow with my attached notes. Make five editable slides, link the evidence, and flag unsupported claims. Save the deck for my review.”

Available tools, account access, and required approvals determine what can run. Reading a skill does not install it or grant access.

**Have a workflow worth sharing?** [Contribute a skill with a concrete example and checks →](CONTRIBUTING.md)

[MIT License](LICENSE) · Community-maintained; not an official OpenAI project.
