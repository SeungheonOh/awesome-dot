# Verification: corrected case-mix rehearsal

## Evidence status

One completed synthetic, supplied-packet rehearsal, assessed and independently rechecked on **2026-10-01**. Read the [fictional input](input.md) and the [completed assessment](assessment.md). All organizations, source excerpts, dates and measurements are invented; source labels are packet locators, not real citations.

The public input preserves the exact claim, complete mock sources and analytical constraints. Only the delivery wording has been generalized. The public assessment preserves the completed findings and calculations, with its opening and assessment-date record adapted for this standalone copy.

This is evidence for the bounded case below. It is not a live-source fact-check, validation of an underlying study, or a certification of behavior across connected applications, sources or other claims.

## Independently checked arithmetic

Each period has 100 observations. Counts weight the published case-type means; averaging the two means without those weights would answer a different question.

| Check | Repeatable calculation | Verified result |
| --- | --- | --- |
| Before aggregate | (20 × 2 + 80 × 8) / 100 | 6.8 minutes |
| Corrected after aggregate | (80 × 3 + 20 × 9) / 100 | 4.2 minutes |
| Corrected relative reduction | (6.8 − 4.2) / 6.8 × 100 | (650/17)% = 38.235294…% |
| Independent form of the same reduction | 100 × (1 − 4.2/6.8) | (650/17)% = 38.235294…% |
| Superseded after aggregate | (80 × 3 + 20 × 7) / 100 | 3.8 minutes |
| Superseded relative reduction | (6.8 − 3.8) / 6.8 × 100 | (750/17)% = 44.117647…% |
| Simple change | 3 − 2; (3 − 2) / 2 × 100 | +1 minute; +50% |
| Complex change | 9 − 8; (9 − 8) / 8 × 100 | +1 minute; +12.5% |
| Simple/Complex case mix | Before: 20/100 and 80/100; after: 80/100 and 20/100 | 20%/80% → 80%/20% |
| Fixed before mix, after means | 0.2 × 3 + 0.8 × 9 | 7.8 minutes |
| Fixed after mix, before means | 0.8 × 2 + 0.2 × 8 | 3.2 minutes |

The recheck used exact rational arithmetic before decimal display. The fixed-mix results are descriptive reweightings, not new observations or causal estimates.

## Interpretation and boundary checks

- **Precision:** The corrected published inputs give about 38.24%, not literally 40%. “About 40%” is a defensible coarse approximation; the unqualified figure needs that nuance. Raw-data precision is unknown. Both 38.24% and the superseded 44.12% round to 40% at ten-percentage-point precision, so that phrase does not identify which table version was used
- **Aggregate versus each type:** The lower aggregate coincides with a shift toward the shorter-wait case type. Both reported case-type means increase, directly contradicting “for every case type” in these pilot periods. Group means do not describe every individual's outcome
- **Version and cutoff:** The S2 correction was published before the 2026-09-15 12:00 UTC cutoff and governs the assessment. The old value is used only to explain the correction. S5 was published after the cutoff and is excluded; it also reports no trial results
- **Independence:** S4 repeats S1 and adds no independent measurements or testing. Its “faster” wording is broader than the measured waiting-time outcome
- **Design and causality:** S3 identifies an uncontrolled before/after comparison, changed case mix and concurrent staff training. A controlled-test description is contradicted; a causal effect attributable to the rule remains unresolved. Failure to establish causation is not evidence of zero effect
- **Metadata gaps:** The exact composite claim's author, publication time and public venue are unspecified. The supplied packet still permits the arithmetic and component assessment. Those gaps are recorded without inventing an attribution or extending the user-bounded source set

The assessment does not establish measurement dates, geography, unique-person counts, population-wide outcomes, raw-data precision, variability, significance or a causal effect. A different claim or broader source scope would need its own assessment.
