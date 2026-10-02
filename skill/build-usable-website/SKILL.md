---
name: build-usable-website
description: Create a new useful website or small web tool with real content, working interactions, editable source, and an honestly verified preview when available. Use for new site creation; use a scoped implementation workflow for changes to an existing application and a user-journey workflow for QA alone.
---

# Build a Usable Website

Deliver the requested website or small web tool so its intended audience can accomplish the main task. The result includes the source, required content and controls, meaningful checks, and enough instructions to run or edit it. A plan, visual mockup, or successful build alone does not establish that the website works.

Use this workflow for a new site or self-contained tool. For a behavior change in an existing application, use `implement-scoped-change`; for an assessment of an existing experience without building it, use `test-user-journey`. A new site still needs focused verification, without automatically expanding the assignment into a full QA engagement.

## Make the useful outcome concrete

Identify who will use the site, the task they should complete, and the content or inputs they need. Translate the request into a small set of observable results: what the visitor sees, what they can do, and what happens afterward. For a clear small request, infer ordinary reversible design choices and start building. Do not require a discovery workshop, elaborate specification, or approval of decisions the user already made.

Inspect supplied content, references, and assets. Distinguish a visual reference from a source of facts. Use the user's actual information where provided; do not invent testimonials, prices, contact details, performance claims, business policies, or live data to fill the layout. If essential content is missing, ask for the specific missing input and continue work that does not depend on it. Clearly identified draft content can support a draft, but it cannot satisfy a requirement for the finished facts.

Resolve choices that change the product contract before implementing their dependent parts:

- **Static information:** Pages and navigation may be sufficient. Do not add forms, accounts, a database, or analytics simply because such sites often have them.
- **Local computation or state:** A calculator or planner may run entirely in the browser. Decide whether state lasts only for the current session, is stored on that device, or can be exported. Label the actual behavior where a visitor could otherwise mistake it for durable or shared storage.
- **Persistent or shared state:** Establish where data lives, who can read or change it, and what existing access and services are available. Browser storage is not a substitute for a requested shared backend.
- **External actions:** A form submission, purchase, booking, message, authentication flow, or live lookup needs a real supported destination and appropriate authorization. Establish those dependencies; a success toast or fabricated response does not implement the action.

If an essential integration is unavailable, finish independently useful work and report the exact incomplete behavior. An explicitly requested prototype may use clearly labeled sample data or simulated flows. Never pass those off as production data, saved records, signed-in sessions, or completed submissions.

## Choose the available implementation path

Honor the user's requested environment, platform, stack, and destination. Inspect the available tools, access, project instructions, existing files, and relevant conventions before choosing an approach. Preserve unrelated work. Use the smallest suitable implementation that fulfills the behavior; a static page need not become a framework application, while a shared workflow may need a backend.

Use existing project patterns and permitted dependencies where they fit. Verify uncertain, version-sensitive framework, hosting, or service details using the tools and current primary documentation available during the actual task. Do not assume a particular CLI, database, hosting account, credential, preview mechanism, or product feature exists. Keep secrets out of client source and exported artifacts.

Treat preview and publication as separate steps. Use a supported preview path within the available environment. If a browser, file path, network destination, or localhost route is denied, respect that boundary; do not switch ports, protocols, tunnels, or tools to reach the same denied target. Use other permitted checks for the claims they support, and report which UI behavior remains untested. A tool's absence may justify another supported method; an access denial does not authorize a workaround.

## Build content and behavior together

Create the actual source and wire the main task through its visible entry point, event handling, state, and output. Put the important content and action where the audience can find them. Choose a consistent visual hierarchy, readable typography, spacing, and assets that support the task. Follow supplied brand or reference constraints without copying irrelevant sections into the product. Use imagery when it adds value; it is not a prerequisite for every useful tool.

Treat each visible control as a promise. A link should reach its intended destination, an action should perform its stated operation, and a form should validate and reach its real handler. Remove unnecessary decorative controls. If a required control depends on missing access or configuration, make its unavailable state clear and retain it as unfinished work rather than creating apparent success.

Handle the states that can occur in the requested flow:

- Distinguish an empty collection, loading data, no matching results, and a failed request where these are real possibilities
- Explain invalid inputs near the relevant field and preserve useful work when an operation fails
- Prevent accidental repeated actions while a consequential request is pending; show success only after the responsible system confirms it
- Make storage lifetime, resets, exports, and sharing behavior match the chosen contract

Use semantic controls and labels, keyboard access, visible focus, and legible contrast. Adapt layout and navigation for narrow and wide viewports. Keep lengthy text, larger values, and error messages from breaking the main task. Avoid adding motion or visual complexity that obscures required content or controls.

## Verify the result visitors will use

Run relevant project checks and inspect the actual page through a permitted browser or preview when available. Derive commands from the implementation and its configuration; do not invent a passing check or run a script that publishes or changes live data under the assumption that it is merely a test.

Exercise the main task from its visible starting point to the observable result. Include the boundary most likely to expose a misleading implementation, such as invalid input, an empty result, a reload after saving, a failed integration, or a repeated action. Choose checks for the actual contract rather than requiring every possible case. Verify responsive behavior and keyboard use in the important flow. Inspect both the displayed output and the underlying effect when the task involves storage or an external service.

Use permitted test data and supported test modes for consequential flows. If verifying a real transaction, message, or shared-data mutation would exceed current authorization, stop before that step and report it as unverified. Do not quietly send a test submission to a live recipient.

Fix problems that prevent the requested task, then recheck the affected behavior on the final source. A successful compile establishes compilation; it does not establish rendering, navigation, persistence, or service delivery. State which checks passed, failed, were blocked, or were not run. A screenshot establishes appearance at that moment, not the behavior of controls.

Stop when the requested behavior and justified available checks are complete, or a concrete blocker prevents further progress. Do not impose a subjective perfection score, endless visual revisions, or unrelated infrastructure work as completion criteria.

## Deliver source and a usable handoff

Lead with what the site now lets its audience do. Provide the source location or artifact and a verified preview link when one is available. Distinguish a temporary preview from a durable published site; do not promise availability the environment does not provide.

Give concise instructions for running the project, editing the main content, and configuring any required service. Use commands and file locations that exist in the delivered source. Include only setup the recipient actually needs, plus material storage or access limitations. Identify unfinished required behavior and the smallest missing input or action without presenting a partial implementation as complete.

Publish only when the user requested it and the destination and action are authorized. Follow the chosen provider's supported workflow, then verify the resulting URL and main behavior. Report publication separately from local implementation or preview, and describe only the state actually confirmed.
