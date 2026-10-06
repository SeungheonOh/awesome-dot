#!/usr/bin/env python3
"""Verify published bytes and recompute saved-result accounting; never execute artifacts.

Use: python -I -B reproduce_saved_evidence.py
Only Python standard-library JSON, hashes, file reads and arithmetic are used.
No grader import, candidate execution, SQLite execution, model calls, network or writes.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATUSES = ('pass', 'fail', 'not_assessed')

def path(relative):
    p = ROOT / relative
    assert not p.is_symlink(), ('symlink', relative)
    p = p.resolve()
    assert p.is_relative_to(ROOT), ('path escape', relative)
    assert p.is_file(), ('missing regular file', relative)
    return p

def digest(relative):
    return hashlib.sha256(path(relative).read_bytes()).hexdigest()

def read(relative):
    return json.loads(path(relative).read_text())

def normalize(status):
    return 'not_assessed' if status in ('unknown', 'not-assessed') else status

def counts(requirements):
    return {s: sum(r['status'] == s for r in requirements) for s in STATUSES}

def verify():
    manifest = read('MANIFEST.json')
    for f in manifest['files']:
        assert digest(f['path']) == f['sha256'], ('manifest hash', f['path'])
        assert path(f['path']).stat().st_size == f['bytes'], ('manifest size', f['path'])
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    assert actual == {f['path'] for f in manifest['files']} | {'MANIFEST.json'}, 'unexpected or absent file'
    source_bindings = read('provenance/source-bindings.json')['files']
    for f in source_bindings:
        if f['treatment'] == 'byte-identical':
            assert digest(f['path']) == f['sha256'], ('original binding', f['path'])
    for guide in read('provenance/packages.json')['files']:
        name = 'guides/' + guide['path']
        b = path(name).read_bytes()
        assert digest(name) == guide['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == guide['git_blob_sha']
    rows = read('results/attempts.json')
    definitions = read('results/requirements.json')
    summary = read('results/summary.json')
    schedule = read('methods/schedule.json')['attempts']
    assert len(rows) == len(schedule) == 24
    assert len({r['attempt_id'] for r in rows}) == 24
    assert sum(len(c['requirements']) for c in definitions.values()) == 53
    assert sum(r['scheduled_requirements'] for r in rows) == 318
    assert sum(len(r['artifacts']) for r in rows) == 45
    schedule_by_id = {a['attempt_id']: a for a in schedule}
    reviewed_ids = set()
    sem = {r['attempt_id']: r for r in read('evidence/semantic/index.json')['review_bindings']}
    for r in rows:
        aid, case = r['attempt_id'], r['case_id']
        sch = schedule_by_id[aid]
        assert (r['condition'], r['repeat'], r['dispatch_index']) == (sch['arm'], sch['repeat'], sch['dispatch_index'])
        assert r['process_integrity'] == 'unknown'
        assert r['counts'] == counts(r['requirements'])
        assert r['completed_criteria'] == (r['counts']['pass'] == r['scheduled_requirements'])
        assert r['scheduled_requirements'] == len(definitions[case]['requirements'])
        receipt = read(r['receipt_path'])
        assert receipt['status'] == r['submission_status']
        assert receipt['artifacts'] == r['artifacts']
        artifact_hashes = {}
        for a in r['artifacts']:
            assert digest(a['path']) == a['sha256'], ('artifact binding', aid, a['path'])
            assert path(a['path']).stat().st_size == a['bytes']
            artifact_hashes[Path(a['path']).name] = a['sha256']
        ep = r['requirements'][0]['evidence_path']
        raw = read(ep)
        checks = raw['checks']
        if isinstance(checks, list):
            checks = {c['id']: c for c in checks}
        assert set(checks) == {d['requirement_id'] for d in definitions[case]['requirements']}
        for requirement, definition in zip(r['requirements'], definitions[case]['requirements']):
            assert all(requirement[k] == v for k,v in definition.items())
            assert requirement['evidence_path'] == ep
            assert requirement['status'] == normalize(checks[requirement['requirement_id']]['status'])
        if case in ('R1','R2'):
            assert raw['artifact_sha256'] == artifact_hashes
            obj = read(f'evidence/objective/{aid}/raw.json')
            for d in definitions[case]['requirements']:
                if d['mode']=='objective':
                    assert checks[d['requirement_id']]['status'] == obj['checks'][d['requirement_id']]['status']
            binding = sem[aid]
            packet = read(binding['packet_manifest_path'])
            assert packet['artifact_sha256'] == artifact_hashes
            assert set(packet['packet_sha256']) == set(binding['packet_file_mapping']) | set(binding.get('omitted_packet_handoffs', {}))
            for old, public in binding['packet_file_mapping'].items():
                assert digest(public) == packet['packet_sha256'][old]
            for old, omitted in binding.get('omitted_packet_handoffs', {}).items():
                assert old == 'README.txt' and omitted['sha256'] == packet['packet_sha256'][old]
            reviews=[]
            for b in binding['reviews']:
                review=read(b['path'])
                assert digest(b['path']) == b['sha256']
                assert review['reviewer_id'] == b['reviewer_id']
                assert b['reviewer_id'] not in reviewed_ids
                reviewed_ids.add(b['reviewer_id'])
                assert review['condition_masked'] is True and review['independent'] is True
                assert review['artifact_sha256'] == artifact_hashes
                reviews.append(review)
            assert len(reviews)==2
            for d in definitions[case]['requirements']:
                if d['mode']!='semantic': continue
                cid=d['requirement_id']
                votes=[review['checks'][cid] for review in reviews]
                assert all(v['rationale'].strip() for v in votes)
                statuses=[normalize(v['status']) for v in votes]
                expected=statuses[0] if statuses[0]==statuses[1] else 'not_assessed'
                assert normalize(checks[cid]['status'])==expected
                assert checks[cid]['reviews']==votes
        elif case=='R3':
            assert raw['source_sha256']==artifact_hashes['report.sql']
        elif case=='R4':
            behavior=read(f'evidence/behavioral/{aid}/behavioral_report.json')
            assert behavior['source_sha256']==artifact_hashes['merge_workspace.py']
            assert behavior['behavior']['checks']==raw['checks']
            assert behavior['returncode']==0 and behavior['execution_status']=='finished'
    assert len(reviewed_ids)==24
    pairs=[]
    case_results=[]
    for case, defs in definitions.items():
        cs={'case_id':case,'label':defs['label'],'requirements_per_attempt':len(defs['requirements']),'conditions':{}}
        for arm in ('C','S'):
            rr=sorted((r for r in rows if r['case_id']==case and r['condition']==arm),key=lambda r:r['repeat'])
            assert [r['repeat'] for r in rr]==[1,2,3]
            cs['conditions'][arm]={'repeats':[{'repeat':r['repeat'],'attempt_id':r['attempt_id'],'counts':r['counts'],'completed_criteria':r['completed_criteria']} for r in rr],'counts':{s:sum(r['counts'][s] for r in rr) for s in STATUSES},'scheduled_requirements':sum(r['scheduled_requirements'] for r in rr),'complete_attempts':sum(r['completed_criteria'] for r in rr),'failed_requirements':sorted({x['requirement_id'] for r in rr for x in r['requirements'] if x['status']=='fail'}),'not_assessed_requirements':sorted({x['requirement_id'] for r in rr for x in r['requirements'] if x['status']=='not_assessed'})}
        for repeat in (1,2,3):
            rr={r['condition']:r for r in rows if r['case_id']==case and r['repeat']==repeat}
            pairs.append({'case_id':case,'repeat':repeat,'C':{'attempt_id':rr['C']['attempt_id'],**rr['C']['counts']},'S':{'attempt_id':rr['S']['attempt_id'],**rr['S']['counts']},'scheduled_requirements_per_condition':len(defs['requirements']),'verified_pass_difference_S_minus_C':rr['S']['counts']['pass']-rr['C']['counts']['pass']})
        cs['three_repeat_pass_difference_S_minus_C']=cs['conditions']['S']['counts']['pass']-cs['conditions']['C']['counts']['pass']
        case_results.append(cs)
    assert case_results==summary['cases']
    assert pairs==read('results/pairs.json')==summary['pairs']
    for arm in ('C','S'):
        rr=[r for r in rows if r['condition']==arm]
        expected={'counts':{s:sum(r['counts'][s] for r in rr) for s in STATUSES},'scheduled_requirements':sum(r['scheduled_requirements'] for r in rr),'complete_attempts':sum(r['completed_criteria'] for r in rr),'attempts':len(rr),'equal_case_mean_verified_fraction':sum(c['conditions'][arm]['counts']['pass']/c['conditions'][arm]['scheduled_requirements'] for c in case_results)/len(case_results)}
        assert expected==summary['conditions'][arm]
    coverage={mode:{s:sum(x['status']==s for r in rows for x in r['requirements'] if x['mode']==mode) for s in STATUSES} for mode in ('objective','semantic','behavioral')}
    assert coverage==summary['evidence_coverage']
    return {'verified_public_files':len(manifest['files']),'attempts':len(rows),'authored_cases':len(definitions),'scheduled_requirement_instances':318,'conditions':summary['conditions'],'evidence_coverage':coverage,'process_integrity':'unknown','candidate_code_executed':False,'model_runs_launched':0,'meaning':'Saved-evidence consistency verified; no independent model rerun or semantic re-review'}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
