---
name: find-finite-workflow-counterexamples
description: "Check a bounded workflow model for reachable forbidden states and return a shortest reproducible action sequence, with explicit model assumptions and coverage limits."
---

# Find a Workflow Counterexample

## When to use

Use this when a user or agent needs to examine whether a small approval, publishing, device-control or job-lifecycle workflow can enter a state that should never occur. The output is a reproducible trace or a scoped finite-model safety result. This is not a substitute for testing the implementation, a penetration test, or a proof of eventual progress.

## Required inputs

- Named state variables with finite domains and explicit initial values
- Actions, enabling conditions and atomic state updates
- A safety property expressed as forbidden state combinations
- The model boundary: omitted actors, time, retries, failures and external effects
- An exploration budget and permission boundaries for using any real records

If an action's effects or ordering are unknown, identify the gap before making a safety claim. Use synthetic fixtures where possible. Do not invoke production actions to replay a counterexample without separate authorization.

## Workflow

1. **Translate the question into a property.** Replace “approval is safe” with a testable statement such as “sent and approval-revoked must never coexist.” Confirm whether approval must exist at send time only or throughout the lifecycle; those are different properties.
2. **Choose an adequate state abstraction.** Enumerate each finite domain. Include distinctions that change action eligibility or the property. Record omitted information rather than treating it as impossible. For Boolean variables, the full state-space upper bound is two to the variable count.
3. **Specify transitions precisely.** Evaluate the guard on the pre-state and apply all updates atomically to produce a successor. Unmentioned variables retain their values. Explore every enabled action, not just a preferred business sequence. A no-op transition or cycle still belongs to the model. If a real action is non-atomic, split it into the relevant intermediate steps.
4. **Validate before exploring.** Reject unknown variables, out-of-domain values, duplicate action identifiers and ambiguous input keys. Bound input size and total states/transitions. Do not evaluate arbitrary expression strings from an imported model; use an explicit condition representation or an appropriate trusted modeling tool.
5. **Explore breadth-first from every permitted initial state.** Use a canonical state key and a visited set. Store the first predecessor and action for each newly reached state. Test the initial states against the property before expanding them. With unit-cost actions, the first violating state gives a shortest action-count witness; it is not necessarily the fastest wall-clock path.
6. **Return a replayable witness.** Follow predecessor links backwards, reverse the sequence, and show the initial state, each action and resulting state. Independently check every guard/update in that trace. State which forbidden combination holds at the end. Preserve action order so equal-length alternatives can be explained.
7. **Make completion explicit.** If the reachable queue is exhausted, report complete exploration of this model. If a budget, timeout or unsupported feature stops exploration, report an incomplete search, explored counts and the remaining frontier. “No violation found so far” must not become “safe.” List states with no enabled actions separately; whether they are errors is a different property.
8. **Compare a proposed repair.** Keep the same initial state and property, change only the intended rule, then rerun. A disappearing witness can mean a real repair or an over-restrictive model; check that required successful workflows remain reachable. Tie each model rule back to implementation evidence before claiming the software is fixed.

## Worked example

Two Boolean variables start as approved=false and sent=false. The forbidden combination is sent=true with approved=false.

Actions:
- Approve: when approved=false, set approved=true
- Send: when approved=true and sent=false, set sent=true
- Revoke: when approved=true, set approved=false

Breadth-first exploration reaches four states. The shortest counterexample has three actions:

1. Initial: approved=false, sent=false
2. Approve: approved=true, sent=false
3. Send: approved=true, sent=true
4. Revoke: approved=false, sent=true, violating the stated property

A repair restricting Revoke to sent=false leaves three reachable states and no violation under this model. Send still remains reachable. This only establishes the property as defined: if the real requirement permits revocation after sending, the original property itself needs correction rather than a code change.

Edge case: if the initial state already has sent=true and approved=false, the counterexample has zero actions. Do not discard it because there is no predecessor.

## Output and evidence

Include the model/version or a content hash, variable domains, initial states, property, assumptions, state/transition counts, completeness status, the witness and its replay check. Separate dead ends from safety violations. If proposing a repair, include before/after evidence and a successful-path regression.

An export may contain the full input model and sensitive business logic. Keep it local unless the user authorizes its destination. A passing finite abstraction does not establish authorization compliance, timing guarantees, fairness, eventual completion, or production correctness.

## Verification checks

Test initial failure, unreachable forbidden states, competing enabled actions, a self-loop, a cycle and an intentionally truncated search. Cross-check a tiny model with direct enumeration independently of the main traversal. Never label a budget-exhausted search complete. Stop when the scoped result and replay evidence are established; expanding the model or changing production behavior is a separate decision.
