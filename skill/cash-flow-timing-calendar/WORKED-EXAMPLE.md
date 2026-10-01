# Worked example: a comfortable month can still dip below zero

All entries below are fictional USD amounts. The horizon is October 2026 in UTC. The opening balance is 300.00 immediately before October 1. A warning means strictly below 0.00; equality does not trigger it.

## Event register

These are expected cash-movement dates, not invoice creation dates. Date certainty is an explicit assumption for the baseline.

| ID | Movement date | Direction | Amount | Meaning |
| --- | --- | --- | ---: | --- |
| E1 | 2026-10-02 | Out | 450.00 | First bill |
| E2 | 2026-10-03 | In | 1,000.00 | First receipt |
| E3 | 2026-10-03 | Out | 800.00 | Second bill |
| E4 | 2026-10-10 | Out | 100.00 | Third bill |
| E5 | 2026-10-15 | In | 800.00 | Second receipt |
| E6 | 2026-10-20 | Out | 200.00 | Fourth bill |
| E7 | 2026-11-01 | Out | 150.00 | Outside the October horizon |

A real workflow would retain source references and uncertainty for each date. This fixture supplies no account, payment instructions or real personal data.

## Expected baseline

With the October 3 receipt processed before its bill:

| Date or unchanged interval | Closing balance |
| --- | ---: |
| October 1 | 300.00 |
| October 2 | -150.00 |
| October 3–9 | 50.00 |
| October 10–14 | -50.00 |
| October 15–19 | 750.00 |
| October 20–31 | 550.00 |

The grouped display is concise; the calculation below retains all 31 daily rows, including quiet days.

- The earliest modeled warning is October 2
- The minimum daily closing balance is -150.00
- The October closing balance is 300.00 + 1,800.00 − 1,550.00 = 550.00
- E7 remains in the boundary register and contributes nothing to October

This is a statement about the supplied arithmetic, not a recommendation to borrow, pay late or move funds.

## Three questions that change the interpretation

1. **What if the October 3 bill settles before the receipt?** Its day still closes at 50.00, but the within-day balance first reaches -950.00. A daily closing table alone hides this distinction
2. **What if E2 arrives on October 6?** The closing balance reaches -950.00 on October 3 and stays there through October 5. The final October balance remains 550.00 because only timing changed inside the horizon
3. **What if E6 moves to November 1?** October ends at 750.00 because that outflow moved outside the boundary. This does not mean the obligation disappeared; the November boundary register now contains E6 and E7

These are selected scenarios, not exhaustive best- and worst-case bounds or forecasts with probabilities.

## Repeatable calculation

The snippet uses only Python's standard library. It simulates the fictional ledger and asserts the expected results without reading accounts, writing files or scheduling anything.

```python
from datetime import date, timedelta
from decimal import Decimal as D

start, end = date(2026, 10, 1), date(2026, 11, 1)
opening = D("300")
events = [
    ("E1", date(2026, 10, 2), "out", D("450")),
    ("E2", date(2026, 10, 3), "in", D("1000")),
    ("E3", date(2026, 10, 3), "out", D("800")),
    ("E4", date(2026, 10, 10), "out", D("100")),
    ("E5", date(2026, 10, 15), "in", D("800")),
    ("E6", date(2026, 10, 20), "out", D("200")),
    ("E7", date(2026, 11, 1), "out", D("150")),
]

def simulate(source, deposits_first=True):
    assert len({e[0] for e in source}) == len(source)
    inside = [e for e in source if start <= e[1] < end]
    outside = [e for e in source if not start <= e[1] < end]
    balance, rows = opening, []
    day = start
    while day < end:
        today = [e for e in inside if e[1] == day]
        first = "in" if deposits_first else "out"
        today.sort(key=lambda e: (e[2] != first, e[0]))
        prior, event_low = balance, balance
        for _, _, direction, amount in today:
            balance += amount if direction == "in" else -amount
            event_low = min(event_low, balance)
        rows.append({"date": day, "opening": prior,
                     "closing": balance, "event_low": event_low})
        day += timedelta(days=1)
    net = sum((e[3] if e[2] == "in" else -e[3]
               for e in inside), D("0"))
    assert rows[-1]["closing"] == opening + net
    assert all(rows[i]["opening"] == rows[i-1]["closing"]
               for i in range(1, len(rows)))
    return rows, outside

baseline, outside = simulate(events)
assert len(baseline) == 31
assert baseline[-1]["closing"] == D("550")
assert min(r["closing"] for r in baseline) == D("-150")
assert next(r["date"] for r in baseline if r["closing"] < 0) == date(2026, 10, 2)
assert baseline[3]["opening"] == baseline[3]["closing"] == D("50")
assert [e[0] for e in outside] == ["E7"]
debits_first, _ = simulate(events, deposits_first=False)
assert min(r["event_low"] for r in debits_first) == D("-950")
assert debits_first[-1]["closing"] == D("550")
late = [(i, date(2026, 10, 6) if i == "E2" else d, k, a)
        for i, d, k, a in events]
late_rows, _ = simulate(late)
assert min(r["closing"] for r in late_rows) == D("-950")
assert late_rows[-1]["closing"] == D("550")
crossing = [(i, end if i == "E6" else d, k, a) for i, d, k, a in events]
crossing_rows, crossing_outside = simulate(crossing)
assert crossing_rows[-1]["closing"] == D("750")
assert {e[0] for e in crossing_outside} == {"E6", "E7"}
print("PASS: baseline, quiet day, same-day ordering, delay and boundary cases")
```

## Missing-data branch

If E3's amount is unknown, the expected output is an incomplete balance from October 3 onward, not the table above with E3 replaced by zero. Show the known subtotal and name the one missing amount. If the opening balance was measured after E1 settled, do not subtract E1 a second time; clarify the opening timestamp before finalizing any balance.

## Evidence

The exact snippet was executed with Python 3.12.14 on 2026-10-01 and produced its stated PASS line. The grouped display was checked against the computed daily values. No spreadsheet application, bank connection, reminder or payment workflow was exercised. This verifies the fictional arithmetic and date boundaries only.

[Return to the skill](SKILL.md)
