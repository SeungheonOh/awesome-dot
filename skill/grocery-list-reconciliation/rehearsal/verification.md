# Verification of the fictional grocery list

The [packet](input.md) was processed from the skill instructions without the prior worked example or a supplied expected result. The [result](result.md) preserves the produced shopping list and arithmetic note, with local reference links added. Its quantities, source coverage and uncertainty statements were independently checked against the packet.

## Repeatable arithmetic

Run this single block with Python 3. It uses only the standard library, writes nothing and does not access a shopping service. Values transcribe the fictional packet; this is an arithmetic check, not a recipe or pantry parser.

```python
from fractions import Fraction as F
from math import ceil

f1, f2, f3 = F(8, 4), F(4 * 2, 2), F(18, 12)
assert (f1, f2, f3) == (F(2), F(4), F(3, 2))
need = {
    'drained chickpeas': 300*f1 + 100*f2,
    'dry rice': 200*f1,
    'cooked rice': 250*f2,
    'fresh tomatoes': 150*f2,
    'rolled oats': 120*f3,
    'peanut butter': 60*f3,
}
# (current quantity, reservation, purchase unit); None means no purchase needed.
stock = {
    'drained chickpeas': (F(360), F(100), F(240)),
    'dry rice': (F(500), F(150), F(250)),
    'cooked rice': (F(500), F(0), F(400)),
    'fresh tomatoes': (F(700), F(200), F(1)),  # exact gram sales in this fixture
    'rolled oats': (F(200), F(50), F(100)),
    'peanut butter': (F(200), F(0), None),
}
# Need, available, used, shortfall, purchase units, purchased grams, usable surplus.
expected = {
    'drained chickpeas': (1000, 260, 260, 740, 4, 960, 220),
    'dry rice': (400, 350, 350, 50, 1, 250, 200),
    'cooked rice': (1000, 500, 500, 500, 2, 800, 300),
    'fresh tomatoes': (600, 500, 500, 100, 100, 100, 0),
    'rolled oats': (180, 150, 150, 30, 1, 100, 70),
    'peanut butter': (90, 200, 90, 0, 0, 0, 110),
}
for key, required in need.items():
    current, reserved, unit = stock[key]
    available = current - reserved
    used = min(required, available)
    shortfall = required - used
    assert min(available, used, shortfall) >= 0
    if unit is None:
        assert shortfall == 0
        count = purchased = F(0)
    else:
        count = ceil(shortfall / unit)
        purchased = count * unit
        assert purchased >= shortfall
        if count:
            assert (count - 1) * unit < shortfall
    surplus = available - used + purchased - shortfall
    assert (required, available, used, shortfall, count, purchased, surplus) == expected[key]
    assert available + purchased == required + surplus
    assert current + purchased == required + surplus + reserved
# P2 is the same tub as P1, never another 360 g stock contribution.
assert stock['drained chickpeas'][0] == 360
assert ceil((need['drained chickpeas'] - (360-100)) / 240) == 4
assert 4 * 400 == 1600 and 4 * 240 == 960  # net mass and drained yield differ
assert 2*f1 == 4  # tablespoons; missing convention prevents a 40 ml deduction
assert 30*f3 == 45  # honey full need; stock remains unchecked
assert 10*f3 == 15  # excluded optional chocolate chips, never a required purchase
coverage = {
    'R1a': 'known', 'R1b': 'known', 'R1c': 'unit unresolved',
    'R2a': 'known', 'R2b': 'known', 'R2c': 'known',
    'R3a': 'known', 'R3b': 'selected peanut butter',
    'R3c': 'stock unchecked; provisional', 'R3d': 'excluded optional',
}
assert len(coverage) == 10
print('PASS: three yield factors, six reconciled identities, minimal supplied pack counts, reservations and ten source-line dispositions')
```

Observed with Python 3.12.14: exit 0 and the stated PASS line. The source-to-result review separately confirmed that P2 is the same chickpea tub, the almond-butter alternative is unselected, the chocolate chips are excluded, the lemon-juice convention is missing, and honey stock is unchecked rather than zero. These semantic assignments are declared inputs to the arithmetic, not facts inferred by its code.

No prices, availability, food condition, dietary suitability, ingredient density, live list save/readback or purchase was checked. The honey amount is a provisional full-need purchase, and the lemon-juice shortfall remains unresolved. The result does not establish that a complete final shopping plan or a connected-list workflow has been executed.
