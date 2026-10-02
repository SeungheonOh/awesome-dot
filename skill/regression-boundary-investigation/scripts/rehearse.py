#!/usr/bin/env python3
"""Generate and investigate only the original local room-slot fixture.

Usage: python3 scripts/rehearse.py NEW_DIRECTORY
The directory must not exist. No existing repository is accepted as input.
There is no cleanup, download, installation, real remote, or shell execution.
"""
import argparse
from datetime import datetime, timezone
import difflib
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


GOOD = '''def is_available(bookings, start, end):
    """Queries and bookings are half-open intervals; touching is allowed."""
    if end <= start:
        raise ValueError("the query needs positive duration")
    return not any(start < booked_end and booked_start < end
                   for booked_start, booked_end in bookings)
'''
REFACTORED = GOOD.replace("in bookings)", "in sorted(bookings))")
BAD = REFACTORED.replace("start < booked_end and booked_start < end", "start <= booked_end and booked_start <= end")
UNAVAILABLE = REFACTORED.replace("def is_available(", "def has_open_slot(")
UNSTABLE = '''import os

def is_available(bookings, start, end):
    if end <= start:
        raise ValueError("the query needs positive duration")
    if os.environ.get("BOOKING_POLICY") == "legacy":
        return not any(start <= booked_end and booked_start <= end
                       for booked_start, booked_end in bookings)
    return not any(start < booked_end and booked_start < end
                   for booked_start, booked_end in bookings)
'''


def digest(data):
    return hashlib.sha256(data).hexdigest()


def dump(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    root = args.directory.resolve()
    root.mkdir(parents=False, exist_ok=False)
    evidence = root / "artifacts"
    evidence.mkdir()
    empty = root / "empty-hooks-and-template"
    empty.mkdir()
    source = root / "original"
    source.mkdir()
    predicate = Path(__file__).resolve().with_name("predicate.py")
    env = {"PATH": os.environ.get("PATH", os.defpath), "LC_ALL": "C", "TZ": "UTC",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_OPTIONAL_LOCKS": "0", "GIT_TERMINAL_PROMPT": "0"}
    command_log = []

    def portable(value):
        return str(value).replace(str(root), "<fixture>").replace(str(predicate.parent.parent), "<skill>").replace(sys.executable, "<python>")

    def run(command, cwd, allowed=(0,), extra=None):
        result = subprocess.run([str(arg) for arg in command], cwd=cwd,
                                env=dict(env, **(extra or {})), text=True,
                                capture_output=True, timeout=30)
        command_log.append({"cwd": portable(cwd), "argv": [portable(arg) for arg in command],
                            "exit": result.returncode})
        if result.returncode not in allowed:
            raise RuntimeError(portable(result.stderr or result.stdout))
        return result

    def git(cwd, *arguments, allowed=(0,), extra=None):
        return run(["git", "--no-optional-locks", "-c", "core.hooksPath=" + str(empty),
                    "-c", "commit.gpgSign=false", "-c", "core.autocrlf=false",
                    *arguments], cwd, allowed, extra)

    git(source, "init", "--object-format=sha1", "--template=" + str(empty), "-b", "fixture-main")
    git(source, "config", "user.name", "Fixture")
    git(source, "config", "user.email", "fixture@example.invalid")
    commits = {}
    serial = 0

    def commit(label, message, files):
        nonlocal serial
        for name, content in files.items():
            (source / name).write_text(content, encoding="utf-8")
        git(source, "add", "--", *files)
        stamp = f"2025-01-01T00:{serial:02d}:00+00:00"
        serial += 1
        git(source, "commit", "-q", "-m", message,
            extra={"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp})
        commits[label] = git(source, "rev-parse", "HEAD").stdout.strip()
        return commits[label]

    commit("M0", "Define half-open room availability", {"slots.py": GOOD,
           "README.md": "Room-slot fixture: touching bookings are allowed.\n",
           ".gitignore": "*.cache\n", "draft.txt": "base draft\n",
           "scratchpad.txt": "base scratchpad\n", "merge-note.txt": "base note\n"})
    commit("M1", "Document integer slot coordinates", {"README.md": "Integer room-slot coordinates; intervals are half-open.\n"})
    commit("M2", "Sort bookings before checking overlap", {"slots.py": REFACTORED})
    commit("M3", "Consolidate contact checks", {"slots.py": BAD})
    commit("M4", "Document the reservation adapter", {"README.md": "The adapter consumes room-slot availability.\n"})
    commit("M5", "Add module usage note", {"slots.py": BAD + "\n# Called by the room-reservation adapter.\n"})

    git(source, "switch", "-c", "fixture-gap", commits["M2"])
    commit("S3", "Rename availability interface during migration", {"slots.py": UNAVAILABLE})
    commit("S4", "Restore API with compatibility-dependent contacts", {"slots.py": UNSTABLE})
    commit("S5", "Use one contact rule in both modes", {"slots.py": BAD})
    commit("S6", "Document migration state", {"README.md": "Availability interface migration notes.\n"})

    git(source, "switch", "-c", "fixture-return", commits["M0"])
    commit("N1", "Use inclusive contact checks", {"slots.py": BAD})
    commit("N2", "Restore half-open contact checks", {"slots.py": REFACTORED})
    for number in range(3, 7):
        commit(f"N{number}", f"Add adapter note {number}", {"README.md": f"Adapter note {number}; touching remains allowed.\n"})
    commit("N7", "Reintroduce inclusive contact checks", {"slots.py": BAD})
    commit("N8", "Record adapter deployment notes", {"README.md": "Local fixture adapter notes.\n"})

    # Create a real interrupted merge, then coexist with other work. Only this
    # newly generated fixture is ever manipulated by the setup.
    git(source, "switch", "-c", "preserve-right", commits["M5"])
    commit("P-right", "Write right planning note", {"merge-note.txt": "right planning note\n"})
    git(source, "switch", "-c", "preserve-left", commits["M5"])
    commit("P-left", "Write left planning note", {"merge-note.txt": "left planning note\n"})
    merged = git(source, "merge", "--no-commit", "preserve-right", allowed=(1,))
    assert "CONFLICT" in merged.stdout and (source / ".git/MERGE_HEAD").exists()
    (source / "draft.txt").write_text("staged draft\n", encoding="utf-8")
    git(source, "add", "--", "draft.txt")
    (source / "draft.txt").write_text("staged draft\nunstaged continuation\n", encoding="utf-8")
    (source / "scratchpad.txt").write_text("unstaged experiment\n", encoding="utf-8")
    (source / "ideas.txt").write_text("untracked idea\n", encoding="utf-8")
    (source / "scratch.cache").write_text("ignored local state\n", encoding="utf-8")

    def snapshot():
        files = {}
        for path in sorted(source.rglob("*")):
            if path.is_file():
                files[path.relative_to(source).as_posix()] = {
                    "sha256": digest(path.read_bytes()), "mode": stat.S_IMODE(path.stat().st_mode)}
        return {"files": files,
                "head": git(source, "rev-parse", "HEAD").stdout.strip(),
                "branch": git(source, "symbolic-ref", "--short", "HEAD").stdout.strip(),
                "status": git(source, "status", "--porcelain=v1", "--untracked-files=all", "--ignored").stdout,
                "staged_diff_sha256": digest(git(source, "diff", "--cached", "--binary").stdout.encode()),
                "unstaged_diff_sha256": digest(git(source, "diff", "--binary").stdout.encode())}

    before = snapshot()
    dump(evidence / "original-before.json", before)
    checks = evidence / "checks.jsonl"

    def clone(name, revision):
        target = root / name
        git(root, "clone", "--quiet", "--no-hardlinks", "--no-checkout",
            "--template=" + str(empty), str(source), str(target))
        git(target, "checkout", "--quiet", "--detach", revision)
        assert not git(target, "status", "--porcelain").stdout
        return target

    def check(target, label):
        result = run([sys.executable, "-I", "-B", str(predicate), "--record", str(checks),
                      "--label", label], target, (0, 1, 125, 128))
        return result.returncode

    searches = {}

    def bisect(name, good_label, bad_label):
        target = clone(name, commits[bad_label])
        good, bad = commits[good_label], commits[bad_label]
        git(target, "checkout", "--quiet", "--detach", good)
        assert check(target, name + ":endpoint-good") == 0
        git(target, "checkout", "--quiet", "--detach", bad)
        assert check(target, name + ":endpoint-bad") == 1
        git(target, "bisect", "start", bad, good)
        outcome = git(target, "bisect", "run", sys.executable, "-I", "-B", str(predicate),
                      "--record", str(checks), "--label", name + ":bisect", allowed=(0, 1, 2))
        (evidence / (name + "-bisect.txt")).write_text(portable(outcome.stdout + outcome.stderr), encoding="utf-8")
        (evidence / (name + "-bisect.log")).write_text(git(target, "bisect", "log").stdout, encoding="utf-8")
        bad_ref = git(target, "rev-parse", "refs/bisect/bad").stdout.strip()
        result = {"good": good, "bad": bad, "bisect_exit": outcome.returncode,
                  "bad_ref": bad_ref, "unique": "is the first bad commit" in outcome.stdout}
        # Save evidence first. This reset is the bisect subcommand, only in the
        # independent clone; it does not mean git reset --hard on original work.
        git(target, "bisect", "reset")
        result["restored_head"] = git(target, "rev-parse", "HEAD").stdout.strip()
        assert result["restored_head"] == bad
        assert not (target / ".git/BISECT_START").exists()
        searches[name] = result
        return target

    monotonic = bisect("monotonic", "M0", "M5")
    assert searches["monotonic"]["unique"] and searches["monotonic"]["bad_ref"] == commits["M3"]
    for label, expected in [("M2", 0), ("M3", 1), ("M4", 1)]:
        git(monotonic, "checkout", "--quiet", "--detach", commits[label])
        assert check(monotonic, "neighbor:" + label) == expected

    gap = bisect("gap", "M0", "S6")
    assert not searches["gap"]["unique"]
    for label, expected in [("M2", 0), ("S3", 125), ("S4", 125), ("S5", 1), ("S6", 1)]:
        git(gap, "checkout", "--quiet", "--detach", commits[label])
        assert check(gap, "gap-audit:" + label) == expected

    returning = bisect("returning", "M0", "N8")
    full_scan = []
    for label in ["M0", *[f"N{number}" for number in range(1, 9)]]:
        git(returning, "checkout", "--quiet", "--detach", commits[label])
        code = check(returning, "ordered-audit:" + label)
        full_scan.append({"label": label, "revision": commits[label], "exit": code})
    assert [row["exit"] for row in full_scan] == [0, 1, 0, 0, 0, 0, 0, 1, 1]
    assert searches["returning"]["unique"] and searches["returning"]["bad_ref"] == commits["N7"]

    # Controlled explanation in fresh copies. Replacing one relation repairs
    # the candidate; reversing that relation reproduces the failure in its parent.
    repair = clone("control-repair", commits["M3"])
    original_bytes = (repair / "slots.py").read_bytes()
    (repair / "slots.py").write_text(REFACTORED, encoding="utf-8")
    assert check(repair, "control:candidate-only-relation-repaired") == 0
    (repair / "slots.py").write_bytes(original_bytes)
    assert check(repair, "control:candidate-restored") == 1
    introduce = clone("control-introduce", commits["M2"])
    (introduce / "slots.py").write_text(BAD, encoding="utf-8")
    assert check(introduce, "control:parent-only-relation-introduced") == 1
    (evidence / "explanation.patch").write_text("".join(difflib.unified_diff(
        BAD.splitlines(True), REFACTORED.splitlines(True), fromfile="a/slots.py", tofile="b/slots.py")), encoding="utf-8")

    after = snapshot()
    dump(evidence / "original-after.json", after)
    assert before == after, "original work changed"
    dump(evidence / "history.json", {"commits": commits, "returning_ordered_audit": full_scan})
    (evidence / "commit-graph.txt").write_text(git(source, "log", "--all", "--graph", "--format=%h %s").stdout, encoding="utf-8")
    records = [json.loads(line) for line in checks.read_text().splitlines()]
    summary = {"verified_at": datetime.now(timezone.utc).isoformat(),
               "tools": {"git": git(source, "--version").stdout.strip(), "python": sys.version.split()[0]},
               "searches": searches, "predicate_invocations": len(records),
               "attempts": sum(len(row["attempts"]) for row in records),
               "cases_per_evaluated_attempt": 10, "original_snapshot_equal": before == after,
               "preserved_file_count_including_git": len(before["files"]),
               "original_merge_still_in_progress": (source / ".git/MERGE_HEAD").is_file(),
               "input_hashes": {name: digest((predicate.parent / name).read_bytes())
                                for name in ("predicate.py", "rehearse.py")},
               "scope": "Original synthetic repositories only; no network, dependencies, remote services, or real project execution."}
    dump(evidence / "summary.json", summary)
    dump(evidence / "commands.json", command_log)
    dump(evidence / "sha256.json", {path.name: digest(path.read_bytes()) for path in sorted(evidence.iterdir()) if path.is_file()})
    print(json.dumps({"outcome": "verified", "predicate_invocations": len(records),
                      "original_preserved": before == after, "artifacts": "artifacts/"}, sort_keys=True))


if __name__ == "__main__":
    main()
