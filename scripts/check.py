"""Check recipe structure, local links and generated navigation, not project execution."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote
from common import ROOT, CATEGORIES, CAPABILITIES, FIELDS, HEADINGS, parse_recipe, section, recipe_files
from build_index import outputs

ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

def validate_recipe(text: str, path: Path | None = None) -> list[str]:
    errors = []
    try:
        r, body = parse_recipe(text)
    except ValueError as exc:
        return [str(exc)]
    if set(r) != FIELDS:
        errors.append(f'metadata keys differ: missing={sorted(FIELDS-set(r))}, extra={sorted(set(r)-FIELDS)}')
        return errors
    for key in ('id','title','summary','category','level','status'):
        if not isinstance(r[key], str):
            errors.append(f'{key} must be a string')
    if errors:
        return errors
    if not ID.fullmatch(r['id']) or not 3 <= len(r['id']) <= 80:
        errors.append('id must be 3–80 lowercase kebab-case characters')
    if not 8 <= len(r['title']) <= 100:
        errors.append('title length must be 8–100 characters')
    if not 40 <= len(r['summary']) <= 400:
        errors.append('summary length must be 40–400 characters')
    if r['category'] not in CATEGORIES:
        errors.append('unknown category')
    if r['level'] not in ('beginner','intermediate','advanced'):
        errors.append('unknown level')
    if r['status'] != 'recipe-not-run':
        errors.append('status must remain recipe-not-run')
    if type(r['timebox_minutes']) is not int or not 15 <= r['timebox_minutes'] <= 240:
        errors.append('timebox_minutes must be an integer from 15 to 240')
    for key, lower, upper in [('capabilities',1,8),('tags',2,6)]:
        value = r[key]
        if not isinstance(value,list) or not all(isinstance(x,str) for x in value):
            errors.append(f'{key} must be a list of strings')
            continue
        if not lower <= len(value) <= upper or len(value) != len(set(value)):
            errors.append(f'{key} count or uniqueness is invalid')
        if key == 'capabilities' and not set(value) <= CAPABILITIES:
            errors.append('unknown capability')
        if key == 'tags' and not all(ID.fullmatch(x) for x in value):
            errors.append('tags must be kebab-case')
    if path is not None and (path.stem != r['id'] or path.parent.name != r['category']):
        errors.append('id/category must match the file path')
    if not re.search(r'^# ' + re.escape(r['title']) + r'\s*$',body,re.M):
        errors.append('H1 must match title metadata')
    for heading in HEADINGS:
        if len(re.findall(r'^## ' + re.escape(heading) + r'\s*$', body, re.M)) != 1:
            errors.append(f'expected exactly one section: {heading}')
    if errors:
        return errors
    prompt_section = section(body,'Copy this prompt into dot')
    prompts = re.findall(r'```text\s*\n(.*?)\n```',prompt_section,re.S)
    if len(prompts) != 1:
        errors.append('main prompt needs exactly one text code block')
    else:
        words = len(prompts[0].split())
        if not 120 <= words <= 280:
            errors.append(f'main prompt must contain 120–280 words, got {words}')
        if not re.search(r'\bdot\b',prompts[0],re.I):
            errors.append('main prompt should address dot')
    iterations = section(body,'Iterate with a purpose')
    if len(re.findall(r'^### ',iterations,re.M)) != 3 or len(re.findall(r'```text\s*\n(.*?)\n```',iterations,re.S)) != 3:
        errors.append('iterations need three named text prompts')
    for heading, low, high in [('Inputs to prepare',3,6),('Expected deliverables',3,6),('Acceptance checks',4,7),('Access, privacy and stop conditions',2,5),('Two possible extensions',2,2)]:
        count = len(re.findall(r'^- ',section(body,heading),re.M))
        if not low <= count <= high:
            errors.append(f'{heading} needs {low}–{high} bullets, got {count}')
    return errors

def stripped_markdown(text: str) -> str:
    return re.sub(r'```.*?```', '', text, flags=re.S)

def anchor_names(text: str) -> set[str]:
    result, counts = set(), {}
    for heading in re.findall(r'^#{1,6} (.+)$',stripped_markdown(text),re.M):
        slug = re.sub(r'[^\w\- ]','',heading.casefold()).replace(' ','-')
        count = counts.get(slug,0)
        result.add(f'{slug}-{count}' if count else slug)
        counts[slug] = count+1
    return result

def link_errors(root: Path) -> list[str]:
    errors = []
    for path in sorted(root.rglob('*.md')):
        if '.git' in path.parts:
            continue
        text = stripped_markdown(path.read_text(encoding='utf-8'))
        for dest in re.findall(r'!?\[[^\]\n]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)',text):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',dest):
                continue
            dest = unquote(dest)
            file_part, _, fragment = dest.partition('#')
            target = (path.parent/file_part).resolve() if file_part else path.resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f'{path.relative_to(root)}: link leaves repository: {dest}')
                continue
            if not target.exists():
                errors.append(f'{path.relative_to(root)}: missing local link: {dest}')
            elif fragment and target.suffix == '.md' and fragment not in anchor_names(target.read_text(encoding='utf-8')):
                errors.append(f'{path.relative_to(root)}: missing heading: {dest}')
    return errors

def check(root: Path = ROOT, minimum: int = 0) -> list[str]:
    errors, seen = [], {'id':{},'title':{},'prompt':{}}
    files = recipe_files(root)
    if len(files) < minimum:
        errors.append(f'expected at least {minimum} recipes, found {len(files)}')
    for path in files:
        text = path.read_text(encoding='utf-8')
        local = validate_recipe(text,path)
        errors += [f'{path.relative_to(root)}: {e}' for e in local]
        if local:
            continue
        r, body = parse_recipe(text)
        prompt = re.findall(r'```text\s*\n(.*?)\n```',section(body,'Copy this prompt into dot'),re.S)[0]
        for key, value in [('id',r['id']),('title',r['title']),('prompt',prompt)]:
            value = ' '.join(value.casefold().split())
            if value in seen[key]:
                errors.append(f'{path.relative_to(root)}: duplicate {key} with {seen[key][value]}')
            seen[key][value] = str(path.relative_to(root))
    errors += link_errors(root)
    if not errors:
        try:
            expected = outputs(root)
        except (ValueError,KeyError) as exc:
            errors.append(f'cannot generate index: {exc}')
        else:
            for name, content in expected.items():
                path = root/name
                if not path.exists() or path.read_text(encoding='utf-8') != content:
                    errors.append(f'{name}: stale or missing; run python3 scripts/build_index.py')
            for path in (root/'recipes').glob('*/README.md'):
                if path.relative_to(root).as_posix() not in expected:
                    errors.append(f'{path.relative_to(root)}: orphan category index')
    return errors

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--minimum',type=int,default=0,help='optional expected minimum recipe count')
    args = p.parse_args()
    issues = check(minimum=args.minimum)
    if issues:
        for issue in issues:
            print(f'ERROR {issue}')
        raise SystemExit(1)
    print(f'PASS: {len(recipe_files())} recipes; metadata, sections, uniqueness, local links and generated navigation checked')
    print('Project execution, external links and account-specific capabilities were not tested.')
