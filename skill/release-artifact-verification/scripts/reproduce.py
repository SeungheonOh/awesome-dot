#!/usr/bin/env python3
"""Build or recheck ONLY the adjacent original offline fixture.

Creates a new output directory, uses new disposable virtual environments, and
executes the reviewed fixture/backend. It is not a general wheel installer,
archive validator, security sandbox, or permission to run third-party payloads.
"""

import argparse
import base64
import configparser
import csv
from datetime import datetime, timezone
from email.parser import BytesParser
import hashlib
import importlib.metadata as metadata
import io
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
WHEEL_NAME = "packet_stamp_demo-0.3.0-py3-none-any.whl"
DIST_INFO = "packet_stamp_demo-0.3.0.dist-info"
LIMIT = 2 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_manifest():
    return {str(p.relative_to(ROOT / "fixtures")): sha(p.read_bytes())
            for p in sorted((ROOT / "fixtures").rglob("*")) if p.is_file()}


def inspect_wheel(path, data_expected):
    """Check this small fixture's exact membership and all RECORD digests."""
    require(path.stat().st_size <= LIMIT, "artifact exceeds 2 MiB")
    members = ["packet_stamp/__init__.py", "packet_stamp/cli.py"] + [
        f"{DIST_INFO}/{n}" for n in ("METADATA", "WHEEL", "entry_points.txt", "top_level.txt", "RECORD")]
    if data_expected:
        members.append("packet_stamp/formats.json")
    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)), "duplicate wheel member")
        require(set(names) == set(members), "unexpected or missing wheel member")
        require(sum(i.file_size for i in infos) <= LIMIT, "expanded artifact exceeds 2 MiB")
        payload = {n: archive.read(n) for n in names}
    records = list(csv.reader(io.StringIO(payload[f"{DIST_INFO}/RECORD"].decode("utf-8"))))
    require(all(len(r) == 3 for r in records), "invalid RECORD row")
    require(len(records) == len(names) and {r[0] for r in records} == set(names), "RECORD coverage mismatch")
    for name, digest, size in records:
        if name == f"{DIST_INFO}/RECORD":
            require(digest == size == "", "RECORD must not hash itself")
        else:
            encoded = base64.urlsafe_b64encode(hashlib.sha256(payload[name]).digest()).rstrip(b"=").decode()
            require(digest == "sha256=" + encoded and size == str(len(payload[name])), "RECORD mismatch: " + name)
    package_metadata = BytesParser().parsebytes(payload[f"{DIST_INFO}/METADATA"])
    wheel_metadata = BytesParser().parsebytes(payload[f"{DIST_INFO}/WHEEL"])
    require(package_metadata["Name"] == "packet-stamp-demo", "distribution name mismatch")
    require(package_metadata["Version"] == "0.3.0", "distribution version mismatch")
    require(package_metadata["Requires-Python"] == ">=3.10", "runtime declaration mismatch")
    require(package_metadata.get_all("Requires-Dist", []) == [], "unexpected runtime dependency")
    require(wheel_metadata["Tag"] == "py3-none-any", "wheel tag mismatch")
    require(wheel_metadata["Root-Is-Purelib"] == "true", "not a pure Python wheel")
    entries = configparser.ConfigParser()
    entries.read_string(payload[f"{DIST_INFO}/entry_points.txt"].decode())
    require(dict(entries["console_scripts"]) == {"packet-stamp": "packet_stamp.cli:main"}, "public entry mismatch")
    for name in ("__init__.py", "cli.py") + (("formats.json",) if data_expected else ()):
        require(payload["packet_stamp/" + name] == (ROOT / "fixtures/source/src/packet_stamp" / name).read_bytes(),
                "packaged source/data differs: " + name)
    return {
        "filename": path.name, "bytes": path.stat().st_size, "sha256": sha(path.read_bytes()),
        "distribution": package_metadata["Name"], "version": package_metadata["Version"],
        "requires_python": package_metadata["Requires-Python"], "tag": wheel_metadata["Tag"],
        "generator": wheel_metadata["Generator"], "record_verified": True,
        "required_data_present": "packet_stamp/formats.json" in names,
        "members": [{"path": n, "bytes": len(payload[n]), "sha256": sha(payload[n])} for n in sorted(names)],
    }


class Recorder:
    def __init__(self, output, run):
        self.output, self.run = output, run
        self.rows = []
        self.env = {"PATH": os.defpath, "LC_ALL": "C", "PYTHONNOUSERSITE": "1",
                    "PYTHONUTF8": "1", "PYTHONDONTWRITEBYTECODE": "1",
                    "PIP_CONFIG_FILE": os.devnull, "SOURCE_DATE_EPOCH": "1704067200"}
        if os.name == "nt" and "SYSTEMROOT" in os.environ:
            self.env["SYSTEMROOT"] = os.environ["SYSTEMROOT"]

    def portable(self, value):
        replacements = [(str(self.run), "$RUN"), (str(self.output), "$OUTPUT"),
                        (str(ROOT), "$SKILL"), (sys.executable, "$PYTHON"),
                        (sys.base_prefix, "$BASE_PYTHON"), (str(Path.home()), "$USER_HOME")]
        if isinstance(value, str):
            for old, new in sorted(replacements, key=lambda x: -len(x[0])):
                value = value.replace(old, new)
            return value
        if isinstance(value, list):
            return [self.portable(v) for v in value]
        if isinstance(value, dict):
            return {k: self.portable(v) for k, v in value.items()}
        return value

    def command(self, label, args, cwd, expected=0):
        args = [str(a) for a in args]
        start = datetime.now(timezone.utc).isoformat()
        try:
            process = subprocess.run(args, cwd=cwd, env=self.env, text=True, encoding="utf-8",
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=90, check=False)
        except subprocess.TimeoutExpired as error:
            self.rows.append({"label": label, "argv": args, "cwd": str(cwd), "started_utc": start, "status": "timeout"})
            self.save()
            raise RuntimeError(label + " timed out; no pass inferred") from error
        self.rows.append({"label": label, "argv": args, "cwd": str(cwd), "started_utc": start,
                          "exit_code": process.returncode, "expected_exit_code": expected,
                          "stdout": process.stdout, "stderr": process.stderr})
        self.save()
        require(process.returncode == expected, label + " unexpected exit: " + str(process.returncode))
        return process

    def save(self):
        write_json(self.output / "commands.json", self.portable(self.rows))


def exercise(wheel, audit, output, run, recorder, label, data_expected):
    envroot = run / (label + "-venv")
    consumer = run / (label + "-consumer")
    consumer.mkdir()
    recorder.command(label + ": create venv", [sys.executable, "-I", "-m", "venv", envroot], consumer)
    binary = envroot / ("Scripts" if os.name == "nt" else "bin")
    python = binary / ("python.exe" if os.name == "nt" else "python")
    cli = binary / ("packet-stamp.exe" if os.name == "nt" else "packet-stamp")
    recorder.command(label + ": package absent before install", [python, "-I", "-c",
        "import importlib.util; assert importlib.util.find_spec('packet_stamp') is None"], consumer)
    recorder.command(label + ": pip version", [python, "-I", "-m", "pip", "--version"], consumer)
    pip_report = run / (label + "-pip-report.json")
    recorder.command(label + ": install exact wheel", [python, "-I", "-m", "pip", "--isolated", "install",
        "--no-index", "--no-deps", "--no-cache-dir", "--disable-pip-version-check", "--no-compile",
        "--report", pip_report, wheel], consumer)
    install = json.loads(pip_report.read_text(encoding="utf-8"))
    require(len(install["install"]) == 1, "installer received unexpected packages")
    installed_item = install["install"][0]
    require(installed_item["download_info"]["archive_info"]["hashes"]["sha256"] == audit["sha256"],
            "installer artifact hash mismatch")
    require(installed_item["metadata"]["version"] == "0.3.0", "installer version mismatch")
    write_json(output / (label + "-installation.json"), recorder.portable(install))
    recorder.command(label + ": dependency consistency", [python, "-I", "-m", "pip", "--isolated", "check",
        "--no-cache-dir", "--disable-pip-version-check"], consumer)
    wrapper = {"path": str(cli), "sha256": sha(cli.read_bytes()), "interpreter_readback": "unverified on Windows"}
    if os.name != "nt":
        shebang = cli.read_bytes().splitlines()[0].decode("utf-8")
        require(shebang == "#!" + str(python), "console wrapper does not use the expected venv interpreter")
        require(os.access(cli, os.X_OK), "console wrapper is not executable")
        wrapper["interpreter_readback"] = shebang
    probe = recorder.command(label + ": installed provenance", [python, "-I", "-B", ROOT / "scripts/probe_installed.py",
        envroot, ROOT / "fixtures/source", run / "rejected-source", run / "verified-source"], consumer)
    readback = json.loads(probe.stdout)
    expected_files = {Path(m["path"]).name: m["sha256"] for m in audit["members"] if m["path"].startswith("packet_stamp/")}
    for name in ("__init__.py", "cli.py", "formats.json"):
        require(readback["installed_package_sha256"][name] == expected_files.get(name), "installed bytes mismatch: " + name)
    require(not Path(readback["cwd"]).is_relative_to(ROOT / "fixtures/source"), "consumer is inside original source")
    help_result = recorder.command(label + ": public help", [cli, "--help"], consumer)
    require("--style" in help_result.stdout, "help did not expose style option")
    version = recorder.command(label + ": public version", [cli, "--version"], consumer)
    require(version.stdout == "0.3.0\n", "public version mismatch")
    result = recorder.command(label + ": data-dependent public command", [cli, "--style", "priority", "Ada"],
                              consumer, expected=0 if data_expected else 2)
    if data_expected:
        require(result.stdout == "PRIORITY: Ada\n" and result.stderr == "", "wrong installed label output")
        unicode_result = recorder.command(label + ": UTF-8 name", [cli, "Zoë"], consumer)
        require(unicode_result.stdout == "TO: Zoë\n", "wrong UTF-8 label output")
        invalid = recorder.command(label + ": invalid style", [cli, "--style", "unknown", "Ada"], consumer, expected=2)
        require("invalid choice" in invalid.stderr and invalid.stdout == "", "invalid option was not rejected")
    else:
        require(result.stdout == "" and result.stderr == "packet-stamp: required bundled data formats.json is missing\n",
                "failure did not demonstrate missing bundled data")
    readback.update({"installed_artifact_sha256": audit["sha256"], "packaging_contract": "pass" if data_expected else "fail",
                     "installation": "pass", "runtime_contract": "pass" if data_expected else "fail",
                     "public_wrapper": wrapper,
                     "public_output": result.stdout, "public_error": result.stderr, "public_exit_code": result.returncode})
    write_json(output / (label + "-readback.json"), recorder.portable(readback))
    return recorder.portable(readback)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path, help="new directory; existing paths are refused")
    parser.add_argument("--verify-bundled", action="store_true", help="recheck shipped wheel bytes; do not rebuild source")
    args = parser.parse_args()
    require(sys.version_info >= (3, 10), "Python 3.10+ required")
    for tool in ("pip",) if args.verify_bundled else ("pip", "setuptools", "wheel"):
        metadata.version(tool)  # Missing prerequisites stop here; no install fallback.
    output = args.output.resolve()
    require(not output.is_relative_to(ROOT), "output must be outside the skill and source checkout")
    output.mkdir(parents=True, exist_ok=False)
    inputs = source_manifest()
    summary = {"fictional": True, "mode": "bundled-readback" if args.verify_bundled else "fresh-build",
               "observed_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
               "platform": sys.platform, "machine": platform.machine(),
               "build_tools": {name: metadata.version(name) for name in ("pip", "setuptools", "wheel")
                               if not args.verify_bundled or name == "pip"},
               "helper_sha256": {p.name: sha(p.read_bytes()) for p in sorted((ROOT / "scripts").glob("*.py"))},
               "source_before": inputs, "artifacts": {}, "results": {}}
    with tempfile.TemporaryDirectory(prefix="packet-stamp-check-") as temporary:
        run = Path(temporary).resolve()
        recorder = Recorder(output, run)
        recorder.env["TMPDIR"] = str(run)
        summary["environment_overrides"] = recorder.portable(recorder.env)
        for label, data_expected in (("rejected", False), ("verified", True)):
            destination = output / label
            destination.mkdir()
            wheel = destination / WHEEL_NAME
            if args.verify_bundled:
                index = json.loads((ROOT / "artifacts/manifest.json").read_text(encoding="utf-8"))
                original = ROOT / "artifacts" / label / WHEEL_NAME
                expected = index["artifacts"][label]
                require(original.stat().st_size == expected["bytes"] and sha(original.read_bytes()) == expected["sha256"],
                        "bundled artifact identity mismatch: " + label)
                shutil.copyfile(original, wheel)
            else:
                source = run / (label + "-source")
                shutil.copytree(ROOT / "fixtures/source", source)
                if data_expected:
                    repair = (ROOT / "fixtures/package-data-repair.toml").read_bytes()
                    with (source / "pyproject.toml").open("ab") as stream:
                        stream.write(b"\n" + repair)
                # Source smoke is separate evidence. Its explicit import path is NOT used below.
                baseline = recorder.command(label + ": source smoke (not artifact proof)", [sys.executable, "-I", "-B", "-c",
                    "import sys; sys.path.insert(0, sys.argv.pop(1)); from packet_stamp.cli import main; raise SystemExit(main())",
                    source / "src", "--style", "priority", "Ada"], source)
                require(baseline.stdout == "PRIORITY: Ada\n", "source fixture baseline failed")
                recorder.command(label + ": build wheel", [sys.executable, "-I", "-m", "pip", "--isolated", "wheel",
                    "--no-index", "--no-deps", "--no-build-isolation", "--no-cache-dir", "--disable-pip-version-check",
                    "--wheel-dir", destination, source], run)
                require(sorted(p.name for p in destination.iterdir()) == [WHEEL_NAME], "unexpected build artifacts")
            audit = inspect_wheel(wheel, data_expected)
            summary["artifacts"][label] = audit
            write_json(output / (label + "-contents.json"), audit)
            summary["results"][label] = exercise(wheel, audit, output, run, recorder, label, data_expected)
        require(summary["artifacts"]["rejected"]["sha256"] != summary["artifacts"]["verified"]["sha256"],
                "packaging repair did not change artifact bytes")
        summary["source_after"] = source_manifest()
        require(summary["source_after"] == inputs, "original input changed")
        summary["inputs_preserved"] = True
        summary["status"] = "expected omitted-data defect observed; corrected artifact passed bounded checks"
        write_json(output / "manifest.json", summary)
    print(json.dumps({"status": summary["status"], "artifacts": {
        label: {k: audit[k] for k in ("filename", "bytes", "sha256", "version")}
        for label, audit in summary["artifacts"].items()}}, indent=2))


if __name__ == "__main__":
    main()
