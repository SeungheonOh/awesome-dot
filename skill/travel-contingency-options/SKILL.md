---
name: travel-contingency-options
description: "Turn an authorized disrupted itinerary into a current, costed shortlist of feasible replacement routes, with local-date checks, booking details and explicit decision gates."
---

# Find a Workable Travel Contingency

Resolve a concrete disruption: a canceled leg, a missed connection, an unusable arrival time or a route the traveler can no longer take. Produce the best feasible next choice and enough verified detail to book it. Searching is useful work even when buying is not yet authorized.

## Establish the trip boundary

Read the supplied itinerary or the relevant authorized booking thread. Retrieve only the matching journey, not the traveler's entire account history. Record:

- Traveler count, starting location and earliest possible departure, including the local date and timezone
- Existing legs, dates, airports/stations, ticket relationships and confirmed disruption status
- The real arrival requirement: destination address or station, local deadline and required arrival buffer
- Hard limits: budget and currency, acceptable modes, baggage, accessibility needs, permitted nearby terminals and overnight stays
- The requested action: compare, prepare a booking, change an existing booking or buy a replacement

Separate hard constraints from preferences. If a constraint is missing, research independently useful options and ask only for the missing choice that changes feasibility. Do not infer a traveler's eligibility to transit a country. Ask for the minimum relevant eligibility information if needed; do not request passport numbers or medical explanations for ordinary route comparison.

## Workflow

### 1. Preserve the existing booking's value

Check the original provider's current disruption and change options in the authorized booking or official service. An included reroute can be preferable to a new ticket. Record what was actually offered, whether linked onward/return legs may be affected, the reply deadline and which actions would consume or cancel the original booking.

Treat a public policy as a rule to check against this fare and incident, not proof of a refund or entitlement. Keep confirmed paid amounts, confirmed reusable credit and possible refunds separate. Do not count an unconfirmed refund toward today's spending limit. Do not cancel a usable leg or accept a voucher merely to inspect alternatives.

### 2. Retrieve candidate routes with evidence

Search available connected travel tools or the cloud browser, favoring the provider's current availability and fare details. Tell the user which browser is in use if browser work is needed. Use the existing account only when authorized; do not create an account or new persistent access to search.

Start with the original provider's recovery options, then the smallest useful set of alternatives allowed by the traveler: other departures, nearby terminals, rail or an overnight stay. Search summaries and static schedules can identify candidates but do not establish seats, sellable fares or operating status.

For each candidate record source link, provider, retrieval timestamp with timezone, travel dates, leg identifiers, local departure/arrival with timezone, ticket structure and evidence status. Use distinctions such as:

- **Provider offer observed:** availability and price seen for the correct travelers and dates at a recorded time; still subject to repricing
- **Schedule only:** a service is listed but availability and fare remain unverified
- **Assumption:** a planning estimate, with its basis and the check needed
- **Unavailable or stale:** the source failed, the offer expired or the evidence predates a material change

Record fare family, included baggage, cancellation/change restrictions and any offer-expiry text actually shown. Open relevant official rules for baggage, connection eligibility, airport transfers and entry/transit requirements during real use. Preserve source date and applicability. Do not invent a policy, URL, confirmation code, availability claim or an expiry when the source provides none.

### 3. Calculate whole-journey feasibility

Normalize each local timestamp to an instant using the location's IANA timezone and the offset applicable on that travel date. Retain both representations. Do not subtract wall-clock times across zones. Resolve ambiguous daylight-saving times or missing dates with the provider; a negative apparent duration is a check failure, not a plausible shortcut.

Evaluate the entire route:

1. Can the traveler reach the departure terminal before the applicable check-in, bag-drop and boarding cutoffs? Include ground travel and the user's preparation constraints.
2. For each transfer, compare actual elapsed connection time with the applicable published minimum and practical requirements. Identify terminal changes, border control, bag collection/recheck and separate-ticket exposure. A single ticket or a nominal minimum alone does not guarantee a comfortable connection.
3. If no applicable minimum or ground-transfer time is verified, mark the route conditional. Do not manufacture a universal safe connection threshold. A connection below a known applicable minimum fails even if the advertised final arrival looks attractive.
4. Add arrival processing and the final ground journey. Show airport/station arrival separately from arrival at the actual required destination. Calculate deadline slack and explain any user-selected buffer.
5. Check overnight dates, service calendars, check-in/check-out dates and local midnight changes for any lodging or ground service. Recheck entry/transit eligibility if the new route changes it.

Exclude failed hard constraints from the recommendation. Keep conditional routes available as fallbacks, with the exact missing evidence that prevents calling them feasible.

### 4. Compare the full incremental cost

For each route show fare/change charge, required baggage, mandatory taxes/fees, necessary ground travel, lodging and any other required charges. State per-traveler versus party totals and currency. Do not hide a required component in an optional-add-ons column.

Distinguish the amount payable now from the estimated eventual net cost after confirmed credits/refunds. Existing sunk costs belong in context, not twice in replacement totals. For mixed currencies, retain original amounts and show a dated exchange-rate estimate; the payment total and card conversion may differ. If a required component has no reliable price, show a partial total or range and mark budget compliance unresolved.

Rank eligible options by the user's hard constraints, then meaningful tradeoffs: arrival slack, transfer risk, total cost, overnight disruption and recoverability. Do not label the cheapest displayed fare the cheapest journey before required components are known.

### 5. Give the decision and booking-ready handoff

Lead with a recommendation, why it meets the constraints and the single next decision or verification needed. Include a compact comparison and, for the preferred option:

- Correct party size, date, origin/destination terminals and exact services
- Local times and timezones, elapsed journey time and destination-arrival calculation
- Ticket structure, baggage, applicable fare restrictions and checked eligibility
- Provider and a verified booking/source link, quoted total and currency, retrieval time and known expiry
- Required unresolved checks, and a fallback if availability disappears

A route with unverified seats, incomplete costs or unresolved transit eligibility is a candidate to check, not a booking-ready offer. Deliver the useful comparison anyway and state the blocker precisely. Keep booking references and other private trip identifiers out of public artifacts.

### 6. Execute only the authorized decision, then verify

A compare request ends with the recommendation. If the user also authorized a purchase or change, continue within that authorization after confirming the exact current offer. Obtain any still-required approval with provider, itinerary, total/currency, payment type, one-time or recurring commitment, service destination and visible cancellation/refund restrictions. Disclose new explicit legal acceptance terms and complete CAPTCHAs only with the required permission. Do not ask for card credentials in chat or transmit highly sensitive credentials yourself.

Reprice immediately before committing. A changed route, higher total than approved, unrequested paid add-on or materially different fare terms requires a new decision. Do not make a nonrefundable replacement dependent on an unconfirmed refund. Preserve the original booking until a safe change sequence is established; if simultaneous holding is impossible, explain the risk and obtain the user's choice before cancellation.

After an authorized transaction, read the provider's confirmation and verify each traveler/leg, dates, paid amount, ticketing status and treatment of the original itinerary. An order submission or payment authorization is not proof that a ticket was issued. On timeout, inspect order status before retrying to avoid a duplicate charge. Report the actual terminal state or the unresolved provider status, with the official next step. Do not book further alternatives automatically.

## Final checks

- Every recommended route passes the hard constraints on sourced evidence or explicitly remains conditional
- Times use date-specific offsets, connections use elapsed instants and arrival includes the final ground journey
- Required costs reconcile; possible refunds do not masquerade as available money
- Rules and availability have source dates, and stale evidence is not reported as current
- The completed output distinguishes research, approval and confirmed transactions

The [fictional worked example](example.md) demonstrates overnight arithmetic, a failed connection, a fragile ground transfer and unknown seat availability. Use it to check the method, never as live travel evidence.

The [repeated-hour rehearsal](rehearsal-clock-change/README.md) adds a fresh fictional [input packet](rehearsal-clock-change/input.md), a [recorded comparison](rehearsal-clock-change/output.md) and an offline [arithmetic verifier](rehearsal-clock-change/verify.py). Use it to check date-specific offsets, elapsed durations across the clock change, unresolved arrival occurrences and full payable-now costs.

## Date arithmetic guardrail

Treat provider-local departure and arrival times as clock values that must map to a real, unambiguous instant. A timezone label alone does not validate a repeated or skipped hour; obtain the intended offset where needed. Calculate flight, processing, connection and ground-transfer durations on the UTC timeline, then convert the resulting instant for display. Adding an elapsed duration directly to local wall-clock time can be wrong across a daylight-saving change.

## Example request

```text
dot, use the authorized itinerary for my canceled journey and find alternatives that reach the destination before [LOCAL DATE, TIME AND TIMEZONE]. Keep the replacement within [TOTAL BUDGET AND CURRENCY], include my required baggage and final ground transfer, and compare the original provider's recovery offer with other feasible routes. Show current sources and a booking-ready preferred option if one is available. Ask before any purchase or cancellation.
```

## Evidence status

This is an executable research-and-decision workflow with a worked example and one recorded fresh-input fictional rehearsal. The rehearsal's local verifier passed 25 fixture checks for IANA offset mappings, UTC elapsed durations, costs and unresolved branches; it does not validate free-form responses or certify the workflow broadly. Real availability, rules, prices, eligibility and transaction completion remain untested here and must be checked in the tools and services available during the actual task.
