# Fictional input and expected brief

This is an invented local exercise. All text, identifiers and context are fictional; no customer records or external service are involved. The links below point into this fixture, not to a live provider.

## Collection context

Question: what should be investigated about exporting in the fictional CedarDesk product?

The authorized input is the complete supplied slice, not a complete customer dataset. Include submissions from `2026-09-01T00:00:00Z` through, but excluding, `2026-09-08T00:00:00Z`. Snapshot: `2026-09-08T12:00:00Z`. Use submission time, not export-row order or incident time.

The optional survey asked: “What worked or did not work when exporting?” Its invitation count, eligible population and nonresponse are unknown. Support comments were selected with the `export` topic filter, which favors people contacting support. The fictional tokens P1–P6 are supplied person-level keys with an explicit cross-channel mapping; no identity is inferred. Two nonempty comments have no respondent key. Product version, export path and account configuration are absent.

## Fictional input

Each JSON object is one raw input row. `source` identifies the original submission/comment; `row` identifies its location in this supplied fixture. `same_episode_as` is explicitly supplied provenance, not an inference. R02 is a second export copy of R01. All records are version 1.

```json
[
  {"row":"R01","source":"survey:S1","channel":"survey","submitted":"2026-09-01T09:00:00Z","respondent":"P1","version":1,"text":"The export button is hard to find, and the downloaded CSV loses my labels."},
  {"row":"R02","source":"survey:S1","channel":"survey","submitted":"2026-09-01T09:00:00Z","respondent":"P1","version":1,"text":"The export button is hard to find, and the downloaded CSV loses my labels."},
  {"row":"R03","source":"survey:S2","channel":"survey","submitted":"2026-09-02T09:00:00Z","respondent":"P2","version":1,"text":"The export button is hard to find."},
  {"row":"R04","source":"survey:S3","channel":"survey","submitted":"2026-09-02T10:00:00Z","respondent":"P3","version":1,"text":"The export button is hard to find."},
  {"row":"R05","source":"support:C1","channel":"support","submitted":"2026-09-03T09:00:00Z","respondent":"P1","version":1,"same_episode_as":"survey:S1","text":"I found export after a hint. Labels still disappear in the CSV."},
  {"row":"R06","source":"survey:S4","channel":"survey","submitted":"2026-09-04T09:00:00Z","respondent":null,"version":1,"text":"The downloaded CSV loses my labels."},
  {"row":"R07","source":"support:C2","channel":"support","submitted":"2026-09-04T10:00:00Z","respondent":null,"version":1,"text":"The downloaded CSV loses my labels."},
  {"row":"R08","source":"survey:S5","channel":"survey","submitted":"2026-09-05T09:00:00Z","respondent":"P4","version":1,"text":"Export was easy to find and all labels stayed in my CSV."},
  {"row":"R09","source":"survey:S6","channel":"survey","submitted":"2026-09-06T09:00:00Z","respondent":"P5","version":1,"text":"The CSV kept its labels, but the date column was wrong."},
  {"row":"R10","source":"survey:S7","channel":"survey","submitted":"2026-09-07T09:00:00Z","respondent":null,"version":1,"text":"   "},
  {"row":"R11","source":"support:C3","channel":"support","submitted":"2026-09-08T00:00:00Z","respondent":"P6","version":1,"text":"Yesterday's export had the wrong date column."}
]
```

## Coding ledger

This is manual, reviewable coding, not an automated semantic classifier. All eight included comments are eligible for all three themes. Each array holds `[theme, stance, exact excerpt]`. D includes difficulty or ease finding the export control, excluding exported-file contents. L includes loss or retention of labels in the CSV, excluding finding the control. T concerns date-column correctness, excluding submission-date metadata. `problem_reported` identifies a source's report, not an independently verified defect.

```json
{
  "survey:S1": [["D","problem_reported","The export button is hard to find"],["L","problem_reported","the downloaded CSV loses my labels."]],
  "survey:S2": [["D","problem_reported","The export button is hard to find."]],
  "survey:S3": [["D","problem_reported","The export button is hard to find."]],
  "support:C1": [["D","problem_reported","I found export after a hint."],["L","problem_reported","Labels still disappear in the CSV."]],
  "survey:S4": [["L","problem_reported","The downloaded CSV loses my labels."]],
  "support:C2": [["L","problem_reported","The downloaded CSV loses my labels."]],
  "survey:S5": [["D","no_problem_reported","Export was easy to find"],["L","no_problem_reported","all labels stayed in my CSV."]],
  "survey:S6": [["L","no_problem_reported","The CSV kept its labels"],["T","problem_reported","the date column was wrong."]]
}
```

C1 is coded as discovery friction in the context of S1's documented difficulty in the same supplied episode; C1 itself reports finding the control after a hint. This is an explicit coding judgment, not proof that the hint was indispensable or exporting was impossible. S6 is mixed about exporting overall, but its label-retention statement is positive and its date-correctness statement reports a problem. No source in this fixture is mixed within a single theme.

## Expected brief

Start by asking what distinguishes the exports that lost labels from the ones that retained them. The reports conflict, and missing version/path information prevents deciding whether this is one reproducible behavior or several different conditions.

Scope: the supplied September 1–7 UTC slice has 11 raw rows, one repeated export copy and 10 unique original records. One blank and one out-of-window record leave 8 analyzable comments: 6 survey and 2 support. Six comments have known person-level keys covering 5 distinct known respondents; 2 comments have unknown identity. The total number of distinct people is unknown.

- **Label retention:** 6 of 8 comments discuss it. Four report loss: [S1/R01, C1/R05, S4/R06 and C2/R07](#fictional-input). These cover 1 known respondent and 2 unknown-identity comments; S1 and C1 are explicitly the same episode. Two other comments, [S5/R08 and S6/R09](#fictional-input), report retained labels. Across both stances there are 3 known respondents plus 2 unknown-identity comments. Different export paths, versions or configurations are possible explanations, not established causes. What conditions differed, and did the same labels actually go through the same export path?
- **Finding export:** 5 of 8 comments discuss it. Four report friction, covering 3 known respondents: [S1, S2, S3 and C1](#fictional-input). C1 says a hint helped. [S5](#fictional-input) reports it was easy to find, bringing the theme to 4 known respondents. S2 and S3 have identical wording but different supplied person-level keys and original submissions, so both remain. Prior familiarity or different interfaces could explain the contrast; neither is documented. What did people see, and what hint resolved C1's difficulty?
- **Date-column correctness:** [S6/R09](#fictional-input) reports a wrong date column, while saying labels were retained. This is 1 of 8 comments and 1 known respondent. The report alone does not distinguish incorrect values from a format or timezone interpretation. What expected and actual values would clarify that distinction?

The themes have 12 source-theme assignments across 8 comments. S1, C1 and S5 belong to D and L; S6 belongs to L and T. These are overlapping counts with the same eight-comment denominator, not mutually exclusive groups. No count here estimates population prevalence or proves an incident count. In particular, matching anonymous text in S4 and C2 does not establish whether one or two people or episodes are represented.

Limits: this is a short, self-selected survey plus topic-filtered support, with unknown invitation and eligibility counts. Product conditions are missing. Different people may share an incident, and distinct submissions may reflect common prompts. No prior comparable window is supplied, so no trend or response rate can be established. The questions above propose an investigation; no outreach, new collection or source changes occurred.

## Reconciliation and expected counts

```text
Raw rows: 11
Repeated copies: 1 (R02 aliases R01, original source survey:S1)
Unique original records: 10
Excluded: 1 blank (R10); 1 outside submission window (R11)
Included unique comments: 8 = 6 survey + 2 support
Known-identity comments: 6; distinct known respondents: 5
Unknown-identity comments: 2; total distinct people: unknown

Theme  Sources/all eligible  Known respondents  Unknown-identity sources  Stance source counts
D      5/8                  4                  0                         problem 4; no problem 1
L      6/8                  3                  2                         problem 4; no problem 2
T      1/8                  1                  0                         problem 1; no problem 0

D intersection L: 3; L intersection T: 1; D intersection T: 0
Union D,L,T: 8; sum of theme source counts: 12
```

R11 mentions yesterday, but it is excluded because submission time falls exactly at the exclusive end of the window. R01 is inside the first included day. The checker additionally tests an exact start timestamp, changed copies, unknown identities and repeated within-theme mentions.

## Reproduce and limits

From this folder:

```bash
python3 check_example.py
```

The script reads the two JSON blocks above, checks provenance-based deduplication, exclusions, exact excerpts, unique-source/known-respondent counts, channel totals, stance partitions and overlapping-theme denominators. It also checks row-order invariance, identical-text preservation, an unresolved changed copy, identity uncertainty, a mixed-stance variant and window boundaries. It does not contact a service or write files.

Observed on 2026-10-01 in the repository's Linux environment with Python 3.12.14: the command exited with status 0 and printed 8 included comments, 5 known respondents, 2 unknown-identity sources and theme source counts D=5, L=6, T=1, each with denominator 8. It finished with `PASS: copies, identities, excerpts, exclusions, overlaps, denominators, stances and boundaries`. The skill frontmatter validator also passed.

This authored fixture is not a live feedback analysis, a test of survey methodology or evidence that manual theme choices are semantically correct. Identity variants and the mixed-stance variant test accounting only; they do not change the expected brief or establish real identities or interpretations.
