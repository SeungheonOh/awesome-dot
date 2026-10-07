# Observable response interface, version 1

Return one JSON object conforming to `output-schema.v1.json`. This interface is identical in both possible future conditions. It requests an observable plan, not private reasoning or executed work.

- `case_id`: the supplied case identifier
- `decision`: `route` when a workflow fits an identifiable result, including a result with an unresolved prerequisite; `clarify` when the desired result or materially different scope needs a question first; `no_fit` when none of the ten supplied candidates fits
- `workflow_sequence`: chosen candidate names in intended dependency order; empty when no route is selected. A clarification may name a provisional route if its conditional status is explicit. Ordinary substeps do not require separate workflow names
- `reason`: a short task-level explanation of fit or uncertainty
- `next_action`: the concrete intended action or bounded partial work, in future/planning terms
- `question`: a focused user question when needed, otherwise `null`
- `prerequisites`: unresolved requirements, each classified as input, capability, or authority, with a concrete description; empty when none are unresolved
- `handoffs`: necessary artifact dependencies between named workflows or ordinary substeps; empty when none are needed. `from` and `to` are descriptive labels and may name ordinary substeps
- `scope`: the boundary of the intended work and of any collection-coverage claim

There is no required wording, answer length, mandatory workflow count, or preferred candidate ranking. Extra workflows are not rewarded. All common candidate texts are available in full. The response should reflect the scenario's actual requested result and constraints.
