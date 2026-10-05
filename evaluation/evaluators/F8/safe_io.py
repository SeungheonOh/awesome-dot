"""Bounded POSIX tree hashing with descriptor-relative, no-follow regular-file reads.

Adapted from the independently reviewed F5 safe-read approach; never executes files.
"""
import hashlib
import os
from pathlib import Path
import stat

MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_TREE_BYTES = 64 * 1024 * 1024
MAX_ENTRIES = 1024
MAX_DEPTH = 16

class FileIssue(ValueError):
    pass


def tree_hashes(root, *, max_file_bytes=MAX_FILE_BYTES, max_tree_bytes=MAX_TREE_BYTES,
                max_entries=MAX_ENTRIES, max_depth=MAX_DEPTH):
    """Hash a bounded regular-file tree; reject all symlinks including root ancestors."""
    if not all(hasattr(os, flag) for flag in ("O_NOFOLLOW", "O_DIRECTORY", "O_NONBLOCK")):
        raise FileIssue("Safe ingestion requires a POSIX no-follow file-descriptor API")
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    hashes = {}
    counters = {"entries": 0, "bytes": 0}
    root_fd = None

    def walk(directory_fd, relative, depth):
        if depth > max_depth:
            raise FileIssue("Tree exceeds public maximum directory depth")
        # scandir yields entries incrementally rather than materializing an unbounded listing.
        with os.scandir(directory_fd) as entries:
            for entry in entries:
                counters["entries"] += 1
                if counters["entries"] > max_entries:
                    raise FileIssue("Tree exceeds public maximum entry count")
                child = relative / entry.name
                info = entry.stat(follow_symlinks=False)
                if stat.S_ISLNK(info.st_mode):
                    raise FileIssue("Symlink is forbidden: " + str(child))
                if stat.S_ISDIR(info.st_mode):
                    child_fd = os.open(entry.name, directory_flags, dir_fd=directory_fd)
                    try:
                        walk(child_fd, child, depth + 1)
                    finally:
                        os.close(child_fd)
                elif stat.S_ISREG(info.st_mode):
                    file_fd = os.open(entry.name, file_flags, dir_fd=directory_fd)
                    try:
                        actual = os.fstat(file_fd)
                        if not stat.S_ISREG(actual.st_mode):
                            raise FileIssue("Not a regular file: " + str(child))
                        if actual.st_size > max_file_bytes:
                            raise FileIssue("File exceeds public 8 MiB limit: " + str(child))
                        if actual.st_size + counters["bytes"] > max_tree_bytes:
                            raise FileIssue("Tree exceeds public 64 MiB total byte limit")
                        digest = hashlib.sha256()
                        read_bytes = 0
                        while True:
                            remaining = min(max_file_bytes - read_bytes,
                                            max_tree_bytes - counters["bytes"])
                            chunk = os.read(file_fd, min(65536, remaining + 1))
                            if not chunk:
                                break
                            read_bytes += len(chunk)
                            counters["bytes"] += len(chunk)
                            if read_bytes > max_file_bytes or counters["bytes"] > max_tree_bytes:
                                raise FileIssue("File/tree grew beyond public safe-read byte limit")
                            digest.update(chunk)
                        hashes[str(child)] = digest.hexdigest()
                    finally:
                        os.close(file_fd)
                else:
                    raise FileIssue("Not a regular file or directory: " + str(child))
        return hashes

    try:
        absolute = Path(root).absolute()
        root_fd = os.open("/", directory_flags)
        for component in absolute.parts[1:]:
            next_fd = os.open(component, directory_flags, dir_fd=root_fd)
            os.close(root_fd)
            root_fd = next_fd
        return walk(root_fd, Path(), 0)
    except FileIssue:
        raise
    except (OSError, ValueError, TypeError) as error:
        raise FileIssue("Cannot ingest regular non-symlink tree: " + type(error).__name__) from error
    finally:
        if root_fd is not None:
            os.close(root_fd)
