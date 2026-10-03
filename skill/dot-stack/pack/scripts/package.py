#!/usr/bin/env python3
"""Build a deterministic native or single-entry archive from reviewed files only."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import tempfile
import zipfile

EPOCH = (2020, 1, 1, 0, 0, 0)
INVENTORY = 'distribution-files.json'
ENTRYPOINT = 'exports/dot-stack.SKILL.txt'
PRIVATE_NAMES = {'.git', '.aws', '.ssh', '.npmrc', '.pypirc', '.netrc',
                 '.dot-stack', 'node_modules', '__pycache__', '.env', 'credentials'}


def safe_relative(name):
    if not isinstance(name, str):
        raise ValueError('Inventory entries must be relative filenames.')
    relative = PurePosixPath(name)
    if (not name or name == '.' or relative.is_absolute() or '..' in relative.parts
            or '\\' in name or ':' in name or str(relative) != name
            or any(ord(char) < 32 or ord(char) == 127 for char in name)):
        raise ValueError(f'Unsafe inventory path: {name!r}')
    if (any(part in PRIVATE_NAMES or part.startswith('.env.') for part in relative.parts)
            or name.endswith('.log')):
        raise ValueError(f'Private/run-state file cannot enter the distribution: {name}')
    return relative


def open_directory(path, create=False, parent_fd=None):
    """Pin each directory without following aliases, including ancestor races."""
    if not hasattr(os, 'O_NOFOLLOW') or not hasattr(os, 'O_DIRECTORY'):
        raise ValueError('Safe packaging requires POSIX no-follow directory support.')
    if '..' in path.parts:
        raise ValueError('Paths must not contain parent traversal.')
    fd = os.dup(parent_fd) if parent_fd is not None else os.open(path.anchor or '.', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts:
            if part in (path.anchor, '.', ''):
                continue
            if create:
                try:
                    os.mkdir(part, dir_fd=fd)
                except FileExistsError:
                    pass
            try:
                next_fd = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            except OSError as error:
                raise ValueError(f'Directory is missing, unsafe or a symlink: {part}') from error
            os.close(fd)
            fd = next_fd
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_regular(root_fd, name):
    relative = safe_relative(name)
    directory = open_directory(Path(*relative.parts[:-1]), parent_fd=root_fd)
    try:
        try:
            fd = os.open(relative.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
        except OSError as error:
            raise ValueError(f'Missing or unsafe source file: {name}') from error
        with os.fdopen(fd, 'rb') as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise ValueError(f'Expected a regular file: {name}')
            return source.read()
    finally:
        os.close(directory)


def source_entries(root):
    root_fd = open_directory(root.absolute())
    try:
        inventory_bytes = read_regular(root_fd, INVENTORY)
        inventory = json.loads(inventory_bytes)
        if (not isinstance(inventory, dict) or inventory.get('schema_version') != 1
                or not isinstance(inventory.get('files'), list)):
            raise ValueError('Missing or invalid reviewed distribution inventory.')
        entries = inventory['files']
        for name in entries:
            safe_relative(name)
        if len({name.casefold() for name in entries}) != len(entries):
            raise ValueError('Inventory entries must be unique, including case-insensitive names.')
        return [(name, inventory_bytes if name == INVENTORY else read_regular(root_fd, name))
                for name in sorted(set(entries + [INVENTORY]))]
    finally:
        os.close(root_fd)


def check_selected(files, single_entry=False):
    # The checker sees only selected bytes, never an unrelated full checkout.
    with tempfile.TemporaryDirectory(prefix='dot-stack-package-check-') as temporary:
        staged = Path(temporary) / 'dot-stack'
        staged.mkdir()
        for name, data in files:
            target = staged / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        checker = Path(__file__).absolute().parent / 'validate.mjs'
        args = ['node', str(checker), str(staged)]
        if single_entry:
            args.append('--single-entry')
        checked = subprocess.run(args, capture_output=True, text=True)
        if checked.returncode != 0:
            raise ValueError('Selected distribution is incomplete or invalid: ' + checked.stdout + checked.stderr)


def archive_bytes(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, data in sorted(files):
            entry = zipfile.ZipInfo('dot-stack/' + name, EPOCH)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.create_system = 3
            entry.external_attr = (0o100644 << 16)
            archive.writestr(entry, data)
    return buffer.getvalue()


def inspect_archive(data, files, single_entry=False):
    """Inspect and validate actual archived resources, including the root entrypoint."""
    expected = {'dot-stack/' + name: content for name, content in files}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            raise ValueError('Archive inventory mismatch or duplicate member.')
        if archive.testzip() is not None:
            raise ValueError('Archive integrity check failed.')
        actual = []
        for item in archive.infolist():
            safe_relative(item.filename)
            if (not stat.S_ISREG(item.external_attr >> 16) or item.flag_bits & 1
                    or item.date_time != EPOCH):
                raise ValueError(f'Unsafe or noncanonical archive member: {item.filename}')
            content = archive.read(item)
            if content != expected[item.filename]:
                raise ValueError(f'Archive content mismatch: {item.filename}')
            actual.append((item.filename.removeprefix('dot-stack/'), content))
    check_selected(actual, single_entry)


def remove_own(directory_fd, name, identity):
    try:
        current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
        if (current.st_dev, current.st_ino) == identity:
            os.unlink(name, dir_fd=directory_fd)
    except FileNotFoundError:
        pass


def package(root: Path, output: Path, format='native') -> dict:
    if format not in ('native', 'single-entry'):
        raise ValueError(f'Unknown export format: {format}')
    root, output = root.absolute(), output.absolute()
    if '..' in output.parts or '..' in root.parts:
        raise ValueError('Paths must not contain parent traversal.')
    if output.is_relative_to(root):
        raise ValueError('Choose an output outside the source pack.')
    receipt = output.with_suffix(output.suffix + '.manifest.json')
    for candidate in [output, receipt, *output.parents]:
        if candidate.is_symlink():
            raise ValueError(f'Output paths must not contain symlinks: {candidate}')
    library = source_entries(root)
    check_selected(library)
    if format == 'single-entry':
        selected = dict(library)
        if ENTRYPOINT not in selected:
            raise ValueError('Reviewed single-entry template is missing from inventory.')
        files = [('SKILL.md', selected[ENTRYPOINT]), ('LICENSE', selected['LICENSE'])]
        files += [('pack/' + name, data) for name, data in library]
    else:
        files = library
    archive = archive_bytes(files)
    inspect_archive(archive, files, format == 'single-entry')
    manifest = {name: hashlib.sha256(data).hexdigest() for name, data in sorted(files)}
    result = {'archive': output.name, 'format': format,
              'sha256': hashlib.sha256(archive).hexdigest(), 'bytes': len(archive),
              'files': manifest, 'timestamps': 'fixed for reproducibility', 'inventory': INVENTORY}
    if format == 'single-entry':
        result.update({'entrypoint': 'dot-stack/SKILL.md', 'resource_root': 'dot-stack/pack',
                       'library_files': len(library), 'library_bytes': 'preserved exactly'})
    directory_fd = open_directory(output.parent, create=True)
    created = []
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        archive_fd = os.open(output.name, flags, 0o644, dir_fd=directory_fd)
        info = os.fstat(archive_fd)
        created.append((output.name, (info.st_dev, info.st_ino)))
        with os.fdopen(archive_fd, 'wb') as archive_file:
            receipt_fd = os.open(receipt.name, flags, 0o644, dir_fd=directory_fd)
            info = os.fstat(receipt_fd)
            created.append((receipt.name, (info.st_dev, info.st_ino)))
            with os.fdopen(receipt_fd, 'w', encoding='utf-8') as receipt_file:
                archive_file.write(archive)
                archive_file.flush()
                os.fsync(archive_file.fileno())
                json.dump(result, receipt_file, indent=2)
                receipt_file.write('\n')
                receipt_file.flush()
                os.fsync(receipt_file.fileno())
        os.fsync(directory_fd)
        for name, identity in created:
            current = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if (current.st_dev, current.st_ino) != identity:
                raise ValueError(f'Output was replaced during packaging: {name}')
        # A renamed/replaced output directory must not yield a misleading receipt.
        current_fd = open_directory(output.parent)
        try:
            current, pinned = os.fstat(current_fd), os.fstat(directory_fd)
            if (current.st_dev, current.st_ino) != (pinned.st_dev, pinned.st_ino):
                raise ValueError('Output directory changed during packaging.')
        finally:
            os.close(current_fd)
        return result
    except BaseException:
        for name, identity in reversed(created):
            remove_own(directory_fd, name, identity)
        raise
    finally:
        os.close(directory_fd)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--format', choices=['native', 'single-entry'], default='native')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).absolute().parents[1]
    result = package(root, args.output, args.format)
    print(json.dumps({key: value for key, value in result.items() if key != 'files'}, indent=2))


if __name__ == '__main__':
    main()
