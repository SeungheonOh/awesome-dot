"""A bounded, local text workspace with explicit three-way review state.

The workspace owns its root directory. Operations are single-process; concurrent
writers and adversarial directory replacement races are outside the contract.
All persistence uses the standard library and save never changes live documents.
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
    """An unresolved incoming version must be resolved before another edit."""


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
    """Return exactly the specified SequenceMatcher hunks in base coordinates."""
    matcher = difflib.SequenceMatcher(a=base, b=variant, autojunk=False)
    return [
        (start, end, tuple(variant[left:right]))
        for operation, start, end, left, right in matcher.get_opcodes()
        if operation != "equal"
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
    ours = _hunks(lines, local.splitlines(keepends=True))
    theirs = _hunks(lines, incoming.splitlines(keepends=True))
    for left in ours:
        for right in theirs:
            # An identical edit, including an insertion, is applied just once.
            if left != right and _overlap(left, right):
                return local, True

    combined = sorted(set(ours).union(theirs), key=lambda hunk: (hunk[0], hunk[1]))
    result = []
    cursor = 0
    for start, end, replacement in combined:
        result.extend(lines[cursor:start])
        result.extend(replacement)
        cursor = end
    result.extend(lines[cursor:])
    return "".join(result), False


def _document(value):
    if not isinstance(value, dict) or set(value) != {"name", "base", "text", "conflict"}:
        raise ValueError("invalid document fields")
    name = _name(value["name"])
    base = _text(value["base"])
    text = _text(value["text"])
    conflict = value["conflict"]
    if conflict is not None:
        if not isinstance(conflict, dict) or set(conflict) != {"base", "local", "incoming"}:
            raise ValueError("invalid conflict fields")
        conflict = {key: _text(conflict[key]) for key in ("base", "local", "incoming")}
        if conflict["base"] != base or conflict["local"] != text:
            raise ValueError("inconsistent conflict")
    return name, {"base": base, "text": text, "conflict": conflict}


def _json_object(pairs):
    """Reject duplicate JSON fields rather than silently taking the last one."""
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
    # Bound the accumulated encoding as well as the eventual file. In
    # particular, do not build a huge snapshot merely to discover it is large.
    encoder = json.JSONEncoder(ensure_ascii=False, separators=(",", ":"))
    chunks = []
    size = 1  # The final newline is part of the snapshot byte limit.
    for chunk in encoder.iterencode(data):
        # Non-ASCII text stays compact. Surrogates, which UTF-8 cannot encode,
        # use the JSON-compatible backslash-u escapes instead.
        encoded = chunk.encode("utf-8", errors="backslashreplace")
        size += len(encoded)
        if size > MAX_BYTES:
            raise ValueError("snapshot too large")
        chunks.append(encoded)
    return b"".join(chunks) + b"\n"


def _open_root(root, create=False):
    try:
        info = root.lstat()
    except FileNotFoundError:
        if not create:
            raise
        root.mkdir()
        info = root.lstat()
    # lstat deliberately does not accept a symlink to a directory.
    if not stat.S_ISDIR(info.st_mode):
        raise ValueError("workspace root must be a real directory")
    return os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)


def _snapshot_info(root_fd):
    try:
        info = os.stat("workspace.json", dir_fd=root_fd, follow_symlinks=False)
    except FileNotFoundError:
        return None
    if not stat.S_ISREG(info.st_mode):
        raise ValueError("snapshot must be a regular file, not a symlink")
    return info


def _load(root_fd):
    info = _snapshot_info(root_fd)
    if info is None:
        return {}
    if info.st_size > MAX_BYTES:
        raise ValueError("snapshot too large")
    fd = os.open(
        "workspace.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=root_fd
    )
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
            raise ValueError("snapshot is not a bounded regular file")
        chunks = []
        remaining = MAX_BYTES + 1
        while remaining:
            chunk = os.read(fd, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        raw = b"".join(chunks)
        if len(raw) > MAX_BYTES:
            raise ValueError("snapshot too large")
    finally:
        os.close(fd)
    return _decode_snapshot(raw)


class MergeWorkspace:
    def __init__(self, root):
        try:
            self.root = Path(os.path.abspath(root))
        except (TypeError, ValueError) as error:
            raise ValueError("invalid workspace root") from error
        root_fd = _open_root(self.root, create=True)
        try:
            self._docs = _load(root_fd)
        finally:
            os.close(root_fd)

    def _lookup(self, name):
        return self._docs[_name(name)]

    def names(self):
        return sorted(self._docs)

    def get(self, name):
        document = self._lookup(name)
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
            raise ValueError("document name already exists")
        if len(self._docs) >= MAX_DOCUMENTS:
            raise ValueError("document limit exceeded")
        self._docs[name] = {"base": text, "text": text, "conflict": None}
        return self.get(name)

    def edit(self, name, text):
        document = self._lookup(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before editing")
        text = _text(text)
        document["text"] = text
        return self.get(name)

    def receive(self, name, incoming):
        document = self._lookup(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before receiving")
        incoming = _text(incoming)
        merged, conflict = _merge(document["base"], document["text"], incoming)
        if conflict:
            document["conflict"] = {
                "base": document["base"],
                "local": document["text"],
                "incoming": incoming,
            }
        else:
            # Separate valid input versions can produce an oversized union.
            # Validate that union before changing either base or working text.
            merged = _text(merged)
            document.update(base=incoming, text=merged, conflict=None)
        return self.get(name)

    def resolve(self, name, choice, text=None):
        document = self._lookup(name)
        conflict = document["conflict"]
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
        document.update(base=conflict["incoming"], text=resolved, conflict=None)
        return self.get(name)

    def rename(self, name, new_name):
        document = self._lookup(name)
        new_name = _name(new_name)
        if new_name == name:
            return self.get(name)
        if new_name in self._docs:
            raise ValueError("document name already exists")
        self._docs[new_name] = document
        del self._docs[name]
        return self.get(new_name)

    def remove(self, name):
        self._lookup(name)
        del self._docs[name]

    def save(self):
        data = {
            "schema_version": 1,
            "documents": [dict(name=name, **self._docs[name]) for name in self.names()],
        }
        raw = _encode_snapshot(data)

        root_fd = _open_root(self.root)
        try:
            _snapshot_info(root_fd)
            fd, temporary = tempfile.mkstemp(prefix=".workspace-", suffix=".tmp", dir=self.root)
            try:
                # fdopen owns the descriptor after it succeeds.
                try:
                    stream = os.fdopen(fd, "wb")
                except BaseException:
                    os.close(fd)
                    raise
                with stream:
                    stream.write(raw)
                os.replace(temporary, self.root / "workspace.json")
            finally:
                try:
                    os.unlink(temporary)
                except FileNotFoundError:
                    pass
        finally:
            os.close(root_fd)
