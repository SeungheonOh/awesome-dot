"""A local review workspace with exact line-based three-way merges.

Dirty state is derived from working text and its upstream base. Saving is a
checkpoint, including unresolved reviews; it never accepts or resolves edits.
Only the Python standard library is used. Importing this module performs no I/O.
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
    """An existing incoming revision must be resolved before editing again."""


def _name(value):
    if (not isinstance(value, str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", value) is None):
        raise ValueError("invalid document name")
    return value


def _text(value):
    if not isinstance(value, str) or len(value) > MAX_TEXT:
        raise ValueError("text must be a string of at most 100000 characters")
    return value


def _hunks(base, variant):
    matcher = difflib.SequenceMatcher(a=base, b=variant, autojunk=False)
    return [(start, end, tuple(variant[left:right]))
            for operation, start, end, left, right in matcher.get_opcodes()
            if operation != "equal"]


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

    original = base.splitlines(keepends=True)
    ours = _hunks(original, local.splitlines(keepends=True))
    theirs = _hunks(original, incoming.splitlines(keepends=True))

    # Each side's opcodes are ordered, with unchanged base lines separating
    # its hunks. A sweep therefore checks every potentially conflicting pair.
    left = right = 0
    while left < len(ours) and right < len(theirs):
        first, second = ours[left], theirs[right]
        if first != second and _overlap(first, second):
            return local, True
        if first[1] < second[1]:
            left += 1
        elif second[1] < first[1]:
            right += 1
        else:
            left += 1
            right += 1

    result = []
    cursor = 0
    for start, end, replacement in sorted(set(ours + theirs)):
        result.extend(original[cursor:start])
        result.extend(replacement)
        cursor = end
    result.extend(original[cursor:])
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
        for item in conflict.values():
            _text(item)
        if conflict["base"] != base or conflict["local"] != text:
            raise ValueError("inconsistent conflict")
        conflict = dict(conflict)
    return name, {"base": base, "text": text, "conflict": conflict}


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key")
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError("invalid JSON constant: " + value)


def _decode_snapshot(raw):
    try:
        data = json.loads(raw, object_pairs_hook=_unique_object,
                          parse_constant=_invalid_constant)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise ValueError("invalid snapshot JSON") from error
    if (not isinstance(data, dict)
            or set(data) != {"schema_version", "documents"}
            or type(data["schema_version"]) is not int
            or data["schema_version"] != 1):
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


class MergeWorkspace:
    def __init__(self, root):
        try:
            self.root = Path(os.path.abspath(root))
        except (TypeError, ValueError) as error:
            raise ValueError("invalid workspace root") from error
        # Do not let mkdir(exist_ok=True) accept an existing directory symlink.
        if self.root.is_symlink():
            raise ValueError("workspace root must not be a symlink")
        self.root.mkdir(exist_ok=True)
        self._docs = {}
        root_fd = self._open_root()
        try:
            try:
                information = os.stat("workspace.json", dir_fd=root_fd,
                                      follow_symlinks=False)
            except FileNotFoundError:
                return
            self._check_snapshot_file(information)
            snapshot_fd = os.open("workspace.json", os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
                                  dir_fd=root_fd)
            try:
                self._check_snapshot_file(os.fstat(snapshot_fd))
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
            os.close(root_fd)
        self._docs = _decode_snapshot(raw)

    def _open_root(self):
        if self.root.is_symlink():
            raise ValueError("workspace root must not be a symlink")
        return os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)

    @staticmethod
    def _check_snapshot_file(information):
        if not stat.S_ISREG(information.st_mode):
            raise ValueError("snapshot must be a regular file")
        if information.st_size > MAX_BYTES:
            raise ValueError("snapshot too large")

    def _existing(self, name):
        return self._docs[_name(name)]

    def names(self):
        return sorted(self._docs)

    def get(self, name):
        document = self._existing(name)
        conflict = document["conflict"]
        return {"base": document["base"], "text": document["text"],
                "dirty": document["text"] != document["base"],
                "conflict": None if conflict is None else dict(conflict)}

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
        document = self._existing(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending incoming revision before editing")
        text = _text(text)
        document["text"] = text
        return self.get(name)

    def receive(self, name, incoming):
        document = self._existing(name)
        if document["conflict"] is not None:
            raise ConflictPending("resolve the pending incoming revision first")
        incoming = _text(incoming)
        merged, conflict = _merge(document["base"], document["text"], incoming)
        if conflict:
            document["conflict"] = {"base": document["base"],
                                    "local": document["text"], "incoming": incoming}
        else:
            _text(merged)
            document.update(base=incoming, text=merged, conflict=None)
        return self.get(name)

    def resolve(self, name, choice, text=None):
        document = self._existing(name)
        conflict = document["conflict"]
        if conflict is None:
            raise ValueError("no pending conflict")
        if not isinstance(choice, str) or choice not in ("local", "incoming", "manual"):
            raise ValueError("invalid resolution choice")
        if choice == "manual":
            resolved = _text(text)
        else:
            if text is not None:
                raise ValueError("text is only valid for manual resolution")
            resolved = conflict[choice]
        document.update(base=conflict["incoming"], text=resolved, conflict=None)
        return self.get(name)

    def rename(self, name, new_name):
        document = self._existing(name)
        new_name = _name(new_name)
        if new_name == name:
            return self.get(name)
        if new_name in self._docs:
            raise ValueError("document name already exists")
        self._docs[new_name] = document
        del self._docs[name]
        return self.get(new_name)

    def remove(self, name):
        self._existing(name)
        del self._docs[name]

    def save(self):
        data = {"schema_version": 1,
                "documents": [dict(name=name, **self._docs[name]) for name in self.names()]}
        # ASCII escaping also permits Python strings containing lone surrogates.
        raw = (json.dumps(data, ensure_ascii=True, separators=(",", ":")) + "\n").encode("utf-8")
        if len(raw) > MAX_BYTES:
            raise ValueError("snapshot too large")

        root_fd = self._open_root()
        temporary_name = None
        try:
            try:
                information = os.stat("workspace.json", dir_fd=root_fd,
                                      follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                if not stat.S_ISREG(information.st_mode):
                    raise ValueError("snapshot destination must be regular")
            descriptor, temporary_path = tempfile.mkstemp(prefix=".workspace-", suffix=".tmp",
                                                          dir=self.root)
            temporary_name = os.path.basename(temporary_path)
            try:
                remaining = memoryview(raw)
                while remaining:
                    written = os.write(descriptor, remaining)
                    if written == 0:
                        raise OSError("snapshot write made no progress")
                    remaining = remaining[written:]
            finally:
                os.close(descriptor)
            os.replace(temporary_name, "workspace.json", src_dir_fd=root_fd, dst_dir_fd=root_fd)
            temporary_name = None
        finally:
            try:
                if temporary_name is not None:
                    try:
                        os.unlink(temporary_name, dir_fd=root_fd)
                    except FileNotFoundError:
                        pass
            finally:
                os.close(root_fd)
