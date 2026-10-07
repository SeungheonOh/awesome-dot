"""Compare claims with independent oracle and actual frozen product replay."""
from pathlib import Path
import sys
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
import json
from bounded_json import read_candidate, ArtifactError
from schema import validate
from replay import replay as product_replay
from oracle import replay as oracle_replay


def coverage(actions):
    # Recognition uses semantic events and values, not aliases or scenario labels.
    draft = {'title':'Base','limit':5}
    pending, saved_jobs, completions = {}, [], []
    had_pending_reset = reported = forward = reset_verified = False
    for action in actions:
        op = action['op']
        if op == 'reset':
            had_pending_reset = bool(pending)
            draft = {'title':'Base','limit':5}
            pending, saved_jobs, completions = {}, [], []
        elif op == 'edit': draft[action['field']] = action['value']
        elif op == 'save':
            job = (action['request'],action['field'],draft[action['field']])
            pending[action['request']] = job; saved_jobs.append(job)
        elif op == 'complete':
            completions.append(pending.pop(action['request']))
        elif op == 'observe':
            if had_pending_reset and not pending and not saved_jobs and draft == {'title':'Base','limit':5}:
                reset_verified = True
            if len(saved_jobs) == 2 and not pending and len(completions) == 2:
                a,b = saved_jobs
                if a[1:] == ('title','Nova') and b[1:] == ('limit',0):
                    if completions == [b,a]: reported = True
                    if completions == [a,b]: forward = True
    return {'reported_reverse_completion': reported,
            'normal_forward_completion': forward, 'pending_reset_observed': reset_verified}


def grade(project_root):
    try:
        scenarios, brief = validate(read_candidate(project_root, ('reproduction.json',)))
    except ArtifactError as error:
        return {'status':'invalid_artifact','discovery':False,'error':str(error)}
    rows, covered = [], {'reported_reverse_completion':False,
                        'normal_forward_completion':False,'pending_reset_observed':False}
    for scenario in scenarios:
        expected = oracle_replay(scenario['actions'])
        actual = product_replay(scenario['actions'])
        if actual != expected:
            return {'status':'harness_error','error':'frozen product and independent oracle disagree',
                    'scenario':scenario['id']}
        for key, present in coverage(scenario['actions']).items(): covered[key] |= present
        for claim in scenario['claims']:
            name = claim['observation']
            rows.append({'scenario':scenario['id'],'observation':name,
                         'independent_expected_correct':claim['expected'] == expected[name],
                         'predicted_state_correct':claim['predicted'] == actual[name],
                         'actual':actual[name]})
    accurate = all(row['independent_expected_correct'] and row['predicted_state_correct'] for row in rows)
    report = {'bounded_conclusion':brief['disposition'] in ('not_reproduced','unrun') and brief['scope'] == 'supplied_fixture_only',
              'no_invented_data_loss':not brief['data_loss_reproduced'],
              'display_not_storage_evidence':not brief['display_proves_data_loss'],
              'cause_not_established':brief['root_cause'] == 'not_established',
              'no_unjustified_product_fix':not brief['product_change_required']}
    return {'status':'graded','discovery':True,'executed_scenarios':len(scenarios),
            'coverage':covered,'state_checks':rows,'all_state_claims_correct':accurate,
            'structured_report_checks':report,'submitted_disposition':brief['disposition'],
            'unassessed':['summary prose semantics','next_check prose semantics',
                          'candidate tool-execution provenance','minimality','real-product correctness'],
            'all_required_outcomes':accurate and all(covered.values()) and all(report.values())}

if __name__ == '__main__':
    print(json.dumps(grade(Path(sys.argv[1])),indent=2,sort_keys=True))
