# Observed verification

Executed on 2026-10-02 with Python 3.12.14 on Linux, using the standard library. No additional software was installed. The fixture commands make no network requests, collect no device logs and perform no upload.

From this companion directory:

```bash
python3 reproduce.py check
python3 reproduce.py build --out reproduced-output
python3 reproduce.py check --out reproduced-output
```

All three commands exited `0`. The fresh reproduction was checked in a separate local copy of the fixture; it is not an additional recipient attachment. A second build to an existing destination is tested and rejected without changing its saved files.

## What was observed

- All nine input objects produce nine ordered event occurrences. The original and policy fingerprints still match their frozen values after the run
- Exact error codes `E_TIMEOUT`, `E_UNREACHABLE` and `E_REMOTE_BUSY` remain at occurrences 3, 6 and 9. A separate positive case appends a repeated error object and retains it as a tenth occurrence with the same operation alias
- `OP-001` correlates occurrences 2, 3, 4, 7, 8 and 9. `OP-002` stays separate. Missing/null identifiers are not filled from adjacent events
- The tie at occurrences 3–4 and backwards timestamp at 4–5 remain visible. Occurrence 6 has an explicit-null timestamp; occurrence 7 has an absent timestamp. A present zero sent-byte count stays distinct from an absent counter
- The complete saved packet bytes match the approved source-derived projection. Its recursive membership is exactly `events.jsonl` and `summary.txt`, with no directories or symlinks
- The separate record matches the source/policy/output hashes and every generated field/removal decision. It records top-level subtree locators, reasons and retained alias assignments, without repeating removed values or raw identifiers
- The summary and source were read together: no completion or root cause was invented, omitted explanatory text is disclosed as a limit, and the result remains `prepared_only` with `shared: false`

The final checker reported:

```text
PASS: 9 source-ordered occurrences, 3 errors, exact codes, counters, timestamp states and aliases
PASS: approved packet membership, complete source/policy/output hashes and separate locator record
PASS: 31 negative cases; saved packet and review record unchanged
PASS: original and policy bytes unchanged; preparation only, no network or upload
LIMIT: this fictional flat-schema excerpt only; metadata outside the bytes and remote access uninspected
```

The 31 rejected cases cover nested or unreviewed retained values, free text in an enum, boolean/string/out-of-range counters, nested/control-character alias inputs, timestamps outside the approved window, duplicate diagnostic-code keys, malformed JSON, non-object and blank records, non-finite nested values, unsupported policy keys/control types/rules/source sets, dropped/reordered/extra event records even with updated output hashes, a changed summary outcome, source drift, unsupported release claims, an existing output destination, extra packet files/directories and symlink members/destinations. The negative mutations leave the saved fixtures unchanged.

Python's default JSON decoder can discard earlier repeated keys and accepts non-finite constants. The helper instead checks ordered key/value pairs before building dictionaries and rejects non-finite constants; source errors report the source line and field when known. These specific API choices were checked against the [Python JSON documentation](https://docs.python.org/3.12/library/json.html#repeated-names-within-an-object) and its [decoder parameters](https://docs.python.org/3.12/library/json.html#json.load), read on 2026-10-02.

## Checked file identities

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `originals/diagnostics.jsonl` | 2894 | `75ab81aae71f8a336a4e0f4b4ac5f0483ccf439a9b75117a2513c77bf3d9b3c9` |
| `policy.json` | 1707 | `26a58115fec53310e744422e1b46ca4cf4399f4abc87a8d51b5de9248c891c07` |
| `example-output/recipient/events.jsonl` | 3234 | `114460484942e8925dd9ae384c63ced444a9b0021d60872094a2a437388f08c1` |
| `example-output/recipient/summary.txt` | 2132 | `9feb191a18fd1c33383648a5ccf40f7fe3aa73acb845791dfce8b31b39599520` |
| `example-output/private/review-record.json` | 16641 | `68785c66cc2c0cc4cec4ff2372b33f5364c655e5d506c39813599f67037eb18a` |

## Limits

This is a regression fixture for one approved, fictional, flat schema. The CLI freezes its supplied source and policy; it is not a general-purpose log processor. Supporting a different source or policy requires a fresh human review and corresponding fixture changes. Someone who edits the policy, expected hashes and checker together can change what it accepts. Hashes bind checks to bytes; they do not independently establish permission or appropriate content.

No filesystem attributes, transport metadata, remote permissions/history, transformed upload, compressed/binary log container, earlier/later log excerpt or real recipient identity was checked. No general anonymity claim follows from aliases. File creation checks are local no-clobber checks, not protection against hostile concurrent filesystem replacement. The script loads this small fixture into memory and is not designed for large or adversarially resource-intensive inputs. Output checks need repeating after edits or packaging, and real sharing requires the applicable destination and permission checks.

## Independent readback

A separate check reproduced the two recipient files and the private-style review record byte-for-byte, reran all 31 negative cases and verified source preservation. A fresh three-event projection kept independent alias namespaces, input order, absent/null/zero distinctions and a qualified unknown outcome; the omitted marker values remained absent from both the packet and the review record. Escaped and nested duplicate keys and a floating-point value in an integer field were rejected. A duplicate-key input failed before creating its output directory. These were original local fixtures; no logs were collected from a device or account, and no sharing occurred.
