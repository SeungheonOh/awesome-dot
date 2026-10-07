#!/usr/bin/env python3
"""Run local source/fixture checks only; no installs, model calls, or skill helpers."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parent
# These exact links are in the two byte-pinned text-merge guides. Neighboring
# workflows are deliberately outside each study's designated package allowlist;
# see packages/README.md and studies/repeated-stress-2026-10-06/guides/README.md.
# The engineering triage guide also omits its pinned WORKED_EXAMPLE.md; the
# study README records its public URL and Git blob. This exact source/target
# exception does not add the example to the frozen trial inputs.
# Keep the pinned source bytes and check every other local link normally.
OMITTED_PACKAGE_LINKS = {
    ("studies/engineering-artifacts-2026-10-07/fixture/sources/bug-reproduction-triage.md", "WORKED_EXAMPLE.md"),
    ("packages/skill/build-text-merge-component/SKILL.md", "../parallel-change-integration/SKILL.md"),
    ("packages/skill/build-text-merge-component/SKILL.md", "../verify-exact-text-patches/SKILL.md"),
    ("packages/skill/build-text-merge-component/SKILL.md", "../implement-scoped-change/SKILL.md"),
    ("studies/repeated-stress-2026-10-06/guides/skill/build-text-merge-component/SKILL.md", "../parallel-change-integration/SKILL.md"),
    ("studies/repeated-stress-2026-10-06/guides/skill/build-text-merge-component/SKILL.md", "../document-revision-reconciliation/SKILL.md"),
    ("studies/repeated-stress-2026-10-06/guides/skill/build-text-merge-component/SKILL.md", "../verify-exact-text-patches/SKILL.md"),
    ("studies/repeated-stress-2026-10-06/guides/skill/build-text-merge-component/SKILL.md", "../implement-scoped-change/SKILL.md"),
}


# Frozen task-routing entry points retain links to deliberately omitted context.
# Each exact pair and pinned original URL is listed in
# contracts/task-routing/provenance/omitted-links.json. No linked content is
# added to the ten-candidate boundary or to the prospective input recipe.
TASK_ROUTING_OMITTED_LINKS = {
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'example.md'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'fixtures/source-inventory.csv'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'fixtures/source-control.json'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'scripts/audit.py'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'outputs/partial/report.md'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'outputs/resolved/report.md'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'outputs/incomplete-control/report.md'),
    ('contracts/task-routing/sources/skill/account-export-audit/SKILL.md', 'verification.md'),
    ('contracts/task-routing/sources/skill/backup-restore-spot-check/SKILL.md', 'worked-example.md'),
    ('contracts/task-routing/sources/skill/code-review-handoff/SKILL.md', 'WORKED_EXAMPLE.md'),
    ('contracts/task-routing/sources/skill/document-export-check/SKILL.md', 'example.md'),
    ('contracts/task-routing/sources/skill/document-export-check/SKILL.md', 'approved-source.docx'),
    ('contracts/task-routing/sources/skill/document-export-check/SKILL.md', 'release-delivery.pdf'),
    ('contracts/task-routing/sources/skill/document-export-check/SKILL.md', 'check_example.py'),
    ('contracts/task-routing/sources/skill/document-export-check/SKILL.md', 'verification.md'),
    ('contracts/task-routing/sources/skill/failing-build-repair/SKILL.md', 'EXAMPLE.md'),
    ('contracts/task-routing/sources/skill/failing-build-repair/SKILL.md', 'REHEARSAL.md'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'example.md'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'fixtures/import-contract.json'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'fixtures/source.csv'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'fixtures/target-before.json'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'fixtures/partial-result.json'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'scripts/rehearse.py'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'verification.md'),
    ('contracts/task-routing/sources/skill/service-import-rehearsal/SKILL.md', 'local-target-roundtrip.md'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'room-enquiry-blank.pdf'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'room-enquiry-draft.pdf'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'preview.png'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'source-brief.md'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'field-map.json'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'verification.md'),
    ('contracts/task-routing/sources/skill/source-backed-form-fill/SKILL.md', 'example.py'),
    ('contracts/task-routing/sources/skill/task-to-skill-router/SKILL.md', 'examples.md'),
    ('contracts/task-routing/sources/skill/task-to-skill-router/SKILL.md', 'remote-discovery-rehearsal.md'),
}
OMITTED_PACKAGE_LINKS |= TASK_ROUTING_OMITTED_LINKS


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def regular_file(path):
    if not path.is_file() or path.is_symlink():
        raise ValueError(f"Expected regular source file: {path.relative_to(ROOT)}")
    return path.read_bytes()


def check_manifests():
    packages = json.loads((ROOT / "packages/manifest.json").read_text())
    total = 0
    for entry in packages["files"]:
        raw = regular_file(ROOT / entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["bytes"]:
            raise ValueError("Pinned package changed: " + entry["path"])
        blob = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
        if blob != entry["git_blob_sha"]:
            raise ValueError("Git blob identity differs: " + entry["path"])
        total += len(raw)
    if len(packages["files"]) != packages["file_count"] or total != packages["total_bytes"]:
        raise ValueError("Package manifest totals differ")
    packets = json.loads((ROOT / "cases/manifest.json").read_text())
    count = 0
    for packet in packets["packets"]:
        base = ROOT / packet["root"]
        expected = {entry["path"] for entry in packet["files"]}
        actual = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
        if actual != expected:
            raise ValueError("Case file allowlist differs: " + packet["case_id"])
        for entry in packet["files"]:
            raw = regular_file(base / entry["path"])
            if sha256(raw) != entry["sha256"] or len(raw) != entry["bytes"]:
                raise ValueError(f"Case bytes changed: {packet['case_id']}/{entry['path']}")
            count += 1
    print(f"Source manifests: {count} case files; {len(packages['files'])} package files ({total} bytes)", flush=True)


def heading_anchors(path):
    anchors = set()
    counts = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)(?:\s+#+)?$", line)
        if not match:
            continue
        title = re.sub(r"[`*_]", "", match.group(1)).strip().lower()
        anchor = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        count = counts.get(anchor, 0)
        counts[anchor] = count + 1
        anchors.add(anchor if count == 0 else f"{anchor}-{count}")
    return anchors


def check_links():
    checked = 0
    exceptions = set()
    for source in ROOT.rglob("*.md"):
        text = source.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", text):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            destination = (source.parent / unquote(parsed.path)).resolve() if parsed.path else source
            pair = (source.relative_to(ROOT).as_posix(), target)
            if pair in OMITTED_PACKAGE_LINKS:
                exceptions.add(pair)
                continue
            if not destination.exists():
                raise ValueError(f"Broken local link: {source.relative_to(ROOT)} -> {target}")
            if parsed.fragment and destination.suffix == ".md":
                if unquote(parsed.fragment) not in heading_anchors(destination):
                    raise ValueError(f"Broken heading link: {source.relative_to(ROOT)} -> {target}")
            checked += 1
    if exceptions != OMITTED_PACKAGE_LINKS:
        raise ValueError("Pinned package cross-link exceptions changed; review the package manifest")
    print(f"Documentation links: {checked} checked; {len(exceptions)} explicitly omitted pinned destinations", flush=True)


def run(command, cwd, env):
    subprocess.run([sys.executable, "-B", *command], cwd=cwd, env=env,
                   check=True, timeout=120)


def main():
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPATH"] = str(ROOT / "harness")
    check_manifests()
    check_links()
    run(["-m", "dot_eval", "inspect-config", "pilot-source-config.json"], ROOT, env)
    print("\nHarness fixtures", flush=True)
    run(["-m", "unittest", "discover", "-s", "tests", "-v"], ROOT / "harness", env)
    for number in range(1, 9):
        print(f"\nF{number} grader fixtures", flush=True)
        pattern = "checks.py" if number == 4 else "test*.py"
        run(["-m", "unittest", "discover", "-s", ".", "-p", pattern, "-v"],
            ROOT / "evaluators" / f"F{number}", env)
    print("\nLocal checks passed. This check made no model calls; sealed-pilot live dispatch remains disabled.", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        print(f"Check failed: {error}", file=sys.stderr)
        raise SystemExit(1)
