"""Fast invariants for the collection's published template."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check import validate_recipe
from common import parse_recipe


class TemplateSmokeTests(unittest.TestCase):
    def test_published_template_is_valid(self):
        text = (ROOT / 'templates' / 'RECIPE.md').read_text(encoding='utf-8')
        self.assertEqual(validate_recipe(text), [])

    def test_plain_markdown_is_not_recipe_metadata(self):
        with self.assertRaisesRegex(ValueError, 'front matter'):
            parse_recipe('# A page without metadata\n')


if __name__ == '__main__':
    unittest.main()
