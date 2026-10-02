# Executed Artifact Verification

Observed on 2026-10-02 with Linux x86-64 and Python 3.12.14. The existing build tools were pip 26.2.1, Setuptools 84.0.0 and wheel 0.48.0. Each newly created venv bootstrapped its bundled pip 25.0.1; no upgrade or dependency download was requested. All source, data and package names are fictional and original to this example.

## Exact retained artifacts

Distribution: `packet-stamp-demo` version `0.3.0`. Both local candidate filenames are `packet_stamp_demo-0.3.0-py3-none-any.whl`; separate directories and hashes identify their different bytes.

| Candidate | Size | Members | Packaging | Installation | Consumer runtime |
| --- | ---: | ---: | --- | --- | --- |
| [Preserved rejected wheel](artifacts/rejected/packet_stamp_demo-0.3.0-py3-none-any.whl) | 2,237 bytes | 7 | Required JSON absent | Passed | Failed with exit 2 |
| [Checked wheel](artifacts/verified/packet_stamp_demo-0.3.0-py3-none-any.whl) | 2,464 bytes | 8 | Exact JSON present | Passed | Passed with exit 0 |

Rejected wheel SHA-256:

```text
123eb61e134938fea1cd9509ce69bd6e3a0f64e65067ae83aaec508addcbad6b
```

Checked wheel SHA-256:

```text
f8196f39158568c1764a10639e0a2cd5136fa7767725954a3e5e0f9f8ab548bf
```

The corrected artifact's complete membership is:

```text
packet_stamp/__init__.py
packet_stamp/cli.py
packet_stamp/formats.json
packet_stamp_demo-0.3.0.dist-info/METADATA
packet_stamp_demo-0.3.0.dist-info/RECORD
packet_stamp_demo-0.3.0.dist-info/WHEEL
packet_stamp_demo-0.3.0.dist-info/entry_points.txt
packet_stamp_demo-0.3.0.dist-info/top_level.txt
```

The [content ledger](artifacts/verified-contents.json) gives exact byte sizes and SHA-256 for every member. The wheel declares no runtime dependencies, `Requires-Python: >=3.10`, a `py3-none-any` tag and `packet-stamp = packet_stamp.cli:main`.

The 65-byte resource `packet_stamp/formats.json` has the same digest in the original source, corrected archive and installed environment:

```text
c093966c588a7304a4123cc0716f69c0935816cb1d1c46b50239eb2f4948cbe1
```

## Build, installation and runtime evidence

The final build run completed 24 recorded subprocess calls, including the expected original CLI failure and invalid-option rejection. The [command transcript](artifacts/commands.json) records argument arrays, working directories, UTC start times, expected and actual exit statuses, standard output and standard error. Local path substitutions are explained in [EXAMPLE.md](EXAMPLE.md); they preserve the relation between source roots, consumer directories and environment interpreters.

1. Ran the source command separately in each temporary source copy. Both returned `PRIORITY: Ada` with exit 0. Those source-path imports are explicitly labeled source smoke and were not reused for installed execution.
2. Built each wheel through existing pip and Setuptools, with no build isolation, no dependency resolution and no index lookup. Both builds returned exit 0. The corrected source copy differed only by the appended package-data declaration.
3. Read every archive member. Exact fixture membership, identity metadata, entry-point registration and `RECORD` hashes/sizes matched their declared state. The original artifact's missing data was preserved as a failed packaging contract, not hidden by the internally valid archive.
4. Created a separate fresh venv for each wheel and proved `packet_stamp` was absent before installation. Direct local wheel installations returned exit 0. Each [installer report](artifacts/verified-installation.json) recorded the consumed SHA-256 matching the corresponding retained artifact; pip installed only the fixture. `pip check` returned exit 0.
5. Ran the provenance probe with each venv's interpreter in isolated mode. It verified `include-system-site-packages = false`, disabled user-site imports, absent `PYTHONPATH`/`PYTHONHOME`, source-free import paths, and a module location inside that venv's site-packages. The probe and public CLI ran in fresh consumer directories outside all source copies.
6. Read the installed wrapper's shebang and executable flag on Linux. It selected that candidate's venv interpreter. Read back the installed code and resource hashes. The [checked readback](artifacts/verified-readback.json) matches the wheel's exact `.py` and JSON bytes; the [rejected readback](artifacts/rejected-readback.json) records the resource as absent.
7. Invoked each installed public wrapper. Both passed help and version checks. The original candidate's data-dependent command exited 2 with `packet-stamp: required bundled data formats.json is missing`. The checked candidate printed `PRIORITY: Ada` and `TO: Zoë` with exit 0. An unknown style exited 2 and reported an invalid choice.
8. Compared the five preserved fixture inputs before and after execution; every hash matched. The [manifest](artifacts/manifest.json) includes both input manifests, helper source hashes, environment overrides, tool versions and stage-specific verdicts.

## Separate readback and guard checks

After copying the final wheels into this skill, ran `reproduce.py --verify-bundled` with a new output directory. It rehashed those shipped files against the manifest, copied and installed those exact bytes into two more fresh venvs, and reproduced the original failure and corrected pass. This did not substitute newly built wheels for the delivered artifacts.

The [guard check record](artifacts/guard-checks.json) also records these actual checks:

- Evaluated the omitted-data wheel against the required passing membership: rejected for a missing member
- Changed only the JSON bytes in a temporary wheel copy while preserving its original `RECORD`: rejected for a resource hash mismatch; the retained wheel was unchanged
- Reran the helper with an existing output directory: it raised `FileExistsError`, and every preexisting output file's digest was unchanged
- Compared the two independently built candidate pairs: both rejected wheels and both checked wheels were byte-identical under the recorded toolchain

The helper's main run succeeds only when it observes the expected negative candidate and the corrected candidate passes. It is a fixture rehearsal, not a general-purpose declaration that any supplied release is good.

Skill frontmatter validation passed. All local Markdown links resolved. The complete 22-file packet passed the public-hygiene scanner's specified path, process-marker and credential patterns. A separate text review also decoded every wheel member and checked the generated reports for raw local execution paths. These are bounded hygiene checks, not a proof that every possible sensitive value can be detected.

## Limits

- Only Linux x86-64, Python 3.12.14 and the listed tools were exercised. The declared Python floor and platform-independent wheel tag are not a tested compatibility matrix
- Windows executable wrappers, macOS installation, other Python versions, GUI behavior and alternate package managers were not run
- The example has no runtime dependencies; dependency resolution, optional extras, native extensions and third-party installation hooks were not tested
- No source-distribution build route, upgrades over a prior installation, uninstall behavior, package-registry upload, production deployment or release promotion was performed
- Timestamp normalization gave identical bytes on this toolchain; reproducibility across backend versions was not established
- Checksums and internal `RECORD` checks detect byte mismatches relative to these records; they do not authenticate a publisher or establish package security
- The minimal environment and offline flags prevent the intended development-path and registry routes in this reviewed fixture. They are not an operating-system sandbox or packet capture

This deliverable verifies an actual local package and one concrete consumer workflow. It is not a release approval, a deployment result or evidence about an unrelated product.

## Independent exact-artifact readback

An independent review inspected the helpers and installed the two delivered wheel digests into separate fresh environments. The bundled-artifact route completed 20 subprocess calls, reproduced the rejected candidate’s missing-resource failure and the corrected candidate’s successful public invocation, and verified installed origins, wrapper interpreter and resource bytes outside the source checkout. The original packet stayed unchanged.

A separate static control kept the same name/version and complete membership and rebuilt an internally consistent `RECORD`, but changed the required resource text. The resource contract still rejected it. That altered copy was inspected only; it was not installed or executed.
