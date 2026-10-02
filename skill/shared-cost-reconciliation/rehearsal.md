# Fresh-input check: whole-yen shares and a later payment outcome

This fictional rehearsal used the workflow instructions with a different packet, without its worked example or a supplied answer. It produced and reopened a first review sheet, then a complete second version after an explicit clarification. The first file remained unchanged. The condensed input and results below retain the facts needed to inspect the arithmetic; no payment service was used.

## First packet

Participants are P1 Nora, P2 Omar, P3 Pia and P4 Quinn. JPY uses whole yen and USD uses cents in this packet; do not convert them. Weighted/equal splits use exact shares, floor to minor units, then largest remainders with tie order P1, P2, P3, P4. All statuses are supplied fictional evidence. The cutoff is September 26, 2026 at 10:00 UTC.

| Source/event | Cash evidence | Cost allocation |
| --- | --- | --- |
| A1 / J1 | Nora paid JPY 10001 | P1:P2:P3 weights 2:1:1; P4 excluded |
| A2 / J1 copy | Same event and receipt as A1 | No additional expense |
| A3 / J2 | Quinn paid JPY 900 | Omar, Pia and Quinn: 300 each |
| A4 / JR1 | Omar received JPY 1000 cash refund for one J1 item | Entire credit belongs to Pia; no proportional redistribution |
| A5 / JT1 | Completed Pia → Nora repayment, JPY 1500 | No new expense |
| A6 / JT1 copy | Same stable ID and completed payment as A5 | No additional repayment |
| A7 / J3 | Pia paid JPY 600 for supplies | Beneficiaries/split missing |
| A8 / JT2 | Submitted Omar → Quinn attempt, JPY 300 | Outcome unknown, not applied |
| A9 / U1 | Quinn paid USD 0.05 | Nora and Quinn equally |

J1's shares are 5001 / 2500 / 2500 / 0 yen. The refund reduces **Omar's cash paid** and **Pia's cost share**. Those are different roles; Nora's status as original payer does not determine either.

## First result and review questions

The allocatable JPY subset has net expense cash and shares of 9901 yen. Its remaining balances after completed JT1 are Nora +3500, Omar −3800, Pia −300 and Quinn +600. This excludes J3 from both the cash and share sides of that subset; the full source cash register still includes J3 and totals 10501 yen. The 600-yen allocation gap remains exposed.

No complete JPY proposal is justified while J3's allocation and JT2's outcome are unresolved. The workflow asked which people share J3 and what rule applies, and requested JT2's outcome at the reporting cutoff or an explicitly revised cutoff.

USD is independently complete. Nora's cost share is 0.03 and Quinn's is 0.02 under the supplied cent rule. Nora owes Quinn USD 0.03; the other participants have no USD allocation. No JPY uncertainty is used to invent a USD conversion or block this separate arithmetic.

## Supplied review update and second result

At the explicit new cutoff, 10:20 UTC, A10 assigns J3 equally to Pia and Quinn, 300 yen each. A11 establishes completed JT2 for the existing ID; A12 is a duplicate copy of that same completed record. The source history is retained, but only JT2's resolved current state enters the arithmetic once.

| Participant | JPY expense cash net of refunds | JPY cost share | Completed repayments sent / received | Remaining JPY balance |
| --- | ---: | ---: | ---: | ---: |
| Nora | 10001 | 5001 | 0 / 1500 | +3500 |
| Omar | −1000 | 2800 | 300 / 0 | −3500 |
| Pia | 600 | 2100 | 1500 / 0 | 0 |
| Quinn | 900 | 600 | 0 / 300 | 0 |
| Total | 10501 | 10501 | 1800 / 1800 | 0 |

The negative cash-paid value for Omar means he received the refund; it is not an account balance. A valid final proposal is **Omar → Nora JPY 3500**, plus the unchanged **Nora → Quinn USD 0.03**. These amounts would extinguish the supported balances within each currency. Replaying A11/A12 does not add another 300-yen payment.

## Independent check and limits

The source-to-result review separately recomputed the weighted whole-yen split, the refund's distinct recipient/beneficiary, both cutoff states, duplicate evidence and the currency-specific proposals. This small arithmetic check was run with Python 3.12.14 and exited 0:

```python
from fractions import Fraction as F

raw = [F(10001*2, 4), F(10001, 4), F(10001, 4), F(0)]
assert raw == [F(10001, 2), F(10001, 4), F(10001, 4), F(0)]
j1 = [int(x) for x in raw]
remainder_order = sorted(range(4), key=lambda i: (-(raw[i]-j1[i]), i))
for i in remainder_order[:10001-sum(j1)]:
    j1[i] += 1
assert j1 == [5001, 2500, 2500, 0] and sum(j1) == 10001
cash1 = [10001, -1000, 0, 900]
shares1 = [5001, 2800, 1800, 300]
# JT1 sent by Pia (+1500), received by Nora (-1500).
repay1 = [-1500, 0, 1500, 0]
assert [c-s+r for c, s, r in zip(cash1, shares1, repay1)] == [3500, -3800, -300, 600]
assert sum(cash1) == sum(shares1) == 9901
cash2 = [10001, -1000, 600, 900]
shares2 = [5001, 2800, 2100, 600]
repay2 = [-1500, 300, 1500, -300]  # JT2 applied once.
assert sum(cash2) == sum(shares2) == 10501
remaining = [c-s+r for c, s, r in zip(cash2, shares2, repay2)]
assert remaining == [3500, -3500, 0, 0]
remaining[1] += 3500  # Proposed Omar-to-Nora settlement, not executed.
remaining[0] -= 3500
assert remaining == [0, 0, 0, 0]
assert 3+2 == 5 and (0-3, 5-2) == (-3, 3)  # USD cents stay separate.
print('PASS: whole-yen allocation, distinct refund roles, both reviewed states and separate-currency proposals')
```

The saved/reopened Markdown sheets and unchanged first-version checksum were checked locally. No bank clearing, recipient account, fees, live spreadsheet, connected save, external sharing or payment execution was established. These two fictional input packets test the workflow's reasoning and review behavior; they are not proof for every allocation policy or data source.
