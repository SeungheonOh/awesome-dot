# Worked example: three gate-repair quotes

All suppliers, documents and terms below are fictional. No supplier was contacted and no offer was accepted.

## Inputs

```yaml
comparison_date: 2026-10-01
currency: GBP
required_scope:
  - refit existing hinges
  - replace latch
  - weatherproof repaired area
  - remove repair waste
confirmed_site_facts:
  - existing timber gate remains in place
priorities:
  - complete required scope
  - known all-in price
  - then lower price
quotes:
  - id: ALDER-1
    valid_through: 2026-10-15
    fixed_net_items:
      labor: 400.00
      materials: 250.00
      weatherproofing: 80.00
      waste_removal: 30.00
    tax: "20% of all listed net items"
    stated_total: 912.00
    scope: "All required work included; no optional work"
    timing: "Proposed start 2026-10-12, subject to acceptance"
  - id: BIRCH-1
    valid_through: 2026-10-08
    fixed_tax_inclusive_total: 980.00
    scope: "All required work included"
    optional_decoration_tax_inclusive: 60.00
    timing: "Start to be agreed"
  - id: CEDAR-1
    valid_through: 2026-10-20
    fixed_net_items:
      labor: 390.00
      weatherproofing: 70.00
    material_allowance_net: 180.00
    scope: "Hinges and latch included in work; waste removal excluded"
    tax: "Not stated"
    timing: "Approximately two weeks after acceptance"
```

## Expected comparison

| Required work | ALDER-1 | BIRCH-1 | CEDAR-1 |
| --- | --- | --- | --- |
| Refit hinges | Included | Included | Included |
| Replace latch | Included | Included | Included, materials allowance |
| Weatherproof repaired area | Included | Included | Included |
| Remove waste | Included | Included | Excluded |

| Quote | Comparable cost evidence | Uncertainty |
| --- | --- | --- |
| ALDER-1 | £760 net + £152 stated tax = £912 all-in | Proposed start still needs agreement |
| BIRCH-1 | £980 all-in for required work | Start not agreed |
| CEDAR-1 | £460 fixed net + £180 material allowance = £640 conditional net subtotal | Tax unknown; waste excluded; materials may exceed allowance |

Alder is £68 below Birch for the complete required scope as described. Birch's £60 decoration is optional: its optional scenario is £1,040, but the core comparison remains £980. Cedar cannot be called the cheapest complete repair because £640 is neither fixed nor all-in and does not cover waste removal.

All three offers are within their stated validity dates on the comparison date. This does not establish that any start date is reserved.

## Questions to return privately

- Cedar: What is the total for the complete required scope including waste and applicable tax? Is the £180 material allowance capped, and what approval is required if it is exceeded?
- Birch: Which start and completion dates can be confirmed before acceptance?
- Alder: Can the proposed start and expected completion be confirmed, and do any unlisted site assumptions affect the fixed price?

## Arithmetic checks

```text
Alder net = 400 + 250 + 80 + 30 = 760
Alder stated tax = 760 × 0.20 = 152
Alder total = 760 + 152 = 912
Birch core minus Alder core = 980 - 912 = 68
Birch optional scenario = 980 + 60 = 1,040
Cedar fixed net = 390 + 70 = 460
Cedar conditional subtotal = 460 + 180 = 640
```

Expected failure behavior: if Alder's source instead stated a £922 total, retain that stated total, show the £10 arithmetic discrepancy, and ask for clarification. Do not silently rewrite the offer to £912 or treat the mismatch as evidence of dishonesty.
