#!/usr/bin/env python3
"""F4 objective integrity/length checks plus explicit blinded review aggregation.

No inference of semantic correctness is performed by this program.
"""
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASE_ID = 'F4'
MAX_WORDS = 500


def digest(data):
    return hashlib.sha256(data).hexdigest()


def assertion(ident, passed, reason, kind='objective'):
    return {'id': ident, 'passed': passed, 'reason': reason, 'kind': kind}


def combine(values):
    if any(value is False for value in values):
        return False
    if any(value is None for value in values):
        return None
    return True


def validate_semantic(record, required, report_hash):
    """Validate review provenance and structure, never prose semantics."""
    if not isinstance(record, dict) or record.get('case_id') != CASE_ID:
        raise ValueError('semantic record must identify case_id F4')
    if record.get('submission_sha256') != report_hash:
        raise ValueError('semantic record SHA-256 does not match decision-brief.txt')
    supplied_groups = record.get('groups')
    if not isinstance(supplied_groups, list):
        raise ValueError('semantic groups must be a list')
    if any(not isinstance(group, dict) for group in supplied_groups):
        raise ValueError('every semantic group must be an object')
    group_ids = [group.get('id') for group in supplied_groups]
    expected_ids = [group['id'] for group in required['groups']]
    if len(group_ids) != len(expected_ids) or set(group_ids) != set(expected_ids):
        raise ValueError('semantic group IDs must be exactly g1 through g5, once each')
    by_group = {group['id']: group for group in supplied_groups}
    normalized = {}
    for expected_group in required['groups']:
        gid = expected_group['id']
        supplied = by_group[gid].get('assertions')
        if not isinstance(supplied, list) or any(not isinstance(item, dict) for item in supplied):
            raise ValueError(gid + ' assertions must be a list of objects')
        got_ids = [item.get('id') for item in supplied]
        expected_assertions = [item['id'] for item in expected_group['assertions']]
        if len(got_ids) != len(expected_assertions) or set(got_ids) != set(expected_assertions):
            raise ValueError(gid + ' must include each frozen assertion ID exactly once')
        by_id = {item['id']: item for item in supplied}
        normalized[gid] = []
        for ident in expected_assertions:
            item = by_id[ident]
            if 'passed' not in item or not (item['passed'] is None or type(item['passed']) is bool):
                raise ValueError(ident + ' passed must be true, false, or null')
            reason = item.get('reason', '')
            if not isinstance(reason, str) or (item['passed'] is not None and not reason.strip()):
                raise ValueError(ident + ' scored assertions require a nonempty reason')
            normalized[gid].append(assertion(ident, item['passed'], reason or 'Blinded semantic review pending.', 'semantic'))
    return normalized


def grade(packet, submission, semantic_path=None):
    packet, submission = Path(packet), Path(submission)
    frozen = json.loads((HERE/'frozen-packet-manifest.json').read_text(encoding='utf-8'))
    required = json.loads((HERE/'semantic-criteria.json').read_text(encoding='utf-8'))
    checks = []
    expected = {item['path']: item for item in frozen['files']}
    packet_exists = packet.is_dir() and not packet.is_symlink()
    checks.append(assertion('packet.directory', packet_exists, 'Packet must be an existing ordinary directory.'))
    actual = set()
    symlinks = []
    if packet_exists:
        for item in packet.rglob('*'):
            relative = str(item.relative_to(packet))
            if item.is_symlink():
                symlinks.append(relative)
            if item.is_file() or item.is_symlink():
                actual.add(relative)
    checks.append(assertion('packet.inventory', actual == set(expected),
        'Exact protected file inventory; missing=' + repr(sorted(set(expected)-actual)) + '; extra=' + repr(sorted(actual-set(expected)))))
    checks.append(assertion('packet.no_symlinks', not symlinks, 'Protected packet symlinks: ' + repr(symlinks)))
    for name, entry in expected.items():
        path = packet/name
        try:
            if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != packet.parent):
                raise ValueError('symlink in protected source path')
            data = path.read_bytes()
            passed = digest(data) == entry['sha256'] and len(data) == entry['bytes']
            reason = 'Frozen SHA-256 and byte count ' + ('match.' if passed else 'do not match.')
        except (OSError, ValueError) as exc:
            passed, reason = False, 'Cannot verify protected source: ' + str(exc)
        checks.append(assertion('source.' + name, passed, reason))
    try:
        supplied_manifest = json.loads((packet/'input-manifest.json').read_text(encoding='utf-8'))
        if not isinstance(supplied_manifest, dict):
            raise ValueError('input-manifest top level must be an object')
        expected_inputs = [entry for name, entry in expected.items() if name.startswith('inputs/')]
        manifest_ok = (supplied_manifest.get('case_id') == CASE_ID and supplied_manifest.get('algorithm') == 'sha256'
            and supplied_manifest.get('inputs') == expected_inputs)
        checks.append(assertion('packet.input_manifest', manifest_ok, 'Input manifest must match the evaluator-frozen source list, exact hashes, and byte counts.'))
    except (OSError, ValueError, TypeError) as exc:
        checks.append(assertion('packet.input_manifest', False, 'Cannot validate input manifest: ' + str(exc)))

    report_path = submission/'decision-brief.txt'
    report_hash = None
    report_text = None
    try:
        if report_path.is_symlink() or not report_path.is_file():
            raise ValueError('report is missing or is not a regular file')
        data = report_path.read_bytes()
        report_hash = digest(data)
        report_text = data.decode('utf-8')
        if not report_text.strip():
            raise ValueError('report is empty or only whitespace')
        checks.append(assertion('submission.report', True, 'Nonempty UTF-8 regular decision-brief.txt is present. SHA-256=' + report_hash))
    except (OSError, UnicodeError, ValueError) as exc:
        checks.append(assertion('submission.report', False, 'Invalid report: ' + str(exc)))

    semantic = {group['id']: [assertion(item['id'], None, 'Blinded semantic review pending.', 'semantic')
                for item in group['assertions']] for group in required['groups']}
    if semantic_path is not None:
        try:
            if report_hash is None:
                raise ValueError('cannot bind semantic record without a readable report')
            review = json.loads(Path(semantic_path).read_text(encoding='utf-8'))
            semantic = validate_semantic(review, required, report_hash)
            checks.append(assertion('review.valid_record', True, 'Semantic IDs, value types, reasons, and report-hash binding are valid; this is not independent validation of the assigned scores.'))
        except (OSError, ValueError, TypeError, KeyError) as exc:
            checks.append(assertion('review.valid_record', False, 'Invalid semantic record: ' + str(exc)))

    word_count = len(report_text.split()) if report_text is not None else None
    word_pass = word_count <= MAX_WORDS if word_count is not None else None
    groups = []
    for group in required['groups']:
        gid = group['id']
        assertions = semantic[gid]
        if gid == 'g5':
            assertions = assertions + [assertion('g5.words', word_pass,
                ('Whitespace word count is ' + str(word_count) + '; maximum is 500.') if word_count is not None else 'Word count unavailable because the report is unreadable.')]
        groups.append({'id': gid, 'passed': combine([item['passed'] for item in assertions]), 'assertions': assertions})
    integrity = {'passed': all(item['passed'] is True for item in checks), 'assertions': checks}
    accepted = combine([integrity['passed']] + [group['passed'] for group in groups])
    return {'case_id': CASE_ID, 'integrity': integrity, 'groups': groups, 'accepted': accepted,
            'quality': {'passed_groups': sum(group['passed'] is True for group in groups),
                        'scored_groups': sum(group['passed'] is not None for group in groups), 'total_groups': 5}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet', required=True, type=Path)
    parser.add_argument('--submission', required=True, type=Path)
    parser.add_argument('--semantic', type=Path, help='Optional blinded assertion scores JSON; absent means pending review.')
    parser.add_argument('--out', required=True, type=Path)
    args = parser.parse_args()
    report = grade(args.packet, args.submission, args.semantic)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(json.dumps({'case_id': report['case_id'], 'integrity_passed': report['integrity']['passed'],
                      'accepted': report['accepted'], 'quality': report['quality']}, sort_keys=True))


if __name__ == '__main__':
    main()
