---
name: repair-quote-comparison
description: "Compare household repair quotes on a common scope, expose missing costs and assumptions, and prepare questions before the user chooses a supplier."
---

# Compare Repair Quotes on the Same Scope

Turn differently worded quotations into an evidence-backed decision sheet. The useful result is an explanation of what each price buys, what could increase it and which question would resolve the biggest uncertainty.

## When to use

Use when a person has competing quotes for the same household repair or a revised quote they want checked against an earlier version. This is document comparison, not a site inspection, technical diagnosis or authority to accept an offer. Use the actual authorized quotes and produce the completed comparison in the requested private destination. A price comparison does not require sharing home details with a new service.

## Required inputs

Collect what is available in a small intake record:

- Repair outcome and mandatory work, expressed independently of any supplier's wording
- Sanitized quote files or excerpts, supplier labels, issue dates, versions and validity dates
- Confirmed measurements and site facts, with their source; separate estimates and supplier assumptions
- User priorities such as total price certainty, finish, completion window, cleanup and warranty coverage
- Comparison date and desired private output format

Ask only for missing facts that change the comparison. Preserve an unpriced requirement as unknown; do not delay useful scope extraction while waiting for every field. Home addresses, entry arrangements, bank details and signatures are unnecessary for the decision sheet.

## Workflow

### Build a traceable quote ledger

1. Read each document using an available file reader. Keep the original unchanged. Assign a stable quote reference and record page or section references for every price, exclusion and material condition. If OCR is necessary, compare important amounts and negations against the original page. A dropped “not” can reverse the meaning of a scope item.
2. Extract supplier, document version, currency, validity, scope, quantity, materials specification, labor, tax treatment, disposal, preparation, finish, cleanup, scheduling statements, payment terms and warranty wording. Label each amount as fixed, estimate, allowance, optional, provisional or unknown. A deposit normally forms part of the quoted total; do not add it again unless the document explicitly describes a separate charge.
3. Compare visible arithmetic with the supplier's stated total. Keep a mismatch in the exceptions list instead of silently correcting their offer. If a revised quote exists, show exactly which prior version it replaces and whether the change affects scope, price or assumptions.

### Normalize the job before comparing prices

4. Build a row for each mandatory requirement. For each supplier use included, excluded, optional, conditional or unspecified, with its evidence reference. “Repair the gate” does not prove that finishing or waste removal is included. Distinguish equivalent outcomes from different methods, material grades or replacement scope; ask for clarification when equivalence depends on professional judgment.
5. Construct a cost bridge for each quote: mandatory fixed items, stated mandatory charges, documented tax, allowances and optional additions. Add amounts only within the same currency and consistent tax basis. Keep an unknown component visibly unknown rather than substituting zero. Do not estimate missing tax from geography or invent an allowance overrun probability. A conditional subtotal is not an all-in price.
6. Check availability and validity as of the comparison date. Separate promised completion dates, approximate lead times and dates contingent on approval or material arrival. An expired offer can remain useful evidence, but its price must be labeled as needing reconfirmation. Read warranty and cancellation language as quoted commercial terms; do not assert legal enforceability.

### Turn uncertainty into a useful decision

7. Identify which quotes meet the mandatory scope with sufficiently complete evidence. Among those, explain price differences and the user's stated priorities. If no weights were supplied, use tradeoffs rather than invented scores. If weights were supplied, disclose the scoring scale, keep hard requirements as gates, and show whether a reasonable change in weights changes the result. Unknowns must not earn favorable scores.
8. Draft supplier-specific questions in the private output. Ask about the highest-impact gaps first: whether a missing task is included, whether an allowance is capped, what makes the estimate change, or which tax and disposal charges apply. Keep questions private unless sending them to the identified suppliers is already part of the authorized request. If that routine clarification is authorized, send only the relevant questions through the available communication app and report what was actually sent. Do not ask for the same authorization again. End with the smallest unresolved decision or missing fact, not a claim that a supplier has been selected.

## Output contract

Return a common-scope matrix, cost bridges preserving original currency and price types, a concise tradeoff summary, and prioritized clarification questions. Every material conclusion must link to a quote reference. Include unresolved site assumptions and any expired or unreadable evidence. An editable sheet is useful when there are many line items; a short Markdown or document comparison is sufficient for a small job.

## Verification

- Recalculate each fully specified subtotal and total independently; report discrepancies rather than changing the quote
- Confirm every mandatory requirement appears once in the scope matrix and that optional work is outside the core comparison
- Check that tax-inclusive and tax-exclusive values are not compared as equivalent totals
- Test whether removing an optional add-on changes only the optional scenario, and whether an unknown mandatory charge prevents an all-in conclusion
- Reopen the final artifact and inspect readable labels, complete source references and visible unknowns; test formulas if a workbook is produced

The [fictional worked example](example.md) shows why a low subtotal with excluded work cannot be ranked as the cheapest complete repair.

## Stop and ask

Pause a recommendation when an unreadable term, missing mandatory item, disputed measurement or safety-critical site condition would determine the result. Continue extracting unaffected evidence. Do not diagnose structural, electrical or other hazardous problems from quotes. A comparison request alone does not authorize supplier contact, bookings, accepting terms, deposits or document sharing. Honor an explicit authorized extension without redundant confirmation, while retaining any required approval for commitments, payments or sensitive sharing. If the destination for the finished comparison is already authorized, save it there and verify the result.

## Example request

```text
dot, compare these repair quotes for my garden gate. I need the same usable result from each: secure the hinges, replace the latch, weatherproof the repaired area and remove the waste. Use the supplied measurements, but show any supplier assumption that differs. Compare the complete cost and how firm each price is, keep optional decoration separate, and draft the questions I should resolve before choosing. Keep everything private and do not contact or commit to a supplier.
```

## Evidence status

The example uses fictional documents and checkable arithmetic. It establishes expected comparison behavior, not actual supplier availability, site suitability or a completed repair.
