# F8 behavioral evidence

Both frozen F8 submissions passed the five original artifact criterion groups after source-reviewed local execution. [execution-results.json](execution-results.json) preserves the per-run results and exact artifact bindings in a public projection; command paths are normalized, and the original record's SHA-256 is included.

| Independent check | C | S |
| --- | ---: | ---: |
| Original behavioral probe | 5/5 groups | 5/5 groups |
| Full submitted suite | 18 passed | 19 passed |
| Focused regression suite | 15 passed | 16 passed |
| Reintroduced stale-generation defect | Detected | Detected |
| Reintroduced unresolved-save defect | Detected | Detected |
| Post-hoc lone-surrogate save/reload | Passed | `UnicodeEncodeError` on save |

The independently run full-suite counts match each submission's saved `checks.txt`. The sensitivity checks used separately assembled, source-reviewed scaffold defect replacements on separate copies, not repaired submissions or evaluator mutant fixtures. They produced targeted assertion failures: replacement tests observed generation 0 instead of 1; unresolved-save tests observed complete instead of draft. Nonzero exits were not treated as sufficient evidence by themselves.

## Execution scope

All submitted Python source and tests were read before execution. Exact-hash copies were run with a clean environment, no bytecode writes, a 10-second wall limit, five-second CPU limit, 512 MiB address-space limit, 8 MiB file-size limit, 64 open files, and core dumps disabled. Ordinary source-reviewed local execution is not a hardened OS sandbox. Process integrity and OS isolation remain unverified.

The production-facing F8 grader was not weakened: its ordinary API still returns pending behavioral groups. No author-fixture allowlist was expanded, and the author-fixture execution entry point was not used. The [original probe](original-probe.py) was extracted unchanged from the predeclared evaluator and its hash was verified before execution. This study separately combined its results with the actual full/focused suites, saved check report, and both defect-sensitivity checks for g5.

Both submitted suites create transient fixtures under a copied-root `.work` directory. This follows the common dispatch override but conflicts with the original task's outside-tree wording; it is a shared protocol inconsistency. Frozen delivered artifacts were unchanged and contain no temporary directory.

## Post-hoc robustness diagnostic

Source review identified a potential serialization difference. The exact same [diagnostic](posthoc-surrogate.py) then tested both submissions with `U+D800` followed by LF. Both constructed and displayed the exact text. C saved, parsed, reloaded, and preserved state/text. S raised `UnicodeEncodeError` while saving UTF-8 JSON because its save used unescaped non-ASCII text.

This diagnostic was not prespecified and does not alter the five primary scores. It is a narrow observed robustness difference, not a general treatment-effect estimate. A future protocol could explicitly specify Unicode serialization policy and include this case before outcomes are known.

The public [score script](../score.py) reads these saved records without running candidate code. Re-executing generated Python is a separate action that requires appropriate source review and a suitable environment.
