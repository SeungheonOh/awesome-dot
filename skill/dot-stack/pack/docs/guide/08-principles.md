# Steer with principle names

The 23 principles are compact ways to ask for a different engineering decision. You do not need to memorize them. Use the one that names the failure you see, and ask the assistant to show what changed because of it.

```text
Apply Prove It Works. The build passed, but the changed import path has not run.
Use the synthetic input and show the stored records after retry.
```

A useful response runs or proposes that check and labels the evidence. Merely listing the principle name is not applying it. Principles guide work inside the task's authorization; they do not override host rules, missing capabilities, or a user's explicit constraints.

## Choose the smallest useful shape

1. [Laziness Protocol](../../skills/principle-laziness-protocol/SKILL.md): prefer the least machinery that actually solves the problem. Before adding a cache, check whether deleting a repeated query solves it
2. [Foundational Thinking](../../skills/principle-foundational-thinking/SKILL.md): settle the essential data structures first. Model a retryable operation's identity and states before writing handlers
3. [Redesign from First Principles](../../skills/principle-redesign-from-first-principles/SKILL.md): incorporate a new requirement coherently. If multi-tenant behavior changes every layer, design tenant ownership explicitly rather than adding unrelated flags
4. [Attack the Premise](../../skills/principle-attack-the-premise/SKILL.md): examine the assumption shared by repeated failed fixes. If more locks never eliminate duplicates, check whether two systems disagree about operation identity
5. [Subtract Before You Add](../../skills/principle-subtract-before-you-add/SKILL.md): remove obsolete structure before extending it. Identify unused adapters and migrate their remaining callers within the approved scope
6. [Minimize Reader Load](../../skills/principle-minimize-reader-load/SKILL.md): reduce hidden state and unnecessary hops. Keep a small operation's decision and result close enough to follow in one reading
7. [Outcome-Oriented Execution](../../skills/principle-outcome-oriented-execution/SKILL.md): move toward the intended end state. Do not preserve a temporary compatibility branch forever merely because an early migration step needed it
8. [Experience First](../../skills/principle-experience-first/SKILL.md): judge the user-visible result. A faster form that loses the user's input on validation failure is not an improvement
9. [Exhaust the Design Space](../../skills/principle-exhaust-the-design-space/SKILL.md): compare genuinely different approaches when precedent is weak. Prototype a streaming parser and a bounded-buffer parser against the same constraints
10. [Build the Lever](../../skills/principle-build-the-lever/SKILL.md): make repeated work or proof repeatable. A small migration audit can identify every old caller and run again after each change

## Put state and rules in the right place

11. [Model the Domain](../../skills/principle-model-the-domain/SKILL.md): give repeated business rules one representation. Encode order transitions once rather than duplicating conditions across endpoints
12. [Boundary Discipline](../../skills/principle-boundary-discipline/SKILL.md): validate at genuine trust boundaries. Parse unknown request data once, then use the validated internal shape
13. [Type System Discipline](../../skills/principle-type-system-discipline/SKILL.md): make contradictory states hard to express. Prefer distinct pending and completed variants to unrelated booleans that can both be true
14. [Make Operations Idempotent](../../skills/principle-make-operations-idempotent/SKILL.md): make retry converge on the intended state. A retry key must identify the same operation, and concurrency still needs a proven storage contract
15. [Migrate Callers Then Delete Legacy APIs](../../skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md): finish migrations rather than accumulating duplicate interfaces. Census callers, migrate them, check external compatibility obligations, then remove the obsolete API when authorized
16. [Separate Before Serializing Shared State](../../skills/principle-separate-before-serializing-shared-state/SKILL.md): remove unnecessary sharing before adding coordination. Give implementation candidates separate workspaces instead of making them queue for one output file

## Demand proof that matches the claim

17. [Prove It Works](../../skills/principle-prove-it-works/SKILL.md): exercise the real artifact. For a saved preference, reload the app and read it back; a successful click is insufficient
18. [Fix Root Causes](../../skills/principle-fix-root-causes/SKILL.md): trace the reproduced failure to its cause. Suppressing a duplicate warning does not prevent the duplicate write
19. [Sequence Work into Verifiable Units](../../skills/principle-sequence-verifiable-units/SKILL.md): finish a small checkable unit before stacking more uncertainty. Move one parser caller, verify it, then apply the pattern to the rest
20. [Test Behavior, Not Implementation](../../skills/principle-test-behavior-not-implementation/SKILL.md): assert observable outcomes with meaningful expected values. A retry test should prove one stored record, not merely count helper calls

## Keep collaboration bounded

21. [Guard the Context Window](../../skills/principle-guard-the-context-window/SKILL.md): preserve the information needed for decisions. Delegate bounded reading when real workers exist; otherwise summarize incrementally with evidence locations instead of pretending to delegate
22. [Never Block on the Human](../../skills/principle-never-block-on-the-human/SKILL.md): continue useful, reversible work that is already authorized while a separate decision is pending. It does not authorize a required approval, expand scope, or interpret silence as consent

## Turn recurring lessons into structure

23. [Encode Lessons in Structure](../../skills/principle-encode-lessons-in-structure/SKILL.md): replace repeated advice with a durable check when warranted. If a migration repeatedly misses a caller class, extend the caller audit and test the extension instead of adding another reminder paragraph

## Put a principle into a concrete instruction

```text
Use Separate Before Serializing Shared State for these experiments.
One output directory per attempt. Name the integration owner.
```

```text
Apply Boundary Discipline. Show where untrusted input becomes validated data.
Remove only the redundant internal guards justified by that boundary.
```

```text
Use Encode Lessons in Structure. Propose a check that catches this failure,
and show it fail on the old example before adding it to the project.
```

Each instruction has a visible consequence. If two principles point in different directions, the assistant should explain the tradeoff. Building a reusable harness costs more up front than one manual check; it earns its place when repetition or risk makes that investment worthwhile.

Next: [Make it yours](09-make-it-yours.md).
