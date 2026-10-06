"""A local, single-process three-way text review workspace.

Merge coordinates are logical lines from splitlines(keepends=True), using
SequenceMatcher with autojunk disabled. Saving is a checkpoint of the complete
review state, not an acceptance of local changes or pending conflicts.

Persistence uses POSIX directory descriptors and O_NOFOLLOW, as supported by
this workspace's local runtime. It provides atomic replacement, not locking or
stronger crash/power-loss durability guarantees.
"""

import difflib
import json
import os
from pathlib import Path
import re
import stat
import tempfile


MAX_BYTES = 2_097_152
MAX_TEXT = 100_000
MAX_DOCUMENTS = 100


class ConflictPending(ValueError):
    """An unresolved incoming revision blocks editing and further receives."""


def _name(value):
    if not isinstance(value, str) or re.fullmatch(
        r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", value
    ) is None:
        raise ValueError("invalid document name")
    return value


def _text(value):
    if not isinstance(value, str) or len(value) > MAX_TEXT:
        raise ValueError("text must be a string of at most 100000 characters")
    return value


def _hunks(base, variant):
    matcher = difflib.SequenceMatcher(a=base, b=variant, autojunk=False)
    return [
        (start, end, tuple(variant[left:right]))
        for op, start, end, left, right in matcher.get_opcodes()
        if op != "equal"
    ]


def _overlap(first, second):
    start, end, _ = first
    other_start, other_end, _ = second
    if start == end and other_start == other_end:
        return start == other_start
    if start == end:
        return other_start <= start <= other_end
    if other_start == other_end:
        return start <= other_start <= end
    return max(start, other_start) < min(end, other_end)


def _merge(base, local, incoming):
    """Return (merged_text, has_conflict) without mutating any document."""
    if local == base:
        return incoming, False
    if incoming == base or local == incoming:
        return local, False

    lines = base.splitlines(keepends=True)
    left = _hunks(lines, local.splitlines(keepends=True))
    right = _hunks(lines, incoming.splitlines(keepends=True))

    # Both opcode lists are ordered in base coordinates. Include touching
    # boundaries in the candidate window, then apply the exact overlap rule.
    # Skipping earlier ranges avoids an unnecessary all-pairs comparison.
    first_possible = 0
    for ours in left:
        while first_possible < len(right) and right[first_possible][1] < ours[0]:
            first_possible += 1
        candidate = first_possible
        while candidate < len(right) and right[candidate][0] <= ours[1]:
            theirs = right[candidate]
            if ours != theirs and _overlap(ours, theirs):
                return local, True
            candidate += 1

    # Identical edits occur once. There are no competing ranges after the
    # check above, and each individual opcode list is nonoverlapping.
    changes = sorted(set(left).union(right), key=lambda hunk: (hunk[0], hunk[1]))
    parts = []
    position = 0
    for start, end, replacement in changes:
        parts.extend(lines[position:start])
        parts.extend(replacement)
        position = end
    parts.extend(lines[position:])
    return "".join(parts), False


def _document(value):
    if not isinstance(value, dict) or set(value) != {
        "name", "base", "text", "conflict"
    }:
        raise ValueError("invalid document fields")
    name = _name(value["name"])
    base = _text(value["base"])
    text = _text(value["text"])
    conflict = value["conflict"]
    if conflict is not None:
        if not isinstance(conflict, dict) or set(conflict) != {
            "base", "local", "incoming"
        }:
            raise ValueError("invalid conflict fields")
        for item in conflict.values():
            _text(item)
        if conflict["base"] != base or conflict["local"] != text:
            raise ValueError("inconsistent conflict")
        conflict = dict(conflict)
    return name, {"base": base, "text": text, "conflict": conflict}


def _unique_object(pairs):
    """Do not allow JSON duplicate fields to silently overwrite evidence."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate snapshot field")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("invalid JSON constant: " + value)


def _decode_snapshot(raw):
    try:
        data = json.loads(
            raw, object_pairs_hook=_unique_object, parse_constant=_invalid_constant
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("invalid snapshot") from error
    if not isinstance(data, dict) or set(data) != {"schema_version", "documents"}:
        raise ValueError("invalid snapshot fields")
    if type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ValueError("unsupported snapshot schema")
    values = data["documents"]
    if not isinstance(values, list) or len(values) > MAX_DOCUMENTS:
        raise ValueError("invalid document collection")
    docs = {}
    for value in values:
        name, doc = _document(value)
        if name in docs:
            raise ValueError("duplicate document name")
        docs[name] = doc
    return docs


def _snapshot_bytes(docs):
    data = {
        "schema_version": 1,
        "documents": [dict(name=name, **docs[name]) for name in sorted(docs)],
    }
    # Incremental encoding bounds the output buffer even if the full live
    # workspace cannot fit in a checkpoint. Retaining Unicode characters
    # also avoids expanding ordinary non-ASCII text into oversized escapes.
    # Python's bytes JSON decoder uses surrogatepass as well; matching that
    # behavior preserves even surrogate-containing Python strings exactly.
    encoder = json.JSONEncoder(ensure_ascii=False, separators=(",", ":"))
    raw = bytearray()
    for chunk in encoder.iterencode(data):
        encoded = chunk.encode("utf-8", "surrogatepass")
        if len(raw) + len(encoded) + 1 > MAX_BYTES:
            raise ValueError("snapshot too large")
        raw.extend(encoded)
    raw.extend(b"\n")
    return bytes(raw)


class MergeWorkspace:
    def __init__(self, root):
        try:
            self.root = Path(os.path.abspath(root))
        except (TypeError, ValueError) as error:
            raise ValueError("invalid workspace root") from error
        self._docs = {}
        directory = self._open_root(create=True)
        try:
            try:
                info = os.stat("workspace.json", dir_fd=directory, follow_symlinks=False)
            except FileNotFoundError:
                return
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise ValueError("snapshot is not a bounded regular file")
            snapshot = os.open(
                "workspace.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=directory,
            )
            try:
                info = os.fstat(snapshot)
                if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                    raise ValueError("snapshot is not a bounded regular file")
                chunks = []
                remaining = MAX_BYTES + 1
                while remaining:
                    chunk = os.read(snapshot, min(65536, remaining))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    remaining -= len(chunk)
                raw = b"".join(chunks)
                if len(raw) > MAX_BYTES:
                    raise ValueError("snapshot too large")
            finally:
                os.close(snapshot)
        finally:
            os.close(directory)
        self._docs = _decode_snapshot(raw)

    def _open_root(self, create=False):
        if create:
            try:
                self.root.mkdir()
            except FileExistsError:
                pass
        info = self.root.lstat()
        if not stat.S_ISDIR(info.st_mode):
            raise ValueError("workspace root must be a directory, not a symlink")
        return os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    def _existing(self, name):
        return self._docs[_name(name)]

    def names(self):
        return sorted(self._docs)

    def get(self, name):
        doc = self._existing(name)
        return {
            "base": doc["base"],
            "text": doc["text"],
            "dirty": doc["text"] != doc["base"],
            "conflict": None if doc["conflict"] is None else dict(doc["conflict"]),
        }

    def add(self, name, text):
        name = _name(name)
        text = _text(text)
        if name in self._docs or len(self._docs) >= MAX_DOCUMENTS:
            raise ValueError("duplicate name or document limit")
        self._docs[name] = {"base": text, "text": text, "conflict": None}
        return self.get(name)

    def edit(self, name, text):
        doc = self._existing(name)
        if doc["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before editing")
        text = _text(text)
        doc["text"] = text
        return self.get(name)

    def receive(self, name, incoming):
        doc = self._existing(name)
        if doc["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before receiving")
        incoming = _text(incoming)
        merged, has_conflict = _merge(doc["base"], doc["text"], incoming)
        if has_conflict:
            doc["conflict"] = {
                "base": doc["base"], "local": doc["text"], "incoming": incoming
            }
        else:
            # Disjoint changes can exceed the limit even though each input
            # fits. Validate the assembled result before changing live state.
            merged = _text(merged)
            doc.update(base=incoming, text=merged, conflict=None)
        return self.get(name)

    def resolve(self, name, choice, text=None):
        doc = self._existing(name)
        conflict = doc["conflict"]
        if conflict is None:
            raise ValueError("no pending conflict")
        if not isinstance(choice, str) or choice not in ("local", "incoming", "manual"):
            raise ValueError("invalid resolution")
        if choice == "manual":
            resolved = _text(text)
        else:
            if text is not None:
                raise ValueError("text only valid for manual resolution")
            resolved = conflict[choice]
        doc.update(base=conflict["incoming"], text=resolved, conflict=None)
        return self.get(name)

    def rename(self, name, new_name):
        doc = self._existing(name)
        new_name = _name(new_name)
        if new_name == name:
            return self.get(name)
        if new_name in self._docs:
            raise ValueError("name exists")
        self._docs[new_name] = doc
        del self._docs[name]
        return self.get(new_name)

    def remove(self, name):
        self._existing(name)
        del self._docs[name]

    def save(self):
        raw = _snapshot_bytes(self._docs)
        directory = self._open_root()
        temporary = None
        descriptor = None
        try:
            try:
                info = os.stat("workspace.json", dir_fd=directory, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                if not stat.S_ISREG(info.st_mode):
                    raise ValueError("snapshot destination must be regular")
            descriptor, path = tempfile.mkstemp(
                prefix=".workspace-", suffix=".tmp", dir=self.root
            )
            temporary = Path(path).name
            with os.fdopen(descriptor, "wb") as stream:
                descriptor = None  # The context manager now owns this descriptor.
                stream.write(raw)
            os.replace(
                temporary, "workspace.json", src_dir_fd=directory, dst_dir_fd=directory
            )
            temporary = None
        finally:
            try:
                if descriptor is not None:
                    os.close(descriptor)
                if temporary is not None:
                    try:
                        os.unlink(temporary, dir_fd=directory)
                    except FileNotFoundError:
                        pass
            finally:
                os.close(directory)
