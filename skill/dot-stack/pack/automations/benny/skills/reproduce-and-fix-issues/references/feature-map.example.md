# User-path feature map

Copy to user-owned `.dot-stack/benny/feature-map.md`. These fictional examples are design aids, not verified selectors or a configured control adapter. Fill each real feature the runner may touch; exclude unconfigured features from scope.

## Per-feature contract

Record purpose; user entry path and alternate entries; actual adapter calls/selectors; relevant states; account/permissions/fixtures/flags/services; correct and broken discriminating states; reset; screenshot/recording/read-only cross-check; known wrong surfaces; and justified environment translations. Mark irrelevant states explicitly. Keep runtime code-path discoveries out of durable user-path instructions.

## Fictional: item list and detail

- Purpose: find a saved item and open its detail
- User path: choose Items, then the fixture row; alternate path is a supported search result
- Selectors: tab Items, list Items, row with unique fixture name, detail heading
- States: loading, empty, service error, selected row, open/closed detail, keyboard focus
- Preconditions: disposable read-authorized account with uniquely named fixture items
- Correct state: selected row and detail identify the same item; Back returns to the prior list/filter
- Reset: close detail, restore starting filter/selection through supported controls
- Evidence: record entry → selection → detail → Back; screenshot detail identity; read the selected item ID without changing it
- Gotcha: similarly named search results are a separate entry path; test both only when in scope

## Fictional: item editor

- Purpose: create or modify a disposable item and verify persistence
- User path: New item from the list, or Edit from a detail view
- Selectors: buttons New item/Edit/Save/Cancel, form Item editor, label-linked title field
- States: clean/dirty, focused, invalid, saving/disabled, save error, success, cancellation
- Preconditions: editable test fixture; known service response; no real customer records
- Correct state: Save persists the change and reopening shows it; Cancel preserves the prior value
- Reset: use the app's documented test reset or authorized fixture restoration
- Evidence: record edit and reopen; screenshot saved value; compare the same stored value read-only
- Gotcha: setting storage directly is not proof that the editor saved correctly

## Fictional: preferences

- Purpose: change a test-only display preference
- User path: Profile menu → Preferences → display option
- Selectors: Profile button, Preferences menu item, named preference control
- States: closed/open, focused, selected/unselected, loading, failure, disabled
- Preconditions: existing authorized disposable session; known starting preference
- Correct state: choice survives reopen/reload as specified; cancellation leaves original value
- Reset: restore the starting preference through the same supported UI
- Evidence: record path and reopen; screenshot final control; read preference value
- Gotcha: operating-system settings are a different surface; security/privacy choices are outside this example

## Authentication precondition

Use an existing approved test session or the host's approved secure login flow. If the defect requires a particular authentication state, describe that state and the authorized setup method. Do not write credentials in this map, script password entry from chat, or infer permission to register accounts. Missing required account state may block reproduction.

## Completeness check

Every enabled feature names reachable entries, actual interface methods, stable selectors, relevant states, reset, acceptance condition, capture plan, and read-only cross-check. Test interrupt/cancel/repeat behavior where relevant. Verify these against the real app before enabling the runner; a completed-looking worksheet is not execution evidence.
