---
id: loan-offer-math-explainer
title: "Loan Offer Math Explainer"
summary: "Explain payment, fee and total-cost differences between fictional fixed-rate loan offers without recommending borrowing."
category: finance
level: intermediate
timebox_minutes: 50
capabilities: ["files"]
tags: ["loan-math", "education", "cost-comparison"]
status: recipe-not-run
---

# Loan Offer Math Explainer

Explain payment, fee and total-cost differences between fictional fixed-rate loan offers without recommending borrowing.

## Scenario

A financial-literacy workshop uses two fictional fixed-rate offers with different fees and terms. Learners need to understand why the smallest monthly payment need not imply the smallest total paid.

## Inputs to prepare

- Synthetic offers with principal, nominal annual rate, term and payment frequency
- Explicit fee treatment, including whether fees are financed or paid separately
- The workshop currency, rounding convention and audience
- Any supplied contractual payment amounts for comparison

## Copy this prompt into dot

```text
dot, explain the arithmetic of [FICTIONAL FIXED-RATE LOAN OFFERS] for [LEARNING AUDIENCE] in [CURRENCY]. Use synthetic terms only. This is educational analysis, not advice to borrow, refinance, choose a lender or accept an offer. Do not access credit records, create accounts, submit applications or initiate transactions.

Confirm principal, nominal annual rate, payment frequency, term and whether each fee is financed or paid upfront. Distinguish the supplied rate from any APR label; do not calculate or certify a legally defined APR. Use a clearly stated periodic-rate convention and a standard fully amortizing model only when the supplied terms fit it. Stop and explain if variable rates, balloon payments or missing terms require a different model.

For each offer, show illustrative periodic payment, interest total, separately paid fees and total cash paid, avoiding double-counted financed fees. Include a short amortization excerpt and reconcile the final balance, allowing an explicit final-payment rounding adjustment. Test a zero-interest example, unequal terms and a fee paid upfront versus financed. Explain why payment size alone is incomplete without choosing an offer. Return formulas, assumptions, source-term references and checks. Label all results illustrative and keep the materials private.
```

## Iterate with a purpose

### 1. Isolate the term effect

```text
Hold the synthetic rate and principal constant while varying only the term. Explain the arithmetic tradeoff between periodic payment and total interest.
```

### 2. Audit fee treatment

```text
Trace one fee through principal, cash received and total paid, comparing financed and upfront versions without counting it twice.
```

### 3. Prepare a workshop example

```text
Write a step-by-step explanation of one fictional amortization row, with a learner check and a separately labeled answer.
```

## Expected deliverables

- A side-by-side educational offer comparison
- A formula sheet with periodic-rate and rounding conventions
- An amortization excerpt and final-balance check
- A list of excluded or incompatible loan features

## Acceptance checks

- The model uses only terms explicitly supplied in the fictional offers
- Financed fees are included in principal exactly once
- A zero-interest case uses a valid non-dividing-by-zero formula
- Total paid separates repayments from upfront fees
- The final balance is reconciled with any rounding adjustment documented
- No computed value is represented as a certified APR or an offer recommendation

## Access, privacy and stop conditions

- Use fictional offers without personal credit, identity or account information
- Missing terms or nonstandard repayment features require clarification before calculation
- No application, borrowing decision, lender contact or financial transaction is authorized

## Two possible extensions

- Add a glossary of payment, principal, interest and fee terms
- Create an intentionally flawed synthetic comparison for learners to audit
