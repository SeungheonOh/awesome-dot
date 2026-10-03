# Hillclimb

Use for repeated scientific improvement of one metric. Read the [execution contract](../references/execution-contract.md). One hypothesis, one measurement, one keep-or-revert decision is the unit of work.

## Inputs and bound

Name the metric, better direction, realistic workload, correctness/resource guardrails, noise threshold, and target. Agree a meaningful time/cost/attempt budget when absent and necessary. A minimum attempt count is used only if requested or justified by the experiment, never as an automatic quota. The stopping rule distinguishes target reached, authorized budget exhausted, blocked, and useful hypotheses exhausted. Never lower the target to manufacture success.

## Steps

1. Ground the workload in the complaint and architecture. Run easy and demanding realistic cases to establish that the harness is sensitive to the problem. If it cannot separate them, repair the measurement before tuning code.
2. Freeze a repeatable metric command and correctness gate. Record baseline revision, inputs, environment, repeated-sample distribution, and a passing baseline regression run. A harness revision creates a new measurement series; do not splice it silently into the old one.
3. Start a local decision trail. Record attempt ID, hypothesis/mechanism, candidate identity, before/after samples, delta, guardrail results, evidence, verdict, and reason. Review previous attempts before choosing the next one.
4. Apply one bounded hypothesis. Parallel alternatives require isolated worktrees and comparable inputs; their results must not write a shared branch. The integrating owner assesses each result rather than combining untested wins.
5. Measure baseline and candidate with the frozen harness, controlling warmup/order and noise. Run guardrails. Keep only a demonstrated meaningful improvement, or an explicitly justified simplification that holds performance. Revert a failed attempt's owned edits in full without disturbing other work. Commit accepted units only within authorized repository practice.
6. On a plateau, inspect rejected mechanisms and the profile. Try a genuinely different category or improve a demonstrated measurement defect. Combining near-misses is a new hypothesis requiring fresh proof. Do not churn random changes, weaken tests, or optimize the benchmark instead of the user's workload.
7. Revalidate the integrated accepted candidate, since independent wins may interact. Check the stop rule and record the terminal state. For a supported unattended run, use [Autonomous run](autonomous-run.md) for wake and resume mechanics while retaining this experiment's target and budget.

## Failure and recovery

A changed environment, dirty competing writer, noisy metric, or stale result invalidates the affected comparison. Resume from the last accepted candidate and preserved log, not from a worker's last claim. If cheap relevant hypotheses remain within the agreed budget, continue. If progress needs new authority, a different target, or disproportionate cost, explain the gate and hold the dependent work.

## Evidence and completion

Report target, baseline-to-final metric and percent delta, sample/noise treatment, attempts kept/reverted/inconclusive, accepted mechanisms, final correctness checks, log location, and the highest-value remaining idea. Label a budget-limited result as partial. Opening a PR is optional and separately authorized.
