#!/usr/bin/env python3
"""Check this fictional migration bundle offline; never open a URL or a browser.

This deliberately small parser accepts the Netscape bookmark structures used by
the fixture. It is not a general browser importer or a validator for arbitrary
HTML exports. The checks compare occurrences, hierarchy and original attributes.
"""
from copy import deepcopy
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Bookmarks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = []
        self.stack = []
        self.pending = None
        self.capture = None
        self.buffer = []
        self.last_node = None
        self.seen_root = False
        self.ignored = None

    def finish_description(self):
        if self.capture and self.capture[0] == "dd":
            self.last_node["description"] = "".join(self.buffer).strip()
            self.capture = None
            self.buffer = []

    def handle_starttag(self, tag, pairs):
        if tag in {"dt", "dl"}:
            self.finish_description()
        if tag in {"meta", "p", "dt"}:
            return
        if tag in {"title", "h1"}:
            require(not self.stack, "Document heading inside bookmark tree")
            self.ignored = tag
            return
        if tag == "dl":
            require(self.capture is None, "Folder opened inside title")
            if self.pending is not None:
                self.stack.append(self.pending["children"])
                self.pending = None
            else:
                require(not self.seen_root, "Unattached folder list")
                self.seen_root = True
                self.stack.append(self.root)
            return
        if tag in {"h3", "a"}:
            require(self.stack and self.capture is None and self.pending is None,
                    "Ambiguous bookmark/folder boundary")
            require(len({key for key, _ in pairs}) == len(pairs),
                    "Duplicate attributes require review")
            self.capture = (tag, dict(pairs), self.getpos()[0])
            self.buffer = []
            return
        if tag == "dd":
            require(self.last_node is not None and self.capture is None,
                    "Description has no unambiguous owner")
            self.capture = ("dd", {}, self.getpos()[0])
            self.buffer = []
            return
        raise ValueError(f"Unsupported HTML element: {tag}")

    def handle_endtag(self, tag):
        if tag in {"title", "h1"}:
            require(self.ignored == tag, "Mismatched document heading")
            self.ignored = None
        elif tag == "dd":
            self.finish_description()
        elif tag in {"h3", "a"}:
            require(self.capture and self.capture[0] == tag, "Mismatched title")
            _, attrs, line = self.capture
            node = {"kind": "folder" if tag == "h3" else "bookmark",
                    "title": "".join(self.buffer), "attributes": attrs,
                    "description": "", "line": line, "children": []}
            self.stack[-1].append(node)
            self.last_node = node
            self.pending = node if tag == "h3" else None
            self.capture = None
            self.buffer = []
        elif tag == "dl":
            self.finish_description()
            require(self.stack and self.capture is None and self.pending is None,
                    "Unbalanced folder list")
            self.stack.pop()
        elif tag not in {"p", "dt"}:
            raise ValueError(f"Unsupported closing element: {tag}")

    def handle_data(self, data):
        if self.capture is not None:
            self.buffer.append(data)
        elif not self.ignored:
            require(not data.strip(), "Unattached text")


def parse(raw):
    parser = Bookmarks()
    parser.feed(raw.decode("utf-8"))
    parser.close()
    parser.finish_description()
    require(parser.seen_root and not parser.stack and parser.capture is None
            and parser.pending is None and parser.ignored is None,
            "Incomplete bookmark document")
    return parser.root


def walk(nodes, prefix=(), names=(), parent=None):
    for index, node in enumerate(nodes):
        path = prefix + (index,)
        labels = names + (node["title"],)
        yield node, path, labels, parent
        yield from walk(node["children"], path, labels, path)


CARRIED = {"add_date", "last_modified", "tags", "shortcuturl"}


def classify(node):
    if node["kind"] == "folder":
        return "included", "Folder retained, including empty folders"
    url = node["attributes"].get("href")
    if not url:
        return "held", "Missing address"
    try:
        parts = urlsplit(url)
        if parts.scheme not in {"https", "http"}:
            return "held", f"Scheme requires a target-specific decision: {parts.scheme or 'none'}"
        if not parts.hostname or any(char.isspace() or ord(char) < 32 for char in url):
            return "held", "Malformed HTTP(S) address"
        if re.search(r"%(?![0-9A-Fa-f]{2})", url):
            return "held", "Malformed percent escape"
        if parts.username is not None or parts.password is not None:
            return "held", "Address contains user information"
        _ = parts.port
    except ValueError:
        return "held", "Malformed HTTP(S) address"
    return "included", "HTTP(S) syntax accepted locally; destination not opened"


def lineage(digest, number):
    return f"sha256:{digest}#occurrence:{number:04d}"


def verify(source, prepared, manifest):
    digest = sha256(source).hexdigest()
    require(manifest["source_sha256"] == digest, "Source bytes changed")
    require(manifest["prepared_sha256"] == sha256(prepared).hexdigest(),
            "Prepared bytes changed")
    source_tree, prepared_tree = parse(source), parse(prepared)
    source_rows = list(walk(source_tree))
    require(len(source_rows) == len(manifest["records"]), "Missing lineage record")
    require(sum(node["kind"] == "folder" for node, *_ in source_rows) == 7,
            "Fixture folder denominator changed")
    require(sum(node["kind"] == "bookmark" for node, *_ in source_rows) == 15,
            "Fixture bookmark denominator changed")
    path_ids = {path: lineage(digest, i) for i, (_, path, _, _) in enumerate(source_rows, 1)}
    expected_output = []
    by_path = {}
    included, held = 0, 0
    for number, ((node, path, names, parent), record) in enumerate(
            zip(source_rows, manifest["records"]), 1):
        status, reason = classify(node)
        identity = lineage(digest, number)
        expected_source = {"lineage_id": identity,
                           "native_source_id": node["attributes"].get("id"),
                           "parent_lineage_id": path_ids.get(parent),
                           "ordinal_path": list(path), "display_path": list(names),
                           "kind": node["kind"], "title": node["title"],
                           "attributes": node["attributes"],
                           "description": node["description"], "source_line": node["line"]}
        require(record["source"] == expected_source, "Source lineage or metadata differs")
        require(record["disposition"] == status and record["reason"] == reason,
                "Held/included classification differs")
        require(record["target_status"] == "not_run" and record["target_id"] is None,
                "Fixture falsely claims a live target result")
        carried = {key: value for key, value in node["attributes"].items() if key in CARRIED}
        sidecar = {key: value for key, value in node["attributes"].items()
                   if key not in CARRIED | {"href"}}
        require(record["carried_attributes"] == (carried if status == "included" else {}),
                "Carried metadata differs")
        require(record["sidecar_only_attributes"] == (sidecar if status == "included"
                                                       else node["attributes"]),
                "Sidecar metadata differs")
        if status == "held":
            held += 1
            require(record["prepared_ordinal_path"] is None, "Held entry leaked into plan")
            continue
        included += node["kind"] == "bookmark"
        target_children = expected_output if parent is None else by_path[parent]["children"]
        output_path = (0,) + (() if parent is None else tuple(by_path[parent]["output_path"])[1:]) + (len(target_children),)
        expected = {"kind": node["kind"], "title": node["title"],
                    "attributes": {"data-source-lineage": identity, **carried},
                    "description": node["description"], "children": [],
                    "output_path": list(output_path)}
        if node["kind"] == "bookmark":
            expected["attributes"]["href"] = node["attributes"]["href"]
        target_children.append(expected)
        by_path[path] = expected
        require(record["prepared_ordinal_path"] == list(output_path), "Planned path differs")
    require((included, held) == (8, 7), "Fixture disposition denominator changed")
    require(len(prepared_tree) == 1 and prepared_tree[0]["kind"] == "folder",
            "Transfer wrapper missing")
    wrapper = prepared_tree[0]
    require(wrapper["title"] == manifest["wrapper_title"] and wrapper["attributes"] == {},
            "Wrapper placement metadata changed")

    def shape(nodes):
        return [{"kind": n["kind"], "title": n["title"], "attributes": n["attributes"],
                 "description": n["description"], "children": shape(n["children"])} for n in nodes]

    require(shape(wrapper["children"]) == shape(expected_output),
            "Ordered tree, URL, occurrence or metadata mismatch")
    require(manifest["counts"] == {"source_folders": 7, "source_bookmarks": 15,
            "prepared_source_folders": 7, "wrapper_folders": 1,
            "included_bookmarks": 8, "held_bookmarks": 7}, "Report counts differ")
    return source_tree, prepared_tree


def main():
    folder = Path(__file__).resolve().parent
    source = (folder / "source-bookmarks.html").read_bytes()
    prepared = (folder / "import-ready.html").read_bytes()
    manifest = json.loads((folder / "lineage.json").read_text(encoding="utf-8"))
    source_tree, _ = verify(source, prepared, manifest)
    by_native_id = {node["attributes"].get("id"): node for node, *_ in walk(source_tree)}
    require(by_native_id["fixture-unicode"]["title"] == "Café UI — 日本語", "Unicode changed")
    require(by_native_id["fixture-blank-title"]["title"] == "", "Blank title changed")
    require(by_native_id["fixture-repeat-a"]["attributes"]["href"] ==
            by_native_id["fixture-repeat-b"]["attributes"]["href"], "Same-folder duplicate lost")
    require(by_native_id["fixture-api-a"]["attributes"]["href"] ==
            by_native_id["fixture-api-b"]["attributes"]["href"], "Cross-folder duplicate lost")
    print("PASS: 7 source folders + 15 link occurrences = 7 retained folders + 8 included + 7 held links")
    print("PASS: hierarchy/order, repeated folder names, empty folders, Unicode, blank title, exact URLs")
    print("PASS: duplicate multiplicity, all original attributes/descriptions, source IDs and derived lineage")
    print("PASS: one wrapper; sidecar-only icon/toolbar metadata; no held URL in import file")
    print("PASS: source and prepared byte digests; no live-import claim")

    mutations = []
    raw_text = prepared.decode("utf-8")
    duplicate_line = next(line for line in raw_text.splitlines(True)
                          if "Release checklist" in line)
    mutations.append(("duplicate occurrence removed", source,
                      raw_text.replace(duplicate_line, "", 1).encode(), deepcopy(manifest)))
    mutations.append(("folder identity/order changed", source,
                      raw_text.replace(">Reference</H3>", ">Reference changed</H3>", 1).encode(), deepcopy(manifest)))
    mutations.append(("URL changed", source,
                      prepared.replace(b"version=2", b"version=3", 1), deepcopy(manifest)))
    mutations.append(("metadata dropped", source,
                      prepared.replace(b' TAGS="api,review"', b"", 1), deepcopy(manifest)))
    mutations.append(("original source changed", source + b"\n", prepared, deepcopy(manifest)))
    missing = deepcopy(manifest)
    missing["records"] = missing["records"][:-1]
    mutations.append(("lineage record removed", source, prepared, missing))
    false_live = deepcopy(manifest)
    false_live["records"][0]["target_status"] = "verified"
    mutations.append(("unsupported live success claimed", source, prepared, false_live))
    for label, changed_source, changed_output, changed_manifest in mutations:
        # Re-sign output mutations so byte hashes cannot mask structural failures.
        changed_manifest["prepared_sha256"] = sha256(changed_output).hexdigest()
        try:
            verify(changed_source, changed_output, changed_manifest)
        except ValueError:
            print(f"PASS negative control: {label}")
        else:
            raise ValueError(f"Mutation was not detected: {label}")
    print("Browser import, target recovery and destination reachability: NOT RUN")


if __name__ == "__main__":
    main()
