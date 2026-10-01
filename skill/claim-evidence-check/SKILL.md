---
name: claim-evidence-check
description: "Trace one precise public claim to its underlying evidence, reproduce checkable arithmetic and return a component-level assessment with defensible wording."
---

# Claim Evidence Check

Use this skill when a consequential statistic, quotation or factual assertion is circulating without enough context. Its outcome is an evidence chain and a carefully bounded assessment of the exact claim. It is not a verdict on a person, institution or entire debate.

## Capture the claim before investigating

Capture the exact wording, the supplied starting locator and the user's question about it. Keep the quotation unchanged in the input record. Separate the author who made the claim from someone who merely quoted it. Establish population, geography, measurement period and the as-of cutoff where available. Ask for the starting source if the claim could refer to different events or versions.

When the user bounds the assessment to a supplied packet, that packet can be the starting source. Record unknown claimant, publication time or venue as evidence gaps rather than forcing external lookup. If missing identity materially changes the proposition being assessed, ask for the needed clarification or mark the affected component unresolved within the permitted scope. Do not invent attribution or expand the source set without authorization.

```text
claim_input:
  exact_wording
  claimant_and_starting_locator
  claim_publication_time
  proposed_population_place_period
  question_to_resolve
  cutoff_with_timezone
  permitted_sources_languages_and_access
  scope_exclusions
```

An ambiguous word such as “average,” “safe,” “available” or “doubled” may require multiple interpretations. Record the plausible meanings before choosing one. Ask if the difference changes the conclusion; otherwise assess both explicitly. Do not silently weaken the claim into an easier one to support.

## Trace and test

1. **Decompose the assertion.** Give each independently checkable component an identifier. Identify quantity, unit, denominator, comparison baseline, population, period and any causal or universal wording. A sentence can contain a correct number and an unsupported explanation. Preserve those as separate components rather than letting one decide the whole verdict.

2. **Open the starting source.** Retrieve the actual page, recording, transcript or authorized file during the run. Record title, issuer, direct locator, publication/update times, retrieval time and accessible coverage. Inspect surrounding context, including figure captions and notes. A search-result excerpt, screenshot fragment or secondhand quotation may support only a narrower check. Do not describe unavailable full text as read.

3. **Follow the evidence chain toward its origin.** Open cited reports, datasets, statements or recordings until reaching direct evidence or a specific access gap. Record every edge: which source cites which, the passage making the connection and whether the citation actually supports that use. Detect circular chains and syndicated copies. An article quoting another article is not a second measurement. Separate original data from the authors' interpretation and subsequent reporting.

4. **Verify identity and chronology.** Match versions, report identifiers, speakers, place names and study populations. Keep event or data-collection dates separate from publication, update and retrieval dates. Check for a correction that changes the relevant figure or qualifier. A later publication may describe an earlier event, but a historical “known by” cutoff excludes evidence first available afterward. If an undated live page lacks a historical snapshot, mark historical wording unverified rather than assigning it an invented date.

5. **Reproduce only what the inspected inputs allow.** For a percentage, show numerator, denominator and units. Relative change is (new − old)/old; percentage-point change is new percentage minus old percentage. A change from 20% to 30% is ten percentage points and a 50% relative increase. An old value of zero does not support that relative-change formula. Check mean versus median, counts versus rates, nominal versus adjusted values, and whether rounding could explain a small discrepancy. Missing raw data can prevent checking an aggregate; label any arithmetic as reproduction of published numbers, not replication of the underlying study.

6. **Assess nonnumeric claims on matching scope.** For quotations, inspect the original passage or timestamp and restore qualifiers through concise paraphrase. For causal language, examine whether the design supports a causal inference rather than merely a before/after difference. For “all,” “never” or “the first,” identify what universe the source actually covers. Limited supporting examples do not establish a universal claim; failure to find a counterexample does not prove it either.

7. **Resolve competing interpretations and evidence.** Check whether apparently conflicting sources use different denominators, windows, versions or meanings. Apply the most relevant direct evidence, explaining why, instead of averaging incompatible measurements or counting citations as votes. Treat a correction as a versioned source update, not proof of bad intent. If comparable sources remain inconsistent, identify the exact unresolved component and the evidence needed to settle it.

8. **Write the strongest defensible conclusion.** Mark each component supported, contradicted or unresolved and explain its scope. “Contradicted” requires incompatible evidence about the same proposition; a narrower study alone usually means the broader claim is unestablished. Separate a source misquotation from the question of whether the underlying proposition might independently be true. Offer a revised sentence that the inspected evidence supports and list the consequential qualifiers restored or removed.

## Make the assessment auditable

Use these record shapes in the returned appendix. Keep the front-page conclusion short enough to be understood without reading the entire chain.

```text
source:
  id, title, issuer, direct_locator, version, publication_time, update_time,
  event_or_measurement_period, retrieval_time, access_coverage, source_role
provenance_edge:
  from_source, to_source, citation_locator, claimed_relationship,
  inspected_relationship, gap_or_circularity
component:
  id, exact_words, testable_proposition, population_place_period,
  metric_units_baseline, evidence_locators, status, explanation,
  alternative_reading, missing_evidence
calculation:
  component_id, input_values_and_locators, formula, units,
  result_before_rounding, displayed_result, limitation
conclusion:
  bounded_answer, supported_rewording, changed_qualifiers,
  strongest_unresolved_question, cutoff, search_limits
checks:
  [{check, observed_result_or_unrun_reason}]
```

Use direct links and specific page, table, paragraph or recording locators. Quote sparingly; an evidence trail should not reproduce an entire copyrighted source. Explain confidence through evidence quality and applicability rather than unsupported numerical scores.

Produce the requested assessment as an actual message or artifact. Save it to the specified authorized destination, and complete explicitly requested routine delivery where the audience and purpose are clear. Inspect the saved content and verify the returned delivery reference; do not report a draft as sent or an unverified file as available. Reuse existing authorization for that bounded action. If delivery introduces new sensitive information or a consequential allegation, follow the applicable approval requirement rather than treating routine sharing permission as sufficient.

## Verify and stop

Revisit the original wording after drafting the conclusion. Check a shortened quote against its surrounding context, inspect a plausible alternative reading, and independently recompute the central arithmetic if inputs permit. Confirm that updated versions and changed denominators are visible. Verify every “contradicted” label against matching scope and ensure every unknown remains unknown.

Stop when each component has a defensible status or an identified evidence gap, not when every search result has been read. State the search boundaries, including inaccessible material. Ask before extending to another claim or taking an action lacking the needed authorization, including paid access, source contact, a consequential accusation or recurring checks. Do not ask again for an already authorized routine artifact handoff whose scope and audience remain unchanged. Allegations about identifiable people require especially careful attribution; do not infer character or motive. Keep high-stakes personal advice outside this public-evidence assessment.

## Worked example

[The fictional processing-time claim](examples/fictional-processing-time-claim.md) includes mock reporting, original numbers, a correction and expected calculations. It tests median-versus-mean confusion, revised evidence, missing populations and causal overstatement. It contains no real-source claims and does not represent an executed fact-check.

## Completed synthetic rehearsal

The [corrected case-mix input](rehearsal/input.md), [completed assessment](rehearsal/assessment.md) and [verification note](rehearsal/verification.md) record one completed supplied-packet rehearsal. It checks count-weighted means, an eligible correction, aggregate versus case-type changes, approximate numerical wording, derivative reporting and an as-of cutoff. The arithmetic was independently rechecked. All sources are fictional; this evidence does not establish live-source access, underlying-study validity or performance across connected applications.
