---
name: simulate-system-scenarios
description: Build and check a rule-based simulation to compare how a system evolves under stated scenarios. Use when the model, trajectories and scenario outcomes are the main deliverable, rather than a fitted predictor, analysis of existing observations, or a synthetic dataset alone.
---

# Simulate System Scenarios

Produce the requested simulation and an answer grounded in its actual outputs. Make the rules, initial conditions and omissions clear enough that someone can understand what the result means. A working program can faithfully implement an unrealistic model; distinguish implementation checks from evidence that the model represents a real system.

Use the requested format and level of detail. A short modeled comparison may need only its calculation and explanation; a reusable simulator needs a working entry point and saved inputs/results. Do not automatically add an interface, animation or large trace archive. Existing implementation and visualization workflows can support those deliverables when needed. A specific cache, retry or finite-state verification task may already have a more suitable workflow.

Use `solve-constrained-optimization` when the main output is a best feasible decision under an objective; comparing supplied simulation scenarios does not establish optimality over other choices.

## Define the modeled question

Start with the decision or behavior the user wants to understand. Identify the scenarios to compare, the outcomes that matter, and what is held constant. Preserve an accepted model rather than quietly replacing it with an easier one. Resolve an ambiguity when different choices materially change the conclusion, and continue independent work where possible.

Specify the state variables, their units, initial state, external inputs, transition or rate rules, and observation period. Distinguish individual entities from aggregate quantities. A fluid approximation may represent fractional work but cannot establish the schedule or completion of individual jobs without an additional model.

Keep modeled facts separate from assumptions and observed data. State consequential omissions such as failures, finite capacity, feedback, setup delays or correlated arrivals when they affect interpretation. Do not add phenomena merely to make the simulator elaborate, or present an invented distribution as an empirical one.

Define what the ending condition means. Stopping at a time, admitting no further arrivals and draining existing work, reaching an event, and approaching steady state answer different questions. Establish whether boundary events are included and which state is observed. An empty initial system may be the correct finite-run condition; it is not automatically a representative steady-state start.

## Give time and state explicit semantics

Choose a representation appropriate to the rules: direct calculation, discrete events, fixed time steps, differential equations, or another justified method. Check available tools before selecting a dependency. Keep simulated time distinct from the computer time taken to run the model.

For discrete events, define ordering at equal timestamps, admission and dispatch rules, ties, priorities and resource ownership. Decide whether same-time events form a batch before decisions occur or are processed sequentially. Do not let insertion order become an accidental policy. A library's scheduler may have a deterministic default that differs from the intended model; for example, [SimPy's scheduling documentation](https://simpy.readthedocs.io/en/stable/topical_guides/time_and_scheduling.html) explains its sequential ordering of equal-time events.

When a decision is meant to use only information available at that moment, keep future realizations out of that decision. A simulator may internally know a sampled completion time, but an online dispatch policy cannot use it unless the model explicitly grants that information. Preserve identities so state changes, resource use and later results can be traced to the right entity.

For continuous or stepped models, write the rates or update equations with consistent units. Separate state from cumulative flows. Carry state across parameter changes unless a reset is part of the model. Handle known discontinuities and regime changes deliberately; an interpolated curve across an unmodeled change can look smooth while answering the wrong problem.

Choose time resolution and numerical tolerances for the requested quantities. Output sampling times are not necessarily the solver's internal steps. A sparse table can miss an extremum or first threshold crossing; use an appropriate event calculation or bounded refinement when the question depends on that time. The [SciPy initial-value solver reference](https://docs.scipy.org/doc/scipy-1.17.0/reference/generated/scipy.integrate.solve_ivp.html) distinguishes requested output times, integration tolerances and event detection, including circumstances in which crossings can be missed.

Do not silently clamp negative inventories, normalize totals or skip conflicting events to hide an invalid update. Determine whether the issue is in the model, numerical method or implementation. A justified boundary rule belongs in the model and must be included in verification.

## Make scenario comparisons comparable

Change the intended scenario inputs while holding the comparison boundary and metric definitions consistent. Preserve the baseline and label each scenario. Avoid comparing a completed run against a partial one or changing initialization, sampling or exclusions without explaining the effect.

For stochastic models, define the relevant distributions and dependencies. State whether parameters come from supplied observations, an accepted theoretical model or invented assumptions. Independence is an assumption to justify, not a side effect of putting values in separate columns.

Control randomness according to the comparison. When common input realizations are appropriate, share them by stable entity/replication identity or controlled streams. Reusing one seed is insufficient if different scenarios consume draws in different orders or numbers. Retain the realized inputs when they are important to exact replay. Keep policy choices separate from the hidden random outcomes they are not allowed to know.

Choose a bounded number of replications or a justified precision criterion. Preserve failed, interrupted or invalid runs with their status instead of selecting only favorable results. Independent replications, multiple entities inside one replication and successive observations of one trajectory are different evidence units. More time samples do not create independent runs.

A deterministic scenario does not need artificial randomness or confidence intervals. For steady-state questions, justify any warm-up and observation window; do not discard the initial period of a finite-run question merely because warm-up is common in other simulations. Separate numerical error, Monte Carlo variation and uncertainty about model assumptions.

## Check the model implementation with meaningful controls

Inspect and run the actual requested computation within the authorized environment and practical resource limits. Preserve source inputs and distinguish a finished run from an event/time/work budget stop. Bound the relevant work without silently changing the modeled horizon or rules.

Use checks that can expose a consequential mistake:

- A small hand-checkable trajectory or known limiting case that tests the key transition, event order or rate interpretation
- Applicable balances, bounds, occupancy limits, nonnegativity or other invariants, calculated from actual state rather than only a parallel counter
- Location- or entity-specific checks where a correct aggregate could hide the wrong transfer or assignment
- A suitable numerical refinement, analytic comparison or alternative calculation when discretization or integration error could change the answer
- A consequential changed-input use of a reusable entry point, checking that outputs and descriptions reflect the actual parameter values

Choose the controls for the model; do not force every item into every task. A count balance does not prove correct priority decisions. A finer plot does not establish numerical convergence. Passing a reference case supports that case and mechanism, not every possible input or the real-world assumptions.

If observational data are available and model validity is part of the request, compare the relevant behavior against evidence not already used to tune the same claim. Explain discrepancies and coverage. Without that evidence, report internal consistency and modeled outcomes without inventing empirical validation.

## Derive metrics from the right population and window

Define the numerator, denominator, unit and observation boundary for each important result. Retain unfinished, rejected, lost or pending entities in the accounting where the question includes them. Latency among completed entities is a conditional result; a policy that leaves difficult work unfinished can look fast under that metric.

Distinguish a snapshot count, a count over an interval, a time-weighted average and an average over events or entities. Sampling queue length at event times does not generally produce its average over elapsed time. For a cumulative quantity, do not confuse the final total with its instantaneous rate.

Recompute important metrics from the saved trajectories, event records or other authoritative outputs. Keep scenario IDs, units and aggregation rules attached. Where paired replications were designed, form the within-pair comparison before summarizing it. Use intervals or statistical tests only when their assumptions and evidence units fit; descriptive ranges and percentiles are not automatically confidence intervals.

Show the tradeoffs that answer the question. A mean can improve while a tail, subgroup or final completion worsens. Do not declare one scenario universally better when the user has not supplied the preference needed to choose between those outcomes.

## Worked finite-queue boundary check

Suppose one worker runs A from time 0 to 10, B arrives at 0 needing one unit of service, and C arrives at 10 needing one unit. The waiting room has one place and the maximum queue wait is 10. Under a policy that processes completions, dispatches existing waiters, then admits arrivals, B starts at 10 and C waits until 11. If starting exactly at the deadline is allowed, all three complete. Expiring B before dispatch or admitting C before the existing waiter would implement a different policy. State that boundary choice and verify this trace explicitly.

For a bounded integer-time queue engine, a simple one-tick-at-a-time implementation can independently check a faster event-driven engine on small workloads. Compare each job's admission, state, start/end and worker assignment, not merely completed totals. Verify resource nonoverlap, queue occupancy bounds, deadline behavior and complete outcome accounting. Use maximum-size cases separately without stepping through an unnecessarily large integer horizon.

Keep completed-job percentiles conditional: with a long job running from 0 to 100 and a short job arriving at 1 with a wait budget of 5, the second may time out at 6. It must stay in the failure counts, not become a zero-latency observation or disappear from the workload denominator. Reconstruct percentile and utilization numerators from the retained job records.

For time-weighted queue summaries, reconstruct half-open intervals from each job's arrival, service start and terminal time. A wait ending in timeout still contributes waiting area; a zero-time rejection does not. Include initial idle time in an explicitly time-zero horizon. Example: one worker is idle until 5, serves A from 5 to 15, while B arrives at 5 and times out at 7. Waiting area is 2 job-time units, running area is 10, mean queue is 2/15 and utilization is 10/15. Averaging only the event snapshots gives a different and generally incorrect time average. Independently sum interval areas, per-job waiting/service durations, and a small integer-tick oracle. Check that same-time end/start transitions never create an artificial duration or overlapping worker assignment.

## Compare the same surviving entities

When scenarios admit or complete different work, compare population changes before interpreting latency. Join outcomes by stable entity ID and verify that arrival and service inputs match; row position is not identity. Partition the workload into completed in both, only in A, only in B and neither. These counts must sum to the full workload. Calculate paired latency differences only within the shared-completion subset, label that subset explicitly, and retain failures separately.

For example, if A completes jobs J1/J2 and B completes J1/J3, a smaller B percentile cannot establish that the same work sped up. J1 is the only paired observation; J2 and J3 represent different completion populations. Export the identities and B-minus-A differences so a reader can inspect this distinction. Never assign zero latency to failed jobs. Reversing A and B should exchange the exclusive populations and negate paired differences; reordering rows should leave the result unchanged. Self-comparison should show unchanged outcomes for every completion.

Verification example: a local finite FIFO model was exercised on 100 deterministic workloads with different pool and queue limits. Checks matched IDs after reversing row order, conserved all four populations, verified A/B symmetry and self-comparison, and rejected missing or changed workloads. This establishes implementation consistency for the bounded model, not production capacity or causal performance improvement.

## Deliver a usable, bounded result

Lead with the finding and the assumptions that materially qualify it. Provide the actual requested model, source or parameter file, results and concise invocation when reuse is requested. Preserve enough initial state, scenario configuration, random-input information and runtime detail to reproduce the delivered computation without hidden session state.

Reopen saved outputs and reconcile the reported values with them. Inspect delivered charts for readable labels, honest scales, correct units and scenario identity. Display precision must not masquerade as numerical or empirical accuracy. If only selected traces were retained, state that coverage rather than claiming a complete event archive.

Separate what was verified: rule implementation, numerical behavior, stochastic comparison, observed-data validation and any later interface or service integration. A simulation under invented assumptions can be useful for learning or design without establishing production throughput, physical safety or real-world causal effects. Deliver the requested evidence and limits; applying the modeled changes to real resources is a separate authorized action.
