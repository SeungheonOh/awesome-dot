---
name: principle-encode-lessons-in-structure
description: "Turn a demonstrated recurring failure into a targeted type, test, lint, or runtime guard when the rule is stable enough to enforce mechanically."
---

# Encode lessons in structure

Use this after a recurring correction or a proven class of defects. Decide first whether the lesson is a stable invariant, a contextual judgment, or a one-time exception. Recurrence is evidence worth investigating, not automatic permission to change project policy.

## Move the rule to its owning layer

1. State the failure and the rule that would have prevented it. Include a valid case the rule must continue to allow. Check whether existing types, tests, or validation already own that responsibility.
2. Prefer a representation that makes the invalid state impossible when it stays understandable. Otherwise choose a focused compiler check, lint, canonical helper, test, or runtime guard according to where the defect becomes observable.
3. Measure the guard against the failure: it must reject the reproduced bad case and accept the legitimate counterexample. A rule that catches more text but confuses valid behavior is not stronger in the useful sense.
4. Integrate at the narrowest shared boundary. Avoid copying the check into every caller. Give failures enough context for someone to fix them.
5. Keep a short rationale where the rule or exception would be surprising. Remove redundant instructions only when the mechanism really replaces them; preserve operational guidance, legal notices, and explanations of intent.

For judgment-dependent lessons, write a concrete example and decision criteria rather than a brittle automatic ban. Record unfinished enforcement work only in an agreed project location. A correction about today's task does not establish a permanent personal preference.

## Example and counterexample

Applies: multiple bugs pass an order identifier to a customer lookup. Introduce distinct validated identifier types at the existing construction boundary, update callers, and add a compile-time rejection example plus a valid lookup test.

Does not apply: a reviewer prefers a shorter explanation for one incident. Do not create a repository-wide length lint or durable communication rule from that single comment.

## Completion and authority

Report the repeated failure, chosen enforcement point, positive and negative checks, and remaining exceptions. New scheduled automation, external notifications, permission changes, or organization-wide policy require their own authority; a “learning loop” cannot supply it. If the rule's validity is disputed, propose the guard and collect a counterexample before enforcing it.
