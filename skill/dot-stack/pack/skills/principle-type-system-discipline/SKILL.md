---
name: principle-type-system-discipline
description: "Use practical domain types, boundary parsing, exhaustive variants, and authoritative schemas to eliminate demonstrated invalid states in typed code."
---

# Type-system discipline

Use this when designing state representations or function signatures, or when an assertion, primitive mix-up, or missed variant reveals a weak contract. Static types can prove properties of modeled code; they do not validate external bytes or eliminate all runtime failures.

## Make the useful invariant structural

- Represent mutually exclusive states as variants with their required payloads. Replace `completed: boolean` plus optional completion time with open or done-with-time, or derive completion from one authoritative field when that expresses the domain correctly.
- Prefer construction that avoids an invalid combination. A nonempty sequence can be a head plus a remainder. A range can be a start plus a nonnegative duration, but duration validation and arithmetic overflow still need treatment. Changing representation relocates proof obligations; it does not make them vanish.
- Distinguish semantic primitives when interchange is a realistic defect: customer and order identifiers, meters and seconds, validated and raw paths. Use the language's newtype, opaque wrapper, value class, or branded type idiom. Keep construction and conversion at explicit boundaries rather than scattering casts.
- Parse untrusted JSON, command input, configuration, environment values, messages, and restored data into domain types. Generated declarations alone do not establish runtime validity, freshness, or authorization.
- Match variants exhaustively using the language's checked idiom. Avoid a catch-all that silently gives a new variant old behavior. Verify that adding a temporary variant causes the intended compile-time failure.
- Derive types from the authoritative schema when one genuinely owns the contract. Preserve intentional differences between transport, persistence, and domain representations through explicit mapping; do not collapse them just because code generation is possible.

## Keep the proof honest and proportionate

Narrow through checks or better construction before using an unsafe assertion. Sometimes a compiler cannot express a fact proven by an external library or runtime invariant. Isolate that assertion at a narrow boundary, document the proof and limitations, and test it. Never cast solely to silence an unexplained error, propagate `any` through the core, or treat a brand as a security boundary.

Strengthen where an operation is partial or confusion creates real risk. `sum` can sensibly accept an empty sequence; `head` needs a nonempty sequence or an explicit optional result. Do not force a nonempty type through the entire application for precision that no consumer needs. Some invariants require database constraints or runtime checks and cannot be delegated to the compiler.

## Example and counterexample

Applies: two string identifiers are repeatedly confused at a lookup boundary. Introduce separately constructed identifier types, reject a swapped argument in a compile-time test, and verify valid parsing and lookup at runtime.

Does not apply: add layers of generic type machinery to a clear total formatter that cannot exhibit the proposed invalid state. The maintenance cost exceeds the proof gained.

## Verification

Run the project's real type checker with its relevant options, compile-time positive and negative examples, and runtime boundary tests. Show which invalid construction or missing case is now rejected, and which properties remain runtime obligations. If no compiler is available, report the type design as reviewed but unverified, with the exact intended check.
