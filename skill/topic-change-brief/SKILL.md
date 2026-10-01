---
name: topic-change-brief
description: "Compare current reporting with a prior topic brief to surface genuine developments, corrections and changed implications while preserving source versions and deduplicating underlying events."
---

# Write a Topic Change Brief

Answer “What changed since this brief, and what difference does it make?” within a named topic and time boundary. Deliver a short delta brief backed by a versioned comparison ledger. New article volume is not the outcome.

This is a temporal comparison, not a fresh audit of one claim or a product capability assessment. Check evidence sufficiently to establish the change, but do not silently expand into either neighboring task. A supplied prior brief is the baseline to compare, not unquestioned ground truth.

## Fix the comparison boundary

Record the topic, population/place or product/version where relevant, prior brief and its as-of cutoff, new cutoff with timezone, intended reader, and permitted source scope. Identify the prior brief's exact revision and its supporting source versions. Ask for a missing baseline if it materially prevents comparison; otherwise label a newly created baseline as such rather than pretending to know what the reader previously saw.

Use two different boundaries:

- **Knowledge boundary:** evidence versions publicly available by the requested cutoff; the update interval is `(prior cutoff, new cutoff]`
- **Event boundary:** when the underlying action, observation or decision happened, and any separate effective or planned date

A new correction of an old event can matter now. An old event newly discovered by this run can be important context, but must be labeled “new to this brief; occurred earlier.” Do not suppress it solely because its event date precedes the interval. Conversely, a new publication of an already-covered event is not automatically a development.

Compare like scope. An expanded geography, changed metric, different cohort or longer measurement period is a scope change until a comparable basis is established. Explain both values rather than manufacturing a trend. Keep private context out of public queries.

## Retrieve and preserve the evidence

For real use, retrieve relevant current primary reporting and official records through already-authorized read-only sources. Open the actual passages, including linked amendments or correction notices, rather than relying on headlines, snippets or search ordering. Independent firsthand reporting may supply observations unavailable in official statements; official origin alone does not establish completeness or truth.

Use a bounded search for developments likely to change the baseline's statements or implications. Record the sources queried, returned date coverage and inaccessible material. A failed or truncated read is a coverage gap, never “nothing changed.” Continue supported comparisons while identifying which conclusion that gap could affect.

For every inspected source version preserve:

```text
source ID, title, issuer/byline, direct URL and exact section/page
source role: official record, firsthand report, analysis, derivative, etc.
original publication date; update/correction date; timezone and date precision
version identifier or dated capture; retrieval time; version availability evidence
event/measurement date; separate decision, effective and planned dates where needed
relevant short excerpts or faithful paraphrases; visible scope and limitations
cited originating source/version; republication/syndication relationship
access result and inspected coverage; missing or truncated sections
```

Preserve the baseline and old evidence; do not overwrite a mutable URL's old wording with its present content. Save only the necessary excerpts and metadata, respecting source limits. A local capture identifies what was read, not its authenticity. An “updated” timestamp without a retrievable content difference establishes no substantive change by itself.

For a historical cutoff, a source retrieved later can be used only if the relevant version was demonstrably available by that cutoff. Retain later corrections in an explicitly out-of-cutoff appendix when useful, without rewriting what was knowable then. Unknown dates and unavailable historical versions remain unknown. Do not assume a date-only timestamp means midnight, or silently assign a timezone when boundary eligibility could change.

## Compare underlying developments

### Link reporting to events

Create a small event ledger, retaining every contributing source locator. Match entity, action/proposition, place, effective period and named record or decision. A common source, direct citation, explicit syndication notice or matching original passage can establish a derivative relationship. A shared topic, similar headline or nearby date cannot establish event identity.

Separate two questions: “Is this the same event?” and “Is this independent evidence?” Independent firsthand accounts may confirm the same event without creating another event. Several sites copying one bulletin are one evidence chain. Conversely, one article can contain several distinct developments, and a follow-on decision is not a duplicate merely because it concerns the same project.

Record why each event link was accepted. If identity or independence is uncertain, retain a possible-duplicate group and avoid a precise development count. Semantic event matching needs judgment; a script can check supplied identifiers and provenance links, not universally decide whether two news stories describe the same thing.

### Classify each proposition against the baseline

Use the narrowest supported label; different propositions in one source may receive different labels.

- **Unchanged:** the inspected evidence repeats an already-recorded proposition without adding relevant support or conditions. Republished old events and copied coverage often belong here
- **Confirmation:** new applicable evidence supports the same proposition. State whether this is a fresh official reaffirmation or an independent observation; copied attribution is not independent confirmation
- **New:** a newly evidenced action, result, condition or decision changes the account. If it occurred before the interval, mark it as newly learned historical context rather than a recent event
- **Correction:** a source amendment or justified reconciliation changes what the brief should say about an earlier fact. Preserve the old statement, replacement, issuer's explanation if present, and affected conclusions. A conflict without a basis for resolving it remains unresolved, not automatically a correction
- **Withdrawal:** an identifiable source retracts support for a proposition or an actor rescinds a decision/commitment. Name what was withdrawn and when. A deleted page, broken link or absence from a later summary does not establish withdrawal; retracting a report also does not by itself prove the opposite proposition

Keep **unresolved** as a status for conflicting or missing evidence, separate from the five supported change labels. A source's new assertion can be reported with attribution while its underlying truth remains unresolved. An earlier unsupported statement need not wait for a publisher's formal correction: identify the brief's own error and the evidence basis for revising it.

Do not call a corrected count a real-world increase/decrease, a revised plan a completed action, or an updated measurement for a different period a correction to the original period. Preserve the distinction between “planned,” “started,” “reported complete,” and independently observed completion.

## Write what matters

Lead with the changes that affect the reader's question. For each include:

```text
classification and concise development
prior statement + baseline locator → current supported statement + source/version
underlying event/decision date; publication/update date when the distinction matters
why it matters: direct consequence or explicitly labeled inference
remaining uncertainty and scope limits
```

Keep supporting implications proportional to evidence. Show the reasoning and relevant premise for an inference; do not turn a plausible effect into a forecast or causal fact. A correction may remove an earlier implication without establishing its opposite. Identify which prior conclusion should be retired, amended or left intact.

Add a compact “still holds” line only when useful, plus coverage gaps and the as-of cutoff. Put the source/event comparison ledger and excluded duplicates behind the brief so the reader can audit it without reading another full news summary. If nothing material changed, say “No material change found in [inspected scope] through [cutoff]” and disclose the gaps. Do not claim that nothing happened everywhere.

Save to the requested authorized destination and verify the saved artifact if a file was requested. Routine delivery requires a clear audience and purpose; preserve any additional approval requirements for sensitive or consequential communication. A one-shot brief does not authorize publication, contacting sources, recurring checks or recurring delivery. Set up recurrence only when explicitly requested, using the requested topic, recipients, cadence and notification rule, and verify the actual setup before saying it will run. Do not describe a draft schedule as active.

## Checks and stopping point

Before delivering:

1. Trace each changed statement to an inspected passage and retained source version; keep inaccessible sources out of the support chain
2. Compare original publication, update, event and effective dates; confirm relevant versions meet the knowledge cutoff
3. Review same-event clusters and derivative edges, including at least one apparent “new headline” that could be old news
4. Reconcile before/after scope and units; identify every prior conclusion changed by a correction or withdrawal
5. Check that copied coverage did not become independent corroboration, plans did not become completions, and inferences remain labeled
6. State actual checks and their limits; do not imply that provenance checks validate a source's honesty or automate editorial judgment

Stop when the bounded developments have supported classifications or explicit gaps and the useful brief is delivered. Broaden research only when it is needed within the user's scope. If a missing baseline, access limit or unresolved identity prevents a reliable comparison, identify the smallest missing input while delivering any supported portion.

## Fictional rehearsal

Read the [fictional source packet](references/fictional-source-packet.md), then the [derived brief and execution record](WORKED_EXAMPLE.md). The packet includes a prior brief, a newly published old event, derivative coverage, a real plan change, a correction, a failed read and later evidence outside the cutoff. All names, reporting and URLs are invented.

The small offline check validates only this packet's declared dates, links and editorial event assignments:

```bash
python3 scripts/check-packet.py
```

## Example requests

```text
dot, update [PRIOR BRIEF / REVISION] on [TOPIC] through [CUTOFF WITH TIMEZONE].
Keep the same [GEOGRAPHY / POPULATION / METRIC / VERSION] and use the relevant
already-authorized primary reporting and official sources. Show genuine
changes and corrections, what still holds, and what I should revise in the
prior conclusion. Distinguish publication dates from event dates, collapse
copied reporting, and make inaccessible sources visible. Return a one-shot
source-linked delta brief for [READER / DECISION].
```

```text
Reconcile [NEW SOURCE VERSION] with the prior topic brief. Explain whether
it changes an event, corrects our earlier account, withdraws a proposition,
or merely repeats existing reporting. Preserve the old wording and dates.
```
