# Design rationale

Use the sections that resolve the actual decision. Replace instructional notes with project facts. A small decision may fit on one page; retain the evidence needed for a consequential one.

## Problem and constraints

State the user outcome, observed source revision, affected callers, compatibility promises, and measured limits. Distinguish facts from assumptions. Name what is outside scope.

## Usage before types

Show what a consumer imports, passes, receives, and does on failure. Include two representative call sites rather than a catalog. The type sketch must support these examples without hidden sequencing rules.

## Proposed shape

Show domain types, signatures, ownership, and data flow. Locate parsing and validation. Explain the invariant each boundary protects, the complexity hidden from callers, and the remaining caller responsibilities. Use labeled pseudocode where the implementation is not yet known.

## Selection and synthesis

Name the base candidate and the task-specific reason it wins. Name any borrowed idea and how it fits the base. Record rejected alternatives, failed candidates, and whether the comparison was independent, model-diverse, or a sequential self-comparison. Do not claim validation merely because candidates agree.

## Tradeoffs and alternatives

Write “Accept X to obtain Y” for consequential tradeoffs. Describe at least one genuinely different feasible design when there is one. Explain its caller burden and hidden complexity. If constraints determine a single viable shape, name those constraints rather than inventing a rival.

## Proof and remaining questions

For each important invariant, name the intended test, current evidence, and status. Ask only questions that could change the choice. Distinguish a product decision from unavailable tool access.

## Next step

Specify the first bounded implementation slice and its acceptance condition. State whether implementation is authorized or the deliverable ends here.
