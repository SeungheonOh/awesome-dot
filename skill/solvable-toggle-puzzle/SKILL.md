---
name: solvable-toggle-puzzle
description: Build a lights-out browser puzzle with guaranteed solvable boards, shortest-solution hints from binary linear algebra, keyboard controls, and exhaustive small-board verification.
---

# Solvable toggle puzzle

Build a small game whose hints are proved by its model. The worked product, Lumen Grid, uses a cross-shaped toggle: pressing a tile flips itself and its orthogonal neighbors; the goal is an all-dark board.

## Choose the scope

Use this workflow for a deterministic finite toggle puzzle, not for arbitrary pathfinding or continuous physics. Establish the board size, press rule, win condition, reset/undo behavior, publishing target, and contribution limits. In a solo build, keep everything in the assigned workspace and approved services. For a skills-only contribution, keep the implementation, tests, and hosting metadata outside the skill repository.

## Chronological workflow

1. **Read and refresh the repository.** Check current contribution guidance, preserve the user's narrower instructions, and update the default branch before work and before publication. Avoid duplicate skills with the same outcome.
2. **Implement the press rule once.** For a row-major cell index, include itself plus in-bounds up/down/left/right cells. Pure `press(board, index)` returns a copy. Generation, gameplay, undo, and solver verification must share this rule; separate ad hoc implementations can disagree at edges.
3. **Generate from a known solved state.** Begin with all zeros and apply a seeded set of presses. The resulting board is solvable by construction. If it remains all zeros, apply one press. Expose the seed or a UTC-date label for reproducibility. Do not generate arbitrary random cell states and assume a solution exists.
4. **Build the algebraic model.** Over GF(2), represent each press as a column of a binary influence matrix A. For current board b, solve `A x = b`; a 1 in x means press that cell once. Addition is XOR. Repeated presses cancel, so a shortest solution need never press a cell twice.
5. **Reduce and enumerate carefully.** Gaussian-eliminate the augmented matrix using XOR and record pivot columns. An all-zero coefficient row with right-hand side 1 proves inconsistency. Assign free variables, solve pivot variables, and enumerate the resulting solution family when the nullity is small. Choose the solution with minimum Hamming weight. Only then call it a shortest solution; arbitrary elimination output is merely one solution.
6. **Keep the UI game-first.** Lead with a tactile board, a few clear counters, and a concise rule. Show the exact initial minimum as a target. Provide one-move hints and an optional full-solution overlay, recomputed from the current board. Mark suggestions separately from the on/off state so a hint is never mistaken for a lit tile.
7. **Make recovery predictable.** Store press history. Undo applies the same press and removes that history entry. Restart restores the original board and resets history and hints. A new seed creates a new board; changing size regenerates the selected seed under the new dimensions. Describe whether move counts exclude undone moves and whether progress persists.
8. **Provide non-pointer play.** Use actual buttons with row, column, state, and suggestion labels. Support arrow-key focus movement and native Space/Enter activation. Preserve focus after rerendering, announce win/status changes, and honor reduced motion. Keep touch targets usable on the small layout.
9. **Prove the solver against gameplay.** Apply every returned solution through the same press function and require all zeros. Test generated boards across both supported sizes. On a sufficiently small board, enumerate every press mask independently, record the minimum count per reachable board, and compare solver output against that table. This checks shortestness rather than merely self-consistency.
10. **Publish and extract the skill.** Verify deployment completion and inspect available previews. Keep unperformed interaction checks explicit. Refresh main, review only the skill diff, publish within granted scope without force-pushing, and verify the remote revision. Continue to another distinct product if the user's assignment is ongoing.

## Representation guardrail

The worked implementation supports only 4×4 and 5×5 boards. It stores each augmented row in a JavaScript 32-bit bit mask, using at most 26 bits. Do not casually extend it to 6×6: JavaScript bitwise operators truncate to 32 bits and would silently corrupt the matrix. For larger boards, use BigInt or explicit bit arrays and impose a practical limit on free-variable enumeration. Report an unavailable shortest solution honestly instead of claiming an unbounded search will finish.

For these 4×4 and 5×5 rules, exhaustive enumeration of the small free-variable family is practical. That fact does not generalize to every board size or toggle topology.

## Validation contract

- A corner press flips three cells; an interior press flips five
- Pressing any cell twice restores the original board
- Press order commutes
- The same seed and size reproduce the same board
- Generated starts are nonempty and solvable
- Solving an all-zero board yields an empty press list
- Applying a returned solution clears every cell
- The chosen solution length equals the independently enumerated minimum on the small board
- Hint after a manual move is recomputed for the new board
- Undo works after winning; restart and size changes clear old overlays and history
- Keyboard focus, touch behavior, and reduced-motion presentation are checked in a real browser when available

The original build checked 200 generated boards across 4×4 and 5×5, deterministic seeds, edge neighborhoods, double-press cancellation, and commutativity. Independently enumerating all 65,536 press masks established minima for all 4,096 reachable 4×4 boards; the solver matched every one. JavaScript syntax checks and private deployment passed. Full browser interaction, mobile visual, and optional WebMCP execution checks remained unverified. These are evidence about that build, not inherited test results for future versions.

## Stop conditions

If generation produces an unsolvable board, repair the shared press rule or solver before styling. If a returned hint cannot be applied to clear the board, remove the correctness claim until fixed. If shortestness is not established, label hints as a valid solution rather than a minimum. Do not add accounts, paid hints, saved progress, telemetry, or external services just because the game can support them.

## Subsequent verification

A hosting-provided desktop image was inspected, prompting a more compact board layout. A jsdom interaction test passed hint-to-win, undo after winning, restart, size changes, arrow-key focus, and read-tool behavior; these are simulated DOM checks, not real-browser coverage.
