---
name: orbital-game-lab
description: "Evaluate a supplied fixed-step trajectory model against conservation, convergence and terminal-event checks; return measured errors and model limits."
---

# Check a numerical trajectory for drift

## When to use

A simulation produces plausible-looking paths, but the user needs evidence that its numerical integration is behaving consistently.

## Required inputs

- The equations, units, initial conditions and integrator implementation or recorded trajectory
- The supported domain, stop conditions and requested simulation duration
- An error tolerance or permission to report measured error without declaring a pass

## Workflow

1. Freeze the model revision and initial conditions. Separate fictional parameters from measured quantities; do not infer real-world calibration from a visually convincing plot.
2. Identify conservation laws that apply to this model. For an ideal inverse-square two-body model, evaluate specific energy v²/2−mu/r and angular momentum. Do not demand conservation across impulses or terminal collisions.
3. Run identical inputs twice to check determinism. Repeat the same physical interval with step h and h/2, using the same event rules. Compare positions and invariants at aligned physical times rather than array indices.
4. Measure maximum absolute and relative error. Use an explicit scale when the initial invariant is near zero; a division by nearly zero is not a useful relative-drift result.
5. Check impact/escape/time-limit boundaries separately. Report whether events are detected only at sampled endpoints and whether reducing the step changes their classification. Stop before applying a fictional model to real navigation.

## Output

A table of cases, step sizes, duration, error measures, terminal outcome and tolerance result, plus reproducible initial conditions and untested model assumptions.

## Verification and limits

Confirm unit consistency, aligned sample times and unchanged initial conditions. A smaller error at one step size is evidence for that case, not proof of stability for every trajectory.
