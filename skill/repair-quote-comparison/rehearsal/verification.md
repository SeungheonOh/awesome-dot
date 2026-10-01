# Verification: fictional repair quotes

One synthetic local rehearsal was reviewed on 2026-10-01. The [result](result.md) is a condensed public decision sheet based only on the [fictional input](input.md). This checks the supplied arithmetic, scope and qualifications; it does not certify supplier availability, site suitability or a live quotation workflow.

## Repeatable arithmetic and date check

Run from any directory with Python 3. Decimal amounts and dates below are copied from the input. The 20% tax rate is used only where the fictional quote supplies it.

```sh
python3 - <<'PY'
from decimal import Decimal as D
from datetime import date

as_of = date(2026, 10, 1)
a_net = sum(map(D, ["180", "120", "20"]))
a_gross = a_net * D("1.20")
assert (a_net, a_net * D("0.20"), a_gross) == (D("320"), D("64"), D("384"))
assert a_gross - D("96") == D("288")
# Conditional optional scenario: same supplied VAT must also apply to handles.
assert a_gross + D("40") * D("1.20") == D("432")
assert D("432") - D("40") * D("1.20") == a_gross
b_base = D("260") + D("100")
assert b_base == D("360")
assert b_base + D("80") == D("440")  # Raw listed subtotal, not net/gross.
c_net = D("200") + D("100") + D("30")
c_gross = c_net * D("1.20")
assert (c_net, c_net * D("0.20"), c_gross) == (D("330"), D("66"), D("396"))
assert c_gross * D("0.50") == D("198")
def gross_at(materials):
    return c_gross + D("1.20") * (materials - D("80"))
assert [gross_at(D(m)) for m in ["70", "80", "90"]] == [D("384"), D("396"), D("408")]
assert c_gross - a_gross == D("12")
assert date(2026, 9, 30) < as_of
assert date(2026, 9, 28) <= as_of <= date(2026, 10, 31)
assert date(2026, 9, 29) <= as_of <= date(2026, 10, 15)
print("PASS: A 384.00 expired; B 440.00 raw subtotal; C 396.00 estimate, deposit 198.00 EUR")
PY
```

Observed with Python 3.12.14: the command printed the stated PASS line. Readback confirmed three mandatory scope rows; B's refinishing is required despite its optional label; A's handles stay outside the core scenario. Deposits are credits, and C's allowance is already included. Local Markdown links and source anchors resolve.

## Boundaries

- A's supplied total and C's estimate recalculate with zero discrepancy; B's base also agrees, but a tax-inclusive total is not specified and cannot be verified
- Dates establish only validity within the supplied excerpts as of 2026-10-01. A needs renewal; B's tax/firmness and C's uncapped allowance prevent a firm current all-in conclusion
- C's below/at/above-allowance tests check a formula, not probabilities or a price ceiling. A's optional gross scenario is conditional on the same tax treatment
- The result preserves missing site assumptions, schedules, warranty and cancellation/deposit-refund terms. No supplier is selected
- Only local text, arithmetic, date and readback checks were performed. No connected application, supplier contact, live availability check, site inspection, booking, payment or acceptance was exercised
- One fictional case does not certify all quote formats, OCR accuracy, legal interpretation or end-to-end execution

[Read the result](result.md) · [Inspect the input](input.md) · [Return to the skill](../SKILL.md)
