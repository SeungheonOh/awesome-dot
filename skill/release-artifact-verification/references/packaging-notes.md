# Packaging Semantics Used by This Example

Official references reviewed on 2026-10-02. These explain the checks; the executed results are in [VERIFICATION.md](../VERIFICATION.md).

## Content and identity

A wheel is a ZIP distribution with package metadata and installation layout. `METADATA` declares its identity; `WHEEL` declares format and compatibility information. `RECORD` lists member hashes and sizes, with its own row left unhashed. The example reads every member and checks those records independently. The external SHA-256 identifies the complete wheel, including metadata. Neither digest is a publisher signature. See the [PyPA wheel specification](https://packaging.python.org/en/latest/specifications/binary-distribution-format/).

Setuptools `package-data` maps import-package names to file patterns. Explicit package data does not need an additional `MANIFEST.in` rule or a version-control plugin. The example disables implicit package-data inclusion, then adds the exact `formats.json` declaration in a copied source tree. It builds each candidate from a fresh copy so cached source lists cannot obscure the change. See [Setuptools data files](https://setuptools.pypa.io/en/latest/userguide/datafiles.html#package-data).

`console_scripts` registers a callable that an installer exposes as a command wrapper. Inspecting that registration proves what was declared; invoking the generated wrapper proves the tested installation can use it. See the [PyPA entry-points specification](https://packaging.python.org/en/latest/specifications/entry-points/).

## Installation and import boundaries

Python virtual environments use their own package directory; access to system site-packages is opt-in. A venv normally bootstraps pip using the interpreter's bundled `ensurepip`. The example does not use `--upgrade-deps`. It records the venv's actual pip version separately from the host builder. See [Python 3.12 venv](https://docs.python.org/3.12/library/venv.html).

Python `-I` excludes the script/current directory and user site from import paths and ignores `PYTHON*` environment variables. The helper also supplies a small explicit subprocess environment and verifies the imported package's location. It invokes the installed console command separately, using the clean environment and the generated venv wrapper. See [Python 3.12 isolated mode](https://docs.python.org/3.12/using/cmdline.html#cmdoption-I).

`importlib.resources.files()` accesses package resources through the import system. The fixture uses this to read its installed data rather than a path relative to the working directory. The readback independently hashes the installed file in this filesystem-backed wheel case. See [Python 3.12 resources](https://docs.python.org/3.12/library/importlib.resources.html).

For pip, `--no-index` suppresses index lookup but can still allow explicitly configured links; it is not a universal network block. The helper supplies a direct local wheel, disables config through `PIP_CONFIG_FILE`, uses isolated pip mode and no dependency resolution, and inspects the report's consumed digest. Build mode also sets `--no-build-isolation`, which requires the backend already to be installed. There is no dependency-install fallback. See [pip install options and reports](https://pip.pypa.io/en/stable/cli/pip_install/) and [pip wheel](https://pip.pypa.io/en/stable/cli/pip_wheel/).

These are a dependency-free fixture's bounded checks. They do not establish general package trust, network containment, reproducibility across backend versions or compatibility with every runtime allowed by a metadata declaration.
