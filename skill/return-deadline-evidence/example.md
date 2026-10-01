# Worked example: request first, receipt later

The merchant and policy below are fictional. These supplied excerpts are the entire policy for this exercise; they are not legal advice or a statement of any real retailer's rules.

## Inputs

```yaml
merchant: Example Home Store
item: unopened table lamp
region: UK
assessment_date: 2026-10-01
timezone: Europe/London
evidence:
  P1:
    kind: purchase_record
    purchased_on: 2026-09-02
  D1:
    kind: item_delivery_confirmation
    delivered_on: 2026-09-05
  T1:
    kind: terms_attached_to_purchase
    applicable_item: table lamp
    request_rule: >-
      Submit a return request within 30 calendar days after delivery.
      The day following delivery is day 1. Requests close at 23:59
      Europe/London on day 30.
    receipt_rule: >-
      After authorization, the item must reach the returns center within
      14 calendar days after the authorization date. The following day
      is day 1. The receipt cutoff hour is not stated.
    condition: unopened, original packaging, supplied accessories included
    fee: 4.50 GBP deducted for the merchant's prepaid return service
    fee_choice: other permitted return methods are not described
actual_return_request: none
actual_authorization: none
```

## Expected result

The evidenced request deadline is 5 October 2026 at 23:59 Europe/London, equivalent to 22:59 UTC on that date. As of 1 October, the item is within the stated request window. The supplied unopened condition appears to match the rule, but acceptance has not been established.

| Boundary | Evidence and calculation | Result |
| --- | --- | --- |
| Request-by | D1 delivery 5 September; T1 says following day is day 1; add 30 calendar days | 5 October 2026, 23:59 Europe/London |
| Received-by | T1 says authorization date plus 14 calendar days | No actual date yet; authorization has not occurred |
| Shipped-by | No source supplies a separate shipping deadline or guaranteed transit duration | Unknown; do not invent a last safe dispatch date |

The purchase date is not used to start this policy's clock. A request on 6 October would be outside the stated request window. Counting delivery day as day 1 would incorrectly produce 4 October.

## Hypothetical later event

```text
If authorization were issued on 2026-10-03:
  day 1 would be 2026-10-04
  day 14 would be 2026-10-17
  candidate received-by date would be 2026-10-17
  exact cutoff hour would remain unknown
```

This is a scenario, not a claim that authorization was issued or a return submitted. Do not enter 17 October as an actual deadline in a live record without the triggering evidence.

## Next-step checklist

- Verify original packaging and supplied accessories are present
- Review the stated £4.50 deduction before choosing the merchant's prepaid service
- Ask the merchant which receipt cutoff hour applies and whether other return methods are allowed
- If the user later chooses to request a return, obtain and preserve the resulting authorization and its actual terms before recalculating the receipt deadline

## Calculation checks

```text
2026-09-05 + 30 calendar days = 2026-10-05
2026-10-03 + 14 calendar days = 2026-10-17
2026-10-05 23:59 Europe/London = 2026-10-05 22:59 UTC
```

Failure branch: if T1 only said “return within 30 days,” the expected answer would retain a candidate date but mark the required action and counting convention unresolved. It would not present the detailed cutoffs above as established.
