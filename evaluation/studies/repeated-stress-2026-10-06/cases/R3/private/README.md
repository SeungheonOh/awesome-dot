# R3 evaluator interface

Explicitly fictional, authored offline SQL maintenance case. Candidate cap: 900 seconds. Candidate packet is ../candidate only. Never expose this directory during the task.

Submission: candidate/output/report.sql (or the same relative path in a trial copy).

Run from any directory:

    PYTHONDONTWRITEBYTECODE=1 python private/grade.py --sql /absolute/trial/output/report.sql

The command writes one JSON report to stdout and returns 2 only for an ungraded infrastructure/input problem. Read `totals` and check statuses, not exit code, to score. Checks are pass/fail/unknown, with equal weight; keep unknown separate. Unsupported execution or malformed inputs are not silently converted to behavioral failures. A query error fails execution; dependent checks are unknown. Missing groups fail grouping; a measure with mismatched observed values fails, while matching observed values with missing coverage remains unknown.

The grader uses canonical public fixtures, copied by bounded no-follow reads into its own disposable private/tmp directory. SQL is a single statement on a read-only immutable SQLite connection. The authorizer only permits SELECT, approved-table READ, and a deterministic-function allowlist. SQL size, SQLite limits, 50M VM progress instructions, five-second progress deadline, and 10,000 rows bound execution. ATTACH, writes, schema access, PRAGMA, and external functions are denied.

`build_fixture.py` documents the fixed seed and produces fixtures plus `expected.json`. Its `oracle` walks Python row dictionaries/lists and child-event sums; it does not query SQLite and does not use the reference query. `reference.sql` is a separately expressed correct query. There are no hidden data sources or holdout windows; three scenarios are public. All 12 checks are listed in manifest.json and TASK.md.

Author validation:

    PYTHONDONTWRITEBYTECODE=1 python private/grade.py --sql private/reference.sql
    PYTHONDONTWRITEBYTECODE=1 python private/validate_controls.py

Saved evidence: reference_result.json (12/12) and control_results.json (seven detected negative controls). Independent validity review also tested an ordinary correlated-subquery solution, which motivated raising the VM limit to avoid query-structure bias.

`manifest.json` records SHA-256 for candidate files and private artifacts. Hashes exclude the manifest itself and disposable directories. The manifest is the freeze boundary. No candidate model runs or publication were performed by the author.
