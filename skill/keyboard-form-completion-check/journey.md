# Workshop-kit draft: contract and keyboard exercise

Everything in this example is fictional. The files are original teaching fixtures. Both pages use the same [business rules](draft-rules.js); the change concerns interaction, instructions and feedback. Opening a page and creating a draft sends nothing, reserves nothing and writes no persistent record. Keep the HTML and JavaScript files together. Use an available browser's local-file support or an existing authorized preview; no installation is needed.

## Independent acceptance contract

The user wants a draft for **LANTERN-42, 2 kits, West shelf**.

- Workshop code is required: uppercase `LANTERN-` followed by exactly two digits; surrounding whitespace is ignored
- Number of kits is required: a single digit from 1 through 4; surrounding whitespace is ignored
- Pickup shelf is required: North shelf or West shelf
- An invalid attempt produces no ready draft and preserves all answers. The user can find the error, return to its field, correct it and complete the same draft using the keyboard
- A valid attempt produces one current local result: `Local draft ready: LANTERN-42; 2 kits; West shelf. Nothing has been sent or reserved.`
- Editing after success makes clear that the ready result is no longer current. Repeating Create replaces the single result rather than accumulating drafts
- Start over clears code, restores 2 kits, selects Choose a shelf and clears errors/result. In the corrected page it returns focus to Workshop code

The focus contract for the corrected fixture is code → kits → shelf → Create local draft → Start over when moving forward. An invalid attempt moves focus to the error summary; Tab reaches its first link, and activating a link focuses the corresponding field. A successful attempt keeps focus at the control that triggered it and updates a status region. Screen-reader announcement quality requires a separate actual test.

## Before and after

[before.html](before.html) contains a click-only styled `div` for Create local draft. It has no keyboard handler, and its form submit handler only cancels default submission. The workshop text is a paragraph rather than a label; failures appear in a plain paragraph without field associations or a recovery focus destination; custom CSS removes control outlines. These are source observations. Whether and how they appear in a given browser must be recorded from that browser.

[after.html](after.html) uses a native submit button and one submit handler. It adds a persistent workshop label, associated instructions, required semantics, per-field errors, a linked summary and a visible focus style. The summary has `tabindex="-1"` for deliberate error focus, not an extra stop during a normal pass. The result has status semantics. None of these attributes alone establishes assistive-technology usability.

## Run record

For each case record page filename and SHA-256, browser/version, OS, viewport/zoom, keyboard-navigation settings, starting focus, keys, actual focus/result, screenshot or other locator, and pass/blocked/unrun. Record an assistive-technology name/version only if used. Do not populate actual results from the expected results below.

Use ordinary browser navigation to open the page. Establish focus inside the document using the browser's normal keyboard route. Browser chrome can add stops outside the page; record them separately. Use native select-menu keys for that browser and verify the displayed choice. Do not use scripted `.focus()`, `.click()` or DOM value writes as substitutes for the user's path.

### K0: establish the original blocker

1. Open before.html afresh. Activate Start over with the keyboard to establish defaults, then use Shift+Tab back through shelf and kits to code
2. Enter `LANTERN-42`, retain `2`, choose `West shelf`
3. Continue forward looking for Create local draft. Make one reverse pass if necessary. Try Enter from the code field to check whether a normal equivalent completion path exists
4. Record whether a local result appears and whether the Create action can be reached. Stop this case once the necessary action is unavailable through these routes; do not click it and call the keyboard journey complete

Source-based prediction: Create is skipped and Enter does not create a result. A pointer-triggered look at the original error paragraph can be useful diagnosis, but is a separate observation outside K0.

### K1: complete a valid corrected draft

1. Open after.html. Reach Start over by keyboard and activate it; verify focus on Workshop code and the three reset values
2. Enter `LANTERN-42`; Tab to kits and retain `2`; Tab to shelf and select `West shelf`
3. Tab to Create local draft, check the focus indicator and activate with Enter
4. Read the exact result required by the contract; verify focus remains on Create. Shift+Tab to shelf and Tab forward again; focus should follow the form's meaningful order

Expected: one correct local result, no visible error summary or stale invalid flags. A screenshot supports visible state only; inspect browser accessibility information separately for name/description claims.

### K2: recover from a wrong code without losing other answers

1. Start over. Enter `LANTERN`, keep `2`, select `West shelf`, then activate Create with Space
2. Verify the error summary receives focus and identifies Workshop code and the required format. Verify kits and shelf retain their values
3. Tab to the summary's Workshop code link and press Enter. Verify focus actually reaches the code field and its hint and error remain associated with it
4. Select the existing value using the platform's normal shortcut and replace it with `LANTERN-42`. Move to Create using Tab and activate
5. Verify the expected ready result, removal of the summary and code error, and removal of the stale invalid state. The fixture revalidates on Create; it does not claim to clear errors on each keystroke

Expected: correction and completion entirely by keyboard, with no loss of the two valid answers. Record computed accessibility information if available; do not infer spoken announcements from that information.

### K3: check error destinations and reset after failure

1. Start over; leave code empty, replace kits with `0`, leave shelf unselected, then activate Create
2. Verify three errors in field order. From the summary, Tab to each error link and activate it in turn, re-triggering the same invalid state as needed to return to the summary
3. Verify each link focuses its own field, not a duplicate ID or the page top. Verify both forward and reverse navigation remain possible
4. Reach Start over by keyboard and activate it. Verify cleared summary and inline errors, no stale invalid states, default values and code focus

Expected: a useful route to all three fields, plus a clean reset. This checks the common error renderer used by the repair, not a new product flow.

### K4: repeated activation and stale result

1. Complete K1, then activate Create again using Space. Verify there is still one current result
2. Shift+Tab to shelf, change it to North shelf and check that the former ready message becomes a draft-changed message
3. Tab to Create and activate. Verify the current result now names North shelf and the same code/quantity; Start over and check the reset contract

Expected: no accumulation of drafts and no old ready message presented as current after editing.

## Bounded source and logic check

With Python 3 and Node already available, run from this folder:

```sh
python3 check_example.py
```

The script checks local resource/ID relationships, selected markup invariants, JavaScript syntax and the shared pure validation/result rules. It does not launch a browser, press keys, calculate an accessibility tree, inspect focus visibility, hear a status announcement or test screen-reader compatibility. The actual execution record is in [sources-and-evidence.md](sources-and-evidence.md).
