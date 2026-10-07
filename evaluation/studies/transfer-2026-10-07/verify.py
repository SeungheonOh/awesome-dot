#!/usr/bin/env python3
"""Bounded saved-evidence accounting. Never executes SQL, candidates or graders."""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys

MAX_FILES = 256
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_TOTAL_BYTES = 8 * 1024 * 1024
SLOTS = tuple(f't{c}-r{r}-{a}' for c in (1, 2) for r in (1, 2, 3) for a in ('c', 's'))
CHECKS = {
    'T1': {'execution', 'schema_types', 'cohort', 'charge_observed', 'credit_observed',
           'charge_total', 'credit_total', 'net', 'scope_parameters', 'population_controls',
           'partition_net', 'feed_controls', 'exceptions', 'unknowns'},
    'T2': {f'T2-{i:02d}' for i in range(1, 13)},
}
ARTIFACTS = {'T1': {'report.sql', 'reconciliation.json'},
             'T2': {'action_register.json', 'handoff.txt'}}

class Invalid(ValueError):
    pass

def require(ok, message):
    if not ok:
        raise Invalid(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def unique(pairs):
    out = {}
    for k, v in pairs:
        require(k not in out, 'duplicate JSON key')
        out[k] = v
    return out

def decode(data):
    def bad(_):
        raise Invalid('nonfinite JSON number')
    def finite_float(s):
        import math
        value = float(s)
        require(math.isfinite(value), 'nonfinite JSON number')
        return value
    return json.loads(data.decode('utf-8'), object_pairs_hook=unique,
                      parse_constant=bad, parse_float=finite_float)

def safe_name(name):
    require(isinstance(name, str) and bool(name), 'invalid path')
    p = PurePosixPath(name)
    require(not p.is_absolute() and str(p) == name and '\\' not in name,
            'nonportable or unsafe path')
    require(all(x not in ('', '.', '..') for x in p.parts), 'unsafe path component')
    require(not any(ord(c) < 32 for c in name), 'control character in path')
    return p.parts

def read_regular(root, name):
    parts = safe_name(name)
    p = root
    for index, part in enumerate(parts):
        p = p / part
        st = p.lstat()
        if index + 1 < len(parts):
            require(stat.S_ISDIR(st.st_mode), 'non-directory path component')
        else:
            require(stat.S_ISREG(st.st_mode) and st.st_nlink == 1, 'unsafe file')
            require(st.st_size <= MAX_FILE_BYTES, 'oversize file')
    with p.open('rb') as handle:
        data = handle.read(MAX_FILE_BYTES + 1)
    require(len(data) <= MAX_FILE_BYTES, 'oversize read')
    after = p.lstat()
    require((st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'file changed during read')
    return data

def inventory(root, expected_hash=None):
    require(root.is_dir() and not root.is_symlink(), 'unsafe package root')
    raw = read_regular(root, 'MANIFEST.json')
    if expected_hash is not None:
        require(re.fullmatch('[0-9a-f]{64}', expected_hash) is not None, 'invalid external digest')
        require(sha(raw) == expected_hash, 'external manifest digest mismatch')
    manifest = decode(raw)
    require(manifest['schema'] == 'transfer-saved-evidence-v1', 'unexpected manifest schema')
    entries = manifest['files']
    require(isinstance(entries, dict) and 0 < len(entries) <= MAX_FILES, 'file count bound')
    require('MANIFEST.json' not in entries, 'manifest cannot include itself')
    seen = set()
    count = 0
    for p in root.rglob('*'):
        count += 1
        require(count <= 4 * MAX_FILES, 'tree size bound')
        require(not p.is_symlink(), 'symlink in package')
        if p.is_dir():
            continue
        require(p.is_file(), 'nonregular package entry')
        seen.add(p.relative_to(root).as_posix())
    require(seen == set(entries) | {'MANIFEST.json'}, 'package inventory mismatch')
    blobs = {}
    total = 0
    for name, entry in entries.items():
        data = read_regular(root, name)
        total += len(data)
        require(total <= MAX_TOTAL_BYTES, 'total byte bound')
        require(entry == {'bytes': len(data), 'sha256': sha(data)}, 'file hash or size mismatch: ' + name)
        blobs[name] = data
    return blobs, sha(raw)

def raw_checks(row):
    raw = row['raw_grade']['checks']
    return {x['id']: x for x in raw} if isinstance(raw, list) else raw

def metrics(rows):
    out = {'case_condition': {}, 'equal_case_mean_verified_fraction': {},
           'not_efficacy_evidence': True, 'paired_S_minus_C': [],
           'planned_requirement_checks': 156, 'planned_submissions': 12}
    for case in ('T1', 'T2'):
        out['case_condition'][case] = {}
        for arm in ('C', 'S'):
            subset = [r for r in rows if r['case'] == case and r['condition'] == arm]
            totals = {k: sum(r[k] for r in subset) for k in ('passed', 'failed', 'unknown', 'scheduled')}
            totals.update(planned_submissions=3, all_met=sum(r['all_met'] for r in subset))
            totals['verified_fraction'] = totals['passed'] / totals['scheduled']
            out['case_condition'][case][arm] = totals
    for arm in ('C', 'S'):
        out['equal_case_mean_verified_fraction'][arm] = sum(
            out['case_condition'][c][arm]['verified_fraction'] for c in ('T1', 'T2')) / 2
    for case in ('T1', 'T2'):
        for repeat in (1, 2, 3):
            pair = {r['condition']: r for r in rows if r['case'] == case and r['repeat'] == repeat}
            out['paired_S_minus_C'].append({'case': case, 'repeat': repeat,
                'both_graded': all(r['grade_status'] == 'graded' for r in pair.values()),
                'verified_fraction_difference': pair['S']['passed'] / pair['S']['scheduled'] -
                                                pair['C']['passed'] / pair['C']['scheduled']})
    return out

def validate_rows(result, blobs):
    rows = result['rows']
    require(len(rows) == 12 and {r['slot_id'] for r in rows} == set(SLOTS), 'planned slots mismatch')
    for row in rows:
        case, repeat, arm = row['slot_id'].split('-')
        require((row['case'], row['repeat'], row['condition']) == (case.upper(), int(repeat[1:]), arm.upper()), 'slot identity mismatch')
        require(row['grade_status'] == 'graded' and row['operational_status'] == 'final_on_time', 'saved outcome mismatch')
        require(set(row['checks']) == CHECKS[row['case']], 'requirement inventory mismatch')
        require(row['checks'] == raw_checks(row), 'raw status mismatch')
        counts = Counter(v['status'] for v in row['checks'].values())
        require(set(counts) <= {'pass', 'fail', 'unknown'}, 'invalid status')
        for name, status in [('passed', 'pass'), ('failed', 'fail'), ('unknown', 'unknown')]:
            require(type(row[name]) is int and row[name] == counts[status], 'status count mismatch')
        require(row['scheduled'] == len(CHECKS[row['case']]), 'denominator mismatch')
        require(row['all_met'] is (counts['pass'] == row['scheduled']), 'all-met mismatch')
        require(row['input_integrity'] == {'issues': [], 'unchanged': True}, 'input integrity mismatch')
        raw = row['raw_grade']
        if row['case'] == 'T1':
            require(raw['totals'] == {s: counts[s] for s in ('pass', 'fail', 'unknown')}, 'raw totals mismatch')
        else:
            require(raw['objective'] == {'passed': counts['pass'], 'failed': counts['fail'],
                                         'unknown': counts['unknown'], 'total': 12}, 'raw totals mismatch')
            require(raw['all_requirements_met'] is row['all_met'], 'raw all-met mismatch')
            require(raw['semantic_prose_quality'] == 'not_scored', 'prose scope mismatch')
        require(set(row['raw_artifacts']) == ARTIFACTS[row['case']], 'artifact inventory mismatch')
        for name, meta in row['raw_artifacts'].items():
            data = blobs['outputs/' + row['slot_id'] + '/' + name]
            require(meta == {'bytes': len(data), 'capture': 'captured', 'sha256': sha(data)}, 'artifact hash mismatch')
            require(raw['artifact_sha256'][name] == sha(data), 'raw artifact hash mismatch')
        saved = decode(blobs['evidence/results/' + row['slot_id'] + '.json'])
        require(saved == row, 'individual result mismatch')
        stdout = decode(blobs['evidence/grading/' + row['slot_id'] + '/stdout.json'])
        require(stdout == raw, 'saved scorer stdout mismatch')
        process = decode(blobs['evidence/grading/' + row['slot_id'] + '/process.json'])
        require(process['returncode'] == 0 and process['timeout'] is False, 'grader process mismatch')
        require(process['stdout_sha256'] == sha(blobs['evidence/grading/' + row['slot_id'] + '/stdout.json']), 'stdout hash mismatch')
        require(process['stderr_sha256'] == sha(blobs['evidence/grading/' + row['slot_id'] + '/stderr.txt']), 'stderr hash mismatch')
    require(result['summary'] == metrics(rows), 'summary mismatch')
    require(sum(r['passed'] for r in rows) == 156 and all(r['all_met'] for r in rows), 'frozen ceiling outcome mismatch')
    return rows

def dt(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00'))

def verify_blobs(blobs):
    result = decode(blobs['evidence/results.json'])
    rows = validate_rows(result, blobs)
    accounting = decode(blobs['evidence/accounting-projection.json'])
    require(accounting['source_results_sha256'] == sha(blobs['evidence/results.json']), 'result provenance mismatch')
    require(accounting['planned_submissions'] == 12 and accounting['first_submissions_captured'] == 12, 'completion denominator mismatch')
    for key in ('missing', 'timeouts', 'late', 'grading_infrastructure_errors', 'candidate_feedback_rescues_replacements_or_reruns'):
        require(accounting[key] == 0, 'completion accounting mismatch')
    require(accounting['primary_grading_passes'] == 1, 'grading pass count mismatch')
    arecords = accounting['rows']
    require(len(arecords) == 12 and {r['slot_id'] for r in arecords} == set(SLOTS), 'accounting slots mismatch')
    by_id = {r['slot_id']: r for r in rows}
    collection = decode(blobs['evidence/collection-projection.json'])['rows']
    require(len(collection) == 12 and {r['slot_id'] for r in collection} == set(SLOTS), 'collection slots mismatch')
    collected = {r['slot_id']: r for r in collection}
    for a in arecords:
        row = by_id[a['slot_id']]
        for key in ('case', 'condition', 'repeat', 'operational_status', 'grade_status', 'passed', 'failed', 'unknown', 'scheduled'):
            require(a[key] == row[key], 'accounting/result mismatch')
        ack, deadline, first = map(dt, (a['acknowledgement_observed_at_utc'], a['deadline_utc'], a['first_terminal_observed_at_utc']))
        require((deadline - ack).total_seconds() == 1800 and ack <= first <= deadline, 'observation budget mismatch')
        require(a['artifact_sha256'] == row['raw_grade']['artifact_sha256'], 'accounting artifact mismatch')
        c = collected[a['slot_id']]
        require(c['first_terminal_observed_at_utc'] == a['first_terminal_observed_at_utc'], 'collection time mismatch')
        require(first <= dt(c['capture_started_at_utc']) <= dt(c['capture_finished_at_utc']), 'capture chronology mismatch')
        require(c['artifacts'] == row['raw_artifacts'], 'capture artifacts mismatch')
    for row in rows:
        launch = decode(blobs['evidence/grading/' + row['slot_id'] + '/launch-projection.json'])
        require(dt(launch['started_at_utc']) > max(dt(c['capture_finished_at_utc']) for c in collection), 'grading started before capture closure')
        require(launch['candidate_code_imported'] is False and launch['isolated_python'] is True, 'scorer launch scope mismatch')
    schedule = decode(blobs['evidence/schedule.json'])
    order = [s for w in schedule['waves'] for s in w['dispatch_order']]
    require(order == [a['slot_id'] for a in sorted(arecords, key=lambda a: a['ordinal'])], 'schedule order mismatch')
    for case in ('T1', 'T2'):
        source = blobs[f'cases/{case}/TASK-source.md']
        effective = blobs[f'cases/{case}/TASK-effective.md']
        require(source.count(b'You have 900 seconds.') == 1, 'source budget count mismatch')
        require(source.replace(b'You have 900 seconds.', b'You have 1800 seconds.') == effective, 'task amendment mismatch')
    amendment = decode(blobs['evidence/budget-amendment.json'])
    for change in amendment['changes']:
        case = change['case']
        require(change['source_task_sha256'] == sha(blobs[f'cases/{case}/TASK-source.md']), 'source task hash mismatch')
        require(change['operational_task_sha256'] == sha(blobs[f'cases/{case}/TASK-effective.md']), 'effective task hash mismatch')
    provenance = decode(blobs['evidence/copied-byte-allowlist.json'])
    require(len({x['public_path'] for x in provenance['files']}) == len(provenance['files']), 'duplicate allowlist path')
    for item in provenance['files']:
        data = blobs[item['public_path']]
        require(item['sha256'] == sha(data) and item['bytes'] == len(data), 'copied evidence hash mismatch')
    prompts = decode(blobs['evidence/dispatch-hash-projection.json'])['records']
    require(len(prompts) == 12 and {p['slot_id'] for p in prompts} == set(SLOTS), 'dispatch hash slots mismatch')
    deviations = [p for p in prompts if p['intended_frozen_sha256'] != p['observed_dispatch_reconstruction_sha256']]
    require(len(deviations) == 1 and deviations[0]['slot_id'] == 't2-r1-c', 'declared deviation mismatch')
    deviation = decode(blobs['evidence/deviation-projection.json'])
    require(deviation['frozen_prompt_sha256'] == deviations[0]['intended_frozen_sha256'], 'intended deviation hash mismatch')
    require(deviation['actual_prompt_reconstruction_sha256'] == deviations[0]['observed_dispatch_reconstruction_sha256'], 'observed deviation hash mismatch')
    require(deviation['exact_delta'] == {'frozen': 'return a brief final message', 'actual': 'return a brief message'}, 'deviation text mismatch')
    return {'submissions': 12, 'output_files': 24, 'checks': 156, 'pass': 156, 'fail': 0, 'unknown': 0,
            'equal_case_means': {'C': 1.0, 'S': 1.0}, 'paired_differences': [0.0] * 6}

def self_test(blobs):
    """Author-written controls for this verifier, never evaluated-agent outcomes."""
    import copy
    passed = []
    verify_blobs(blobs)
    passed.append('positive_saved_evidence')
    def reject(name, call):
        try:
            call()
        except (Invalid, ValueError, KeyError, TypeError, OSError):
            passed.append(name)
        else:
            raise Invalid('negative control was accepted: ' + name)
    reject('duplicate_json_key', lambda: decode(b'{"a":1,"a":2}'))
    reject('nonfinite_json', lambda: decode(b'{"a":1e999}'))
    for name in ('../escape', '/absolute', 'a/../b', 'a//b', 'a\\b'):
        reject('unsafe_path_' + str(len(passed)), lambda name=name: safe_name(name))
    altered = dict(blobs)
    altered['outputs/t1-r1-c/report.sql'] += b'\n'
    reject('changed_output_byte', lambda: verify_blobs(altered))
    base = decode(blobs['evidence/results.json'])
    for name, mutate in (
        ('missing_slot', lambda r: r['rows'].pop()),
        ('changed_status', lambda r: r['rows'][0]['checks']['execution'].update(status='fail')),
        ('changed_denominator', lambda r: r['rows'][0].update(scheduled=15)),
        ('changed_summary', lambda r: r['summary']['equal_case_mean_verified_fraction'].update(C=0.5)),
    ):
        edited = copy.deepcopy(base)
        mutate(edited)
        changed = dict(blobs, **{'evidence/results.json': json.dumps(edited).encode()})
        reject(name, lambda changed=changed: verify_blobs(changed))
    return {'evidence_type': 'authored verifier controls, not evaluated-agent outcomes',
            'passed': len(passed), 'failed': 0, 'controls': passed}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256', help='independently obtained digest; authenticates this package inventory only')
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    try:
        root = Path(__file__).absolute().parent
        blobs, digest = inventory(root, args.manifest_sha256)
        result = verify_blobs(blobs)
        if args.self_test:
            result['self_tests'] = self_test(blobs)
        result['manifest_sha256'] = digest
        result['external_manifest_digest_checked'] = args.manifest_sha256 is not None
        result['scope'] = 'Saved hashes and accounting only; no candidate, SQL, scorer, or native dispatch execution'
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    except (Invalid, KeyError, TypeError, ValueError, OSError, RecursionError) as exc:
        print('Verification failed: ' + str(exc), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
