# Eval

Use to test whether a skill, prompt, structure, or workflow change improves a defined outcome. Read the [execution contract](../references/execution-contract.md). An evaluation request authorizes the bounded experiment, not deployment or promotion of a winner.

## Inputs and preregistration

Name the baseline and variant, target behavior, representative task set, candidate environments, permitted tools, run/time/cost limits, and promotion threshold. Fix three to six observable criteria, failures that disqualify a result, and how ties or missing evidence are handled before seeing outputs. Include regression tasks outside the changed behavior. Do not claim general improvement from one convenient example.

## Steps

1. Freeze exact instruction and fixture identities. Keep baseline and variant workload, tool access, starting data, and run limits comparable. If the host cannot run both conditions, document the confound rather than calling the result controlled.
2. Create isolated candidate environments with ordinary project-shaped names. Keep evaluative labels, variant identity, scoring rubric, and other candidate results out of the visible prompt and files. The user task must remain natural and complete; blinding must not withhold safety constraints or required task information.
3. Run the same organic request per condition. Use independent contexts if available. Repeat or counterbalance enough to address expected variance within budget. If only one context is available, describe sequential contamination and avoid claims of independent agents or model diversity.
4. Save outputs, diffs, executed checks, timings, and sanctioned observable tool traces. Do not request private reasoning or infer which instructions were read from self-report. If the host exposes no authorized execution trace, mark instruction-following evidence unavailable; never search guessed private transcript stores.
5. Give a separate judge anonymized outputs and the fixed rubric. Score matched outputs on the same scale without provider/model labels. Prefer executable correctness and safety checks over taste. If independent judging is unavailable, report self-assessment explicitly.
6. Inspect every submitted artifact and reconcile judge claims against evidence. A missing output, failed tool, or timed-out run is a result to count, not silently drop. Investigate rubric ambiguity and report disagreements without changing scoring to favor a preferred variant.
7. Summarize per-criterion results, failures, variability, resource cost, and confounds. Recommend promotion only within the tested scope and threshold. Additional tasks or a revised metric form a new experiment, not a retroactive correction of the original result.

## Failure and completion

Stop the dependent run on unauthorized data sharing, missing essential tools, or unsafe fixture behavior. Retain failed receipts. Return variant identities, preregistered criteria, task/run counts, evidence class (static, simulated, or live host), blinded judge status, results, limits, and the promotion recommendation. Do not advertise an unrun host as compatible or install the variant automatically.
