import importlib.util
import json
import subprocess
from pathlib import Path
import tempfile
import unittest
import zipfile

module_path = Path(__file__).resolve().parents[1] / 'scripts/package.py'
spec = importlib.util.spec_from_file_location('packaging_helper', module_path)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


def setup(directory, entries=None):
    root = directory / 'pack'
    root.mkdir()
    validator = module_path.parent / 'validate.mjs'
    expression = f"import * as v from {json.dumps(validator.as_uri())};console.log(JSON.stringify([v.REQUIRED_SKILLS,v.REQUIRED_PRINCIPLES,v.REQUIRED_PLAYBOOKS]));"
    skills, principles, playbooks = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', expression], text=True))
    def put(name, text):
        file = root / name
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text)
    for name in skills + ['principle-' + p for p in principles]:
        put(f'skills/{name}/SKILL.md', f'---\nname: {name}\ndescription: "A synthetic validation fixture."\n---\n# Fixture\n')
    for name in ['reproduce-and-fix-issues', 'setup-benny', 'triage-issue-reports']:
        put(f'automations/benny/skills/{name}/SKILL.md', f'---\nname: {name}\ndescription: "A synthetic validation fixture."\n---\n# Fixture\n')
    for name in playbooks:
        put(f'skills/dot-mode/playbooks/{name}.md', '# Fixture\n')
    for name in ['README.md', 'VERIFICATION.md', 'tools/README.md', 'tools/dot-stack.mjs']:
        put(name, 'literal content\n')
    for name in ['package.json', 'plugin.json', '.claude-plugin/plugin.json']:
        put(name, json.dumps({'name': 'dot-stack', 'version': '0.1.0'}))
    put('LICENSE', (module_path.parents[1] / 'LICENSE').read_text())
    selected = entries if entries is not None else sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file())
    put('distribution-files.json', json.dumps({'schema_version': 1, 'files': selected}))
    return root


class PackageTests(unittest.TestCase):
    def test_determinism_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory)
            first = helper.package(root, directory / 'a.zip')
            second = helper.package(root, directory / 'b.zip')
            self.assertEqual(first['sha256'], second['sha256'])
            self.assertGreater(len(first['files']), 75)
            self.assertEqual(json.loads((directory / 'a.zip.manifest.json').read_text())['sha256'], first['sha256'])
            with self.assertRaises(FileExistsError):
                helper.package(root, directory / 'a.zip')

    def test_refuses_self_inclusion_and_source_symlinks(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory)
            with self.assertRaises(ValueError):
                helper.package(root, root / 'self.zip')
            (root / 'README.md').unlink()
            (root / 'README.md').symlink_to(directory / 'outside')
            with self.assertRaises(ValueError):
                helper.package(root, directory / 'link.zip')

    def test_unlisted_private_files_never_enter_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory)
            (root / '.aws').mkdir()
            for name in ['.npmrc', '.aws/credentials', 'private-debug.log', '.env']:
                (root / name).write_text('synthetic-private-fixture')
            helper.package(root, directory / 'out.zip')
            with zipfile.ZipFile(directory / 'out.zip') as archive:
                self.assertNotIn('dot-stack/.npmrc', archive.namelist())
                self.assertNotIn('dot-stack/.aws/credentials', archive.namelist())
                self.assertNotIn('dot-stack/private-debug.log', archive.namelist())
                self.assertIn('dot-stack/LICENSE', archive.namelist())

    def test_listed_private_file_fails_before_output_creation(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory, ['.npmrc'])
            (root / '.npmrc').write_text('synthetic-private-fixture')
            with self.assertRaises(ValueError):
                helper.package(root, directory / 'out.zip')
            self.assertFalse((directory / 'out.zip').exists())

    def test_dangling_receipt_link_never_writes_target(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory)
            target = directory / 'do-not-create'
            (directory / 'out.zip.manifest.json').symlink_to(target)
            with self.assertRaises(ValueError):
                helper.package(root, directory / 'out.zip')
            self.assertFalse(target.exists())
            self.assertFalse((directory / 'out.zip').exists())

    def test_existing_receipt_kept_and_own_partial_archive_removed(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory)
            receipt = directory / 'out.zip.manifest.json'
            receipt.write_text('old evidence')
            with self.assertRaises(FileExistsError):
                helper.package(root, directory / 'out.zip')
            self.assertEqual(receipt.read_text(), 'old evidence')
            self.assertFalse((directory / 'out.zip').exists())

    def test_inventory_traversal_and_duplicate_entries_fail(self):
        for entries in [['../outside'], ['/outside'], ['README.md', 'README.md']]:
            with self.subTest(entries=entries), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                root = setup(directory, entries)
                with self.assertRaises(ValueError):
                    helper.package(root, directory / 'out.zip')
                self.assertFalse((directory / 'out.zip').exists())

    def test_selected_inventory_must_be_complete_even_when_source_is_complete(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            root = setup(directory, ['README.md'])
            with self.assertRaisesRegex(ValueError, 'Selected distribution'):
                helper.package(root, directory / 'out.zip')
            self.assertFalse((directory / 'out.zip').exists())


if __name__ == '__main__':
    unittest.main()
