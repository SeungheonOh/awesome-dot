# Contributing

Make the next reader more capable. Add a distinct outcome, a clearer check or real evidence, rather than another themed variation.

## Add a Markdown recipe

1. Read the [content contract](CONTENT-CONTRACT.md), [architecture](docs/ARCHITECTURE.md) and [safe-use guide](docs/SAFE-USE.md)
2. Search the [catalog](CATALOG.md) for overlapping outcomes
3. Copy [templates/RECIPE.md](templates/RECIPE.md) to `recipes/<category>/<new-id>.md`
4. Replace the metadata and every section with a specific, self-contained brief
5. Keep `status: recipe-not-run`; requested deliverables are not evidence of execution
6. Rebuild the navigation and run the checks below
7. Review the rendered Markdown and open a pull request explaining the distinct outcome

```sh
python3 scripts/build_index.py
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

Python 3.11 or newer is sufficient; no third-party packages or credentials are required. You do not need these scripts to read or use a recipe.

## Editorial checklist

- The project solves a concrete problem or creates a distinctive experience
- Its core outcome differs from existing recipes, not only the visual theme
- Inputs, access and output formats are explicit
- The main prompt includes verification and material boundaries
- Iterations introduce a meaningful change, test or extension
- Acceptance checks are observable and include an edge case
- Language is approachable to an engineer unfamiliar with AI
- No private data, secrets, hidden instructions or fabricated runs
- External factual claims have sources where needed
- Wording does not imply official OpenAI affiliation or universal feature availability

## Improve a guide

Edit the canonical Markdown. Preserve published IDs unless a migration is essential. Prefer a narrow correction with a concrete explanation. For a product-dependent issue, state the observed date and access conditions rather than presenting one account's behavior as universal.

## Submit a real run report

Use [RUN-LOG](templates/RUN-LOG.md), sanitize the evidence and link only authorized artifacts. State which checks actually ran. Export failures and blocked integrations are useful evidence when explained honestly. A report does not automatically change the recipe's status or prove broad compatibility.

## Automated checks and their limits

The checker validates the small metadata contract, required sections, source layout, unique IDs/titles/prompts, local Markdown links and generated-index freshness. Tests cover common invalid inputs. Network links are not fetched by CI. These checks cannot replace editorial review or validate account-specific features.

By contributing, you confirm you have the right to share the material and agree to distribute it under the repository's MIT License.
