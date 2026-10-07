"""Trusted bounded JSON reads. Candidate bytes are data, never imported or executed."""
import json
import os
import stat

class ArtifactError(ValueError):
    pass

def reject(message):
    raise ArtifactError(message)

def exact(obj, keys):
    if type(obj) is not dict or set(obj) != set(keys):
        reject('object keys do not match schema')

def bounded_text(value, limit=64, allow_empty=False):
    if type(value) is not str or len(value) > limit or (not allow_empty and not value):
        reject('invalid bounded string')
    if any(ord(char) < 32 for char in value):
        reject('control characters are not allowed')

def unique_pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            reject('duplicate JSON object key')
        out[key] = value
    return out

def read_artifact(path, max_bytes=65536, dir_fd=None):
    # Open supplied file once; reject final-component links and non-regular files.
    # The coordinator must supply a private staging directory without symlink parents.
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    try:
        fd = os.open(path, flags, dir_fd=dir_fd)
        with os.fdopen(fd, 'rb') as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode):
                reject('artifact is not a regular file')
            if info.st_size > max_bytes:
                reject('artifact exceeds byte bound')
            raw = stream.read(max_bytes + 1)
        if len(raw) > max_bytes:
            reject('artifact exceeds byte bound')
        text = raw.decode('utf-8')
        # Limit nesting before the recursive JSON parser sees input.
        depth = 0
        quoted = escaped = False
        for char in text:
            if quoted:
                if escaped: escaped = False
                elif char == '\\': escaped = True
                elif char == '"': quoted = False
            elif char == '"': quoted = True
            elif char in '[{':
                depth += 1
                if depth > 12: reject('artifact exceeds nesting bound')
            elif char in ']}': depth -= 1
        return json.loads(text, object_pairs_hook=unique_pairs,
                          parse_constant=lambda value: reject('non-finite JSON number'))
    except ArtifactError:
        raise
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise ArtifactError('cannot read valid bounded JSON') from error


def read_candidate(project_root, components):
    """Discover a fixed relative artifact without following any candidate symlinks."""
    directory = None
    try:
        directory = os.open(project_root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        for component in components[:-1]:
            next_directory = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                     dir_fd=directory)
            os.close(directory)
            directory = next_directory
        return read_artifact(components[-1], dir_fd=directory)
    except ArtifactError:
        raise
    except OSError as error:
        raise ArtifactError('artifact not discovered at required safe path') from error
    finally:
        if directory is not None:
            os.close(directory)
