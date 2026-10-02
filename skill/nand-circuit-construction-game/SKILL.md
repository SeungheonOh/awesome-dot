---
name: nand-circuit-construction-game
description: Build an interactive NAND-only combinational-logic game with exhaustive truth-table validation, editable acyclic circuits, and tested gate budgets. Use for Boolean circuit teaching tools rather than analog or timed electronics simulation.
---

# NAND circuit construction game

Build a game where correctness is visible for every possible input, rather than inferred from a few animations. A single gate type keeps the editing language small while shared subexpressions make the puzzles interesting.

## Inputs and scope

Define target Boolean functions, input names, gate budgets, example circuits and short hints. Keep the simulator combinational: no feedback, timing, metastability or physical-electronics claims. One to three Boolean inputs give at most eight truth-table rows, making exhaustive checking cheap enough for every edit.

For a skills-only repository, keep this reusable procedure in the contribution and deliver the game and tests separately. Public hosting requires its own authorization.

## Construction order

1. Define circuit identity independently of its drawing. Number the primary inputs first, followed by gates in creation order. Each NAND has exactly two references to primary inputs or earlier gates. A separate node reference chooses the output. Reject forward references, nonexistent outputs and budget violations at the model boundary.
2. Exhaust the input space. Enumerate binary rows in a stable documented order; evaluate gates topologically using NAND(a,b)=1−(a AND b). Compare the selected output with a separately defined target function for every row. Return all intermediate node values, row matches and overall solved status from the same pure evaluator.
3. Build example solutions before the UI. For XOR, share A NAND B between two branches: NAND A with the shared value, NAND B with it, then NAND the branch results. For a selector, combine A AND not-S with B AND S through complemented NAND branches. Verify examples against the independent target truth function, not hand-entered expected labels.
4. Distinguish a construction budget from a proven minimum. For small-input puzzles, an independent breadth-first search can represent each signal by its truth-table bitmask. A state is the set of available signal functions. Add each possible NAND of two available functions, deduplicate function sets, and search by added-gate count. Repeated equivalent functions do not add capability under unlimited fan-out. Do not run an uncontrolled search for larger input spaces or call unsearched budgets optimal.
5. Make the editor preserve the graph invariant. Each socket selector offers only primary inputs and earlier gates. Adding a gate can select it as the output. Removing only the final gate avoids repairing arbitrary downstream references; if it was the output, select a remaining valid node. Store bounded immutable edit snapshots for Undo.
6. Draw from model values, not a second simulator. Show the selected truth row's 0/1 values on inputs, wires, gates and output. Let the user choose a row or toggle an input. Match the table and diagram on every change. A horizontally scrollable circuit is preferable to unreadably shrinking a long diagram on a phone.
7. Give precise feedback. Show matched cases out of total and which rows fail. Do not declare a circuit solved merely because the currently selected row matches. Keep hint/example assistance explicit. An assisted solve should not overwrite a previously earned unaided solve, and Undo should not erase the fact that a solution was revealed.
8. Reset deliberately. A new challenge clears its working circuit, probe, hint index and undo history. If retaining session-level achievements, label them as session progress. Avoid silently persisting account-like history or implying progress survives reload when it does not.
9. Export an inspectable recipe: challenge ID, input names, gate operations/references, selected output, and the complete actual-versus-target truth table. A partially correct circuit may be exported if labeled by its actual table; export must not imply completion.

## Verification plan

Test every example circuit against every input. Include repeated gate inputs (inversion), shared intermediate nodes, an output wired directly to a primary input, a forward-reference error, an invalid output and an exceeded budget. For tiny-input puzzles, compare budgets with the independent bitmask search.

Interaction tests should cover adding a winning gate, disabling Add at budget, Undo, challenge switching, assisted examples, a socket edit that breaks a previously solved circuit, input probes, removing the selected output, reset, guide dismissal and exported truth tables. Verify that every offered socket reference is valid for that gate.

Render an actual generated SVG diagram with an independent renderer when possible and inspect labels, wire endpoints and logical ordering. This is useful diagram evidence but does not establish the complete page's responsive layout or keyboard usability; those need real-browser checks.

## Worked build

NAND Garden implemented nine challenges: inversion, AND, OR, NOR, XOR, equality, three-input AND, a selector, and majority. All nine example circuits passed exhaustive target comparisons. Breadth-first truth-function search verified the one- and two-input budgets; the three-input budgets were deliberately described only as construction targets.

Simulated-DOM tests passed the editing, undo, budget, probe, example, output-repair and recipe flows. A generated four-gate selector diagram was rendered with CairoSVG and visually inspected. Actual browser layout and device interaction remained unverified. These are results of that implementation, not automatic guarantees for another game built from the skill.

## Delivery

Deliver the game with its examples and model/interaction checks. State which budgets are proven, whether assistance/progress is retained, and which browser checks remain. Publish only where authorized; a skill-only contribution should contain the workflow rather than game assets or tests.
