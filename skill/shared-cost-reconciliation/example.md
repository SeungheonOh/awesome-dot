# Fictional review loop: a shared workshop purchase

Every participant, receipt and payment record here is invented. The output is a balance proposal, not a statement that real money is owed or paid. No payment service or connected account was accessed.

## Supplied request and rules

Prepare a private shared-cost ledger for three supplied participant IDs: P1 Ari, P2 Bo and P3 Cleo. Keep USD and EUR separate; both use cents in this fixture. Include gross receipt amounts as supplied, without adding tax. Do not initiate payments or share the ledger.

Equal splits use largest fractional remainder after flooring to cents, with ties resolved in the fixed order P1, P2, P3. A full reversal cancels its original recorded shares. Apply only completed repayments. Pending or failed attempts remain in the evidence register, not the repayment total.

### Initial packet: version 1, September 25 at 09:00 UTC

| Source/event | Evidence and cash direction | Allocation rule |
| --- | --- | --- |
| S1 / E1 | Ari paid USD 100.01 for the room | Equal shares among P1, P2, P3 |
| S2 / E1 copy | Another copy of the same receipt/event E1 | Corroboration only; adds no cost |
| S3 / E2 | Bo paid USD 45.00 for snacks | P1:P2 weights 1:2; Cleo does not share this item |
| S4 / E3 | Cleo paid USD 30.00 for a personal supply item included for reconciliation | P3 only |
| S5 / R1 | Cleo collected a USD 6.00 cash refund for E2 | Explicit credits: USD 2.00 to P1's cost share, USD 4.00 to P2's; Cleo received the cash but receives no cost-share credit |
| S6 / T1 | Completed repayment: Bo → Ari, USD 10.00; transaction ID T1 | Balance adjustment only, not an expense |
| S7 / T1 copy | The recipient's matching copy of completed T1 | Adds no second repayment |
| S8 / E4 | Ari paid USD 12.00 for labels | Beneficiaries and split are not supplied |
| S9 / T2 | Pending attempted repayment: Cleo → Ari, USD 5.00 | Outcome unresolved; do not apply or duplicate it |
| S10 / E5 | Cleo paid EUR 9.00 for a separate shared item | Equal shares among P1, P2, P3 |

The receipt and repayment IDs above are supplied identity evidence. Matching labels or amounts alone did not establish the duplicates. “Completed” and “pending” are statuses from the fictional packet, not independently observed bank outcomes.

## First useful result

E1 allocates USD 33.34 / 33.34 / 33.33 under the stated cent rule. E2 allocates USD 15.00 / 30.00 / 0.00. E3 allocates USD 0.00 / 0.00 / 30.00. R1 reduces P1/P2 shares by 2.00/4.00, but reduces **Cleo's** net cash paid by 6.00. Subtracting the refund from Bo's cash merely because Bo paid E2 would be wrong.

The known USD cost-allocation subset is 169.01. E4 adds another known cash outlay of 12.00, giving 181.01 source net expense cash, but its allocation remains unknown. The difference is exposed rather than assigned to an arbitrary person.

| Participant | Known-subset expense cash paid, net of refunds | Known cost share | Completed repayments sent / received | Known-subset remaining balance |
| --- | ---: | ---: | ---: | ---: |
| P1 Ari | 100.01 | 46.34 | 0.00 / 10.00 | +43.67 |
| P2 Bo | 45.00 | 59.34 | 10.00 / 0.00 | −4.34 |
| P3 Cleo | 24.00 | 63.33 | 0.00 / 0.00 | −39.33 |

Positive means receive; negative means owe. This table intentionally excludes E4's cash **and** allocation, so its zero-sum result describes only the known subset. It is not the complete USD balance or a ready transfer list. The full cash register still retains E4 and the pending T2 attempt.

The separate EUR ledger is complete under the packet: Ari owes EUR 3.00, Bo owes EUR 3.00, Cleo should receive EUR 6.00. A EUR-only proposal is Ari → Cleo 3.00 and Bo → Cleo 3.00. No USD/EUR conversion or cross-currency cancellation is used.

Two decisions remain for USD: which participants share E4 and by what rule; and what happened to T2. The existing evidence can be saved as a provisional private draft without waiting for those answers. No reminder, group message or payment is implied.

## The review changes the result

At 09:15 UTC the user supplies **S11**, an explicit clarification: E4 belongs equally to Ari and Bo, USD 6.00 each; Cleo is excluded. This resolves E4. Recomputing the whole USD ledger gives +49.67 / −10.34 / −39.33. T2 is still pending, so the draft must not suggest duplicating Cleo's attempted payment.

At 09:20 UTC, **S12** supplies a later status record for the same T2 ID: the attempt failed and no money moved. This is an explicit outcome update, not an inference from silence or a newer arbitrary export. Retain both statuses in the review trail. T2 contributes no completed repayment; no second transfer is created by importing S12 again.

### Reviewed version 3 at 09:25 UTC

| Participant | Full USD expense cash paid, net of refunds | Full USD cost share | Completed repayments sent / received | Remaining USD balance |
| --- | ---: | ---: | ---: | ---: |
| P1 Ari | 112.01 | 52.34 | 0.00 / 10.00 | +49.67 |
| P2 Bo | 45.00 | 65.34 | 10.00 / 0.00 | −10.34 |
| P3 Cleo | 24.00 | 63.33 | 0.00 / 0.00 | −39.33 |
| Total | 181.01 | 181.01 | 10.00 / 10.00 | 0.00 |

One valid proposal is Bo → Ari **USD 10.34** and Cleo → Ari **USD 39.33**. The EUR proposal remains unchanged. This extinguishes the supported balances in each currency; it is not a claim about minimum transaction count, fees, verified recipient accounts or actual payment execution. Payment methods and any fees remain outside the supplied arithmetic.

## Repeatable arithmetic and source-boundary checks

Run this Python 3 block locally. It uses integer cents and exact fractions, writes nothing and contacts no service. Event identity, statuses and split rules are explicit transcriptions of the packet, not automatically inferred from receipt images.

```python
from fractions import Fraction

people = ('P1', 'P2', 'P3')

def allocate(amount, weights):
    assert amount >= 0 and all(w >= 0 for w in weights.values())
    assert set(weights) <= set(people) and sum(weights.values()) > 0
    exact = {p: Fraction(amount * weights.get(p, 0), sum(weights.values())) for p in people}
    result = {p: int(exact[p]) for p in people}
    remaining = amount - sum(result.values())
    order = sorted(people, key=lambda p: (-(exact[p] - result[p]), people.index(p)))
    for p in order[:remaining]:
        result[p] += 1
    assert sum(result.values()) == amount
    return result

equal = dict.fromkeys(people, 1)
e1 = allocate(10001, equal)
assert e1 == {'P1': 3334, 'P2': 3334, 'P3': 3333}
assert allocate(10001, dict(reversed(list(equal.items())))) == e1
e2 = allocate(4500, {'P1': 1, 'P2': 2})
e3 = {'P1': 0, 'P2': 0, 'P3': 3000}
refund_shares = {'P1': -200, 'P2': -400, 'P3': 0}
assert sum(refund_shares.values()) == -600
shares = {p: e1[p] + e2[p] + e3[p] + refund_shares[p] for p in people}
# R1's cash recipient is P3; it must not be guessed from original payer P2.
cash = {'P1': 10001, 'P2': 4500, 'P3': 3000-600}
assert sum(cash.values()) == sum(shares.values()) == 16901

repayments = [('T1', 'P2', 'P1', 1000, 'completed'),
              ('T1', 'P2', 'P1', 1000, 'completed'),
              ('T2', 'P3', 'P1', 500, 'pending')]

def balances(cash, shares, events):
    result = {p: cash[p] - shares[p] for p in people}
    seen = {}
    for event, sender, receiver, amount, status in events:
        record = (sender, receiver, amount, status)
        if event in seen:
            assert seen[event] == record  # Conflicting versions need reconciliation first.
            continue
        seen[event] = record
        if status == 'completed':
            result[sender] += amount
            result[receiver] -= amount
    assert sum(result.values()) == 0
    return result

initial = balances(cash, shares, repayments)
assert initial == {'P1': 4367, 'P2': -434, 'P3': -3933}
# A wrong refund recipient can still conserve the group total.
wrong_cash = dict(cash, P2=cash['P2']-600, P3=cash['P3']+600)
wrong = balances(wrong_cash, shares, repayments)
assert sum(wrong.values()) == 0 and wrong != initial
assert wrong == {'P1': 4367, 'P2': -1034, 'P3': -3333}
assert sum(cash.values()) + 1200 - sum(shares.values()) == 1200  # E4's held allocation.
full_cash = dict(cash, P1=cash['P1']+1200)
full_shares = dict(shares, P1=shares['P1']+600, P2=shares['P2']+600)
assert full_shares == {'P1': 5234, 'P2': 6534, 'P3': 6333}
assert sum(full_cash.values()) == sum(full_shares.values()) == 18101
stage2 = balances(full_cash, full_shares, repayments)
assert stage2 == {'P1': 4967, 'P2': -1034, 'P3': -3933}
# The actual workflow retains history; the arithmetic receives resolved current states.
resolved = [x for x in repayments if x[0] != 'T2'] + [('T2', 'P3', 'P1', 500, 'failed')]
assert balances(full_cash, full_shares, resolved) == stage2
assert balances(full_cash, full_shares, resolved + [resolved[-1]]) == stage2
proposal = [('P2', 'P1', 1034), ('P3', 'P1', 3933)]
after = stage2.copy()
for sender, receiver, amount in proposal:
    assert amount > 0
    after[sender] += amount
    after[receiver] -= amount
assert after == dict.fromkeys(people, 0)
# Hypothetical completion of pending T2 is a separate counterfactual, not the recorded result.
completed_t2 = [x for x in repayments if x[0] != 'T2'] + [('T2', 'P3', 'P1', 500, 'completed')]
assert balances(full_cash, full_shares, completed_t2) == {'P1': 4467, 'P2': -1034, 'P3': -3433}
# Separate hypothetical: owing 100 cents then paying 300 reverses the balance.
assert balances({'P1': 100, 'P2': 0, 'P3': 0},
                {'P1': 0, 'P2': 100, 'P3': 0},
                [('OVER', 'P2', 'P1', 300, 'completed')]) == {'P1': -200, 'P2': 200, 'P3': 0}
eur_cash = {'P1': 0, 'P2': 0, 'P3': 900}
eur_shares = allocate(900, equal)
assert balances(eur_cash, eur_shares, []) == {'P1': -300, 'P2': -300, 'P3': 600}
print('PASS: cent allocation, cash/refund direction, duplicate repayments, held split, review correction, pending/failed distinction and separate currencies')
```

## Observed checks and limits

The block was run with Python 3.12.14: exit 0 and the stated PASS line. A separate source-to-table review checked the refund recipient, each participant's beneficiary rule, the known-subset label, the status updates and both final proposals. Those semantic mappings are supplied to the code; its conservation identities alone cannot establish them. A balanced ledger can still allocate money to the wrong person. The small overpayment assertion is a separate hypothetical check of balance direction, not an additional event in the example ledger.

The example does not establish bank clearing, recipient identity, fees, exchange rates, receipt authenticity, native workbook behavior, remote save/readback, sharing or payment execution. The three fictional review versions demonstrate how the output changes when evidence arrives; no real person was asked or contacted.
