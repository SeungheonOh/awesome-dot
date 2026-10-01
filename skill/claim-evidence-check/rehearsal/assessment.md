# NewQueue claim assessment

Completed assessment of the [fictional source packet](input.md). Evidence cutoff: **2026-09-15 12:00 UTC**. All citations below are exact packet locators, not live links.

## Bottom line

The claim is misleading as a whole. The corrected published table supports an **aggregate mean waiting-time reduction of 38.24%**, reasonably described as “about 40%.” It contradicts a reduction for every reported case type: the mean rose from 2 to 3 minutes for Simple cases and from 8 to 9 minutes for Complex cases. The methods explicitly describe a before/after pilot without randomization or a concurrent control; the new rule’s causal effect is unresolved. [S2:R1–R4; S3:L1–L3]

**Defensible replacement:** “In the pilot’s corrected published figures, mean waiting time across the observed cases fell from 6.8 to 4.2 minutes, about 38%, as the case mix shifted toward Simple cases. Mean waits increased by one minute within both reported case types, and the uncontrolled before/after comparison does not establish that NewQueue caused the aggregate decline.”

## Claim and scope

Exact wording, preserved unchanged:

> “NewQueue cut mean waiting time by 40% for every case type, and a controlled test proved the new rule caused the improvement.”

- **Claimant and starting locator:** The exact composite claim is supplied in `input.md`, immediately below its introductory cutoff sentence. Its original author, publication time and public venue are unspecified. It is not a verbatim S1 or S4 quotation, and this assessment does not attribute it to either issuer
- **Question:** What parts of that wording can the supplied evidence support by the cutoff?
- **Population/place/period:** Observed cases in the fictional NewQueue pilot; two reported case types; 100 observations before and 100 after. Geography, eligibility, sampling frame and actual measurement dates are not supplied. These are observations, not necessarily 200 distinct people [S2:L1, R1–R4; S3:L3]
- **Permitted sources/access:** Only the supplied English-language mock excerpts, complete for this exercise. No browsing, source contact, account access or external delivery
- **Exclusions:** No inference about service-processing time, satisfaction or total journey time; no assertion about individual outcomes or the rest of the service population [S3:L3–L4]
- **Ambiguities:** S1’s “average” is not an explicit definition of mean, although the linked table provides means. “40%” can be literal or coarse rounding. “For every case type” differs materially from an aggregate result. “Cut” may describe a before/after change or assert causation; those readings are assessed separately

## Component findings

| ID | Exact words assessed | Testable proposition and metric | Status | Evidence and explanation | Alternative reading / missing evidence |
| --- | --- | --- | --- | --- | --- |
| C1 | “cut mean waiting time” | Across the pilot observations, the after-period aggregate arithmetic mean is lower than the before-period mean; minutes per observation | **Supported for the descriptive aggregate reading** | Count-weighted means are 6.8 before and 4.2 after [S2:R1–R4] | “Cut” as a causal verb is assessed in C5. Other populations and outcome measures are not established |
| C2 | “by 40%” | Aggregate relative reduction against the before-period mean | **Contradicted if literal; supported as “about 40%”** | The corrected published inputs reproduce 38.235294…%, not exactly 40%. Ordinary rounding to the nearest whole percent gives 38%; coarse rounding to the nearest ten percentage points gives 40% [S2:R1–R4] | Exact underlying precision cannot be audited without unrounded inputs/raw observations. “About 40%” appears in S1:L1; the claim omits “about” |
| C3 | “for every case type” | Each reported case-type mean fell by 40%, or at least fell | **Contradicted** | Simple increased 2→3 minutes, +50%; Complex increased 8→9, +12.5%. Both are directly inconsistent with a decrease in the same pilot periods [S2:R1–R4] | Reading this as an aggregate claim removes the universal qualifier and does not preserve the original assertion. Unreported types are unknown, but the observed counterexamples already defeat “every” |
| C4 | “a controlled test” | The evidence supporting this pilot result came from a controlled comparison | **Contradicted** | The methods state a before/after pilot, not a randomized or concurrent controlled comparison [S3:L1] | No qualifying controlled result is provided by the cutoff. S4 adds no independent test [S4:L2] |
| C5 | “proved the new rule caused the improvement” | The rule caused the observed aggregate decline, with evidence sufficient to establish that causal attribution | **Unresolved; proof is not established** | Changing case mix and concurrent staff training prevent attribution from these comparisons alone. There is no control, adjustment model or statistical test supplied [S3:L1–L2; S2:L3; S1:L3] | The packet does not prove the rule had no effect either. A matching causal comparison addressing alternative explanations would be needed; a claim of proof exceeds the evidence |

The table calculations are reproductions of supplied summary numbers, not replication of an underlying study. No uncertainty interval, significance result or outcome probability can be computed reliably from these summaries alone. [S2:L3]

## Corrected arithmetic and case mix

Each denominator is the 100 observations in its own period. The counts must weight the case-type means.

- **Before:** (20 × 2 + 80 × 8) / 100 = 680 / 100 = **6.8 minutes** [S2:R1–R2]
- **After, corrected:** (80 × 3 + 20 × 9) / 100 = 420 / 100 = **4.2 minutes** [S2:R3–R4]
- **Absolute decrease:** 6.8 − 4.2 = **2.6 minutes**
- **Relative decrease:** (6.8 − 4.2) / 6.8 × 100 = 650/17% = **38.235294…%**, displayed as **38.24%**
- **Simple:** (3 − 2) / 2 × 100 = **50% increase**, or **1 minute** [S2:R1, R3]
- **Complex:** (9 − 8) / 8 × 100 = **12.5% increase**, or **1 minute** [S2:R2, R4]

Simple cases increased from 20/100 = 20% to 80/100 = 80% of observations: **+60 percentage points**, not a 60% relative increase. They have shorter mean waits in both periods. Consequently, the aggregate can fall while both case-type means rise. [S2:R1–R4]

An illustrative fixed-mix arithmetic check applies the before-period weights to the after means: 0.2 × 3 + 0.8 × 9 = **7.8 minutes**, one minute above the before mean of 6.8. Using the after-period weights, the before means instead give 0.8 × 2 + 0.2 × 8 = **3.2 minutes**, again one minute below the actual after mean of 4.2. These are descriptive reweightings of published means, not observed new samples, individual trajectories or estimates of the rule’s causal effect.

### Version correction

The correction was public on **2026-09-14 16:00 UTC**, before the requested cutoff, so the After/Complex mean of **9** governs this assessment. The superseded value **7** would produce an after mean of (80 × 3 + 20 × 7) / 100 = **3.8 minutes** and a reduction of **44.117647…%**. That older calculation cannot be substituted for the corrected **38.235294…%**. Counts and all other cells were unchanged. [S2:L2]

The announcement and bulletin predate the correction. Their reported “about 40%” does not demonstrate use of the corrected version. Both 44.12% and 38.24% round to 40% at coarse ten-percentage-point precision, so the rounded phrase alone cannot identify which inputs were used. [S1 publication time, L1–L2; S4 publication time, L1; S2:L2]

## Audit appendix

### Source records

The supplied packet was assessed on **2026-10-01**. This assessment date is distinct from the fictional historical publication cutoff. The exercise stipulates all excerpt contents and publication dates; no external historical archive was consulted. The source records below describe coverage of the supplied excerpts, not access to external publications.

| ID | Title / issuer | Direct locator and version | Publication / update | Event or measurement period | Access coverage / role |
| --- | --- | --- | --- | --- | --- |
| S1 | Issuer announcement / unnamed NewQueue issuer | `input.md`, S1 heading, S1:L1–L3; supplied excerpt | Published 2026-09-12 09:00 UTC; no update stated | Before/after pilot; dates absent | Entire supplied excerpt read; initial issuer interpretation, not original measurements |
| S2 | Pilot table D1 / issuer not separately named | `input.md`, S2 heading, S2:L1–L3 and S2:R1–R4; corrected table plus explicit change record | Original 2026-09-12 08:00 UTC; corrected 2026-09-14 16:00 UTC | Before/after pilot; dates absent | Entire supplied corrected table and correction note read; direct summary measurements. Original full table was not separately supplied; its one changed cell is documented in S2:L2 |
| S3 | Methods note / issuer not separately named | `input.md`, S3 heading, S3:L1–L4; supplied version | Published 2026-09-12 08:00 UTC; no update stated | Same described pilot; dates absent | Entire supplied excerpt read; direct design and measurement-scope description |
| S4 | Trade bulletin / unnamed trade publisher | `input.md`, S4 heading, S4:L1–L2; supplied version | Published 2026-09-13 11:00 UTC; no update stated | Reports issuer’s pilot result | Entire supplied excerpt read; derivative reporting, no independent evidence |
| S5 | Later trial announcement / issuer not separately named | `input.md`, S5 heading, S5:L1–L2; supplied version | Published 2026-09-16 10:00 UTC; no update stated | Proposed controlled comparison “next month”; no results | Entire supplied excerpt read solely to classify chronology; excluded from historical assessment because first public after cutoff |

### Provenance edges

| From → to | Citation locator / claimed relationship | Inspected relationship | Gap or circularity |
| --- | --- | --- | --- |
| S4 → S1 | S4:L1–L2: bulletin attributes about-40%-faster wording to issuer announcement | Direct attribution confirmed; no new measurements or testing | Derivative repetition, not an independent confirmation. “Faster” is broader and less metric-specific than the measured waiting-time reduction |
| S1 → S2 | S1:L2: before/after comparison uses D1 | Supplied D1 contains counts and mean waiting times enabling aggregate arithmetic | Announcement predates correction. It does not identify a later revised calculation |
| S2 corrected → S2 superseded | S2:L2: After/Complex changes 7→9; other cells unchanged | Explicit change record supplies both values, allowing bounded reconstruction of the older calculation | Full original table is not separately inspected; no additional version history supplied |

S3 is companion design evidence identified as the methods note in the packet, not a cited reference in S1’s supplied excerpt. No citation edge to S3 is invented. The exact claim’s route to S1 is also unspecified. There is no circular citation chain in the supplied excerpts; the observable reporting chain terminates at summary table D1, with observation-level data absent.

### Calculation records

| Component | Inputs and locators | Formula / units | Before rounding → displayed | Limitation |
| --- | --- | --- | --- | --- |
| C1–C2 | Counts 20/80, means 2/8; S2:R1–R2 | Sum(count × mean)/sum(count); minutes | 34/5 → 6.8 | Summary reconstruction only |
| C1–C2 | Counts 80/20, means 3/9; S2:R3–R4 | Same; minutes | 21/5 → 4.2 | Corrected version only |
| C2 | Before 6.8; after 4.2, derived above | (before − after)/before × 100; percent reduction | 650/17% → 38.24% | Not a percentage-point change; unknown raw precision |
| C3 | 2→3; S2:R1, R3 | (after − before)/before × 100; percent increase | 50% → 50% | Group means, not within-person changes |
| C3 | 8→9; S2:R2, R4 | Same | 25/2% → 12.5% | Group means, not within-person changes |
| C2 version check | Original After/Complex 7; S2:L2, R3–R4 | Old after weighted mean; old relative reduction | 19/5 min; 750/17% → 3.8 min; 44.12% | Superseded; used only to show correction impact |
| C1/C3 scope check | S2:R1–R4 | Fixed before weights × after means; minutes | 39/5 → 7.8 | Descriptive standardization, not causal estimation |
| C1/C3 alternative check | S2:R1–R4 | Fixed after weights × before means; minutes | 16/5 → 3.2 | Same limitation |

### Conclusion record

- **Bounded answer:** The aggregate decrease is supported at about 38%; “about 40%” is a coarse approximation. Every-reported-type improvement and a controlled-test description are contradicted. Causal attribution remains unresolved
- **Supported rewording:** The replacement statement at the top preserves both the aggregate result and the opposite within-type results
- **Qualifiers restored/removed:** Restore “pilot,” “observed cases,” “corrected published figures,” “aggregate” and approximate precision; replace “every case type” with the actual increases; remove “controlled test,” “proved” and causal attribution
- **Strongest unresolved question:** What, if any, waiting-time effect is attributable specifically to NewQueue rather than changing case mix, staff training or other differences? These summaries cannot settle it
- **Cutoff:** 2026-09-15 12:00 UTC; S2’s correction is eligible and S5 is not
- **Search limits:** Only five supplied synthetic excerpts. No network search, live citations, original records, external version history, individual data, dispersion estimates or unprovided statistical analysis

### Final checks

- Rechecked the original full sentence: aggregate, universal, numerical, design and causal components are separately addressed
- Checked surrounding supplied context: S1 contains no statistical test, S2 marks a correction, S3 restricts design and outcome scope, S4 is derivative and S5 is too late
- Checked alternative readings: exact versus approximate 40%; aggregate versus per-type; descriptive versus causal “cut”; fixed before and fixed after case-mix weights
- Independently recomputed the central percentage as 100 × (1 − 4.2/6.8) = 650/17% = 38.235294…%, matching the difference-over-baseline calculation
- Verified denominators: each period totals 100; both case-type shares change; no paired-individual assumption made
- Verified contradiction scope: numerical mismatch is bounded to literal exactness using published values; case-type and design contradictions concern the same pilot. Lack of causal identification is not called proof of no causal effect
- Kept unknowns explicit: measurement dates, geography, distinct-person count, raw precision, variability, significance, individual changes and causal effects remain unestablished
