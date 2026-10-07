#!/usr/bin/env python3
"""Read-only authored routing-contract checks; no model calls or semantic grading."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError('non-finite JSON value: ' + value)


def parse(text):
    return json.loads(text, object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def regular_file(relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or '..' in path.parts or str(path) != relative:
        raise ValueError('Expected package-relative path: ' + relative)
    local = ROOT / relative
    if any((ROOT / Path(*path.parts[:i])).is_symlink()
           for i in range(1, len(path.parts) + 1)) or not local.is_file():
        raise ValueError('Expected regular package file: ' + relative)
    return local.read_bytes()


def load(relative):
    return parse(regular_file(relative).decode('utf-8'))


def schema_issues(value, schema, path='$'):
    """Only the JSON Schema subset used by this package: type, enum, object/items."""
    issues = []
    types = schema.get('type')
    if isinstance(types, str):
        types = [types]
    kind = ('null' if value is None else 'boolean' if isinstance(value, bool)
            else 'object' if isinstance(value, dict) else 'array'
            if isinstance(value, list) else 'string' if isinstance(value, str)
            else 'number')
    if types and kind not in types:
        return [f'{path}: expected {types}; got {kind}']
    if 'enum' in schema and value not in schema['enum']:
        issues.append(f'{path}: value outside enum')
    if isinstance(value, dict):
        properties = schema.get('properties', {})
        for key in schema.get('required', []):
            if key not in value:
                issues.append(f'{path}: missing property {key}')
        if schema.get('additionalProperties') is False:
            for key in value:
                if key not in properties:
                    issues.append(f'{path}: unexpected property {key}')
        for key in properties.keys() & value.keys():
            issues += schema_issues(value[key], properties[key], path + '.' + key)
    elif isinstance(value, list) and 'items' in schema:
        for index, item in enumerate(value):
            issues += schema_issues(item, schema['items'], f'{path}[{index}]')
    return issues


def check_response(raw, case_id):
    try:
        obj = parse(raw)
    except (ValueError, TypeError) as error:
        return {'interface_valid': False, 'interface_issues': [str(error)],
                'semantic_adequacy': None, 'semantic_review_required': True,
                'allowset_diagnostics': None}
    issues = schema_issues(obj, load('public/output-schema.v1.json'))
    if isinstance(obj, dict) and obj.get('case_id') != case_id:
        issues.append('$.case_id: does not match assigned case')
    rubric = next(c for c in load('author/rubric.v2.json')['cases']
                  if c['id'] == case_id)
    diagnostics = None
    if isinstance(obj, dict):
        diagnostics = {
            'decision_in_authored_allowset': obj.get('decision') in rubric['decision_allowset'],
            'sequence_in_authored_allowset': obj.get('workflow_sequence') in rubric['acceptable_sequences'],
            'meaning': 'Diagnostic only. Listed routes need semantic review; unlisted source-grounded alternatives need adjudication, not automatic failure.'}
    return {'interface_valid': not issues, 'interface_issues': issues,
            'semantic_adequacy': None, 'semantic_review_required': True,
            'allowset_diagnostics': diagnostics}


def assemble(case_id, condition):
    """Reconstruct prospective bytes for hash checking only; never dispatch them."""
    plan = load('provenance/prospective-inputs.json')
    case = next(c for c in load('public/requests.v1.json')['cases']
                if c['case_id'] == case_id)
    chunks = [regular_file('public/common-instruction.md'), b'\nRESPONSE INTERFACE\n',
              regular_file('public/interface.md'), b'\nJSON SCHEMA\n',
              regular_file('public/output-schema.v1.json'),
              b'\nCOMPLETE CANDIDATE ENTRY POINTS\n']
    for name in plan['candidate_order']:
        chunks.extend([('\nCANDIDATE ' + name + '\n').encode(),
                       regular_file('sources/skill/' + name + '/SKILL.md')])
    chunks.extend([b'\nHYPOTHETICAL REQUEST PACKET\n',
                   json.dumps(case, ensure_ascii=False, indent=2).encode(), b'\n'])
    common = b''.join(chunks)
    if condition == 'baseline':
        return common
    if condition == 'router':
        return common + b'\nADDITIONAL ROUTING ENTRY POINT\n' + regular_file(
            'sources/skill/task-to-skill-router/SKILL.md')
    raise ValueError('Unknown prospective condition')


def verify(expected_manifest=None):
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    manifest_raw = regular_file('MANIFEST.json')
    if expected_manifest:
        require(digest(manifest_raw) == expected_manifest, 'External manifest digest differs')
    manifest = parse(manifest_raw.decode('utf-8'))
    entries = manifest['files']
    registered = {e['path'] for e in entries}
    actual = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
              if p.is_file() and p != ROOT / 'MANIFEST.json'}
    require(not any(p.is_symlink() for p in ROOT.rglob('*')), 'Public package contains a symlink')
    require(len(registered) == len(entries), 'Duplicate manifest paths')
    require(actual == registered, 'Public package allowlist differs')
    for entry in entries:
        data = regular_file(entry['path'])
        require(len(data) == entry['bytes'] and digest(data) == entry['sha256'],
                'Frozen bytes differ: ' + entry['path'])
    require(manifest['model_trials_run'] == 0, 'Authored package must record zero trials')
    require(manifest['completed_exact_v2_author_reviews'] == 2, 'Review completion metadata')
    projection = load('provenance/publication-map.json')
    for entry in projection['exact_copies']:
        data = regular_file(entry['path'])
        require(digest(data) == entry['sha256'] and len(data) == entry['bytes'],
                'Original authored bytes differ: ' + entry['path'])
    source = load('source-manifest.json')
    require(len(source['sources']) == 11, 'Expected ten candidate sources plus router')
    for entry in source['sources']:
        data = regular_file(entry['local_path'])
        require(digest(data) == entry['sha256'] and len(data) == entry['bytes'],
                'Source digest differs: ' + entry['path'])
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        require(blob == entry['git_blob_sha1'], 'Source Git identity: ' + entry['path'])
    public = load('public/requests.v1.json')
    rubric = load('author/rubric.v2.json')
    ids = [c['case_id'] for c in public['cases']]
    require(ids == [f'R{i:02}' for i in range(1, 13)], 'Ordered 12 public cases')
    require([c['id'] for c in rubric['cases']] == ids, 'Rubric case binding')
    require(rubric['model_trials_run'] == 0, 'Rubric trial metadata')
    for case in public['cases']:
        require(set(case) == {'case_id', 'request', 'packet'},
                case['case_id'] + ' has non-public-packet fields')
    semantic = {k: v for k, v in rubric.items() if k != 'status'}
    canonical = digest(json.dumps(semantic, sort_keys=True,
                                 separators=(',', ':'), ensure_ascii=False).encode())
    binding = next(p for p in projection['projections'] if p['path'] == 'author/rubric.v2.json')
    require(canonical == binding['semantic_content_sha256'], 'Semantic rubric changed')
    for case in rubric['cases']:
        for evidence in case['contract_evidence']:
            lines = regular_file('sources/' + evidence['path']).decode('utf-8').splitlines()
            excerpt = '\n'.join(lines[evidence['line_start'] - 1:evidence['line_end']])
            require(digest(excerpt.encode()) == evidence['text_sha256'],
                    case['id'] + ' source evidence anchor')
            require(evidence['commit'] == source['pinned_commit'], case['id'] + ' source pin')
    index = load('controls/index.v2.json')
    controls = index['controls']
    control_content = {**index, 'controls': [
        {k: v for k, v in control.items() if k != 'semantic_status'}
        for control in controls]}
    control_hash = digest(json.dumps(control_content, sort_keys=True,
                                     separators=(',', ':'), ensure_ascii=False).encode())
    control_binding = next(p for p in projection['projections']
                           if p['path'] == 'controls/index.v2.json')
    require(control_hash == control_binding['semantic_content_sha256'],
            'Authored control labels, rationales or bindings changed')
    require(len(controls) == 39 and len({c['control_id'] for c in controls}) == 39,
            'Expected 39 distinct authored controls')
    checked = []
    for control in controls:
        result = check_response(regular_file(control['response_file']).decode('utf-8'),
                                control['case_id'])
        require(result['interface_valid'] == control['expected_interface_valid'],
                control['control_id'] + ' interface expectation')
        require(result['semantic_adequacy'] is None, 'No mechanical semantic judgment')
        require(control['expected_semantic_adequacy'] == (
            'inadequate' if control['kind'] == 'negative' else 'adequate'),
            control['control_id'] + ' authored-label consistency')
        checked.append({'control_id': control['control_id'],
                        'interface_valid': result['interface_valid'],
                        'semantic_adequacy': None})
    for case_id in ids:
        require({c['kind'] for c in controls if c['case_id'] == case_id} ==
                {'positive', 'equivalent', 'negative'}, case_id + ' control coverage')
    reviews = load('provenance/review-projections.json')
    require({r['reviewer_label'] for r in reviews['reviewers']} == {'A', 'B'},
            'Two named review projections')
    for review in reviews['reviewers']:
        require(review['reviewed_manifest_sha256'] == projection['original_source_freeze_manifest_sha256'],
                'Review must bind original freeze')
        require(review['verdict'] == 'approved_as_authored_contract_regression' and
                review['authored_controls_reviewed'] == 39, 'Authored review status')
    plan = load('provenance/prospective-inputs.json')
    require(len(plan['candidate_order']) == len(set(plan['candidate_order'])) == 10,
            'Ten-candidate scope')
    require(plan['model_trials_run'] == 0, 'Prospective recipe is unrun')
    prompts = []
    addition = b'\nADDITIONAL ROUTING ENTRY POINT\n' + regular_file(
        'sources/skill/task-to-skill-router/SKILL.md')
    for case_id in ids:
        baseline, router = assemble(case_id, 'baseline'), assemble(case_id, 'router')
        require(router == baseline + addition, case_id + ' only prospective router addition')
        prompts.append({'case_id': case_id, 'baseline_bytes': len(baseline),
                        'baseline_sha256': digest(baseline), 'router_bytes': len(router),
                        'router_sha256': digest(router), 'shared_prefix_identical': True})
    require(prompts == plan['prospective_prompt_hashes'], 'Prospective recipe hashes differ')
    missing = set()
    for entry in source['sources']:
        file = ROOT / entry['local_path']
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)',
                                 file.read_text(encoding='utf-8')):
            parsed = urlsplit(target)
            if not parsed.scheme and not parsed.netloc and not (file.parent / parsed.path).exists():
                missing.add((entry['local_path'], target))
    omitted = load('provenance/omitted-links.json')['omitted_links']
    require(len(omitted) == 34 and missing == {(e['source'], e['target']) for e in omitted},
            'Exact omitted-reference mapping differs')
    return {'status': 'passed' if not errors else 'failed', 'errors': errors,
            'kind': 'Authored regression byte, source-binding and interface checks only',
            'public_manifest_sha256': digest(manifest_raw),
            'manifest_files_checked': len(entries), 'cases': len(ids),
            'authored_controls_checked': checked, 'semantic_grading_run': False,
            'model_trials_run': 0, 'prospective_input_hashes_checked': 24,
            'completed_exact_v2_author_reviews': 2,
            'review_evidence_limit': 'Public projections preserve original hashes, not original review transcripts.',
            'scope': 'No scenario execution, network access, subprocesses, model calls or filesystem writes.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', help='Optional externally retained public manifest digest')
    parser.add_argument('--response', type=Path, help='Read one saved response; never grade its semantics')
    parser.add_argument('--case', choices=[f'R{i:02}' for i in range(1, 13)])
    args = parser.parse_args()
    if args.response and not args.case:
        parser.error('--response requires --case')
    if args.case and not args.response:
        parser.error('--case requires --response')
    try:
        report = verify(args.manifest_sha256)
        if report['status'] == 'passed' and args.response:
            report['response_check'] = check_response(args.response.read_text(encoding='utf-8'), args.case)
            if not report['response_check']['interface_valid']:
                report['status'] = 'failed'
        print(json.dumps(report, indent=2))
        return 0 if report['status'] == 'passed' else 1
    except (OSError, ValueError, KeyError, TypeError, StopIteration) as error:
        print(json.dumps({'status': 'failed', 'error': str(error),
                          'semantic_grading_run': False, 'model_trials_run': 0}, indent=2))
        return 1


if __name__ == '__main__':
    sys.exit(main())
