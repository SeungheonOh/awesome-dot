"""Build navigation from canonical Markdown recipes; no external dependencies."""
from __future__ import annotations
import json
from pathlib import Path
from common import ROOT, CATEGORIES, load_recipes

NOTICE = '<!-- Generated navigation. Edit recipe Markdown, then run scripts/build_index.py. -->\n'
START, END = '<!-- catalog-summary:start -->', '<!-- catalog-summary:end -->'

def safe(text):
    return text.replace('|', '\\|').replace('\n', ' ')

def outputs(root: Path = ROOT, records: list[dict] | None = None) -> dict[str, str]:
    records = load_recipes(root) if records is None else records
    result = {}
    intro = [NOTICE, '# Project catalog', '', f'**{len(records)} original recipes. All are proposed, not executed.**', '', 'Choose an outcome, open the full guide, and copy its prompt into dot. Timeboxes are first-session planning budgets; capability labels identify access to check.', '', '[Start at work](docs/WORKPLACE-QUICKSTART.md) · [Learning paths](docs/LEARNING-PATHS.md) · [Agent guide](docs/AGENT-GUIDE.md)', '', '## Categories', '']
    summary = [f'**{len(records)} original recipes · {len(set(r["category"] for r in records))} categories · every recipe marked not run**', '', '| Explore | Recipes |', '| --- | ---: |'] if records else ['The collection structure is ready. Original recipe batches are being authored and checked.']
    if not records:
        intro.append('Original recipe batches are being authored and checked. The workplace quickstart is ready to use above.')
    sections = []
    for category, title in CATEGORIES.items():
        group = [r for r in records if r['category'] == category]
        if not group:
            continue
        intro.append(f'- [{title}](recipes/{category}/README.md): {len(group)} recipes')
        summary.append(f'| [{title}](recipes/{category}/README.md) | {len(group)} |')
        category_lines = [NOTICE, f'# {title}', '', f'{len(group)} proposed recipes. These are project briefs, not executed demonstrations.', '', '[All recipes](../../CATALOG.md) · [Start here](../../START-HERE.md)', '', '| Project | Level | Outcome |', '| --- | --- | --- |']
        sections += ['', f'## {title}', '', '| Project | Level | First session | Capabilities to check |', '| --- | --- | --- | --- |']
        for r in group:
            category_lines.append(f"| [{safe(r['title'])}]({r['id']}.md) | {r['level']} | {safe(r['summary'])} |")
            sections.append(f"| [{safe(r['title'])}]({r['path']}) | {r['level']} | {r['timebox_minutes']} min | {', '.join(r['capabilities'])} |")
        result[f'recipes/{category}/README.md'] = '\n'.join(category_lines) + '\n'
    result['CATALOG.md'] = '\n'.join(intro + sections + ['', '## Machine-readable navigation', '', '[catalog.json](catalog.json) contains compact metadata and paths. Full prompts and checks remain in canonical Markdown.']) + '\n'
    # One metadata record per line keeps the derived index compact and reviewable.
    result['catalog.json'] = '{\n  "schema_version": 1,\n  "count": ' + str(len(records)) + ',\n  "recipes": [\n' + ',\n'.join('    ' + json.dumps(r, ensure_ascii=False, separators=(',', ':')) for r in records) + '\n  ]\n}\n'
    readme = (root/'README.md').read_text(encoding='utf-8')
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(END) < readme.index(START):
        raise ValueError('README needs one ordered catalog-summary marker pair')
    result['README.md'] = readme.split(START)[0] + START + '\n' + '\n'.join(summary) + '\n' + END + readme.split(END)[1]
    return result

def build(root: Path = ROOT) -> int:
    expected = outputs(root)
    for path in (root/'recipes').glob('*/README.md'):
        if path.relative_to(root).as_posix() not in expected:
            path.unlink()
    for name, content in expected.items():
        path = root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    return len(expected)

if __name__ == '__main__':
    print(f'Updated {build()} navigation files')
