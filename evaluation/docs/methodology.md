# Methodology

## Research question

On these eight task cases, does supplying a designated skill package change acceptable first-submission completion, artifact quality, elapsed time, or provider-reported usage?

The unit of comparison is the same case attempted independently in two arms:

- **C, control:** common competent instruction, task, inputs, tool access, and time budget; no target package supplied
- **S, skill:** the same setup plus an exact allowlist from the designated pinned package

The treatment includes guide text and relevant bundled examples or helpers. It does not isolate the effect of wording, packaging, or instructions alone. Package presence does not prove the agent used it correctly. Guide/example reading and agent-side checks count toward the attempt's time cap.

## Design

Eight fictional A cases each receive one fresh C/S pair, for 16 planned attempts. Randomize case order and balance within-pair order at four CS and four SC pairs. Freeze the assignment seed and realized schedule before outcomes. Keep the agent/model/reasoning configuration and allowed tools identical within every pair.

The suite covers four everyday information workflows and four structured engineering/artifact workflows. The [case index](../cases/README.md) gives exact inputs and required outputs. F6 is within-domain SQL transfer; task resemblance to package examples limits generalization. No B variants or independently held-out replications are included.

Public tasks and answers can become familiar to models or users. Run-time isolation prevents direct answer access during an attempt; it cannot establish absence of pretraining exposure or prior familiarity. Disclose these limits, and use fresh independently authored cases for later claims beyond this suite.

## Outcomes

Each task has five predeclared criterion groups. Overall acceptance also requires protected-input/output integrity, process-integrity review, and review of free-text and verification claims. Missing reviews remain unknown. Synthetic semantic-review records only test grading integration; they are not independent ratings of model work.

Report:

1. Every scheduled attempt and its terminal or unresolved status
2. Raw C/S paired outcomes, absolute acceptance rates, and wins/ties/losses
3. Equal-case paired acceptance and quality differences on these cases
4. Missing-outcome bounds and leave-one-case-out sensitivity
5. Per-attempt elapsed time, timeout cap, and observed usage counters with coverage

Failures, timeouts, cancellations, interrupted attempts, and unscored submissions remain in the scheduled denominator. Do not silently exclude attempts, replace failures with retries, or select the best repeat. An authorized repair or rerun is a separately identified phase with its own accounting.

With one pair per case, this is an exploratory sample. Do not attach an inferential confidence interval, significance claim, power claim, or population-wide efficacy estimate. Missingness bounds are not population confidence intervals. Tied observed pairs do not establish certainty of no effect.

## Time and usage

Process elapsed time includes startup, service waits, guide/example reading, tools, and self-checks. Controller staging, blind export, and grading are recorded separately. Event-arrival intervals are local observation windows, not pure model compute. Accepted-pair latency is a selected-subset secondary measure.

Keep provider input, cached-input, cache-write, output, and reasoning-output counters separate. Preserve per-turn records and state scheduled, observed, and complete-capture coverage. Leave missing fields null; do not infer subset relationships, convert characters to tokens, or estimate dollar billing. Actual human review effort remains unmeasured unless separately observed.

## Limits

Local artifact tasks do not measure delivered emails, completed bookings, live calendar changes, account access, native document fidelity, or full dot product performance. No measured skill effect exists yet. Passing fixture tests establishes properties of the harness and graders only.
