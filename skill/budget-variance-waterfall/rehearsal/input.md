# Fictional budget input packet

Prepare a private review artifact in Markdown for September 2026, USD. Use positive spending and negative refunds. Do not contact anyone or access accounts. A chart is optional; an exact text bridge is sufficient. Do not invent a missing amount or a reason for spending changes. Produce the useful known portion even if a complete total cannot be established.

## Planned amounts

| Category | Plan |
| --- | ---: |
| Operations | 300.00 |
| Transport | 150.00 |
| Supplies | 250.00 |
| Shared | 0.00 |

## Actual source rows

| Source row | Record ID | Label/category | Kind | Amount |
| --- | --- | --- | --- | ---: |
| Export A row 1 | R1 | Operations | Purchase | 280.00 |
| Export A row 2 | R2 | Transport | Purchase | 170.00 |
| Export A row 3 | R3 | Supplies | Purchase | 240.00 |
| Export A row 4 | R4 | Supplies | Refund | -30.00 |
| Export B row 1 | R4 | Supplies | Refund | -30.00 |
| Export B row 2 | R5 | Shared purchase | Purchase requiring split | 45.00 |
| Export B row 3 | R6 | Between-wallet transfer | Transfer | 200.00 |
| Export B row 4 | R7 | Miscellaneous | Purchase | 20.00 |
| Export B row 5 | R8 | Repair | Purchase | Unknown |

## Explicit source decisions

- The two R4 rows are confirmed copies of the same refund in overlapping exports. Count the underlying refund once and preserve both source references
- R5 is one purchase. Its approved allocation is 15.00 Operations and 30.00 Supplies; do not also count the unsplit 45.00 as another expense
- R6 is a transfer between wallets and is outside spending
- R8 is a real in-period purchase in this fictional ledger, but its nonnegative amount has not been supplied. It is not zero and should not disappear
- Categories absent from the plan have a zero plan in this fixture
- Use cents exactly and keep a mapping/audit trail

Return a category comparison, a readable reconciliation, treatment of the duplicate/split/transfer, and the smallest question needed to finish the unknown part. Explain which claims are complete and which are provisional.
