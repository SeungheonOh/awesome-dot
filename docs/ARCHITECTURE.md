# Architecture and editorial design

## The design problem

A long list of prompts is easy to make and hard to use. This collection organizes original dot projects around distinct outcomes, with enough context to begin and enough checks to evaluate the result. Engineers new to AI start with familiar work before moving to richer creative or connected workflows.

## Information architecture

1. **README:** an approachable workplace-first entry point and clear task routes
2. **Workplace quickstart:** a complete fictional exercise with no account connection or install
3. **Task briefing, glossary and corporate data guidance:** shared working habits in plain language
4. **CATALOG and category indexes:** a directory of specific outcomes
5. **Canonical recipe pages:** stable Markdown briefs usable by humans and dot agents
6. **Learning paths:** deliberate progressions without duplicated projects
7. **A small template and checker:** maintainability without a framework dependency

Categories separate engineering, team operations, games, spatial studies, visual work, everyday plans and evidence-based understanding. They are navigation, not claims that dot has a built-in feature for every domain.

## Canonical Markdown, derived navigation

Each `recipes/<category>/<id>.md` file is the source of truth. A short front matter block supports routing by outcome, difficulty and required capability. Stable body headings expose the inputs, prompt, iterations, deliverables, checks and stop conditions. There is no duplicate JSON source containing the full recipe text.

A small Python script derives category indexes, `CATALOG.md`, a compact metadata-only `catalog.json`, and the bounded summary block in README. The scripts are maintenance conveniences; readers and dot agents can consume the Markdown directly without running or installing anything.

The [content contract](../CONTENT-CONTRACT.md) describes the supported metadata subset and body structure. The checker uses Python's standard library. It validates structure, local links, uniqueness and generated-index freshness. It cannot prove usefulness, safety or product availability; human review and actual project checks remain necessary.

## Stable identifiers

IDs are global, stable kebab-case strings. Paths include their category. Keep published IDs stable. A category move requires updating references. Rich instructions belong in the body, not in an expanding metadata model. Change the contract, template, parser and tests together when the structure genuinely needs to evolve.

## Distinctness rule

Two projects must differ in their core user outcome and important acceptance criteria. A new color palette, renamed reminder, new game skin or different news topic is insufficient. No count target justifies padding. Workplace guides and creative recipes serve different entry points without pretending every hobby project is corporate work.

## Quality gates

- Metadata, identifiers, paths and stable headings agree
- Main prompts are substantive and self-contained
- Each recipe includes three useful iterations and observable checks
- Exact duplicate IDs, titles and prompts are rejected
- Local links and generated indexes are current
- Initial recipe status remains explicitly not run
- No private data, credentials or fabricated execution evidence

The repository checks do not execute projects, browse every external source or test integrations. CI is evidence about the content package only.

## Why no installer?

These are project briefs. Copy/paste is the baseline interface. The optional planner under `skills/` is an original text artifact with familiar packaging, not a claim that dot automatically recognizes arbitrary skill files. The repository does not depend on a private API, a particular account tier or undisclosed product controls.
