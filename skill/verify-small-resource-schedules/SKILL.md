---
name: verify-small-resource-schedules
description: "Check a bounded job schedule for precedence and resource conflicts, derive finish-time lower bounds, and distinguish a feasible plan from an exact optimum or an incomplete search."
---

# Verify a Small Resource-Constrained Schedule

## When to use

Use this when an agent or user has a small set of jobs, fixed durations and dependencies and needs a reviewable plan before executing anything. Typical inputs are a simplified CI pipeline, a synthetic scheduling exercise or a bounded production-plan model.

The task checks the supplied model. It does not trigger builds, assign real staff, change CI configuration, reserve resources or predict production runtime from invented durations. If durations are uncertain measurements, retain that uncertainty separately from the deterministic calculation.

## Required inputs

- Jobs with stable IDs, labels, duration units and prerequisite IDs
- Worker/resource count and whether resources are interchangeable
- Any release times, deadlines, setup/transfer costs, affinity rules or preemption permissions
- The candidate schedule, if the request is verification rather than generation
- The objective, such as earliest final completion, and any discrete-time or search-size restriction
- The authorized output and whether changes to the plan are allowed

A simple two-identical-worker model may exclude release dates, setup costs and preemption, but those exclusions must be stated. Do not silently reduce heterogeneous workers or a job needing several resources simultaneously to that model.

## Workflow

### 1. Establish the exact scheduling model

Preserve the supplied graph and candidate plan. Confirm the time unit and whether durations and starts are integers. Validate stable unique IDs, positive finite durations, known prerequisite references and the supported resource model. Detect cycles before looking for an execution order; a topological-order failure is not a slow solver.

Keep job labels separate from identity so renaming a display label does not change dependencies. Do not treat an omitted prerequisite list as evidence of independence when the input schema leaves that field unknown. Ask for a missing rule when it changes feasibility, while completing independent input checks.

For real CI, record whether durations came from one run, a percentile, a bound or a synthetic example. A fixed-duration result does not account for cache misses, queue delay, contention or flaky retries unless the model includes them.

### 2. Verify the candidate before optimizing

Represent each job by resource assignment and a half-open interval [start,end), with end=start+duration. Check every job is assigned exactly as required, starts within the modeled horizon and obeys the declared time granularity.

For each dependency A→B, require end(A)≤start(B). For each pair sharing an exclusive resource, require nonoverlapping intervals. Touching endpoints are allowed under the half-open convention. List violations with job IDs, resource and exact intervals rather than a single undifferentiated invalid result.

Calculate makespan only for a complete plan. If some rows are missing or invalid, report the observed partial extent without calling it the final completion time. Do not export an incomplete plan as ready to execute.

### 3. Derive lower bounds with their assumptions

For interchangeable workers and indivisible nonpreemptive jobs, total work divided by worker count gives a load lower bound. With integer time, round that bound upward. The longest weighted path through the prerequisite DAG gives a precedence lower bound. Their maximum is still only a lower bound.

Check these calculations independently of the candidate schedule. A valid schedule whose makespan equals a proven lower bound is optimal for the modeled objective. A schedule above the bound may or may not be improvable; the gap alone is not proof of wasted time.

Do not use this bound unchanged for unequal worker speeds, simultaneous resource demands or unmodeled setup/transfer times. Those require the relevant additional constraints.

### 4. Search only within a declared finite scope

If exact generation is requested and the domain is small enough, test increasing integer horizons beginning at the lower bound. Within a horizon, enumerate permissible start times and worker assignments consistent with prerequisites and resource occupancy. A fixed topological assignment order is acceptable when all permissible starts and assignments are still covered.

Use pruning only when its validity is established. A job’s remaining dependency-chain length can limit its latest possible start. Worker-label symmetry can reduce equivalent choices only for interchangeable resources with the same relevant state. Do not force a particular source job to start at zero merely because that makes search convenient.

Record the node/time budget and whether each smaller horizon was fully ruled out. Finding a feasible schedule does not prove optimality unless a lower bound is met or all smaller relevant horizons have been excluded. If the budget is reached, return a verified feasible incumbent or the original valid plan with optimality unverified. Do not replace a user’s better valid plan with a slower fallback just because the search stopped.

### 5. Independently check and explain the result

Run the resulting plan through a separate feasibility check, recomputing ends, overlaps, prerequisite constraints and makespan. For small synthetic cases, compare the solver with an independent enumeration that does not reuse its pruning or lower-bound logic.

Separate three conclusions: feasible, optimal under the declared finite model, and useful for the real workflow. Only the first two follow from scheduling arithmetic. Operational usefulness also depends on whether the input durations and omitted constraints are realistic.

Return enough evidence to reproduce the result, including the immutable graph, plan, modeled constraints and the specific search outcome. Do not execute jobs or change a production pipeline as part of a planning review.

## Deliverables

- Validated job/dependency inventory and model assumptions
- Candidate violations, if any, with exact resource/time witnesses
- A feasible plan or an explicit unresolved/no-feasible-plan result within the tested horizon
- Load and precedence lower bounds, final makespan and the basis of any optimality claim
- Search budget, tested coverage and operational limits

## Worked example

Three fictional jobs A, B and C each require 3 integer ticks. They have no dependencies and cannot pause. Two identical workers are available at tick 0; one worker can run only one job at a time.

Total work is 9 ticks, so the rounded load bound is ceil(9/2)=5. The longest dependency chain is 3. The combined bound is therefore 5, but a finish time of 5 is impossible: a worker cannot fit two indivisible 3-tick jobs into five ticks, so two workers can complete at most two such jobs by then.

A feasible schedule is:

| Job | Worker | Interval |
| --- | --- | --- |
| A | 1 | [0,3) |
| B | 2 | [0,3) |
| C | 1 | [3,6) |

Its makespan is 6. A and C touch at tick 3 without overlapping. The direct capacity argument rules out horizon 5, establishing optimality for this model. The worked fixture was also executed by a bounded integer solver, which returned makespan 6 after 17 search nodes. An independent small-case enumeration was used on 81 duration/dependency combinations to check the solver’s results; that finite test coverage is not a certification of arbitrary scheduling software.

If C instead needs a specialized worker or may overlap a setup phase, this is a different model. Keep the original result qualified rather than silently applying it to the revised constraints.

## Failure and recovery

- **Cycle or missing reference:** return the offending graph evidence; do not delete an edge to obtain a plan
- **Invalid candidate:** preserve it and show violations; change it only within the requested planning scope
- **Budget reached:** retain a verified valid plan, lower bound and unresolved optimality; do not label the first found plan shortest
- **Unsupported resources or fractional timing:** identify the unsupported assumption and ask for the smallest model decision
- **Late asynchronous solver response:** discard it if the graph or candidate has changed; it must not overwrite newer user work

## Example request

“Check these jobs and this two-worker plan. Durations are fixed integer ticks, workers are interchangeable and jobs cannot pause. Show dependency or overlap errors, calculate finish-time lower bounds, and, if the bounded search completes, return the shortest feasible plan. Preserve the original and do not run or edit the real pipeline.”
