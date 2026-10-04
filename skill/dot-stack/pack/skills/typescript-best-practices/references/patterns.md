# TypeScript patterns and proof

The complete examples are [examples.ts](examples.ts); compile-time counterexamples are [type-checks.ts](type-checks.ts). They require an already available TypeScript compiler with support for the shown syntax and an ES2022 library. They install nothing. From this reference directory, run:

```sh
tsc --strict --noUncheckedIndexedAccess --exactOptionalPropertyTypes \
  --target ES2022 --module NodeNext --moduleResolution NodeNext \
  --noEmit examples.ts type-checks.ts
```

A project may use stricter settings. Check with its actual compiler as well. If `tsc` is not available, report these type claims unverified rather than silently substituting a parser or transpiler.

## Brands require constructors

`parseUserId` checks the entire string grammar before the one branded assertion. The brand prevents ordinary accidental mixing at compile time; it is erased at runtime and can be bypassed by an unsafe cast. It is neither authentication nor validation of untrusted values by itself. The constructor returns a specific error without echoing potentially sensitive rejected input.

Use the project's existing brand convention. A unique-symbol property avoids accidental structural collisions in this example; no single spelling is mandatory across repositories. Do not brand every string reflexively.

## Constructive models still need numeric validation

`NonEmpty<T>` encodes a known first element, and `first` indexes exactly that position. `isNonEmpty` checks both length and an own index-zero property: `new Array<number>(1)` has length one but no first element, so length alone is an unsound guard. A random numeric index can still return `undefined` under `noUncheckedIndexedAccess`; a non-empty tuple does not prove arbitrary indexing safe. A regular array remains correct for `sum`, whose empty result is zero.

The guard describes the array at the check, not after arbitrary mutation. A mutable alias can remove its first element even when this reference is readonly. Use the frozen copy returned by `snapshotNonEmpty` when the guarantee must survive mutation of the source or an asynchronous handoff. Snapshot creation returns `undefined` for an empty or missing-head array, so callers must narrow that result. An explicitly present `undefined` element is legitimate when `T` includes `undefined`. These collection helpers assume the existing element type is trusted; they do not parse hostile objects or validate every element.

Pairs can model an even-length sequence as `readonly (readonly [T, T])[]` when pair grouping reflects the actual domain. Converting to that structure still needs validation at an external boundary.

A `number` duration allows negative values, NaN, and infinity. `parseDurationMs` rejects them. `makeTimeRange` additionally validates the start and computed end against the supported date range, then returns a branded frozen record. The combined invariant belongs to that constructor, not a comment. `Object.freeze` is shallow; that is sufficient here because the fields are primitives.

The example accepts fractional milliseconds. If a project requires integer timestamps or duration units, add and test that constraint rather than claiming this example already enforces it.

## Unions and exhaustiveness

`LoadState` cannot normally represent both loading and ready at once. Switching on `kind` narrows the payload. The `never` assignment rejects a newly added variant unless the operation handles it. This is a compile-time safeguard for the declared union, not validation of a JSON response; parse external state before calling `renderState`.

## Unknown input becomes a constructed value

`parseUser` rejects null, arrays, missing fields, inherited-only fields, unknown keys, and invalid roles, then returns a new domain object. This example chooses strict unknown-key rejection. A forward-compatible protocol may intentionally ignore additional fields instead; state and test that policy explicitly. Avoid spreading the entire external input into a trusted object.

If the repository already uses a runtime schema library, prefer its parser and inferred type. Keep schema and inferred contract together. Do not introduce a dependency solely to replace this small example, or claim that a hand-written type predicate validates more than it checks.

## Assertions and narrowing have different jobs

Use discriminant narrowing, `in`, `typeof`, and `instanceof` when they describe actual possibilities. An assertion cannot turn bad data into valid data. The small assertions in validated brand constructors express a fact the compiler cannot derive. `as const` preserves literals; it is not the same risk as `payload as User`. A justified interop assertion should be localized and tested.

`satisfies` checks that the expression fits `ViewConfig` and preserves the useful literal theme in this example. It does not coerce data or run a validator. Do not promise identical literal inference for every type or expression; compile the actual case.

## Derivation and API design

`UserRole` and `ParsedUser` derive from the owning type or function. `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, and indexed access can prevent redundant definitions. They do not eliminate the need for a domain model when transport and domain invariants differ.

Object arguments make `displayUser` self-describing. For a simple one-argument function, a wrapper object may add noise. Choose from actual callers. Logging uses the project's conventions; a CLI's normal stdout is not an accidental debug log.

## Runtime validation to pair with compilation

Exercise actual exported functions after compiling the positive examples. Assert at least:

- `sum([])` is zero; `isNonEmpty([])` and a length-one sparse array are false; `first(["a"])` is `"a"`
- Empty and sparse snapshots are absent; a valid snapshot is frozen and its first element survives mutation of the source array
- A dense array containing an explicit `undefined` has a present head when its element type allows it
- Valid IDs and users are accepted; bad IDs, null, missing roles, invalid roles, and unexpected keys are rejected
- Zero and positive duration are accepted; negative, NaN, infinity, and strings are rejected
- A normal range gives the expected end; non-finite start and overflowing end are rejected
- Each load-state branch returns its literal expected value

Use explicit expected-error assertions for the negative type fixtures. Do not delete them as “comments”: an unused directive causes a compiler error and reveals that an invalid use unexpectedly became legal. These examples are educational fixtures; passing them does not verify the user's application.
