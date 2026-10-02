#!/usr/bin/env python3
"""Reproduce only the adjacent fictional plain-file handoff; never run payloads.

The JSON source preserves otherwise conflicting logical filenames without making
this skill's own checkout depend on a case-sensitive filesystem. This is a small
fixture reproducer, not an arbitrary archive extractor or full Markdown parser.
"""
import argparse
import hashlib
import json
import platform
import posixpath
import re
import shutil
import stat
import subprocess
import zipfile
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 2 * 1024 * 1024
LINK = re.compile(r"\[([^\]\n]*)\]\(([^)\s]+)\)")
RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9¹²³]|LPT[1-9¹²³])(?:\.|$)", re.I)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, ensure_ascii=False) + "\n").encode("utf-8")


def relative_name(name):
    require(isinstance(name, str) and bool(name), "Missing relative name")
    require(not name.startswith("/") and "\\" not in name, "Expected relative POSIX-style name")
    require(all(p not in ("", ".", "..") for p in name.split("/")), "Non-canonical path")


def windows_screen(names, base):
    """Conservative ASCII fixture screen; not an OS filesystem emulation."""
    issues, occupied = [], {}
    for name in sorted(names):
        relative_name(name)
        components = name.split("/")
        for i, part in enumerate(components):
            prefix = "/".join(components[:i + 1])
            kind = "file" if i == len(components) - 1 else "directory"
            key = prefix.casefold()
            observed = (prefix, kind)
            if key in occupied and occupied[key] != observed:
                issue = "case/type collision: " + occupied[key][0] + " <> " + prefix
                if issue not in issues:
                    issues.append(issue)
            occupied[key] = observed
            if any(c in '<>:"|?*' or ord(c) < 32 for c in part):
                issues.append("Windows-incompatible component: " + prefix)
            if part.endswith((" ", ".")) or RESERVED.match(part):
                issues.append("Windows shell/reserved-name conflict: " + prefix)
            if not part.isascii():
                issues.append("outside this ASCII fixture screen: " + prefix)
        if len(base.rstrip("\\") + "\\" + name.replace("/", "\\")) > 240:
            issues.append("exceeds this fixture's conservative 240-character path budget: " + name)
    return sorted(set(issues))


def link_graph(files):
    edges = []
    for name, data in sorted(files.items()):
        if not name.endswith(".md"):
            continue
        text = data.decode("utf-8")
        for ordinal, match in enumerate(LINK.finditer(text), start=1):
            url = urlsplit(match.group(2))
            require(not url.scheme and not url.netloc and not url.query and not url.fragment,
                    "Fixture supports only simple relative file links")
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), unquote(url.path)))
            require(target in files, "Missing selected dependency: " + name + " -> " + target)
            edges.append((name, ordinal, match.group(1), target))
    return sorted(edges)


def build_payload(bundle, plan):
    rows = bundle["files"]
    require(all(type(r["selected"]) is bool for r in rows), "Explicit selection required")
    originals = {r["path"]: r["text"].encode("utf-8") for r in rows}
    require(len(originals) == len(rows), "Duplicate original path")
    for name in originals:
        relative_name(name)
    selected = {r["path"]: originals[r["path"]] for r in rows if r["selected"]}
    mapping = {r["source"]: r["destination"] for r in plan["rows"]}
    require(len(mapping) == len(plan["rows"]), "Duplicate mapping source")
    require(set(mapping) == set(selected), "Map does not cover exactly the selected files")
    require(len(set(mapping.values())) == len(mapping), "Duplicate destination")
    root = plan["package_root"]
    relative_name(root)
    require("/" not in root, "Use one package root folder")
    require(plan["generated_members"] == ["MANIFEST.json", "HANDOFF.txt"],
            "This fixture requires its exact two declared support members")
    all_destinations = list(mapping.values()) + plan["generated_members"]
    require(len(set(all_destinations)) == len(all_destinations), "Generated-member collision")
    output_issues = windows_screen([root + "/" + n for n in all_destinations], plan["target_extraction_base"])
    require(not output_issues, "Destination naming screen failed: " + str(output_issues))
    before_links = link_graph(selected)
    files, records = {}, []
    for row in plan["rows"]:
        source, destination = row["source"], row["destination"]
        text = selected[source].decode("utf-8")
        for edit in row["replacements"]:
            require(edit["count"] > 0 and text.count(edit["old"]) == edit["count"],
                    "Reviewed reference occurrence changed: " + source)
            text = text.replace(edit["old"], edit["new"])
        output = text.encode("utf-8")
        files[destination] = output
        records.append({
            "source": source, "destination": destination,
            "source_bytes": len(selected[source]), "source_sha256": sha(selected[source]),
            "package_bytes": len(output), "package_sha256": sha(output),
            "byte_identical": output == selected[source],
            "approved_reference_changes": row["replacements"],
        })
    after_links = link_graph(files)
    expected_links = sorted((mapping[source], ordinal, label, mapping[target])
                            for source, ordinal, label, target in before_links)
    require(after_links == expected_links, "A reference changed its logical target")
    manifest = {
        "fictional": True, "recipient": plan["recipient"], "target": plan["target"],
        "source_count": len(originals), "selected_count": len(selected),
        "excluded": [{"path": r["path"], "reason": r["reason"]} for r in rows if not r["selected"]],
        "generated_members": plan["generated_members"], "records": records,
        "relative_links": [{"from": a, "ordinal": ordinal, "label": label, "to": b}
                           for a, ordinal, label, b in after_links],
        "metadata_policy": plan["metadata_policy"],
    }
    files["MANIFEST.json"] = encoded(manifest)
    files["HANDOFF.txt"] = (
        "Maple client help: fictional documentation handoff for Rowan Alder\n"
        "Extract the whole Maple-client-help folder into a new empty location.\n"
        "Keep its internal folders together. Open Start here.md as UTF-8 text.\n"
        "A compatible Markdown viewer may make the relative links clickable.\n"
        "Both setup and troubleshooting guides remain distinct.\n"
        "This is a help-document bundle; the fictional client is not included.\n"
        "MANIFEST.json records the original names and the approved copy changes.\n"
        "Prepared locally only. Windows extraction and viewer behavior are untested.\n"
    ).encode("utf-8")
    return files, manifest, windows_screen(selected, plan["target_extraction_base"])


def inventory(folder):
    result = {}
    for path in sorted(folder.rglob("*")):
        require(not path.is_symlink(), "Unexpected linked path in readback")
        if path.is_file():
            result[path.relative_to(folder).as_posix()] = path.read_bytes()
        else:
            require(path.is_dir(), "Unexpected special file in readback")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path, help="New, absent output folder")
    parser.add_argument("--native-unzip", action="store_true", help="Use installed Info-ZIP unzip for readback")
    args = parser.parse_args()
    source_path, map_path = [ROOT / "fixtures" / name for name in ("source-bundle.json", "reviewed-map.json")]
    before = {p.name: p.read_bytes() for p in (source_path, map_path)}
    bundle, plan = [json.loads(before[p.name]) for p in (source_path, map_path)]
    files, manifest, original_issues = build_payload(bundle, plan)
    require(sum(map(len, files.values())) <= LIMIT, "Fixture expanded content exceeds 2 MiB")
    unzip = shutil.which("unzip") if args.native_unzip else None
    require(not args.native_unzip or unzip is not None, "Requested native unzip is unavailable")
    args.out.mkdir(parents=False, exist_ok=False)
    prepared = args.out / "prepared" / plan["package_root"]
    for name, data in sorted(files.items()):
        target = prepared / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
    require(inventory(prepared) == files, "Prepared-copy readback differs")
    archive = args.out / "maple-client-help.zip"
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_STORED) as package:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(plan["package_root"] + "/" + name, (2026, 10, 1, 12, 0, 0))
            info.create_system = 3
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            package.writestr(info, data)
    require(archive.stat().st_size <= LIMIT, "ZIP exceeds 2 MiB")
    expected_members = {plan["package_root"] + "/" + n: d for n, d in files.items()}
    with zipfile.ZipFile(archive) as package:
        require(len(package.infolist()) == len(expected_members), "Archive member count differs")
        require(set(package.namelist()) == set(expected_members), "Archive selection differs")
        require(not package.comment and package.testzip() is None, "ZIP read check failed")
        for item in package.infolist():
            require(stat.S_ISREG(item.external_attr >> 16), "Expected ordinary regular member")
            require(not item.extra and not item.comment, "Unexpected archive metadata")
            require(package.read(item) == expected_members[item.filename], "Archive bytes differ")
    extracted = args.out / "extracted"
    extracted.mkdir()
    if unzip:
        version = subprocess.run([unzip, "-v"], check=True, text=True, capture_output=True).stdout.splitlines()[0]
        subprocess.run([unzip, "-q", str(archive.resolve()), "-d", str(extracted.resolve())],
                       check=True, text=True, capture_output=True)
        method = {"method": "installed native unzip", "tool": version, "exit_code": 0}
    else:
        # Only extract the exact archive just created and checked above.
        with zipfile.ZipFile(archive) as package:
            package.extractall(extracted)
        method = {"method": "Python standard-library extraction", "native_tool": False}
    recovered = inventory(extracted)
    require(recovered == expected_members, "Extracted membership or bytes differ")
    project = {n: recovered[plan["package_root"] + "/" + n] for n in files}
    selected_destinations = {r["destination"] for r in manifest["records"]}
    recovered_links = link_graph({n: d for n, d in project.items() if n in selected_destinations})
    require(recovered_links == [(r["from"], r["ordinal"], r["label"], r["to"])
                                for r in manifest["relative_links"]], "Readback links differ")
    for data in recovered.values():
        data.decode("utf-8")
    require(all(p.read_bytes() == before[p.name] for p in (source_path, map_path)), "Fixture input changed during run")
    report = {
        "observed_platform": platform.system(), "python": platform.python_version(),
        "archive": {"name": archive.name, "bytes": archive.stat().st_size, "sha256": sha(archive.read_bytes()),
                    "members": len(expected_members), "expanded_bytes": sum(map(len, files.values()))},
        "inputs": {name: {"bytes": len(data), "sha256": sha(data), "unchanged": True} for name, data in before.items()},
        "counts": {"source": len(bundle["files"]), "selected": len(selected_destinations),
                   "excluded": len(manifest["excluded"]), "generated": len(files) - len(selected_destinations),
                   "source_byte_identical": sum(r["byte_identical"] for r in manifest["records"]),
                   "reference_edited": sum(not r["byte_identical"] for r in manifest["records"]),
                   "relative_links_resolved": len(recovered_links)},
        "source_naming_findings": original_issues, "destination_naming_findings": [],
        "native_or_library_readback": method, "all_extracted_members_exact": True,
        "all_extracted_members_utf8_readable": True,
        "target_windows_extraction": "not tested", "target_viewer_behavior": "not tested",
        "sent_or_uploaded": False,
    }
    for name, value in (("manifest.json", manifest), ("readback.json", report)):
        with (args.out / name).open("xb") as handle:
            handle.write(encoded(value))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
