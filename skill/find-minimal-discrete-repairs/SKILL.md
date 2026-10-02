---
name: find-minimal-discrete-repairs
description: "Find a minimum-cost repair for a small finite configuration while preserving locked choices, verifying the goal predicate and separating a valid target from a safe sequence of real changes."
---

# Find Minimal Discrete Repairs

## When to use

Use this when a user or agent has a small configuration that violates explicit rules and wants the fewest changes, a lowest-cost alternative or one verified next edit. Examples include a bounded flag model, a finite arrangement puzzle or a small configuration planner.

The output is a proposal within the supplied model. It does not apply settings, change permissions, deploy a service or establish that a production migration is safe.

## Required inputs

- An immutable starting configuration and finite candidate values for each field
- The exact goal/validity predicate and any fixed or locked fields
- Permitted edit operations, their costs and whether ordering matters
- Whether intermediate configurations must also satisfy constraints
- A search bound, tie-breaking rule and requested output

Do not infer permission to relax a locked field because no repair was found. If costs or allowed values are unknown, resolve the part that changes the optimum rather than silently treating all edits as equivalent.

## Workflow

### 1. Separate target validity from transition validity

Define what makes a final configuration valid. Separately identify restrictions on how the system can move there. A valid set of feature flags may still be unsafe to reach by flipping them in an arbitrary order.

For independent Boolean toggles with unit cost and no intermediate restrictions, the cost between two configurations is the number of differing coordinates. For categorical fields, that simple distance applies only when one allowed operation changes a field directly to any chosen alternative at the same cost. More complex transition rules need a path search, not just comparison of final states.

### 2. Validate the finite domain and freeze the baseline

Check field identities, allowed values, locks and numeric costs. Compute or bound the size of the candidate product before searching. Twelve Boolean fields have 4,096 configurations; a dozen fields with many categorical values can be much larger.

Use a baseline copy that cannot change during the solve. A repair calculated before the user edits a field is stale even if it still happens to satisfy the goal. Preserve the original configuration and state exactly which fields a proposed repair changes.

### 3. Enumerate and verify candidates within scope

For a small complete search, enumerate the permitted combinations while keeping locked values fixed. Apply the exact goal predicate to each candidate. Record verified valid configurations or enough information to recover an optimal witness.

Do not stop at the first valid candidate unless its cost reaches a proven lower bound. Enumeration order is not an optimality argument. If a budget ends before all relevant alternatives have been excluded, return a verified incumbent with optimality unknown, or an explicit incomplete result.

### 4. Calculate the declared cost exactly

For independent Boolean toggles, compute the XOR of the starting and target masks and count its set bits. This is a shortest edit count because every differing bit must be flipped at least once and flipping each exactly once reaches the target.

For independent weighted field changes, sum the supplied coordinate costs. Use exact arithmetic or a defined comparison tolerance appropriate to the model; reject non-finite or unexplained costs. If edit effects interact or a field may require several intermediate values, use the actual transition graph instead of this shortcut.

Keep feasibility, minimal cost and uniqueness separate. Several targets can share the same minimum cost. Use an explicit stable tie-break for repeatability, without calling the first tied target aesthetically or operationally best.

### 5. Produce a verified next edit only when justified

When independent toggles are the allowed operation, choose one differing coordinate from a minimum-cost witness. Flipping it reduces the remaining minimum distance by exactly one: the witness is now one step closer, and a single flip cannot reduce distance by more than one.

This reasoning does not hold automatically for constrained transitions. If intermediate states have requirements, verify that the proposed step is permitted and that a remaining path still exists. Do not turn a target-state proof into an execution plan without those checks.

Preserve user choices when required. An interactive hint should clearly show the changed coordinate and remaining distance, keep keyboard focus usable, and be invalidated if the underlying model or baseline changes.

### 6. Independently verify the result and recovery controls

Check the returned target against the original rules, recalculate its edit set and cost, and compare with a separate small oracle where practical. Test ties, an already valid baseline, unsatisfiable locks, invalid input, undo and reset.

For a finite geometric model, an independent simulator using a different representation can catch mistakes shared by the optimizer and its main validator. The implementation that motivated this workflow compared 8,192 mirror configurations against a separate vector-based ray simulation, then verified each hint reduced the exact remaining flip distance by one. That evidence concerns the tested model, not physical optics or a live configuration service.

## Worked example

Three Boolean fields A, B and C start at 000. The rules require A to differ from B and B to equal C. The only valid targets are:

- 100: change A, cost 1
- 011: change B and C, cost 2

Under independent unit-cost flips, 100 is the unique minimum repair. If A is locked at zero, 100 is unavailable and the minimum repair becomes 011 with cost 2. If all three fields are locked, no repair exists within the permitted domain.

Direct enumeration of all eight assignments confirms those two valid targets and their costs. A production rollout may still have ordering constraints absent from this example; changing B before C temporarily violates B=C. Report that difference instead of asserting that the target can be applied safely one field at a time.

## Deliverable and stopping point

Return the baseline, locked fields, validity rules, search coverage, chosen target, exact changed fields, cost, ties and the basis of minimality. State whether intermediate-state safety was checked. Apply nothing outside the model unless the user's request separately authorizes the concrete real-world changes.
