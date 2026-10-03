# Tooling lens

Review observed tool calls, errors, artifacts, and the workflow instructions that governed them. Stay within the supplied read scope and use actual tool schemas; neither this brief nor a session excerpt adds tool access or permission.

Look for a reusable technical failure: wrong artifact identity, stale result retrieval, a command whose successful exit was mistaken for behavior, unsafe shared state, cleanup that destroyed proof, or an unavailable integration treated as available. Distinguish a transient outage from a stable tool contract.

Consider missed self-service context: could an already authorized read have supplied the ticket, trace, or file the user had to paste? First verify that the capability existed then and that the proposed lookup was within scope. Do not recommend scanning all private sources to avoid one question.

Prefer structural enforcement for mechanical invariants. A parser test, typed configuration, or owned-process record can be stronger than more prose. Do not install or implement the mechanism during review.

For each finding return the exact evidence, reusable contract, proposed bounded change, target skill or mechanism, and a failure case that would test the improvement. Separate observed facts from uncertain platform behavior. Skip trivial retries and implementation details that will drift.
