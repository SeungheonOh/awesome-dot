# Fictional worked example: soup and rice

All recipes, package labels, stock confirmations and choices below are invented. They illustrate arithmetic and evidence handling, not cooking advice, current product availability or allergen suitability.

## Supplied inputs

- **U1:** Make 3 servings of R1 and 2.5 servings of R2, one batch each. Targets already include desired leftovers. Do not include the optional parsley. Prepare the list in chat; do not buy or save it anywhere
- **C1:** Both fictional recipes explicitly define 1 tbsp as 15 ml. No other volume conversions are needed
- **P1:** The user has just confirmed available stock for this plan: half a red onion; 40 ml olive oil; 150 g canned chopped tomatoes including liquid; 60 g cooked, drained chickpeas; 50 g dry rice; 100 ml coconut milk. Salt stock is unmeasured. No numeric deduction is authorized by “there is some salt”
- **K1:** Supplied purchase labels: red onions sold singly; oil in 250 ml bottles; canned chopped tomatoes, 400 g net including liquid; chickpeas, 400 g net / 240 g drained per can; dry rice in 500 g bags. No coconut-milk can size is supplied

| Source | Recipe / base yield | Original ingredient |
|---|---|---|
| R1.1 | Tomato-coconut soup / 4 servings | 1 red onion |
| R1.2 | R1 | 2 tbsp olive oil |
| R1.3 | R1 | 1 can chopped tomatoes, 400 g including liquid |
| R1.4 | R1 | 240 g cooked, drained chickpeas |
| R1.5 | R1 | 1 can coconut milk, size unstated |
| R1.6 | R1 | Salt to taste |
| R1.7 | R1 | 1 handful fresh parsley, optional |
| R2.1 | Tomato-chickpea rice / 2 servings | 1/2 red onion |
| R2.2 | R2 | 1 tbsp olive oil |
| R2.3 | R2 | 200 g canned chopped tomatoes including liquid |
| R2.4 | R2 | 100 g cooked, drained chickpeas |
| R2.5 | R2 | 160 g dry rice |

## Checked result

Scale R1 by 3/4 and R2 by 5/4. A recipe ingredient's preparation amount is not rounded to a purchase item before aggregation.

| Required item | Source contributions after scaling | Gross need | P1 stock used | Shortfall | K1 purchase | Left after recipes |
|---|---|---|---|---|---|---|
| Red onion | R1.1: 3/4; R2.1: 5/8 | 1 3/8 onions | 1/2 onion | 7/8 onion | 1 onion | 1/8 onion |
| Olive oil | R1.2: 22.5 ml; R2.2: 18.75 ml (C1) | 41.25 ml | 40 ml | 1.25 ml | 1 × 250 ml bottle | 248.75 ml |
| Canned chopped tomatoes, with liquid | R1.3: 300 g; R2.3: 250 g | 550 g | 150 g | 400 g | 1 × 400 g can | 0 g |
| Chickpeas, cooked and drained | R1.4: 180 g; R2.4: 125 g | 305 g | 60 g | 245 g | 2 × 400 g net cans, 240 g drained each | 235 g drained |
| Dry rice | R2.5: 200 g | 200 g | 50 g | 150 g | 1 × 500 g bag | 350 g |

The short shopping list is one red onion, one 250 ml bottle of olive oil, one 400 g can of chopped tomatoes, two cans of chickpeas with 240 g drained yield each, and one 500 g bag of dry rice. The large oil surplus is a consequence of the supplied 250 ml purchase option; a smaller available bottle could change that decision.

Keep these separate:

- **Coconut milk, R1.5:** 3/4 of the source's unspecified can. P1's 100 ml is real stock but cannot be subtracted from an unknown-size can. Check the recipe's can volume before finalizing the purchase amount. A different product's usual can size would not resolve the source
- **Salt, R1.6:** To taste; confirm adequate stock. Quantity and purchase amount remain unquantified, not zero
- **Parsley, R1.7:** 3/4 handful if chosen; excluded from required purchases by U1. Do not convert a handful to grams or buy it automatically

All 12 ingredient lines are represented: nine contribute to the five numeric required rows, two remain unresolved, and one optional line is excluded. Known rows reconcile; the full shopping quantity is not yet complete. No list was written to an external app.

## Executable arithmetic and coverage check

Run this Python block with Python 3. It uses only the standard library and writes no files. Raw quantities, factors and pack bases are represented explicitly so each source contribution can be checked separately from the final totals.

```python
from collections import defaultdict
from fractions import Fraction as F
from math import ceil

# Source amounts retain recipe units; conversion multipliers come from C1/K1/R1.3.
# id, canonical identity, original amount, original unit, canonical unit, multiplier
rows = [
    ("R1.1", "red onion", "1", "each", "each", "1"),
    ("R1.2", "olive oil", "2", "tbsp", "ml", "15"),
    ("R1.3", "chopped tomatoes with liquid", "1", "400g can", "g", "400"),
    ("R1.4", "cooked drained chickpeas", "240", "g", "g", "1"),
    ("R1.5", "coconut milk", "1", "unsized can", "unsized can", "1"),
    ("R1.6", "salt", None, "to taste", "to taste", None),
    ("R1.7", "fresh parsley", "1", "handful", "handful", "1"),
    ("R2.1", "red onion", "1/2", "each", "each", "1"),
    ("R2.2", "olive oil", "1", "tbsp", "ml", "15"),
    ("R2.3", "chopped tomatoes with liquid", "200", "g", "g", "1"),
    ("R2.4", "cooked drained chickpeas", "100", "g", "g", "1"),
    ("R2.5", "dry rice", "160", "g", "g", "1"),
]
factors = {"R1": F(3, 4), "R2": F("2.5") / F(2)}
scaled = {
    sid: None if amount is None else F(amount) * factors[sid[:2]] * F(mult)
    for sid, _, amount, _, _, mult in rows
}
expected_contributions = {
    "R1.1": F(3, 4), "R1.2": F("22.5"), "R1.3": F(300),
    "R1.4": F(180), "R1.5": F(3, 4), "R1.6": None,
    "R1.7": F(3, 4), "R2.1": F(5, 8), "R2.2": F("18.75"),
    "R2.3": F(250), "R2.4": F(125), "R2.5": F(200),
}
assert scaled == expected_contributions

unresolved = {"R1.5", "R1.6"}
optional_excluded = {"R1.7"}
required_ids = {sid for sid, *_ in rows} - unresolved - optional_excluded
contributions = defaultdict(dict)
for sid, identity, _, _, unit, _ in rows:
    if sid in required_ids:
        contributions[(identity, unit)][sid] = scaled[sid]
assert sum(len(values) for values in contributions.values()) == 9
assert required_ids | unresolved | optional_excluded == set(expected_contributions)
assert not (required_ids & unresolved or required_ids & optional_excluded
            or unresolved & optional_excluded)

# P1 compatible stocks and K1 usable purchase amounts, in each row's canonical unit.
# The chickpea package is 400 g net, but its USABLE drained amount is 240 g.
stock_and_pack = {
    ("red onion", "each"): (F(1, 2), F(1)),
    ("olive oil", "ml"): (F(40), F(250)),
    ("chopped tomatoes with liquid", "g"): (F(150), F(400)),
    ("cooked drained chickpeas", "g"): (F(60), F(240)),
    ("dry rice", "g"): (F(50), F(500)),
}
expected = {
    # identity: (gross, stock used, shortfall, package count, leftover)
    "red onion": (F(11, 8), F(1, 2), F(7, 8), 1, F(1, 8)),
    "olive oil": (F("41.25"), F(40), F("1.25"), 1, F("248.75")),
    "chopped tomatoes with liquid": (F(550), F(150), F(400), 1, F(0)),
    "cooked drained chickpeas": (F(305), F(60), F(245), 2, F(235)),
    "dry rice": (F(200), F(50), F(150), 1, F(350)),
}
for key, sources in contributions.items():
    gross = sum(sources.values(), F(0))
    stock, pack = stock_and_pack[key]
    used = min(gross, stock)
    shortfall = gross - used
    count = ceil(shortfall / pack)
    leftover = stock - used + count * pack - shortfall
    assert (gross, used, shortfall, count, leftover) == expected[key[0]]
    assert stock + count * pack == gross + leftover
    assert count * pack >= shortfall >= 0
    assert count == 0 or (count - 1) * pack < shortfall

# Incompatible coconut-milk units deliberately have no numerical stock deduction.
coconut_requirement = (scaled["R1.5"], "unsized can")
coconut_stock = (F(100), "ml")
assert coconut_requirement[1] != coconut_stock[1]
assert "coconut milk" not in expected
assert scaled["R1.6"] is None  # Unknown is not zero.

# Branch: sufficient stock requires no purchase; excess remains pantry stock.
gross, stock, pack = F(200), F(300), F(500)
used = min(gross, stock)
shortfall = gross - used
count = ceil(shortfall / pack)
assert (count, stock - used + count * pack - shortfall) == (0, F(100))

# Batch arrangement must not multiply a target that already describes the total.
def yield_factor(source_yield, requested_yield, basis, batches):
    assert basis in {"total", "per-batch"}
    assert source_yield > 0 and requested_yield > 0 and batches > 0
    total = requested_yield * batches if basis == "per-batch" else requested_yield
    return F(total) / F(source_yield)

assert yield_factor(4, 8, "total", 2) == 2  # Eight total, arranged in two batches.
assert yield_factor(4, 6, "per-batch", 2) == 3  # Twelve total servings.
assert yield_factor(4, 8, "total", 1) == yield_factor(4, 8, "total", 2)
print("PASS: 12 source lines; 9 numeric contributions; 5 reconciled purchases;")
print("      2 unresolved lines; 1 excluded optional line; stock and batch branches")
```

Run the checked block directly from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/grocery-list-reconciliation/example.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'grocery-example', 'exec'))
PY
```

Observed locally with Python 3.12.14 on 2026-10-01: the check passed. It verifies this synthetic arithmetic, source coverage, incompatibility, sufficient-stock case and total-versus-per-batch yield distinction. It does not verify real recipe scaling, product labels, pantry condition, prices, live list writes or purchasing.
