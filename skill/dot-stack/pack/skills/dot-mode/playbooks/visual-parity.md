# Visual parity

Use for a visual migration or matching an approved implementation. Read the [execution contract](../references/execution-contract.md). The approved baseline is the spec and remains unchanged during comparison.

## Inputs

Baseline revision or reference images, candidate, target viewports/devices, fonts, content, relevant interaction states, rendering environment, and the agreed difference tolerance. Pixel-exact requests require zero meaningful difference under controlled conditions; a tolerance must not be invented after a failure.

## Steps

1. Capture and freeze the baseline before editing. Cover loading, empty, error, expanded/focused/hovered states as relevant. Record viewport, scale, browser/runtime, font readiness, animation settings, and data fixtures so captures are comparable.
2. Validate the comparison harness with a deliberate visible change. Define allowed nondeterministic regions only for a justified external source, never to mask changed product behavior. Keep baseline and harness review separate from the migration.
3. Migrate shared primitives first, then coherent components. One writer owns each component and shared dependency. Parallel work uses isolated worktrees and the same baseline settings.
4. Capture candidate states and compute image differences. Inspect the diff and affected interaction, not just an aggregate score. Investigate font/antialiasing/environment noise separately from layout, paint, and content regressions.
5. Fix candidate defects and rerun affected states. If the baseline itself is wrong, stop for the product decision; do not update it silently. Do not restructure unrelated behavior merely to appease a screenshot check.
6. Verify keyboard access, focus visibility, interaction semantics, and responsive behavior where the change can affect them. Pixel equality alone does not prove accessibility or event handling.

## Failure and completion

Missing baseline, unsupported rendering environment, or incomparable screenshots prevents a parity claim. Retain mismatches and the exact candidate identity. Return components and states tested, difference/tolerance results, baseline/harness locations, interaction checks, and remaining gaps. Publish only if requested. A failing diff is not a reason for an unbounded retry loop or to broaden scope.
