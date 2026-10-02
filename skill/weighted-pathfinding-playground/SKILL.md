---
name: weighted-pathfinding-playground
description: Build an editable grid-routing visualizer that compares A* and Dijkstra on weighted terrain, reconciles route cost, and handles animation, edits, and unreachable goals correctly.
---

# Weighted pathfinding playground

Make algorithm behavior observable: a user paints walls and terrain, chooses a search method, and watches explored cells become a least-cost route. The worked product is Routecraft, a 12×10 synthetic terrain grid.

## Inputs and scope

Define movement rules, terrain costs, endpoints, supported algorithms, interaction modes, and delivery target. Use a small finite grid for a learning instrument. Do not imply real navigation, accessibility, or safety suitability from a synthetic model.

Read repository guidance, honor the user's allowed services and solo-work limits, and keep app source/tests outside a skills-only contribution. Refresh the default branch before editing and pushing. Publishing a private app on a public hosting endpoint needs an explicit audience decision.

## Chronological build

1. **Fix the cost contract first.** The example allows four orthogonal directions, no diagonals, open-cell entry cost 1, rough-cell entry cost 5, and impassable walls. The starting cell costs zero. State these rules in both the model and interface.
2. **Implement shared neighbors and validation.** Use one row-major index convention and explicit row/column bounds. Reject unsupported terrain values, invalid dimensions, invalid endpoint indices, and unknown method names. Do not allow row-wrap neighbors or negative costs.
3. **Implement Dijkstra as the reference.** Track best known cost, parent, frontier, closed set, and exploration order. Update a neighbor only when the candidate cost improves. Finish when the goal is removed from the minimum-cost frontier, not merely discovered. Reconstruct the path through parent links.
4. **Add A* with a justified heuristic.** For this four-direction grid, Manhattan distance multiplied by the minimum traversable entry cost is a lower bound. With costs at least 1 it is also consistent, so closed nodes need not reopen. If the movement/cost model changes, re-prove consistency or support reopening; do not reuse this assumption blindly.
5. **Separate computation from animation.** Compute the result and exploration order from a snapshot. Animate that order for explanation, then reveal the final route. The visualization speed must never change the path or cost. Provide a skip-to-result control.
6. **Invalidate stale results immediately.** Painting terrain, moving an endpoint, selecting another algorithm, or replacing a map stops the animation and clears old metrics/path colors. Never let an old timer repaint a new map. Protect start and goal from wall painting and prevent them from accidentally merging unless same-endpoint behavior is deliberately supported.
7. **Make editing accessible.** Use clear brush selection and distinct wall, rough, explored, route, start, and goal states. Support pointer painting and keyboard focus/activation. Keep move focus separate from cell cost. Reset restores a known example; a newly generated map resets endpoints when its guaranteed corridor depends on those positions.
8. **Generate useful examples honestly.** A seeded random map can reserve an open corridor to ensure the initial endpoints connect. The corridor is a generation aid, not proof that later user edits remain solvable. Treat an unreachable goal as an expected result with a clear recovery instruction.
9. **Test optimality and interaction recovery.** Compare A* and Dijkstra costs across many deterministic maps, then independently reconcile each returned route's adjacency and entry-cost sum. Test a small weighted detour by hand. Add simulated-DOM checks for run/skip, edit invalidation, no-route display, method changes, endpoint placement, and map reset.
10. **Package and contribute.** Validate the selected host's static-asset configuration without confusing a dry-run with a live deployment. Preserve the authorized audience. Extract the model decisions, failure modes, and evidence into this skill; keep product files elsewhere. Pull main before pushing, inspect the skill-only diff, use a non-force update, and verify the remote commit.

## Useful invariants

- Every path cell is traversable; consecutive cells are orthogonal neighbors
- Reported cost equals the sum of destination-cell costs along the route, excluding the start
- On an open 12×10 grid from opposite corners, both cost and step count are 20
- The same start and goal produce cost zero and a one-cell path
- Sealing both exits from the corner start produces no route
- In a 3×2 grid with top row `[1,5,1]` and bottom row `[1,1,1]`, routing between the top corners costs 4 via the longer bottom detour, instead of 6 through rough terrain
- A* and Dijkstra agree on optimal cost, though equally cheap paths and expansion counts can differ
- A slower animation returns the same result; editing during it clears the pending sequence

Deterministic tie-breaking makes demonstrations repeatable. It does not make one equally optimal path inherently better. Report “explored” according to a defined event, such as removal from the frontier, rather than mixing discovered and expanded nodes.

## Evidence and limits

The original implementation passed 100 seeded A*/Dijkstra comparisons, path adjacency and cost reconciliation, an open-grid check, unreachable and same-endpoint cases, and the hand-calculated weighted detour. A jsdom interaction test passed run/skip, painting invalidation, no-path display, algorithm switching, start placement, and new-map endpoint reset. JavaScript syntax and Wrangler static packaging dry-run passed. Live hosting, real pointer-drag behavior, and mobile visuals were unverified at contribution time.

The small grid uses a simple scanned frontier for clarity. For large maps, use a priority queue and benchmark before promising responsive exploration. Do not hide a slow search behind animation or claim that fewer expanded nodes always means faster wall-clock execution.

## Repair guidance

When a route looks wrong, first compare the reported cost with its cells and check entry-cost semantics. If A* disagrees with Dijkstra, inspect the heuristic and reopening rule before tuning the UI. If stale highlights appear after edits, repair timer cancellation and result ownership. When there is no route, keep that result explicit rather than quietly deleting user-painted walls.
