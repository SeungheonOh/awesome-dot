# Recipe content contract

Canonical recipes are UTF-8 Markdown files at `recipes/<category>/<id>.md`. A reader or dot agent can use one guide without installing software or loading a data framework. [The recipe template](templates/RECIPE.md) shows the complete format.

## Metadata

A small YAML-compatible front matter block contains exactly these fields:

- `id`: globally unique, stable lowercase kebab-case
- `title`: a specific project title, quoted as a JSON string
- `summary`: one sentence stating the outcome, quoted as a JSON string
- `category`: the containing category directory
- `level`: `beginner`, `intermediate`, or `advanced`
- `timebox_minutes`: integer 15–240; a suggested first-session planning budget, not a promise
- `capabilities`: a JSON-style list drawn from `research`, `files`, `images`, `code`, `websites`, `connected-apps`, `scheduling`, `computer-access`
- `tags`: a JSON-style list of 2–6 useful lowercase kebab-case tags
- `status`: `recipe-not-run`

Keep each metadata value on one line. This deliberately small YAML subset can be checked with Python's standard library. Full YAML syntax, custom tags and executable metadata are not supported.

## Stable body headings

- `# <Title>` and the one-line summary
- `## Scenario`: a concrete motivating situation
- `## Inputs to prepare`: 3–6 specific inputs or choices
- `## Copy this prompt into dot`: one standalone `text` code block, 120–280 words, with bracketed placeholders, a specific outcome, validation and relevant boundaries
- `## Iterate with a purpose`: exactly three named follow-up prompts that add distinct steps
- `## Expected deliverables`: 3–6 concrete outputs, described as requested rather than already made
- `## Acceptance checks`: 4–7 observable, project-specific checks, including an edge case
- `## Access, privacy and stop conditions`: 2–5 concrete prerequisites, limits or points requiring a user decision
- `## Two possible extensions`: exactly two optional next steps

The front matter supports navigation; the Markdown body contains the substance. No duplicate JSON source of the full recipe is maintained. Generated category indexes, `CATALOG.md`, `catalog.json` and the bounded README summary are derived navigation, not editable recipe content.

## Categories

`engineering-workflows`, `team-operations`, `web-games`, `3d-spatial`, `creative-coding`, `image-editing`, `design-publishing`, `personal-reminders`, `life-logistics`, `learning`, `finance`, `news-research`.

## Editorial requirements

Recipes must differ in their core outcome and acceptance criteria, not only their theme. Use plain language and fictional or sanitized inputs. The main prompt must be useful when copied on its own, including safeguards.

Capabilities vary by account, connected apps and available environment. An open app is not computer-access permission. Do not imply built-in 3D/CAD capability: scripts, rendering and exports depend on an available toolchain. Image tools need not preserve exact geometry, typography or pixels. Scheduled work needs supported scheduling, a timezone, a destination and explicit bounds; do not promise continuous observation or arbitrary instant triggers.

Finance recipes are read-only budgeting and educational analysis, not individualized investment recommendations or transactions. Sources for live research must be retrieved and dated during the actual run. Use authorized image assets. State visibility and recipients before publishing or sharing. Do not include secrets, personal account data, private assistant instructions, internal tool names, invented product controls or unverified official affiliation.

All initial recipes are `recipe-not-run`. Repository checks validate the collection, not the proposed projects. A claim of execution needs a separately reviewed [run log](templates/RUN-LOG.md).
