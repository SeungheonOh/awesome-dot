# FICTIONAL worked example: is the announced venue usable?

Everything in this example is invented: the organization, notices, event, dates and measurements. The source labels refer only to mock excerpts below; they are not real URLs or documents. No web retrieval, venue verification or booking occurred. For a real execution, retrieve current primary evidence and replace every mock locator with an inspected source.

## Supplied task

A neighborhood history group is comparing its planned scanning event at West Annex with postponement. Its organizers want a private decision brief, not an action. The event date is 2030-04-20. Two must-haves are seating for at least 40 people and a documented step-free public route to Hall A. The group has not authorized the assistant to choose a new date, book a room or contact anyone.

Use the historical evidence cutoff 2030-04-12 12:00 UTC. The question is what was supported by sources available at that cutoff. All timestamps in this exercise use UTC. Do not bring later knowledge into the initial answer.

## Supplied mock source excerpts

### MOCK-S1: Annex facilities page, section “Hall A”

- Publisher: fictional West Annex Facilities
- Publication: 2030-02-01 09:00
- Last stated update: 2030-03-01 09:00
- Supplied snapshot captured: 2030-04-12 10:00
- Excerpt: “Hall A seats 60. The north entrance provides the marked step-free public route. The main entrance has six steps.”
- Coverage: the Hall A section and entrance note only

### MOCK-S2: Building works notice, paragraph 2

- Publisher: fictional West Annex Facilities
- Publication: 2030-04-10 14:00
- Supplied snapshot captured: 2030-04-12 10:05
- Event/effective window: 2030-04-18 through 2030-04-22, inclusive
- Excerpt: “The north entrance will be closed during paving works. Hall A remains open. Visitors should use the main entrance.”
- Coverage: complete short notice; no alternative step-free route is mentioned

### MOCK-S3: Local Bulletin headline and article paragraph 3

- Publisher: fictional Local Bulletin, a separate publication
- Publication: 2030-04-11 16:00
- Supplied snapshot captured: 2030-04-12 10:10
- Headline: “Annex closes for repairs”
- Paragraph 3: “The facilities notice says Hall A remains open while the north entrance is closed.”
- Provenance: the article explicitly cites MOCK-S2; it supplies no site visit or separate access assessment

### MOCK-S4: Later facilities update, paragraph 1

- Publisher: fictional West Annex Facilities
- Publication and supplied capture: 2030-04-15 11:00
- Excerpt: “The paving work has been delayed. The north entrance will remain open on April 20.”
- Coverage: complete update
- This is intentionally supplied to test cutoff handling. It was unavailable at the requested April 12 boundary

## Expected analysis

**Answer at the cutoff:** The evidence supports the seating requirement but does not establish the required step-free route on the event date. Hall A is documented as remaining open; the headline claiming the entire Annex closes overstates its own underlying notice. Do not describe the event as confirmed suitable or booked.

**Criterion C1, seating:** Supported by MOCK-S1: stated capacity 60 exceeds the required 40. This is a facilities specification, not an independent occupancy inspection. No contrary capacity evidence is supplied.

**Criterion C2, step-free route:** Unresolved for the event date. MOCK-S1 identifies a step-free north entrance, and MOCK-S2 closes that entrance during a window containing April 20. The suggested main entrance has steps. These records establish the loss of the documented route; they do not establish that every possible alternative route is inaccessible. Absence of an alternative in the notice is not proof that no alternative exists.

**Option comparison:** The current plan cannot yet meet the user's positive-verification requirement. Postponement remains an option whose replacement date and access conditions have not been supplied. Do not claim it is arranged or necessarily best. The decision-changing question is: “What documented step-free public route would serve Hall A on April 20 under the April 10 works notice?” Leave that question unsent.

**Source dependence:** MOCK-S3 is independent as a publisher but derivative as evidence about the closure. It does not corroborate MOCK-S2 through a separate observation. The headline/body mismatch should be explained rather than counted as a true primary-source conflict.

**Cutoff:** Exclude MOCK-S4 from the April 12 answer. If a later, separately requested current brief were prepared, that update would trigger rechecking relevant access details. It cannot silently revise this historical assessment.

## Expected output fragments

```text
decision: retain the planned venue or consider postponement
cutoff: 2030-04-12 12:00 UTC
answer_or_blocker: step-free public access on the event date is not verified
comparison:
  planned venue / seating / supported / MOCK-S1 section Hall A
  planned venue / step-free route / unresolved / MOCK-S1 + MOCK-S2
  postponement / replacement conditions / unresolved / no supplied evidence
excluded_after_cutoff: MOCK-S4
next_step: obtain the missing access detail before treating suitability as confirmed
```

Expected checks: preserve capacity units, distinguish notice date from works dates, reject the headline's building-wide closure claim, identify derivative reporting, exclude later evidence and keep an unmentioned route unknown. These are expected results for an authored fixture. A real execution must report its own observed checks and accessible coverage.
