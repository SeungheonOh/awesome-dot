---
name: decision-source-brief
description: "Turn a bounded decision into a source-backed brief with explicit options, evidence gaps and the next question that could change the choice."
---

# Decision Source Brief

Help someone arrive at a useful discussion or decision with the evidence already organized. The result is a short decision brief and an inspectable source appendix, rather than a general news digest. Use this when public facts affect a concrete choice. Produce the requested artifact and complete any explicitly authorized routine handoff; the research itself does not authorize commitments or unsolicited contact.

## Establish the decision

Obtain the question, decision owner, audience, options already under consideration, must-have constraints, research cutoff and timezone. Ask for the decision deadline only when it changes which information is useful. Clarify whether the user wants a neutral comparison or a conditional recommendation against their stated criteria. Do not invent their priorities, risk tolerance or preferred outcome.

Separate sanitized decision context from search terms. Private budgets, team plans and personal circumstances can remain in the brief without appearing in external queries. Confirm any source restrictions, permitted languages and relevant jurisdiction or location. If the decision itself is unclear, ask one question that distinguishes the competing interpretations and gather only evidence useful to both in the meantime.

Use the following input record. It can be a table or a labeled object; no special software is required:

```text
decision: exact question and named options
owner_and_audience: who uses the brief, not permission to contact them
criteria: [{id, requirement, must_have_or_preference, user_supplied_priority}]
scope: subject identities, place, date window, excluded topics
cutoff: timestamp with timezone; current snapshot or historical evidence boundary
source_constraints: approved starting sources, access and language limits
private_context: facts allowed in the private result but excluded from queries
output: requested length, format, neutral comparison or conditional recommendation
```

A missing preference may remain unspecified. A missing hard constraint that reverses the comparison requires clarification.

## Build the brief

1. **Turn the decision into answerable questions.** Map each criterion to a factual question and the evidence that could answer it. Identify decision-critical questions separately from background. For example, a stated capacity requirement needs a current specification for the exact space; publicity about the building as a whole is inadequate. Give each question an identifier so irrelevant discoveries do not expand the task.

2. **Retrieve the strongest available evidence.** Open original policy documents, specifications, official notices, datasets or other primary material appropriate to the question. Retrieve them during the actual run; remembered facts and search snippets are leads, not inspected evidence. Then consult independent reporting where it adds observation, context or a genuine challenge. A first-party source can establish its issuer's stated rule but does not independently verify its performance claims. Respect restricted access and label a partial excerpt as partial.

3. **Record dates and provenance as you read.** For each source retain title, issuer, direct URL or authorized file locator, document version, publication time, update time, event/effective date, retrieval time and accessible coverage. Use “not stated” for missing dates. A page update date is not necessarily the date every sentence changed. Trace repeated claims to their underlying source so ten articles repeating one notice do not become ten independent confirmations.

4. **Apply the cutoff consistently.** For a current brief, disclose the latest retrieval time and any source older than the relevant change. For a historical brief, distinguish “what was knowable by the cutoff” from “what later evidence says about an earlier event.” Exclude later-published evidence from the former, or place it in a clearly separate hindsight note only if requested. Do not claim a mutable page represents its historical version without a dated snapshot or supplied copy.

5. **Compare each option against each criterion.** Mark a criterion supported, contradicted, conditional or unresolved, citing the exact passage, section or table. Separate a fact from your synthesis about its effect on the choice. Unknown is not a failure unless the user's criterion explicitly requires positive verification. An option that fails a documented must-have cannot be rescued by an invented weighting score. If all options lack decisive evidence, the useful result is a precise next question rather than a forced winner.

6. **Resolve consequential disagreements.** Check entity identity, geography, measurement units, document version and event date before treating sources as contradictory. Prefer evidence with direct relevance and adequate methodology, not automatically whichever source is newest or most confident. A newer summary may still repeat an older rule. When comparable primary records genuinely conflict, show both and explain which criterion remains unsettled; do not infer motives or manufacture balance between unequal evidence.

7. **Write for the actual decision.** Lead with the supported answer or the blocker. Include only background needed to understand the comparison, developments that change an option, and neutral questions for discussion. If requested, make a recommendation conditional on the user's stated criteria and spell out what new fact would change it. Do not transform an operational brief into individualized medical, legal or investment advice.

## Return these records

The brief should be readable without opening the appendix. The appendix should let another reader audit it.

```text
brief:
  decision, cutoff, scope
  answer_or_blocker
  option_comparison: [{option, criterion_id, finding, evidence_ids, condition}]
  decision_changing_unknowns: [{question, affected_options, evidence_needed}]
  next_step: a question or user decision, not an action already taken
sources:
  [{id, title, issuer, direct_locator, version, publication_time, update_time,
    event_or_effective_time, retrieval_time, access_coverage, source_type,
    originating_evidence_id}]
evidence:
  [{id, question_id, claim, source_id, exact_locator, attribution,
    support_status, limitation, assistant_inference_if_any}]
checks:
  [{check, result, evidence_or_unrun_reason}]
```

Do not invent a confidence percentage. Explain evidence strength in terms of directness, current applicability, independence, completeness and unresolved conflict.

Create the requested brief in the format and destination the user authorized. If they explicitly requested a routine delivery to a named audience, complete it using available access without asking again merely because it is a delivery. Check the saved artifact, citations and intended permissions, and verify the delivered reference or message before reporting success. A failed save or send is a specific blocker; retain the completed private artifact and report the smallest recovery step. New audiences, sensitive disclosures and consequential commitments still require the applicable authorization.

## Check before handing it over

- Open or revisit every decision-critical citation and verify that its passage supports the wording, not just the topic
- Confirm entity, location, event/effective date and research cutoff are distinct and correct
- Inspect one potentially stale source and one apparently conflicting account; record “none found in the bounded source set” when appropriate rather than inventing a conflict
- Check that an unanswered question stays open and a repeated assertion is not counted as independent evidence
- Re-evaluate the answer after temporarily removing the weakest decisive source; disclose if the conclusion depends entirely on it
- Verify that every recommended next step belongs to the stated decision and no unauthorized or unverified communication or commitment is reported as completed

Stop researching when all decision-critical questions have usable evidence or specific documented gaps, the conflicts have been investigated within scope, and more background would not change the comparison. Do not promise exhaustive research. Ask before widening the decision or taking an action without the needed authority, such as paying for access, unsolicited source contact, new sharing or future monitoring. Honor an already explicit, permitted request to save or deliver the result rather than seeking duplicate approval. If access blocks a decisive source, return the useful partial brief and the smallest missing input.

## Worked example

[The fictional venue decision](examples/fictional-venue-decision.md) supplies mock excerpts and an expected analysis. It demonstrates a decision blocked by one unverified must-have, a misleading headline and a post-cutoff update. It is an authored exercise, not evidence of a real investigation or a completed external action.
