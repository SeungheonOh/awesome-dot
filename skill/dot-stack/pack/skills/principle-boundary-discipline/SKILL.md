---
name: principle-boundary-discipline
description: "Place parsing, validation, and error translation at actual trust boundaries while keeping domain logic independent of transport and framework details."
---

# Boundary discipline

Use this while shaping adapters, configuration loading, persistence access, validation, or error handling. Establish where a value becomes trustworthy and what can invalidate that trust.

## Establish the contract

- List actual boundaries: command arguments, files, network responses, database rows, plugins, messages, and mutable state restored after restart. “Inside the repository” is not a trust guarantee.
- Parse raw values into domain values at the entry boundary. Validate shape and relevant semantic constraints, including cross-field relationships. Return a useful failure without exposing secrets or fabricating defaults that hide corrupt input.
- Pass those domain values into a small core. Keep transport decoding, framework objects, storage records, and presentation-specific error formatting in adapters. A pure calculation should be testable without booting a server.
- Handle a failure where the caller can decide what to do: translate a domain error into an HTTP response or CLI exit at the outer edge; propagate information through intermediate code rather than logging and swallowing it repeatedly.
- Remove repeated checks only after establishing the invariant and its lifetime. Mutation, deserialization, unsafe foreign code, concurrent writes, and mixed-version data can introduce new boundaries. Authorization and freshness checks often belong at use time, not only at initial parsing.

Expose domain concepts in interfaces rather than accidentally publishing a database driver's representation. Keep reusable mechanism separate from caller-specific policy, but do not build adapters for hypothetical future transports.

## Example and counterexample

Applies: a configuration loader produces a validated `RetryPolicy`; retry calculations accept that value directly. Invalid negative delays fail at loading with the offending field identified. The calculation tests require no filesystem.

Does not apply: a long-lived record was valid when read but another actor can revoke its permission before use. The initial validation does not justify deleting the transactional authorization check. Likewise, a typed assertion does not turn unparsed JSON into validated data.

## Verification

Exercise malformed and semantically invalid boundary inputs, valid inputs through the real adapter, and the core independently. Inspect where each invariant is established and whether mutation can break it. The result should identify the boundary, the trusted representation, and any guards intentionally retained. Do not call an internal check redundant solely because a static type exists.
