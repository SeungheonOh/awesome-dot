---
name: principle-subtract-before-you-add
description: "Simplify the directly affected design by removing proven dead or redundant structure before extending it, while preserving live contracts and necessary safeguards."
---

# Subtract before you add

Use this when an addition or refactor would otherwise build on obsolete paths, duplicated decisions, empty references, or misleading scaffolding. Remove complexity with evidence, not by assuming every existing constraint is unnecessary.

## Find safe subtraction

Identify what the change actually depends on. Look for unreachable code, unused internal exports, duplicate validation of the same stable invariant, obsolete compatibility paths whose consumers have migrated, or references with no distinct content. Inspect callers, configuration, dynamic registration, generated use, and documented public contracts before calling something dead.

For each removal, state the behavior that remains, why the removed structure no longer contributes, and the check that could detect a mistaken deletion. Prefer a separate coherent removal unit when it makes the following change easier to review. If proof is weak or the cleanup is unrelated, leave it in place and proceed with the bounded task.

Cut unnecessary scope before polishing it. Design for specified and observed uses plus credible failure modes, rather than elaborate hypothetical extensions. This does not mean deleting security validation, recovery handling, accessibility, legal notices, or guards required by a real boundary. Low-frequency but high-consequence failures may be essential requirements.

For prompts or documentation, consolidate duplicate instructions while preserving unique exceptions and rationale. Remove an empty stub only after checking inbound links and its role in navigation; repair references as part of the same change. Do not remove license or attribution text as “clutter.”

## Example and counterexample

Applies: a private parser retains a disabled format with no supported files or callers. Confirm the scope, delete that branch and obsolete examples, run the remaining format fixtures, then add the requested format to the smaller parser.

Does not apply: a validator appears redundant because all current tests use valid input, but it is the only check on external payloads. Keep it and add an invalid-input case. Likewise, repository search alone cannot establish that a published API is unused.

## Evidence and stop

Report what was removed, how reachability or redundancy was established, and the preserved-behavior checks. Stop when further deletion depends on an unapproved compatibility decision or uncertain external use. File and data deletion must remain within existing authority; a design preference cannot authorize destructive cleanup.
