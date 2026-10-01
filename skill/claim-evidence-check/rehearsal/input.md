# Fictional claim-check packet

Assess this claim as it could be supported by information available no later than 2026-09-15 12:00 UTC:

“NewQueue cut mean waiting time by 40% for every case type, and a controlled test proved the new rule caused the improvement.”

Use only the mock source excerpts below. They are invented, complete for this exercise, and have no real URLs. Do not browse or invent live citations. Return a Markdown claim assessment with exact source locators, corrected arithmetic, claim components, uncertainty, and a short defensible replacement statement. Do not contact anyone or deliver the assessment to a third party as part of this exercise.

## S1 — issuer announcement, published 2026-09-12 09:00 UTC

S1:L1: “Our NewQueue pilot cut average waits by about 40%. Visitors across the service can expect faster handling.”
S1:L2: “The comparison uses the before and after pilot periods in table D1.”
S1:L3: “This announcement does not report sample variability or a statistical test.”

## S2 — pilot table D1, original publication 2026-09-12 08:00 UTC; corrected 2026-09-14 16:00 UTC

S2:L1: The rows below are the corrected table, with waiting time measured in minutes. Each period has 100 observations.

| Locator | Period | Case type | Count | Mean waiting minutes |
| --- | --- | --- | ---: | ---: |
| S2:R1 | Before | Simple | 20 | 2 |
| S2:R2 | Before | Complex | 80 | 8 |
| S2:R3 | After | Simple | 80 | 3 |
| S2:R4 | After | Complex | 20 | 9 |

S2:L2: The original version incorrectly showed the After/Complex mean as 7; the correction changes it to 9. Counts and all other cells are unchanged. Use the corrected version for analysis after its publication.
S2:L3: No observation-level times, dispersion estimates, uncertainty intervals or adjustment model are supplied.

## S3 — methods note, published 2026-09-12 08:00 UTC

S3:L1: This was a before/after pilot, not a randomized or concurrent controlled comparison.
S3:L2: Case mix changed between periods as shown in D1. Staff training also began during the after period.
S3:L3: There is no evidence in this packet that identical individuals were tracked across both periods.
S3:L4: The pilot measured waiting time, not service-processing time, satisfaction or end-to-end journey time.

## S4 — trade bulletin, published 2026-09-13 11:00 UTC

S4:L1: “NewQueue is about 40% faster, according to the issuer's announcement.”
S4:L2: The bulletin cites S1 and reports no new measurements or independent testing.

## S5 — later trial announcement, published 2026-09-16 10:00 UTC

S5:L1: “A new controlled comparison will begin next month.”
S5:L2: No results are reported. This source was not public by the requested cutoff.

## Output constraints

- Preserve the difference between an aggregate mean and each case type
- Distinguish the corrected table from its superseded version
- Do not invent probabilities, statistical significance, causal conclusions or individual outcomes
- A later source cannot establish what was known by the cutoff
- The answer should still be useful even where the claim is only partly assessable
