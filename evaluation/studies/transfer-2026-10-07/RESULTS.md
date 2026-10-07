# Results and every scheduled status

All entries below come from the unchanged saved primary results. Twelve of twelve first submissions were on time. There are 156 pass, zero fail and zero unknown statuses. All 24 first captured output files retain their original bytes and hashes. Operational missingness, timeout and grader-infrastructure counts are all zero.

## Submissions in planned order

| Submission | Status | Pass / scheduled | Fail | Unknown | All met | First terminal observed UTC |
|---|---|---:|---:|---:|---|---|
| [t1-r1-c](evidence/results/t1-r1-c.json) | final_on_time | 14/14 | 0 | 0 | yes | 2026-10-07T04:22:44Z |
| [t1-r1-s](evidence/results/t1-r1-s.json) | final_on_time | 14/14 | 0 | 0 | yes | 2026-10-07T04:23:35Z |
| [t2-r1-s](evidence/results/t2-r1-s.json) | final_on_time | 12/12 | 0 | 0 | yes | 2026-10-07T04:28:01Z |
| [t2-r1-c](evidence/results/t2-r1-c.json) | final_on_time | 12/12 | 0 | 0 | yes | 2026-10-07T04:27:49Z |
| [t1-r2-s](evidence/results/t1-r2-s.json) | final_on_time | 14/14 | 0 | 0 | yes | 2026-10-07T04:31:18Z |
| [t1-r2-c](evidence/results/t1-r2-c.json) | final_on_time | 14/14 | 0 | 0 | yes | 2026-10-07T04:31:33Z |
| [t2-r2-c](evidence/results/t2-r2-c.json) | final_on_time | 12/12 | 0 | 0 | yes | 2026-10-07T04:36:05Z |
| [t2-r2-s](evidence/results/t2-r2-s.json) | final_on_time | 12/12 | 0 | 0 | yes | 2026-10-07T04:36:08Z |
| [t1-r3-c](evidence/results/t1-r3-c.json) | final_on_time | 14/14 | 0 | 0 | yes | 2026-10-07T04:38:26Z |
| [t1-r3-s](evidence/results/t1-r3-s.json) | final_on_time | 14/14 | 0 | 0 | yes | 2026-10-07T04:40:10Z |
| [t2-r3-s](evidence/results/t2-r3-s.json) | final_on_time | 12/12 | 0 | 0 | yes | 2026-10-07T04:44:10Z |
| [t2-r3-c](evidence/results/t2-r3-c.json) | final_on_time | 12/12 | 0 | 0 | yes | 2026-10-07T04:43:38Z |

## Descriptive summaries

| Case | Condition | Pass / scheduled | All met / planned | Verified fraction |
|---|---|---:|---:|---:|
| T1 | C | 42/42 | 3/3 | 1.0 |
| T1 | S | 42/42 | 3/3 | 1.0 |
| T2 | C | 36/36 | 3/3 | 1.0 |
| T2 | S | 36/36 | 3/3 | 1.0 |

Each condition has 78/78 checks and 6/6 all-met submissions. The equal-case mean is 1.0 for C and 1.0 for S. All six paired differences (T1 repeats 1–3, T2 repeats 1–3) are 0.0; both pair members were graded in every pair. This observed ceiling tie supports no efficacy, equivalence, speed, cost, population or production claim.

## Every T1 status

The fourteen rows by six submissions below account for all 84 scheduled T1 statuses. Check descriptions and frozen source-derived expectations are under `cases/T1/scoring/`.

| Check | t1-r1-c | t1-r1-s | t1-r2-c | t1-r2-s | t1-r3-c | t1-r3-s |
|---|---|---|---|---|---|---|
| charge_observed | pass | pass | pass | pass | pass | pass |
| charge_total | pass | pass | pass | pass | pass | pass |
| cohort | pass | pass | pass | pass | pass | pass |
| credit_observed | pass | pass | pass | pass | pass | pass |
| credit_total | pass | pass | pass | pass | pass | pass |
| exceptions | pass | pass | pass | pass | pass | pass |
| execution | pass | pass | pass | pass | pass | pass |
| feed_controls | pass | pass | pass | pass | pass | pass |
| net | pass | pass | pass | pass | pass | pass |
| partition_net | pass | pass | pass | pass | pass | pass |
| population_controls | pass | pass | pass | pass | pass | pass |
| schema_types | pass | pass | pass | pass | pass | pass |
| scope_parameters | pass | pass | pass | pass | pass | pass |
| unknowns | pass | pass | pass | pass | pass | pass |

## Every T2 status

The twelve rows by six submissions below account for all 72 scheduled T2 statuses. Check descriptions and frozen source-derived expectations are under `cases/T2/scoring/`. Free-text meaning is not certified.

| Check | t2-r1-c | t2-r1-s | t2-r2-c | t2-r2-s | t2-r3-c | t2-r3-s |
|---|---|---|---|---|---|---|
| T2-01 | pass | pass | pass | pass | pass | pass |
| T2-02 | pass | pass | pass | pass | pass | pass |
| T2-03 | pass | pass | pass | pass | pass | pass |
| T2-04 | pass | pass | pass | pass | pass | pass |
| T2-05 | pass | pass | pass | pass | pass | pass |
| T2-06 | pass | pass | pass | pass | pass | pass |
| T2-07 | pass | pass | pass | pass | pass | pass |
| T2-08 | pass | pass | pass | pass | pass | pass |
| T2-09 | pass | pass | pass | pass | pass | pass |
| T2-10 | pass | pass | pass | pass | pass | pass |
| T2-11 | pass | pass | pass | pass | pass | pass |
| T2-12 | pass | pass | pass | pass | pass | pass |

## Raw files and provenance

Each submission's two original files are under `outputs/<submission>/`. Their byte lengths and SHA-256 hashes appear in the unchanged individual and aggregate result records and in the manifest. Saved scorer stdout contains the original detailed reasons/evidence for every status. No statuses or output bytes were repaired or retuned during publication preparation.

The T2 repeat 1 C dispatch deviation remains attached to its passing observation. Its presence must not be omitted when discussing exact condition parity; impact is unknown. Collection was at observer time, so these output snapshots do not prove atomic generation-time contents.
