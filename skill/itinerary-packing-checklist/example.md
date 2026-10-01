# Fictional worked example: a short activity trip

Every booking, venue, forecast, measurement and transport rule here is invented. Dates use a supplied fixed local offset of UTC+01:00 throughout, with no overnight travel or zone change. No live provider was consulted and no actual itinerary, packing list or reservation was changed.

## Supplied sources

- **I1, confirmed itinerary:** Leave home on 2026-11-05 and return on 2026-11-09. Lodging check-in Nov 5, checkout Nov 9. A craft workshop is on Nov 6, a ridge walk on Nov 7 and a pool visit on Nov 8
- **U1, preferences:** One clean everyday top, underwear item and pair of socks per travel day. No extra daily changes or spare sets. Wear one set on departure. Reuse the same long trousers and closed walking shoes throughout. One reusable sleepwear set. Bring the camera; omit optional swimming goggles
- **L1, confirmed laundry arrangement:** All three used sets of tops/underwear/socks can be washed after the Nov 7 activities and will be dry and returned by 07:00 Nov 8, before that day's use. Capacity is three of each category. No other wash is planned
- **V1, workshop booking:** Long trousers and closed shoes are required. No special safety rating is specified. The venue provides the necessary apron and tools
- **V2, pool booking:** Bring swimwear; the venue provides a towel. Goggles are optional
- **W1, supplied fictional forecast:** Valid Nov 5–9 at the trip's activity locations, issued Nov 3. Range 8–16°C, rain for the Nov 7 ridge walk. The traveler selected the packed rain shell for this plan. This is illustrative evidence, not an actual forecast
- **B1, supplied fictional carrier/fare rule:** One cabin bag up to 55 × 35 × 20 cm and one personal bag up to 40 × 30 × 15 cm; dimensions include wheels and handles. Their combined packed weight, including empty bags, must not exceed 7.00 kg. Worn clothing is excluded. No checked-bag entitlement is supplied
- **E1, selected essentials:** Phone, charger, toiletries and a small wallet/document pouch. Keep document identifiers and any personal reasons out of the checklist
- **P1, supplied measurements:** Cabin bag 53 × 34 × 19 cm, empty 1.20 kg; personal bag 38 × 28 × 13 cm, empty 0.30 kg. The item weights below include their normal cases/containers. Camera weight is not yet measured

## Initial checked list

Five calendar travel days; four lodging nights. For each clean-clothing category, label the three physical items A, B and C: use A on Nov 5, B on Nov 6, C on Nov 7; wash all three; use clean A on Nov 8 and clean B on Nov 9. Three items total, one worn on departure, so pack two of each category. This reduction depends on L1.

| Location / item | Quantity packed | Unit weight | Known contribution | Need evidence |
|---|---:|---:|---:|---|
| Cabin bag itself | 1 | 1.20 kg | 1.20 kg | B1, P1 |
| Everyday tops | 2 | 0.18 kg | 0.36 kg | I1, U1, L1 |
| Underwear | 2 | 0.05 kg | 0.10 kg | I1, U1, L1 |
| Sock pairs | 2 | 0.04 kg | 0.08 kg | I1, U1, L1 |
| Sleepwear set | 1 | 0.25 kg | 0.25 kg | U1, four nights in I1 |
| Rain shell | 1 | 0.30 kg | 0.30 kg | W1, user selection |
| Swimwear | 1 | 0.16 kg | 0.16 kg | I1, V2 |
| Toiletries pouch | 1 | 0.35 kg | 0.35 kg | E1 |
| Personal bag itself | 1 | 0.30 kg | 0.30 kg | B1, P1 |
| Charger | 1 | 0.12 kg | 0.12 kg | E1 |
| Phone | 1 | 0.18 kg | 0.18 kg | E1 |
| Wallet/document pouch | 1 | 0.15 kg | 0.15 kg | E1 |
| Camera in personal bag | 1 | Unknown | Unknown | U1; P1 weight pending |

P1 supplies the item weights in every numeric row. Worn on departure: one everyday top, underwear item and pair of socks, plus the reusable long trousers and closed walking shoes. Those shoes and trousers also cover V1. The workshop apron/tools and pool towel are provider-supplied; goggles are optional and excluded by U1.

Known cabin subtotal: **2.80 kg**. Known personal subtotal: **0.75 kg plus camera**. Combined known subtotal: **3.55 kg plus camera**. The 3.45 kg difference from B1's limit is the maximum remaining weight budget for the camera and any additions, not proof that the bags comply. Both supplied bag dimensions satisfy B1, but the contents have not been physically packed or checked for bulging.

Checks before leaving: weigh the camera and final packed bags, verify physical fit, and verify any applicable item-specific transport rules if the toiletries/camera contents require them. The sample supplies no live liquid or battery rules; it does not declare those items cleared.

## Changed itinerary and missing-evidence branch

The user supplies a confirmed revision:

- **I2:** Return on Nov 10 instead, with lodging checkout separately confirmed for Nov 10. The Nov 8 pool booking has been removed from this packing plan; its cancellation/refund status is outside scope. A Nov 9 drawing session replaces it. Other activities and L1 are unchanged
- **V3:** The drawing venue requires a sketchbook; drawing materials are provided. No new clothing requirement
- **P2:** The selected sketchbook is 0.24 kg and goes in the cabin bag. The camera is still unweighed

Update the list:

- Six travel days and five lodging nights. Clean-clothing use becomes A, B, C, then washed A, B, C. Keep two of each category packed; the extra day fits the confirmed clean inventory
- Remove the 0.16 kg swimwear because no remaining activity or user preference needs it. The pool towel and optional goggles do not become new purchases
- Add one 0.24 kg sketchbook. New known cabin subtotal is 2.88 kg; personal stays 0.75 kg plus camera; combined known subtotal is **3.63 kg plus camera**
- W1 stops Nov 9. Add a task to obtain relevant Nov 10 weather evidence in real use; don't extend the old forecast or invent the extra day's conditions
- If L1 becomes unavailable, recalculate to six clean sets total and **five packed** tops, underwear items and sock pairs. Do not keep the lighter laundry-dependent list. This would add 0.81 kg to the revised known subtotal, producing **4.44 kg plus camera**

If the user subsequently measures the camera at **0.85 kg**, the revised laundry-confirmed list totals **4.48 kg** across the two bags. That is under the fictional 7 kg rule for the listed load. It still does not establish physical fit, rule compliance for unexamined item contents, a live allowance, or final weight after extra items are added.

## Executable count, source and weight check

The following standard-library Python check exercises the supplied fixture. It tests each item's evidence references, dated clothing coverage, activity coverage, changed-source removal, weight subtotals and the blocked-to-complete weight branch. It makes no external requests and writes no files.

```python
from datetime import date, timedelta
from decimal import Decimal as D

start = date(2026, 11, 5)
original_end = date(2026, 11, 9)
revised_end = date(2026, 11, 10)
laundry_return = date(2026, 11, 8)  # L1: before use, three washed per category.

def days_through(end):
    return [start + timedelta(days=n) for n in range((end - start).days + 1)]

def clean_inventory(end, laundry=True):
    dates = days_through(end)
    intervals = ([sum(d < laundry_return for d in dates),
                  sum(d >= laundry_return for d in dates)]
                 if laundry else [len(dates)])
    total = max(intervals)
    return total, total - 1  # One of each is worn on departure under U1.

assert (len(days_through(original_end)), (original_end - start).days) == (5, 4)
assert (len(days_through(revised_end)), (revised_end - start).days) == (6, 5)
assert clean_inventory(original_end) == clean_inventory(revised_end) == (3, 2)
assert clean_inventory(revised_end, laundry=False) == (6, 5)
# Explicit reuse after L1; never repeat a used item before its wash/return.
for end in (original_end, revised_end):
    used = set()
    for day, item in zip(days_through(end), "ABCABC"):
        if day == laundry_return:
            assert len(used) == 3  # Exactly the promised laundry capacity.
            used.clear()
        assert item not in used
        used.add(item)

sources = {"I1", "U1", "L1", "V1", "V2", "W1", "B1", "E1", "P1",
           "I2", "V3", "P2"}
# item: bag, count, measured unit kg (None means unknown), purpose sources
items = {
    "cabin bag": ("cabin", 1, D("1.20"), {"B1", "P1"}),
    "tops": ("cabin", 2, D("0.18"), {"I1", "U1", "L1"}),
    "underwear": ("cabin", 2, D("0.05"), {"I1", "U1", "L1"}),
    "sock pairs": ("cabin", 2, D("0.04"), {"I1", "U1", "L1"}),
    "sleepwear": ("cabin", 1, D("0.25"), {"I1", "U1"}),
    "rain shell": ("cabin", 1, D("0.30"), {"W1"}),
    "swimwear": ("cabin", 1, D("0.16"), {"I1", "V2"}),
    "toiletries": ("cabin", 1, D("0.35"), {"E1"}),
    "personal bag": ("personal", 1, D("0.30"), {"B1", "P1"}),
    "charger": ("personal", 1, D("0.12"), {"E1"}),
    "phone": ("personal", 1, D("0.18"), {"E1"}),
    "wallet/documents": ("personal", 1, D("0.15"), {"E1"}),
    "camera": ("personal", 1, None, {"U1", "P1"}),
}
for bag, count, weight, evidence in items.values():
    assert bag in {"cabin", "personal"} and count > 0
    assert evidence and evidence <= sources
    assert weight is None or weight >= 0

worn = {"top": {"U1"}, "underwear": {"U1"}, "socks": {"U1"},
        "long trousers": {"U1", "V1"}, "closed walking shoes": {"U1", "V1"}}
provided = {"apron": {"V1"}, "tools": {"V1"}, "pool towel": {"V2"}}
excluded = {"goggles": {"U1", "V2"}}
requirements = {"V1": {"long trousers", "closed walking shoes", "apron", "tools"},
                "W1": {"rain shell"}, "V2": {"swimwear", "pool towel"}}
covered = set(items) | set(worn) | set(provided)
for source, needs in requirements.items():
    assert source in sources and needs <= covered
assert not (set(excluded) & covered)
assert all(evidence <= sources for mapping in (worn, provided, excluded)
           for evidence in mapping.values())

limit = D("7.00")
def weight_result(load):
    known = {"cabin": D(0), "personal": D(0)}
    unknown = []
    for name, (bag, count, unit_weight, _) in load.items():
        if unit_weight is None:
            unknown.append(name)
        else:
            known[bag] += count * unit_weight
    total = sum(known.values(), D(0))
    state = "over limit" if total > limit else ("incomplete" if unknown else "within limit")
    return known, total, unknown, state

assert weight_result(items) == ({"cabin": D("2.80"), "personal": D("0.75")},
                                D("3.55"), ["camera"], "incomplete")
assert limit - weight_result(items)[1] == D("3.45")
assert all(x <= y for x, y in zip((53, 34, 19), (55, 35, 20)))
assert all(x <= y for x, y in zip((38, 28, 13), (40, 30, 15)))

revised = {name: (bag, count, mass, (evidence - {"I1"}) | {"I2"})
           for name, (bag, count, mass, evidence) in items.items()
           if name != "swimwear"}
revised["sketchbook"] = ("cabin", 1, D("0.24"), {"I2", "V3", "P2"})
assert weight_result(revised) == ({"cabin": D("2.88"), "personal": D("0.75")},
                                  D("3.63"), ["camera"], "incomplete")
assert not any("V2" in row[3] for row in revised.values())
revised_provided = {name: refs for name, refs in provided.items() if "V2" not in refs}
revised_provided["drawing materials"] = {"V3"}
assert {"sketchbook", "drawing materials"} <= set(revised) | set(revised_provided)
forecast_dates = set(days_through(original_end))
assert set(days_through(revised_end)) - forecast_dates == {date(2026, 11, 10)}

no_laundry = dict(revised)
for name in ("tops", "underwear", "sock pairs"):
    bag, _, mass, evidence = no_laundry[name]
    no_laundry[name] = (bag, 5, mass, evidence - {"L1"})
assert weight_result(no_laundry)[1] == D("4.44")
assert weight_result(no_laundry)[3] == "incomplete"
measured = dict(revised)
bag, count, _, evidence = measured["camera"]
measured["camera"] = (bag, count, D("0.85"), evidence)
assert weight_result(measured)[1:] == (D("4.48"), [], "within limit")
# A partial subtotal already above the limit proves a weight problem.
heavy = dict(revised)
heavy["cabin bag"] = ("cabin", 1, D("5.00"), {"P1"})
assert weight_result(heavy)[3] == "over limit"
print("PASS: 5/4 then 6/5 day/night counts; laundry and no-laundry quantities;")
print("      activity/source coverage; 3.55/3.63 kg partials; 4.48 kg measured branch")
```

Run the block from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/itinerary-packing-checklist/example.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'packing-example', 'exec'))
PY
```

Observed locally with Python 3.12.14 on 2026-10-01: all assertions passed. This checks the synthetic inputs and calculations; it does not test live source retrieval, actual bag fit, laundry performance, security restrictions or an app write.
