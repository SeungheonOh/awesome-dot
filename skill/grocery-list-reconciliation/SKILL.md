---
name: grocery-list-reconciliation
description: "Turn selected recipes, target servings and pantry records into a checked shopping list with scaled quantities, supported unit conversions, stock deductions, purchase-pack rounding and visible unknowns. Use for grocery preparation, not buying food or giving dietary guarantees."
---

# Reconcile Recipes Into a Grocery List

Make one usable list from the dishes the user actually selected. Show what to buy, what existing stock covers, optional additions, and the few details that still need checking. Keep the arithmetic traceable without making the user fill out a questionnaire or inspect a ledger to shop.

## Start from the available ingredients

Read the supplied recipes, authorized recipe links/files, requested servings and pantry information. Reuse stated choices. Ask only for a missing fact that changes the result, such as an absent recipe yield or which of two alternatives the user wants. Prepare unaffected items while a question is open.

Capture:

- Recipe name/source and version, original yield, total requested yield, any batch arrangement and intended leftovers
- Each ingredient's original quantity, unit, identity and preparation state; preserve the source line
- Ingredients marked optional, “to taste,” divided between steps, or offered as alternatives
- Pantry quantity, compatible form/unit, date or confirmation, reservations for other uses, and whether the user says it is available for this plan
- Known package sizes, count/weight basis and acceptable purchasing options, if supplied or researched for this task
- Requested list destination and whether the user wants a new list, additions, or an update to an existing one

If recipes are linked but inaccessible, request the needed recipe text; do not substitute a similar recipe. If yield means “makes 12 pieces” rather than “serves 4,” preserve that basis until a portion conversion is supplied. Do not count planned leftovers twice when the requested servings already include them.

A missing pantry record means “stock not checked,” not confirmed zero. A recipe may still produce a provisional full-need list. An old “some rice” note cannot justify a numeric deduction. Use the user's current availability statement without claiming to verify freshness or food safety.

## 1. Scale each recipe before combining it

Assign a small source ID to each recipe and ingredient line. For ordinary scalable ingredients:

```text
scale factor = total requested yield / source yield
scaled amount = source amount × scale factor
```

Resolve whether a stated yield is total or per batch before scaling. Eight total servings made in two four-serving batches still means eight servings; the batch arrangement does not multiply the total again. If the user explicitly asks for six servings per batch across two batches, first calculate twelve total servings. Preserve batch-specific exceptions from the recipe separately.

Use exact fractions or decimal arithmetic; retain unrounded amounts until purchasing. A factor of 1.25 is valid. Do not round each dish to whole onions, cans or bottles before consolidating. Counts such as half an onion can remain fractional preparation quantities; an indivisible ingredient or recipe that requires whole eggs may need a user choice about batch size or a recipe-supported adjustment.

- Apply the recipe's explicit scaling exceptions. “Oil as needed,” cooking water, baking-pan size, timings and temperatures do not automatically scale like measured ingredients
- Keep unknown or qualitative amounts as unknown; never replace “to taste” with zero or a guessed teaspoon
- Check repeated ingredient mentions: “2 tbsp oil, divided” plus instructions using those 2 tbsp is one source quantity, not three additions
- Preserve optional amounts separately. For “A or B,” select the user's chosen branch; otherwise expose the choice without adding both to the required total
- Suggest substitutions only when useful; do not silently use them to eliminate a shortage or infer their equivalence

## 2. Merge identities, not just similar names

A grocery identity includes the ingredient, relevant variety and required form. Merge compatible lines, retaining every source contribution. Keep dry versus cooked rice, fresh versus canned tomatoes, tomato paste versus chopped tomatoes, sweetened versus unsweetened milk, and drained versus undrained contents distinct unless the recipe or user supplies a valid equivalence.

Normalize units only with evidence:

- Exact same-dimension conversions, such as kilograms to grams, can be applied directly
- Resolve ambiguous units such as a cup, tablespoon or ounce from the source convention before converting; retain the original measure if its system is unclear
- A mass-to-volume conversion needs an ingredient- and form-specific density or a relevant labeled equivalence; do not use water's density for other ingredients
- A count-to-mass conversion needs the relevant item size or measured yield. One lemon is not a known volume of juice; one clove is not a known mass of garlic
- A can, jar or bunch needs its actual size and the relevant usable yield. Net can mass does not establish drained mass. Keep “3/4 can, size unknown” separate from milliliters or grams
- Show unlike supported quantities side by side when conversion is unavailable; do not pretend their sum is a single number

Record the conversion basis beside affected lines. Only source-confirmed aliases may share a row. Do not translate a brand-specific or dietary-specific ingredient into a generic item if that could change what is purchased.

## 3. Deduct available stock once

Aggregate the required amounts first. Match stock to the same ingredient identity, form and measurement basis. Subtract only confirmed usable quantities available for this plan, after any reservations. If pantry records conflict or may refer to the same container, resolve the duplication rather than summing them.

For each compatible quantity:

```text
allocated stock = min(required amount, available compatible stock)
shopping shortfall = required amount - allocated stock
unused pantry stock = available compatible stock - allocated stock
```

Deduct a shared pantry quantity once across the plan, not once per dish. Keep an allocation note when only some dishes can use that stock. Optional ingredients must not consume stock needed by required ingredients unless the user selected them. A package's total weight, an estimated remaining fraction and a measured remainder are different evidence; prefer the current measured or user-confirmed quantity.

If pantry stock is “100 ml coconut milk” but the recipe needs an unknown-size can, retain both values and ask for the can size. A quantity uncertainty does not disappear just because the user owns some of the ingredient.

## 4. Turn shortfalls into purchase quantities

Keep recipe need, stock used, purchase quantity and expected surplus distinct. When the relevant package size is evidenced:

```text
packages to buy = ceiling(shopping shortfall / usable amount per package)
purchased usable amount = packages to buy × usable amount per package
left after recipes = unused pantry stock + purchased usable amount - shopping shortfall
```

A zero shortfall means zero packages. A loose item sold individually can use a one-item purchase unit; a weight-based counter may allow the exact shortfall. If several acceptable pack sizes exist, use the user's stated preference or show a small useful choice; don't claim cheapest without current prices or minimal waste without comparing the feasible sizes.

Round only at the actual purchase step. Distinguish “2 × 400 g net cans, each yielding 240 g drained” from “480 g cans.” Mark package sizes and availability as unverified if not checked. Unknown usable yield means the purchase count is provisional or unresolved. Do not add a default spare pack or pantry restock unless requested.

Leave uncertain ingredients in a short “check before shopping” section with their known amount and the precise missing fact. Group the rest by ordinary store sections if that helps; don't let an ambiguous garnish block a clear rice purchase.

## 5. Check the list against the sources

Before presenting or saving:

- Map every recipe ingredient to a required row, optional row, selected alternative, deliberately excluded ingredient or unresolved item; no source line silently disappears
- Recompute each recipe's factor and each merged row from its source contributions
- Check that matched units and ingredient forms really agree and that each pantry quantity was used at most once
- Confirm that stock allocations and shortfalls are nonnegative and the known purchases cover the known shortfalls
- Reconcile expected leftovers independently. Keep unquantified ingredients outside numeric completeness claims
- If a serving, recipe or substitution changed, recompute all affected shared ingredients from source rows; don't patch only the obvious new item

Make the consumer-facing list brief: item/form, purchase quantity, and a useful note about package basis or uncertainty. Put arithmetic/source detail below it or in a linked companion only when helpful. Say “known measured ingredients reconciled; coconut-milk size still needed,” rather than calling an unresolved plan complete.

## 6. Save within the requested destination

If the user asked to save to an already-authorized list destination, do so using the available connector or supported app flow. Preserve existing unrelated entries and checked-off state; don't clear or replace a list unless that is what the user requested. Before retrying an uncertain write, read back to avoid duplicate entries.

Reopen the saved list and verify item identity, quantities, notes and optional/unknown distinctions. Report a verified link or list name and what remains unresolved. If saving is blocked, deliver the useful list in conversation and explain the narrow blocker; don't claim it was saved.

List preparation does not authorize checkout, purchases, subscriptions, pantry deletion or sharing with a new audience. Respect stated dietary constraints, but do not promise allergen safety, cross-contact prevention or nutritional/medical suitability. Product labels and suitability decisions may still need the user's check; keep private health reasons out of an ordinary shared grocery list.

## Worked check

[The fictional example](example.md) contains two recipes, fractional scaling, shared ingredients, confirmed stock, two-can rounding, an unknown-size can and an optional garnish. Its executable check covers every source ingredient and demonstrates where numeric reconciliation must stop. Use real user inputs in practice; the sample is not a recipe recommendation or a live shopping-list write.

A [fresh-input rehearsal](rehearsal/result.md) checks total versus per-batch yields, a duplicate pantry record, reservations, dry/cooked identity boundaries and unresolved stock/units. Its [input and arithmetic checks](rehearsal/verification.md) make the result inspectable without a shopping integration.
