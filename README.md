# awesome-dot

## A practical dot guide for engineers

**Use OpenAI dot to make progress on familiar work, even if you are new to AI assistants.**

Start with a small task, give dot enough context, and check the result. Then explore original project recipes for engineering, research, everyday life, visual work and playful experiments.

**[Start at work: turn a fictional bug report into a useful plan](docs/WORKPLACE-QUICKSTART.md)**

No account connections, repository access or installation needed for the example. It is a short first-session exercise, not a promise about completion time.

[Browse recipes](CATALOG.md) · [Write a better task brief](docs/TASK-BRIEFS.md) · [Read as a dot agent](docs/AGENT-GUIDE.md) · [Understand access](docs/CAPABILITIES.md)

### What would you like to do?

- **Make a vague work request actionable:** [try the workplace quickstart](docs/WORKPLACE-QUICKSTART.md)
- **Get better results with less back-and-forth:** [use a task brief](docs/TASK-BRIEFS.md)
- **Know what is safe to provide at work:** [check the corporate data guide](docs/CORPORATE-DATA.md)
- **Find a concrete project:** [open the catalog](CATALOG.md)
- **Understand unfamiliar terms:** [read the plain-language glossary](docs/GLOSSARY.md)
- **Grow beyond your first task:** [follow a learning path](docs/LEARNING-PATHS.md)

### What is inside?

Each original recipe has a specific goal, an input checklist, a standalone copyable prompt, three follow-up iterations, expected deliverables, observable acceptance checks and project-specific boundaries. Canonical content is Markdown, readable by people and usable as a brief for another dot agent.

<!-- catalog-summary:start -->
**70 original recipes · 7 categories · every recipe marked not run**

| Explore | Recipes |
| --- | ---: |
| [Team operations](recipes/team-operations/README.md) | 10 |
| [Web games](recipes/web-games/README.md) | 10 |
| [3D and spatial studies](recipes/3d-spatial/README.md) | 10 |
| [Creative coding](recipes/creative-coding/README.md) | 10 |
| [Image editing](recipes/image-editing/README.md) | 10 |
| [Design and publishing](recipes/design-publishing/README.md) | 10 |
| [Finance](recipes/finance/README.md) | 10 |
<!-- catalog-summary:end -->

### Start a useful conversation

> dot, help me achieve [OUTCOME] using [INPUTS]. The audience is [WHO] and the constraints are [LIMITS]. First check what you can do with the access available here. Produce [DELIVERABLE], then check [ACCEPTANCE CRITERIA]. Ask before any step that needs a decision from me. Keep the first version private and tell me what remains unverified.

For a more specific starting point, copy a recipe's main prompt and replace its bracketed placeholders. You do **not** need to install this repository into dot. An [optional reusable planning prompt](skills/dot-project-planner/SKILL.md) is provided as text; automatic installation or loading is not claimed.

### Be ambitious about the result, precise about the evidence

All project recipes are **proposed, not executed demonstrations**. Their acceptance checks tell you how to inspect a future result; they are not proof that the project already works. Repository checks only validate the collection itself. Access, tools and supported actions vary by account and environment.

Scheduling needs confirmed setup. 3D scripts and exports need compatible software. Image inputs must be authorized. Finance projects are read-only analysis and budgeting, not transactions or investment recommendations. Review data, recipients and visibility before sharing. See [capabilities](docs/CAPABILITIES.md), [safe use](docs/SAFE-USE.md) and [status definitions](docs/STATUS.md).

### A Markdown-first repository

| Path | Purpose |
| --- | --- |
| `recipes/` | Canonical project guides, grouped by outcome |
| `docs/` | Workplace onboarding, task briefing, access and review guidance |
| `templates/` | A recipe template and an honest project run log |
| `skills/dot-project-planner/` | Optional original planning prompt, with copy/paste fallback |
| `scripts/` and `tests/` | Small index and content checks, not a required runtime |

See the [architecture](docs/ARCHITECTURE.md) and [contribution guide](CONTRIBUTING.md) for the content contract and maintenance workflow.

This community-authored repository is not an official OpenAI project or endorsement. Original text and code use the [MIT License](LICENSE); product names and third-party assets remain subject to their owners' rights.
