---
name: solve-constrained-optimization
description: Formulate and solve linear or mixed-integer allocation, blending, and selection problems, then verify the returned plan and its optimality limits against the original rules. Use when a constrained optimum is the main output, rather than descriptive data analysis or ranking already supplied options.
---

# Solve Constrained Optimization

Deliver a usable allocation or decision, the model that gives it meaning, and evidence for its feasibility and claimed quality. If the requirements cannot be met or the solve remains incomplete, return that bounded result clearly. A solver's success flag is not a substitute for checking that the right problem was encoded.

Keep the requested scope. A small calculation may need only a transparent answer; a reusable planning request may need editable inputs, runnable source and saved results. Do not automatically build a dashboard or general-purpose solver. Fixed-duration job scheduling, finite configuration repairs and exactly-once cover have more specific workflows when those are the actual problem. A request to rank supplied options by preferences does not automatically need mathematical optimization.

## Establish what can change

Read the requirements, source data and any existing formulation before choosing an algorithm. Identify the decisions the user can actually make, their units and their domains. Continuous quantities, whole batches, binary choices and start times are different variables. A duration used as a quantity of work is not necessarily a clock interval; a quantity that must be purchased in packs cannot be treated as freely divisible.

Separate decision variables from fixed inputs and uncertain assumptions. Record consequential identity and indexing rules: whether two rows describe separate resources, alternative offers, repeated records or parts of one shared capacity. Preserve the user's definition of available stock, demand, cost, output and waste. Unknown capacity or cost is not automatically zero or unlimited.

Define the objective in terms the user recognizes, with its direction and units. Include fixed charges, per-unit charges, penalties or benefits only where the task supplies or accepts them. Distinguish an objective from a hard requirement: a budget cap cannot be violated merely because another term improves.

If several objectives matter, preserve the stated priority. Minimizing cost first and then waste among minimum-cost plans is different from minimizing a weighted sum. Do not invent exchange rates between credits, time and service quality. Resolve a missing consequential preference while continuing work that does not depend on it.

## Make the formulation traceable

Write the variables, bounds, objective and constraints in a form a reader can compare with the original rules. A compact equation set or named constraint table is often enough. Retain a mapping from solver coordinates to meaningful resource or option IDs.

Check the distinctions that can change the feasible set:

- At least, at most and exactly are different requirements. Allowed surplus must still consume the resources the contract assigns to it
- One production or allocation decision may create several outputs simultaneously; do not allocate its full capacity separately to each output
- Shared capacity must be counted across all users, periods or products that consume it. Carry inventory or balance terms across periods where required
- Once-only activation charges, minimum lots and conditional availability need their actual logical relationship to use. Work must not occur without its required activation, and an unused option must not incur an invented charge
- Whole counts and binary choices need explicit domains and bounds. A binary variable is not merely an unbounded nonnegative integer
- Existing commitments, locks and exclusions remain constraints unless the user asks to change them

Use valid, reasonably tight bounds for logical or activation formulations. An arbitrary huge constant can weaken the model or create numerical problems; an unjustifiably small one can exclude a legitimate solution. Preserve a nonlinear relationship when it is real. Products of decision variables, ratios with variable denominators and some conditional rules cannot simply be passed off as linear coefficients.

Check units and signs before solving. Multiplying a greater-than inequality by a negative value reverses its direction. A maximization converted to minimization must be converted back consistently in the reported objective and bounds. Default library bounds may exclude permitted negative values or allow unintended quantities; inspect them explicitly. The official [SciPy linear-programming reference](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.optimize.linprog.html) illustrates the distinction between variable bounds, equality rows and inequality rows.

## Choose a method suited to the model

Use available tools and a method appropriate to the variable domains and relationships. A transparent calculation or complete bounded enumeration may be preferable for a tiny problem. Linear programming handles divisible variables with linear relationships. Mixed-integer methods handle linear models with required integer or binary decisions; rounding a relaxed solution is not an integer optimization method.

For a nonlinear problem, keep the actual model and choose a suitable method or explain the unsupported part. A local convergence result does not by itself establish a global optimum. Do not relabel an approximation as an exact reformulation without justification.

Set computational limits proportional to the problem and requested confidence. Preserve relevant solver/version/settings, the exact model inputs and termination reason when using a solver. A time or search budget is a stopping condition, not a claim that all possibilities were examined. If the user supplied a proposed plan, check it against the original rules; a useful baseline may already be feasible even when it is not best.

Do not discard warnings, failed solves or contradictory diagnostics. Inspect formulation and numerical scale before changing requirements or trying increasingly expensive methods. When a small independent calculation, relaxation, lower bound or known case can test an important claim, use it. Exact arithmetic and proof certificates are valuable when warranted, but are not mandatory artifacts for every ordinary optimization request.

## Interpret the result before using its values

Keep these outcomes separate:

| Outcome | What it supports |
| --- | --- |
| Verified feasible plan | Its original constraints hold under the stated arithmetic or tolerance; optimality may remain unresolved |
| Optimum established within stated limits | Feasibility plus the method's applicable optimality evidence, including numerical tolerances where relevant |
| Search limit with an incumbent | A checked available plan, with any valid bound and remaining gap; not automatic optimality |
| Infeasible model | No plan satisfies the stated model, supported by a completed method or an applicable contradiction/certificate |
| Unbounded objective | The encoded model permits indefinite improvement in the objective direction; often a missing real constraint needs investigation |
| Invalid input, unsupported model or failed computation | No optimization conclusion follows until the problem is resolved |

A solver can stop without a usable candidate, and a returned vector can violate constraints within or beyond a numerical tolerance. Check the actual status before relying on objective or coordinate fields. For a minimization problem, a verified feasible plan supplies an upper bound; a justified relaxation or solver bound may supply a lower bound. Reverse that interpretation appropriately for maximization. Do not present a heuristic estimate as a certified bound.

Report a gap only when its two endpoints refer to the same objective and model. State whether it is absolute or relative, and avoid a misleading percentage when the objective is zero or near zero. Solver-reported optimality is subject to its documented tolerances; exact equality claims need corresponding evidence. The [SciPy mixed-integer reference](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.optimize.milp.html) documents statuses, optional incumbent values and objective-bound fields; other tools may use different conventions.

For a prioritized objective, establish the primary result before optimizing the secondary one over the appropriately fixed primary level. If the primary optimum is unresolved, say so rather than claiming a globally lexicographic result. Numerical slack used to preserve a primary level must not silently permit a material degradation.

## Verify the delivered plan against original rules

Recompute outputs, resource use and objective from the actual returned decisions and original input records. Avoid relying solely on the same transformed matrix or helper that built the model: a shared indexing, sign or double-counting mistake can make both agree on the wrong problem.

Check variable bounds and domains, all material constraints, activation logic and every objective component. Confirm that a purported integer plan really represents permitted whole decisions. Use tolerances appropriate to the quantity and numerical method, and disclose consequential residuals rather than hiding them behind display rounding. A mathematically tiny violation may still be unacceptable for an indivisible item or a hard external limit.

When delivering files, reopen the saved allocation and use it for the final readback. Preserve IDs, units and enough precision for its consumer. The report, model and saved plan must describe the same scenario. If runnable source is requested, exercise its documented invocation using the delivered inputs and inspect the actual output.

Treat a rounded or operationally simplified allocation as a new candidate. Check it again against every original requirement and recalculate its objective. Rounding up can exceed capacity; rounding down can miss demand. A repaired rounded plan may be useful without being optimal on its new grid. Do not transfer the unrounded solution's optimality claim to it.

## Explain limits and the next decision

Lead with the allocation or scoped failure and its practical meaning. Include the objective value, consequential binding constraints or spare capacity, quality evidence and material assumptions. Keep detailed logs or model files available when they help reuse; do not impose a full ledger on a short answer.

For infeasibility, identify a useful conflict or limiting condition when supported. Do not call a conflict minimal unless that was established. A separately labeled relaxation can show what would need to change, but it is not a feasible solution to the original request and must not replace it silently. For incomplete work, preserve the best checked plan and the unresolved quality limit.

Use sensitivity or alternate scenarios when uncertain inputs or a requested change could alter the decision. Re-solve the affected model and state what changed; a binding constraint or one local marginal value does not establish the result of an arbitrary large change. Distinguish exact supplied constants from measured estimates and uncertain future capacity.

An optimized plan is conditional on the model. Synthetic rates, assumed costs and idealized capacities do not establish real-world savings or operating guarantees. Return the requested artifact and checked conclusion; ordering resources, changing live allocations or deploying a policy requires its own authorized scope.
