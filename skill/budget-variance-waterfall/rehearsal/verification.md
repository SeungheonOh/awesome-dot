# Verification: fictional budget rehearsal

One synthetic local rehearsal was reviewed on 2026-10-01. The [result](result.md) is a condensed public version of its review artifact; the [input](input.md) contains the entire fictional case. This checks this case, not general reliability or a live budgeting workflow.

## Repeatable arithmetic check

Run from any directory with Python 3. Values below are integer cents copied from the input; x is deliberately never assigned a value.

```sh
python3 - <<'PY'
from fractions import Fraction

plan = [30000, 15000, 25000, 0]
raw_known = [28000, 17000, 24000, -3000, -3000, 4500, 20000, 2000]
actual_known = [28000 + 1500, 17000, 24000 - 3000 + 3000, 0, 2000]
variance = [a - p for a, p in zip(actual_known, plan + [0])]
assert sum(plan) == 70000
assert sum(raw_known) == 89500
assert sum(raw_known) + 3000 - 20000 == sum(actual_known) == 72500
assert sum([28000, 17000, 24000, 4500, 2000]) - 3000 == 72500
assert actual_known == [29500, 17000, 24000, 0, 2000]
assert variance == [-500, 2000, -1000, 0, 2000]
assert sum(plan) + sum(variance) == 72500
assert 1500 + 3000 == 4500
assert sum(v for v in variance if v > 0) == 4000
assert -sum(v for v in variance if v < 0) == 1500
assert [Fraction(100 * variance[i], plan[i]) for i in range(3)] == [
    Fraction(-5, 3), Fraction(40, 3), Fraction(-4, 1)]
assert 10000 + 2000 - 2000 == 10000  # Separate cancellation test only.
print("PASS: plan 700.00; known spending 725.00; known variance +25.00 USD")
PY
```

Observed with Python 3.12.14: the command printed the stated PASS line. The public table, mapping and text bridge were read back against these checks. R4 appears at both source locators but contributes one −$30.00 refund; R5 contributes $45.00 once through its $15.00/$30.00 split; R6's $200.00 is excluded. Local Markdown links and anchors resolve.

## Boundaries

- Complete spending is $725.00 + x and complete signed variance is +$25.00 + x; x remains an unknown positive exact-cent amount. These are symbolic identities, not a verified numerical total
- Zero-plan percentages are not calculated. The cancellation assertion is an arithmetic-only test, not an additional ledger row or an observed category pair. No negative-plan case is present
- The source does not establish a shared tax basis or reasons for spending changes
- No connected financial account, live export, spreadsheet application or graphical chart renderer was exercised. No financial records or external communications were changed
- One fictional case and local arithmetic/readback checks do not certify every input, chart format, connected-app workflow or end-to-end use

[Read the result](result.md) · [Inspect the input](input.md) · [Return to the skill](../SKILL.md)
