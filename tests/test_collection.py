"""Standard-library regression tests for canonical recipe validation and navigation.

Run from the repository root with ``python3 -m unittest discover -s tests -v``.
Every integration test builds its own temporary collection; no real recipe or
checked-in generated file is changed.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))

import build_index
import check
import common


MAIN_PROMPT = """dot, help me create [SPECIFIC DELIVERABLE] for [AUDIENCE] so they can [CONCRETE OUTCOME]. Use [AUTHORIZED INPUTS] and stay within [SCOPE]. The first version should fit [FORMAT OR SIZE LIMIT], and the most important constraint is [CONSTRAINT].

First check which inputs and capabilities are available. If a missing detail materially changes the result, ask me. Otherwise state a reasonable assumption and make a reversible draft. Do not invent facts, sources, completed actions or evidence of testing.

Produce the smallest complete version with [REQUIRED ELEMENTS]. Explain how each important part uses the supplied evidence. Test [NORMAL CASE], [EDGE CASE] and [REPEATED OR INTERRUPTED ACTION] where possible, and label unrun checks clearly.

Keep the work private. Before any sharing, account change, external action or expansion of scope, identify the destination and consequence and ask for any required decision. Return the artifact, the check results, known limits and the smallest next step."""

METADATA = {
    'id': 'example-project-brief',
    'title': 'Example Project Brief',
    'summary': 'Turn a bounded example task into an inspectable draft with explicit checks and limits.',
    'category': 'engineering-workflows',
    'level': 'beginner',
    'timebox_minutes': 30,
    'capabilities': ['files'],
    'tags': ['planning', 'review'],
    'status': 'recipe-not-run',
}


def metadata_text(metadata: dict) -> str:
    lines = []
    for key, value in metadata.items():
        if isinstance(value, str) and key not in ('title', 'summary'):
            encoded = value
        else:
            encoded = json.dumps(value, ensure_ascii=False)
        lines.append(f'{key}: {encoded}')
    return '\n'.join(lines)


def recipe(metadata: dict | None = None, prompt: str = MAIN_PROMPT) -> str:
    """A complete, independent fixture following templates/RECIPE.md."""
    data = {**METADATA, **(metadata or {})}
    body = f'''# {data['title']}

{data['summary']}

## Scenario

A project reviewer needs a small, inspectable draft using sanitized inputs.

## Inputs to prepare

- The intended audience and concrete outcome
- A minimal authorized input or synthetic example
- The required format and review criteria

## Copy this prompt into dot

```text
{prompt}
```

## Iterate with a purpose

### 1. Improve usability

```text
Inspect the draft and simplify its hardest step while preserving the checks.
```

### 2. Test uncertainty

```text
Propose a small test for the assumption most likely to affect this draft.
```

### 3. Add a capability

```text
Describe one optional extension and wait for approval before expanding scope.
```

## Expected deliverables

- A concrete draft in the requested format
- An evidence and assumption record
- A check report with unrun items clearly marked

## Acceptance checks

- The output addresses the supplied audience and goal
- Claims can be traced to authorized supplied inputs
- An empty input has an explicit handling path
- The report separates observed results from unrun checks

## Access, privacy and stop conditions

- Use only authorized inputs and ask before exposing them to a new audience
- Stop and explain limitations if required access is unavailable

## Two possible extensions

- Add a second realistic example after the first passes review
- Create a reusable checklist from an actual run
'''
    return f'---\n{metadata_text(data)}\n---\n\n{body}'


def replace_section(text: str, heading: str, content: str) -> str:
    marker = f'## {heading}\n'
    before, rest = text.split(marker, 1)
    _, next_marker, after = rest.partition('\n## ')
    return before + marker + '\n' + content + '\n' + (next_marker + after if next_marker else '')


class TemporaryCollection(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.write('README.md', '# Test collection\n\nKeep this introduction.\n\n'
                   + build_index.START + '\nold summary\n' + build_index.END
                   + '\n\nKeep this conclusion.\n')
        self.write('START-HERE.md', '# Start here\n')
        for name in ('WORKPLACE-QUICKSTART', 'LEARNING-PATHS', 'AGENT-GUIDE'):
            self.write(f'docs/{name}.md', f'# {name}\n')

    def write(self, name: str, content: str) -> Path:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
        return path

    def add_recipe(self, **metadata) -> Path:
        values = {**METADATA, **metadata}
        return self.write(f"recipes/{values['category']}/{values['id']}.md", recipe(metadata))

    def assert_issue(self, errors: list[str], expected: str):
        self.assertTrue(any(expected in error for error in errors), (expected, errors))


class ParseRecipeTests(unittest.TestCase):
    def test_valid_metadata_preserves_types_and_body(self):
        data, body = common.parse_recipe(recipe())
        self.assertEqual(data, METADATA)
        self.assertIs(type(data['timebox_minutes']), int)
        self.assertIsInstance(data['capabilities'], list)
        self.assertTrue(body.startswith('\n# Example Project Brief\n'))

    def test_quoted_colon_and_unicode_are_preserved(self):
        title = 'Plan: café review'
        data, _ = common.parse_recipe(recipe({'title': title}))
        self.assertEqual(data['title'], title)

    def test_rejects_invalid_opening_or_closing_delimiters(self):
        text = recipe()
        cases = (text.lstrip('-'), '\n' + text, text.replace('---\n', '--\n', 1),
                 text.replace('\n---\n', '\n--\n', 1), text.split('\n---\n', 1)[0])
        for invalid in cases:
            with self.subTest(invalid=invalid[:40]), self.assertRaises(ValueError):
                common.parse_recipe(invalid)

    def test_only_first_closing_delimiter_splits_body(self):
        _, body = common.parse_recipe(recipe() + '\n---\nMore body text\n')
        self.assertTrue(body.endswith('\n---\nMore body text\n'))

    def test_duplicate_key_is_rejected(self):
        invalid = recipe().replace('id: example-project-brief\n',
                                   'id: example-project-brief\nid: duplicate-project\n')
        with self.assertRaisesRegex(ValueError, 'duplicate metadata key: id'):
            common.parse_recipe(invalid)

    def test_malformed_metadata_lines_are_rejected(self):
        for line in ('id:no-space', 'id', 'id: a-valid-id\n\ntitle: \"A title\"', 'id: an unquoted phrase', 'tags: [broken',
                     'title: "unterminated', 'title: "valid" trailing'):
            with self.subTest(line=line), self.assertRaises(ValueError):
                common.parse_recipe('---\n' + line + '\n---\nbody\n')


class RecipeValidationTests(unittest.TestCase):
    def assert_issue(self, text: str, expected: str, path: Path | None = None):
        errors = check.validate_recipe(text, path)
        self.assertTrue(any(expected in error for error in errors), (expected, errors))

    def test_complete_fixture_passes(self):
        self.assertEqual(check.validate_recipe(recipe()), [])
        path = Path('recipes/engineering-workflows/example-project-brief.md')
        self.assertEqual(check.validate_recipe(recipe(), path), [])

    def test_parse_error_becomes_diagnostic(self):
        self.assert_issue('not a recipe', 'front matter')

    def test_missing_and_extra_fields(self):
        for field in METADATA:
            data = METADATA.copy()
            del data[field]
            invalid = '---\n' + metadata_text(data) + '\n---\nbody\n'
            with self.subTest(field=field):
                self.assert_issue(invalid, f"missing=['{field}']")
        self.assert_issue(recipe({'extra': 'unexpected'}), "extra=['extra']")

    def test_string_fields_reject_other_scalar_types(self):
        for field in ('id', 'title', 'summary', 'category', 'level', 'status'):
            with self.subTest(field=field):
                self.assert_issue(recipe({field: 123}), f'{field} must be a string')

    def test_timebox_bounds_and_scalar_types(self):
        for value in (15, 240):
            with self.subTest(value=value):
                self.assertEqual(check.validate_recipe(recipe({'timebox_minutes': value})), [])
        for value in (14, 241, 'thirty', ['30']):
            with self.subTest(value=value):
                self.assert_issue(recipe({'timebox_minutes': value}), 'timebox_minutes must be an integer')
        self.assert_issue(recipe().replace('timebox_minutes: 30', 'timebox_minutes: "30"'),
                          'timebox_minutes must be an integer')

    def test_invalid_enums_and_identifier(self):
        for field, value, diagnostic in (
            ('id', 'x', 'id must be'), ('category', 'unknown-category', 'unknown category'),
            ('level', 'expert', 'unknown level'), ('status', 'tested', 'status must remain'),
        ):
            with self.subTest(field=field):
                self.assert_issue(recipe({field: value}), diagnostic)

    def test_title_and_summary_length_limits(self):
        for field, lower, upper in (('title', 8, 100), ('summary', 40, 400)):
            for length in (lower, upper):
                with self.subTest(field=field, length=length):
                    self.assertEqual(check.validate_recipe(recipe({field: 'a' * length})), [])
            for length in (lower - 1, upper + 1):
                with self.subTest(field=field, length=length):
                    self.assert_issue(recipe({field: 'a' * length}), f'{field} length')

    def test_list_types_counts_duplicates_and_values(self):
        cases = [('capabilities', 'files', 'must be a list of strings'),
                 ('capabilities', [1], 'must be a list of strings'),
                 ('capabilities', [], 'count or uniqueness'),
                 ('capabilities', ['files', 'files'], 'count or uniqueness'),
                 ('capabilities', ['telepathy'], 'unknown capability'),
                 ('tags', ['one'], 'count or uniqueness'),
                 ('tags', ['one', 'one'], 'count or uniqueness'),
                 ('tags', ['UPPER', 'valid'], 'tags must be kebab-case'),
                 ('tags', ['one', 'two', 'three', 'four', 'five', 'six', 'seven'], 'count or uniqueness')]
        for field, value, diagnostic in cases:
            with self.subTest(field=field, value=value):
                self.assert_issue(recipe({field: value}), diagnostic)

    def test_file_path_must_match_metadata(self):
        for path in ('recipes/engineering-workflows/another-project.md',
                     'recipes/learning/example-project-brief.md'):
            with self.subTest(path=path):
                self.assert_issue(recipe(), 'id/category must match the file path', Path(path))

    def test_h1_and_required_section_presence_and_uniqueness(self):
        self.assert_issue(recipe().replace('# Example Project Brief', '# Different title'), 'H1 must match')
        for heading in common.HEADINGS:
            with self.subTest(heading=heading, mode='missing'):
                self.assert_issue(recipe().replace(f'## {heading}\n', '## Other heading\n'),
                                  f'expected exactly one section: {heading}')
            with self.subTest(heading=heading, mode='duplicate'):
                self.assert_issue(recipe() + f'\n## {heading}\n',
                                  f'expected exactly one section: {heading}')

    def test_main_prompt_word_count_boundaries(self):
        for words in (120, 280):
            with self.subTest(words=words):
                self.assertEqual(check.validate_recipe(recipe(prompt='dot ' + 'word ' * (words - 1))), [])
        for words in (119, 281):
            with self.subTest(words=words):
                self.assert_issue(recipe(prompt='dot ' + 'word ' * (words - 1)), f'got {words}')

    def test_main_prompt_requires_one_text_block_and_addresses_dot(self):
        for content in ('No code block.', '```python\nprint(1)\n```',
                        '```text\ndot first\n```\n```text\ndot second\n```'):
            with self.subTest(content=content):
                self.assert_issue(replace_section(recipe(), 'Copy this prompt into dot', content),
                                  'main prompt needs exactly one text code block')
        self.assert_issue(recipe(prompt=MAIN_PROMPT.replace('dot,', 'Assistant,')), 'should address dot')

    def test_iterations_require_three_named_prompts(self):
        self.assert_issue(recipe().replace('### 3. Add a capability', 'Add a capability'),
                          'iterations need three named text prompts')
        self.assert_issue(recipe().replace('Describe one optional extension and wait for approval before expanding scope.\n```',
                                           'Describe one optional extension and wait for approval before expanding scope.'),
                          'iterations need three named text prompts')

    def test_bullet_count_boundaries(self):
        for heading, lower, upper in (
            ('Inputs to prepare', 3, 6), ('Expected deliverables', 3, 6),
            ('Acceptance checks', 4, 7), ('Access, privacy and stop conditions', 2, 5),
            ('Two possible extensions', 2, 2),
        ):
            for count in sorted({lower, upper}):
                with self.subTest(heading=heading, count=count):
                    text = replace_section(recipe(), heading, '- A concrete item\n' * count)
                    self.assertEqual(check.validate_recipe(text), [])
            for count in (lower - 1, upper + 1):
                with self.subTest(heading=heading, count=count):
                    text = replace_section(recipe(), heading, '- A concrete item\n' * count)
                    self.assert_issue(text, f'{heading} needs {lower}–{upper} bullets, got {count}')


class LocalLinkTests(TemporaryCollection):
    def test_valid_relative_links_fragments_images_and_url_encoding(self):
        self.write('assets/an image.png', 'placeholder')
        self.write('docs/target.md', '# Target page\n\n## A useful heading\n')
        self.write('docs/source.md', '[same](#source)\n# Source\n'
                   '[target](target.md#a-useful-heading)\n'
                   '![image](../assets/an%20image.png)\n'
                   '[root](../START-HERE.md "Start guide")\n')
        self.assertEqual(check.link_errors(self.root), [])

    def test_missing_local_file_and_anchor_are_reported(self):
        self.write('source.md', '[missing](does-not-exist.md)\n[anchor](START-HERE.md#absent)\n')
        issues = check.link_errors(self.root)
        self.assert_issue(issues, 'missing local link: does-not-exist.md')
        self.assert_issue(issues, 'missing heading: START-HERE.md#absent')

    def test_links_leaving_repository_are_rejected(self):
        self.write('source.md', '[outside](../outside.md)\n[encoded](%2e%2e/outside.md)\n')
        issues = check.link_errors(self.root)
        self.assertEqual(sum('link leaves repository' in issue for issue in issues), 2)

    def test_external_urls_are_not_fetched(self):
        self.write('source.md', '[web](https://example.invalid/missing)\n'
                   '[mail](mailto:editor@example.invalid)\n[app](custom+app:target)\n')
        self.assertEqual(check.link_errors(self.root), [])

    def test_fenced_examples_are_ignored(self):
        self.write('source.md', '# Real heading\n\n```markdown\n'
                   '[example](missing.md)\n## Imaginary heading\n```\n')
        self.assertEqual(check.link_errors(self.root), [])
        self.assertEqual(check.anchor_names((self.root / 'source.md').read_text()), {'real-heading'})

    def test_duplicate_heading_slugs_are_numbered(self):
        text = '# Same heading\n## Same heading\n### Same heading\n# Punctuation: OK!\n'
        self.assertEqual(check.anchor_names(text),
                         {'same-heading', 'same-heading-1', 'same-heading-2', 'punctuation-ok'})

    def test_git_metadata_is_excluded(self):
        self.write('.git/notes.md', '[ignored](missing.md)\n')
        self.assertEqual(check.link_errors(self.root), [])


class CollectionTests(TemporaryCollection):
    def test_generated_collection_passes_and_minimum_is_enforced(self):
        self.add_recipe()
        build_index.build(self.root)
        self.assertEqual(check.check(self.root, minimum=1), [])
        self.assert_issue(check.check(self.root, minimum=2), 'expected at least 2 recipes, found 1')

    def test_recipe_enumeration_excludes_category_readmes(self):
        path = self.add_recipe()
        self.write('recipes/engineering-workflows/README.md', '# Navigation\n')
        self.write('recipes/loose-file.md', '# Not a canonical recipe\n')
        self.assertEqual(common.recipe_files(self.root), [path])

    def test_duplicate_ids_titles_and_prompts(self):
        self.add_recipe()
        self.add_recipe(category='learning')
        issues = check.check(self.root)
        for field in ('id', 'title', 'prompt'):
            self.assert_issue(issues, f'duplicate {field}')

    def test_duplicate_titles_and_prompts_normalize_case_and_whitespace(self):
        self.add_recipe()
        duplicate = recipe({'id': 'second-project-brief', 'title': 'EXAMPLE   PROJECT BRIEF'},
                           prompt='  '.join(MAIN_PROMPT.upper().split()))
        self.write('recipes/engineering-workflows/second-project-brief.md', duplicate)
        issues = check.check(self.root)
        self.assert_issue(issues, 'duplicate title')
        self.assert_issue(issues, 'duplicate prompt')

    def test_invalid_recipes_report_errors_without_generating(self):
        self.write('recipes/learning/broken.md', 'not a recipe')
        self.assert_issue(check.check(self.root), 'recipe must begin with')


class GeneratedIndexTests(TemporaryCollection):
    def test_build_is_idempotent_and_preserves_readme_surroundings(self):
        self.add_recipe()
        first_count = build_index.build(self.root)
        first = {name: (self.root / name).read_bytes() for name in build_index.outputs(self.root)}
        self.assertEqual(build_index.build(self.root), first_count)
        self.assertEqual(first, {name: (self.root / name).read_bytes() for name in first})
        readme = (self.root / 'README.md').read_text()
        self.assertIn('Keep this introduction.', readme)
        self.assertTrue(readme.endswith('Keep this conclusion.\n'))
        self.assertEqual(readme.count(build_index.START), 1)
        self.assertEqual(readme.count(build_index.END), 1)

    def test_generated_json_has_only_navigation_metadata(self):
        self.add_recipe()
        output = build_index.outputs(self.root)
        data = json.loads(output['catalog.json'])
        self.assertEqual(data['schema_version'], 1)
        self.assertEqual(data['count'], 1)
        self.assertEqual(len(data['recipes']), 1)
        self.assertEqual(set(data['recipes'][0]), set(METADATA) | {'path'})
        self.assertNotIn(MAIN_PROMPT, output['catalog.json'])

    def test_missing_or_stale_generated_file_is_detected(self):
        self.add_recipe()
        self.assert_issue(check.check(self.root), 'CATALOG.md: stale or missing')
        build_index.build(self.root)
        self.write('catalog.json', '{}\n')
        self.assert_issue(check.check(self.root), 'catalog.json: stale or missing')
        build_index.build(self.root)
        self.write('CATALOG.md', (self.root / 'CATALOG.md').read_text() + '\nChanged by hand.\n')
        self.assert_issue(check.check(self.root), 'CATALOG.md: stale or missing')

    def test_orphan_category_index_is_detected_and_removed(self):
        self.add_recipe()
        build_index.build(self.root)
        orphan = self.write('recipes/learning/README.md', '# Old category\n')
        self.assert_issue(check.check(self.root), 'recipes/learning/README.md: orphan category index')
        build_index.build(self.root)
        self.assertFalse(orphan.exists())
        self.assertEqual(check.check(self.root), [])

    def test_removing_last_recipe_cleans_its_category_index(self):
        path = self.add_recipe()
        build_index.build(self.root)
        path.unlink()
        build_index.build(self.root)
        self.assertFalse((path.parent / 'README.md').exists())
        self.assertEqual(json.loads((self.root / 'catalog.json').read_text())['count'], 0)
        self.assertEqual(check.check(self.root), [])

    def test_invalid_readme_markers_are_rejected(self):
        for text in ('# Missing markers\n', build_index.END + '\n' + build_index.START,
                     build_index.START + build_index.START + build_index.END,
                     build_index.START + build_index.END + build_index.END):
            with self.subTest(text=text):
                self.write('README.md', text)
                with self.assertRaisesRegex(ValueError, 'ordered catalog-summary marker pair'):
                    build_index.outputs(self.root)

    def test_readme_marker_error_becomes_checker_diagnostic(self):
        self.write('README.md', '# Missing markers\n')
        self.assert_issue(check.check(self.root), 'cannot generate index: README needs')

    def test_records_sort_by_category_then_casefolded_title(self):
        self.add_recipe(id='zebra-learning', title='Zebra Learning Plan', category='learning')
        self.add_recipe(id='zebra-engineering', title='Zebra Engineering Plan')
        self.add_recipe(id='alpha-engineering', title='alpha Engineering Plan')
        records = common.load_recipes(self.root)
        self.assertEqual([r['id'] for r in records],
                         ['alpha-engineering', 'zebra-engineering', 'zebra-learning'])

    def test_markdown_table_text_escapes_pipe(self):
        self.add_recipe(title='Example | Project Brief')
        result = build_index.outputs(self.root)
        self.assertIn('Example \\| Project Brief', result['CATALOG.md'])
        self.assertIn('Example \\| Project Brief', result['recipes/engineering-workflows/README.md'])


if __name__ == '__main__':
    unittest.main()
