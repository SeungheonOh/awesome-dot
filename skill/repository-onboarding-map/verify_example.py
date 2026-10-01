"""Validate the reviewed fictional snapshot with stdlib Python and installed Make."""
import ast
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "WORKED_EXAMPLE.md"
PATTERN = r"^### `([^`]+)`\n\n```[^\n]*\n(.*?)^```$"
EXPECTED = {
    "README.md", "Makefile", ".python-version", ".github/workflows/check.yml",
    ".env.example", "app/config.py", "app/labels.py", "app/cli.py",
    "tests/test_labels.py", "tools/render_help.py", "docs/cli-help.txt",
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    original = SOURCE.read_bytes()
    matches = re.findall(PATTERN, original.decode(), re.MULTILINE | re.DOTALL)
    files = dict(matches)
    require(len(matches) == len(files), "duplicate source block")
    require(set(files) == EXPECTED, "fixture path set changed; review before executing")
    digest = hashlib.sha256()
    for name, content in sorted(files.items()):
        digest.update(name.encode() + b"\0" + content.encode() + b"\0")
    print("snapshot sha256:", digest.hexdigest(), flush=True)
    print("interpreter:", sys.executable, sys.version.split()[0], flush=True)
    make = shutil.which("make")
    require(make is not None, "GNU Make must already be installed; no installation attempted")
    trees = {p: ast.parse(s) for p, s in files.items() if p.endswith(".py")}

    def imports(path):
        return {(n.module, a.name) for n in ast.walk(trees[path])
                if isinstance(n, ast.ImportFrom) for a in n.names}

    require(imports("app/cli.py") == {
        ("app.config", "read_prefix"), ("app.labels", "make_label")}, "CLI import edges")
    require(imports("tests/test_labels.py") == {("app.labels", "make_label")}, "test edge")
    require(("app.cli", "build_parser") in imports("tools/render_help.py"), "generator edge")
    require(not any(isinstance(n, (ast.Import, ast.ImportFrom))
                    for n in ast.walk(trees["app/labels.py"])), "pure module has imports")
    cli_dump = ast.dump(trees["app/cli.py"])
    for expression in ('parser.add_argument("title")',
                       'print(make_label(args.title, read_prefix()))'):
        require(ast.dump(ast.parse(expression).body[0].value) in cli_dump, expression)
    guard = ast.parse('if __name__ == "__main__":\n    main()').body[0]
    require(ast.dump(guard) in cli_dump, "module entry guard")
    config_call = ast.parse('os.environ.get("WAYMARK_PREFIX", "note")').body[0].value
    require(ast.dump(config_call) in ast.dump(trees["app/config.py"]), "configuration reader")
    require('make verify' in files["README.md"], "stale command fixture missing")
    makefile = files["Makefile"]
    require(not re.search(r"^(?:verify\s*:|(?:-?include)\s|[^\n:]*%[^\n:]*:)",
                          makefile, re.MULTILINE), "verify may now resolve")
    require('check:\n\tPYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m unittest discover -s tests -v'
            in makefile, "unit recipe changed; review execution")
    require('docs:\n\tPYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m tools.render_help'
            in makefile, "generator recipe changed; review execution")
    require('- run: make check' in files[".github/workflows/check.yml"], "CI route changed")
    print("PASS selected source relationships and stale command conflict", flush=True)

    # Preserve only ordinary process necessities; this is not a security sandbox.
    env = {k: os.environ[k] for k in ("PATH", "SYSTEMROOT") if k in os.environ}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1", LC_ALL="C", TERM="dumb")
    with tempfile.TemporaryDirectory(prefix="waymark-example-") as tmp:
        root = Path(tmp)
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        def run(args, override=None):
            result = subprocess.run(args, cwd=root, env=env | (override or {}),
                                    text=True, capture_output=True, timeout=20)
            require(result.returncode == 0,
                    f"command failed: {args!r}\n{result.stdout}\n{result.stderr}")
            print("PASS", " ".join(args), flush=True)
            return result.stdout, result.stderr

        _, errors = run([make, "check", f"PYTHON={sys.executable}"])
        require("Ran 2 tests" in errors and "OK" in errors, "unit baseline incomplete")
        for prefix in ("note", "demo"):
            out, _ = run([sys.executable, "-m", "app.cli", "Blue Sky"],
                         {"WAYMARK_PREFIX": prefix})
            require(out == prefix + ":blue-sky\n", "CLI prefix/output mismatch")
        probe = (
            'from app.config import read_prefix; from app.labels import make_label; '
            'assert read_prefix() == "note"; '
            'assert make_label(" Blue\\tSky ", "note") == "note:blue-sky"'
        )
        run([sys.executable, "-c", probe])
        generated = root / "docs/cli-help.txt"
        before = generated.read_text()
        require("--topic" in before, "stale help fixture missing")
        run([make, "docs", f"PYTHON={sys.executable}"])
        after = generated.read_text()
        out, _ = run([sys.executable, "-c",
                      'from app.cli import build_parser; '
                      'print(build_parser().format_help(), end="")'])
        require(after == "# Generated by tools/render_help.py; do not edit.\n" + out,
                "generated help is not derived from parser")
        require(after != before and "--topic" not in after and "title" in after,
                "generated/source conflict not demonstrated")
        actual = {p.relative_to(root).as_posix(): p.read_text()
                  for p in root.rglob("*") if p.is_file()}
        require(actual.keys() == files.keys(), "unexpected generated file")
        changed = sorted(p for p in files if actual[p] != files[p])
        require(changed == ["docs/cli-help.txt"], f"unexpected changes: {changed}")
        print("PASS generated help drift; only changed file:", changed[0], flush=True)
    require(SOURCE.read_bytes() == original, "source Markdown changed")
    print("PASS fixture checks; original snapshot unchanged", flush=True)


if __name__ == "__main__":
    main()
