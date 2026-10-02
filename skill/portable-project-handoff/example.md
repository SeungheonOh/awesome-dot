# A Client Help Handoff with Two Different Guides

All people, files and content are original fictional examples. The recipient is Rowan Alder, who wants to read a small documentation bundle for the fictional Maple client on Windows 11 using File Explorer extraction and a plain UTF-8 editor. The application itself is not included. No account, upload, external contact or real person's files are involved.

## Fictional request and boundaries

“Prepare a ZIP for Rowan from these seven selected project files. Keep the starting page, both guides, release notes, interface colour notes, keyboard shortcuts and license. Leave the old draft, preview cache and scratch notes out. Make the three destination renames listed below and repair only their six matching links in the copied text. Keep the originals unchanged. Use the new local handoff folder, keep the ZIP below 2 MiB, and don't send it yet.”

The source collection has ten logical files, each with exact UTF-8 text in [source-bundle.json](fixtures/source-bundle.json). Storing the original names as JSON records is intentional: the example remains check-outable on filesystems that cannot store both `docs/Guide.md` and `docs/guide.md`, or the colon in `notes/Release:notes.md`. It is a small complete source bundle, not an assertion that a Windows source directory ever contained those names. The handoff itself is a real ZIP with real regular-file members.

All selected links stay within the seven selected files. There are no external dependencies, scripts, executables, macros, symlinks or native application packages.

## Exact selection and copied names

| Original logical path | Package-relative path | Bytes |
| --- | --- | --- |
| `Start here.md` | `Start here.md` | Three approved link-target replacements |
| `docs/Guide.md` | `docs/setup-guide.md` | Unchanged |
| `docs/guide.md` | `docs/troubleshooting-guide.md` | One approved link-target replacement |
| `notes/Release:notes.md` | `notes/release-notes.md` | Two approved link-target replacements |
| `assets/Interface Colors.txt` | `assets/Interface Colors.txt` | Unchanged |
| `reference/Keyboard shortcuts.txt` | `reference/Keyboard shortcuts.txt` | Unchanged |
| `LICENSE.txt` | `LICENSE.txt` | Unchanged |

The two source guides are different documents: one describes setup, the other troubleshooting. They must not be collapsed as duplicates. The new names preserve that distinction. Internal spaces in `Start here.md` and `Interface Colors.txt` remain; their existing percent-encoded links remain valid in the fixture's link grammar.

Excluded, with original source records preserved:

- `drafts/old-help.md`: superseded draft expressly outside the handoff
- `preview-cache/ui-preview.txt`: regenerable preview description, referenced by no selected file
- `scratch/personal-reminder.txt`: excluded scratch note; its contents are wholly fictional

The ZIP adds two declared support members: `MANIFEST.json` and `HANDOFF.txt`. They do not replace or expand the selected project files. The outer folder is `Maple-client-help`.

## Six exact approved reference edits

| Copied file | Original destination text | New destination text |
| --- | --- | --- |
| `Start here.md` | `docs/Guide.md` | `docs/setup-guide.md` |
| `Start here.md` | `docs/guide.md` | `docs/troubleshooting-guide.md` |
| `Start here.md` | `notes/Release%3Anotes.md` | `notes/release-notes.md` |
| `docs/troubleshooting-guide.md` | `../notes/Release%3Anotes.md` | `../notes/release-notes.md` |
| `notes/release-notes.md` | `../docs/Guide.md` | `../docs/setup-guide.md` |
| `notes/release-notes.md` | `../docs/guide.md` | `../docs/troubleshooting-guide.md` |

Each occurrence is expected exactly once. [reviewed-map.json](fixtures/reviewed-map.json) stores the parenthesized replacement tokens and counts. The builder rejects an unexpected occurrence count rather than guessing. It separately retains each link's ordinal and label, then checks that its target is the mapped identity of the original target. Swapping the setup and troubleshooting targets fails even though the set of destinations is unchanged.

## Archive and readback

The delivered [ZIP](artifacts/maple-client-help.zip) is 9,846 bytes with SHA-256:

```text
58168fa9f6580545de2f64b20b2efebf254c6b027325a02cfddbed4c1e3bcab8
```

It contains nine regular files, totalling 8,462 expanded bytes. ZIP members use a fixed fictional timestamp and ordinary non-executable regular-file attributes; source filesystem timestamps, permissions, extended attributes and native document identities are not represented by this source bundle. `ZIP_STORED` avoids compression-version variability for this tiny reproducible example.

The actual archive was reopened, then extracted by installed native Linux `unzip` into a new isolated folder. All nine extracted members matched their planned bytes and decoded as UTF-8. All twelve relative links resolved to their intended selected files. Four selected files stayed byte-identical; three contain only the six reviewed reference edits. Both source JSON files remained byte-identical throughout the run.

The destination name check found no conflicts under the example's conservative ASCII Windows screen. It uses a fictional short extraction base, `C:\Handoffs`, and a conservative 240-character total path budget for this example. That budget is a preparation choice, not a universal Windows limit. The source screen reported the guide-name collision and colon-containing component.

This establishes the Linux extraction and plain-text/reference results above. Windows File Explorer extraction, the recipient's actual disk/path settings, clickable Markdown rendering, macOS extraction and application execution were not tested. The prepared package has not been sent. A later recipient-side check should extract the entire folder into a fresh location and read `Start here.md`, both distinct guides and the keyboard/colour references; it should report the actual extraction/viewer used.
