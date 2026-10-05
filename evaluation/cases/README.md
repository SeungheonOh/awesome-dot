# Cases

Eight original fictional task packets. Each directory contains only the task, its input manifest, and authorized inputs. [manifest.json](manifest.json) records exact bytes. Evaluator answers and controls live separately under [evaluators](../evaluators/README.md).

| Case | Task | Designated package | Required deliverables |
| --- | --- | --- | --- |
| [F1](F1/task.txt) | Reconcile expense evidence | expense-report-reconciliation | Claim lines, source map, exceptions |
| [F2](F2/task.txt) | Resolve meeting actions and handoff | meeting-action-handoff | Action records and handoff |
| [F3](F3/task.txt) | Find meeting windows | meeting-window-coordination | Ranked options and explanation |
| [F4](F4/task.txt) | Make a source-grounded decision | decision-source-brief | Decision brief |
| [F5](F5/task.txt) | Reconcile document revisions | document-revision-reconciliation | Candidate text and decisions |
| [F6](F6/task.txt) | Reconcile a SQLite report | sql-report-reconciliation | SQL, result CSV, and notes |
| [F7](F7/task.txt) | Verify a JSON Patch | compare-json-and-verify-patch | Patch, summary, and validation status |
| [F8](F8/task.txt) | Maintain a text-merge caller | build-text-merge-component | Edited caller/session, protected scaffold copies, regressions, and checks |

The task text is authoritative for the output contract. F6 includes a fixed SQLite database and corresponding CSV exports. F8 includes an intentionally incomplete starter scaffold; its smoke tests are candidate task material, not repository-wide passing tests.

The packets are public benchmark fixtures, not permanently held-out tasks. Supply only the appropriate packet allowlist to a fresh attempt. Never expose the answer keys, reference outputs, controls, or another attempt's artifacts. A different folder is not an access boundary.
