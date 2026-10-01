---
name: errand-window-plan
description: "Order user-selected errands around opening hours, appointment windows and arrival or completion cutoffs using authorized directional travel data. Produce a feasible stop-by-stop plan with waiting, buffers, finish times and unresolved stops; do not book, buy or start navigation."
---

# Fit errands into their actual windows

Turn a bounded set of selected stops into a plan the user can inspect before leaving. A shorter journey can still miss a counter cutoff; a place being open does not establish that the requested service is available. Keep those constraints visible.

This workflow orders travel and service visits. It does not discover new errands, manage a calendar, pack for a trip, move appointments, place orders or make reservations.

## Establish the planning inputs

Use the request and relevant authorized sources. Ask for a missing choice only when it changes feasibility or the choice of plan.

- **Trip:** date, date-specific time zone, start point, earliest departure, end point, latest required return/arrival and travel mode. A different end point is not implicitly a return home
- **Stops:** stable neutral label, required or optional, user-selected optional priority, service needed and any ordering dependency
- **Service time:** duration supplied by the user or applicable source, including its uncertainty; distinguish service from queuing, check-in, parking and walking. Do not invent a duration to make a stop fit
- **Access:** applicable branch and service, dated opening intervals, breaks, closure exceptions, appointment evidence and capacity/eligibility conditions relevant to this visit
- **Cutoffs:** exact time and whether it governs physical arrival, check-in, service start or service completion. Record inclusivity and any mandatory early-arrival allowance
- **Travel:** directional leg durations for the actual mode and intended departure period, source, retrieval/supplied timestamp and any range or confidence limit. Record exactly which portions are covered
- **Buffers and waiting:** user-supplied or explicitly accepted allowances; where waiting is allowed, how long, and whether before opening is permitted. Distinguish a waiting allowance from permission to enter closed premises
- **Preferences:** for example preserve every required stop, then include the preferred optional stop, then finish earlier. Obtain a choice before relaxing hard constraints

Use neutral point labels in reusable outputs. Do not include access codes, unnecessary home details or sensitive reasons for a visit.

## 1. Make the evidence usable

For real tasks, check current official opening/service hours and date-specific exceptions when needed. Match the exact location and requested service. Use appointment confirmations for appointment-specific restrictions, without assuming they override every closure or check-in rule. Record the source link/reference, effective date, source issue/update time if known, retrieval time, and relevant time zone. A page without an update date has an unknown update date, not today's date.

Read authorized routing data for the intended travel mode and time. A map result for driving is not a walking estimate, and A→B need not equal B→A. Transit may require departures, transfers and last-service constraints rather than a constant duration. Recheck affected legs when a changed order shifts them outside their evidence's valid departure period.

Do not send private start/end points, sensitive visit details or a detailed personal itinerary to a new routing or other service without authority covering that disclosure. Use already-authorized information or ask for the narrowly missing permission. Continue checking the nonsensitive constraints while routing is blocked.

Keep an evidence register and classify each relevant fact as confirmed for the visit, supplied but unverified, stale, conflicting or unknown. Current traffic, queues and service availability can change even after a check. Do not present a supplied fictional matrix as a live route result.

Handle gaps explicitly:

- **Closed:** exclude an optional stop and explain why. If a required stop is closed, report that no complete plan fits the stated day; preserve useful partial options without calling them complete
- **Unknown/conflicting hours or cutoff meaning:** keep that stop unresolved. Do not infer hours from similar branches, previous weeks or a generic business listing
- **Missing service duration or travel leg:** leave the dependent plan conditional. Missing is not zero; never substitute the reverse leg silently
- **Service inside opening hours is uncertain:** distinguish an opening-hours fit from evidence that a counter, pickup or appointment will accept the visit

## 2. Normalize time constraints

Convert each dated local timestamp to an unambiguous instant before comparing it. Preserve local displays and offsets. Ask about a genuinely ambiguous daylight-saving time; do not silently choose an occurrence. Retain separate intervals for split opening hours, overnight hours and each applicable service window.

Write the actual tests, not one generic “deadline” column:

```text
arrival <= arrival cutoff
check-in complete <= check-in cutoff              # if separately specified
service_start within an allowed start interval
service_finish <= completion cutoff              # only when that rule applies
end_arrival <= user's end-point deadline
```

An arrival cutoff does not become a completion cutoff, nor does a start deadline grant permission to remain after closing. Apply all independently stated conditions. Where a service must finish within one opening interval, do not run it through a closed lunch break. If appointment rules are unclear, ask rather than infer that late arrival is accepted.

Check-in effort that consumes time needs its own supplied duration or an explicit source requirement; arriving five minutes early does not prove that check-in takes five minutes. For an exact appointment, represent the required start as a fixed instant, with its separately stated arrival/check-in constraints.

## 3. Test orders with their actual waiting

First retain every required stop. Test selected optional-stop subsets separately; do not quietly delete a required stop or downgrade it to optional. For a small supplied set, enumerate orders and reject ones violating dependencies or hard constraints. For a larger set, inspect promising orders but state the search limit; a heuristic is not proof that no solution exists.

For each proposed order, propagate from the known start point and departure:

```text
arrival = previous_departure + supported_leg_time + leg_buffer
service_start = next admissible start at or after arrival
waiting = service_start - arrival
service_finish = service_start + supplied_service_duration
departure = service_finish + separate post-service allowance, if any
```

For fixed appointments, the admissible start is the appointment time and arrival must satisfy its own rule. Add separately timed check-in before testing that start. For ordinary visits, check the entire service interval against the applicable rules. Apply each allowance once: do not add parking again if the leg already includes it, and do not call unused buffer observed waiting.

If early arrival needs waiting, verify that the proposed location and duration are permitted. If waiting there is disallowed, a later departure or wait at an already-permitted earlier point may make the order feasible. Recompute the entire affected suffix and recheck earlier cutoffs. Otherwise reject that timing; do not pretend that waiting inside a closed venue is allowed. With time-dependent routes, later departure can change travel time, so a fixed-duration earliest-start calculation is insufficient.

Continue from the final stop to the actual end point and test the user's deadline. A plan ending at the last shop is incomplete if the user needs to reach another place afterward.

For each feasible candidate, show waiting and slack against every relevant hard cutoff. Slack means remaining room under the stated inputs, not a promised lateness tolerance. Where travel/service times have supported ranges, evaluate plausible combinations or a clearly identified upper-bound case; do not label an arbitrary extra allowance statistically reliable. Identify the first constraint to fail in a sensitivity check. Avoid precise probability claims unsupported by data.

## 4. Choose and explain the useful plan

Apply the user's priorities only after hard constraints pass. Show an optional stop's effect on finish time, waiting and the tightest cutoff. If an optional stop makes a required visit fail, present a required-only plan and the optional stop as omitted or unresolved, with a reason. If no complete plan can be verified, say whether the obstacle is a demonstrated conflict or missing evidence.

Explain one useful rejected order using the failed event and amount, rather than vaguely calling it inefficient. Claim “best among the checked orders under this matrix and selection rule” only when that comparison was actually performed. Do not claim a globally optimal real-world route from an incomplete, estimated or time-insensitive matrix.

If inputs change, preserve source records and user constraints; recompute the changed leg/window and all downstream events. Do not change a reservation or extend the user's deadline merely because that creates a feasible calculation.

## Output and verification

Deliver a compact plan with:

1. Status: feasible under stated inputs, conditional on named gaps, or no complete feasible plan established
2. Trip date/time zone, start/end points, departure and end deadline
3. Ordered stops with required/optional status, travel plus distinct buffer, arrival, waiting, service start/finish and applicable cutoff/slack
4. End-point arrival, included/omitted optional stops, one important tradeoff and a rejected order when useful
5. Unresolved or closed stops with the missing evidence/decision, source references/timestamps, and material uncertainty
6. Actual action status: source records unchanged; no navigation started, purchases made, appointments changed or bookings submitted by this planning workflow

Before handing it over, independently recompute the selected order and check every leg, service interval, cutoff, wait permission and final return. Check that a completion test wasn't substituted for an arrival test; optional stops were not treated as required; and unknown values didn't become zero. Refresh time-sensitive facts when a real plan is being used after its evidence has gone stale. Give no guaranteed arrival or acceptance claim.

If the user separately requests navigation, buying, booking, sharing or a calendar change, treat that as a distinct action subject to its own authority and verification. The proposed route itself performs none of them.

## Worked check

[example.md](example.md) contains a completely fictional three-stop request, a complete directional matrix, the resulting plan and an explained rejection. Run the standard-library [checker](check_example.py) from the repository root:

```bash
python3 skill/errand-window-plan/check_example.py
```

The checker tests fixed-departure, constant-duration fixture orders. It is a small demonstration, not a live route optimizer or a general appointment scheduler.
