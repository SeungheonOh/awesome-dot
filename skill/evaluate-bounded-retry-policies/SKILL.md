---
name: evaluate-bounded-retry-policies
description: "Evaluate a retry policy against operation safety, attempt and time budgets, provider hints and reproducible failure scenarios before applying it to an authorized integration."
---

# Evaluate a bounded retry policy

## When to use

Use this when an integration needs more reliable recovery from transient failures, or when comparing retry behavior before a code change. Return an explicit policy and evidence about its bounded behavior. A simulation does not authorize live requests or prove production capacity.

## Required inputs

- The authorized operation, target and whether it can change external state
- Service-specific retryable outcomes and documented rate-limit hints
- Existing client/SDK retry behavior and ownership of cancellation
- Maximum total attempts, end-to-end deadline and per-attempt timeout
- Backoff base, cap and jitter policy
- Representative failure scenarios and the permitted test environment

If operation safety or the effect of a previous uncertain attempt is unknown, resolve that before repeating a consequential request. A timeout can mean that a response was lost after the server acted.

## Workflow

### 1. Diagnose the failure class first

Separate a transient response from invalid input, missing authorization, an unsupported client configuration or a permanent contract mismatch. Follow the provider's documented classification rather than retrying every exception or every response in a broad status class.

Inspect the exact error, endpoint, request method and relevant client configuration. For example, one client timing out while another succeeds may warrant checking its documented use of the environment's proxy settings before adding more attempts. Keep normal network and certificate protections intact.

### 2. Establish whether repeating the operation is safe

For a read-only operation, confirm the same bounded read can be repeated. For a mutation, use the service's actual idempotency or reconciliation contract. Reusing an operation identity may be essential; generating a new one for every retry can defeat deduplication.

Check the result of an uncertain prior attempt when the service offers an authorized status lookup. Do not infer “nothing happened” from a disconnected client. [AWS's guidance on idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) explains this distinction between repeated requests and repeated effects.

### 3. Set one overall budget

State whether the configured number means total attempts or retries after the first attempt. Count all attempted calls consistently, including rate-limited responses when that is the chosen contract. Do not let an outer loop multiply a hidden SDK retry budget without accounting for it.

Use a monotonic elapsed-time deadline for execution. Before sleeping and again before starting another attempt, check remaining time and cancellation. Bound each attempt by the remaining overall time, and stop when another attempt cannot fit. A cap on backoff alone is not a cap on total execution time.

### 4. Combine backoff and provider guidance deliberately

Define the base delay, growth and local cap, then specify the jitter distribution. “Use jitter” is not enough to reproduce behavior. Two common choices draw from zero to the capped delay, or from half the cap to the cap; they have different expected delays.

Parse provider hints according to their documented representation. HTTP Retry-After can use a date or a nonnegative integer number of seconds; see [RFC 9110 section 10.2.3](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after). Handle malformed values and clock disagreement explicitly.

When a hint establishes an earliest allowed retry, do not shorten that wait to fit a local backoff cap. Wait at least as long as required, or stop if the overall deadline would be exceeded. Record whether jitter is applied before or after the provider minimum. The [AWS retry/backoff pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/retry-backoff.html) provides broader context on retry load and operation safety.

### 5. Compare the costs as well as completion

For a synthetic comparison, fix arrivals, service assumptions, failure timing, attempt budgets and random inputs. A per-client/per-attempt seeded draw can make policy comparisons reproducible without changing the random sequence merely because one policy schedules a different number of events.

Measure total attempts, retries, completed operations, budget stops, deadline stops and request concentration over explicit time buckets. Label latency quantiles computed only among successful operations; otherwise a policy that abandons slow cases can appear misleadingly fast.

Keep the model's omissions visible: request duration, queues, network loss, correlated failures, side effects and capacity changes can materially alter the result. Do not conclude one jitter choice is universally best from one seed or scenario.

### 6. Verify stopping and cleanup

Test success on the first attempt, recovery after transient failure, an exhausted attempt budget, a provider hint beyond the deadline, cancellation during sleep, cancellation during an in-flight request, and terminal failures that must not be retried.

For an implementation, verify that completed or canceled work leaves no future retry timer active. A stale response or error from an earlier generation must not restart or stop a newer request. Keep the smallest failing sequence as a regression before making an authorized fix.

Live testing requires its own permitted scope. A local simulation or unit-test success is not permission to send load to a service or to repeat a financial, messaging or other consequential operation.

## Worked example

Three synthetic read clients start at time 0. A model service accepts one success in each one-second window, with no outage. The policy permits three total attempts, waits one second between failures and has an exclusive four-second deadline.

Client 1 succeeds at 0. Client 2 succeeds at 1 after one retry. Client 3 succeeds at 2 after two retries. Six requests produce three completed operations; successful completion times are 0, 1 and 2 seconds.

With an exclusive two-second deadline, Client 3's planned attempt at 2 must not start. The result becomes five requests, two completions and one deadline stop. Calling that outcome three successful clients because a future retry was planned would be incorrect.

## Executed checks and limits

A discrete-event implementation matched the small examples and 450 seeded policy/scenario combinations. Checks enforced total-attempt bounds, exclusive deadlines, capacity conservation, nonnegative jitter ranges, provider-minimum waits and deterministic replay. Simulated-interface tests covered per-client traces, complete event export and invalidation after parameter edits.

An exported pressure chart was rendered and inspected separately. The simulator used instantaneous synthetic responses and did not execute real HTTP calls, parse live Retry-After headers, exercise real cancellation timers or verify mutation idempotency. Those remain separate checks before applying a policy to a live integration.
