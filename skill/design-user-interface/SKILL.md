---
name: design-user-interface
description: Design or revise a human-facing interface before implementation, delivering an editable task flow and screen/state specification with requested wireframes. Use when navigation, controls, and interaction behavior need deciding; artwork, diagrams of already decided flows, implementation, and live functional QA have separate workflows.
---

# Design a User Interface

Produce a reviewable interaction design that someone can revise and implement: connected screens, concrete content and controls, and rules for what happens when a person acts. Save the actual editable specification and any requested drawings. A collection of attractive screens or advice about interface principles does not settle the interaction.

Use this workflow for a design deliverable, not as a compulsory phase of every build. Keep requirements with `define-project-brief`, programmatic interfaces with `design-api-contract`, established-flow diagrams with `visualize-information`, and isolated artwork with `create-visual-asset`. Implementation and functional QA remain with `build-usable-website`, `implement-scoped-change`, and `test-user-journey` as appropriate.

## Establish the task and design boundary

Read the request and relevant supplied product material. Identify the person's goal, starting information, entry point, and observable completion. Preserve the chosen platform, accepted scope, terminology, content, and existing product patterns. A phone interface should not silently become a website, and a local redesign should not reorganize the whole product.

Separate requirements and accepted decisions from observed conventions and new proposals. A reference screen can establish layout without establishing a business rule. Reuse supplied facts accurately; label invented sample content and proposed wording. Use representative values that expose the decisions the interface must support rather than filling every view with interchangeable placeholders.

Resolve missing information only when it changes the design materially. Make ordinary reversible choices when design judgment is delegated. For a consequential choice, state the proposal and its effect beside the affected flow, or ask for the decision if work depends on it. Keep independent parts moving. Do not invent account requirements, permissions, policies, retention, or service capabilities to make a path appear complete.

Choose fidelity and an available authoring format from the requested result and expected edits. A small flow may need readable screen descriptions and a transition table; requested wireframes need actual drawings. Honor a specified native format. There is no default requirement for personas, a research workshop, a design system, a screen count, or a clickable prototype.

## Decide the flow and visible choices

Trace the useful task from its entry point to completion. Group information and actions around what the person needs to understand or decide at each moment. Show meaningful branches, where the person can leave, and how they return or recover. Add a screen, panel, or overlay because it resolves a task need; do not turn each state into a separate screen automatically.

Give screens and material states consistent names or identifiers so the flow, drawings, and behavior rules refer to the same things. For each relevant view, specify:

- Its purpose, the condition that opens it, and the content hierarchy
- Concrete labels and representative content, including units, required input, defaults, and validation rules when they matter
- Available actions, what each affects, and any condition that changes availability or needs explaining
- The resulting view or state, and what information lets the person recognize the outcome

Keep decisions legible in the interface itself. Use action labels that distinguish viewing, editing, saving, submitting, and discarding where their effects differ. State what a bulk action affects before it is taken. Prefer the product's familiar controls and navigation unless the task gives a reason to change them; explain a material departure briefly.

Match layout and input behavior to the specified platform. Account for the relevant viewport or window sizes, lengthy content, and keyboard or touch operation. Specify reading order, visible focus, meaningful control names, and an alternative to a gesture when those affect completing this flow. Distinguish selection from focus and define important focus destinations after an overlay, error, or removed item. For web widgets, [WAI's keyboard-interface guidance](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) supports that distinction and predictable focus movement; it is not a substitute for the chosen platform's conventions or runtime testing.

## Make state and recovery explicit

Connect visible actions to precise state changes. For each consequential transition, record the starting condition, action, immediate feedback, eventual result, and what is retained or discarded. Put shared rules in one place and reference them from the affected screens. Do not rely on arrows or button labels alone to explain behavior.

Include only states that can occur in the task. Where relevant, settle:

- **Data and drafts:** what is currently displayed, what is being edited, and what is confirmed saved; what survives Back, Close, a changed selection, or interruption; when a discard warning is warranted
- **Waiting and outcomes:** how pending work differs from an empty result, failure, partial result, or confirmed completion; which actions remain available while waiting
- **Recovery:** what the person can correct or retry, what work is preserved, and where they land afterward; whether a repeated action could repeat an effect
- **Uncertainty:** what the interface can truthfully say when an operation may have happened but confirmation is missing, and what supported next step can resolve it

Write the important messages, not just an instruction to “show an error.” Identify the affected input or operation and a useful next step. For web forms, [WAI's notification guidance](https://www.w3.org/WAI/tutorials/forms/notifications/) supports associating errors with the relevant control and explaining correction. Do not imply that every error needs a modal or that color alone explains its meaning.

Tie each success, cancellation, retry, or recovery promise to a supplied capability or an explicitly proposed dependency. Stopping a wait does not necessarily undo an operation; a local draft does not establish durable storage. When the service contract is missing, label the affected branch and required capability rather than designing fictional certainty. Keep backend mechanisms and API definitions with their own owners.

## Save the editable specification

Author the flow and state rules as readable editable text or native structures. Where drawings are requested, preserve meaningful editable objects such as text, controls, frames, and connectors. A flattened image placed in an editable container does not satisfy object-level editing. Use an appropriate available format and include dependencies needed to reopen it; do not promise a proprietary format or conversion the tools cannot produce.

Keep the drawing, written rules, and any export on the same revision. Show exact operative labels in the drawings where practical, with nearby references for rules too detailed to fit. Keep unresolved proposals visible where they affect the design. A separate polished export may aid review, but it does not replace the editable source.

Use supported authoring and rendering routes. If access to a file, browser, or preview target is denied, do not work around the denial through another route. Complete permitted checks and identify the specific missing artifact or inspection. Creating this specification does not authorize hosting, publication, live submissions, or changes to the application.

## Check the design and hand it over

Walk an ordinary path and the material boundary or interruption from the request using concrete content. At each step, check whether a person can determine what to do next and whether an implementer can determine the intended result without supplying a missing rule. Trace retained values, selection, navigation, and completion evidence across views. Repair contradictions and dead ends rather than changing the requirements to fit the drawings.

Check the saved artifacts separately:

- **Editability:** reopen or inspect the source structure and confirm that the required content and drawing objects remain editable. When available, try a representative edit in a copy. State whether an actual editor was exercised or only source structure was checked
- **Readability:** render or open the saved drawings and requested exports at their intended reading size. Inspect labels, clipping, overlap, connectors, and important state differences. Source inspection alone cannot establish that a drawing is readable
- **Consistency:** compare screen identifiers, labels, conditions, sample values, action results, and unresolved decisions across the specification and drawings. Recheck affected artifacts after a revision

These checks establish a coherent design artifact, not working interactions, accessibility conformance, persistence, service delivery, or usability findings from participants. Report any unavailable check specifically. Do not describe a static walkthrough as an executed user journey.

Deliver the editable specification, requested drawings and exports, concise rationale for material choices, and remaining decisions or dependencies. Identify what was checked and any limitation that changes how the design should be used. If implementation was also requested, continue within that scope once the necessary decisions are settled; the design artifact does not create an extra approval gate.
