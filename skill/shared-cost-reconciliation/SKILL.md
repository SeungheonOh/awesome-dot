---
name: shared-cost-reconciliation
description: "Reconcile a group's expenses, explicit shares, refunds and recorded repayments into per-person balances and a reviewable settlement proposal, keeping unresolved allocations and currencies separate."
---

# Reconcile Shared Costs

Turn the supplied receipts and payment records into a clear answer to who paid, who benefited, and what remains owed. Produce the actual ledger and balance sheet in the requested format, with a concise settlement proposal when the evidence supports one. This is a shared-obligation workflow, not an employer expense claim or a budget forecast.

## Establish the rules that change the answer

Use the authorized records, participant labels, reporting cutoff and requested destination. Gather the group's actual allocation rules: equal shares, named amounts, weighted shares, item-level beneficiaries, exclusions, and the rule for distributing indivisible minor units. A payer is not necessarily a beneficiary. Do not infer an equal split merely because several people attended.

Identify currency and precision from the records or a reliable applicable convention; “dollars” may be ambiguous, and not every currency has two decimal places. Keep separate currency ledgers unless the user explicitly supplied or approved the conversion basis, date, fee treatment and rounding. A card's converted amount and its receipt are evidence for one payment, not two expenses.

Retain only identifiers needed to distinguish participants and transactions. Supplied names are ledger labels, not verified payment recipients. Do not infer a recipient account or disclose private receipt details merely because the final balances are useful to the group.

Ask only for a decision-changing missing rule. Continue the supported arithmetic and prepare the useful draft while an answer is missing. Label the affected currency or component provisional rather than silently inventing a share.

## 1. Register evidence without counting it twice

Give each economic event a stable ID and retain its source locators, date/status, currency, amount, payer or refund recipient, beneficiaries, allocation rule and revision. Preserve the underlying records.

Separate three event types:

- **Expense:** a payer's outlay and the corresponding beneficiaries' cost
- **Refund or adjustment:** a reduction or correction tied to an identified expense/item, with its actual cash recipient and affected beneficiaries
- **Repayment between participants:** an already-recorded transfer that changes outstanding balances but creates no new shared expense

Distinguish a receipt, its card posting and a forwarded copy from separate purchases. Repeated exports with the same stable event ID add provenance, not another amount. Similar merchant/amount/date alone is insufficient to merge events. Hold conflicting versions until the applicable correction is clear; do not choose whichever total makes the ledger balance.

For repayments, preserve reported, confirmed, pending, failed and unknown outcomes. Apply only the completion state supported by the source and the user's accounting boundary. State whether that is a supplied report or an independently read payment record. A proposed transfer or pending payment is not completed settlement. Record each transfer once with both endpoints, even when payer and recipient each supplied a copy.

## 2. Allocate each supported expense

Use exact decimal or integer-minor-unit arithmetic. For a weighted split, check that all named participants exist, weights are nonnegative, the total weight is positive, and any fixed amounts plus residual shares cover exactly the intended expense.

Calculate the unrounded shares before rounding. Use the group's rounding rule when supplied. If no rule was supplied, a disclosed deterministic minor-unit allocation can be proposed in the private draft; show who receives the indivisible remainder rather than requiring the user to invent a method before any work proceeds. Keep that proposal distinguishable from an agreed rule. When using an approved or clearly proposed largest-remainder rule, floor the exact nonnegative minor-unit shares and assign residual units to the largest fractional remainders, using the approved stable tie order, or a disclosed proposed order based on the supplied stable participant IDs. Do not silently treat that proposal as agreed or always burden the last person in a display list. Record the rule and the resulting minor-unit allocations so later sorting cannot change them.

Other approved rules may be valid. Apply the specified one consistently and expose any residual that its instructions do not resolve. Never fix a rounding discrepancy by changing the source expense total.

For a refund, use the evidenced item and beneficiary treatment. A refund for one person's item need not be spread across everyone who shared the original receipt. A full reversal should cancel the original recorded allocations exactly; do not reround against a changed participant set. For a partial proportional refund, use that rule only when it is actually supplied or accepted. Retain the fact that the cash recipient may differ from the original payer.

Leave an expense's allocation unresolved when its beneficiaries, split rule, material amount or refund linkage is unknown. Show its known cash evidence separately. A known payer does not make an unknown allocation solvable.

## 3. Build balances in separate views

For each currency, retain these quantities separately:

```text
net expense cash paid = expense outlays - refunds received
net cost share = allocated expenses - allocated refund credits
balance before repayments = net expense cash paid - net cost share
remaining balance = balance before repayments + repayments sent - repayments received
```

A positive remaining balance means the participant should receive money; a negative balance means they owe money under the supplied rules. State this sign convention beside the table. A recorded repayment changes both participants' outstanding positions without changing the group's net expense total. Do not cap a recorded payment at the previous debt; an overpayment can reverse who owes whom.

For a complete ledger, the sum of net expense cash paid equals the sum of net cost shares, and remaining balances sum to zero within each currency. Verify these identities independently, including negative adjustments and zero balances.

When a material event is held, do not force the full view to balance by assigning the gap to an arbitrary person. Show the cash amount, the unresolved allocation and the exact question. A known-subset comparison can remain useful, but label it as a subset; its zero-sum result does not prove the full ledger is complete. Do not present its transfer list as ready for payment. An unaffected currency may still have a complete balance sheet.

## 4. Propose settlement only after the ledger is ready

Check the cutoff, unresolved events, repayment status and any pending transfers before preparing an actionable proposal. Pending transfers may make the next step “verify this outcome” even when all cost shares are known; do not propose paying the same obligation twice.

Pair debtors and creditors within the same currency and allocate amounts that exactly extinguish their supported remaining balances. A deterministic greedy proposal can be easy to inspect, but do not call it the minimum number of transfers or the cheapest plan unless that property was actually established under the user's constraints. Keep fee, recipient and payment-method assumptions visible.

Show payer label, recipient label, currency, amount and the balances the proposal would settle. This is a proposal, not a payment instruction sent to a bank. Do not fabricate account details or mark the proposal paid. This workflow does not initiate transfers; the user completes any payment in their chosen service.

## 5. Review corrections and save the useful result

Present a short review sheet: source totals, per-person balances, held events, pending repayments and the smallest questions needed. Keep the arithmetic detail available underneath or in an accompanying file. A user should be able to challenge an expense or rule without reconstructing the whole calculation.

When a correction arrives, bind it to the affected event/version, preserve the prior value and recompute all affected balances and proposals from the event records. Do not patch only the visible amount someone questioned. Reimporting unchanged evidence or a previously applied repayment must not change the result.

Save to the already-authorized destination when requested. Preserve unrelated sheets, formulas or ledger entries when updating an existing file; use current revisions and supported conditional writes where available. Reopen the saved artifact and check the actual event coverage, currency, amounts, signs, held states and proposal. A failed or uncertain save is not a verified result; inspect it before retrying.

Sharing the ledger needs an authorized audience and data scope. A private calculation request does not authorize group messages, disclosure of receipts, public links or financial transfers. If sharing was explicitly requested within that scope, complete it and verify delivery without asking for the same permission again.

## Output and completion checks

Deliver:

- A source-linked event ledger distinguishing expenses, refunds and repayments
- Explicit allocation rules and minor-unit rounding, including held items
- Per-currency participant balances with the sign convention and completeness status
- A settlement proposal only where justified, otherwise the precise pending evidence or decision
- A short correction trail and an honest save/readback result when an artifact was requested

Check each event once, each allocation sum against its expense/refund, the group conservation identities, repayment direction, currency separation and the absence of unsupported participant/account assumptions. Test a fractional split, a linked refund, a duplicate record and a pending repayment relevant to the actual input.

The [fictional review loop](example.md) shows a missing split resolved by a later clarification, without treating a pending transfer as paid. A [fresh-input rehearsal](rehearsal.md) adds whole-yen weighted shares and a later completed-payment update. These are local fictional checks, not evidence that anyone owes or transferred real money.
