# Your first useful work task with dot

**Outcome:** turn an incomplete bug report into a clear investigation plan and a small set of acceptance tests.

This exercise uses fictional information below. You do not need a connected account, repository, real customer data or installed software. It demonstrates how to brief and review dot, not a completed product test. The suggested first-session budget is 10–15 minutes; actual time varies.

## 1. Give dot a complete, bounded task

Copy this entire prompt:

```text
dot, help me turn this fictional bug report into a useful engineering investigation brief. I am new to working with an AI assistant. Use only the information below; do not browse, open accounts or infer facts about a real product.

Product: a fictional team dashboard called Fieldboard.
Report: “When I hide archived projects, the dashboard looks correct, but the downloaded CSV still includes archived projects.”
Observed on: a desktop browser. Browser version and date are unknown.
Expected behavior: the CSV should contain the same set of projects visible under the current filters, across all result pages.
Available sample rows:
- P-101, Cedar, active
- P-102, Harbor, archived
- P-103, Juniper, active
- P-104, Kestrel, archived
Known controls: an “Include archived” toggle, a project-name search field, and pagination. We do not have the source code, logs or an actual application.

Produce three things: a concise bug ticket, a read-only investigation plan, and an acceptance-test checklist. Separate reported facts, assumptions and questions. State which missing answers would change the plan. Include tests for the toggle both on and off, a search with no matches, more than one page of results, and exporting twice after changing the filter.

Do not invent a root cause, claim to reproduce the bug or say a fix is verified. Keep the proposed tests independent of any particular framework. End with the smallest next step an engineer can take and what evidence would justify calling the issue resolved.
```

## 2. Review the result like an engineer

A strong result should preserve these facts:

- With “Include archived” off and no search, the sample export should contain P-101 and P-103 only
- With it on, all four sample rows should be eligible
- “Across all result pages” is different from exporting only the current page
- The CSV behavior is reported; it has not been reproduced here
- No code, logs or browser version are available

The result should not claim that a specific function, API or cache caused the bug. That would be a hypothesis without evidence.

## 3. Try a useful follow-up

```text
Review your brief for unsupported assumptions. Label each proposed cause as a hypothesis and say what observation would distinguish it from the alternatives. Then reduce the acceptance checklist to the smallest set that still catches stale filter state, pagination mistakes and an empty result.
```

This is a better iteration than “make it better” because it identifies the quality problem and the desired improvement.

## 4. Add one piece of evidence

Use this fictional update:

```text
New fictional evidence: the export request includes includeArchived=true even when the toggle is off. The visible table request includes includeArchived=false. Update the investigation plan and distinguish what this narrows down from what it still does not prove. Do not invent source code or claim the defect is fixed.
```

A good update narrows the investigation to how the export request is constructed, while still leaving the precise implementation and fix unverified.

## 5. Know when you are done

You are done with this exercise when you have a usable ticket, a bounded investigation plan, relevant edge cases and clearly marked unknowns. You have **not** reproduced or fixed a real application bug.

For a real work item, first check [what data you may provide](CORPORATE-DATA.md). Then use a [task brief](TASK-BRIEFS.md) to specify the repository, authorized scope, expected output and checks. A request to explain a failure is different from authorization to edit, push or deploy code.

## What you practiced

- Providing concrete inputs instead of an open-ended request
- Asking for a named output that you can inspect
- Distinguishing evidence from plausible explanation
- Checking edge cases and repeated actions
- Stopping at the correct milestone
