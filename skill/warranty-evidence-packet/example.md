# Fictional warranty packet

All names, identifiers, records and terms are invented. There is no real contact address or submission endpoint. These text fixtures represent documents, not photographs or a real purchase.

## Given sources

- E1, order confirmation: Paper Finch Home sold one Mosslight ML-4 task lamp on 2025-05-07; order TEST-1042. The supplied confirmation establishes this purchase, but says nothing about authorized-retailer status
- E2, delivery record: the item in TEST-1042 was delivered on 2025-05-10
- E3, supplied fictional warranty, version 2025-01, household ML-series products: coverage for defects in materials or workmanship for the original household purchaser, bought from an authorized retailer; starts on delivery and ends immediately before the second delivery anniversary. Excludes normal battery-capacity decline and impact/liquid damage. Provider decides whether a fault is covered and chooses repair or replacement. Written review requires an order confirmation, delivery evidence, model and serial, and a symptom account. Photos are optional for initial written review. Do not ship without separate authorization. Charges, if any, require a separate proposal
- E4, user-supplied account dated 2026-10-01: “I am the original purchaser and use it at home. Since 2026-09-25, the light becomes noticeably dimmer after about ten minutes on a full-charge indicator. I observed this twice. I don't know the cause. No drop or liquid exposure that I know of. I have not opened it or tried repairs.”
- E5, user-supplied label transcription: model ML-4; serial TEST-ML4-042. No label photo is supplied

The fictional user asks for a private packet only and says they would prefer repair if covered, subject to the provider’s remedy process. No contact, upload or claim submission is authorized. Assessment date: 2026-10-01.

## Expected prepared request

Subject: Warranty review request, Mosslight ML-4, order TEST-1042

Please review whether my Mosslight ML-4 task lamp is covered under the supplied warranty. I purchased it from Paper Finch Home on 2025-05-07; the delivery record shows 2025-05-10. The serial number I transcribed from the label is TEST-ML4-042.

I first noticed the issue on 2026-09-25. On two occasions, the lamp became noticeably dimmer after about ten minutes while starting with a full-charge indicator. I do not know the cause. I am the original purchaser and use it at home. I know of no drop or liquid exposure. I have not opened it or attempted repairs.

I have included the order confirmation, delivery record, supplied warranty, symptom account and label transcription. I have not included photographs. Please confirm whether Paper Finch Home qualifies as an authorized retailer and whether this reported issue is covered, including whether the battery-capacity exclusion is relevant. If covered, I would prefer repair, subject to the warranty's remedy process. Please advise on the next step; this request does not authorize paid work or shipment.

## Checked expected assessment

| Condition | Evidence | Result |
|---|---|---|
| Date window | E2 + E3 | Supported: 2025-05-10 ≤ 2026-10-01 < 2027-05-10 |
| Original purchaser and household use | E4 | Supported by user report, not independent verification |
| Authorized retailer | E1 + E3 | Unknown; purchase proof alone does not establish this |
| Covered defect rather than excluded capacity decline | E3 + E4 | Unknown; symptoms are not a diagnosis |
| Required initial written-review material | E1, E2, E4, E5 | Complete under these fictional terms |
| Optional photos | None supplied | Not included; no image fabricated |
| Claim status | Private preparation request | Prepared only; not submitted or accepted |

All five supplied sources appear in the private manifest as original synthetic text records. The label remains a transcription, never a photograph. Eligibility is unresolved even though the initial written-review packet is complete. Provider questions should remain in the request; do not replace them with “covered defect” or “authorized retailer.”

Missing decision evidence: retailer authorization and provider assessment of the symptom/cause. Neither creates permission for self-diagnosis, paid testing or an external submission.

## Reproduce and expected edge behavior

From this directory: `python3 check_example.py`

Observed in the repository's Linux environment with Python 3.12.14: exit status 0; output confirmed complete packet, unresolved eligibility, preparation-only status and five unchanged source digests, followed by `PASS: dates, completeness, uncertainty, original evidence, private readback and action scope`.

The check additionally verifies:

- The last covered date is 2027-05-09; 2027-05-10 is outside the fictional date rule
- Removing the serial makes the packet incomplete without changing the unknown eligibility factors
- An unauthorized recipient or attachment prevents submission; existing preparation permission never becomes sending permission
- Even hypothetical routine-submission permission stops at a newly proposed charge or waiver
- Altered evidence fails its recorded checksum; the real test originals remain unchanged

These are local fixture checks, not a live warranty determination, legal review, actual photo-redaction test or completed external submission.
