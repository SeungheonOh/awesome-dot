# Worked example: normalize without hiding uncertainty

All records and policies below are fictional. Contents: [authorization and rules](#authorization-and-rules), [source CSV](#source-csv), [expected cleaned rows](#expected-cleaned-rows), [exceptions and lineage](#exceptions-and-lineage), [reconciliation](#reconciliation), [checks](#checks).

## Authorization and rules

The user supplied this CSV and export specification and requested a new cleaned CSV beside it. The original remains unchanged. No account, upload or live sheet is involved.

```json
{
  "source_id": "ledger-export-A",
  "encoding": "UTF-8",
  "delimiter": ",",
  "header_record": 1,
  "source_record_numbering": "data-record ordinal, excluding the header",
  "schema": {
    "record_id": "text; never remove leading zeros",
    "customer_id": "text; surrounding export padding is insignificant",
    "doc_date": "ISO YYYY-MM-DD is accepted; no slash-date locale is supplied",
    "amount": "decimal; comma thousands separator, period decimal separator; parentheses mean negative",
    "currency": "uppercase ISO code; supplied values are USD and EUR",
    "status": "trim and case-fold before applying the supplied dictionary",
    "reference": "text preserved exactly"
  },
  "missing_amount_tokens": ["", "N/A"],
  "status_dictionary": {
    "paid": "paid", "open": "open", "hold": "on_hold",
    "credit": "credit", "awaiting info": "needs_info"
  },
  "duplicate_rule": "The export can repeat the same event. Collapse records equal across every business column after approved normalizations; retain the first occurrence and every source ordinal. Matching record_id alone is insufficient.",
  "unresolved_rule": "Keep conflicting records and ambiguous date text. Do not choose a winner or infer a date locale."
}
```

## Source CSV

Each data record occupies one physical line in this fixture, but lineage uses data-record ordinals. The amount in record 1 contains a quoted delimiter.

```csv
record_id,doc_date,customer_id,amount,currency,status,reference
00041,2026-09-01, 0017 ,"1,200.00",usd, paid ,A-7
00042,2026-09-02,0017,20,USD,open,B-2
00042,2026-09-02,0017,20,USD,open,B-2
00043,03/09/2026,0020,50.00,EUR,hold,C-1
00043,03/09/2026,0020,55.00,EUR,hold,C-1
00044,2026-09-04,0004,,USD,open,D-5
00045,2026-09-05,0004,(25.00),USD,credit,D-6
00046,2026-09-06,0004,N/A,USD,open,D-7
00047,2026-09-07,0004,10.50,eur,Awaiting info,E-2
00048,2026-09-08,0004,0,USD,open,F-2
```

## Expected cleaned rows

A blank `amount` is a null, not zero. `amount_state` retains why it is null. `doc_date_raw` and `amount_raw` preserve the inputs whose parsed representation could obscure meaning. The immutable source supplies all other original cell values. The semicolon in `source_records` is a lineage-list separator, not part of a business ID.

```csv
source_records,record_id,doc_date_raw,doc_date_iso,customer_id,amount_raw,amount,amount_state,currency,status,reference,review_flags
1,00041,2026-09-01,2026-09-01,0017,"1,200.00",1200.00,present,USD,paid,A-7,
2;3,00042,2026-09-02,2026-09-02,0017,20,20.00,present,USD,open,B-2,
4,00043,03/09/2026,,0020,50.00,50.00,present,EUR,on_hold,C-1,ambiguous_date;conflicting_key
5,00043,03/09/2026,,0020,55.00,55.00,present,EUR,on_hold,C-1,ambiguous_date;conflicting_key
6,00044,2026-09-04,2026-09-04,0004,,,blank,USD,open,D-5,
7,00045,2026-09-05,2026-09-05,0004,(25.00),-25.00,present,USD,credit,D-6,
8,00046,2026-09-06,2026-09-06,0004,N/A,,source_marker,USD,open,D-7,
9,00047,2026-09-07,2026-09-07,0004,10.50,10.50,present,EUR,needs_info,E-2,
10,00048,2026-09-08,2026-09-08,0004,0,0.00,present,USD,open,F-2,
```

## Exceptions and lineage

```json
{
  "source_dispositions": {
    "kept_representatives": [1, 2, 4, 5, 6, 7, 8, 9, 10],
    "absorbed_duplicates": [{"source_record": 3, "survivor_source_record": 2}],
    "excluded": [],
    "quarantined": [],
    "added_output_rows": []
  },
  "exceptions": [
    {
      "source_records": [4, 5],
      "field": "doc_date",
      "raw": "03/09/2026",
      "reason": "No day/month convention supplied",
      "resolution_needed": "Establish whether the intended date is March 9 or September 3",
      "output_behavior": "Keep raw date; leave parsed date null"
    },
    {
      "source_records": [4, 5],
      "field": "record_id",
      "raw": "00043",
      "reason": "Same key and reference, conflicting amounts 50.00 and 55.00 EUR",
      "resolution_needed": "Establish whether these are separate events or which record is authoritative",
      "output_behavior": "Keep both records; include 105.00 EUR in a clearly provisional known-value total"
    },
    {
      "source_records": [6, 8],
      "field": "amount",
      "reason": "Two amounts are missing under the supplied token rules",
      "resolution_needed": "Obtain amounts if a complete monetary total is required",
      "output_behavior": "Keep null amounts with distinct blank/source_marker reasons"
    }
  ]
}
```

Records 2 and 3 represent one event only because the supplied export rule establishes that equality across all normalized business fields permits collapse. The repeated key at records 4 and 5 does not satisfy that rule. Keep both despite the tempting choice of the larger or later-looking value.

## Reconciliation

```json
{
  "population": {
    "source_detail_records": 10,
    "kept_source_representatives": 9,
    "absorbed_duplicate_records": 1,
    "output_rows": 9,
    "output_distinct_record_ids": 8,
    "output_lineage_source_records": 10
  },
  "USD": {
    "source_rows": 7,
    "source_present_amounts": 5,
    "source_known_value_total": "1215.00",
    "removed_duplicate_value": "20.00",
    "output_rows": 6,
    "output_present_amounts": 4,
    "output_null_amounts": 2,
    "output_zero_amounts": 1,
    "output_known_value_total": "1195.00"
  },
  "EUR": {
    "source_rows": 3,
    "source_known_value_total": "115.50",
    "removed_duplicate_value": "0.00",
    "output_rows": 3,
    "output_present_amounts": 3,
    "output_null_amounts": 0,
    "output_zero_amounts": 0,
    "output_known_value_total": "115.50",
    "unresolved_conflict_contribution": "105.00",
    "nonconflicting_known_value_total": "10.50"
  },
  "independent_business_control": null,
  "conclusion": "Internal row/value reconciliation passes. USD is incomplete because two amounts are missing; EUR is provisional because the conflicting key remains unresolved. Do not combine the currencies."
}
```

## Checks

Parse the two CSV blocks with a CSV reader, keeping source values as strings. Build the candidate independently from the raw block using the supplied rules, then compare every field to the expected cleaned block. Check the totals again with independent decimal arithmetic:

```python
from decimal import Decimal as D

assert D("1200") + D("20") + D("20") - D("25") + D("0") == D("1215.00")
assert D("1200") + D("20") - D("25") + D("0") == D("1195.00")
assert D("1215.00") - D("20.00") == D("1195.00")
assert D("50") + D("55") + D("10.50") == D("115.50")
assert D("115.50") - D("105.00") == D("10.50")
assert 10 == 9 + 1
```

Verify that each ordinal 1 through 10 occurs exactly once in output lineage, identifiers retain their zeros, exactly two dates remain unresolved, one zero survives, and neither missing amount has become zero. A source hash and a post-save readback should be checked when this fixture is materialized as files. These example checks do not establish a live application write or any business control total.
