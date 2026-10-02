# Executed Verification

Observed on 2026-10-02 using Linux, Python 3.12.14 and installed Info-ZIP UnZip 6.00. All source material is fictional, authored for this example. No user project, external service, credential, upload, recipient contact, program execution from the ZIP, or operating-system configuration change was involved.

## Retained artifacts

| Artifact | Evidence |
| --- | --- |
| [ZIP](artifacts/maple-client-help.zip) | 9,846 bytes; 9 regular members; 8,462 expanded bytes |
| [Manifest](artifacts/manifest.json) | 7 selected source-to-package rows, 3 explicit exclusions, 2 generated support members, source/package SHA-256 values and 12 mapped relative links |
| [Readback](artifacts/readback.json) | Actual native Linux extraction result, input preservation, counts and explicit untested target-platform fields |
| [Source bundle](fixtures/source-bundle.json) | All 10 original logical paths and their exact UTF-8 text; unchanged before/after |
| [Reviewed map](fixtures/reviewed-map.json) | Three approved copy-only renames and six exact reference changes; unchanged before/after |

ZIP SHA-256:

```text
58168fa9f6580545de2f64b20b2efebf254c6b027325a02cfddbed4c1e3bcab8
```

Source bundle SHA-256:

```text
3433cf0f5e59dd0fcbcd94b12f7048dd8f2e9883e8909991aa60cfff80b1c9a8
```

Reviewed map SHA-256:

```text
025cb246e8990892720da191b28fbb8a3dd7970aa49699bf3db24c314ab4399a
```

## Actual checks

1. Ran the reproducer with native extraction into a new isolated output directory. It read the exact source bundle/map, created and reopened actual prepared files, built the ZIP, reopened all ZIP members, then invoked the installed native `unzip` tool. Exit code was 0.
2. Independently read back the extracted tree. Exact file membership and all bytes matched the package plan; all nine members decoded as UTF-8. Twelve inline relative links resolved inside the extraction to the original logical targets under the approved map.
3. Compared byte results separately: four selected files remained byte-identical to the source records; three selected files contained only the six approved reference replacements. No excluded source entered the ZIP. Both JSON inputs remained unchanged.
4. Inspected archive metadata: regular-file attributes, no executable permission bits, no member extra fields or comments, no archive comment, fixed fictional timestamp and the expected single top-level folder. The generated manifest names the source identities and exclusions; these are safe to disclose here only because every item is fictional.
5. Reran against the existing output directory. The helper raised `FileExistsError` before writing; every preexisting output file's SHA-256 remained unchanged.
6. Ran a second fresh reproduction using Python standard-library extraction. That separately built ZIP was byte-identical to the native-run ZIP. Its report correctly labeled the method as Python extraction, and its byte/link checks also passed.
7. Executed the exact in-memory [scenario checks](scenario-checks.md). They rejected a case-colliding destination, a required-but-excluded dependency, an existing-but-wrong reference target, swapped targets for the two guide links, an undeclared support-member list, and a changed reference occurrence count. Each link retains its ordinal and label as well as its target. The unmodified fixture still passed and retained internal spaces and unchanged text bytes.
8. Ran the skill frontmatter validator: `Skill is valid!`.
9. Ran the repository's public-hygiene scanner on all ten final proposed files. It reported no matches for its specified internal-path, process-marker or credential patterns. This bounded pattern check does not prove absence of every possible sensitive value; the fixture and archive contents were also inspected directly.

Only locally generated fictional rehearsal directories were removed after retaining the exact ZIP, manifest and readback. The reproducer itself never deletes or overwrites an existing output directory, and real handoff files must not be cleaned up without authority.

## What remains untested

- Windows File Explorer extraction and the fictional recipient's actual filesystem, path depth, application versions and permissions
- macOS Finder extraction or behavior on either case-sensitive or case-insensitive APFS
- Clickable Markdown rendering, native application portability, executable behavior, fonts or external dependencies
- Arbitrary Unicode filename equivalence, general Markdown syntax, binary application references, native document packages, ACLs and extended attributes
- Actual transmission, destination access, recipient receipt or recipient use

The helper's filename screen is intentionally limited to the supplied ASCII scenario and a conservative path budget. It does not emulate Windows or macOS. The source names remain in portable JSON records; there was no case-colliding public directory checkout and no claim that the original names could be created on Windows.

Platform-rule references were reviewed on 2026-10-02: [Microsoft naming rules](https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file), [Microsoft path-length behavior](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation), and [Apple filesystem options](https://support.apple.com/guide/disk-utility/file-system-formats-dsku19ed921c/mac).
