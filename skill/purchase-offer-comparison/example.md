# Fictional example: two exact bottles

All products, merchants, quotes and tax rules below are invented. They demonstrate one bounded comparison, not current offers. The timestamp is part of the fixture; no retailer was contacted and no address, payment or membership data was used.

## Requirement and source packet

**U1:** Compare exactly two new **Aster 600 bottles, 600 ml, graphite, loop lid included**, delivered to the already-quoted destination by **2026-10-09**. For this comparison, an estimated arrival range ending by that date is acceptable; no delivery guarantee is required. No surplus or substitutions. Prepare a private comparison only. Existing Harbor Club membership is unknown; do not enroll.

**T1:** All supplied quotes were captured at **2026-10-01 10:00 UTC**, in USD, for U1's destination. Complete quotes A1, B1 and D1, including B1's stated promotion scenario, explicitly use order-level rounding to cents, half up. For those offers, the fictional 8% tax applies to discounted merchandise plus mandatory handling; delivery is not taxed. C1 supplies no applicable tax basis or amount. These are supplied rules, not inferred real tax rates.

| Source / offer | Exact listing and quantity | Charges and promotion | Fulfillment and visible returns |
|---|---|---|---|
| A1 / Meadow Supply | Exact Aster 600 variant; $32.50 each; two singles | $1.20 mandatory order handling; $4.95 delivery; $5.30 tax; quoted total $76.45 | Two available in supplied quote; estimated arrival Oct 6–8. R-A: unopened returns within 30 days of delivery; buyer pays return postage; outbound shipping not refunded |
| B1 / Harbor Cart | Exact variant; $72.00 per two-pack; one pack | $0 handling and delivery; $5.76 baseline tax; baseline total $77.76. P-B: 10% off merchandise for existing active Harbor Club members, this two-pack eligible, no code stacking, valid through Oct 2 23:59:59 UTC | One two-pack available in supplied quote; estimated arrival Oct 7–9. R-B: unopened returns within 14 days of delivery; $4 label fee per return order |
| C1 / Fern Market | Exact variant; $27.00 each; two singles | $0 handling explicitly; delivery and tax withheld until destination-specific quote; no payable total | Required quantity not verified. “Dispatch Oct 5” only, no arrival estimate. Return terms absent from packet |
| D1 / Slate Bazaar | Aster **450**, **450 ml**, graphite, loop lid; one two-pack at $48.00 | $0 handling and delivery; $3.84 tax; $51.84 quoted total | Supplied quote shows one pack and Oct 6–8 estimated arrival; incompatible capacity and model, regardless of price |

P-B does not establish that U1 belongs to Harbor Club. Its discounted result is a calculated scenario, not a verified eligible checkout quote. The completed rows are snapshots; availability and price need rechecking before any real commitment.

## Checked comparison

| Offer | Delivered-cost bridge | Status |
|---|---|---|
| Meadow Supply | 2 × $32.50 + $1.20 + $4.95 + $5.30 = **$76.45** | Best supported non-member baseline; exact quantity and estimated arrival meet U1 |
| Harbor Cart, baseline | 1 × $72.00 + $0 + $0 + $5.76 = **$77.76** | Exact and feasible in supplied quote; $1.31 above Meadow |
| Harbor Cart, member scenario | $72.00 − $7.20 + $0 + $0 + $5.18 = **$69.98** | Conditional; $6.47 below Meadow only if existing membership and checkout applicability are confirmed |
| Fern Market | 2 × $27.00 = **$54.00 known merchandise subtotal**; delivery and tax unknown | Total, quantity availability and arrival unresolved; cannot rank as cheapest delivered offer |
| Slate Bazaar | $48.00 + $3.84 = **$51.84** | Excluded; the 450 ml model does not satisfy U1 |

Recommendation: Meadow Supply is the lowest complete baseline among the compatible offers in this packet. Before choosing, the one user-specific question that could reverse the price ranking is whether an existing active Harbor Club membership applies. Do not enroll. Fern Market needs a complete quote, quantity check and arrival estimate before it can compete. Both complete compatible offers have estimated arrival ranges, not guarantees. Meadow has the longer visible return window; Harbor specifies a $4 return-label fee. Return-postage cost at Meadow remains unknown and is not added to the delivered purchase total.

No offer was accepted, cart created or purchase made. No discount, stock or delivery claim was checked live.

## Executable arithmetic, identity and eligibility check

Run with Python 3, standard library only. The checker derives totals from pack counts and price components, uses the supplied tax rule, excludes the wrong variant and preserves missing charges. It also checks expiry and that unknown membership cannot silently select the member total.

```python
from datetime import date, datetime, timezone
from decimal import Decimal as D, ROUND_HALF_UP

CENT = D("0.01")
AS_OF = datetime(2026, 10, 1, 10, tzinfo=timezone.utc)
EXPIRY = datetime(2026, 10, 2, 23, 59, 59, tzinfo=timezone.utc)
DEADLINE = date(2026, 10, 9)
REQUIRED = ("Aster 600", 600, "graphite", "loop", "new")

def money(value):
    return value.quantize(CENT, rounding=ROUND_HALF_UP)

# id: (variant, units/pack, packs, price/pack, handling, delivery, stock, arrival)
offers = {
    "A1": (REQUIRED, 1, 2, D("32.50"), D("1.20"), D("4.95"), 2,
           (date(2026, 10, 6), date(2026, 10, 8))),
    "B1": (REQUIRED, 2, 1, D("72.00"), D("0"), D("0"), 1,
           (date(2026, 10, 7), date(2026, 10, 9))),
    "C1": (REQUIRED, 1, 2, D("27.00"), D("0"), None, None, None),
    "D1": (("Aster 450", 450, "graphite", "loop", "new"),
           2, 1, D("48.00"), D("0"), D("0"), 1,
           (date(2026, 10, 6), date(2026, 10, 8))),
}

def bridge(offer_id, discount_rate=D("0")):
    variant, unit_count, packs, price, handling, delivery, stock, arrival = offers[offer_id]
    merchandise = packs * price
    discount = money(merchandise * discount_rate)
    # C1's source withholds tax, so the fixture deliberately cannot derive it.
    tax = None if offer_id == "C1" else money((merchandise - discount + handling) * D("0.08"))
    total = (None if tax is None or delivery is None else
             money(merchandise - discount + handling + delivery + tax))
    return {"units": unit_count * packs, "merchandise": merchandise,
            "discount": discount, "tax": tax, "total": total}

def eligible_member_rate(member_status, at):
    # Exact eligible two-pack and no stacking are supplied by P-B.
    return D("0.10") if member_status is True and at <= EXPIRY else D("0")

def feasible(offer_id, cost):
    variant, unit_count, packs, price, handling, delivery, stock, arrival = offers[offer_id]
    return (variant == REQUIRED and cost["units"] == 2 and cost["total"] is not None
            and stock is not None and stock >= packs
            and arrival is not None and arrival[1] <= DEADLINE)

base = {oid: bridge(oid) for oid in offers}
assert {oid: row["units"] for oid, row in base.items()} == dict.fromkeys(offers, 2)
assert [base[x]["total"] for x in offers] == [D("76.45"), D("77.76"), None, D("51.84")]
assert [base[x]["tax"] for x in offers] == [D("5.30"), D("5.76"), None, D("3.84")]
assert base["C1"]["merchandise"] == D("54.00") and base["C1"]["total"] is None
assert offers["C1"][6] is None and offers["C1"][7] is None
assert not feasible("D1", base["D1"])  # Lower total cannot fix wrong model/capacity.
complete = {oid: row["total"] for oid, row in base.items() if feasible(oid, row)}
assert complete == {"A1": D("76.45"), "B1": D("77.76")}
assert min(complete, key=complete.get) == "A1"
assert complete["B1"] - complete["A1"] == D("1.31")

assert eligible_member_rate(None, AS_OF) == D("0")
assert eligible_member_rate(False, AS_OF) == D("0")
conditional = bridge("B1", eligible_member_rate(True, AS_OF))
assert (conditional["discount"], conditional["tax"], conditional["total"]) == (
    D("7.20"), D("5.18"), D("69.98"))
assert feasible("B1", conditional)
assert complete["A1"] - conditional["total"] == D("6.47")
member_scenario = {"A1": base["A1"]["total"], "B1": conditional["total"]}
assert min(member_scenario, key=member_scenario.get) == "B1"
after_expiry = datetime(2026, 10, 3, tzinfo=timezone.utc)
assert bridge("B1", eligible_member_rate(True, after_expiry))["total"] == D("77.76")

# Quantity check uses available PACKS; arrival must meet the actual deadline.
saved = offers["B1"]
offers["B1"] = (*saved[:6], 0, saved[7])
assert not feasible("B1", base["B1"])
offers["B1"] = (*saved[:7], (date(2026, 10, 9), date(2026, 10, 10)))
assert not feasible("B1", base["B1"])
offers["B1"] = saved
print("PASS: 4 offer identities and quantities; 3 complete arithmetic bridges;")
print("      conditional discount reverses winner; unknown costs, stock and arrival stay open")
```

Run the fenced block from the repository root:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('skill/purchase-offer-comparison/example.md').read_text()
code = text.split('```python\n', 1)[1].split('\n```', 1)[0]
exec(compile(code, 'purchase-offer-example', 'exec'))
PY
```

Observed locally on 2026-10-01 with Python 3.12.14: the fenced check passed, and the skill frontmatter validator passed. This checks only the fictional identities, quantities, arithmetic, promotion branch and feasibility gates. It does not verify live merchant prices, destination taxes, account eligibility, return rights, actual inventory or a transaction.
