---
name: principle-experience-first
description: "Resolve feature and design tradeoffs around the consumer’s successful workflow, including accessibility, feedback, failure recovery, and maintainability."
---

# Experience first

Use this when implementation convenience or feature breadth competes with the quality of the delivered experience. Name the consumer: an end user, an API caller, an operator, or the next maintainer. Their success provides the target; foundations and implementation sequence serve it.

## Make quality observable

Describe the central task in the consumer's terms and identify where friction can prevent completion. Specify the relevant acceptance conditions before choosing scope:

- Entry, successful completion, and understandable feedback
- Loading, empty, invalid, error, and interrupted states where the workflow can encounter them
- Keyboard and assistive-technology access for interactive surfaces
- Cancellation, retry, and recovery without duplicate effects or lost work
- Predictable contracts and actionable errors for APIs and command-line tools

Prioritize the core loop. An extra option must solve an observed need, not merely be easy to expose. Where scope is negotiable, propose fewer complete capabilities over a wider unfinished surface. Explicitly requested features and contractual requirements remain obligations; do not silently remove them in the name of polish.

Prototype when uncertainty is about interaction or feel, and inspect the actual experience when tools permit. Check transitions, spacing, focus, alignment, and error wording after the main behavior works. For a library, equivalent care goes into naming, defaults, documentation, and debugging affordances. Include maintenance costs that will affect future reliability.

## Example and counterexample

Applies: an upload flow needs a cancel/retry path before another optional filter. Verify that cancel releases resources, retry does not create two records, and focus reaches the error explanation.

Does not apply: a user requests a narrow data-export fix under a deadline. Do not turn it into a visual redesign or omit required export fields. Improve the relevant error message if in scope, and propose unrelated changes separately.

## Evidence

Report the representative task exercised, the states inspected, and what remains unverified. A rendered mockup establishes appearance, not working interactions; passing API tests does not establish keyboard usability. If a product tradeoff would change the agreed scope, present the impact and obtain the decision rather than substituting personal taste for acceptance criteria.
