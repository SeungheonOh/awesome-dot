# Confidence in historical explanations

A credible answer preserves the difference between a record, an interpretation of that record, and a missing answer. Confidence belongs to individual claims. A strong answer to one part of the question cannot lend certainty to an unsupported threshold or timeline.

## Five tiers

### Direct

An explicit attributable statement answers the question: a design decision says why an option was chosen, a review explains a constraint, or an author records a motivating failure. Cite the exact artifact, section or message, author if relevant, and date.

Phrase it as what the record establishes: “The design note says the queue was introduced to survive restarts.” Direct evidence of a stated intention does not establish that it was the only motivation, remained applicable, or was successfully implemented. An obsolete note may be direct historical evidence and weak evidence of today's requirement at the same time.

### Supported

Several genuinely different pieces of indirect evidence converge on an explanation. Name each contribution and the remaining uncertainty. Three documents copying the same ticket are one evidentiary lineage, not three independent confirmations.

Example: a failure report, tests introduced for that failure, and a contemporaneous review discussing recovery all point toward a reliability-driven change. Say “The evidence strongly supports...” and show the inference. Mere temporal proximity or matching vocabulary is weaker.

### Inferred

A reasonable interpretation fits the context, but the record does not explicitly establish it. Make the step visible: “The retry was added immediately after the timeout incident, so an incident response is a plausible explanation. The review does not state that connection.” Use “appears,” “suggests,” “likely,” or “consistent with” according to strength.

A mechanism that seems sensible today is not proof of original intent. Several other implementations could have served the same goal.

### Speculative

A possible explanation has thin evidence and competitors fit as well. Present it only when it helps a decision or identifies a useful next check. Say “One possibility is..., but the available record does not establish it.” Do not fill an answer with every imaginable hypothesis.

### Unknown

The relevant answer was not established. Name the question, sources searched, time window or query scope, and the precise limit. “No rationale found in the two linked reviews; team discussions were unavailable” is more useful than “Nobody documented this.” Unknown is a legitimate result.

## Causal language requires support

“Because,” “the team decided,” “was designed to,” and “fixed” carry different proof obligations. A source may prove a decision was stated; runtime evidence may prove an observed outcome; neither alone proves both. “Merged” means the merge was observed, not release or deployment. “Resolved” is a tracker state until behavior has been checked.

Keep qualifiers that encode evidence. Editing “may have addressed the incident” into “addressed the incident” changes the claim, not just the style. Avoid “obviously,” “clearly,” and flattering agreement as substitutes for proof.

## Counter the tidy-story bias

Do not assume the current design was deliberate or optimal. Copying a neighboring pattern, migration constraints, temporary workarounds, or mistaken premises can explain code too, but each needs evidence. Do not assume a user-proposed explanation is right merely because it sounds reasonable.

Ask what you would expect to observe if the favored explanation were false. For a performance rationale, a relevant benchmark or explicit design discussion discriminates better than a function name. For an incident fix, a linked action item is stronger than a coincidental decline in errors.

## Contradictory records

Present both sources with dates and scope. A ticket can describe a business trigger while a review describes the implementation tradeoff; those may be complementary. A superseded draft can disagree with the accepted design without making both equally authoritative. If the record does not resolve the conflict, keep it unresolved rather than choosing the cleaner story.

Do not reduce every answer's confidence merely because some unrelated source was unavailable. Tie gaps to the claims they affect. Conversely, a direct statement in one source does not erase a material contradictory statement elsewhere.

## Null results and coverage

A completed query returning no matches can establish a narrow null result. It cannot establish “no incidents ever occurred.” Retention expiry, sampling, changed names, permissions, incomplete exports, and time-zone mismatch may limit the result. Record these where relevant. Unsearched is distinct from searched-empty.

## Final calibration

For each consequential claim ask:

1. What exact evidence supports it, and at which revision or time?
2. Is it observed behavior, stated intent, or inference?
3. Does the wording match the strength of that evidence?
4. Is any source duplicated, stale, superseded, or contradicted?
5. What missing evidence would change the answer?

Move unsupported claims to a qualified interpretation or omit them. Do not invent a gap merely to satisfy a section template if the narrow question really was answered.
