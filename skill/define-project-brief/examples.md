# Briefs that change the next action

These are fictional illustrations of the method, not records of completed projects.

## A request with two different outcomes

Request: “Make it easier to find unfinished orders in the existing workspace.”

Available context: staff currently search by customer name; the table already shows an order's fulfillment state. A note suggests both a saved view and a new notification system. The request does not mention notifications.

A useful first question is whether “unfinished” means not dispatched or not paid. Those interpretations select different records. Choosing a framework or asking for a launch date would not resolve this ambiguity.

If the user answers “not dispatched,” a brief can say:

- Purpose: let fulfillment staff find orders still waiting for dispatch in the current workspace
- Scope: add a visible way to filter the existing order list by the existing dispatch state; keep customer search and record-opening behavior
- Acceptance: an undispatched order is included; a dispatched order is excluded; an empty result is distinguishable from a loading or access failure; combining the filter with a customer search retains both conditions
- Dependency: inspect the actual state values and existing table behavior before deciding how the filter is implemented
- Outside this request: the notification idea remains a separate proposal

Do not define “late,” add a payment filter, or promise a new notification without evidence that those belong to the requested outcome. If the user also asked for implementation, the next step is to inspect the existing code and implement the agreed behavior, not to stop at the brief.

## Editorial criteria without a fake score

Request: “Turn these technical notes into an introduction for new volunteers. Keep it to one page and explain how they can get help.”

The notes include equipment names, a troubleshooting history, and a supplied help address. The brief should make the reader's first use the test:

- A newcomer can tell what the service does, what they need before starting, and where to get help
- Essential unfamiliar terms are explained where first used
- The help address and the stated availability restriction remain exact
- The introduction fits the requested page format; detailed troubleshooting history moves only if the user requested an additional reference, otherwise it is omitted from this introduction

No readability percentage or invented volunteer feedback is needed. If a one-page limit conflicts with required content, explain the concrete tradeoff and ask which constraint can change; do not remove a consequential qualification to make the page fit.

## A clear task should move directly

Request: “In this draft, replace the outdated support address with the supplied new address, keep all other text unchanged, and save a copy.”

The outcome and boundary are already clear. Read the draft, locate the exact occurrences, make the requested replacement in a copy, and verify that the address changes are the only content edits. Do not create a project brief, ask for an audience, or propose a broader rewrite.
