# Worked example: rate, cash timing and unknown renewals

This fictional inventory is in USD. Supplied prices already include all charges for this fixture. The review window includes October 1, 2026 and excludes October 1, 2027. No source account or provider was accessed.

## Supplied records

| ID | Neutral label | Charge | Interval | Next charge | Original calendar anchor | Rule | Note |
| --- | --- | ---: | --- | --- | --- | --- | --- |
| S1 | Writing tool | 10.00 | Monthly | 2026-10-15 | 2026-10-15 | R1 | Active |
| S2 | Reference library | 120.00 | Annually | 2027-01-10 | 2027-01-10 | R1 | Active |
| S3 | Workshop membership | 30.00 | Every 3 months | 2026-11-01 | 2026-11-01 | R1 | Active |
| S4 | Trial workspace | Unknown | Monthly after trial | 2026-11-20 | 2026-11-20 | R1 | Future price not supplied |
| S5 | Writing tool, second record | 10.00 | Monthly | 2026-10-15 | 2026-10-15 | R1 | Could be a repeated record or another seat |
| S6 | Prepaid archive | 60.00 | Annually | 2027-10-01 | 2027-10-01 | R1 | Already prepaid for the reviewed period |

The fictional source explicitly supplies each original calendar anchor above as well as rule R1: if the original billing day does not exist in a target month, use that month's last day. Always calculate from that original anchor; do not let a clipped February date permanently move subsequent billing days earlier. The anchors happen to equal the next dates in this reviewed fixture, but are separate source fields, not inferred copies. The regressions below exercise different anchor and next dates. A real inventory must obtain the provider's actual rule rather than assume R1. An unknown anchor or rule preserves the supplied next charge while leaving later dates unresolved; a mismatch flags the next date as conflicted and also stops later projection.

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

This standard-library snippet uses Python 3.10 or later and expands only the supplied fictional R1 rule, retains unknown prices and checks the period boundary. Its helper represents an anchor as a full date; real source terms may instead establish the required billing day and cycle phase without a historical signup date. It is not a general provider billing engine. Its regression cases are separate from S1–S6 and do not change the reviewed inventory totals. It never signs in or changes a subscription.

```python
import calendar
from dataclasses import dataclass
from datetime import date
from decimal import Decimal as D

start, end = date(2026, 10, 1), date(2027, 10, 1)
R1 = "original_day_clamp"

@dataclass(frozen=True)
class Record:
    ident: str
    amount: D | None
    interval: int  # Months, as supplied for this fixture.
    next_charge: date
    calendar_anchor: date | None
    recurrence_rule: str | None

records = [
    Record("S1", D("10"), 1, date(2026, 10, 15), date(2026, 10, 15), R1),
    Record("S2", D("120"), 12, date(2027, 1, 10), date(2027, 1, 10), R1),
    Record("S3", D("30"), 3, date(2026, 11, 1), date(2026, 11, 1), R1),
    Record("S4", None, 1, date(2026, 11, 20), date(2026, 11, 20), R1),
    Record("S5", D("10"), 1, date(2026, 10, 15), date(2026, 10, 15), R1),
    Record("S6", D("60"), 12, date(2027, 10, 1), date(2027, 10, 1), R1),
]

def anchored_month(anchor, offset):
    index = anchor.year * 12 + anchor.month - 1 + offset
    year, month_zero = divmod(index, 12)
    month = month_zero + 1
    return date(year, month,
                min(anchor.day, calendar.monthrange(year, month)[1]))

def recurrence_dates(record, end):
    # Preserve the supplied next date; never reconstruct earlier charges.
    dates = [record.next_charge] if record.next_charge < end else []
    assert record.interval > 0
    anchor = record.calendar_anchor
    if anchor is None or record.recurrence_rule != R1:
        return dates, "Later dates unresolved: anchor or supported rule unavailable"
    offset = ((record.next_charge.year - anchor.year) * 12
              + record.next_charge.month - anchor.month)
    if (offset < 0 or offset % record.interval != 0
            or anchored_month(anchor, offset) != record.next_charge):
        return dates, "Source conflict: next date disagrees with anchor/interval/rule"
    offset += record.interval
    while True:
        when = anchored_month(anchor, offset)
        if when >= end:
            break
        dates.append(when)
        offset += record.interval
    return dates, None

charges, unresolved = [], {}
for record in records:
    dates, issue = recurrence_dates(record, end)
    if issue:
        unresolved[record.ident] = issue  # Blocks a complete, verified period total.
    charges.extend((record.ident, when, record.amount)
                   for when in dates if start <= when < end)
assert not unresolved  # Only this fixture has all recurrence inputs resolved.
known = sum((amount for _, _, amount in charges if amount is not None), D("0"))
unknown = [c for c in charges if c[2] is None]
run_rate = sum((r.amount * D(12) / D(r.interval)
                for r in records if r.amount is not None), D("0"))
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

# Regressions: only the fictional supplied R1 rule is asserted here.
clipped = Record("T1", D("10"), 1, date(2027, 2, 28), date(2027, 1, 31), R1)
dates, issue = recurrence_dates(clipped, date(2027, 5, 1))
assert issue is None
assert dates == [date(2027, 2, 28), date(2027, 3, 31), date(2027, 4, 30)]
for anchor, rule in [(None, R1), (date(2027, 1, 31), None),
                     (date(2027, 1, 31), "another_provider_rule")]:
    missing = Record("T2", D("10"), 1, date(2027, 2, 28), anchor, rule)
    dates, issue = recurrence_dates(missing, date(2027, 5, 1))
    assert dates == [date(2027, 2, 28)] and issue.startswith("Later dates unresolved")
conflict = Record("T3", D("10"), 1, date(2027, 3, 28), date(2027, 1, 31), R1)
dates, issue = recurrence_dates(conflict, date(2027, 5, 1))
assert dates == [date(2027, 3, 28)] and issue.startswith("Source conflict")
leap = Record("T4", D("60"), 12, date(2029, 2, 28), date(2028, 2, 29), R1)
dates, issue = recurrence_dates(leap, date(2032, 3, 1))
assert issue is None
assert dates == [date(2029, 2, 28), date(2030, 2, 28),
                 date(2031, 2, 28), date(2032, 2, 29)]
print("PASS: cash totals, unknown prices, duplicate branch and separate recurrence anchors")
print("PASS: clipped next dates, unresolved rules, source conflicts and leap-year return")
```

## Questions to return with the result

- Is S5 a duplicate export record or a separate seat? No provider change is needed merely to resolve this identity
- What is S4's post-trial price, and does the supplied monthly renewal rule remain correct?
- Are the supplied terms still current for the user's actual review date? This fictional fixture does not establish live pricing

## Evidence

The exact Python snippet ran with Python 3.12.14 on 2026-10-01 and produced both stated PASS lines. The monthly values and unknown-event counts were checked against the expanded occurrences. The clipped-next-date, missing-anchor/rule, unsupported-rule, source-conflict and yearly leap-anchor checks use only the fictional supplied R1 policy; they establish no real merchant's behavior. No subscription was canceled, renewed, contacted or changed; no live price or achieved saving is claimed.

[Return to the skill](SKILL.md)
