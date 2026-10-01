---
name: purchase-offer-comparison
description: "Compare equivalent retail offers for an exact product and quantity using current delivered costs, promotion eligibility, delivery constraints and visible return terms."
---

# Compare Exact Retail Offers

Find the best supported offer for the user's actual purchase requirement. The result should explain the payable total, whether the exact quantity and variant are available, what conditions could change the price, and which unknowns prevent a firm choice.

This is retail-offer comparison. It is not comparison of repair work, labor scope or estimates for a service. Comparing offers alone does not authorize account creation, membership enrollment, contacting merchants or purchasing.

## Intake

Use the request and authorized sources to establish:

- Exact product or acceptable specification: model/part number, capacity, dimensions, color if material, region/plug, included components, condition and acceptable substitutions
- Required usable quantity, acceptable pack sizes and whether buying surplus is acceptable
- Delivery or pickup destination at the minimum detail needed, required arrival date, shipping constraints and whether a delivery estimate is acceptable
- Budget including mandatory charges, comparison currency and any priorities beyond price
- Existing memberships, coupon eligibility, payment constraints or credits the user wants considered; distinguish confirmed from unknown eligibility
- Any merchants already selected and whether the task is comparison only or an already-requested purchase

Do not ask for a full address, credentials or payment information merely to compare public offers. If a precise checkout quote requires personal information, use only the authorized information and destination under applicable privacy permissions, or ask for the missing authority. Continue with labeled incomplete totals for other offers.

If the product specification is broad, first clarify the requirement that changes compatibility. Do not silently turn a search for an exact replacement into a recommendation for a different model.

## Workflow

### 1. Record exact offer evidence

Use current merchant/product sources and available authorized checkout evidence. Record a timestamp with time zone, URL or source document reference, seller identity, fulfillment party, exact listing variant, quantity available and quoted destination. A marketplace's name is not the seller's identity. A search snippet or old screenshot is a lead; it does not establish present checkout price or stock.

Assign an offer ID and retain source references for each material field. When a product page and cart disagree, preserve both observations and use the latest applicable checkout quote only after verifying that variant, seller, quantity, destination and promotion conditions match. If a price, stock check or policy cannot be retrieved, label it unverified rather than filling it from another seller's page.

### 2. Gate compatibility before comparing totals

Build an exact-match row for each requirement. Check capacity, size, model suffix, regional version, color where required, bundle contents, warranty variant, condition and seller-specific restrictions. “Similar” is not equivalent. A compatible alternative may be shown separately if useful, with the mismatch clearly stated, but it cannot win the exact-product comparison.

Normalize packs into delivered usable units. For a one-unit listing and a two-pack, state both the number of packs ordered and the units supplied. Do not compare one pack against a required two units. If packs force surplus, show the full cash cost and surplus; do not pretend that prorated unit cost is the amount payable. If surplus is unacceptable, exclude that offer from the feasible set.

Check that the required quantity is orderable, not merely that the page says “in stock.” A listing with unknown stock remains unverified. Check shipping restrictions and expected arrival, including the difference between dispatch time and delivery time. A stated date range is an estimate unless explicitly guaranteed by the merchant; do not create your own guarantee.

### 3. Build a delivered-cost bridge

For each exact offer, compute using decimal currency arithmetic:

```text
item cost = payable packs × price per pack
payable delivered total = item cost
                         − applicable immediate discount
                         + mandatory options or required components
                         + mandatory merchant/order fees
                         + chosen feasible delivery charge
                         + tax not already included
                         + other unavoidable, evidenced charges
```

Keep the bridge consistent with the merchant's documented tax and rounding basis. Tax-inclusive prices must not receive tax a second time. If a source supplies only a tax amount, use and label that quote rather than inventing a jurisdictional rule. Distinguish per-line from order-level rounding. Do not derive missing tax, duties or fees solely from a geographic guess.

Choose the least expensive delivery option that meets the user's actual constraints, not an unusable slower option. Include mandatory packaging, adapters or options only when required for the specified purchase; leave optional warranties, donations and upgrades outside the core total. Split shipments can have separate charges and arrival dates. If an indispensable component's price is unknown, the complete total is unknown.

An unknown charge is not zero. Show a known subtotal and the missing components without ranking it as a complete delivered total. Zero shipping or tax needs evidence. When the merchant states a complete payable total without exposing every component, retain that quoted total and say which breakdown is unavailable; do not manufacture a reconciliation.

Preserve source currency. If cross-currency comparison is necessary, disclose the dated conversion source, settlement assumptions and unresolved payment or foreign-exchange fees. A converted estimate is not a verified payable total in the user's currency. Show non-price constraints separately rather than hiding them in an invented numerical score.

### 4. Separate unconditional and conditional offers

Check each promotion's eligible product, seller, quantity, destination, minimum spend, expiry/time zone, exclusions, usage limits and combination rules. A banner does not prove that a code applies to this cart. Recalculate any shipping threshold and tax basis affected by a discount according to the actual terms. Do not stack codes unless permitted and demonstrated.

- **Confirmed applicable:** terms match this offer and the user's eligibility is established; show the discount and source
- **Conditional:** a required fact such as existing membership or first-order status is unknown; show a separate scenario, never the default payable price
- **Ineligible or expired:** leave the discount out and explain the reason
- **Unverified at checkout:** preserve that uncertainty even if the terms look compatible; recheck the actual cart before any commitment

Already-paid membership is not a new checkout charge, but it must actually apply. A new membership, trial, newsletter signup or account is an additional decision, with its own cost, renewal and permissions. Do not enroll automatically to make an offer look cheaper. If the user explicitly wants a new-membership scenario, include the required membership cost and recurring commitment rather than allocating it across speculative future purchases.

Keep gift cards, store credit, rewards and payment instruments distinct from price reductions. Show pre-credit purchase cost and cash due if relevant; a consumed balance still has value. Future cashback, points or rebates do not reduce today's payable total. Note their conditions separately and do not promise receipt.

### 5. Compare feasible offers and commercial tradeoffs

Rank only offers with sufficient evidence for the exact variant, quantity, delivered cost and required delivery constraints. Describe the best supported offer **as of the recorded check**, not the cheapest offer everywhere. If all totals or availability are unresolved, return the partial comparison and the next fact needed; a winner is not mandatory.

Read visible return conditions relevant to the proposed purchase: return window and its trigger, opened/unopened restrictions, final-sale exclusions, return shipping, restocking or label fees, original-shipping refund treatment and seller versus marketplace process. Record what the source actually says; do not claim legal enforceability or infer statutory rights. An absent policy is unknown, not generous. Potential return costs are a separate risk comparison, not added to a purchase the user may keep.

Explain meaningful differences in delivery confidence, return friction, condition and seller terms alongside the price gap. If a conditional discount changes the winner, state the precise condition and show both outcomes. Do not recommend spending extra merely to unlock a discount without showing the resulting full cash cost and user relevance.

### 6. Handle an already-requested purchase carefully

When purchase is already authorized, carry forward the exact confirmed offer rather than asking the user to repeat the same authority. Immediately before commitment, verify seller, item/variant, quantity, destination/service method, final total and currency, payment type, any subscription or recurring commitment, and visible cancellation/return restrictions. Check that the offer remains within the user's approved total limit and approved scope.

Follow the applicable transaction, terms and privacy approvals. Disclose any newly required agreement through its actual link and obtain any required acceptance. Pause for a changed seller, incompatible variant, missing quantity, unexpected recurring charge, price over the approved cap or new material term. Use the required secure handoff for highly sensitive payment or credential data; never solicit it in a comparison document.

Do not accept a new membership or account, save payment details, replace the product, purchase, or promise availability merely because the cheapest scenario depends on it. If the comparison was the entire request, stop with the recommendation and open questions. If an authorized purchase succeeds, verify the confirmation and report the real order status; an accepted cart or clicked button alone is not completion.

## Output contract

Provide a concise recommendation or explain why no firm recommendation is possible, then one row per offer:

| Field | Required content |
|---|---|
| Identity | Merchant/seller, offer link, model/variant/condition, timestamp |
| Quantity | Pack size × packs, usable units, surplus if any |
| Compatibility | Exact / incompatible / unresolved, with the decisive source |
| Cost | Items, discount, mandatory charges, delivery, tax treatment, delivered total or named unknowns |
| Eligibility | Baseline and conditional promotion scenarios with their source and expiry |
| Fulfillment | Required stock evidence, destination, arrival range and qualification |
| Returns | Visible window, trigger, exclusions and fees, or unknown |
| Decision | Feasible / conditional / unresolved / excluded; reason and next check |

Keep expired observations or incompatible variants visible as exclusions rather than silently dropping inconvenient evidence. Link material claims to their specific sources. Give the user the smallest remaining question that would change the decision.

## Verification and stopping rules

- Reconcile quantity and variant before checking prices; incompatible cheap offers cannot win
- Recalculate completed bridges with Decimal-style arithmetic and the source's rounding rule; report quoted-total mismatches rather than silently changing an offer
- Check discounts against documented terms and established eligibility, including a no-discount baseline
- Preserve every unknown mandatory cost and unavailable stock check; neither may become zero or “in stock”
- Verify delivery means arrival where required, and keep estimates distinct from guarantees
- Keep return costs, optional extras, future rewards and credits distinct from current delivered price
- Reopen the completed comparison and check totals, labels, sources and as-of time

Stop the dependent recommendation or purchase when a missing fact could reverse feasibility or exceed authorization. Continue comparison of unaffected offers. On blocked pages, use other authorized sources or request an exact quote; do not bypass access restrictions, create accounts or transmit personal details without the required authority.

The [fictional worked example](example.md) checks a two-unit versus two-pack comparison, a conditional member discount, an incompatible capacity and an incomplete offer using Decimal arithmetic.
