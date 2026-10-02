"""Rehearse only the supplied fictional queue fixture, using Git and Python.

Usage: python scripts/rehearse.py /path/to/a-new-empty-run-directory
The destination must not exist. Existing checkouts are never accepted as input.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


FIXTURES = Path(__file__).resolve().parents[1] / "fixtures"
COMMAND = "python -B -m unittest -v"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    root = Path(sys.argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=False)
    artifacts = root / "artifacts"
    artifacts.mkdir()
    empty = root / "empty-config-and-hooks"
    empty.mkdir()
    config = root / "gitconfig"
    config.write_text("")
    env = os.environ.copy()
    # Prevent inherited repository selectors and command-injected config from
    # directing a fixture command at an unrelated checkout.
    for key in list(env):
        if key.startswith("GIT_"):
            del env[key]
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": str(config),
        "GIT_ATTR_NOSYSTEM": "1", "GIT_OPTIONAL_LOCKS": "0",
        "GIT_AUTHOR_NAME": "Queue Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
        "GIT_COMMITTER_NAME": "Queue Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
        "GIT_AUTHOR_DATE": "2026-01-15T12:00:00+0000",
        "GIT_COMMITTER_DATE": "2026-01-15T12:00:00+0000",
        "GIT_TERMINAL_PROMPT": "0", "LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1",
    })
    git_prefix = [
        "git", "-c", f"core.hooksPath={empty}", "-c", "commit.gpgSign=false",
        "-c", "tag.gpgSign=false", "-c", "gc.auto=0", "-c", "maintenance.auto=false",
        "-c", "rerere.enabled=false", "-c", "core.autocrlf=false",
    ]

    def run(args, cwd=root, expected=0):
        result = subprocess.run(args, cwd=cwd, env=env, capture_output=True)
        if result.returncode != expected:
            raise RuntimeError(f"Unexpected exit {result.returncode}: {args}\n"
                               + (result.stdout + result.stderr).decode(errors="replace"))
        return result

    def git(repo, *args, expected=0):
        return run([*git_prefix, "-C", str(repo), *args], expected=expected).stdout

    def text(repo, *args, expected=0):
        return git(repo, *args, expected=expected).decode().strip()

    def save(name, value):
        (artifacts / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

    def install(repo, part):
        for path in sorted((FIXTURES / part).iterdir()):
            shutil.copyfile(path, repo / path.name)

    def commit(repo, message):
        git(repo, "add", "--all")
        git(repo, "commit", "-m", message)
        return text(repo, "rev-parse", "HEAD")

    def clone(source, name, branch):
        repo = root / name
        run([*git_prefix, "clone", "--no-hardlinks", f"--template={empty}", str(source), str(repo)])
        git(repo, "checkout", "-b", branch)
        return repo

    def snapshot(repo):
        return {
            "head": text(repo, "rev-parse", "HEAD"),
            "branch": text(repo, "symbolic-ref", "HEAD"),
            "refs": text(repo, "for-each-ref", "--format=%(refname) %(objectname)").splitlines(),
            "status": git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all").decode(),
            "index_sha256": digest((repo / ".git/index").read_bytes()),
            "staged_diff_sha256": digest(git(repo, "diff", "--cached", "--binary")),
            "unstaged_diff_sha256": digest(git(repo, "diff", "--binary")),
            "files": {
                str(path.relative_to(repo)): {"sha256": digest(path.read_bytes()), "mode": path.stat().st_mode & 0o777}
                for path in sorted(repo.rglob("*"))
                if path.is_file() and ".git" not in path.relative_to(repo).parts
            },
        }

    checks = []

    def test(repo, label, count, expected=0, committed=True):
        revision = text(repo, "rev-parse", "HEAD")
        tree = text(repo, "rev-parse", "HEAD^{tree}") if committed else text(repo, "write-tree")
        before = git(repo, "status", "--porcelain=v1", "--untracked-files=all")
        if committed:
            assert before == b"", (label, before)
        result = run([sys.executable, "-B", "-m", "unittest", "-v"], cwd=repo, expected=expected)
        output = (result.stdout + result.stderr).decode().replace(str(root), "<rehearsal>")
        assert f"Ran {count} tests" in output, output
        assert git(repo, "status", "--porcelain=v1", "--untracked-files=all") == before
        assert text(repo, "rev-parse", "HEAD") == revision
        (artifacts / f"{label}.log").write_text(output)
        checks.append({"label": label, "cwd": repo.name, "command": COMMAND,
                       "revision": revision, "tree": tree, "committed_tree": committed,
                       "expected_exit": expected, "actual_exit": result.returncode,
                       "tests_run": count, "result": "passed" if expected == 0 else "failed as expected",
                       "finished_at": datetime.now(timezone.utc).isoformat()})
        return output

    original = root / "original"
    original.mkdir()
    git(original, "init", "--initial-branch=main", "--object-format=sha1", f"--template={empty}")
    install(original, "base")
    (original / ".gitignore").write_text("*.cache\n")
    (original / "notes.txt").write_text("Fictional reading queue.\n")
    base = commit(original, "Base: preserve reading order")
    test(original, "base", 3)

    # Staged and unstaged bytes of one path differ, plus independent unstaged,
    # untracked and ignored files. None belongs in the integration result.
    (original / "notes.txt").write_text("Staged draft: reading queue.\n")
    git(original, "add", "notes.txt")
    (original / "notes.txt").write_text("Staged draft: reading queue.\nUnstaged paragraph.\n")
    with (original / "queue_summary.py").open("a") as stream:
        stream.write("\n# Uncommitted local experiment.\n")
    (original / "ideas.txt").write_text("Untracked idea, keep it.\n")
    (original / "scratch.cache").write_text("Ignored scratch value, keep it.\n")
    before_original = snapshot(original)

    contributors, inputs = {}, {}
    for name, count, expected in [("count", 5, 0), ("minutes", 6, 0), ("proposed-order", 4, 1)]:
        repo = clone(original, name, f"contribution/{name}")
        install(repo, name)
        inputs[name] = commit(repo, f"{name}: independent contribution")
        output = test(repo, name, count, expected)
        if expected:
            assert "failures=1" in output and "test_input_order_is_preserved" in output
        contributors[name] = repo

    integration = clone(original, "integration", "integration/accepted")
    for name, revision in inputs.items():
        git(integration, "fetch", "--no-tags", str(contributors[name]), revision)
        git(integration, "branch", f"input/{name}", revision)
    git(integration, "branch", "input/base", base)

    # Pin first, then demonstrate a moving source branch while the fixed input
    # remains unchanged. This successor has no integration acceptance.
    count_repo = contributors["count"]
    (count_repo / "count-notes.txt").write_text("Follow-up documentation, outside COUNT-1 acceptance.\n")
    newer_count = commit(count_repo, "count: later documentation contribution")
    before_concurrent = snapshot(count_repo)
    # A bare, local-only remote models delivery without contacting a service.
    # Seed the later contributor tip so the new integration must preserve it.
    delivery = root / "delivery.git"
    git(root, "init", "--bare", "--initial-branch=main", "--object-format=sha1", f"--template={empty}", str(delivery))
    git(count_repo, "push", str(delivery), f"{newer_count}:refs/heads/contribution/count")
    before_remote = text(delivery, "for-each-ref", "--format=%(refname) %(objectname)").splitlines()
    assert before_remote == [f"refs/heads/contribution/count {newer_count}"]

    git(integration, "merge", "--no-ff", "--no-commit", inputs["count"])
    first_merge = commit(integration, "Integrate accepted COUNT-1")
    conflict = run([*git_prefix, "-C", str(integration), "merge", "--no-ff", "--no-commit", inputs["minutes"]], expected=1)
    conflict_text = (conflict.stdout + conflict.stderr).decode()
    assert text(integration, "diff", "--name-only", "--diff-filter=U") == "queue_summary.py"
    assert text(integration, "rev-parse", "MERGE_HEAD") == inputs["minutes"]
    (artifacts / "mechanical-conflict.txt").write_text(
        conflict_text + "\n" + (integration / "queue_summary.py").read_text())
    stages = {str(stage): digest(git(integration, "show", f":{stage}:queue_summary.py")) for stage in (1, 2, 3)}
    assert stages["1"] == digest((FIXTURES / "base/queue_summary.py").read_bytes())
    assert stages["2"] == digest((FIXTURES / "count/queue_summary.py").read_bytes())
    assert stages["3"] == digest((FIXTURES / "minutes/queue_summary.py").read_bytes())
    install(integration, "integrated")
    git(integration, "add", "queue_summary.py", "test_integration.py")
    assert git(integration, "ls-files", "--unmerged") == b""
    git(integration, "diff", "--cached", "--check")
    final = commit(integration, "Integrate accepted MINUTES-1; preserve both additive fields")
    final_tree = text(integration, "rev-parse", "HEAD^{tree}")
    test(integration, "integrated", 10)
    for ancestor in (base, inputs["count"], inputs["minutes"]):
        git(integration, "merge-base", "--is-ancestor", ancestor, final)
    git(integration, "merge-base", "--is-ancestor", inputs["proposed-order"], final, expected=1)
    git(integration, "fetch", "--no-tags", str(count_repo), newer_count)
    git(integration, "branch", "observed/count-successor", newer_count)
    git(integration, "merge-base", "--is-ancestor", newer_count, final, expected=1)
    assert text(integration, "rev-list", "--parents", "-n", "1", final).split() == [final, first_merge, inputs["minutes"]]

    (artifacts / "integration.patch").write_bytes(git(integration, "diff", "--binary", base, final))
    (artifacts / "held-order-proposal.patch").write_bytes(git(integration, "diff", "--binary", base, inputs["proposed-order"]))
    (artifacts / "commit-graph.txt").write_bytes(git(integration, "log", "--all", "--graph", "--decorate", "--oneline"))
    bundle = artifacts / "integration.bundle"
    git(integration, "bundle", "create", str(bundle), "refs/heads/integration/accepted",
        "refs/heads/input/base", "refs/heads/input/count", "refs/heads/input/minutes",
        "refs/heads/input/proposed-order", "refs/heads/observed/count-successor")
    git(integration, "bundle", "verify", str(bundle))
    restored = root / "restored"
    run([*git_prefix, "clone", f"--template={empty}", "--branch", "integration/accepted", str(bundle), str(restored)])
    assert text(restored, "rev-parse", "HEAD") == final
    assert text(restored, "rev-parse", "HEAD^{tree}") == final_tree
    test(restored, "restored-bundle", 10)

    patched = root / "patched"
    run([*git_prefix, "clone", f"--template={empty}", "--branch", "input/base", str(bundle), str(patched)])
    git(patched, "apply", "--check", str(artifacts / "integration.patch"))
    git(patched, "apply", "--index", str(artifacts / "integration.patch"))
    assert text(patched, "write-tree") == final_tree
    test(patched, "applied-patch", 10, committed=False)

    # The fixture request explicitly names this new local delivery ref. No
    # existing branch is replaced, and no network destination is configured.
    git(integration, "push", str(delivery), f"{final}:refs/heads/integration/accepted")
    advertised = text(integration, "ls-remote", str(delivery), "refs/heads/integration/accepted")
    assert advertised.split() == [final, "refs/heads/integration/accepted"]
    assert text(delivery, "rev-parse", "refs/heads/contribution/count") == newer_count
    remote_readback = root / "local-remote-readback"
    run([*git_prefix, "clone", f"--template={empty}", "--branch", "integration/accepted", str(delivery), str(remote_readback)])
    assert text(remote_readback, "rev-parse", "HEAD") == final
    assert text(remote_readback, "rev-parse", "HEAD^{tree}") == final_tree
    test(remote_readback, "local-remote-readback", 10)
    save("local-remote-readback.json", {
        "destination": "delivery.git (new local bare fixture repository)",
        "network_used": False, "new_target_ref": "refs/heads/integration/accepted",
        "before_refs": before_remote,
        "after_refs": text(delivery, "for-each-ref", "--format=%(refname) %(objectname)").splitlines(),
        "advertised_integration": advertised,
        "cloned_commit": final, "cloned_tree": final_tree,
        "existing_contributor_ref_preserved": True,
    })

    after_original, after_concurrent = snapshot(original), snapshot(count_repo)
    assert before_original == after_original, "Original checkout changed"
    assert before_concurrent == after_concurrent, "Concurrent contributor changed"
    assert git(integration, "status", "--porcelain=v1", "--untracked-files=all") == b""
    save("original-before.json", before_original)
    save("original-after.json", after_original)
    save("concurrent-before.json", before_concurrent)
    save("concurrent-after.json", after_concurrent)
    save("verification.json", {
        "fixture": "fictional reading queue; no external repository or service",
        "git": run(["git", "--version"]).stdout.decode().strip(),
        "python": sys.version.split()[0], "platform": sys.platform,
        "base": base, "accepted": {key: inputs[key] for key in ("count", "minutes")},
        "held": {"proposed-order": inputs["proposed-order"]},
        "observed_unaccepted_successor": newer_count,
        "integration_branch": "integration/accepted", "integration_commit": final,
        "integration_tree": final_tree, "merge_parents": [first_merge, inputs["minutes"]],
        "mechanical_conflict_stages_sha256": stages,
        "original_exact_snapshot_unchanged": before_original == after_original,
        "contributor_exact_snapshot_unchanged": before_concurrent == after_concurrent,
        "held_proposal_is_ancestor": False, "newer_count_is_ancestor": False,
        "restored_bundle_commit_and_tree_match": True, "applied_patch_tree_matches": True,
        "local_bare_remote_commit_and_tree_match": True,
        "local_bare_remote_existing_contributor_ref_preserved": True,
        "checks": checks, "log_paths": "absolute rehearsal roots replaced with <rehearsal>",
        "fixture_sha256": {str(path.relative_to(FIXTURES)): digest(path.read_bytes())
                           for path in sorted(FIXTURES.rglob("*")) if path.is_file()},
    })
    save("artifact-sha256.json", {path.name: digest(path.read_bytes())
                                for path in sorted(artifacts.iterdir()) if path.is_file()})
    print(f"PASS: integrated {final}; 10 tests passed in each final replay")
    print("Original dirty checkout and later contributor state are unchanged; ORDER-2 remains held.")
    print(f"Artifacts: {artifacts}")


if __name__ == "__main__":
    main()
