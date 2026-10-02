---
name: check-dimensional-calculations
description: "Review a bounded calculation with explicit units, carry base dimensions through each operation, reject incompatible sums and conversions, and return a reproducible result with numerical and physical assumptions."
---

# Check a calculation with dimensions

## When to use

Use this when converting measurements, reviewing a formula, checking a spreadsheet's quantity logic or implementing a small calculation interface. The outcome is a calculation whose operations and requested output unit agree dimensionally, with the physical assumptions still visible.

Dimensional agreement is necessary for many formulas but is not a proof of their physical meaning. Torque and energy share dimensions. A length ratio can describe many different quantities. Review the quantity's meaning separately.

## Required inputs

- The formula, intermediate steps and values, each with an explicit unit where applicable
- The intended quantity and target unit
- Unit definitions and conventions, especially ambiguous names
- Numerical precision and uncertainty requirements
- A bounded supported domain, such as length, mass and time

If a unit is missing or ambiguous, identify exactly which value needs clarification. Do not guess whether lb means mass or force, whether a gallon is US or imperial, or whether a temperature is an absolute reading or an interval. A small tool may reject unsupported quantities; a broader review should use a library and unit definitions suited to the task.

## Workflow

### 1. Establish definitions before arithmetic

Record the accepted unit symbols, case rules, scale factors and base dimensions. Distinguish exact defining factors from rounded measurements. For example, the international inch is 0.0254 m; a measured length still has measurement uncertainty.

Use an authoritative unit reference. For SI derived units and selected non-SI conversions, start with [NIST's SI derived-unit tables](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes) and [conversion factors](https://www.nist.gov/pml/special-publication-811/nist-guide-si-appendix-b-conversion-factors/nist-guide-si-appendix-b8). Define a day explicitly if treating it as exactly 86,400 seconds rather than a civil-calendar interval.

Do not handle offset units by multiplying a scale alone. Celsius readings require an offset when converted to kelvin; temperature differences are a separate case. Reject them if that distinction is outside the chosen implementation.

### 2. Parse structure without running input as code

For user-entered formulas, use a bounded parser or a suitable library, not eval. Specify supported operators and precedence. Require explicit multiplication if implicit multiplication would create ambiguity. Decide how powers, unary minus, functions and variable names behave.

Limit input length, tokens, nesting and exponent range. Resolve variables only from authorized earlier definitions or supplied values. Reject unknown names and accidental overwrites. Preserve the original expression for review and show the exact line that failed.

### 3. Carry value and dimensions together

Represent each quantity as a base-unit magnitude plus a dimension vector. For length, mass and time, the vector for speed is [1, 0, -1]; the vector for energy is [2, 1, -2].

- Addition/subtraction require identical vectors; combine magnitudes only after normalization
- Multiplication adds vectors and multiplies magnitudes
- Division subtracts vectors and divides magnitudes; reject zero divisors
- An integer power multiplies every vector component by that exponent

Zero is not automatically dimensionless. Zero metres can be added to metres, but a bare zero needs an explicit policy before being used to bridge incompatible quantities. Retain dimensions through cancellation.

### 4. Check numerical behavior separately

Reject non-finite values and unsupported numerical ranges. Consider underflow as well as overflow: a tiny nonzero intermediate silently becoming zero can change the conclusion. For cancellation and very different magnitudes, binary floating point can lose meaningful information even when the result is finite.

Choose decimal, rational or higher-precision arithmetic when the task requires it. Do not present extra displayed digits as measurement accuracy. Keep unrounded computed values in a reproducibility record when permitted; state the display precision and the actual arithmetic model.

### 5. Validate the target and physical interpretation

Normalize the target unit independently and require its dimension vector to match the final quantity. Divide by its scale only after that check. Do not coerce an incompatible result simply because the requested unit looks plausible.

Then review the formula's meaning: does the speed use total elapsed time, does runtime assume constant power, does a density apply to the material and conditions in question? Clearly label simplifying assumptions. A unit check cannot certify a medical dosage, structural design or safety-critical decision.

### 6. Produce a reviewable result

Return the original inputs, definitions, intermediate quantities in base units, final target conversion, assumptions and verification limits. Preserve any uncertainty provided by the user rather than dropping it. Export only the supplied scope; a calculation result is not permission to update a live system.

In an interface, edits to either the formula or target must invalidate old results and downloads. Render expressions as text. Test recovery from an invalid target and from a dimensional error, not just successful conversions.

## Worked example

A trip covers 180 km in 2 h plus 30 min. The desired result is average speed in km/h.

1. Normalize distance: 180,000 m
2. Normalize time: 7,200 s + 1,800 s = 9,000 s
3. Divide: 20 m/s, with vector [1, 0, -1]
4. Normalize km/h: 1,000/3,600 m/s, with the same vector
5. Convert: 20 ÷ (1,000/3,600) = 72 km/h

The result assumes the time is the total elapsed trip time. It is not an instantaneous speed. Changing the target to kg must fail. Adding the distance directly to the elapsed time must also fail, before any export is offered.

## Verification examples

The small JavaScript implementation used during this workflow was tested on Node 24.19 with 500 generated scaled length/mass/time expressions checked against independently calculated magnitude/vector expectations. Reference cases covered inch-to-centimetre, pound-mass-to-gram, watt-hour-to-joule, litre-to-cubic-centimetre and pascal base dimensions.

Additional tests covered incompatible sums, target mismatches, division by zero, malformed syntax, deep nesting, overflow/underflow and variable-name collisions. Simulated-interface checks covered stale-result clearing, exact JSON export and recovery after an error. These tests establish bounded software behavior; they do not establish uncertainty propagation, real-browser accessibility or physical correctness of arbitrary formulas.
