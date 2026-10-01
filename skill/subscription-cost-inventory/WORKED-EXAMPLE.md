# Worked example: rate, cash timing and unknown renewals

This fictional inventory is in USD. Supplied prices already include all charges for this fixture. The review window includes October 1, 2026 and excludes October 1, 2027. No source account or provider was accessed.

## Supplied records

| ID | Neutral label | Charge | Interval | Next charge | Note |
| --- | --- | ---: | --- | --- | --- |
| S1 | Writing tool | 10.00 | Monthly | 2026-10-15 | Active |
| S2 | Reference library | 120.00 | Annually | 2027-01-10 | Active |
| S3 | Workshop membership | 30.00 | Every 3 months | 2026-11-01 | Active |
| S4 | Trial workspace | Unknown | Monthly after trial | 2026-11-20 | Future price not supplied |
| S5 | Writing tool, second record | 10.00 | Monthly | 2026-10-15 | Could be a repeated record or another seat |
| S6 | Prepaid archive | 60.00 | Annually | 2027-10-01 | Already prepaid for the reviewed period |

The source explicitly supplies a month-end clipping rule: if the original billing day does not exist in a target month, use that month's last day. Always calculate from the original billing anchor; do not let a clipped February date permanently move subsequent billing days earlier. A real inventory must ask for the provider's actual rule rather than assume this one.

## Expected inventory view

| ID | Monthly equivalent | Annual run-rate | Known cash charges in window |
| --- | ---: | ---: | ---: |
| S1 | 10.00 | 120.00 | 120.00 |
| S2 | 10.00 | 120.00 | 120.00 |
| S3 | 10.00 | 120.00 | 120.00 |
| S4 | Unknown | Unknown | 11 unknown-price charge events |
| S5 | 10.00 | 120.00 | 120.00 |
| S6 | 5.00 | 60.00 | 0.00 |

Known annual run-rate is 540.00; the known charge subtotal inside this window is 480.00. Neither is a complete total while S4's future price is unresolved. The difference is not an error: S6 has a continuing annual rate but its next charge falls exactly outside the window.

Keep S5 in the subtotal until the user resolves its identity. If it is a duplicate exported record, the corrected known cash subtotal becomes 360.00. That is a data correction, not achieved savings or a canceled service. If it is a separate seat, retain 480.00.

## Monthly cash view

| Month | Known charges | Unknown-price events |
| --- | ---: | ---: |
| 2026-10 | 20.00 | 0 |
| 2026-11 | 50.00 | 1 |
| 2026-12 | 20.00 | 1 |
| 2027-01 | 140.00 | 1 |
| 2027-02 | 50.00 | 1 |
| 2027-03 | 20.00 | 1 |
| 2027-04 | 20.00 | 1 |
| 2027-05 | 50.00 | 1 |
| 2027-06 | 20.00 | 1 |
| 2027-07 | 20.00 | 1 |
| 2027-08 | 50.00 | 1 |
| 2027-09 | 20.00 | 1 |

## Repeatable check

This standard-library snippet expands the supplied recurrence rules, retains unknown prices and checks the period boundary. It never signs in or changes a subscription.

```python
import calendar
from datetime import date
from decimal import Decimal as D

start, end = date(2026, 10, 1), date(2027, 10, 1)
records = [
    ("S1", D("10"), 1, date(2026, 10, 15)),
    ("S2", D("120"), 12, date(2027, 1, 10)),
    ("S3", D("30"), 3, date(2026, 11, 1)),
    ("S4", None, 1, date(2026, 11, 20)),
    ("S5", D("10"), 1, date(2026, 10, 15)),
    ("S6", D("60"), 12, date(2027, 10, 1)),
]

def anchored_month(anchor, offset):
    index = anchor.year * 12 + anchor.month - 1 + offset
    year, month_zero = divmod(index, 12)
    month = month_zero + 1
    return date(year, month,
                min(anchor.day, calendar.monthrange(year, month)[1]))

charges = []
for ident, amount, interval, anchor in records:
    assert interval > 0
    occurrence = 0
    while True:
        when = anchored_month(anchor, occurrence * interval)
        if when >= end:
            break
        if when >= start:
            charges.append((ident, when, amount))
        occurrence += 1
known = sum((amount for _, _, amount in charges if amount is not None), D("0"))
unknown = [c for c in charges if c[2] is None]
run_rate = sum((amount * D(12) / D(interval)
                for _, amount, interval, _ in records if amount is not None), D("0"))
assert known == D("480") and run_rate == D("540")
assert len(unknown) == 11
assert not any(ident == "S6" for ident, _, _ in charges)
assert sum((a for i, _, a in charges if i == "S2"), D("0")) == D("120")
assert sum((a for i, _, a in charges if i == "S3"), D("0")) == D("120")
monthly = {}
for _, when, amount in charges:
    key = when.strftime("%Y-%m")
    monthly[key] = monthly.get(key, D("0")) + (amount if amount is not None else D("0"))
# The monthly numeric column is a KNOWN subtotal; unknown-event counts stay separate.
assert sum(monthly.values(), D("0")) == known
assert monthly["2027-01"] == D("140")
corrected_if_duplicate = sum((a for i, _, a in charges
                              if i != "S5" and a is not None), D("0"))
assert corrected_if_duplicate == D("360")
assert anchored_month(date(2028, 2, 29), 12) == date(2029, 2, 28)
assert anchored_month(date(2027, 1, 31), 1) == date(2027, 2, 28)
assert anchored_month(date(2027, 1, 31), 2) == date(2027, 3, 31)
print("PASS: cash totals, unknown prices, duplicate branch and anchored dates")
```

## Questions to return with the result

- Is S5 a duplicate export record or a separate seat? No provider change is needed merely to resolve this identity
- What is S4's post-trial price, and does the supplied monthly renewal rule remain correct?
- Are the supplied terms still current for the user's actual review date? This fictional fixture does not establish live pricing

## Evidence

The exact Python snippet ran with Python 3.12.14 on 2026-10-01 and produced the stated PASS line. The monthly values and unknown-event counts were checked against the expanded occurrences. No subscription was canceled, renewed, contacted or changed; no live price or achieved saving is claimed.

[Return to the skill](SKILL.md)
