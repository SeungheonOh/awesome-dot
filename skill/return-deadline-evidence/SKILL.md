---
name: return-deadline-evidence
description: "Establish a retail item's evidenced return deadline, distinguish request, shipping and receipt cutoffs, and prepare the next step without initiating a return."
---

# Find the Return Deadline That Actually Matters

Resolve the small but consequential questions hidden in a return policy: which event starts the clock, what must happen by the deadline, and which terms apply to this purchase.

## When to use

Use when a person wants to know whether they still have time to return or exchange an item, or needs a checklist before deciding. This workflow completes the evidence analysis and a practical next step using real authorized purchase records. An eligibility-check request alone does not authorize a return submission, merchant contact or postage purchase; it also cannot establish acceptance. It does not determine statutory rights or settle a contract dispute.

## Required inputs

Create an intake record with merchant, country or region, sanitized item description and category, desired outcome, purchase date, delivery evidence, item condition and assessment date. Attach order-specific terms when available. Record timezone when a cutoff time matters and whether the purchase involved a marketplace seller, store or direct merchant.

Use order and receipt identifiers only within the authorized source when necessary to locate the item; omit them from the summary. Do not request payment credentials, a home address or a full account export for a date calculation. If purchase and delivery are both possible triggers, retain both rather than selecting one early.

## Workflow

### Establish applicable evidence

1. Read the supplied purchase record, delivery record and terms. Give each source a short reference, date and page or section. Distinguish order placed, payment processed, shipped, delivered, collected and authorized-return events. A shipment email is not delivery evidence. If the item arrived in multiple parcels, determine which delivery relates to this item.
2. When more evidence is needed, use the available connected merchant record or current official merchant help pages. Record the exact URL, retrieval date, region, sales channel and scope. A policy currently online may differ from the terms attached to an older purchase. Keep purchase-specific evidence and current general guidance in separate fields, and expose conflicts without asserting a legal winner.
3. Extract the policy as a rule record: applicable category and condition; triggering event; window length and unit; whether the trigger day is counted; required action; cutoff time and zone; stated exceptions; fees; packaging and proof requirements. “Return within 30 days” leaves important ambiguity if the source never says whether that means request, dispatch or receipt. Do not fill those gaps from common retail practice.

### Calculate each distinct boundary

4. Build a dated event line and calculate only rules whose required fields are known. For calendar days, show the trigger, counting convention and resulting date. For business days, use the relevant merchant's stated weekend and holiday rules; missing jurisdiction or holiday treatment makes the result provisional. Month-based periods need the source's month-end rule. Use timezone-aware arithmetic for exact times and distinguish calendar-day windows from elapsed-hour windows across clock changes.
5. Keep request-by, authorization expiry, shipped-by and received-by deadlines as separate rows. A successful request would not necessarily satisfy a later receipt requirement. If a second window starts only after an authorization that has not happened, show its formula and a clearly hypothetical example rather than assigning an actual deadline.
6. Compare the assessment date with the evidenced boundary. Use a narrow conclusion: within the stated request window, potentially late, or unresolved. Check category exclusions and item condition before calling an item apparently eligible. Being inside a window does not establish acceptance, warranty coverage or a refund amount.

### Prepare the practical next step

7. List what the user would need before acting: item and accessories, permitted packaging, receipt evidence, condition checks, stated fee and any later shipping obligation. Preserve unknowns. Do not infer a safe last dispatch date from a carrier's typical transit estimate or treat a shipping label as proof of receipt.
8. If uncertainty determines the decision, draft a precise merchant question in the private output. Ask about the actual ambiguity, such as “Does this date mean the request must be submitted or the parcel received?” If the evidenced window has passed, state that fact and the available official contact route without promising discretion or an exception. Do not infer permission for fallback outreach from a request to check dates. When a routine clarification to an identified merchant is already explicitly requested, send only the relevant question and authorized purchase details through a supported channel, then distinguish a sent question from a received answer.

## Output contract

Return an evidence sheet with source applicability, a timeline, one row for each candidate or established deadline, date calculations, visible fees and conditions, unresolved questions and a readiness checklist. The opening summary should identify the most urgent evidenced action boundary without overstating eligibility. Keep sensitive purchase details out of any shareable version.

## Verification

- Recalculate dates independently and show the counting convention; test the adjacent day to catch an off-by-one error
- Confirm the trigger comes from this item's evidence, not a different parcel or an assumed purchase date
- Confirm every calculated deadline states what action it governs and whether it is actual or hypothetical
- Check the exact region, channel, category and policy date before using current guidance
- If no exact cutoff is established, retain a date-level conclusion and an unresolved question rather than inventing 23:59
- Reopen any exported document and confirm source references, qualifications and unresolved costs remain visible

Use the [fictional worked example](example.md) to distinguish an initial request deadline from a later receipt deadline.

## Stop and ask

Ask when the policy trigger, counting convention, applicable terms or condition exception would change the answer. Provide independent preparation work while that remains unresolved. If the user has also requested an action such as asking the merchant a specific question, honor that existing authorization rather than asking again. For a return submission, collection booking or postage purchase, first establish the exact item, destination, required data, applicable terms and any charges, and obtain only the approval still required. Keep the analysis available even if the action is blocked. Save the finished evidence sheet to an already authorized private destination and verify it is readable. Refer disputes about legal rights or contested contract terms to qualified help rather than making a legal determination.

## Example request

```text
dot, use my sanitized receipt, delivery confirmation and attached merchant terms to work out the deadline for returning this lamp. Tell me whether the relevant date is for requesting, shipping or the merchant receiving it. Show the date calculation and any packaging or fee requirements. If the terms are unclear, draft the smallest question that resolves them. Do not start the return or contact anyone.
```

## Evidence status

The example demonstrates calculation and uncertainty handling using invented terms. Live merchant rules, order eligibility and external actions must be checked and reported separately during an actual use.
