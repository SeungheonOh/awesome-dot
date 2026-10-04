"""Focused distribution tests. Synthetic damage never touches the source pack."""
import hashlib
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from package_test import helper

ROOT = Path(__file__).resolve().parents[1]


def fixture(directory):
    root = directory / 'source'
    for name, data in helper.source_entries(ROOT):
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return root


def omit(root, name):
    inventory = root / helper.INVENTORY
    data = json.loads(inventory.read_text())
    data['files'].remove(name)
    inventory.write_text(json.dumps(data))


def digest_tree(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


class ExportTests(unittest.TestCase):
    def test_single_entry_preserves_library_repeatably_and_runs_extracted_helpers(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            first = helper.package(root, directory / 'first.zip', 'single-entry')
            second = helper.package(root, directory / 'second.zip', 'single-entry')
            self.assertEqual(first['sha256'], second['sha256'])
            self.assertEqual(first['resource_root'], 'dot-stack/pack')
            selected = helper.source_entries(root)
            self.assertEqual(first['library_files'], len(selected))
            self.assertEqual(len(first['files']), len(selected) + 2)
            with zipfile.ZipFile(directory / 'first.zip') as archive:
                self.assertEqual(archive.read('dot-stack/LICENSE'), (root / 'LICENSE').read_bytes())
                for name, data in selected:
                    self.assertEqual(archive.read('dot-stack/pack/' + name), data, name)
                extracted = directory / 'extracted'
                archive.extractall(extracted)
            skill = extracted / 'dot-stack'
            before = digest_tree(skill)
            for args in [
                ['node', 'pack/scripts/validate.mjs', str(skill), '--single-entry'],
                ['node', 'pack/tools/dot-stack.mjs', '--help'],
                ['node', 'pack/tools/dot-stack.mjs', 'doctor'],
            ]:
                result = subprocess.run(args, cwd=skill, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(digest_tree(skill), before)

    def test_unlisted_files_are_excluded_in_both_formats(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            for name in ['private-note.txt', '.env', 'old-output.zip', 'run.log']:
                (root / name).write_text('private fixture')
            for format in ['native', 'single-entry']:
                result = helper.package(root, directory / (format + '.zip'), format)
                self.assertFalse(any('private-note' in name or name.endswith('.zip') for name in result['files']))

    def test_missing_reviewed_resources_and_helper_imports_fail(self):
        for name in ['skills/dot-mode/references/execution-contract.md', 'tools/lib/core.mjs', helper.ENTRYPOINT]:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                root = fixture(directory)
                omit(root, name)  # File still exists in checkout; it is absent from selected bytes.
                with self.assertRaises(ValueError):
                    helper.package(root, directory / 'out.zip', 'single-entry')
                self.assertFalse((directory / 'out.zip').exists())

    def test_invalid_root_metadata_and_bad_resource_links_fail(self):
        original = (ROOT / helper.ENTRYPOINT).read_text()
        variants = [
            original.replace('name: dot-stack', 'name: other'),
            original.replace('name: dot-stack', 'name: dot-stack\nname: duplicate'),
            original.replace('name: dot-stack', 'name: dot-stack\nallowed-tools: "shell"'),
            original.replace('description: "Use dot-stack', 'description: "' + 'x' * 201),
            original.replace('(pack/tools/README.md)', '(pack/tools/missing.md)'),
            original.replace('(pack/tools/README.md)', '(../outside.md)'),
            original.replace('(pack/tools/README.md)', '(%2e%2e/outside.md)'),
            original.replace('(pack/tools/README.md)', '(pack\\tools\\README.md)'),
        ]
        for text in variants:
            with self.subTest(text=text[:80]), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                root = fixture(directory)
                (root / helper.ENTRYPOINT).write_text(text)
                with self.assertRaises(ValueError):
                    helper.package(root, directory / 'out.zip', 'single-entry')
                self.assertFalse((directory / 'out.zip').exists())

    def test_unsafe_inventory_paths_private_names_and_case_collisions_fail(self):
        for extra in ['../outside', '/outside', 'a\\b', 'a:b', './README.md',
                      'a//b', '.', 'a\x00b', 'a\nb', '.env.local', 'run.log', 'readme.md']:
            with self.subTest(extra=extra), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                root = fixture(directory)
                inventory = root / helper.INVENTORY
                data = json.loads(inventory.read_text())
                data['files'].append(extra)
                inventory.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    helper.package(root, directory / 'out.zip', 'single-entry')

    def test_source_root_parent_file_symlinks_and_special_files_fail(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            alias = directory / 'alias'
            alias.symlink_to(root, target_is_directory=True)
            with self.assertRaises(ValueError):
                helper.package(alias, directory / 'out.zip', 'single-entry')
            target = root / 'README.md'
            data = target.read_bytes()
            target.unlink()
            target.symlink_to(directory / 'missing')
            with self.assertRaises(ValueError):
                helper.package(root, directory / 'out.zip', 'single-entry')
            target.unlink()
            os.mkfifo(target)
            with self.assertRaises(ValueError):
                helper.package(root, directory / 'out.zip', 'single-entry')
            target.unlink()
            target.write_bytes(data)
            (root / 'exports').rename(root / 'held-exports')
            (root / 'exports').symlink_to(root / 'held-exports', target_is_directory=True)
            with self.assertRaises(ValueError):
                helper.package(root, directory / 'out.zip', 'single-entry')

    def test_output_collisions_and_aliases_preserve_existing_bytes(self):
        for collision in ['out.zip', 'out.zip.manifest.json']:
            with self.subTest(collision=collision), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                root = fixture(directory)
                existing = directory / collision
                existing.write_bytes(b'pre-existing evidence')
                with self.assertRaises(FileExistsError):
                    helper.package(root, directory / 'out.zip', 'single-entry')
                self.assertEqual(existing.read_bytes(), b'pre-existing evidence')
                other = 'out.zip' if collision.endswith('.json') else 'out.zip.manifest.json'
                self.assertFalse((directory / other).exists())
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            target = directory / 'target'
            target.mkdir()
            alias = directory / 'alias'
            alias.symlink_to(target, target_is_directory=True)
            with self.assertRaises(ValueError):
                helper.package(root, alias / 'out.zip', 'single-entry')
            self.assertEqual(list(target.iterdir()), [])
            for output in [root / 'self.zip', directory / 'target/../out.zip']:
                with self.assertRaises(ValueError):
                    helper.package(root, output, 'single-entry')

    def test_interrupted_receipt_cleans_only_owned_new_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            preserved = directory / 'other.zip'
            preserved.write_bytes(b'previous candidate')
            with patch.object(helper.json, 'dump', side_effect=KeyboardInterrupt):
                with self.assertRaises(KeyboardInterrupt):
                    helper.package(root, directory / 'out.zip', 'single-entry')
            self.assertFalse((directory / 'out.zip').exists())
            self.assertFalse((directory / 'out.zip.manifest.json').exists())
            self.assertEqual(preserved.read_bytes(), b'previous candidate')

    def test_failure_cleanup_preserves_replacement_file(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            output = directory / 'out.zip'
            def interrupt(*args, **kwargs):
                output.unlink()
                output.write_bytes(b'another writers replacement')
                raise RuntimeError('injected receipt failure')
            with patch.object(helper.json, 'dump', side_effect=interrupt):
                with self.assertRaises(RuntimeError):
                    helper.package(root, output, 'single-entry')
            self.assertEqual(output.read_bytes(), b'another writers replacement')
            self.assertFalse((directory / 'out.zip.manifest.json').exists())

    def test_parent_alias_swap_does_not_redirect_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = fixture(directory)
            destination = directory / 'destination'
            destination.mkdir()
            outside = directory / 'outside'
            outside.mkdir()
            held = directory / 'held'
            original_open = helper.os.open
            def swap(name, flags, *args, **kwargs):
                if name == 'out.zip' and flags & os.O_CREAT:
                    destination.rename(held)
                    destination.symlink_to(outside, target_is_directory=True)
                return original_open(name, flags, *args, **kwargs)
            with patch.object(helper.os, 'open', side_effect=swap):
                with self.assertRaises(ValueError):
                    helper.package(root, destination / 'out.zip', 'single-entry')
            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(list(held.iterdir()), [])

    def test_archive_tampering_is_rejected_before_output_creation(self):
        original = helper.archive_bytes
        def change_archive(files, mode):
            data = original(files)
            with zipfile.ZipFile(io.BytesIO(data)) as source:
                entries = [(item, source.read(item)) for item in source.infolist()]
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, 'w') as target:
                for index, (item, data) in enumerate(entries):
                    if index == 0:
                        if mode == 'missing':
                            continue
                        if mode == 'changed':
                            data += b'changed'
                        if mode == 'symlink':
                            item.external_attr = (stat.S_IFLNK | 0o777) << 16
                    target.writestr(item, data)
                if mode == 'extra':
                    target.writestr('dot-stack/private-note.txt', 'private')
                if mode == 'duplicate':
                    target.writestr(entries[0][0], entries[0][1])
            return buffer.getvalue()
        for mode in ['missing', 'changed', 'symlink', 'extra', 'duplicate']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                root = fixture(directory)
                with patch.object(helper, 'archive_bytes', side_effect=lambda files: change_archive(files, mode)):
                    with self.assertRaises(ValueError):
                        helper.package(root, directory / 'out.zip', 'single-entry')
                self.assertFalse((directory / 'out.zip').exists())


if __name__ == '__main__':
    unittest.main()
