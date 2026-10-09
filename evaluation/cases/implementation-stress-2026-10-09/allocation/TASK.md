> Public contract projection. Behavior and mathematical requirements are unchanged. Delivery/evaluation process instructions, where present, are omitted. See provenance.json for source hashes and changes. This package is UNRUN.

# Exact capped allocation for a shared-services ledger

Implement `allocate(total, groups)` in `solution.py`, using Python 3.12 standard library only. This is an implementation task: submit executable source, not a precomputed answer. The function is pure and must not mutate inputs. No network, filesystem, subprocess, or external-service work is requested.

A service ledger allocates a whole number of usage credits while preserving guaranteed floors and hard caps. Each group is a dict with unique ASCII `id`, integer `priority`, nonnegative integer `floor`, integer `cap >= floor`, and rational `weight: [numerator, denominator]` (numerator >= 0, denominator > 0). Smaller `(priority, id)` wins an exact tie. IDs use ASCII letters, digits, hyphen, and underscore. Input order is significant only for output rows, never for allocation ties. Fractions need not be reduced.

## Exact allocation rule

1. Give every group its floor. Write `R = total - sum(floor)` and `capacity_i = cap_i - floor_i`. If total is outside `[sum(floor), sum(cap)]`, raise `ValueError`. Empty groups are allowed, and only total 0 is feasible.
2. Allocate residual credits continuously among groups of strictly positive weight first. Let `P = min(R, sum(capacity for positive-weight groups))`. If P equals this capacity sum, their residual ideal is their capacity. Otherwise use the unique water level `lambda >= 0` such that `sum(min(capacity_i, lambda * weight_i)) = P`, and give each positive-weight group that exact residual ideal. Zero-capacity groups remain zero.
3. If credits remain after all positive-weight capacity is filled, allocate those credits among zero-weight groups with capacity using exactly the same capped water-fill rule but an effective weight of 1 for each. If no credits remain, their residual ideals are zero. Thus zero-weight groups still get floors and can absorb leftover credits only after positive-weight capacity is exhausted. There is no alternative infeasibility rule for zero weights.
4. Each group's full exact quota is its floor plus its residual ideal. Take all quota floors. Let K be total minus their sum. Give one additional credit to each of the K groups with the largest strictly positive fractional quota remainder, in descending exact remainder order, then ascending `(priority, id)`. A group gets at most one remainder credit. A quota at its integer cap cannot get one. This rounding is done once on the final water-filled quotas, not after each saturation round.

Return exactly this structure (dict key order is immaterial):

`{"rows": [{"id": str, "units": int, "quota": [int, int]}, ...], "remainder_awards": [str, ...]}`

Rows are in original input order. Quotas are exact reduced fractions with positive denominator (zero is `[0,1]`). `remainder_awards` is the award order from step 4, including its tie order. Integers and exact rational arithmetic are required semantically; any implementation yielding the exact result is valid. Do not use display rounding to decide allocations.

Example: total 8 and groups `[{"id":"a","priority":0,"floor":1,"cap":3,"weight":[5,1]}, {"id":"b","priority":1,"floor":0,"cap":9,"weight":[1,1]}, {"id":"c","priority":2,"floor":1,"cap":9,"weight":[1,1]}]` produce rows a = 3 with quota 3/1, b = 2 with quota 2/1, c = 3 with quota 3/1, and no remainder awards.

Another example: total 2, three groups with floor 0, cap 9, weights 1/1, and IDs b,a,c with priorities 0,0,1 in that input order produce units 1,1,0, each quota 2/3, and awards `["a","b"]`.

## Finite tested domain and checks

There are at most 256 groups, floor/cap/total are integers of magnitude at most 10^30 (nonnegative except deliberately infeasible totals may be -1), weight numerators are at most 10^24 and denominators at most 10^9, priorities are in [-1000,1000], and IDs have at most 40 ASCII characters. All input fields and types obey this contract; infeasible totals are the only deliberately invalid inputs. Python bool values are not supplied as integers. No requirement outside this domain is graded.

Tests compose these disclosed classes: ordinary uncapped ratios; rational rather than integer weights; multiple cap saturation rounds; floors and already-saturated groups; exact ties under reordered inputs; integers beyond float precision; positive/zero-weight phase transitions; empty/all-zero/single-group cases; totals at and outside feasibility boundaries; and large totals where work proportional to the number of credits is impractical. The largest tested input fits the stated limits. A call must finish within 5 seconds and the frozen suite within 120 seconds on an ordinary Python worker with 512 MiB available memory; these generous limits are only to exclude nonterminating or per-credit algorithms. Report an unavailable execution as unassessed, not a correctness failure.

This is a specified synthetic accounting algorithm, not an election rule or financial recommendation. If supplied, the compare-integer-apportionment guide supports exact quotas and tie reasoning; capped water-fill and zero-weight fallback are additional rules fully defined here. The guide does not supply their implementation.
