# Worked example: a comfortable month can still dip below zero

All entries below are fictional USD amounts for sanitized account A. The horizon is October 2026 in UTC. The opening balance is a ledger balance of 300.00 immediately before October 1, with no pending amounts already reflected and no bridge needed. All E1–E7 entries belong to A. A warning means strictly below 0.00; equality does not trigger it.

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

A real workflow would retain source references and uncertainty for each date. This fixture supplies no real account, payment instructions or personal data.

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

## Opening-balance and account regressions

These additional, independent fictional records do not change E1–E7. They illustrate three checks before running a daily calendar:

- **Balance basis:** A has ledger 100.00 and available 80.00 at October 1, with a 20.00 hold already reflected only in available. The supplied scenario says October 2's 20.00 settlement replaces that exact hold simultaneously. Available therefore stays 80.00; subtracting another 20.00 would falsely show 60.00. Ledger drops from 100.00 to 80.00. This is a supplied posting assumption, not a bank rule or a claim about unobserved intraday release timing. Unknown linkage, reflection or release timing leaves the effect unresolved
- **Older snapshot:** A's ledger snapshot is 300.00 at September 30 09:00 UTC. A confirmed 100.00 debit at noon belongs in the separate bridge, giving October's opening 200.00. It is outside October but cannot be dropped from the bridge. The snapshot's inclusion of any event at exactly 09:00 must be explicit; incomplete bridge coverage leaves the opening unresolved
- **Account boundary:** A opens at 100.00 and B at 1,000.00, both USD ledger balances at October's boundary with no reflected pending amounts. A alone pays 200.00. A reaches −100.00 even though the optional same-currency aggregate is 900.00. No transfer is assumed. Unknown account assignment blocks a complete result, and a mixed-currency total is not calculated

The following standalone snippet checks only these stated fixtures and guards. It is not a bank-data importer or a model of posting rules. `None` means unresolved, never zero. Amounts passed to the account check are already reconciled remaining effects on the stated ledger basis.

```python
from datetime import datetime as DT
from decimal import Decimal as D

def utc(s):
    return DT.fromisoformat(s + "+00:00")

boundary = utc("2026-10-01T00:00:00")

def remaining_effect(snapshot, event):
    if (snapshot["account"], snapshot["currency"]) != (event["account"], event["currency"]):
        return None
    if snapshot["basis"] not in {"ledger", "available"}:
        return None  # An "other" basis would need its own supplied definition.
    reflected = snapshot["reflected"].get(event["movement"])
    if reflected is None or event["signed_effect"] is None:
        return None
    if reflected != 0 and event["simultaneous_replacement"] is not True:
        return None
    return event["signed_effect"] - reflected

available = dict(account="A", currency="USD", at=boundary,
                 basis="available", amount=D("80"), reflected={"P1": D("-20")})
ledger = dict(available, basis="ledger", amount=D("100"), reflected={"P1": D("0")})
settlement = dict(id="S1", movement="P1", account="A", currency="USD",
                  at=utc("2026-10-02T00:00:00"), signed_effect=D("-20"),
                  simultaneous_replacement=True)
assert available["amount"] + remaining_effect(available, settlement) == D("80")
assert ledger["amount"] + remaining_effect(ledger, settlement) == D("80")
assert remaining_effect(dict(available, reflected={"P1": None}), settlement) is None
assert remaining_effect(available, dict(settlement, movement="unlinked")) is None
assert remaining_effect(available, dict(settlement, simultaneous_replacement=None)) is None
assert remaining_effect(dict(available, basis="unspecified"), settlement) is None

def bridge_opening(snapshot, bridge, horizon, coverage_complete):
    # Tuples are (ID, account, currency, timestamp, signed remaining effect).
    ids = [e[0] for e in bridge + horizon]
    if len(set(ids)) != len(ids):
        raise ValueError("Duplicate or overlapping bridge/horizon movement")
    if not coverage_complete:
        return None
    if (snapshot["at"] is None or snapshot["at"] > boundary
            or snapshot["amount"] is None):
        return None  # No backward inference from a later or unknown snapshot.
    balance = snapshot["amount"]
    for ident, account, currency, at, effect in bridge:
        if not snapshot["at"] <= at < boundary:
            raise ValueError("Not a snapshot-to-boundary movement")
        if (account, currency) != (snapshot["account"], snapshot["currency"]):
            return None
        if at == snapshot["at"]:
            included = snapshot["included_at_timestamp"].get(ident)
            if included is None:
                return None
            if included:
                continue
        if effect is None:
            return None
        balance += effect
    return balance

snapshot = dict(account="A", currency="USD", basis="ledger", amount=D("300"),
                at=utc("2026-09-30T09:00:00"), included_at_timestamp={})
debit = ("D1", "A", "USD", utc("2026-09-30T12:00:00"), D("-100"))
assert bridge_opening(snapshot, [debit], [], True) == D("200")
assert bridge_opening(dict(snapshot, at=utc("2026-10-02T00:00:00")), [], [], True) is None
assert bridge_opening(dict(snapshot, amount=None), [debit], [], True) is None
assert bridge_opening(dict(snapshot, at=None), [debit], [], True) is None
assert bridge_opening(snapshot, [debit], [], False) is None
assert bridge_opening(snapshot, [debit[:-1] + (None,)], [], True) is None
tie = ("T1", "A", "USD", snapshot["at"], D("-10"))
assert bridge_opening(snapshot, [tie, debit], [], True) is None
assert bridge_opening(dict(snapshot, included_at_timestamp={"T1": True}),
                      [tie, debit], [], True) == D("200")
assert bridge_opening(dict(snapshot, included_at_timestamp={"T1": False}),
                      [tie, debit], [], True) == D("190")
try:
    bridge_opening(snapshot, [debit], [debit], True)
except ValueError:
    pass
else:
    raise AssertionError("Bridge/horizon overlap was counted twice")
try:
    bridge_opening(snapshot, [("H1", "A", "USD", boundary, D("-10"))], [], True)
except ValueError:
    pass
else:
    raise AssertionError("A horizon-boundary event was put in the bridge")

def close_accounts(openings, effects):
    balances = dict(openings)
    for _, account, currency, effect in effects:
        key = (account, currency)
        if key not in balances or effect is None or balances[key] is None:
            return None  # Do not guess which account/currency an event affects.
        balances[key] += effect
    return balances

def same_currency_total(balances):
    if balances is None or len({currency for _, currency in balances}) != 1:
        return None
    return None if None in balances.values() else sum(balances.values(), D("0"))

# Both openings are USD ledger balances immediately before boundary movements;
# no pending amounts are reflected, and effects occur within October.
openings = {("A", "USD"): D("100"), ("B", "USD"): D("1000")}
effects = [("A-bill", "A", "USD", D("-200"))]
closed = close_accounts(openings, effects)
assert closed == {("A", "USD"): D("-100"), ("B", "USD"): D("1000")}
assert [key for key, value in closed.items() if value < 0] == [("A", "USD")]
assert same_currency_total(closed) == D("900")  # A's warning still stands.
assert close_accounts(openings, [("unknown", None, "USD", D("-200"))]) is None
assert close_accounts(openings, [("mismatch", "A", "EUR", D("-200"))]) is None
assert same_currency_total({("A", "USD"): D("-100"), ("B", "EUR"): D("1000")}) is None
print("PASS: balance basis, reflected hold, bridge, unknowns, overlap and account boundaries")
```

## Evidence

Both exact snippets were executed separately with Python 3.12.14 on 2026-10-01 and each produced its stated PASS line. The original grouped display was rechecked against all 31 computed daily values. No spreadsheet application, bank connection, reminder or payment workflow was exercised. These checks verify the supplied fictional arithmetic and boundary guards only; they do not establish real posting behavior or end-to-end account-data handling.

[Return to the skill](SKILL.md)
