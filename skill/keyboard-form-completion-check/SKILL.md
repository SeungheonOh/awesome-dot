---
name: keyboard-form-completion-check
description: "Check whether a specific web-form task can be completed by keyboard, including labels, instructions, validation recovery and focus. Repair and retest the bounded journey when code changes are authorized."
---

# Complete a Web Form by Keyboard

Establish whether a person can reach the intended outcome using the keyboard: find the fields, understand what to enter, correct a mistake, activate the action and recognize completion. Produce evidence from that journey and, when requested, a working scoped repair. A list of HTML attributes alone is not a completed check.

## Establish the task boundary

Read the supplied material and identify:

- Exact page or local preview, code revision if available, and browser/OS to check
- Entry point, intended outcome, required values and the rule defining a valid result
- A disposable record or fictional values, reset method, and any autosave or submission effects
- Whether the request is to inspect, fix, or both; files and environment within the repair scope

Use existing tools and the requested environment. Do not install an audit package just to run this journey. Do not substitute a mock page for the actual product and call it verified. If execution is unavailable, inspect the available source and return a runnable procedure with browser results explicitly unrun.

Treat typing into a live form as possible transmission. Use the already authorized test destination and data. Stop before a new recipient, real booking, payment, attestation or other unapproved effect; complete the safe portion and identify that boundary. A request to repair this form already authorizes ordinary in-scope edits and retesting. Do not request the same permission again.

## Define the journey before changing it

Write a compact contract: initial state → action and field values → invalid-state recovery → valid outcome. Include how success is distinguished from a spinner, a button click or an unchanged old confirmation. Choose the smallest relevant set:

1. A valid completion from a clean reset
2. One realistic invalid submission, correction and completion without re-entering unrelated valid answers
3. A neighboring state affected by the proposed repair, such as a newly revealed field, Back, repeated submission or reset

Do not add every possible field combination. Follow a supported keyboard convention for each control; select menus and radio groups need their native arrow-key behavior, not one Tab per option. Record browser settings that change keyboard navigation rather than silently changing a user's preferences.

For the bundled offline journey, read [journey.md](journey.md). It contains the independent contract, reset and exact cases for the original and corrected pages.

## Run and record the actual path

Enter the page using the browser's normal navigation, then operate the form with Tab, Shift+Tab, typing and appropriate activation keys. Observe focus after each meaningful transition. Do not replace a failed keyboard step with a pointer click, a script click, direct value assignment or programmatic focus and count it as success. Those methods can support a separately labeled diagnosis.

Record control or region reached, key/action, visible result, focus target, expected result and evidence locator. Check that focus remains visible and is not covered by page content, including after an error or newly revealed section. Traverse backward at a meaningful point; verify a user can leave a control without getting trapped. Stop the failing case when the necessary action cannot be reached after a forward and reverse pass, or when a trap prevents progress. Report the last usable state instead of repeatedly cycling through the page.

Inspect visible labels and instructions alongside the browser's accessibility information when available. Distinguish a visible label, an associated source label and the browser's computed accessible name/description. A placeholder is not a durable instruction. Required status, format and units must be understandable before an avoidable error. Use [sources-and-evidence.md](sources-and-evidence.md) when naming a standard or deciding how much a source or tool observation proves.

On validation failure, check the recovery route: an understandable error identifies the field and correction; the relevant error is associated with its control; valid answers remain; focus moves to a useful error summary or invalid field, or an equally discoverable supported pattern works. If there is a summary link, activate it with the keyboard and verify the actual destination. Correct the value, submit again and check that stale error state clears.

For success, inspect the actual receipt, saved record or local result required by the contract. A status-region attribute does not prove an announcement was heard. Name the screen reader and version only if that combination was actually used; report what it announced. Without it, mark announcement behavior untested.

## Repair within the authorized scope

If asked only to check, return the observed blocker and a precise proposed repair. If asked to fix, preserve a recoverable baseline and change the responsible code now:

- Prefer the appropriate native input, button or link over a styled generic element. Adding a role or `tabindex` alone does not implement keyboard activation
- Associate persistent labels and useful hints with stable control IDs. Keep required rules and business validation intact
- Give errors text, field associations and a deliberate recovery destination; remove stale errors when their state is resolved
- Preserve natural focus order where it makes sense. Avoid positive `tabindex` values or broad key interception to conceal an order problem
- Ensure the repaired action has one intended handler path, so keyboard activation does not introduce duplicate processing

Adapt to the product's existing components and validation pattern. Do not redesign the whole form, add a framework, suppress errors or relax a requirement to get a passing path. If the cause lies outside the authorized files, explain the needed change and continue any independent in-scope work.

Run relevant existing checks and replay the formerly blocked journey on the changed revision from the stated reset. Then run the affected neighboring case. Verify the same values, recovery, focus and result, not merely that the new button exists. A source change with unrun browser tests is a patch awaiting that check, not a verified fix.

## Deliver and stop

Save a short journey report with the target/revision, environment, contract, reset, exact actions, observed results, evidence and remaining gaps. Include the concrete patch or changed-file links when repairs were requested, plus the retest result. Preserve a before/after screenshot or brief recording for a focus or layout claim when the available tool can capture it; source snippets support different claims.

Use one outcome: **completed under the tested conditions**, **blocked at the named step**, or **not executed**. State each case's result separately if coverage differs. Stop when the requested journey and affected recovery path are checked, or a specific missing access, decision or external effect blocks progress. Report only the supported scope: this is neither a whole-site audit nor a WCAG certification.

## Bundled example

The fictional workshop-kit planner includes [before.html](before.html), [after.html](after.html), shared [draft-rules.js](draft-rules.js) and a [portable check](check_example.py). Open either HTML page with its adjacent script available; it processes only a local draft and has no recipient or submission endpoint. [journey.md](journey.md) gives the keyboard exercise; [sources-and-evidence.md](sources-and-evidence.md) states what was actually checked.

Example request:

> Check the workshop-kit form from entry through correcting an invalid code and creating a local draft, using only the keyboard. Fix the provided page if the journey is blocked. Preserve the validation rules and entered answers, then replay the same journey. Report the exact outcome and any browser or assistive-technology checks you could not run.
