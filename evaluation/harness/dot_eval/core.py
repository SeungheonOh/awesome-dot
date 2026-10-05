"""Hashing, explicit input allowlists, and controller-owned append-only records."""
from __future__ import annotations
import datetime as dt
import fcntl
import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath


class IntegrityError(ValueError):
    pass


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        raise IntegrityError(f"Expected a regular, non-symlink file: {path}")
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def relative_path(value):
    p = PurePosixPath(value)
    if not value or value == "." or p.is_absolute() or ".." in p.parts or "\\" in value or str(p) != value:
        raise IntegrityError(f"Unsafe or noncanonical relative path: {value!r}")
    return p


def child(root, relative):
    root = Path(root).resolve()
    p = root / relative_path(relative)
    if not p.resolve().is_relative_to(root):
        raise IntegrityError("Path escapes its declared root")
    for part in (p, *p.parents):
        if part == root:
            break
        if part.is_symlink():
            raise IntegrityError("Symlinks are not permitted in evaluation packets")
    return p


def load_json(path, max_bytes=8 * 1024 * 1024):
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise IntegrityError("JSON document exceeds the declared size limit")
    def no_duplicates(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise IntegrityError(f"Duplicate JSON key: {k}")
            d[k] = v
        return d
    return json.loads(read_regular_file(path, max_bytes=max_bytes).decode("utf-8"), object_pairs_hook=no_duplicates,
                      parse_constant=lambda value: (_ for _ in ()).throw(IntegrityError(f"Invalid number: {value}")))


def create_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(canonical(value) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())


def file_manifest(root):
    """Bounded descriptor-relative collector; never follow links or untrusted paths.

    Reject root/ancestor symlinks, hardlinked files, special files, changing files,
    excessive depth/count/bytes. A verified execution boundary must still stop
    untrusted background writers before collection; this is not that boundary.
    """
    root = Path(root).absolute()
    if not root.exists() and not root.is_symlink():
        return []
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open("/", directory_flags)
    result = []
    total_bytes = 0
    entries_seen = 0
    try:
        for component in root.parts[1:]:
            if component in (".", ".."):
                raise IntegrityError("Noncanonical artifact root")
            next_fd = os.open(component, directory_flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        def walk(directory_fd, prefix, depth):
            nonlocal total_bytes, entries_seen
            if depth > 32:
                raise IntegrityError("Artifact directory depth limit exceeded")
            with os.scandir(directory_fd) as entries:
                names = sorted(entry.name for entry in entries)
            for name in names:
                entries_seen += 1
                if entries_seen > 10000:
                    raise IntegrityError("Artifact entry count limit exceeded")
                info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                relative = prefix + name
                if stat.S_ISDIR(info.st_mode):
                    nested = os.open(name, directory_flags, dir_fd=directory_fd)
                    try:
                        walk(nested, relative + "/", depth + 1)
                    finally:
                        os.close(nested)
                elif stat.S_ISREG(info.st_mode):
                    if info.st_nlink != 1:
                        raise IntegrityError("Hardlinked artifacts are not permitted")
                    if info.st_size > 64 * 1024 * 1024 or total_bytes + info.st_size > 256 * 1024 * 1024:
                        raise IntegrityError("Artifact byte limit exceeded")
                    handle = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory_fd)
                    with os.fdopen(handle, "rb") as stream:
                        before = os.fstat(stream.fileno())
                        if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or (before.st_dev, before.st_ino) != (info.st_dev, info.st_ino):
                            raise IntegrityError("Artifact changed during collection")
                        h = hashlib.sha256()
                        observed = 0
                        while True:
                            chunk = stream.read(min(1024 * 1024, info.st_size - observed + 1))
                            if not chunk:
                                break
                            observed += len(chunk)
                            if observed > info.st_size:
                                raise IntegrityError("Artifact grew during collection")
                            h.update(chunk)
                        after = os.fstat(stream.fileno())
                        if observed != info.st_size or (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                            raise IntegrityError("Artifact changed during collection")
                    total_bytes += observed
                    result.append({"path": relative, "sha256": h.hexdigest(), "bytes": observed})
                else:
                    raise IntegrityError("Symlink or special artifact rejected")
        walk(fd, "", 0)
        return sorted(result, key=lambda value: value["path"])
    except OSError as error:
        raise IntegrityError(f"Artifact traversal/collection failed: {type(error).__name__}") from error
    finally:
        os.close(fd)


class Ledger:
    """Single-host locked append-only hash chain; detects edits, not trusted storage deletion.

    The final head must be retained independently to detect truncation. This is not
    an OS-enforced append-only store or a signature and cannot defeat an adversarial owner.
    """
    def __init__(self, path):
        self.path = Path(path)

    @staticmethod
    def _decode(data):
        records = []
        previous = None
        for number, line in enumerate(data.splitlines(), 1):
            row = json.loads(line)
            claimed = row.pop("record_sha256")
            if row.get("sequence") != number or row.get("previous_sha256") != previous or digest(row) != claimed:
                raise IntegrityError(f"Ledger chain failure at record {number}")
            row["record_sha256"] = claimed
            records.append(row)
            previous = claimed
        return records

    def read(self):
        return self._decode(self.path.read_bytes()) if self.path.exists() else []

    def append(self, event, **payload):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a+b") as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            stream.seek(0)
            rows = self._decode(stream.read())
            row = {"sequence": len(rows) + 1, "previous_sha256": rows[-1]["record_sha256"] if rows else None,
                   "at_utc": utc_now(), "event": event, "payload": payload}
            row["record_sha256"] = digest(row)
            stream.seek(0, os.SEEK_END)
            stream.write(canonical(row) + b"\n")
            stream.flush()
            os.fsync(stream.fileno())
            return row


def read_regular_file(path, max_bytes=64 * 1024 * 1024, expected_sha256=None, expected_bytes=None):
    """Bounded no-follow read through directory descriptors; no caller-selected links."""
    path = Path(path).absolute()
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open("/", directory_flags)
    try:
        for part in path.parts[1:-1]:
            if part in (".", ".."):
                raise IntegrityError("Noncanonical read path")
            next_fd = os.open(part, directory_flags, dir_fd=fd)
            os.close(fd)
            fd = next_fd
        if path.name in ("", ".", ".."):
            raise IntegrityError("Expected a file name")
        handle = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
        with os.fdopen(handle, "rb") as stream:
            before = os.fstat(stream.fileno())
            if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1 or before.st_size > max_bytes:
                raise IntegrityError("Nonregular, hardlinked or oversized file rejected")
            if expected_bytes is not None and before.st_size != expected_bytes:
                raise IntegrityError("File size changed from frozen manifest")
            contents = stream.read(max_bytes + 1)
            after = os.fstat(stream.fileno())
            if len(contents) > max_bytes or len(contents) != before.st_size or (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (after.st_size, after.st_mtime_ns, after.st_ctime_ns):
                raise IntegrityError("File changed during bounded read")
        if expected_sha256 is not None and hashlib.sha256(contents).hexdigest() != expected_sha256:
            raise IntegrityError("File contents differ from frozen manifest")
        return contents
    except OSError as error:
        raise IntegrityError(f"Safe file read failed: {type(error).__name__}") from error
    finally:
        os.close(fd)


def copy_verified_file(source, target, expected_sha256, expected_bytes):
    contents = read_regular_file(source, expected_sha256=expected_sha256, expected_bytes=expected_bytes)
    with Path(target).open("xb") as stream:
        stream.write(contents)
