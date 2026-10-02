"""Inspect this fictional package in the interpreter that actually imports it."""

import hashlib
import importlib.metadata as metadata
import importlib.util
import json
import os
from pathlib import Path
import site
import sys
import sysconfig


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    venv = Path(sys.argv[1]).resolve()
    source_roots = [Path(p).resolve() for p in sys.argv[2:]]
    require(Path(sys.prefix).resolve() == venv, "wrong virtual environment")
    require(sys.prefix != sys.base_prefix, "not running in a virtual environment")
    require(sys.flags.isolated == 1, "provenance probe is not in isolated mode")
    require(site.ENABLE_USER_SITE is False, "user site is enabled")
    configuration = (venv / "pyvenv.cfg").read_text(encoding="utf-8").lower()
    require("include-system-site-packages = false" in configuration, "system site-packages is enabled")
    require("PYTHONPATH" not in os.environ and "PYTHONHOME" not in os.environ, "injected Python path")
    require(all(not Path.cwd().resolve().is_relative_to(root) for root in source_roots), "consumer cwd is inside source")
    for entry in sys.path:
        require(bool(entry), "current-directory path entry")
        path = Path(entry).resolve()
        require(all(not path.is_relative_to(root) for root in source_roots), "source path leaked into imports")
    purelib = Path(sysconfig.get_path("purelib")).resolve()
    require(purelib.is_relative_to(venv), "site-packages is outside the virtual environment")
    spec = importlib.util.find_spec("packet_stamp")
    require(spec is not None and spec.origin is not None, "package unavailable")
    origin = Path(spec.origin).resolve()
    require(origin.is_relative_to(purelib), "package resolved outside installed site-packages")
    import packet_stamp

    dist = metadata.distribution("packet-stamp-demo")
    require(dist.version == packet_stamp.__version__ == "0.3.0", "installed version mismatch")
    entries = [(e.name, e.value) for e in dist.entry_points if e.group == "console_scripts"]
    require(entries == [("packet-stamp", "packet_stamp.cli:main")], "entry point mismatch")
    installed = {}
    for name in ("__init__.py", "cli.py", "formats.json"):
        path = origin.parent / name
        installed[name] = hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None
    print(json.dumps({
        "prefix": sys.prefix,
        "base_prefix": sys.base_prefix,
        "python": sys.version.split()[0],
        "executable": sys.executable,
        "user_site_enabled": site.ENABLE_USER_SITE,
        "system_site_enabled": False,
        "isolated_probe": bool(sys.flags.isolated),
        "sys_path": sys.path,
        "cwd": str(Path.cwd()),
        "module_origin": str(origin),
        "distribution_version": dist.version,
        "console_scripts": entries,
        "installed_package_sha256": installed,
    }, indent=2))


if __name__ == "__main__":
    main()
