#!/usr/bin/env python3
"""Authored verifier filesystem controls only; no agents, SQL or graders."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).absolute().parent
spec = importlib.util.spec_from_file_location('saved_verifier', ROOT / 'verify.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

class InventoryControls(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='.verifier-test-', dir=ROOT)
        self.root = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        (self.root / 'sample.txt').write_bytes(b'public fictional fixture\n')
        self.freeze()

    def freeze(self):
        files = {}
        for p in self.root.rglob('*'):
            if p.is_file() and p.name != 'MANIFEST.json':
                data = p.read_bytes()
                files[p.relative_to(self.root).as_posix()] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
        (self.root / 'MANIFEST.json').write_text(json.dumps({'schema': 'transfer-saved-evidence-v1', 'files': files}))

    def test_positive_inventory(self):
        blobs, digest = v.inventory(self.root)
        self.assertEqual(set(blobs), {'sample.txt'})
        self.assertEqual(len(digest), 64)

    def test_positive_external_digest(self):
        digest = hashlib.sha256((self.root / 'MANIFEST.json').read_bytes()).hexdigest()
        self.assertEqual(v.inventory(self.root, digest)[1], digest)

    def test_wrong_external_digest(self):
        with self.assertRaises(v.Invalid):
            v.inventory(self.root, '0' * 64)

    def test_missing_file(self):
        (self.root / 'sample.txt').unlink()
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_extra_file(self):
        (self.root / 'extra.txt').write_text('extra')
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_changed_byte(self):
        (self.root / 'sample.txt').write_bytes(b'changed fixture\n')
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_symlink_leaf(self):
        (self.root / 'copy.txt').symlink_to('sample.txt')
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_symlink_directory(self):
        (self.root / 'inside').mkdir()
        (self.root / 'alias').symlink_to('inside', target_is_directory=True)
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_hardlink(self):
        os.link(self.root / 'sample.txt', self.root / 'linked.txt')
        self.freeze()
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_nonregular_entry(self):
        if not hasattr(os, 'mkfifo'):
            self.skipTest('FIFO unavailable')
        os.mkfifo(self.root / 'pipe')
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_oversize_file(self):
        (self.root / 'sample.txt').write_bytes(b'x' * (v.MAX_FILE_BYTES + 1))
        self.freeze()
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

    def test_unsafe_manifest_path(self):
        m = json.loads((self.root / 'MANIFEST.json').read_text())
        m['files']['../escape.txt'] = m['files'].pop('sample.txt')
        (self.root / 'MANIFEST.json').write_text(json.dumps(m))
        with self.assertRaises(v.Invalid):
            v.inventory(self.root)

if __name__ == '__main__':
    unittest.main(verbosity=2)
