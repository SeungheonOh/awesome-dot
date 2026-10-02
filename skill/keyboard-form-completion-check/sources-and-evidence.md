# Sources and evidence limits

Primary references checked on 2026-10-02. The guidance below is paraphrased; the fictional journey and code are original. WAI tutorials and WCAG Understanding pages explain practices and criteria, but do not certify this example.

## References that affect this workflow

- [W3C: Understanding Keyboard, 2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html): test whether the functionality can be achieved through a keyboard interface. An alternative usable keyboard route can matter; a skipped pointer control alone is not enough to establish a failure
- [W3C: Understanding Focus Order, 2.4.3](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html): sequential navigation should preserve meaning and operation. There can be more than one meaningful order; do not equate “matches every visual position” with the entire criterion
- [W3C: Understanding Focus Visible, 2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html): observe an actual visible focus indication during keyboard operation. A CSS selector's presence is only source evidence
- [W3C: Understanding Focus Not Obscured (Minimum), 2.4.11](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html): the minimum criterion concerns a focused component being entirely hidden by authored content. Fully unobscured focus is a stronger goal; do not misstate the minimum threshold
- [WAI: Labeling Controls](https://www.w3.org/WAI/tutorials/forms/labels/): use meaningful labels associated with controls. For an explicit HTML label, its `for` value matches the control's ID
- [WAI: User Notification](https://www.w3.org/WAI/tutorials/forms/notifications/): give understandable success/error feedback; an error summary can identify fields, explain corrections and link to the relevant controls. A summary is a useful pattern, not the only possible compliant implementation
- [MDN: aria-describedby](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-describedby): associate supplementary descriptions through referenced element IDs. Descriptions supplement a name; they do not implement interaction or prove what a screen reader will announce
- [MDN: button](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button): use the native button's form behavior deliberately, including its type. Keep one submission path so the repair does not duplicate processing

## What each evidence type establishes

| Evidence | Supports | Does not establish |
| --- | --- | --- |
| Source review or HTML parser | Declared labels, ID references, event handlers, selected structural relationships | Computed accessible name, actual keyboard navigation or visible focus |
| Pure JavaScript rule tests | The supplied inputs receive the specified validation/result values | Browser event dispatch, DOM updates, focus or announcements |
| Browser accessibility information | Exposed name, role, state and description in that browser | What a specific screen reader speaks or whether a person can finish the task |
| Recorded keyboard journey | The observed actions, focus and result in the named environment/revision | Every browser, every input device, unvisited paths or whole-site conformance |
| Screenshot or recording | Visible result and focus appearance where captured | Hidden state, stored data or audible announcements |
| Actual assistive-technology run | Behavior observed with the named version, configuration and browser | Universal screen-reader usability or certification |

## Bundled fixture verification

On 2026-10-02, the portable check was run with Python 3.12.14 and Node v24.19.0. [example-checks.json](example-checks.json) contains the exact page/script hashes and results. The check passed selected label/ID/resource relationships, expected native-control markup, JavaScript controller syntax and pure-rule cases for valid input, malformed codes, quantity boundaries, invalid shelf, trimming and result text. The skill frontmatter/name validator also passed.

The original source has a click-only Create control, a form handler that prevents default submission without creating a draft, a non-label Workshop code paragraph, unassociated global errors and suppressed control outlines. The corrected source contains the changes described in [journey.md](journey.md). The shared rules have the same identity for both pages.

No browser was operated during creation of this packet. K0–K4 are **unrun**. Browser-computed names/descriptions, actual focus order, focus visibility/obscuration, rendered layout and screen-reader announcements are **unverified**. The file named after.html is the supplied corrected implementation, not a claim that every user-facing check passed. Use the journey to test it and append the actual environment, file hashes and observations before describing a verified keyboard repair.

An independent source review reran the inspected offline checker and reproduced example-checks.json exactly. It confirmed the written source relationships, validation/control logic and reference scope; no browser, local server or assistive technology was operated during that review. The keyboard exercise remains unrun.
