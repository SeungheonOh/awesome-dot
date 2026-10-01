# Fictional grocery list

## Buy

- **Chickpeas:** 4 × 400 g net cans, each yielding 240 g drained. Buy 960 g drained; **220 g usable surplus** after the plan
- **Dry rice:** 1 × 250 g bag; **200 g usable surplus**
- **Cooked rice:** 2 × 400 g pouches; **300 g usable surplus**
- **Fresh tomatoes:** 100 g, sold by exact weight; **no surplus**
- **Rolled oats:** 1 × 100 g bag; **70 g usable surplus**
- **Honey, provisional:** 45 g by exact weight if no pantry stock is allocated. Stock has not been checked; buying the full need leaves no purchased honey surplus, but total pantry surplus is unknown

**Already covered:** Peanut butter needs 90 g; use pantry stock and leave **110 g available**. Buy none

## Check before shopping

**Lemon juice:** The recipes need **4 tablespoons**, and **40 ml** is available. Confirm how many milliliters the recipe means by one tablespoon before comparing these quantities or calculating stock use, shortfall or surplus. If more is needed, a purchase unit is also needed to determine package count

Chocolate chips are excluded. Almond butter is the unselected alternative. Neither is on the required list

## Source and arithmetic note

All recipes, stock statements and purchase units are fictional and supplied in the [preparation packet](input.md). This is the reviewed result of one synthetic rehearsal; [verification](verification.md) describes the actual checks and limits. Prices and live availability are unverified. Surplus means usable stock left after this plan, **excluding all reservations**

### Scaling and ingredient coverage

| Source | Factor and scaled ingredients | Disposition |
|---|---|---|
| R1, bowl base | 8 total servings ÷ 4 = **2**. R1a: 600 g drained chickpeas; R1b: 400 g dry rice; R1c: 4 tablespoons lemon juice | Chickpeas and dry rice reconciled below; lemon juice unresolved |
| R2, warm salad | (4 servings per batch × 2 batches) ÷ 2 = **4**. R2a: 400 g drained chickpeas; R2b: 1,000 g cooked rice; R2c: 600 g fresh tomatoes | All reconciled below |
| R3, oat bites | 18 pieces ÷ 12 = **1.5**. R3a: 180 g rolled oats; R3b: 90 g peanut butter; R3c: 45 g honey; R3d: 15 g optional chocolate chips | Oats and selected peanut butter reconciled; honey provisional; almond-butter alternative unselected; chocolate chips excluded |

R1's two batches and intended leftovers are already included in its eight total servings. R3 remains measured in pieces; no servings conversion is used

### Stock allocation and purchases

All quantities below are grams, on the stated ingredient basis. Lemon juice is kept outside this numeric reconciliation

| Ingredient / source | Need | Available after reservations | Stock used | Shortfall | Purchase basis / amount | Usable surplus |
|---|---:|---:|---:|---:|---|---:|
| Drained chickpeas, R1a + R2a | 600 + 400 = 1,000 | P1: 360 − 100 = 260 | 260 | 740 | B1: ceiling(740 ÷ 240) = 4 cans; 960 drained | 220 |
| Dry rice, R1b | 400 | P3: 500 − 150 = 350 | 350 | 50 | B2: ceiling(50 ÷ 250) = 1 bag; 250 | 200 |
| Cooked rice, R2b | 1,000 | P4: 500 | 500 | 500 | B3: ceiling(500 ÷ 400) = 2 pouches; 800 | 300 |
| Fresh tomatoes, R2c | 600 | P5: 700 − 200 = 500 | 500 | 100 | B4: exact weight, 100 | 0 |
| Rolled oats, R3a | 180 | P7: 200 − 50 = 150 | 150 | 30 | B5: ceiling(30 ÷ 100) = 1 bag; 100 | 70 |
| Peanut butter, R3b | 90 | P8: 200 | 90 | 0 | None | 110 |
| Honey, R3c | 45 | Unchecked | None allocated pending check | Undetermined; provisional full need 45 | B6: provisional exact weight, 45 | Purchased surplus 0 under full-need purchase; total unknown |

- P2 duplicates P1's same chickpea tub; it adds no stock. The available 260 g is deducted once from the combined 1,000 g need
- Dry rice and cooked rice remain separate. P6's 40 ml lemon juice remains unallocated because the tablespoon convention is missing
- For each fully quantified row: stock used = min(need, available); shortfall = need − stock used; surplus = available − stock used + purchase − shortfall
- Independent surplus checks: chickpeas 260 + 960 − 1,000 = 220; dry rice 350 + 250 − 400 = 200; cooked rice 500 + 800 − 1,000 = 300; tomatoes 500 + 100 − 600 = 0; oats 150 + 100 − 180 = 70; peanut butter 200 − 90 = 110
- Every ingredient line has a disposition. Known compatible measured quantities are reconciled; honey stock and the lemon-juice measurement gap remain open
