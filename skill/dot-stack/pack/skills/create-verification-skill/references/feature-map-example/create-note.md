# Create a note

Illustrative contract: users create a note from the toolbar, a keyboard shortcut, or a project CLI; saving persists it and cancellation discards an unfinished draft. See the [example limits](README.md) before adapting.

## Sub-features

- `create-open`: toolbar and keyboard entry each open a blank editor
- `create-save`: save stores the title and body once, including repeated-click protection if promised
- `create-cancel`: cancel creates no saved note
- `create-persist`: a newly opened view sees the same saved content
- `create-cli`: the documented CLI creates a note visible through the browser

## How to get to it

In the sample app, select `New note`, or press `n` when focus is outside an editable field. A CLI is an additional entry point only if the actual repository implements one. Record its inspected invocation in the real feature map, not a guessed command.

## Driving it with Playwright

Preconditions: isolated baseline fixture, expected app revision, no note titled `Release checklist`, and an already-open sample app page. This snippet belongs inside an existing Playwright test with `page` and `expect` supplied by that runner:

```ts
await page.getByRole('button', { name: 'New note', exact: true }).click();
const editor = page.getByRole('form', { name: 'Note editor' });
await expect(editor).toBeVisible();
await editor.getByRole('textbox', { name: 'Title', exact: true }).fill('Release checklist');
await editor.getByRole('textbox', { name: 'Body', exact: true }).fill('Check release notes');
await editor.getByRole('button', { name: 'Save note', exact: true }).click();
await expect(page.getByRole('status')).toHaveText('Note saved');
await page.getByRole('link', { name: 'All notes', exact: true }).click();
await page.getByRole('link', { name: 'Release checklist', exact: true }).click();
await expect(editor.getByRole('textbox', { name: 'Body', exact: true }))
  .toHaveValue('Check release notes');
```

Separately reset to the baseline and test the keyboard entry. Test cancellation by entering `Discard me`, selecting `Cancel`, and asserting that the saved list has no such note. If a CLI exists, run its observed create command, capture its exit and output, then reopen the created note in the browser. Label unsupported paths, do not imply parity.

Capture the action trace and the reopened persisted state. A successful toast alone is insufficient. If reload is part of the persistence claim, reload and recheck the same note through a public entry point.

## Gotchas

- `n` in a textbox is text input, not a shortcut
- A save may normalize whitespace; assert the documented stored value
- Do not query private component state to stand in for persistence
- A cancellation failure is product behavior to report, not a reason to weaken the map
- Cleanup removes only test-owned notes and processes, while retaining evidence
