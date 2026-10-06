"""A local, checkpointable three-way text review workspace.

Merges use exact logical lines and SequenceMatcher's base-relative opcodes.
Saving is a checkpoint, including unfinished edits and unresolved reviews; it
never changes a document's merge base or marks its working text clean.

Limits are 100 documents, 100,000 characters per text, and 2,097,152 snapshot
bytes. Roots are owned, single-process directories. Atomic replacement does
not promise crash durability, concurrent-writer safety, or protection against
adversarial directory replacement. SequenceMatcher can take quadratic time
on repetitive line sequences; its specified alignment is preserved here.
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
    """The outstanding incoming version must be resolved first."""


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
    """Return non-equal opcodes with immutable replacement line sequences."""
    matcher = difflib.SequenceMatcher(a=base, b=variant, autojunk=False)
    return [
        (start, end, tuple(variant[first:last]))
        for operation, start, end, first, last in matcher.get_opcodes()
        if operation != "equal"
    ]


def _overlap(a, b):
    start, end, _ = a
    other_start, other_end, _ = b
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
    left = _hunks(lines, local.splitlines(keepends=True))
    right = _hunks(lines, incoming.splitlines(keepends=True))

    # Each branch's opcodes are ordered, disjoint, and separated by equal
    # spans. A two-way sweep tests every potentially interacting pair without
    # a quadratic cross-product of independent changes.
    i = j = 0
    while i < len(left) and j < len(right):
        ours, theirs = left[i], right[j]
        if ours != theirs and _overlap(ours, theirs):
            return local, True
        if ours[1] < theirs[1]:
            i += 1
        elif theirs[1] < ours[1]:
            j += 1
        else:
            i += 1
            j += 1

    result = []
    cursor = 0
    for start, end, replacement in sorted(
        set(left).union(right), key=lambda hunk: (hunk[0], hunk[1])
    ):
        result.extend(lines[cursor:start])
        result.extend(replacement)
        cursor = end
    result.extend(lines[cursor:])
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
        for content in conflict.values():
            _text(content)
        if conflict["base"] != base or conflict["local"] != text:
            raise ValueError("inconsistent conflict")
        conflict = dict(conflict)
    return name, {"base": base, "text": text, "conflict": conflict}


def _json_object(pairs):
    """Reject duplicate JSON fields instead of silently taking the last one."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate snapshot field")
        result[key] = value
    return result


def _json_constant(value):
    raise ValueError("non-JSON numeric constant")


def _decode_snapshot(raw):
    try:
        data = json.loads(
            raw, object_pairs_hook=_json_object, parse_constant=_json_constant
        )
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("invalid snapshot") from error
    if (
        not isinstance(data, dict)
        or set(data) != {"schema_version", "documents"}
        or type(data["schema_version"]) is not int
        or data["schema_version"] != 1
    ):
        raise ValueError("unsupported snapshot schema")
    documents = data["documents"]
    if not isinstance(documents, list) or len(documents) > MAX_DOCUMENTS:
        raise ValueError("invalid document collection")
    result = {}
    for value in documents:
        name, document = _document(value)
        if name in result:
            raise ValueError("duplicate document name")
        result[name] = document
    return result


def _encode_snapshot(data):
    # Incremental encoding rejects excessive checkpoints before constructing
    # their entire serialized form. No individual text exceeds MAX_TEXT.
    encoder = json.JSONEncoder(ensure_ascii=False, separators=(",", ":"))
    chunks = []
    size = 1  # Include the terminating newline in the byte limit.
    for piece in encoder.iterencode(data):
        # json.loads(bytes) uses the matching surrogatepass decoder. This
        # also preserves exact Python string code points for surrogate text,
        # rather than combining an escaped surrogate pair on reload.
        chunk = piece.encode("utf-8", errors="surrogatepass")
        size += len(chunk)
        if size > MAX_BYTES:
            raise ValueError("snapshot too large")
        chunks.append(chunk)
    return b"".join(chunks) + b"\n"


class MergeWorkspace:
    def __init__(self, root):
        try:
            self.root = Path(os.path.abspath(root))
        except TypeError as error:
            raise ValueError("invalid workspace root") from error
        # Only the root itself may be created; the parent must already exist.
        try:
            self.root.mkdir()
        except FileExistsError:
            pass
        root_fd = self._open_root()
        try:
            self._docs = self._load(root_fd)
        finally:
            os.close(root_fd)

    def _open_root(self):
        mode = self.root.lstat().st_mode
        if not stat.S_ISDIR(mode):
            raise ValueError("workspace root must be a directory, not a symlink")
        return os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    @staticmethod
    def _snapshot_stat(root_fd):
        try:
            info = os.stat("workspace.json", dir_fd=root_fd, follow_symlinks=False)
        except FileNotFoundError:
            return None
        if not stat.S_ISREG(info.st_mode):
            raise ValueError("snapshot must be a regular file, not a symlink")
        return info

    @classmethod
    def _load(cls, root_fd):
        info = cls._snapshot_stat(root_fd)
        if info is None:
            return {}
        if info.st_size > MAX_BYTES:
            raise ValueError("snapshot too large")
        file_fd = os.open(
            "workspace.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
            dir_fd=root_fd,
        )
        try:
            info = os.fstat(file_fd)
            if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_BYTES:
                raise ValueError("snapshot is not a bounded regular file")
            chunks = []
            remaining = MAX_BYTES + 1
            while remaining:
                chunk = os.read(file_fd, min(65_536, remaining))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            raw = b"".join(chunks)
            if len(raw) > MAX_BYTES:
                raise ValueError("snapshot too large")
        finally:
            os.close(file_fd)
        return _decode_snapshot(raw)

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
        self._docs[name] = {
            "base": document["base"], "text": text, "conflict": None
        }
        return self.get(name)

    def receive(self, name, incoming):
        document = self._existing(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending conflict before receiving")
        incoming = _text(incoming)
        base, local = document["base"], document["text"]
        merged, conflicted = _merge(base, local, incoming)
        if conflicted:
            replacement = {
                "base": base,
                "text": local,
                "conflict": {"base": base, "local": local, "incoming": incoming},
            }
        else:
            # Individually valid branches can combine into an oversized text.
            # Validate the result before committing either it or the new base.
            replacement = {"base": incoming, "text": _text(merged), "conflict": None}
        self._docs[name] = replacement
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
                raise ValueError("text is only valid for manual resolution")
            resolved = conflict[choice]
        self._docs[name] = {
            "base": conflict["incoming"], "text": resolved, "conflict": None
        }
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
            "documents": [dict(name=name, **self._docs[name]) for name in self.names()],
        }
        raw = _encode_snapshot(data)

        root_fd = self._open_root()
        temporary = None
        temporary_fd = None
        try:
            self._snapshot_stat(root_fd)
            temporary_fd, temporary = tempfile.mkstemp(
                prefix=".workspace-", suffix=".tmp", dir=self.root
            )
            stream = os.fdopen(temporary_fd, "wb")
            temporary_fd = None  # The stream now owns this descriptor.
            with stream:
                stream.write(raw)
            os.replace(temporary, self.root / "workspace.json")
        finally:
            if temporary_fd is not None:
                os.close(temporary_fd)
            try:
                if temporary is not None:
                    try:
                        os.unlink(temporary)
                    except FileNotFoundError:
                        pass
            finally:
                os.close(root_fd)
