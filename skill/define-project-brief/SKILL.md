---
name: define-project-brief
description: Turn an underspecified project request into an actionable brief with outcomes, scope, acceptance criteria, and the few decisions that affect delivery. Use before substantial work when different reasonable interpretations would produce different results.
---

# Define a Project Brief

Turn a fuzzy request and its available context into a brief someone can act on. Resolve ambiguity about the result, rather than prescribing a project-management ceremony. A clear small task may need only a sentence and its completion check; do not make the user approve a formal brief before ordinary work they already requested.

This skill establishes what should be achieved. It does not choose a workflow from a collection, optimize a schedule, or expand a request into a product roadmap.

## Find the actual job

Read the request, supplied material, and relevant existing work. Reuse facts already available instead of asking the user to fill in a template. Identify:

- Who will use the result and what they need to accomplish
- The current difficulty, with a concrete example when available
- The requested deliverable, its destination, and constraints that affect it
- What would make the result useful, and what would make it unacceptable

Keep a proposed solution separate from the underlying need. “Add a dashboard” might mean finding late orders, explaining an existing report, or producing a screen for a demonstration. If the user has explicitly chosen a dashboard, preserve that choice; use the distinction to understand its required behavior, not to replace it with your preferred product.

Look for existing decisions and conventions before reopening them. The user's latest instruction can resolve an older conflict. A newer file date alone cannot establish which proposal was accepted.

## Resolve only consequential ambiguity

Ask a question when its answer changes scope, an irreversible choice, a material commitment, or how success will be judged. Frame the question around a concrete difference: “Should an empty search show no matches or all records?” is more useful than “Can you elaborate?”

Proceed with disclosed ordinary assumptions when the work is easy to revise and the request permits judgment. Keep unresolved consequential choices visible instead of silently choosing them. A draft can be complete enough to review while one decision remains open; mark the affected part and continue independent work.

When several interpretations are genuinely plausible, explain their different outcomes and recommend one using the user's stated priorities. Do not invent priorities, time savings, demand, budget, or authority to make the recommendation sound settled.

Avoid collecting information that will not change this brief. A missing launch date does not block describing an internal tool. A missing audience does matter if it determines whether the output is an executive summary or an operational manual.

## Describe a bounded result

Write the brief around observable outcomes. Include the following only to the depth the task needs:

**Purpose and user.** State the problem and intended beneficiary in concrete language. Explain how the result will be used, not just what file or feature will exist.

**Scope and boundaries.** Name the behavior or content included, the existing behavior that must survive, and any plausible adjacent work explicitly excluded. Avoid invented exclusions that make a straightforward request harder. Distinguish the current deliverable from possible later improvements.

**Acceptance criteria.** Translate each important requirement into an observable example or check. State the starting condition, action or supplied input, expected result, and relevant exception. Match the check to the work: a reader can find the required answer in a guide; an exported file preserves specified fields; an application handles an empty result without losing the query. Do not use “intuitive,” “robust,” or “high quality” as the only acceptance criterion.

**Inputs and dependencies.** Name the sources, access, decisions, or other deliverables actually needed. Distinguish what is available from what is assumed. Say which part is blocked by a missing dependency rather than labeling the whole project blocked.

**Open decisions.** State the choice, why it matters, and who can resolve it if known. Record an assumption as an assumption, not as a user decision. Do not invent an owner, deadline, estimate, or commitment.

Keep implementation choices out of the requirements unless the user selected them, compatibility demands them, or evidence makes them necessary. “Return the approved record identifiers” is a behavior requirement; a specific database or framework may be only one implementation option.

## Check that the brief can guide real work

Walk through one ordinary use and one important boundary case using the actual context. Check that the acceptance criteria would distinguish a useful result from a plausible but wrong one. If every criterion can pass while the user's main difficulty remains, revise the brief.

Check each requirement against its source. Remove unsupported scope, reconcile duplicates, and surface contradictions that remain unresolved. Qualitative work still needs judgment: use a reader task, concrete examples, or stated editorial criteria rather than forcing it into a misleading numeric score.

Choose the smallest deliverable that achieves the requested outcome while preserving required behavior. “Smallest” does not authorize omitting a required output, quality gate, or essential failure path.

## Deliver and continue

Return the usable brief in the requested format. A practical default is a short purpose paragraph, a bounded scope, acceptance criteria, and the remaining decisions or dependencies. Link the relevant source material where doing so makes the reasoning reviewable; a separate traceability ledger is unnecessary for a small task.

If the user asked only for a brief, finish there. If they asked for the work itself, continue into the authorized implementation when the brief is sufficiently clear. Ask only for a consequential unresolved choice or an action that still requires approval. Do not insert a new approval round merely because you wrote the brief.

As new evidence changes the task, update the affected scope and acceptance criteria. Explain a material change before work that depends on it. Report proposed, implemented, and verified outcomes accurately; a finished brief is not a delivered project.

[Examples](examples.md) show a vague software request, an editorial request, and a clear task that should proceed without a formal briefing exercise.
