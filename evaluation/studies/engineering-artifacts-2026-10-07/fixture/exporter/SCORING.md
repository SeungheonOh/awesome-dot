# Exporter grading contract

Candidate artifact: project/tests/cases.json. Designated treatment guide:
write-behavior-tests at the pinned source revision. The public project is
intentionally correct. Candidate authoring scope is tests only.

The trusted runner discovers and validates the fixed file and executes every
case by invoking the requested declared public entry point. It never imports
candidate files. Expected payloads are compared using JSON-structure equality,
including list order and multiplicity; mapping key order is irrelevant.

Outcomes:
1. discovery: required-path artifact parses and meets bounded schema; case count
   is 1..24, so an empty suite cannot be a green discovery
2. correct_program_specificity: every assertion accepts correct_a and correct_b
3. duplicate_collapse: at least one assertion rejects loss of equal occurrences
4. zero_as_missing: at least one assertion rejects integer zero becoming null
5. sort_instead_of_stable_order: at least one assertion rejects code sorting
6. wrong_empty_representation: at least one assertion rejects items null for []
7. consumer_filter_bypass: at least one public consumer assertion rejects the
   inclusion of unselected records; core-only assertions cannot earn this credit

Mutation outcomes 3..7 are gated on outcome 2. Raw mismatches remain visible.
A invalid artifact has no discovery/specificity/mutation credit; no hidden test
is silently added to the candidate suite. all_required_outcomes requires all
seven outcomes. Scores are not collapsed into a performance percentage.

Frozen controls:
- strong: 8 contract-correct cases, both correct programs accepted, all 5 killed
- weak: ordinary green case, both correct programs accepted, no mutant killed
- wrong_expectation: incorrect expectation fails both correct programs, zero
  qualified mutation credit despite raw mutant mismatches
- core_only: accepts both correct programs, detects 4 mutants, misses consumer
- selftest selective witnesses: isolate each individual mutant independently

Important limits: this measures the submitted assertions, not the quality of a
candidate's explanatory prose or whether the candidate personally ran the runner.
No model-generated programs are executed by the grader. Two correct solutions
reduce overfitting to private structure but do not prove all future compatible
implementations will be accepted. Invalid product inputs are outside scope.
