---
name: compare-weighted-grid-routes
description: "Compute and verify routes through a supplied bounded weighted grid, comparing total cost and search behavior under declared movement rules."
---

# Compare weighted grid routes

## When to use

A user or agent needs a least-cost route or a check of a pathfinding implementation on a discrete grid.

## Required inputs

- Grid cells, obstacles, start/goal and allowed moves
- Nonnegative cost semantics, including whether cost is paid on entry
- Desired algorithms and resource bounds

## Workflow

1. Validate the start/goal and traversable cells. Fix whether diagonal moves are allowed and what they cost before comparing algorithms.
2. Use Dijkstra as the reference for nonnegative costs. For A*, choose a heuristic admissible for the actual movement/cost model; Manhattan distance times minimum entry cost applies to an orthogonal grid.
3. Preserve deterministic tie-breaking for reproducible paths. Keep expanded-node count separate from measured runtime.
4. Recompute every returned route cost directly from its cells, check adjacency and obstacles, and compare with the reference optimum. A different path can have the same optimal cost.
5. Return no-route explicitly when appropriate. Do not alter walls or weights to manufacture a solution.

## Output

Routes, exact cost convention, verified total costs, search metrics and no-route cases. This is a discrete model, not real-world navigation.

## Verification and limits

Test same start/goal, disconnected regions, an expensive short route versus a cheaper longer route, and A* against Dijkstra across bounded generated grids.
