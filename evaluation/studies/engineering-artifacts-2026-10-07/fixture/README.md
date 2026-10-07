# Original engineering outcome cases, review packet v2

Status: prepared for independent review. No candidate/model trials have run.
No remote repository, historical result, or historical evaluation was changed.
These fixtures, reports, runners, controls, and graders were authored for this
packet. The two designated guides are unchanged snapshots from the repository
commit identified in provenance.json; no external task dataset was copied.

## Cases

- exporter: tests-only task for a documented public inventory download consumer.
  Candidate writes project/tests/cases.json. Two separately expressed correct
  implementations and five isolated plausible mutants are evaluator-owned.
- triage: correct asynchronous two-input controller under reversed completion.
  Candidate writes project/reproduction.json. A separate event-history oracle
  checks product state and declarative report claims. This is an intentional
  no-defect control, not a task requiring an invented bug or a product patch.

Read PROTOCOL.md and each case's SCORING.md before use. Only common/ is candidate
material. sources/<designated-guide>.md is added only in the guide condition.
Never expose trusted/, controls/, authoring/, validation/, selftest.py, scoring,
protocol, or provenance to a candidate. Do not run candidates in this shared
review directory or give them access to its parents.

## Reproduce author-side harness checks

Python 3.10+ on POSIX, standard library only:

    python -I -B selftest.py
    python -I -B verify_freeze.py

The first command runs 34 harness tests, including 24 completion permutations
and 500 seeded state-machine scripts inside two of those tests. These counts
are not 553 model trials or independent experimental tasks. All are author
validation and must be reported as such.

To grade a submitted project directory, use an evaluator-owned copy of this
packet and invoke one of these with the candidate project root as the argument:

    python -I -B exporter/trusted/grade.py /private/staging/candidate-project
    python -I -B triage/trusted/grade.py /private/staging/candidate-project

Only the fixed relative JSON path is discovered. Candidate files are never
imported, evaluated, or run by grading. Every score is printed as JSON. A process
exit code of zero means a score was produced; it does not mean the artifact
passed. Check status, individual fields, and all_required_outcomes. A harness
error is not a candidate failure and requires investigation.

The public convenience runners are part of the supplied baseline. If candidates
have a shell, any runner invocation belongs to the trial's isolated environment.
Grading always uses the frozen evaluator copies, never candidate-edited runners.
Changes beyond the allowed output are a separate scope violation for the trial
coordinator to report. There is no authorization to execute candidate-authored
programs, including any that accompany the requested JSON artifact.

## Limits

These are narrow synthetic engineering-workflow probes. The exporter measures
behavior-test discrimination at declared boundaries, not general coding skill.
The triage case measures concrete action/state/report-field correctness and
bounded non-reproduction, not overall writing quality. Its free-text semantics,
candidate tool-execution provenance, and minimality are explicitly unassessed.
Two correct implementations and a separate oracle reduce correlated mistakes;
they are not formal proofs and were not authored by independent humans.

## Revision history

Version 1 is preserved at the separate v1 stage and must not be used for trials.
Independent review found the triage candidate-visible bounded_json.py mistakenly
contained the hidden exporter grader. This both exposed grading logic and broke
the isolated public triage command. Its 29 tests did not cover that command.
Version 2 installs the correct bounded loader and adds four checks for public
runner execution, common/trusted file parity, exact candidate-file inventory,
and hidden-source exclusion. No candidate saw either packet in a trial.
