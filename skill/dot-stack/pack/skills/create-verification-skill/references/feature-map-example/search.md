# Search notes

Illustrative contract: users search titles and bodies, open a matching note, distinguish no matches from a failed search, and clear the query. The app assumptions and driver limits are in the [index](README.md).

## Sub-features

- `search-open`: toolbar and keyboard entries reach the search dialog
- `search-title` and `search-body`: matching works for the documented fields
- `search-result`: opening a result reaches the corresponding note
- `search-empty`: completed successful search with no matches is distinguishable from loading and failure
- `search-clear`: clearing restores the documented default view
- `search-cli`: an implemented CLI returns the same matching identities

## How to get to it

The sample browser has a `Search` button and `/` shortcut outside editable fields. Include a CLI entry only after inspecting one in the project. Treat archived-content options and permission filters as separate states when supported.

## Driving it with Playwright

Preconditions: the shared baseline, expected build and data directory, and no existing search dialog. This excerpt uses the existing runner's `page` and `expect`:

```ts
await page.getByRole('button', { name: 'Search', exact: true }).click();
const dialog = page.getByRole('dialog', { name: 'Search notes' });
const query = dialog.getByRole('searchbox', { name: 'Search notes' });
await expect(query).toBeFocused();
await query.fill('quarterly');
const results = dialog.getByRole('list', { name: 'Search results' });
await expect(results.getByRole('link', { name: 'Quarterly plan' })).toBeVisible();
await expect(results.getByRole('link', { name: 'Grocery list' })).toHaveCount(0);
await query.fill('budget');
await expect(results.getByRole('link', { name: 'Quarterly plan' })).toBeVisible();
await query.fill('volcano');
await expect(dialog.getByRole('status')).toHaveText('No matching notes');
await dialog.getByRole('button', { name: 'Clear search' }).click();
await expect(query).toHaveValue('');
await expect(dialog.getByRole('region', { name: 'Recent notes' })).toBeVisible();
```

Test the keyboard entry from a clean page separately. Reopen search before testing result navigation. If a CLI is implemented, capture its real command and compare result IDs, not just similar text. A read-only search should leave note data unchanged; compare a public read before and after if that property matters.

Record screenshots or trace states for populated results and the completed empty state, with query and app identity visible. To test unavailable search, use the project's existing controlled fault fixture rather than breaking a shared service.

## Gotchas

- Wait for the expected result or completion indicator; debounce timing is not a fixed sleep contract
- A spinner disappearing does not prove that the query completed successfully
- Navigation changes page state; reset before another independent query
- Newer queries must not be overwritten by an older delayed response
- Permission and archive filters may explain absent results; record their settings
- Retain proof after test fixture teardown
