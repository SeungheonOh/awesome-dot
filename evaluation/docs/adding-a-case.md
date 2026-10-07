# Evaluate one skill change

Start with a task where a wrong decision would matter, then decide what evidence would distinguish a useful result from a plausible-looking one. Keep the first comparison small. The [action-handoff example](../examples/action-handoff/task.txt) below is an executable author-control exercise, not a model result or a new benchmark case.

## 1. State the comparison before collecting outputs

Choose one question and label its conditions literally:

- **Package supplied / no designated package:** give both conditions the same common instructions and task inputs; supply the pinned target guide and its declared examples/helpers only in the first. “No designated package” does not mean an otherwise skill-free agent. Record ambient instructions and tools, including what you cannot inspect.
- **Previous skill / revised skill:** supply the corresponding pinned package in each condition. Record every changed file; this measures the package revision, not an isolated wording change unless wording is the only difference.

Keep the common inputs, permissions, allowed tools, requested model/reasoning settings, and budgets equal. Use fresh contexts. Record the requested configuration separately from observed runtime facts: if the actual serving model/build is not exposed, write `unknown`. A requested setting does not prove equal compute, and a skill being supplied does not prove it was used.

## 2. Write the task and a few checkable assertions

Use original fictional data or appropriately sanitized material. State the deliverable, source-of-truth rules, allowed actions, and what to do when facts are missing. Prefer a few assertions tied to consequential decisions over many formatting checks. Before seeing outputs, save the task, package identities, assertions, grader, planned attempts/order, budgets, and collection rules.

For the [action-handoff task](../examples/action-handoff/task.txt), three source lines contain an assigned and dated action, a tentative suggestion, and an agreed action with no assignee or deadline. Its four assertions check:

1. A valid JSON object with the requested fields and types
2. Exactly one entry for each agreed action, with no suggestion promoted to an action
3. The explicit owner and date preserved for the assigned action
4. Unknown owner and date retained as `null` for the unassigned action

The [checker](../examples/action-handoff/check.py) accepts either action order and either object-key order. It reads at most 16 KiB plus one byte, rejects duplicate JSON keys, and inspects data without executing submitted code. It checks this exact structured task; it does not judge general prose quality, delivered messages, or task completion outside the saved file. A future task that permits paraphrases needs a suitable content check rather than accidental exact-string matching.

## 3. Test the checker before testing a skill

Write both valid equivalents and deliberate errors. The [authored controls](../examples/action-handoff/test_check.py) include a correct answer, reversed order/changed whitespace, an invented owner or date, a promoted suggestion, duplicate or missing actions, malformed JSON, and missing fields. If an acceptable equivalent fails, or a relevant wrong answer passes, fix the assertion before freezing the study.

From the repository root, with POSIX Python 3.12 and no dependency installation:

```sh
python -I -B evaluation/examples/action-handoff/test_check.py -v
python -I -B evaluation/verify.py --tests-only
python -I -B evaluation/verify.py
```

The first command exercises only this example. The second includes it through a top-level test-discovery bridge. The third runs the core local verification for the original fixtures and two original studies; the [evaluation index](../README.md#verify-locally) also lists the separate package commands. These commands do not collect model outputs, recreate historical dispatch, or recover unpublished prompts from hashes or public projections. **Authored-control test passes are not model attempts or evidence of skill improvement.**

To inspect an already saved artifact, run:

```sh
python -I -B evaluation/examples/action-handoff/check.py /path/to/actions.json
```

Exit status is `0` for all four assertions passing, `1` for an invalid or failing captured artifact, and `2` when the artifact cannot be read and remains unassessed. For example, assigning Mira to S3 produces this assertion record:

```json
{
  "id": "unassigned_fields",
  "status": "failed",
  "evidence": {
    "source": "task.txt#S3",
    "observed": [{"source_id": "S3", "owner": "Mira", "due_date": null}]
  },
  "errors": ["S3 must occur once with owner and due_date both null"]
}
```

This is an authored negative example. The source locator identifies the labeled line in `task.txt`; it is not a claim that a model made this error. Preserve the whole checker report alongside the exact artifact when evaluating a real submission.

## 4. Collect first outputs without rewriting the record

For a new study, create a new versioned folder such as `evaluation/studies/action-handoff-YYYY-MM-DD-v1/`. Keep its task/package freeze, schedule, raw outputs, per-assertion evidence, operational status, and report together. Keep answer keys, grader code, and other attempts outside candidate access; directory separation alone does not enforce that boundary. State any isolation or blinding limits you cannot verify.

The [sealed-pilot harness](../harness/README.md) is not a general live launcher. Its source configuration fixes eight families and five criterion groups per case, and `live-run` always fails closed. Do not add “F9,” edit its frozen configuration, retrofit this example into it, or change published historical packages/results. Use a separately reviewed and authorized runtime for a new study; this guide and its checker do not supply one. The existing [protocol gates](protocol.md#before-model-trials) explain the missing runtime guarantees.

Give every planned attempt an ID before launch. Retain its first output exactly, including malformed, incomplete, or failing work. Do not strip fences, repair JSON, replace failures with retries, or choose the best repeat. If repairs or reruns are allowed, predeclare and report them as a separate phase with links to the originals.

Separate an assessed task failure from an operational collection failure or unavailable grading evidence. A captured JSON file missing a required field fails this task; an unreadable or never-captured artifact does not establish what the model produced. Keep unavailable outcomes and blocked assertions explicitly unassessed, with the reason, rather than silently passing them, counting them as model failures, or dropping them from the scheduled denominator. If a claim requires execution, semantic review, or external-delivery evidence you did not collect, leave that domain unassessed; source inspection alone does not establish a completed action.

## 5. Report the whole small comparison

Show every scheduled condition/case/repeat, its operational status, and passed/failed/unassessed assertions with source evidence. State the planned and assessed denominators. Keep authored controls separate from model attempts, and keep overlapping checks or review votes out of inflated sample counts. Report ties and regressions as prominently as improvements; do not select positive cases after seeing results.

Name the files and revisions compared, any deviations, and what the checks cannot establish. Report only measured usage or timing with its capture coverage; leave unavailable fields unknown. Do not fabricate tokens, cost, human effort, time savings, or speedups from observation windows. A small synthetic comparison supports a description of those artifacts, not a population-wide effectiveness claim; equal scores do not establish equivalence.

For the repository's existing definitions and limitations, see the [methodology](methodology.md), [protocol](protocol.md), and [published results index](../results/README.md). Keep each study's design and units separate when reporting it.

To plan a future end-to-end workflow study, see [Measure completed-workflow benefit](measuring-workflow-benefit.md) and its [blank record](../templates/workflow-study-record.md); this guidance does not report current observed productivity results.
