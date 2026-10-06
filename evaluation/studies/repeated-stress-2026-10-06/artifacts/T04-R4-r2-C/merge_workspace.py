"""An offline, line-based review workspace with atomic JSON checkpoints.

All filesystem operations are confined to the explicitly supplied workspace root.
The root is owned by the caller; concurrent writers and directory replacement
races are outside this module's contract. Importing the module creates no files.
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
    """A pending review must be resolved before editing or receiving again."""


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


def _hunks(base_lines, variant_lines):
    matcher = difflib.SequenceMatcher(
        a=base_lines, b=variant_lines, autojunk=False
    )
    return [
        (start, end, tuple(variant_lines[a:b]))
        for operation, start, end, a, b in matcher.get_opcodes()
        if operation != "equal"
    ]


def _overlap(left, right):
    start, end, _ = left
    other_start, other_end, _ = right
    if start == end and other_start == other_end:
        return start == other_start
    if start == end:
        return other_start <= start <= other_end
    if other_start == other_end:
        return start <= other_start <= end
    return max(start, other_start) < min(end, other_end)


def _merge(base, local, incoming):
    """Return (working text, has_conflict), without changing any state."""
    if local == base:
        return incoming, False
    if incoming == base or local == incoming:
        return local, False

    base_lines = base.splitlines(keepends=True)
    local_hunks = _hunks(base_lines, local.splitlines(keepends=True))
    incoming_hunks = _hunks(base_lines, incoming.splitlines(keepends=True))
    for ours in local_hunks:
        for theirs in incoming_hunks:
            if ours != theirs and _overlap(ours, theirs):
                return local, True

    # Identical hunks count once. All remaining hunks have compatible base
    # coordinates; in particular, no insertion touches another side's range.
    hunks = sorted(set(local_hunks + incoming_hunks), key=lambda h: (h[0], h[1]))
    result = []
    cursor = 0
    for start, end, replacement in hunks:
        result.extend(base_lines[cursor:start])
        result.extend(replacement)
        cursor = end
    result.extend(base_lines[cursor:])
    return "".join(result), False


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
        conflict = {key: _text(conflict[key]) for key in ("base", "local", "incoming")}
        if conflict["base"] != base or conflict["local"] != text:
            raise ValueError("inconsistent conflict")
    return name, {"base": base, "text": text, "conflict": conflict}


def _unique_object(pairs):
    """Reject duplicate JSON fields instead of silently dropping an entry."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("non-JSON numeric constant: " + value)


def _decode_snapshot(raw):
    try:
        data = json.loads(
            raw, object_pairs_hook=_unique_object, parse_constant=_invalid_constant
        )
    except (json.JSONDecodeError, UnicodeError, RecursionError) as error:
        raise ValueError("invalid snapshot JSON") from error
    if (
        not isinstance(data, dict)
        or set(data) != {"schema_version", "documents"}
        or type(data["schema_version"]) is not int
        or data["schema_version"] != 1
    ):
        raise ValueError("unsupported snapshot schema")
    if not isinstance(data["documents"], list) or len(data["documents"]) > MAX_DOCUMENTS:
        raise ValueError("invalid document collection")
    documents = {}
    for value in data["documents"]:
        name, document = _document(value)
        if name in documents:
            raise ValueError("duplicate document name")
        documents[name] = document
    return documents


def _encode_snapshot(data):
    """Bound serialized bytes before opening or changing any checkpoint file."""
    chunks = []
    size = 1  # Reserve the final newline.
    encoder = json.JSONEncoder(ensure_ascii=False, separators=(",", ":"))
    for chunk in encoder.iterencode(data):
        # Escape lone surrogate code points while retaining ordinary UTF-8.
        raw = chunk.encode("utf-8", errors="backslashreplace")
        size += len(raw)
        if size > MAX_BYTES:
            raise ValueError("snapshot too large")
        chunks.append(raw)
    return b"".join(chunks) + b"\n"


def _snapshot_status(root_fd):
    """Inspect the final directory entry without following a symlink."""
    try:
        status = os.stat("workspace.json", dir_fd=root_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(status.st_mode):
        raise ValueError("snapshot must be a regular file, not a symlink")
    return status


def _read_snapshot(root_fd):
    status = _snapshot_status(root_fd)
    if status is None:
        return None
    if status.st_size > MAX_BYTES:
        raise ValueError("snapshot too large")
    snapshot_fd = os.open(
        "workspace.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=root_fd
    )
    try:
        status = os.fstat(snapshot_fd)
        if not stat.S_ISREG(status.st_mode) or status.st_size > MAX_BYTES:
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
        return raw
    finally:
        os.close(snapshot_fd)


class MergeWorkspace:
    def __init__(self, root):
        try:
            self.root = Path(os.path.abspath(root))
        except (TypeError, ValueError) as error:
            raise ValueError("invalid workspace root") from error
        self._docs = {}
        root_fd = self._open_root(create=True)
        try:
            raw = _read_snapshot(root_fd)
        finally:
            os.close(root_fd)
        if raw is not None:
            self._docs = _decode_snapshot(raw)

    def _open_root(self, create=False):
        try:
            status = self.root.lstat()
        except FileNotFoundError:
            if not create:
                raise
            # Only the root itself may be created; its parent must exist.
            self.root.mkdir()
            status = self.root.lstat()
        if stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise ValueError("workspace root must be a directory, not a symlink")
        return os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    def _existing(self, name):
        return self._docs[_name(name)]

    def names(self):
        return sorted(self._docs)

    def get(self, name):
        document = self._existing(name)
        conflict = document["conflict"]
        return {
            "base": document["base"],
            "text": document["text"],
            "dirty": document["text"] != document["base"],
            "conflict": None if conflict is None else dict(conflict),
        }

    def add(self, name, text):
        name = _name(name)
        text = _text(text)
        if name in self._docs:
            raise ValueError("document name exists")
        if len(self._docs) >= MAX_DOCUMENTS:
            raise ValueError("document limit exceeded")
        self._docs[name] = {"base": text, "text": text, "conflict": None}
        return self.get(name)

    def edit(self, name, text):
        document = self._existing(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before editing")
        text = _text(text)
        document["text"] = text
        return self.get(name)

    def receive(self, name, incoming):
        document = self._existing(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before receiving")
        incoming = _text(incoming)
        merged, has_conflict = _merge(document["base"], document["text"], incoming)
        if has_conflict:
            document["conflict"] = {
                "base": document["base"],
                "local": document["text"],
                "incoming": incoming,
            }
        else:
            # Independent changes can combine into an oversized working text.
            # Check the result before changing either the text or the base.
            merged = _text(merged)
            document.update(base=incoming, text=merged, conflict=None)
        return self.get(name)

    def resolve(self, name, choice, text=None):
        document = self._existing(name)
        conflict = document["conflict"]
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
        document.update(base=conflict["incoming"], text=resolved, conflict=None)
        return self.get(name)

    def rename(self, name, new_name):
        document = self._existing(name)
        new_name = _name(new_name)
        if new_name == name:
            return self.get(name)
        if new_name in self._docs:
            raise ValueError("document name exists")
        self._docs[new_name] = document
        del self._docs[name]
        return self.get(new_name)

    def remove(self, name):
        self._existing(name)
        del self._docs[name]

    def save(self):
        data = {
            "schema_version": 1,
            "documents": [
                {"name": name, **self._docs[name]} for name in self.names()
            ],
        }
        raw = _encode_snapshot(data)

        root_fd = self._open_root()
        temporary_path = None
        temporary_fd = None
        try:
            _snapshot_status(root_fd)
            temporary_fd, temporary_path = tempfile.mkstemp(
                prefix=".workspace-", suffix=".tmp", dir=self.root
            )
            with os.fdopen(temporary_fd, "wb") as stream:
                temporary_fd = None  # The context manager now owns this fd.
                stream.write(raw)
            os.replace(temporary_path, self.root / "workspace.json")
        finally:
            try:
                if temporary_fd is not None:
                    os.close(temporary_fd)
            finally:
                try:
                    if temporary_path is not None:
                        try:
                            os.unlink(temporary_path)
                        except FileNotFoundError:
                            pass  # Successful replacement consumed the temp file.
                finally:
                    os.close(root_fd)
