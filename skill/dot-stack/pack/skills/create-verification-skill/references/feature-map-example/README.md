# Example Notes feature map

This is an illustrative map for a small Notes app. It is not a shipped app or an installed command set. The browser examples use the real Playwright test API, but the sample app, accessible names, and test fixtures must be replaced with observed project facts. Never copy these selectors into a generated recipe without checking the target app.

## Shared fixture contract

The example assumes a test-owned local app, an isolated data directory, and a browser test runner already configured by the project. Its fixture contains `Quarterly plan` with body `Draft budget`, and `Grocery list` with body `Apples`. It contains neither `Release checklist` nor `Discard me`. A project recipe supplies the actual run command, URL, build identity, fixture setup, and cleanup commands; they are deliberately not invented here.

Before each drive, check app identity and fixture ownership. Reset to the baseline between independent tests. If two runs cannot be isolated, use one driver and serialize actions. Readiness waits target an observable state, not a fixed sleep.

## Feature contract

Each feature has four sections:

1. Sub-features, with stable IDs and behavioral outcomes
2. How to get to it, listing user entry points
3. Driving it with the actual driver, including preconditions, action, and expected result
4. Gotchas, including misleading signals and cleanup constraints

Record feature ID and entry point with each result. Browser evidence combines action trace with resulting UI, plus persistence or other side effects when relevant. CLI evidence records exact command, stdout, stderr, exit code, and resulting public state. Capture only synthetic data; exclude tokens and personal records.

## Coverage and unavailable paths

A toolbar pass does not verify a keyboard shortcut. “Blocked: CLI executable unavailable” is different from “Verified: empty search returns no matches.” A verified missing prerequisite does not verify the feature itself. Preserve failed evidence as well as passing evidence, and retain both after cleanup.

## Features

- [Create a note](create-note.md): opening, saving, cancellation, persistence, and CLI parity
- [Search notes](search.md): title/body match, keyboard entry, empty result, clearing, and CLI parity
