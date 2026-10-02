# Packet Stamp: An Installable Wheel That Cannot Print a Label

All package code, inputs and names in this example are original and fictional. The runnable result is a tiny dependency-free Python wheel, not a model of another project's build. The interesting failure happens after a real installation.

## The request and contract

> Verify the local Packet Stamp candidate as a fresh user. It must install offline and expose `packet-stamp`. `packet-stamp --style priority Ada` must print `PRIORITY: Ada` with exit 0. `packet-stamp Zoë` must print `TO: Zoë`. The installed package must contain the exact `formats.json` used by these commands. You may repair packaging metadata in a copied fixture and build a corrected candidate. Preserve the original source and failed wheel. Use the existing Python toolchain, install only this original fixture in disposable environments, and do not use a registry or promote a release.

The original [pyproject.toml](fixtures/source/pyproject.toml) declares distribution `packet-stamp-demo` version `0.3.0`, import package `packet_stamp`, and the public console command. It deliberately excludes implicit package data. The source tree contains [formats.json](fixtures/source/src/packet_stamp/formats.json), and the [CLI](fixtures/source/src/packet_stamp/cli.py) reads it through `importlib.resources`.

The CLI has no network or subprocess operations. It parses arguments, opens one package resource, formats a string and writes standard output or a bounded missing-resource error. The source build uses the existing Setuptools backend; it has no `setup.py`, custom build backend or dependency downloads.

## The observed defect

Running the source from its own `src` directory prints the correct label. Building that same source succeeds. The resulting wheel installs successfully in a new venv, and its installed command passes `--help` and prints `0.3.0` for `--version`.

The actual consumer invocation fails:

```text
$RUN/rejected-venv/bin/packet-stamp --style priority Ada
exit: 2
stdout: empty
stderr: packet-stamp: required bundled data formats.json is missing
```

Archive inspection gives the packaging cause: the original wheel has seven members and no `packet_stamp/formats.json`. Its internal `RECORD` is nevertheless consistent. An internally consistent archive can omit required content, and successful installation does not exercise every application resource.

| Evidence stage | Original wheel | Corrected wheel |
| --- | --- | --- |
| Build process | Exit 0 | Exit 0 |
| Required package content | Fail: data absent | Pass: exact JSON included |
| Wheel internal hashes | Pass | Pass |
| Fresh offline installation | Pass | Pass |
| Installed help/version | Pass | Pass |
| Data-dependent public command | Exit 2, missing resource | Exit 0, exact expected label |
| Installed package location | Inside original candidate's venv | Inside corrected candidate's new venv |

## The authorized repair

Append the [two-line packaging declaration](fixtures/package-data-repair.toml) to `pyproject.toml` in a second fresh source copy:

```toml
[tool.setuptools.package-data]
packet_stamp = ["formats.json"]
```

The application code and data bytes stay identical. The original fixture is not edited. Both candidates remain version `0.3.0` because this is a fictional comparison of local build candidates; neither was released to a package registry. The different SHA-256 digests are essential to identifying which was tested. For an actual release, follow its versioning policy; this example is not a procedure for overwriting published versions.

The corrected wheel contains eight members, including the exact 65-byte JSON resource. Its fresh installation resolves the package inside its own venv and yields:

```text
packet-stamp --style priority Ada
PRIORITY: Ada

packet-stamp Zoë
TO: Zoë
```

Both commands exit 0. An unsupported style exits 2 and reports an invalid choice. The main regression check is the same label command that failed before the packaging change.

## Reproduce with existing tools

Prerequisites: Python 3.10 or later with working `venv`/`ensurepip`, an existing host pip, and, for build mode, existing Setuptools and wheel packages. The actual checked environment was Linux x86-64 and Python 3.12.14. Other systems are not certified by this run.

Read [reproduce.py](scripts/reproduce.py), [probe_installed.py](scripts/probe_installed.py) and the four fixture source files before running. From this skill directory, select a new output path outside the skill:

```sh
python3 scripts/reproduce.py --verify-bundled --output ../packet-stamp-readback
```

This rechecks the two shipped wheels' stored SHA-256 values before copying them, then installs those exact copied bytes in separate disposable environments. It does not build source. The negative candidate's missing-data failure is expected; overall success means that failure was observed and the corrected candidate passed the bounded contract.

To rebuild both candidates and repeat all checks:

```sh
python3 scripts/reproduce.py --output ../packet-stamp-rebuild
```

Build mode copies the original fixture twice, appends the repair to only one copy, runs each source smoke separately, and uses the existing backend:

```sh
$PYTHON -I -m pip --isolated wheel --no-index --no-deps \
  --no-build-isolation --no-cache-dir --disable-pip-version-check \
  --wheel-dir "$OUTPUT/verified" "$RUN/verified-source"
```

Each candidate is installed by its new environment's pip using a direct wheel path:

```sh
$RUN/verified-venv/bin/python -I -m pip --isolated install \
  --no-index --no-deps --no-cache-dir --disable-pip-version-check \
  --no-compile --report "$RUN/verified-pip-report.json" \
  "$OUTPUT/verified/packet_stamp_demo-0.3.0-py3-none-any.whl"
```

The helper uses argument arrays, not a shell, for these subprocesses. `$PYTHON`, `$RUN`, `$OUTPUT`, `$SKILL`, `$BASE_PYTHON` and `$USER_HOME` in retained evidence are documented path substitutions: the current interpreter, disposable run root, selected output directory, this skill, the interpreter installation and the current user's home directory. They are not literal executable paths or downloadable URLs. Temp directories inside the run root also vary. Installer reports retain their original structure with local path substitutions; artifact digests, versions and member bytes are unchanged.

`SOURCE_DATE_EPOCH=1704067200` stabilizes wheel member timestamps for the example. Two builds using the recorded toolchain were byte-identical. A different backend or runtime may produce different archive bytes; compare fresh digests and contract evidence rather than claiming cross-toolchain bit reproducibility.

## Helper scope and outputs

The helper accepts only `--output` and `--verify-bundled`. It cannot be pointed at an arbitrary wheel or project. It:

- Requires a new output directory and refuses an existing path before changing it
- Reads the adjacent original fixture; build mode modifies only its temporary copies
- Uses a small subprocess environment, omits injected Python paths, disables user-site imports, and runs consumer commands outside every source copy
- Creates venvs with their default system-package isolation and bundled pip; it never uses a system package installation or upgrade command
- Invokes existing pip/Setuptools only, disables index/dependency lookup, and has no download or registry fallback
- Independently checks exact archive membership, `RECORD`, public entry registration, installed file hashes, venv provenance and the real public wrapper
- Records commands and outputs as they complete; an unexpected exit or 90-second per-command timeout stops the run without a pass
- Removes only the disposable directory it created after saving the evidence; original fixture and persisted output directories are preserved

The output contains the two wheels, a manifest, exact content ledgers, normalized installer reports, installed readbacks and the command transcript. Reusing an output path raises `FileExistsError`; choose a new path instead of clearing existing evidence.

The checks are purpose-built for this fixture's membership and metadata. They do not validate arbitrary wheel formats, enforce a network sandbox, verify package publisher identity, resolve third-party dependencies or test upgrades. Read [VERIFICATION.md](VERIFICATION.md) for the exact retained artifacts and executed coverage.
