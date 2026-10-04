# Issue and project records

## Useful evidence

Issues often preserve the product problem, affected users, business deadlines, compliance requirements, and acceptance conditions behind engineering work. Parent initiatives and project documents can explain why a tactical subtask existed. Comments and status history reveal changed scope or a reopened failure.

## Search the actual tracker

Inspect the available read/search schema first. Start with exact issue IDs linked from commits or reviews, then search the feature name, prior name, business term, and error text within the relevant project and period. Do not guess tool calls or treat a missing integration as a searchable empty source.

Read full descriptions and relevant comments. Follow parents, subtasks, duplicates, and explicit links to a canonical record. Read attached project requirements when accessible. Labels and milestones guide searches but are not substitutes for a stated rationale.

## What distinguishes a strong finding

A dated comment saying “We chose B because A would change the billing contract” directly bears on the decision. A parent initiative may explain timing but not the technical mechanism. A customer-request label without the underlying description is circumstantial. A ticket's acceptance criteria may show the intended behavior even when the implementation fell short.

## Failure modes

- A closed ticket may have been reopened or repurposed; inspect history
- Generic template text is weak evidence of real motivation
- A duplicate chain can hide the substantive discussion
- A plan predating implementation may have been superseded
- Inaccessible private attachments remain a gap; do not infer their contents
- “Done” in the tracker does not prove the final product was verified

## Return

Include ticket ID, title, exact link, relevant dated statement, relationship to the target change, parent/project context, and direct versus circumstantial status. Record queries and useful nulls. Return cross-source document or discussion links as leads without contacting anyone or changing the issue.
