#!/usr/bin/env python3
"""Check this offline fixture's source and pure rules, never browser behavior."""
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.elements = []
        self.scripts = []
        self._script = None
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs))
        if tag == "script" and "src" not in attrs:
            self._script = []

    def handle_data(self, data):
        if self._script is not None:
            self._script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._script is not None:
            self.scripts.append("".join(self._script))
            self._script = None


def main():
    root = Path(__file__).resolve().parent
    node = shutil.which("node")
    if not node:
        raise SystemExit("Node is unavailable; no dependency was installed. JavaScript checks were not run.")
    pages = {}
    hashes = {}
    for filename in ("before.html", "after.html"):
        content = (root / filename).read_bytes()
        page = Page(content.decode("utf-8"))
        pages[filename] = page
        hashes[filename] = sha256(content).hexdigest()
        ids = [attrs["id"] for _, attrs in page.elements if "id" in attrs]
        assert len(ids) == len(set(ids)), f"{filename}: duplicate IDs"
        for tag, attrs in page.elements:
            if tag == "label":
                assert attrs.get("for") in ids, f"{filename}: missing label target"
            for attribute in ("aria-describedby", "aria-labelledby"):
                assert all(target in ids for target in attrs.get(attribute, "").split()), f"{filename}: missing ARIA target"
            if "src" in attrs:
                assert tag == "script" and attrs["src"] == "draft-rules.js", f"{filename}: unexpected resource"
                assert (root / attrs["src"]).is_file(), f"{filename}: missing script"
            assert "action" not in attrs and "formaction" not in attrs, f"{filename}: unexpected form endpoint"
        assert len(page.scripts) == 1, f"{filename}: expected one inline controller"

    before = {attrs["id"]: (tag, attrs) for tag, attrs in pages["before.html"].elements if "id" in attrs}
    after = {attrs["id"]: (tag, attrs) for tag, attrs in pages["after.html"].elements if "id" in attrs}
    assert before["create-draft"][0] == "div"
    assert "tabindex" not in before["create-draft"][1]
    assert after["create-draft"][0] == "button"
    assert after["create-draft"][1]["type"] == "submit"
    labels = {attrs["for"] for tag, attrs in pages["after.html"].elements if tag == "label"}
    assert labels == {"code", "kits", "shelf"}
    for field in labels:
        assert "required" in after[field][1]
        assert after[field][1]["aria-describedby"] == f"{field}-hint"
        assert f"{field}-error" in after
    assert after["error-summary"][1]["tabindex"] == "-1"
    assert "hidden" in after["error-summary"][1]
    assert after["result"][1]["role"] == "status"

    rules_source = (root / "draft-rules.js").read_text(encoding="utf-8")
    hashes["draft-rules.js"] = sha256(rules_source.encode("utf-8")).hexdigest()
    # Execute only the pure shared rules. Controllers receive syntax checks, no mock DOM.
    test = r'''
const assert = require("node:assert/strict");
const vm = require("node:vm");
const input = JSON.parse(require("node:fs").readFileSync(0, "utf8"));
for (const source of input.controllers) new vm.Script(source);
const rules = vm.runInNewContext(input.rules + "\nDraftRules;");
const plain = value => JSON.parse(JSON.stringify(value));
const valid = {code: "LANTERN-42", kits: "2", shelf: "West shelf"};
assert.deepEqual(plain(rules.validate(valid)), {errors: [], draft: {code: "LANTERN-42", kits: 2, shelf: "West shelf"}});
assert.equal(rules.describe(rules.validate(valid).draft), "Local draft ready: LANTERN-42; 2 kits; West shelf. Nothing has been sent or reserved.");
assert.deepEqual(plain(rules.validate({...valid, code: "LANTERN"}).errors).map(e => e.field), ["code"]);
assert.deepEqual(plain(rules.validate({code: "", kits: "0", shelf: ""}).errors).map(e => e.field), ["code", "kits", "shelf"]);
for (const kits of ["1", "4"]) assert.equal(rules.validate({...valid, kits}).errors.length, 0);
for (const kits of ["", "0", "5", "2.5", "02", "2e0"]) assert.deepEqual(plain(rules.validate({...valid, kits}).errors).map(e => e.field), ["kits"]);
for (const code of ["lantern-42", "LANTERN-4", "LANTERN-420"]) assert.deepEqual(plain(rules.validate({...valid, code}).errors).map(e => e.field), ["code"]);
assert.equal(rules.validate({...valid, code: " LANTERN-42 ", kits: " 2 "}).errors.length, 0);
assert.equal(rules.validate({...valid, shelf: "North shelf"}).errors.length, 0);
assert.equal(rules.validate({...valid, shelf: "South shelf"}).draft, null);
assert.equal(rules.describe(rules.validate({...valid, kits: "1"}).draft), "Local draft ready: LANTERN-42; 1 kit; West shelf. Nothing has been sent or reserved.");
assert.deepEqual(valid, {code: "LANTERN-42", kits: "2", shelf: "West shelf"});
process.stdout.write(JSON.stringify({javascript_syntax: "pass", pure_rule_contract_cases: "pass", node_version: process.version}));
'''
    completed = subprocess.run([node, "-e", test], input=json.dumps({
        "rules": rules_source,
        "controllers": [page.scripts[0] for page in pages.values()],
    }), text=True, capture_output=True, check=True)
    report = {
        "scope": "Selected source relationships, controller syntax, and shared pure business rules only",
        "markup_relationships": "pass",
        **json.loads(completed.stdout),
        "python_version": sys.version.split()[0],
        "sha256": hashes,
        "browser_keyboard_cases": "unrun",
        "computed_accessibility_tree": "unrun",
        "screen_reader_announcements": "unrun",
        "visual_focus_and_obscuration": "unrun",
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
