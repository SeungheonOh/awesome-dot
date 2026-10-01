# Worked example: one confirmed event, two blocked calculations

All asset names, manuals and documents below are fictional. The care rules are synthetic fixtures for testing an administrative workflow, not instructions for a real appliance.

## Inputs

```yaml
assessment_date: 2026-04-15
review_through: 2026-08-31
assets:
  - id: ASSET-A
    label: utility-room air cleaner
    model: Airloom A100
  - id: ASSET-B
    label: cupboard extractor
    model: Boxwell B200
  - id: ASSET-C
    label: desk ventilator
    model: Cirrus C300
sources:
  H1:
    type: service_record
    asset: ASSET-A
    task: intake-grille cleaning
    performed_on: 2026-01-31
    invoice_issued_on: 2026-02-05
    status: completed
  H2:
    type: user_note
    asset: ASSET-A
    task: intake-grille cleaning
    claimed_date: 2026-02-02
    wording: "I think the grille was cleaned on Monday"
  H3:
    type: quote
    asset: ASSET-B
    task: screen cleaning
    proposed_on: 2026-03-10
    status: quoted_only
  M1:
    type: fictional_model_manual
    model: Airloom A100
    task: intake-grille cleaning
    rule: >-
      Review three calendar months after the last completed cleaning.
      If the target month lacks that day, use its last calendar day.
  M2:
    type: fictional_model_manual
    model: Boxwell B200
    task: screen cleaning
    rule: "Review six calendar months after completed cleaning"
  M3:
    type: fictional_model_manual
    model: Cirrus C200
    task: grille review
    rule: "Review every two calendar months"
```

## Expected history treatment

| Asset | History conclusion | Basis |
| --- | --- | --- |
| ASSET-A | Documented cleaning on 31 January 2026; user-reported 2 February remains a conflicting note | H1 explicitly states the performed-on date; H2 expresses uncertainty |
| ASSET-B | Completion history unknown; proposed work retained separately | H3 is a quote and does not confirm work occurred |
| ASSET-C | No completion history supplied; manual match unresolved | M3 describes C200, while the asset is C300 |

Do not use H1's 5 February invoice date as the maintenance date. Do not delete H2; if the user later supplies evidence that H1 is wrong, the calculation should be revisited. If H2 were another explicit completion report rather than an uncertain recollection, the conflict would need resolution before finalizing an anchor.

## Expected next-review view

| Asset | Anchor | Rule | Next review | State |
| --- | --- | --- | --- | --- |
| ASSET-A | 2026-01-31, H1 | Three calendar months, clamp missing day to month end, M1 | 2026-04-30 | Upcoming within the review horizon |
| ASSET-B | Unknown | Six calendar months after completion, M2 | Unknown | Need actual completion evidence |
| ASSET-C | Unknown | No model-matched rule | Unknown | Find C300 guidance and history |

```text
ASSET-A calculation:
  January 31 + 3 calendar months targets April 31
  April has 30 days
  M1 explicitly says to use the target month's last day
  result = April 30, 2026
```

Do not add a July review by assuming the April task will be performed. The next interval can be calculated after qualifying completion evidence arrives.

## Hypothetical new evidence

```yaml
H4:
  type: user_completion_report
  asset: ASSET-A
  task: intake-grille cleaning
  performed_on: 2026-05-02
```

If this new report is actually supplied later, preserve H1 as history, record H4 as user-reported completed, and calculate the next review from 2 May to 2 August. Label its evidence level accurately; a user report does not become a supplier service certificate.

## Checks and useful questions

- 31 January plus three calendar months under M1 equals 30 April, not 1 May from adding 90 days
- 2 May plus three calendar months equals 2 August
- Ask whether ASSET-B's quoted work was performed and what evidence establishes its date
- Ask for the C300 manual rather than silently applying C200 guidance
- No reminder, service appointment or completed physical work is created by producing this record
