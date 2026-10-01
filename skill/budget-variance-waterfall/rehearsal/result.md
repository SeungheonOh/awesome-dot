# September budget review: a missing amount stays visible

Condensed result from one fictional rehearsal. September 2026 · USD · supplied amounts only. The [input packet](input.md) is reproduced for this public example; its request for a private review is part of the fictional scenario.

## Result

The plan is **$700.00**. Known spending is **$725.00**, a **$25.00 known overrun**. That is a subtotal, not complete spending. Let **x** be the missing R8 Repair amount in USD. The packet says it is nonnegative and not zero; with exact cents, x ≥ $0.01.

- Complete spending: **$725.00 + x**
- Complete signed variance: **+$25.00 + x**
- Spending is above plan by more than $25.00; its exact total and largest variance driver remain unresolved

Positive spending and negative refunds follow the [source decisions](input.md#explicit-source-decisions). Signed variance means actual minus plan. The packet does not establish a common tax-inclusion basis; these are supplied-amount calculations without invented tax adjustments. Arithmetic drivers do not establish why spending changed.

## Category comparison

An absent plan category means zero only because this fixture explicitly says so. An unknown actual amount never means zero. Percentages below are exact fractions of plan, not contribution-to-net percentages.

| Category | Plan | Actual | Signed currency variance | Variance / plan |
| --- | ---: | ---: | ---: | ---: |
| Operations | $300.00 | $295.00 | −$5.00 | −5/3% |
| Transport | $150.00 | $170.00 | +$20.00 | 40/3% |
| Supplies | $250.00 | $240.00 | −$10.00 | −4% |
| Shared | $0.00 | $0.00 | $0.00 | Not applicable: zero plan |
| Miscellaneous | $0.00 | $20.00 | +$20.00 | Not applicable: zero plan |
| Unresolved amount: Repair (R8) | $0.00 | x | +x | Not applicable: zero plan |
| **Complete total, symbolic** | **$700.00** | **$725.00 + x** | **+$25.00 + x** | **100 × (25 + x) / 700 %; unresolved** |

Source: [planned amounts](input.md#planned-amounts), [actual rows](input.md#actual-source-rows), and [explicit allocation and classification rules](input.md#explicit-source-decisions).

Known gross increases of $40.00 offset known reductions of $15.00, leaving +$25.00. Complete gross increases are $40.00 + x. Transport and Miscellaneous each add $20.00; Supplies and Operations reduce the gap by $10.00 and $5.00. Repair cannot be ranked until x is known. Contribution-to-net shares are omitted because the complete net is unknown.

## Exact text bridge

The signs, order and values match the category table. The $725.00 intermediate level is explicitly a known subtotal.

| Step | Movement | Running amount |
| --- | ---: | ---: |
| Planned total | Start | $700.00 |
| Operations | −$5.00 | $695.00 |
| Transport | +$20.00 | $715.00 |
| Supplies | −$10.00 | $705.00 |
| Shared | $0.00 | $705.00 |
| Miscellaneous | +$20.00 | $725.00, known subtotal |
| Unresolved amount: Repair | +x | $725.00 + x, complete symbolic endpoint |

**$700.00 − $5.00 + $20.00 − $10.00 + $0.00 + $20.00 + x = $725.00 + x.**

## Mapping and audit trail

Original amounts and both refund locators are retained. A zero counted contribution below excludes a copy or transfer; it does not rewrite the original amount.

| Source locator | ID | Original label and amount | Reporting treatment |
| --- | --- | --- | --- |
| Export A row 1 | R1 | Operations $280.00 | Operations $280.00 |
| Export A row 2 | R2 | Transport $170.00 | Transport $170.00 |
| Export A row 3 | R3 | Supplies $240.00 | Supplies $240.00 |
| Export A row 4 | R4 | Supplies refund −$30.00 | One underlying refund: Supplies −$30.00; also appears at Export B row 1 |
| Export B row 1 | R4 | Supplies refund −$30.00 | Confirmed copy of Export A row 4; $0.00 additional spending |
| Export B row 2 | R5 | Shared purchase $45.00 | Operations $15.00 + Supplies $30.00 = $45.00; no additional Shared expense |
| Export B row 3 | R6 | Between-wallet transfer $200.00 | Outside spending; $0.00 counted |
| Export B row 4 | R7 | Miscellaneous $20.00 | Miscellaneous $20.00 against zero plan |
| Export B row 5 | R8 | Repair, amount unknown | Repair x against zero plan; keep unresolved |

The [input](input.md#explicit-source-decisions) authorizes counting R4 once, allocating R5 and excluding R6. Matching labels or amounts alone would not justify deduplication. All four supplied plan categories are unchanged; Miscellaneous and Repair receive zero plans under the fixture rule.

## Independent reconciliation

1. Plan: $300.00 + $150.00 + $250.00 + $0.00 = **$700.00**
2. All known raw source rows, including the duplicate refund and transfer: **$895.00**. This is not spending
3. Remove the duplicate negative refund contribution and the transfer: $895.00 + $30.00 − $200.00 = **$725.00**. The +$30.00 is a deduplication adjustment, not income or another purchase
4. Unique known purchases $755.00 − one refund $30.00 = **$725.00**
5. Categories: $295.00 + $170.00 + $240.00 + $0.00 + $20.00 = **$725.00**
6. Plan plus known variances: $700.00 + $25.00 = **$725.00**. Adding the same unresolved x to every complete-spending route preserves the reconciliation

Known currency calculations have no rounding residual. There is no negative plan or exactly opposing category pair in this case; a separate arithmetic-only cancellation check is recorded in the [verification note](verification.md).

## What is complete, and what remains open

Known category amounts, duplicate treatment, split allocation, transfer exclusion and the $725.00 subtotal reconcile under the supplied rules. The complete numerical actual total, variance, overall percentage and Repair ranking do not. Tax-basis comparability remains a separate source limitation. No spending motive is supplied.

**Smallest question to finish the missing-amount calculation: What is the September R8 Repair purchase amount in USD, to the cent?**

[Input](input.md) · [Verification and limits](verification.md) · [Return to the skill](../SKILL.md)
