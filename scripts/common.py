"""Read the collection's deliberately small Markdown metadata format."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    'engineering-workflows': 'Engineering workflows', 'team-operations': 'Team operations',
    'web-games': 'Web games', '3d-spatial': '3D and spatial studies',
    'creative-coding': 'Creative coding', 'image-editing': 'Image editing',
    'design-publishing': 'Design and publishing', 'personal-reminders': 'Personal reminders',
    'life-logistics': 'Life logistics', 'learning': 'Learning',
    'finance': 'Finance', 'news-research': 'News and research',
}
CAPABILITIES = {'research', 'files', 'images', 'code', 'websites', 'connected-apps', 'scheduling', 'computer-access'}
FIELDS = {'id', 'title', 'summary', 'category', 'level', 'timebox_minutes', 'capabilities', 'tags', 'status'}
HEADINGS = [
    'Scenario', 'Inputs to prepare', 'Copy this prompt into dot', 'Iterate with a purpose',
    'Expected deliverables', 'Acceptance checks', 'Access, privacy and stop conditions',
    'Two possible extensions',
]

def parse_recipe(text: str) -> tuple[dict, str]:
    if not text.startswith('---\n'):
        raise ValueError('recipe must begin with --- front matter')
    parts = text.split('\n---\n', 1)
    if len(parts) != 2:
        raise ValueError('front matter has no closing --- delimiter')
    metadata = {}
    for line in parts[0].splitlines()[1:]:
        if not line or ': ' not in line:
            raise ValueError('metadata must use one key: value per line')
        key, value = line.split(': ', 1)
        if key in metadata:
            raise ValueError(f'duplicate metadata key: {key}')
        if value.startswith(('"', '[')) or value.isdigit():
            try:
                metadata[key] = json.loads(value)
            except json.JSONDecodeError as exc:
                raise ValueError(f'invalid metadata value for {key}') from exc
        elif re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
            metadata[key] = value
        else:
            raise ValueError(f'quote the metadata value for {key} as a JSON string')
    return metadata, parts[1]

def section(body: str, title: str) -> str:
    match = re.search(r'^## ' + re.escape(title) + r'\s*\n(.*?)(?=^## |\Z)', body, re.M | re.S)
    return match.group(1).strip() if match else ''

def recipe_files(root: Path = ROOT):
    return sorted(p for p in (root/'recipes').glob('*/*.md') if p.name != 'README.md')

def load_recipes(root: Path = ROOT) -> list[dict]:
    records = []
    for path in recipe_files(root):
        record, _ = parse_recipe(path.read_text(encoding='utf-8'))
        record['path'] = path.relative_to(root).as_posix()
        records.append(record)
    return sorted(records, key=lambda r: (list(CATEGORIES).index(r['category']), r['title'].casefold()))
