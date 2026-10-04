---
name: typescript-best-practices
description: "Model TypeScript domains and trust boundaries with validated constructors, discriminated unions, precise types, and real compiler and behavioral checks."
---


# TypeScript best practices

Use the project's compiler settings, libraries, and conventions. Portable frontmatter does not enable path-based activation; apply this workflow when the actual task concerns TypeScript design, review, or edits. These guidelines improve contracts, not merely the appearance of types.

## Model the real domain

- Use discriminated unions for genuine variants instead of mutually dependent optional fields
- Brand primitives when mixing two same-shaped values creates a real risk. Validate at the constructor and follow an existing branding convention where one exists
- Construct stronger shapes only when they make operations total. A non-empty tuple supports the first element, but an arbitrary numeric index may still be out of bounds. A length check does not reject sparse arrays; check head presence, and use a frozen snapshot when mutable aliases could invalidate the guard
- Keep ordinary arrays when empty input has a valid result. Returning `T | undefined` can be more honest than forcing a non-empty input
- Numeric fields alone do not exclude negative, non-finite, or overflowing values. Validate duration, timestamp, range, and unit constraints explicitly
- Encode ownership and mutability deliberately. `readonly` protects at compile time; it is not deep runtime immutability or a security boundary

## Parse at the trust boundary

External JSON, files, network messages, environment settings, and unchecked library results enter as `unknown`. Reuse the repository's schema system and infer types where supported. Do not add a dependency for one trivial guard or maintain a duplicate schema, interface, and predicate.

When validating manually, check every required field and return a constructed domain object. A type predicate must actually prove its claim. State the policy for unknown fields, versions, malformed data, and compatibility; ignoring all unknown fields is not universally safe. Do not repeatedly reparse trusted internal domain objects unless they cross a new trust boundary.

Avoid unchecked assertions and non-null assertions that hide a missing contract. A justified assertion in a small validated constructor or interoperability boundary can be correct; `as const` has a different role from claiming arbitrary input is a user. `satisfies` checks assignability without converting a value, but does not validate runtime data. Preserve warranted compiler expectation directives in negative type tests.

## Keep APIs and diagnostics useful

Prefer compiler narrowing through discriminants, `in`, `typeof`, and `instanceof` before hand-written guards and assertions. Use exhaustive checks for closed unions. Derive transport-facing types from actual schemas where appropriate; create a domain model when it owns a different invariant rather than blindly leaking generated types.

Use object parameters when they prevent positional mistakes or improve readable call sites. One or two obvious arguments need no mandatory object wrapper. Do not claim allocation cost matters without a relevant measurement.

Use the project's structured logger for operational diagnostics and keep secrets out of messages. Standard output is a legitimate interface for a CLI; do not prohibit it globally.

## Prove the contracts

Read [patterns](references/patterns.md) for examples and caveats. [examples.ts](references/examples.ts) is a self-contained positive example, and [type-checks.ts](references/type-checks.ts) asserts invalid uses with expected compiler errors. Compile with the real compiler and strict settings; text matching is not type validation.

Run behavioral tests against the real parsers and domain functions as well. Cover malformed external data, finite/nonnegative numeric limits, empty collections, and variant behavior. A brand compiles away, so type tests alone cannot prove parsing. A passing runtime test cannot prove callers are rejected by the type checker. State missing checks separately.
