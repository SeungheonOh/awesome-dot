"""Ordinary authored link fixtures for exact frozen-guide omissions only."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('evaluation_link_check', HERE / 'check.py')
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class RoutingReferenceChecks(unittest.TestCase):
    def test_exact_mapping_is_the_documented_allowlist(self):
        mapping = json.loads((HERE / 'contracts/task-routing/provenance/omitted-links.json').read_text())
        pairs = {('contracts/task-routing/' + row['source'], row['target'])
                 for row in mapping['omitted_links']}
        self.assertEqual(34, len(pairs))
        self.assertEqual(CHECK.TASK_ROUTING_OMITTED_LINKS, pairs)
        self.assertTrue(pairs <= CHECK.OMITTED_PACKAGE_LINKS)

    def fixture_check(self, extra_source=None, extra_target=None, omit_pair=None):
        with tempfile.TemporaryDirectory(prefix='routing-links-') as directory:
            root = Path(directory)
            for source, target in CHECK.OMITTED_PACKAGE_LINKS:
                if (source, target) == omit_pair:
                    continue
                path = root / source
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('a') as out:
                    out.write(f'[Omitted authored context]({target})\n')
            if extra_source:
                path = root / extra_source
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open('a') as out:
                    out.write(f'[Unlisted context]({extra_target})\n')
            previous = CHECK.ROOT
            try:
                CHECK.ROOT = root
                with contextlib.redirect_stdout(io.StringIO()):
                    CHECK.check_links()
            finally:
                CHECK.ROOT = previous

    def test_all_exact_omissions_are_allowed(self):
        self.fixture_check()

    def test_neighboring_target_is_not_exempt(self):
        source, target = sorted(CHECK.TASK_ROUTING_OMITTED_LINKS)[0]
        with self.assertRaisesRegex(ValueError, 'Broken local link:'):
            self.fixture_check(source, 'neighbor-' + target)

    def test_same_target_from_neighboring_source_is_not_exempt(self):
        source, target = sorted(CHECK.TASK_ROUTING_OMITTED_LINKS)[0]
        neighboring = str(Path(source).with_name('NEIGHBOR.md'))
        with self.assertRaisesRegex(ValueError, 'Broken local link:'):
            self.fixture_check(neighboring, target)

    def test_unused_exception_requires_review(self):
        pair = sorted(CHECK.TASK_ROUTING_OMITTED_LINKS)[0]
        with self.assertRaisesRegex(ValueError, 'exceptions changed'):
            self.fixture_check(omit_pair=pair)


if __name__ == '__main__':
    unittest.main()
