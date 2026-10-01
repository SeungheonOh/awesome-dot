# Fictional example: valid unordered records, invalid ordering assumption

The archive's fictional response contract promises the complete matching print records and their multiplicity, in unspecified order. Each record contains `entry_id`, `title` and `copies`. The test incorrectly compares the returned list with one fixed list order.

The fictional user asks: “Investigate and fix this ordering-sensitive test. Keep the product's unordered response contract. Check that missing, extra and duplicate records still fail.” This authorizes the scoped test edit and local checks; there is no need to ask again before making that exact edit.

## Evidence and repair

The synthetic product function returns a copy of the same records shuffled by a local seeded generator. Before and after use the same predeclared seeds, the same product function and the same inputs. No attempt is retried until green.

The erroneous assertion is:

```python
require(actual == expected, "Ordered list equality failed")
```

The repair is:

```python
require(Counter(actual) == Counter(expected), "Complete-record multiset equality failed")
```

Here `Record` is a frozen dataclass: equality and hashing retain every declared field. `Counter` retains multiplicity. Converting the records to sets would let an added duplicate pass, so the example explicitly demonstrates and rejects that shortcut. A real response with nested or unhashable records needs a contract-aware canonical representation; dropping fields to make it hashable is not a valid repair.

This finding is an unsupported test assumption: valid response ordering changes but the promised record content does not. Sorting production output would add behavior the contract does not require. The example leaves the product function unchanged.

## Executed experiment

Run from this folder:

```sh
python3 check_example.py > example-results.json
```

The script uses only Python's standard library and in-memory fictional data. [example-results.json](example-results.json) records the observed results, environment, source digests, per-attempt seeds and returned order. It distinguishes implementation content digests from real repository commits.

The predeclared experiment uses seeds 0 through 11 once each for the original assertion and once each for the repaired assertion. It also exhausts the permutations of this small fixture and checks invalid outputs. The recorded result retains the actual pass/fail denominators rather than reporting only the final pass. These chosen seeds are a diagnostic sample, not a failure-probability estimate.

Every negative control must fail the repaired assertion:

- A missing record
- An extra new record
- An added duplicate
- A same-length replacement of one record with a duplicate of another
- A changed title with the same identifier
- Removal of one required duplicate from an alternate expected multiset

The harness treats those expected assertion failures as evidence that detection remains intact. Unexpected errors stop the script with a nonzero exit; they are not relabeled successes. Product and fixture digests, test implementation digests, budget and raw attempt outcomes remain in the record.

## Outcome and limits

On CPython 3.12.14, Linux x86_64, the original assertion failed 11 of 12 completed comparisons and passed one. The repaired assertion passed all 12 of the same seeded comparisons and all six fixture permutations. Every listed negative control produced the expected assertion failure. No attempt was skipped or retried. The full record is alongside the fixture in `example-results.json`.

This is a complete local demonstration of the narrow comparison repair. It does not test a real repository, test-runner retry settings, asynchronous races, shared fixtures, remote services or CI. Those paths would require the authorized artifacts and environment checks in the skill before making a claim about a real flaky test.
