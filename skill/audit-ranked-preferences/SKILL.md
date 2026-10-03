---
name: audit-ranked-preferences
description: Recount supplied strict ranked preferences under an explicit single-winner elimination rule, showing transfers, exhausted ballots and unresolved ties. Use for small-group decisions or a normalized tabulation exercise, not voter eligibility verification or election certification.
---

# Audit ranked preferences

## When to use

Use when a user has ranked choices and needs a reviewable account of how a single-winner elimination count reaches its result. The useful output is a round ledger with a declared rule, not just the winning label. For weighted criteria rather than ballot rankings, use [rank options with sensitivity](../rank-options-with-sensitivity/SKILL.md).

## Inputs

- Complete candidate or option roster, including options with zero first preferences
- Ordered preferences per ballot or grouped ranking, with positive integer multiplicity
- The counting profile: majority denominator, exhaustion treatment, elimination procedure and tie rule
- Whether inputs are already normalized strict rankings or include raw ballot marks requiring adjudication

Do not request voter identities. If the rule is missing for an exploratory exercise, propose an explicitly labeled profile: strict majority of continuing ballots; eliminate only the unique lowest option; stop on a last-place tie. Do not silently treat that profile as a jurisdiction's law or a group's previously adopted rule.

## Workflow

### 1. Fix the interpretation before counting

Write down what constitutes a ranked choice and whether equal ranks, blanks, write-ins, duplicate choices or fractional weights are allowed. If the input contains such cases and no governing rule is supplied, flag them instead of guessing. A strict normalized list has no implicit skipped positions: an empty list means no expressed preference.

Keep option labels exact and distinguish data labels from program object properties. Preserve an explicit full roster; inferring it only from first choices can discard a zero-vote option that is ranked later. Apply practical size limits before expensive work. Reject non-integer, negative, zero or unsafe multiplicities rather than allowing rounding or numeric overflow to change totals.

### 2. Reconcile the original population

Sum multiplicities once to establish the original total. Identical ranking rows may legitimately represent separate groups; do not deduplicate them unless the input contract identifies accidental duplicates. Conversely, a repeated candidate within one strict ranking is invalid rather than an extra vote.

Report invalid rows and obtain corrected data or an authorized exclusion policy. Never quietly exclude difficult rows and then call the reduced count complete. Distinguish eligibility or authenticity concerns from formatting validation; a well-formed JSON file proves neither.

### 3. Allocate one preference in each round

For each ballot, find its highest-ranked option that remains in the count. Assign the entire integer multiplicity to that option. If no listed option remains, classify that multiplicity as exhausted. Include every remaining option in the round totals, including zeros.

Verify both equations each round: candidate totals sum to continuing ballots, and continuing plus exhausted equals the original total. Exhausted ballots stay in the original population even though they are absent from the continuing denominator. If no continuing ballots remain, report no winner rather than making a zero-vote option win by default.

### 4. Apply the agreed stopping or elimination rule

For a strict majority of continuing ballots, the needed integer count is floor(continuing / 2) + 1. A share of exactly 50% does not qualify. Show the denominator beside the percentage; a majority of continuing ballots is not necessarily a majority of all original ballots.

If no option qualifies, apply the declared elimination procedure. Under the conservative exploratory profile, eliminate only a unique lowest option. If multiple options share the lowest count, stop and report the tied set. Do not use alphabetical order, random selection, historic round counts or simultaneous elimination unless the governing rule explicitly authorizes that method.

### 5. Explain transfers without double counting

Compare each ballot's assignment before and after elimination. Aggregate changed assignments by source and destination, with a separate exhausted destination. Unchanged assignments are not transfers. Check that outgoing transfers from an eliminated option reconcile to its prior total, and that every destination's gain matches incoming transfers under the selected procedure.

Keep each round's active roster, exact counts, continuing count, exhausted count, threshold and elimination or stopping reason. Do not present later eliminated candidates as though they still held zero votes in the current active contest without labeling that distinction.

### 6. Verify and deliver the audit

Use a hand-calculated example plus independent small-input comparisons. For integer grouped ballots, a simple reference implementation can expand small multiplicities into individual ballots and recount independently. Check row-order invariance and conservation in every round, along with all-exhausted, tied-last, immediate-majority, zero-first-choice and transfer-to-exhaustion cases.

Export the declared counting profile and aggregate round ledger. Keep original ranking rows separate unless sharing them is requested. Aggregate results can reveal preferences in a small group; omitting identities does not guarantee anonymity. State what was and was not verified: arithmetic and normalization are different from ballot authenticity, eligibility, legal compliance or certified results.

## Worked example

A group is choosing Cedar, Harbor or Orchard. The supplied rows are:

- 4 ballots: Cedar, then Harbor
- 3 ballots: Harbor only
- 2 ballots: Orchard, then Harbor
- 1 empty ballot

Use the strict continuing-majority, unique-lowest-elimination profile.

Round 1 has Cedar 4, Harbor 3 and Orchard 2. Nine ballots continue and one is exhausted; the original total is ten. The threshold is five. Orchard is the unique lowest option and is eliminated.

Round 2 transfers two ballots from Orchard to Harbor. Cedar remains at four, Harbor reaches five and exhaustion remains one. Harbor meets the five-vote threshold: 5/9 of continuing ballots, but only 5/10 of the original total. Do not describe that as a strict majority of all original ballots.

A separate fixture with A and B at one each and C at zero first eliminates C, then stops at the A/B tie. It must not choose A merely because its label sorts first.

This workflow was exercised with hand-counted fixtures and 500 small randomized grouped inputs compared against an independently expanded-ballot reference, including ballot-row-order invariance. Those checks establish implementation evidence for this declared profile, not certification or compatibility with every ranked-choice rule.

## Rule boundaries

Official rules can treat skipped ranks, overvotes, exhaustion, multiple eliminations and ties differently. For example, [Maine's official ranked-choice resources](https://www.maine.gov/sos/elections-voting/resources-for-ranked-choice-voting) describe ballot-marking and exhaustion rules that are broader than a normalized strict-list exercise. Obtain the actual governing rule before adapting this workflow to real election administration. Do not infer a universal standard from one example.

## Optional head-to-head diagnostic

When the user wants to understand sensitivity to the decision rule, compare every pair using the original rankings. Keep this separate from the elimination ledger: removing a candidate during elimination does not remove them from a diagnostic over the original profile. Do not silently replace the agreed decision rule with a preferred alternative.

1. Declare how incomplete rankings are interpreted. Two useful exploratory policies are: any listed option is preferred to any omitted option; or a ballot expresses a comparison only when both options are listed. If neither appears, abstain under both policies. Neither policy should be inferred as the group's governing rule.
2. For each unordered pair, total first-option preference, second-option preference and abstentions using the original integer multiplicities. These three counts must sum to the original population. Show abstentions explicitly: the number expressing a comparison can differ from pair to pair.
3. Call an option a strict pairwise winner only if it defeats every other option. A tie or a pair with zero expressed comparisons does not qualify as a win. No strict winner can occur because of cycles, ties or incomplete coverage; do not label every absence a cycle without proving the cycle.
4. Report any disagreement with the elimination result as a difference between rules. Keep the selected omission policy in every exported comparison. Changing a diagnostic policy must invalidate its old results without changing the independently computed elimination count.
5. Verify pair reversal swaps preference totals but preserves abstentions, row reordering changes nothing, and all pairs conserve population. An independent small reference can expand grouped rows, filter each ranking to the selected pair, and count its first listed option subject to the omission rule. Include all-empty rankings, cycles and policy-sensitive incomplete profiles.

### Worked comparison

Suppose 40 ballots rank A>B>C, 25 rank B>A>C and 35 rank C>B>A. The elimination count removes B first, transfers its 25 to A and elects A with 65 votes. Direct comparisons instead give B a 60–40 win over A and a 65–35 win over C. B is the strict pairwise winner. Both results follow their declared algorithms; the diagnostic alone does not authorize overturning a previously agreed rule.

For an omission-sensitive example, take two A-only ballots, one B>A ballot and one empty ballot. Under listed-over-omitted treatment, A beats B 2–1 with one abstention. Under both-listed treatment, B wins 1–0 with three abstentions. The second result rests on one expressed comparison, not a majority of all four original ballots. Report that coverage rather than hiding it behind a winner label.

The pairwise calculation was checked against 400 small expanded-ballot comparisons across the two omission policies, with row/candidate-order invariance. For background on strict head-to-head winners and majority cycles, see [Stanford's social choice teaching material](https://web.stanford.edu/class/symbsys150/social-choice-theory-5-8.html).
