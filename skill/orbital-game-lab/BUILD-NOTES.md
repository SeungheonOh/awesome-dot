# Orbit Lab: observed build record

Built October 1, 2026, as an original, dependency-free example for awesome-dot.

## Actual sequence

1. Cloned the repository, read README and CONTRIBUTING, and waited for the owner's requested restructuring window
2. Pulled main to `ea8e298` before implementation, then refreshed it during the build
3. Chose a small game/learning lab rather than another prose-only guide: one launch, three gates, two adjustable variables
4. Implemented pure model functions first; generated each mission's gates from a known reference launch
5. Authored the responsive canvas workspace, control panel, telemetry, prediction, comparison trace, recovery states and flight manual using only HTML/CSS/JavaScript
6. Tested all three solutions, energy drift, impact, escape and deterministic replay with Node.js; syntax-checked the UI module
7. Packaged the static app for private Sites hosting; no account data or credentials belong to this example
8. Wrote the chronological skill from the implementation and evidence, not from a hypothetical product

## Observed checks

`node example/test.mjs` passes all three mission solutions plus impact, escape and deterministic replay. Maximum relative energy drifts observed: 2.75e-10, 2.48e-6 and 6.48e-6. The acceptance threshold is 0.002 (0.2%). `node --check example/dist/app.mjs` passes.

A browser attempt to open the local preview returned `ERR_BLOCKED_BY_CLIENT`. The hosting service supplied a desktop preview image, which was inspected for layout and chart rendering. Real-browser keyboard/touch interaction and mobile visual inspection were not verified in that environment. Responsive CSS and accessible labels are implemented; their existence is not equivalent to an accessibility audit. No benchmark for low-powered phones was run.

## Reuse notes

Use the included files without a build step. A static web server is required for ES modules; opening index.html as a local file may fail in some browsers. Nothing is fetched from outside the app. Progress is intentionally session-only. The optional browser agent interface reports local simulation state only and is not required for play.

The physical model is educational and synthetic. The game does not provide real orbit predictions or operational advice. Original source and text are contributed under the repository's MIT license.

Optional WebMCP registration was source-checked against the supplied interface documentation. No supported browser tool context was available to execute it; that integration remains unverified.
