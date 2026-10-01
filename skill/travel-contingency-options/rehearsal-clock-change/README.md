# Repeated-hour travel rehearsal

This recorded fresh-input rehearsal uses invented schedules and prices across the
2026-11-01 clock change in America/New_York and America/Chicago. It tests a specific
failure mode: a later displayed arrival clock can represent an earlier instant.

- [Input packet](input.md): the fictional request, constraints and three candidates
- [Recorded result](output.md): recommendation, complete costs and conditional branches
- [Local verifier](verify.py): reads the packet and independently recomputes its arithmetic

To repeat the comparison, use the [workflow](../SKILL.md) with the input packet,
then compare the result with the recorded output. Do not supply the output as an
input or use real providers for this exercise.

## Run the local check

From the repository root:

```sh
python3 skill/travel-contingency-options/rehearsal-clock-change/verify.py
```

Requires Python 3.9 or newer and local IANA timezone data for the two named zones.
The verifier uses only the Python standard library, reads the adjacent input
packet and makes no network requests or file changes. It runs from any working
directory. Missing timezone data is a failed prerequisite, not a passed check.

## Observed checks

The packaged fixture passed 25 checks on 2026-10-01 using Python 3.12.14 and
system IANA timezone data 2026b. Supplied offsets were validated against the named
zones on the travel date; all elapsed arithmetic used UTC instants.

- A: departure 04:10 UTC; terminal 06:30 UTC; 75 elapsed minutes to venue
  07:45 UTC = 01:45 −06:00; 30 minutes of slack; USD 485 total and USD 15 headroom
- B: departure 04:40 UTC; terminal 07:10 UTC; venue 08:00 UTC = 02:00 −06:00;
  15 minutes of slack; USD 425 total and USD 75 headroom
- A reaches the terminal 40 real minutes earlier despite its later displayed
  clock, and the venue 15 minutes earlier
- C remains unselected: possible terminal arrivals 06:10/07:10 UTC and venue
  arrivals 07:15/08:15 UTC; USD 360 known cost plus an unknown bag charge
- The unconfirmed USD 150 refund is not deducted from payable-now totals or
  added to spending headroom

## Evidence limits

This is one recorded fictional comparison plus a deterministic fixture check.
The recorded result was reviewed against those calculations. The verifier
recomputes the input's arithmetic; it does not grade free-form responses or prove
the workflow handles every travel disruption. Availability, prices, provider
rules, booking cutoffs, real-world transfer times, eligibility and transactions
were not tested. There are no real offers, booking links or provider observations.
