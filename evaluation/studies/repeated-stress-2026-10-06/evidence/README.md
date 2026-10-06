# Saved grading evidence

[Study overview](../README.md) · [All outcomes](../results/attempts.json) · [Methods](../methods/README.md)

- [Mechanical reports](objective/): R1/R2 JSON checks and R3 read-only SQL checks, with original raw stdout/stderr and path-redacted execution records
- [Semantic review bindings](semantic/index.json): 24 distinct AI-assisted masked reviews, two per R1/R2 submission, with all original rationales and the unchanged frozen-grader merge
- [Bounded behavioral reports](behavioral/index.json): six source-reviewed R4 executions of the same 13 frozen requirements, with exact reports/logs and public plan summaries

The 36 semantic requirement instances received 72 initial votes, all passing; no disagreement or third review was needed. Mechanical reports were retained even where later semantic integration supplements them. R4 behavior was assessed separately, so the R1–R3 source audit's out-of-scope R4 rows are not primary missingness in the final study.

Public projections are labeled and retain original record hashes. Hashes of omitted private plan/approval details and machine paths are commitments; they do not make those omitted records independently reproducible. Candidate notes are self-reports, not independent test evidence. No model rerun is needed to inspect or reproduce this saved accounting.
