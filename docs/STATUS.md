# What has and has not been tested

## Current recipe status: `recipe-not-run`

Every recipe in the initial edition is an original, proposed project brief. It has not been executed end to end in dot as part of preparing this collection. Prompts, screenshots, integrations, exports and schedules must not be described as working demonstrations without actual run evidence.

The repository's automated checks validate content structure, metadata, generated files and local links. They do not validate the outcome of the projects themselves.

## Distinguish four kinds of evidence

| Evidence | What it establishes | What it does not establish |
| --- | --- | --- |
| A valid Markdown recipe | Required metadata and sections are present | The prompt will work in every account |
| A passing repository check | The checked repository invariants hold | The projects were executed |
| A recorded project run | A specific result under stated conditions | General product capability or repeatability |
| A reproducible run with artifacts | Others can inspect a result and attempt the checks | Safety or fitness for high-stakes use |

## How to document an actual run

Use the [run-log template](../templates/RUN-LOG.md). Record the recipe ID, date, relevant tool/access availability, sanitized inputs, actual outputs, exact checks performed, failures and remaining limitations. Link only artifacts you can share. Do not include internal assistant instructions, personal account data or credentials.

Attach the evidence in a contribution and ask maintainers to review it. Do not change the recipe status merely because text was generated, a file exists, or a single happy-path check passed. A future status vocabulary should be added through an explicit content-contract and editorial change.

## Timeboxes and difficulty

Timeboxes are suggested first-session planning budgets, not promises about speed or completion. Difficulty reflects the amount of setup, iteration and verification a reader should expect, not the intelligence of the reader or a guaranteed limitation of dot.

## Source and product claims

These recipes do not depend on claims about current pricing, account entitlements or undocumented product controls. When a project needs live facts, its prompt asks dot to retrieve and date them during the run. Consult the available product interface and official documentation for current capability details.
