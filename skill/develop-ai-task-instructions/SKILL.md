---
name: develop-ai-task-instructions
description: Develop, improve, or compare reusable AI task instructions with task-specific evaluation cases, acceptance checks, and bounded evidence. Use when the deliverable is instructions or their evaluation for future inputs, rather than completing the downstream task once. Preserve supplied candidates in evaluation-only work.
---

# Develop AI Task Instructions

Deliver instructions someone can use again, together with a practical way to judge whether they work for the intended task. When execution is requested and available within scope, return actual case-level results. A plausible rewrite or the author's self-review alone does not establish improvement.

Keep development and evaluation in one workflow. For evaluation-only requests, retain the exact supplied candidates and report findings; proposed revisions remain separate and untested until developing them is authorized. A request for one extraction, summary, or other finished answer should use that task's workflow directly.

## Establish the task contract

Read the user's requirements, existing instructions, supplied examples, and relevant consumer requirements. Identify the future task these instructions must support and the decision the evaluation should inform: readiness for a bounded use, comparison of candidates, or diagnosis of a known failure.

Settle the consequential parts of the contract:

- Inputs and variable meanings, permitted source material, relevant conversation context, and capabilities the task actually requires
- Output content and format, field types or relationships where applicable, and meaningful limits on length or scope
- Treatment of missing, ambiguous, conflicting, or unusable input, including when to ask for clarification or return an unresolved value
- Must-pass requirements, acceptable variation, and preferences that can be traded off under the user's priorities
- Requested target system, execution access, resource limits, and authorized deliverable destination

Do not infer correctness from the old prompt's behavior. If examples conflict with a written requirement, identify the conflict before making it an acceptance rule. Use disclosed assumptions for ordinary gaps; ask only when an unresolved choice changes the task or the comparison. Continue work on settled requirements.

Size the work to the decision. A narrow formatting instruction may need a few discriminating cases and exact checks. Source-grounded synthesis needs meaningful content judgments. Neither needs a standard benchmark size, grading framework, or elaborate automation by default.

## Develop the candidate when requested

When creating or improving instructions, produce the actual candidate text in the requested form. For evaluation-only work, inspect the supplied candidates and continue to defining cases without rewriting them. State the intended result, available inputs, consequential decision rules, and output contract clearly enough to work without this conversation. Define replaceable variables and how their values are supplied. Keep stable instructions distinguishable from each task's source material and examples.

Use examples when they clarify a decision that prose alone leaves ambiguous. Check that every example obeys the contract, including its missing-value and uncertainty rules. Vary the underlying situation when useful; several near-identical examples may teach an accidental pattern. Do not hard-code evaluation answers into a supposedly general instruction.

Preserve the user's chosen format and scope. Add a procedure only where it improves an observable result. Remove contradictions and irrelevant instructions instead of continually appending exceptions. If the task requires unavailable source material, tools, or context capacity, identify that dependency; more emphatic wording cannot supply it.

For an existing candidate, keep a recoverable original and assign a new version to each revision. If activation or selection of the instructions is itself part of the requested behavior, include appropriate and inappropriate invocation cases and distinguish selection results from task results. Merely packaging text as a skill does not establish either behavior.

## Define cases and expected properties

Choose original fictional or otherwise authorized inputs that exercise the decisions in the contract. Include ordinary work and relevant variations, such as missing information, repeated records, qualified statements, or a valid unusual format. Select coverage for plausible task failures rather than generating a large arbitrary set. Mark synthetic inputs as synthetic; do not present invented frequencies as the real input distribution.

For each case, retain its identity, input version, purpose, and expected properties with a basis in the requirement or source. Define those properties before inspecting candidate outputs. Check generated expectations independently against the source; accepting the same model's generated answer as its own oracle can preserve the same mistake. A useful case must distinguish acceptable behavior from a plausible error.

For example, a fictional invoice case might require two occurrences of the same line item to survive and an identifier's leading zero to remain intact. A fictional meeting case might require a tentative date to remain tentative and an unassigned action to have no invented owner. These are content properties; the evaluator need not insist on one sentence's wording.

Separate cases used to write or select candidates from held-out checks reserved for the selected candidate. Record which inputs, references, and results were exposed during development. Near-duplicate documents or variants of one source belong in the same exposure group when they reveal each other's answers. An already inspected example cannot become held out merely by moving it to another folder.

Once held-out results inform a revision or selection, record that exposure and treat them as development evidence for subsequent versions. Use fresh checks when justified and available, or state that the final checks were reused. Do not claim an untouched set when the same author created and used all of it during development. The executing candidate receives each case's authorized input, but not its hidden reference answer or grading notes.

## Choose checks that match the contract

Use deterministic checks for properties with a reliable exact rule: parseability, required fields, types, counts, exact identifiers, numeric tolerances, or supported relationships. Define any normalization before comparison and preserve meaningful distinctions such as leading zeros, duplicates, and null versus zero. A valid schema does not establish correct content.

Use a semantic rubric for properties such as faithfulness, material coverage, preservation of uncertainty, or suitability for a stated audience. Describe observable grounds for each decision and provide anchors when the categories would otherwise be vague. Allow valid alternatives to a reference answer. Require evidence from the source and output for consequential judgments, not a grader's confidence number.

Keep must-pass gates separate from preference scores. An elegant answer with an invented fact does not become acceptable by averaging accuracy with style when factual support is required. Define aggregation, thresholds, and tie handling before comparing candidates; do not invent weights or loosen a gate to favor the preferred version. Use pass, fail, or unverified where the available evidence supports those distinctions.

Check the evaluator as well as the candidate. Inspect disagreements, borderline decisions, and suspicious passes against the contract and original material. A grader can misread a reference or reward the wrong feature. If a rule or reference is corrected, preserve the reason and regrade all affected candidates consistently. Leave genuinely unresolved judgments visible rather than forcing a winner.

For model-assisted judging, keep the rubric and grader version fixed within a comparison. Hide candidate labels where useful and check whether reversing pair order changes a consequential judgment. Do not let verbosity substitute for satisfying a requirement. These are known concerns in [OpenAI's evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices); a second model judgment still needs calibration against source-based decisions. Distinguish actual human review, model-assisted review, and author self-review.

## Freeze the comparison and run within bounds

Before a measured comparison, save the exact candidate versions, case versions, checks, rubric, and run plan. Preserve the rendered instruction and input actually submitted, including relevant message roles, examples, attachments, or retrieved context. A filename or candidate nickname alone is insufficient to identify what ran; use immutable copies, hashes, or an equivalent version record.

Record the target and runtime as exposed by the execution environment: provider/model identifier, snapshot if available, consequential settings, output limits, tools, context handling, and run date. Mark unexposed identity or settings as unknown. Do not infer a model version from its writing or self-description. Model versions can affect behavior, as [OpenAI's prompting documentation](https://developers.openai.com/api/docs/guides/prompt-engineering) explains; a named model alias is not evidence of an immutable runtime.

Use comparable conditions across candidates. Keep source versions, available capabilities, supplied context, and grading criteria matched unless that difference is the explicit subject of the comparison. Start clean contexts where the test requires them; document unavoidable shared history. If several factors change together, attribute the result to the combined change rather than the wording alone.

Choose a finite case set and a bounded repetition plan proportionate to expected variability and available resources. Declare the number of repetitions, retry policy, resource ceiling, and stopping conditions before seeing favorable outcomes. Repeats can reveal instability on the same cases; they do not create additional distinct tasks. Fresh contexts on the same model are not independent models, populations, or evidence of general performance.

Run only through capabilities that are available and authorized for the requested work. Use isolated outputs for local trials. Creating instructions or preparing evaluations does not itself authorize external API calls, new installations, live service mutations, deployment, or ongoing monitoring. If the target cannot be run, finish the candidate, cases, and checks; label the comparison unrun. A local surrogate trial may be useful when within scope, but identify its difference from the requested target.

Retain every planned run's disposition and every attempted run's output or error. Distinguish task failures, malformed or truncated outputs, incomplete execution, infrastructure failures, and runs never started. Link retries to their original attempts; never replace a failure with a later success or keep retrying for an attractive answer. Record measured resource use where available and mark missing usage unknown.

## Diagnose, revise, and compare

Summarize results by requirement and meaningful case group. Show distinct cases, attempted runs, repeats, retries, passes, failures, and unverified outcomes with explicit denominators. Keep operational completion separate from quality among completed outputs. A timeout without an answer cannot pass content checks; it also does not establish which content error the model would have made. Avoid reporting only the best repeat or only completed successes.

Inspect actual failures before editing instructions. Distinguish an instruction defect from missing context, a task capability limit, a faulty test input, an incorrect expectation, or a grading error. Make changes that address the supported cause. When development is authorized, revise the smallest useful portion, preserve the earlier candidate, and rerun affected cases plus relevant checks for regressions. A fix for one case should not silently change the overall contract.

Keep development gains separate from held-out results. Report the cases where a candidate improves, regresses, ties, or remains uncertain. If candidates meet different preferences, apply the user's priority or state the unresolved tradeoff. Synthetic results establish behavior only on the tested fictional cases and conditions; they are not production benchmarks. Small or dependent samples do not justify population accuracy, statistical significance, or broad superiority claims.

Stop under the declared conditions when the requested decision is supported, the limit is reached, or a material blocker prevents further authorized work. An inconclusive comparison is a valid result. Name the smallest useful next evidence rather than expanding the evaluation indefinitely.

## Deliver and verify the reusable result

Return the candidate instructions, their input and invocation contract, and the task-specific cases and checks in the requested format. For evaluation-only work, deliver the evaluation alongside the unchanged supplied candidates. Include the exact versions and available runtime details needed to interpret or repeat the work, the exposure history, and concise case-level findings when execution occurred.

Separate measured observations, source-based review, proposed improvements, and unrun checks. State which version is recommended and why only when the evidence supports that choice. Retain meaningful failures and known limitations in the deliverable rather than hiding them behind a single score.

Reopen the saved artifacts. Confirm that variables, referenced inputs, expected properties, and output requirements are usable without hidden context; that results identify the candidate actually run; and that any promised checks or examples exist and can be read. If the final candidate changed after the last run, identify it as untested until the relevant checks are repeated. Deliver the verified location or files without implying publication or integration occurred.
