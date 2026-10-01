---
name: orbital-game-lab
description: Build a playable, deterministic orbital-mechanics browser lab with solvable missions, trajectory previews, explicit model limits, and numerical tests. Use for a small interactive physics game or learning tool, not real spacecraft navigation.
---

# Orbital game lab

Turn a physical idea into an experiment someone can immediately play. The worked product is **Orbit Lab**: set a probe's launch speed and angle, predict its path, and pass three gates with one impulse.

## Inputs and boundaries

- A learning objective and intended player. If unspecified, use a beginner exploring how sideways speed changes an orbit
- A browser-based delivery target, and permission to publish if hosting is requested
- The user's constraints on collaborators, dependencies, services, and public repository contributions
- An environment with Node.js for deterministic checks; a static HTTP server for local play

Use fictional units and synthetic missions. No account, API key, live data, model calls, purchase, or backend is needed. Follow explicit solo-work limits. Hosting and repository publication are separate actions; obtain permission for each when not already supplied.

## Chronological procedure

1. **Read the destination first.** Fetch current repository guidance and contribution structure. Keep unrelated changes intact. In a moving repository, refresh the default branch before editing and again before publishing your change. Never force-push over concurrent work.
2. **Choose one playable loop.** Define the controls, goal, success, failure and reset before adding decoration. Here: two sliders → launch → gate progress → success, impact, escape or time limit → retry. A help section supports the loop; it does not replace the game.
3. **Isolate the model.** Put pure functions in a separate module. This example uses inverse-square acceleration and velocity-Verlet with a fixed 1/120-second step. Rendering and wall-clock frame rate must not change simulated results. Keep the domain finite and stop at surface contact, escape or the time limit.
4. **Make missions demonstrably solvable.** Start with a known safe trajectory, then place gates at sampled points along it. Do not eyeball targets and hope a solution exists. Expose an optional working launch so an unfamiliar player can learn by comparison. Keep it available without penalty.
5. **Build the actual working surface.** Lead with a large orbit plot and adjacent controls. Use a restrained palette, legible telemetry and a distinctive planet/trajectory treatment. Draw the scene procedurally; external art or network requests would add no value here. Include a custom favicon.
6. **Connect feedback and recovery.** Recompute the prediction after edits, show progress in text as well as rings, distinguish impact from escape, and preserve the last path as a faint comparison. Disable launch edits during flight. Provide pause/resume and reset; pause when the page is hidden. Keep keyboard controls usable without hijacking slider or button keys.
7. **Test numerical and interaction invariants.** Run the example tests below. Check mission switching, pause, reset, prediction toggling, control labels, mobile layout and hidden-tab behavior when a real browser is available. Make deterministic tests independent of the UI. Report unavailable browser checks honestly.
8. **Publish the product, then extract the method.** Use the user's selected hosting service and keep its initial audience private unless wider sharing is authorized. Verify terminal deployment success. Never commit host credentials, private data, runtime state or host account metadata to the public skill folder.
9. **Contribute the reusable result.** Contribute only the skill instructions. Keep product source, test files, deployment metadata and build notes outside the skills repository. Summarize the tested method and relevant limits within the skill itself. Pull current main, review only your diff, run the checks again, commit and push within the granted scope. On a non-fast-forward rejection, fetch and reconcile; never discard another contributor's changes. Verify the remote commit before claiming it was pushed.

## Model and trade-offs

For position **r**, acceleration is `a = -mu * r / |r|^3`. Update position using the current acceleration, calculate acceleration at the new position, then update velocity with the mean acceleration. Specific orbital energy is `|v|^2 / 2 - mu / |r|`.

The example chooses `mu = 1,800,000`, surface radius `46`, an impact threshold of `51`, escape radius `780`, and a 28-second simulation limit. These are game parameters, not measurements. Gate collision radius is 24 units; a slower time step is preferable to inflating a gate silently if numerical misses appear. Orbital energy should remain nearly constant away from terminal events. Negative energy indicates a bound ideal two-body trajectory, not guaranteed mission success.

This model omits atmosphere, thrust after launch, relativity, rotating reference frames and interacting celestial bodies. It must never be used for real navigation or engineering safety decisions.

## Validation and delivery

Keep the implementation and test suite in the product workspace, not in the skills contribution. Validate these observable properties before calling the product complete:

- All three reference launches intersect all three gates
- Repeat runs return identical trajectories
- Zero speed impacts; sufficiently high speed escapes
- Relative energy drift stays below 0.2% for the three reference trajectories
- Prediction uses the same integration code as the live flight
- A failed or paused flight can be reset without retaining old gate progress
- The page labels its fictional model and needs no remote dependencies

For the original build, the three reference trajectories passed with maximum relative energy drifts of 2.75e-10, 2.48e-6 and 6.48e-6. Impact, escape, deterministic replay and JavaScript syntax checks passed. A hosting-provided desktop image was inspected. Local browser access was unavailable, so full keyboard/touch, mobile visual and optional WebMCP execution checks remained unverified. These observations describe that build; rerun checks on each new implementation rather than inheriting its success.

Deliver the finished product through the requested hosting channel. The repository contribution is this skill alone: the chronological procedure, model choices, acceptance criteria and honest limits. Do not upload the app, tests or a separate build diary unless explicitly requested.

## Failure handling

If a mission has no passing reference trajectory, fix the model or target generation before tuning aesthetics. If browser testing is unavailable, retain the tested source and state exactly which interactions remain unverified. If publishing fails, keep the working local artifact and resume the same deployment rather than creating duplicates. If the user asks for scientifically calibrated data or another model, establish the units, sources and error tolerance before replacing the fictional parameters.
