"""A local, single-process workspace for exact line-based three-way merges.

Snapshots are bounded and validated before they become live state. Checkpointing
never changes a document's merge base, working text, or pending review.
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
    """A document must be resolved before it can be edited or receive updates."""


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
        for tag, start, end, left, right in matcher.get_opcodes()
        if tag != "equal"
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
    if local == base:
        return incoming, False
    if incoming == base or local == incoming:
        return local, False

    lines = base.splitlines(keepends=True)
    local_hunks = _hunks(lines, local.splitlines(keepends=True))
    incoming_hunks = _hunks(lines, incoming.splitlines(keepends=True))
    # Each side's non-equal opcodes are ordered and separated by equal
    # base lines. A sweep checks every possible cross-side overlap without
    # comparing unrelated pairs of edits.
    left_index = right_index = 0
    while left_index < len(local_hunks) and right_index < len(incoming_hunks):
        ours = local_hunks[left_index]
        theirs = incoming_hunks[right_index]
        if ours != theirs and _overlap(ours, theirs):
            return local, True
        if ours[1] <= theirs[1]:
            left_index += 1
        if theirs[1] <= ours[1]:
            right_index += 1

    # Identical edits are shared, rather than applied twice. Every other pair
    # is disjoint here, so each hunk still refers to the original base lines.
    hunks = sorted(set(local_hunks + incoming_hunks))
    merged = []
    cursor = 0
    for start, end, replacement in hunks:
        merged.extend(lines[cursor:start])
        merged.extend(replacement)
        cursor = end
    merged.extend(lines[cursor:])
    return "".join(merged), False


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


def _json_object(pairs):
    """Do not silently discard duplicate JSON object members."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("invalid JSON constant: " + value)


def _decode_snapshot(raw):
    try:
        data = json.loads(
            raw, object_pairs_hook=_json_object, parse_constant=_invalid_constant
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("invalid snapshot JSON") from error
    if (
        not isinstance(data, dict)
        or set(data) != {"schema_version", "documents"}
        or type(data["schema_version"]) is not int
        or data["schema_version"] != 1
    ):
        raise ValueError("unsupported snapshot schema")
    values = data["documents"]
    if not isinstance(values, list) or len(values) > MAX_DOCUMENTS:
        raise ValueError("invalid document collection")
    documents = {}
    for value in values:
        name, document = _document(value)
        if name in documents:
            raise ValueError("duplicate document name")
        documents[name] = document
    return documents



def _encode_snapshot(data):
    # Bound serialization memory as well as the final file: a workspace can
    # contain much more working text than one checkpoint is allowed to hold.
    chunks = []
    size = 1  # The terminating newline is included in the byte limit.
    for chunk in json.JSONEncoder(ensure_ascii=False).iterencode(data):
        # Match json.loads(bytes)' surrogate handling for Python strings.
        encoded = chunk.encode("utf-8", "surrogatepass")
        size += len(encoded)
        if size > MAX_BYTES:
            raise ValueError("snapshot too large")
        chunks.append(encoded)
    return b"".join(chunks) + b"\n"


def _snapshot_stat(directory_fd):
    try:
        info = os.stat(
            "workspace.json", dir_fd=directory_fd, follow_symlinks=False
        )
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("snapshot must be a regular file, not a symlink")
    return info


class MergeWorkspace:
    def __init__(self, root):
        try:
            self.root = Path(os.path.abspath(root))
        except (TypeError, ValueError) as error:
            raise ValueError("invalid workspace root") from error
        self._docs = {}
        directory_fd = self._open_root(create=True)
        try:
            info = _snapshot_stat(directory_fd)
            if info is None:
                return
            if info.st_size > MAX_BYTES:
                raise ValueError("snapshot too large")
            snapshot_fd = os.open(
                "workspace.json",
                os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                dir_fd=directory_fd,
            )
            try:
                info = os.fstat(snapshot_fd)
                if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                    raise ValueError("snapshot is not a bounded regular file")
                chunks = []
                remaining = MAX_BYTES + 1
                while remaining:
                    chunk = os.read(snapshot_fd, min(65_536, remaining))
                    if not chunk:
                        break
                    chunks.append(chunk)
                    remaining -= len(chunk)
                raw = b"".join(chunks)
                if len(raw) > MAX_BYTES:
                    raise ValueError("snapshot too large")
            finally:
                os.close(snapshot_fd)
        finally:
            os.close(directory_fd)
        self._docs = _decode_snapshot(raw)

    def _open_root(self, create=False):
        try:
            info = self.root.lstat()
        except FileNotFoundError:
            if not create:
                raise
            self.root.mkdir(exist_ok=True)
            info = self.root.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
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
        if name in self._docs:
            raise ValueError("document name already exists")
        if len(self._docs) >= MAX_DOCUMENTS:
            raise ValueError("document limit exceeded")
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
        merged, conflict = _merge(doc["base"], doc["text"], incoming)
        if conflict:
            doc["conflict"] = {
                "base": doc["base"], "local": doc["text"], "incoming": incoming
            }
        else:
            # Independent edits can produce a result longer than either input.
            # Validate it before advancing the base or changing working text.
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
                raise ValueError("text is only valid for manual resolution")
            resolved = conflict[choice]
        doc.update(base=conflict["incoming"], text=resolved, conflict=None)
        return self.get(name)

    def rename(self, name, new_name):
        doc = self._existing(name)
        new_name = _name(new_name)
        if name == new_name:
            return self.get(name)
        if new_name in self._docs:
            raise ValueError("document name already exists")
        self._docs[new_name] = doc
        del self._docs[name]
        return self.get(new_name)

    def remove(self, name):
        self._existing(name)
        del self._docs[name]

    def save(self):
        data = {
            "schema_version": 1,
            "documents": [dict(name=name, **self._docs[name]) for name in self.names()],
        }
        raw = _encode_snapshot(data)
        directory_fd = self._open_root()
        temporary_name = None
        try:
            _snapshot_stat(directory_fd)
            temporary_fd, temporary_path = tempfile.mkstemp(
                prefix=".workspace-", suffix=".tmp", dir=self.root
            )
            temporary_name = Path(temporary_path).name
            try:
                stream = os.fdopen(temporary_fd, "wb")
            except BaseException:
                os.close(temporary_fd)
                raise
            with stream:
                stream.write(raw)
            os.replace(
                temporary_name, "workspace.json",
                src_dir_fd=directory_fd, dst_dir_fd=directory_fd,
            )
            temporary_name = None
        finally:
            try:
                if temporary_name is not None:
                    try:
                        os.unlink(temporary_name, dir_fd=directory_fd)
                    except FileNotFoundError:
                        pass
            finally:
                os.close(directory_fd)
