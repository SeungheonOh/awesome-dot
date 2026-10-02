# Verification of the fictional comparison

Checked on 2026-10-02 with Python 3.12.14. The records are fictional; these checks establish the example's arithmetic and source accounting, not measured performance of a real assistant.

## What was actually checked

1. Checked the entry point's name and description, its required workflow sections, and the local references. These structural checks do not establish the substantive reliability of an analysis.
2. Read the available source records and review gates before comparing the timing results; the example retains an accepted-output boundary on both sides.
3. Executed the single Python block in [example.md](example.md) directly from the saved Markdown. Observed result: `PASS: quantity gates, correction, attempt counts, timing partitions, paired differences and bounds`.
4. Manually reconciled the input tables, review records and written result. There are six attempted tasks, five accepted final outputs, one unfinished task and one in-task retry. The two initial failing artifacts are A1-v1 and A3-v1. A1's soap correction changes 0 to 1 and its four correction minutes appear once. A2's 16-minute interval contains its unknown review; it is not added twice.
5. Checked the reported metric populations: one exact active-effort pair to acceptance, two elapsed-time pairs to acceptance, and three tasks per variant in session accounting. A3's measured time through cutoff never becomes time to acceptance. A2's missing active time remains bounded, not imputed.
6. Recomputed the headline numbers: P1 active −2 minutes and −14.3%; elapsed differences +7 and +12 with mean/median +9.5; baseline setup-inclusive effort 49; assisted effort bound 38–54; spent-effort difference −11 to +5. The example's outcome counts differ, so these totals do not establish equal-output savings.
7. Walked through missing-baseline, unreviewed-output, zero-baseline and mismatched-scope branches in the instructions. They require a one-variant description, unverified quality rather than presumed acceptance, no relative division by zero, and an unmatched or separate-group description respectively. These are author walkthroughs, not independent execution tests.
8. Checked all relative Markdown file links after the three files were saved. Each target exists in this folder. Read back the saved draft and example for the authorization boundary, unknown-versus-zero treatment, original assignment/order, setup scope and stop conditions.

## Commands

The example was executed from this folder without installing a dependency or creating a runner:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('example.md')
s = p.read_text()
blocks = s.split('```python\n')
assert len(blocks) == 2, 'Expected one runnable Python block'
code = blocks[1].split('\n```', 1)[0]
exec(compile(code, str(p) + '#arithmetic-check', 'exec'))
PY
```

The example's standard-library arithmetic block reproduces its numerical checks without an external service.

## Limits

All task records, timing values and outcomes in the worked example are fictional fixture data. The checks establish arithmetic consistency and the fixture's quantity/coverage decisions. They do not validate real timing instrumentation, reproduce actual assistant performance or establish external validity, statistical significance or cause.

The arithmetic block checks quantity vectors and row coverage; source-ID/unit rendering and review-event interpretation were checked manually from the supplied fixture. It is not a general parser or analysis engine. No source access, live output acceptance, saved-result delivery or cross-application behavior was exercised.

A separate source-to-result review independently recomputed the recorded efforts, bounds, acceptance denominators and elapsed differences without finding a numerical contradiction. Review of a different fictional case also preserved concurrent person-minutes, hybrid manual recovery, the original task identity of a retry and an unknown effort upper bound from incomplete logging. These were local reasoning checks, not a new real-world experiment.
