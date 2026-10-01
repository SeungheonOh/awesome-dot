# Recorded Fixture Verification

Executed on 2026-10-01 using Python 3.12.14 on Linux. The exact runnable command and code are in the [worked example](worked-example.md#reproduce-the-executed-check). The command completed with exit status 0; all fixture assertions passed. The skill frontmatter/name validator also passed.

## Observed recovery report

```text
Capture: capture-sep28 (fictional historical snapshot)
Selection: six explicitly selected fictional items
Manifest entries: 5 / 6 selected
Backup payloads found: 4 / 6 selected
Restored copies created: 4 / 6 selected
Restored bytes match both baselines: 3 / 4 copied, 3 / 6 selected
UTF-8 text reopen passed: 3 / 3 attempted, 3 / 4 copied
Historical bytes and text readability both verified: 2 / 6 selected
Source and backup byte digests and membership preserved: true
Manifest unchanged: true
Existing destination collision rejected without overwrite: true
```

| Item | Historical evidence / payload | Restored bytes | Reopen result | Current source | Outcome |
| --- | --- | --- | --- | --- | --- |
| `guide.txt` | Manifest and payload present | 32 bytes, both baselines match | UTF-8 passed | Matches historical bytes | Historical bytes and text readability verified |
| `plan.txt` | Manifest and payload present | 20 bytes, both baselines match | UTF-8 passed | Known later edit differs | Historical bytes and text readability verified; source change recorded separately |
| `unlisted.txt` | Manifest entry missing; payload search not performed | No copy | Not attempted | Not compared | Historical evidence missing |
| `absent.txt` | Manifest present; payload absent | No copy | Not attempted | Not compared | Backup payload missing |
| `copy-check.txt` | Manifest and 51-byte payload agree | 50 bytes, both comparisons fail | UTF-8 passed | Matches historical bytes | Copy verification failed despite readable text |
| `drawing.fiction` | Manifest and payload present | 49 bytes, both baselines match | Untested; unsupported format | Matches historical bytes | Bytes verified; usability untested |

Representative observed SHA-256 values:

```text
guide.txt manifest = backup = restored
3e989a0ad91f41d5ff21066f3e92ae3b048efb5a0a6082476e091754a964c27a

copy-check.txt manifest = backup
b807ef478435bc3c27adbdf85dc05f5390221a3d7d31436186666a1a99dd546c

copy-check.txt restored (deliberate fixture-only short write)
f4735bcb5c8389278b7160396b1e1899aea92539325667950f7b192db2c7e83a
```

The failed copy, missing evidence, unavailable payload and unsupported format are expected test outcomes, not failed assertions. They stay visible in the completed report and prevent a blanket pass. Both the historical source-change distinction and the fact that readable text can have mismatched bytes are verified by assertions.

## Additional isolated baseline-conflict regression

Executed separately within the same command, using its own temporary plain-file fixture. Its manifest describes the historical text “Use the ivory cover.” Its preexisting synthetic backup payload says “Use the violet cover.” The restore copies that backup payload faithfully, then reopens and reads it. No source, backup or manifest repair is performed.

```text
Backup payload matches historical manifest: false
Restored bytes match observed backup payload: true
Restored bytes match historical manifest: false
UTF-8 reopen: passed
Outcome: backup-versus-manifest baseline conflict
Source, backup and manifest preserved: true
```

The shared outcome classifier requires faithful copying, backup-to-manifest agreement, restored-to-manifest agreement and a successful text reopen before reporting historical bytes and text readability verified. This regression establishes that a readable faithful copy of a conflicting backup is not historical success. The deliberately truncated copy remains a separate `copy verification failed` case. The original six-item table and counts above are unchanged; this regression is not added to their denominators.

## Limits and next decisions

- The known fixture manifest was created from synthetic capture bytes. The check does not authenticate a real manifest or establish full backup coverage
- Readability was tested only by reopening and decoding ordinary UTF-8 text. No application consistency, native-document fidelity, metadata, permissions, encryption or external dependencies were tested
- Source and backup preservation checks compare regular-file membership and content digests. They do not claim preservation of access timestamps or all filesystem metadata
- No real restore service or user destination was exercised. A real run must establish its own authorized access, stable snapshot identity, destination isolation and readback results
- In a real run, request the missing historical record for `unlisted.txt`, locate the requested payload for `absent.txt`, recheck the baseline before an authorized fresh copy of `copy-check.txt`, and obtain a compatible open check for `drawing.fiction`
- Temporary fixture files were removed by the fixture's context manager only after the checks completed. Real restored copies remain where the user approved; deletion or cleanup needs its own authority

Conclusion: this executed rehearsal demonstrates bounded retrieval, exclusive creation, readback, digest comparison and honest per-file outcomes. It does not demonstrate a fully recoverable backup.
