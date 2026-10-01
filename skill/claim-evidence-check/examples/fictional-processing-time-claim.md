# FICTIONAL worked example: a processing-time claim

All organizations, documents, figures and dates below are invented. MOCK identifiers are local exercise labels, not real sources or URLs. No current web research or real-data validation ran. In an actual check, retrieve the current original material, record real retrieval times and inspect the full relevant context.

## Supplied claim and scope

Exact claim: “The new form cut mean permit decision time in half for every applicant.”

Starting source: MOCK-C1, a fictional community newsletter. The user wants to know whether the sentence is supported by the cited pilot report. Use the cutoff 2030-03-20 12:00 UTC. Do not assess whether the fictional department is trustworthy or whether the form should be adopted.

## Mock sources supplied for the exercise

### MOCK-C1: Community newsletter, paragraph 4

- Published: 2030-03-10 10:00 UTC
- Supplied capture: 2030-03-20 09:00 UTC
- Excerpt: “The new form cut mean permit decision time in half for every applicant.”
- The paragraph cites MOCK-C2, table 1
- No independent measurement or applicant interviews are supplied

### MOCK-C2: Form pilot report, version 1, table 1 and methods note

- Publisher: fictional Service Design Office
- Published: 2030-03-08 09:00 UTC
- Supplied capture: 2030-03-09 09:00 UTC
- Measurement windows: January 2030 before the form change; February 2030 afterward

```text
                         Before           After
Completed online cases   180              120
Median business days     12               6
Mean business days       20               18
```

Methods excerpt: “Counts include online applications receiving a decision during each month. Pending cases and applications made in person are excluded. The cohorts contain different applicants. There was no concurrent comparison group; staffing also changed between periods.”

### MOCK-C3: Corrected pilot report, version 2, correction note and table 1

- Same fictional publisher and document identity as MOCK-C2
- Published update: 2030-03-15 14:00 UTC
- Supplied capture: 2030-03-20 09:10 UTC
- Measurement windows remain January and February 2030
- Correction excerpt: “The after-period mean in table 1 is corrected from 18 to 19 business days following a transcription check. The median, case counts and methods note are unchanged.”
- Accessible coverage: correction note, table 1 and complete methods note
- No underlying case-level dataset is supplied

## Expected evidence chain

MOCK-C1 cites MOCK-C2 table 1. MOCK-C2 is the underlying pilot report, not independent corroboration of the newsletter. MOCK-C3 is a later version of that same report. Its correction was available before the cutoff and supersedes the affected after-period mean. The January/February measurements must not be dated March 15 merely because the correction appeared then.

## Expected component assessment

**Component A: the reported mean fell by half.** Contradicted within the cited pilot comparison. Using the corrected table, the mean fell from 20 to 19 business days: a one-day reduction, or (20 − 19) / 20 × 100 = 5%. Even the superseded after-value of 18 would yield 10%, not 50%. Retain both calculations only to explain the version issue; use 19 for the cutoff assessment.

**Component B: a time measure fell by half.** Supported only for the reported median of these completed online cohorts: (12 − 6) / 12 × 100 = 50%, a six-business-day reduction. A median is not a mean, and neither describes every individual's wait. This component supports a narrower rewritten statement, not the original wording.

**Component C: the new form caused the change.** Unresolved. The supplied evidence is a before/after comparison without a concurrent comparison group, and staffing also changed. The result alone cannot isolate the form's effect. Do not claim staffing caused the difference either.

**Component D: every applicant benefited.** Unresolved and not established by this source. Pending and in-person applications are excluded, and only cohort aggregates are supplied. A lower cohort median does not demonstrate improvement for every applicant. There are no matched individual outcomes with which to evaluate that universal wording.

## Expected conclusion

“The pilot report describes a fall in median decision time from 12 to 6 business days among completed online applications in the two measured months. Its corrected mean fell from 20 to 19 business days. These aggregate, before/after figures do not establish that the form caused the change or that every applicant benefited.”

The strongest unresolved question is whether comparable data covering pending and in-person applications, with a design capable of separating concurrent changes, would support a broader conclusion. This is a missing-evidence question, not an instruction to obtain private applicant records.

## Expected output and checks

Return the unchanged quoted claim, four component records, the versioned source chain, both central calculations and the bounded rewrite. Label calculations as arithmetic on supplied report values. Raw-data validation and study replication remain unperformed.

Expected checks include:

- Corrected mean: (20 − 19) / 20 = 0.05; median: (12 − 6) / 12 = 0.5
- Units remain business days; the observed months remain January/February
- The newsletter is derivative evidence, and report versions are not independent studies
- A missing population is not silently added to the sample
- Unsupported causality is not converted into a contrary causal story
- The revised sentence removes “mean,” “caused” and “every” only where necessary, while retaining the supported median result

These are expected answers for an authored exercise, not a report that live source checks or an experiment were executed.
