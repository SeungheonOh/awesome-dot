# F4 frozen semantic rubric

## Review discipline

This is an independent, closed-source factual/decision review, not a preferred prose or workflow test. The scored contract is the common task and six sources. Review the complete anonymized report and read cited source sections. Judge meanings, calculations, applicability, and implications, never keywords, phrase overlap, ordering, formatting, persuasiveness, or similarity to the reference report. Equivalent paraphrases and genuinely supported conditional conclusions are acceptable. No guide, treatment identity, historical solution, model run, or external knowledge is needed.

A group passes only if every assertion in it passes. Contradictions are assessed across the entire report; a correct passage elsewhere does not cancel a material false claim. Distinguish an unresolved must-have from a confirmed failure. Do not penalize omission of an unused tie-break, speculative costs the task expressly excludes, or details that the report is not asked to include. File/section references can cover adjacent claims and need not have one mandatory spelling. All source locators below identify this case's packet under ../../cases/F4.

Manual/independent semantic scores remain null until supplied. The stdlib grader does not infer semantics from tokens. A semantic record must bind to the exact submitted report SHA-256 and contain every frozen assertion ID once. Each rated assertion needs a nonempty reason describing report evidence and source support. Scores may be true, false, or null; a null assertion means review pending. Do not let synthetic control scores stand in for blinded review of a runner output.

## Independent factual key

- Exact scope: AlderRoster Community 3.4; BeaconCrew Basic 2.8; CedarShift Team 5.1. Knowledge cutoff 2026-03-31 17:00 UTC.
- AlderRoster: M1 yes; M2 yes with Export Bridge; eligible; CSV generation online only. USD 10.00 x 12 + USD 15.00 = USD 135.00/month; x 12 = USD 1,620.00/year.
- BeaconCrew: M1 no (view-only offline); M2 yes; ineligible. USD 6.00 x 12 = USD 72.00/month; x 12 = USD 864.00/year. Plus 3.0 headline is inapplicable.
- CedarShift: M1 yes; M2 unknown only for coordinator notes; eligibility unconfirmed; CSV generation available offline; four core fields documented. USD 7.50 x 12 + USD 12.00 = USD 102.00/month; x 12 = USD 1,224.00/year. No extra fee if notes are included.
- Current supported choice: AlderRoster, the only confirmed eligible candidate. It is also valid to wait for clarification before committing while naming AlderRoster as the current supported choice.
- Precisely sufficient reversal condition: cutoff-available exact Team 5.1 CSV Pack evidence confirming coordinator-notes inclusion makes CedarShift eligible and USD 396.00/year cheaper. A negative clarification or unresolved answer preserves AlderRoster (negative = failure; unresolved = unknown). BeaconCrew remains ineligible. The April 2 update cannot be used to settle a March 31 knowledge-cutoff decision, despite its claimed March 25 applicability.

## Five binary groups

### g1

- **g1.1**: AlderRoster Community 3.4 meets M1 and M2 with Export Bridge, so is confirmed eligible. Do not treat online-only CSV generation as a must-have failure; mentioning this unused tie-break attribute is optional.
  - Contract/source anchors: task.txt: Decision contract and report bullet 1; inputs/01-user-requirements.txt#MUST-HAVES; inputs/01-user-requirements.txt#PRIORITIES; inputs/02-alderroster-community-3.4.txt#OFFLINE; inputs/02-alderroster-community-3.4.txt#CSV.
- **g1.2**: BeaconCrew Basic 2.8 meets M2 and fails M1: offline viewing is not editing. It is ineligible.
  - Contract/source anchors: inputs/01-user-requirements.txt#MUST-HAVES; inputs/03-beaconcrew-basic-2.8.txt#OFFLINE; inputs/03-beaconcrew-basic-2.8.txt#CSV.
- **g1.3**: CedarShift Team 5.1 meets M1; M2 and eligibility remain unconfirmed solely because coordinator-notes CSV support is unknown, rather than proven absent. Do not invent gaps in the four core fields or offline generation; explicitly reciting those documented attributes is optional.
  - Contract/source anchors: inputs/01-user-requirements.txt#UNCERTAINTY; inputs/05-cedarshift-team-5.1.txt#OFFLINE; inputs/05-cedarshift-team-5.1.txt#CSV-CORE; inputs/05-cedarshift-team-5.1.txt#NOTES-GAP.
- **g1.4**: The three exact candidate plan/version identities and the 2026-03-31 17:00 UTC as-of context are unambiguous; the report does not evaluate a substituted plan/version/date.
  - Contract/source anchors: task.txt: Decision contract; inputs/01-user-requirements.txt#CUTOFF.

### g2

- **g2.1**: Comparable cost basis is 12 paid seats plus organization-wide mandatory module charges, held constant for 12 months, with no invented discount/tax/optional cost. A common cost-basis sentence plus candidate formulas is sufficient.
  - Contract/source anchors: task.txt: report bullet 2; inputs/01-user-requirements.txt#POPULATION; inputs/02-alderroster-community-3.4.txt#PRICE; inputs/03-beaconcrew-basic-2.8.txt#PRICE; inputs/05-cedarshift-team-5.1.txt#PRICE.
- **g2.2**: AlderRoster monthly USD 135.00 and 12-month USD 1620.00 are correct: 12*10.00+15.00, then *12.
  - Contract/source anchors: inputs/02-alderroster-community-3.4.txt#PRICE; inputs/01-user-requirements.txt#POPULATION.
- **g2.3**: BeaconCrew monthly USD 72.00 and 12-month USD 864.00 are correct: 12*6.00, then *12.
  - Contract/source anchors: inputs/03-beaconcrew-basic-2.8.txt#PRICE; inputs/01-user-requirements.txt#POPULATION.
- **g2.4**: CedarShift monthly USD 102.00 and 12-month USD 1224.00 are correct: 12*7.50+12.00, then *12.
  - Contract/source anchors: inputs/05-cedarshift-team-5.1.txt#PRICE; inputs/01-user-requirements.txt#POPULATION.

### g3

- **g3.1**: AlderRoster Community 3.4 is identified as the current evidence-supported choice. A recommendation to defer commitment pending the precise CedarShift clarification is also acceptable if the current AlderRoster choice remains explicit. No unconfirmed/ineligible app is the unconditional current selection.
  - Contract/source anchors: task.txt: report bullet 3; inputs/01-user-requirements.txt#PRIORITIES.
- **g3.2**: Reasoning applies must-haves before cost and ordered tie-breaks only when appropriate; it introduces no invented weights or priorities. No need to recite unused tie-breaks; accurately stating that no cost tie arises suffices.
  - Contract/source anchors: inputs/01-user-requirements.txt#PRIORITIES; inputs/01-user-requirements.txt#UNCERTAINTY.

### g4

- **g4.1**: Decisive feature, price, exclusion, and uncertainty statements have resolvable relevant file/section citations; equivalent unambiguous citation styles and grouped citations covering adjacent claims are allowed. No exact citation string is required.
  - Contract/source anchors: task.txt: report bullet 4; ../../cases/F4/inputs: all six source files.
- **g4.2**: The report explicitly avoids applying the BeaconCrew Plus 3.0 headline to Basic 2.8 and excludes the April 2 CedarShift clarification from cutoff evidence even though it claims earlier behavior.
  - Contract/source anchors: task.txt: Decision contract and report instruction beginning Briefly explain why; inputs/04-beaconcrew-overview.txt#QUALIFIER; inputs/06-cedarshift-update.txt#UPDATE; inputs/06-cedarshift-update.txt#TIMING; inputs/01-user-requirements.txt#CUTOFF.
- **g4.3**: Provider statements, derived calculations/conclusions, and the designed unknown are distinguishable. The report contains no unsupported decisive outside facts, invented broader uncertainty, or false claim of product testing, provider contact, purchase, or other external action. Attribution can be a report-wide statement; no special vocabulary is required.
  - Contract/source anchors: task.txt: report instructions on sources and designed uncertainty; final paragraph; inputs/01-user-requirements.txt#UNCERTAINTY.

### g5

- **g5.1**: Explains that exact-plan/version, cutoff-available evidence about coordinator_notes in CedarShift CSV would settle the gap: confirmation makes CedarShift the cheapest eligible choice; explicit exclusion makes it fail M2 and preserves AlderRoster; still unknown leaves CedarShift unconfirmed and preserves AlderRoster. Equivalent concise conditionals are accepted. The arithmetic savings figure is optional, but if supplied must be correct (USD 396.00 yearly).
  - Contract/source anchors: task.txt: report instruction beginning Explain exactly what evidence would settle; inputs/01-user-requirements.txt#UNCERTAINTY; inputs/01-user-requirements.txt#PRIORITIES; inputs/05-cedarshift-team-5.1.txt#NOTES-GAP; inputs/05-cedarshift-team-5.1.txt#PRICE.
- **g5.words** (objective): decision-brief.txt has at most 500 whitespace-separated words. Grader computes this without semantic inference.

## Accepted variation and rejection boundaries

“Documented eligible,” “meets both requirements in the supplied specification,” and similar phrases are equivalent. “Unknown,” “not yet established,” and “unconfirmed” are equivalent for CedarShift; “does not support CSV notes” is not. The exact source spellings of columns may be paraphrased as ordinary field names. Totals may use comma separators or dollar signs with an unambiguous USD context, but the requested two-decimal amounts must be present. A comparison in paragraphs, bullets, or a compact plain-text list can pass. The reference is one accepted example, not a mandatory template.

A correct recommendation cannot rescue incorrect prices or eligibility statuses. A correct total without its required cost basis fails the pertinent cost assertion. Recommending CedarShift provisionally only if the specified evidence is available by the cutoff is acceptable when AlderRoster is still named as the current supported choice. Recommending it unconditionally on the basis of the later update is not. A generic “check with the vendor” that omits the precise field, applicability, and decision outcomes does not meet g5.1.

## Objective integrity gate

The evaluator checks byte hashes of all frozen runner files (including task and manifest), exact packet file inventory, input-manifest consistency, and the presence of a nonempty UTF-8 decision-brief.txt. Protected-file changes, missing or extra packet files, unsafe symlinks, missing/undecodable/empty reports, and invalid or mismatched semantic score records fail integrity. Extra files outside the protected packet in a submission are ignored; no extra deliverable is required. Word count belongs to g5, not a subjective writing-style criterion. A valid report with no semantic record has pending groups and accepted=null, never an automatic pass.

## Control limitations

Controls and their synthetic semantic records deliberately exercise every group and the objective gates. These records are author-declared expected classifications, not independent validation of a semantic reviewer. Re-score controls blind before relying on human/model review reliability. The local checks establish fixture integrity, arithmetic values, schema/hash binding, null handling, score aggregation, and the intended control defects only.
