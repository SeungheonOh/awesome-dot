# Worked example: the total stayed flat, but the categories changed

This is fictional club spending in USD. It demonstrates the calculation and review steps, not a connection to a financial account.

## Inputs

Positive actual amounts mean spending; negative amounts mean refunds. The club explicitly classifies the transfer as outside spending. A missing actual category means zero in this supplied fixture, not a general rule.

```csv
category,planned
supplies,80.00
venue,120.00
printing,30.00
transport,20.00
```

```csv
id,category,kind,amount
A01,supplies,purchase,120.00
A02,supplies,refund,-20.00
A03,venue,purchase,100.00
A04,printing,purchase,45.00
A05,unbudgeted,purchase,5.00
A06,between-wallets,transfer,50.00
```

## Expected deliverable

| Category | Planned | Actual spending | Actual minus plan |
| --- | ---: | ---: | ---: |
| Supplies | 80.00 | 100.00 | +20.00 |
| Venue | 120.00 | 100.00 | -20.00 |
| Printing | 30.00 | 45.00 | +15.00 |
| Transport | 20.00 | 0.00 | -20.00 |
| Unbudgeted | 0.00 | 5.00 | +5.00 |
| Total | 250.00 | 250.00 | 0.00 |

The text equivalent of the waterfall is:

```text
Planned 250.00
+ supplies 20.00 -> 270.00
- venue 20.00 -> 250.00
+ printing 15.00 -> 265.00
- transport 20.00 -> 245.00
+ unbudgeted 5.00 -> 250.00 actual
```

A useful conclusion is: “Total spending matches the plan, but increases of 40.00 offset reductions of 40.00. Supplies and printing are above their planned amounts. The transfer is excluded under the supplied classification.”

Do not turn that into a claim about why people spent differently. Do not show a category's share of net variance: the net is zero. The unbudgeted category also has no meaningful conventional percentage increase from a zero plan.

## Repeatable arithmetic check

The following standard-library snippet is the exact calculation checked for this example. Values use decimal currency arithmetic. It does not read accounts, write files or contact services.

```python
from decimal import Decimal as D

plan = {"supplies": D("80"), "venue": D("120"),
        "printing": D("30"), "transport": D("20")}
rows = [
    ("A01", "supplies", "purchase", D("120")),
    ("A02", "supplies", "refund", D("-20")),
    ("A03", "venue", "purchase", D("100")),
    ("A04", "printing", "purchase", D("45")),
    ("A05", "unbudgeted", "purchase", D("5")),
    ("A06", "between-wallets", "transfer", D("50")),
]
assert len({r[0] for r in rows}) == len(rows)
actual = {}
for _, category, kind, amount in rows:
    if kind != "transfer":
        actual[category] = actual.get(category, D("0")) + amount
categories = list(plan) + [c for c in actual if c not in plan]
variance = {c: actual.get(c, D("0")) - plan.get(c, D("0"))
            for c in categories}
planned_total = sum(plan.values(), D("0"))
actual_total = sum(actual.values(), D("0"))
assert planned_total == actual_total == D("250")
assert planned_total + sum(variance.values(), D("0")) == actual_total
assert actual["supplies"] == D("100")
assert "between-wallets" not in actual
assert sum((v for v in variance.values() if v > 0), D("0")) == D("40")
assert sum((-v for v in variance.values() if v < 0), D("0")) == D("40")
print("PASS: seven accounting invariants; net variance 0.00 USD")
```

## Decision branch

If A06's classification is unknown, keep it unresolved. Report confirmed spending of 250.00 plus an unresolved 50.00 entry; do not quietly report 250.00 as a complete total or assume the entry is a cost. Ask only the classification question needed to finish the comparison.

If two rows share the same ID, stop the reconciliation and ask whether one is a repeated export or a separate entry with a bad identifier. Identical amounts alone are not grounds for deduplication.

## Evidence

The Python snippet was executed with Python 3.12.14 on 2026-10-01 and produced the stated PASS line. The table, refund treatment, gross increases and reductions were checked against that result. No chart renderer, spreadsheet application or financial account was exercised. This verifies the fictional arithmetic example, not an end-to-end live budgeting workflow.

[Return to the skill](SKILL.md)
