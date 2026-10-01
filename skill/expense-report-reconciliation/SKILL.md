---
name: expense-report-reconciliation
description: "Turn authorized receipts, credit notes and a supplied expense policy into a traceable, reconciled expense report with supported, excluded and unresolved amounts; save or submit only within the requested authority."
---

# Reconcile Receipts Into an Expense Report

Produce the requested expense artifact, with every receipt and credit accounted for and every claimed amount tied to evidence and a policy rule. Distinguish “supported under the supplied policy” from employer approval, reimbursement, payment or tax deductibility. This workflow does not make transactions, decide tax treatment or create replacement receipts.

## Establish the reporting boundary

Inspect the authorized material and identify:

- Claimant, reporting period/project, business-purpose evidence and any required cost-center fields
- Receipts, invoices, credit notes and, where available, matching payment/posted-currency records
- Supplied policy version, applicability dates, limits, excluded categories, documentation rules and any written exception authority
- Report currency, permitted conversion evidence, rounding method and whether amounts are reported gross or net
- Desired artifact/template, save location, and whether the task includes preparation, a named-system draft, or submission to a specified recipient
- Any declaration, certification or attestation the submission requires

Ask about missing facts that materially change a claim. Meanwhile, extract readable evidence and prepare unaffected lines. If the policy or its applicability is missing, create an evidence-only draft with eligibility unresolved; do not substitute an assumed company policy. A report total is not a budget and does not prove the evidence set contains every expense in the period.

A request to create and save a report authorizes that ordinary artifact operation within the named destination. Carry it out without redundant approval. It does not authorize new sharing, reimbursement transfers, paying a balance, inventing a business purpose, accepting new terms, or certifying unknown facts.

## 1. Preserve and inventory the evidence

1. Keep originals unchanged. Record source ID, filename or stable service ID, relevant page/region, revision or content digest where available, and extraction method. Work on copies; never edit a receipt to make it fit the policy.
2. Identify each document's role: expense evidence, credit/refund, payment evidence, policy, purpose statement or exception approval. An invoice and its card charge generally support one transaction, not two claimable expenses. A card record alone does not establish purchased items or business purpose.
3. Preserve extracted text alongside normalized fields. Flag unclear characters, totals and dates for source-image inspection. A confidence score is not a substitute for checking a consequential value against the original.
4. Capture merchant, receipt/invoice identifier, transaction date, currency, line items, net/tax/tip/other charges/gross when separately evidenced, payment status and payment method category needed by the template. Keep unnecessary card/account details out of the report.
5. Record purpose exactly as documented, with its source: user statement, project note or other authorized evidence. Use “purpose not provided” when absent. Merchant category, trip proximity or a plausible story does not prove business use.

An unreadable receipt remains in the source register and exceptions. A missing amount is unknown, never zero. Do not request access to unrelated statements or upload receipts to a new extraction service just for convenience.

## 2. Build canonical transactions before summing

Create stable transaction IDs independently of source IDs. Link all supporting sources to each transaction, then investigate potential duplicates using receipt ID, merchant, date, currency, gross amount, itemization and payment reference when available.

- A confirmed duplicate scan/copy supports the same canonical transaction. Preserve both originals, record why they are duplicates, and give the duplicate a zero incremental claim disposition
- Similar merchant/date/amount values are candidates, not proof. Preserve possible repeated purchases; mark the disputed incremental amount unresolved until evidence distinguishes them
- A receipt plus a statement charge is an evidence pair, not a duplicate expense to discard blindly
- A replacement invoice needs an evidenced supersession link. Do not add both, or silently pick the newer file
- A credit note must link to the original transaction or remain an unresolved credit. Do not ignore it because it reduces the claim

Every supplied receipt, credit note and relevant payment record must have a source-to-line mapping. Show allowed, disallowed or unresolved monetary dispositions; for corroborating documents or exact-copy exclusions, identify the canonical line and the zero incremental financial effect. Keep the coverage register separate from summed expense lines so evidence copies cannot inflate totals.

## 3. Normalize money without inventing evidence

Use decimal arithmetic or integer minor units; retain original amounts and currency. Do not infer an ambiguous currency from a symbol alone or add unlike currencies.

For each canonical transaction:

1. Reconcile stated components to gross where the document exposes them. Respect inclusive versus exclusive tax, explicit service fees and tips; do not add tax twice. Preserve a receipt rounding line only when evidenced. Investigate unexplained residuals rather than manufacture a balancing adjustment.
2. Record tax exactly as shown. “Tax not stated,” explicit zero tax and “not applicable under this template” are different. Do not reverse-engineer a tax rate, claim recoverability, assign a jurisdiction or give tax advice. If the template requires an unsupported tax allocation, leave it unresolved for the appropriate reviewer.
3. Convert under the supplied policy. If it uses actual posted card amounts, retain both original currency and posted reporting-currency amount, with statement evidence. Otherwise record the permitted rate source, effective date, direction, precision and policy rule. Do not silently use a convenient current rate.
4. Apply the supplied rounding convention at its specified stage. If none is given and rounding affects a claim or cap, ask; an illustrative calculation can be labeled provisional. Keep unrounded calculations for audit when meaningful.
5. Convert refunds using their own posted evidence or the specified refund conversion rule. An original purchase's rate is not automatically the refund rate. Preserve a negative signed credit and distinguish a credit note from a posted refund; do not count the same credit twice.

If currency conversion is unsupported, retain the original-currency amount and exclude it from a final reporting-currency claim subtotal as unresolved. State that a complete converted total is unavailable. A known credit on a missing or prior-period purchase may require a separate adjustment under policy; do not attach it to an unrelated positive charge just to balance this report.

## 4. Allocate, apply policy and expose decisions

Create one or more allocation lines per canonical transaction. Each line needs source references, amount/currency, purpose evidence, category, policy clause, disposition and reason.

Use these dispositions consistently:

- **Allowed:** evidence supports this amount under the supplied policy; still subject to the normal reviewer/approval process
- **Disallowed:** a documented policy exclusion, personal allocation, cap excess, confirmed already-settled exclusion or duplicate incremental claim
- **Unresolved:** a missing fact, contradictory record, unclear applicability, unapproved exception, uncertain duplicate or unsupported conversion prevents classification

Apply explicit business/personal splits using item-level amounts or a supplied allocation basis. Do not assume equal shares or allocate taxes, tips and service charges arbitrarily. Reconcile allocated gross back to the source gross and disclose an unresolved residual when a reliable split is impossible. A required participant count or business-purpose statement must be evidenced before applying a per-person limit.

Apply caps at the actual policy unit: item, meal, person, day, journey or report. Group related receipts when the limit requires it; do not give each receipt a fresh allowance. Record excluded excess separately. If category-specific caps depend on ambiguous classification, show the alternatives and ask for the smallest missing decision.

Link a refund to the refunded items and their original allocation. Reverse the relevant allowed, disallowed and/or unresolved portions under the policy, rather than reducing an arbitrary subtotal. Partial refunds need an item match or evidenced allocation. Where a cap and a later credit interact, recompute the transaction's eligible net amount under the supplied rule; do not automatically reverse the credit's full face value from an already-capped claim.

Preserve explicit personal exclusions even when an overall receipt looks work-related. Keep unsigned/unsupported exceptions unresolved. Never mark “approved” because a report was generated or a form accepted it.

## 5. Reconcile independent views

Validate from original evidence, not only from the transformed report:

```text
Unique transaction net amount = purchases + signed credits
Unique transaction net amount = allowed + disallowed + unresolved allocations
Incremental claim of confirmed duplicate evidence = 0
Proposed claim = allowed allocations, including applicable negative adjustments
```

Run these equations separately by original currency and, when conversion is fully supported, reporting currency. Never compare a mixed-currency source sum to a converted total. Preserve currencies with unknown amounts/conversions in a separate coverage statement.

Also check:

- Every source is linked; no source silently disappears and no statement line becomes an extra expense
- Each canonical transaction's allocations sum to its signed amount; known refunds and policy exclusions remain visible
- Component tax appears once in the source record, not once per split and then summed repeatedly
- Each allowed line has amount evidence, required purpose evidence and a policy basis
- Duplicates and capped groups obey their confirmed grouping rule
- Totals match any genuinely comparable supplied control; explain missing scope or dates instead of forcing agreement

If the policy needs a decision, the deliverable can be a reconciled draft with exceptions. A final claim should not include unresolved amounts. If a missing credit or duplicate could overstate an otherwise allowed subtotal, keep the affected claim group provisional rather than presenting it as ready to submit.

## 6. Save the requested artifact and complete authorized delivery

Use the requested native template or format when tools can preserve it. Include the source register, allocation detail, reconciliation, exceptions and claim subtotal, either in the report or approved companion files. Preserve formulas and required fields in a workbook; inspect rendered output when preparing a document. Do not substitute a flattened export for a required working spreadsheet without making the limitation clear.

Save to the authorized destination, reopen the saved artifact and repeat key checks from the readback: source coverage, signed credits, totals, unresolved flags, purpose attribution and identifier preservation. Keep source originals intact. If updating an existing report, recheck its revision before writing and avoid overwriting newer edits. Inspect uncertain write outcomes before retrying.

Before an authorized submission, verify the exact destination, recipient/audience, included report/receipts and any required declaration. Existing explicit authority for those data and that ordinary submission is sufficient; do not ask again solely because sending is involved. Stop only the dependent step if the site introduces a different recipient, sensitive data not covered, a payment, new agreement or unsupported attestation. State exactly what needs authorization. Never make an attestation the available facts cannot support; have the user review and perform a personal certification when required.

Read back the submitted status and reference ID when available. Distinguish “saved,” “draft in expense system,” “submitted,” “approved” and “paid.” A successful upload is not evidence of reimbursement. Do not repeatedly submit after a timeout; inspect for an existing report first.

## Completion record

Deliver the actual saved artifact/link, report currency and proposed claim total, excluded and unresolved totals, the material outstanding questions, and verified delivery status. State any conversion, source-reading or format limitation. Do not expose unnecessary personal financial details in a summary.

Use [the fictional worked example](example.md) to check a multi-receipt case with a duplicate, item split, cap, separately converted refund and unknown purpose. Its local CSV readback demonstrates the arithmetic and evidence mapping, not a real claim, tax determination or live submission.
